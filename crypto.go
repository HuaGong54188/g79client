package g79client

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"math/big"
	"strings"
)

// AES密钥列表
var keys = []string{
	"60F1E0D1FD635362430747215CF1C2FF",
	"EA5B62D27D0338374852C4B9469D7AC6",
	"17238D55501C5F020B155FB3303591E6",
	"8C5CEAE0F443E006A050266F73ADD5B0",
	"1C02CE22FB22F0E72060217418F351F3",
	"9A01773FEBB0CFE0EBDBF37F4D23C27F",
	"43F32300BF252CC320E2572ACE766367",
	"07F161011B3101F1ED0301735631E734",
	"0454E7707A5F37565601E100406060AF",
	"647554BAD3100C43C16660F002CC10F3",
	"E157213170F842382032564265B0B043",
	"914FC59311B04151393EF6896A847636",
	"0710C0205D224237025323265C145FA1",
	"054E6F01165267025C3111F562A921E9",
	"722D1789E792E2CA0D5322211FD0F5AE",
	"91F7C751FCF671F34943430772341799",
}

// 生成随机字符串
func randomString(length int) (string, error) {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	result := make([]byte, length)
	for i := range result {
		num, err := rand.Int(rand.Reader, big.NewInt(int64(len(charset))))
		if err != nil {
			return "", err
		}
		result[i] = charset[num.Int64()]
	}
	return string(result), nil
}

// HTTP加密
func HttpEncrypt(body []byte) ([]byte, error) {
	// 对齐到16字节块并添加16个随机字节
	blockSize := 16
	targetLen := ((len(body) + blockSize + blockSize - 1) / blockSize) * blockSize
	buffer := make([]byte, targetLen)
	copy(buffer, body)

	// 添加16个随机字节
	tailRandom, err := randomString(16)
	if err != nil {
		return nil, err
	}
	copy(buffer[len(body):], []byte(tailRandom))

	// 生成标志位
	highNibble, err := rand.Int(rand.Reader, big.NewInt(15))
	if err != nil {
		return nil, err
	}
	flag := byte((highNibble.Int64() << 4) | 0x0C)

	// 生成IV
	iv, err := randomString(16)
	if err != nil {
		return nil, err
	}
	ivBytes := []byte(iv)

	// 选择密钥
	keyIndex := (flag >> 4) & 0x0F
	keyBytes, err := hex.DecodeString(keys[keyIndex])
	if err != nil {
		return nil, err
	}

	// AES加密
	block, err := aes.NewCipher(keyBytes)
	if err != nil {
		return nil, err
	}

	mode := cipher.NewCBCEncrypter(block, ivBytes)
	cipherText := make([]byte, len(buffer))
	mode.CryptBlocks(cipherText, buffer)

	// 组装结果
	result := make([]byte, 16+len(cipherText)+1)
	copy(result[0:16], ivBytes)
	copy(result[16:16+len(cipherText)], cipherText)
	result[len(result)-1] = flag

	return result, nil
}

// HTTP解密
func HttpDecrypt(payload []byte) ([]byte, error) {
	if len(payload) < 18 {
		return nil, fmt.Errorf("payload too short")
	}

	flag := payload[len(payload)-1]
	iv := payload[0:16]
	cipherText := payload[16 : len(payload)-1]

	keyIndex := (flag >> 4) & 0x0F
	keyBytes, err := hex.DecodeString(keys[keyIndex])
	if err != nil {
		return nil, err
	}

	block, err := aes.NewCipher(keyBytes)
	if err != nil {
		return nil, err
	}

	mode := cipher.NewCBCDecrypter(block, iv)
	plainText := make([]byte, len(cipherText))
	mode.CryptBlocks(plainText, cipherText)

	// 移除尾部的零字节
	lastNonZero := len(plainText) - 1
	for lastNonZero >= 0 && plainText[lastNonZero] == 0 {
		lastNonZero--
	}
	if lastNonZero < 0 {
		return []byte{}, nil
	}

	return plainText[:lastNonZero+1], nil
}

// 计算动态token
func CalculateDynamicToken(path, content, token string) string {
	salt := "0eGsBkhl"

	// 计算token的MD5
	tokenMd5 := fmt.Sprintf("%x", md5.Sum([]byte(token)))

	// 构建payload
	payload := tokenMd5 + content + salt + strings.TrimSuffix(path, "?")

	// 计算payload的MD5
	payloadMd5 := fmt.Sprintf("%x", md5.Sum([]byte(payload)))

	// 转换为二进制字符串
	binaryString := ""
	for _, b := range []byte(payloadMd5) {
		binaryString += fmt.Sprintf("%08b", b)
	}

	// 左移6位
	binaryString = binaryString[6:] + binaryString[:6]

	// 对每个字节进行位反转并异或
	transformed := make([]byte, len(payloadMd5))
	copy(transformed, []byte(payloadMd5))

	for i := 0; i < len(transformed); i++ {
		section := binaryString[i*8 : i*8+8]
		reversedByte := byte(0)
		for j := 0; j < 8; j++ {
			if section[7-j] == '1' {
				reversedByte |= (1 << (j & 0x1F))
			}
		}
		transformed[i] = reversedByte ^ transformed[i]
	}

	// Base64编码并处理
	b64 := base64.StdEncoding.EncodeToString(transformed)
	tokenShort := strings.ReplaceAll(strings.ReplaceAll(b64[:16], "+", "m"), "/", "o") + "1"

	return tokenShort
}

// 获取有效JSON边界
func GetValidJSON(decryptedBody []byte) []byte {
	blocksCount := 0
	readableLength := 0

	for i, b := range decryptedBody {
		switch b {
		case 0x7B: // '{'
			blocksCount++
		case 0x7D: // '}'
			blocksCount--
		}

		if blocksCount == 0 && i != 0 {
			readableLength = i + 1
			break
		}
	}

	if readableLength != 0 {
		return decryptedBody[:readableLength]
	}
	return decryptedBody
}
