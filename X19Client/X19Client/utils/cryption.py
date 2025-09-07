from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random

# Predefined keys after processing
netease_aes_cbc_256_keys = [
    bytes.fromhex(hex_str.translate({ord(c): None for c in ' '}))
    for hex_str in [
        "1C8D9CAD811F2F1E3F7B3B5D208DBE83",
        "96271EAE017F444B342EB8C53AE106BA",
        "6B5FF1292C60237E776923CF4C49ED9A",
        "F020969C883F9C7ADC2C5A130FD1A9CC",
        "607EB25E875E8C9B5C1C5D08648F2D8F",
        "E67D0B4397CCB39C97A78F03315FBE03",
        "3F8F5F7CC35950BF5C9E2B56B20A1F1B",
        "7B8D1D7D674D7D8D917F7D0F2A4D9B48",
        "78289B0C06234B2A2A7D9D7C3C1C1CD3",
        "180928C6AF6C703FBD1A1C8C7EB06C8F",
        "9D2B5D4D0C843E445C4E2A3E19CCCC3F",
        "ED33B9EF6DCC3D2D45428AF516F80A4A",
        "7B6CBC5C215E3E4B7E2F5F5A206823DD",
        "7932137D6A2E1B7E204D6D891ED55D95",
        "0E516BF59BEE9EB6712F5E5D63AC89D2",
        "ED8BBB2D808A0D8F353F3F7B0E486BE5"
    ]
]

# XOR each byte in the keys with 0x7C
netease_aes_cbc_256_keys = [
    bytes([b ^ 0x7C for b in key]) for key in netease_aes_cbc_256_keys
]

def netease_decryption_4o_0xfm_aes_cbc_256(content: str) -> str:
    # Convert content to bytes
    content = bytes.fromhex(content)
    # Extract components from content
    iv = content[:16]
    encrypted_body = content[16:-1]
    key_index_byte = content[-1]
    
    # Calculate key index (upper 4 bits)
    key_index = (key_index_byte >> 4) & 0x0F
    key = netease_aes_cbc_256_keys[key_index]
    
    # AES-CBC-256 decryption
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_body = cipher.decrypt(encrypted_body)
    
    # Find valid JSON boundary
    blocks_count = 0
    readable_length = 0
    for i, byte in enumerate(decrypted_body):
        if byte == 0x7B:  # '{'
            blocks_count += 1
        elif byte == 0x7D:  # '}'
            blocks_count -= 1
        
        if blocks_count == 0 and i != 0:
            readable_length = i + 1
            break
    
    # Extract valid data
    if readable_length != 0:
        valid_data = decrypted_body[:readable_length]
    else:
        valid_data = decrypted_body
    
    # Convert to string and clean up
    return valid_data.decode('utf-8', errors='ignore').strip('\x00').strip()

def netease_encryption_4o_0xfm_aes_cbc_256(plaintext: str) -> str:
    """
    网易AES-CBC-256加密函数
    参数:
        plaintext: 要加密的JSON字符串
    返回:
        加密后的十六进制字符串
    """
    # 1. 准备明文数据
    plain_bytes = plaintext.encode('utf-8')
    
    # 2. 随机选择密钥索引 (0-15)
    key_index = random.randint(0, 15)
    key = netease_aes_cbc_256_keys[key_index]
    
    # 3. 生成随机IV (16字节)
    iv = get_random_bytes(16)
    
    # 4. 应用PKCS7填充
    block_size = AES.block_size
    padding_length = block_size - (len(plain_bytes) % block_size)
    padded_data = plain_bytes + bytes([padding_length] * padding_length)
    
    # 5. 执行AES-CBC-256加密
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded_data)
    
    # 6. 构建完整加密结构
    # 最后一个字节: 高4位存储密钥索引，低4位为0
    key_index_byte = (key_index << 4) & 0xF0
    encrypted_content = iv + ciphertext + bytes([key_index_byte])
    
    # 7. 返回十六进制格式的加密结果
    return encrypted_content.hex().upper()