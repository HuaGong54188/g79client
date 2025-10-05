package g79client

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/google/uuid"
)

// 认证相关结构体
type LoginEntity struct {
	EntityID string `json:"entity_id"`
	Token    string `json:"token"`
	Seed     string `json:"seed"`
}

type LoginResponse struct {
	Response
	Entity LoginEntity `json:"entity"`
}

// {'HostNum': 200, 'ServerHostNum': 8000, 'TempServerStop': 0, 'CdnUrl': 'https://g79.gdl.netease.com/', 'H5VersionUrl': 'https://g79.update.netease.com/cdnversion/obt_h5version.json', 'SeadraUrl': 'https://pub-api.seadra.netease.com', 'HomeServerUrl': 'https://g79mclobthome.minecraft.cn', 'HomeServerGrayUrl': 'https://g79mclobthomegray.nie.netease.com:9443', 'WebServerUrl': 'https://g79mclobt.minecraft.cn', 'WebServerGrayUrl': 'https://g79mclobtgray.nie.netease.com:9443', 'CoreServerUrl': 'https://g79obtapigtcoregray.minecraft.cn', 'CoreServerGrayUrl': 'https://g79obtapigtcoregray.minecraft.cn', 'TransferServerUrl': 'https://g79.update.netease.com/transferserver_obt_new.list', 'TransferServerHttpUrl': 'https://g79transfernew.nie.netease.com', 'TransferServerNewHttpUrl': 'https://g79mcltransfer.minecraft.cn', 'MomentUrl': 'https://x19-pyq.webcgi.163.com/', 'ForumUrl': 'https://mcpel-web.16163.com', 'AuthServerUrl': 'https://g79authobt.minecraft.cn', 'ChatServerUrl': 'https://x19.update.netease.com/chatserver.list', 'PathNUrl': 'https://impression.update.netease.com/lighten/atlas_x19_hangzhou-{isp}.txt', 'PePathNUrl': 'https://impression.update.netease.com/lighten/atlas_g79_hangzhou-{isp}.txt', 'PathNIpv6Url': 'https://impression.update.netease.com/lighten/x19/cnv6.txt', 'PePathNIpv6Url': 'https://impression.update.netease.com/lighten/g79/cnv6.txt', 'LinkServerUrl': 'https://g79.update.netease.com/linkserver_obt.list', 'ApiGatewayUrl': 'https://g79apigatewayobt.minecraft.cn', 'ApiGatewayWeiXinUrl': 'https://g79apigatewayobtweixin.minecraft.cn', 'ApiGatewayGrayUrl': 'https://g79apigatewaygrayobt.nie.netease.com', 'communityHost': 'https://news-api.16163.com/app/g79/api', 'WelfareUrl': 'https://mc.163.com/pe/client/', 'DCWebUrl': 'https://x19apigatewayobt.nie.netease.com', 'RentalTransferUrl': 'https://mcrealms.update.netease.com/isp_map_production.json', 'MgbSdkUrl': 'https://mgbsdk.matrix.netease.com'}
type G79ReleaseJSON struct {
	CoreServerURL            string `json:"CoreServerUrl"`
	AuthServerURL            string `json:"AuthServerUrl"`
	WebServerUrl             string `json:"WebServerUrl"`
	ApiGatewayUrl            string `json:"ApiGatewayUrl"`
	TransferServerUrl        string `json:"TransferServerUrl"`
	TransferServerNewHttpUrl string `json:"TransferServerNewHttpUrl"`
	ChatServerURL            string `json:"ChatServerUrl"`
	LinkServerURL            string `json:"LinkServerUrl"`
}

type X19ReleaseJSON struct {
	CoreServerURL              string `json:"CoreServerUrl"`
	WebServerURL               string `json:"WebServerUrl"`
	WebServerGrayURL           string `json:"WebServerGrayUrl"`
	TransferServerURL          string `json:"TransferServerUrl"`
	TransferServerHTTPURL      string `json:"TransferServerHttpUrl"`
	PeTransferServerURL        string `json:"PeTransferServerUrl"`
	PeTransferServerHTTPURL    string `json:"PeTransferServerHttpUrl"`
	PeTransferServerNewHTTPURL string `json:"PeTransferServerNewHttpUrl"`
	AuthServerURL              string `json:"AuthServerUrl"`
	AuthServerCppURL           string `json:"AuthServerCppUrl"`
	ChatServerURL              string `json:"ChatServerUrl"`
	ApiGatewayURL              string `json:"ApiGatewayUrl"`
	ApiGatewayGrayURL          string `json:"ApiGatewayGrayUrl"`
	DCWebURL                   string `json:"DCWebUrl"`
	RentalTransferURL          string `json:"RentalTransferUrl"`
}

const x19DefaultVersion = "1.15.7.20505"

type PatchInfo struct {
	IOS []string `json:"ios"`
}

// Cookie数据结构
type CookieData struct {
	SauthJSON string `json:"sauth_json"`
}

type SauthData struct {
	GameID         string `json:"gameid"`
	LoginChannel   string `json:"login_channel"`
	AppChannel     string `json:"app_channel"`
	Platform       string `json:"platform"`
	SDKUID         string `json:"sdkuid"`
	SessionID      string `json:"sessionid"`
	SDKVersion     string `json:"sdk_version"`
	UDID           string `json:"udid"`
	DeviceID       string `json:"deviceid"`
	AimInfo        string `json:"aim_info"`
	ClientLoginSN  string `json:"client_login_sn"`
	GasToken       string `json:"gas_token"`
	SourcePlatform string `json:"source_platform"`
	IP             string `json:"ip"`
}

// 使用Cookie进行PE认证
func (c *Client) G79AuthenticateWithCookie(cookieStr string) error {
	// 解析Cookie
	var cookieData CookieData
	err := json.Unmarshal([]byte(cookieStr), &cookieData)
	if err != nil {
		return fmt.Errorf("解析Cookie失败: %v", err)
	}

	var sauthData SauthData
	err = json.Unmarshal([]byte(cookieData.SauthJSON), &sauthData)
	if err != nil {
		return fmt.Errorf("解析SauthJSON失败: %v", err)
	}

	// 执行PE认证
	err = c.g79PerformPEAuthWithCookie(&sauthData)
	if err != nil {
		return fmt.Errorf("PE认证失败: %v", err)
	}

	// 获取用户详情
	userDetail, err := c.GetUserDetail()
	if err != nil {
		return fmt.Errorf("获取用户信息失败: %v", err)
	}

	c.UserDetail = &userDetail.Entity

	return nil
}

// 使用Cookie执行PE认证
func (c *Client) g79PerformPEAuthWithCookie(sauthData *SauthData) error {
	seed := uuid.New().String()
	messagePart := "2b3e7ca013bb30a74d822579860c042b"
	clientLoginSN := "db797f983ca314e00626b9212705d8cc"

	// 使用传入的Cookie数据构建认证数据
	sauthJSON := map[string]any{
		"aim_info":         sauthData.AimInfo,
		"app_channel":      "app_store",
		"client_login_sn":  clientLoginSN,
		"deviceid":         sauthData.DeviceID,
		"gameid":           sauthData.GameID,
		"get_access_token": "1",
		"ip":               sauthData.IP,
		"login_channel":    sauthData.LoginChannel,
		"platform":         "ios",
		"sdk_version":      "5.9.0",
		"sdkuid":           sauthData.SDKUID,
		"sessionid":        sauthData.SessionID,
		"udid":             sauthData.UDID,
	}

	saData := map[string]any{
		"app_channel":   "app_store",
		"app_ver":       c.G79LatestVersion,
		"core_num":      "6",
		"cpu_digit":     "0",
		"cpu_hz":        "",
		"cpu_name":      "",
		"device_height": "2796",
		"device_model":  "iPhone16,2",
		"device_width":  "1290",
		"disk":          "",
		"emulator":      0,
		"first_udid":    sauthData.UDID,
		"is_guest":      0,
		"launcher_type": "PE_C++",
		"mac_addr":      "02:00:00:00:00:00",
		"network":       "--",
		"os_name":       "iOS",
		"os_ver":        "18.1.1",
		"ram":           "8034369536",
		"rom":           "",
		"root":          false,
		"sdk_ver":       "5.9.0",
		"start_type":    "default",
		"udid":          sauthData.UDID,
	}

	saDataJSON, _ := json.Marshal(saData)

	peauth := map[string]any{
		"engine_version": c.EngineVersion,
		"extra_param":    "extra",
		"message":        fmt.Sprintf("%sapple%s%s%s", c.EngineVersion, c.G79LatestVersion, messagePart, seed),
		"patch_version":  c.G79LatestVersion,
		"pay_channel":    "",
		"sa_data":        string(saDataJSON),
		"sauth_json":     sauthJSON,
		"seed":           seed,
		"sign":           "AAAAAAAAAAAAAAAAAAAAAA==",
	}

	// 序列化并加密
	peauthJSON, err := json.Marshal(peauth)
	if err != nil {
		return err
	}

	encryptedPayload, err := G79HttpEncrypt(peauthJSON)
	if err != nil {
		return err
	}

	// 发送认证请求
	req, err := http.NewRequest("POST", c.G79ReleaseJSON.CoreServerURL+"/pe-authentication", strings.NewReader(hex.EncodeToString(encryptedPayload)))
	if err != nil {
		return err
	}

	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, err := readResponseBody(resp)
	if err != nil {
		return err
	}

	// 解密响应
	encryptedResp, err := hex.DecodeString(string(respBody))
	if err != nil {
		return err
	}

	decryptedResp, err := G79HttpDecrypt(encryptedResp)
	if err != nil {
		return err
	}

	validJSON := GetValidJSON(decryptedResp)

	var loginResp LoginResponse
	err = json.Unmarshal(validJSON, &loginResp)
	if err != nil {
		return fmt.Errorf("解析登录响应失败: %v, 响应内容: %s", err, string(validJSON))
	}

	if loginResp.Code != 0 {
		return fmt.Errorf("登录失败 (code: %d): %s", loginResp.Code, loginResp.Message)
	}

	// 设置用户凭证
	c.SetCredentials(loginResp.Entity.EntityID, loginResp.Entity.Token)
	c.Seed = loginResp.Entity.Seed

	return nil
}

type X19LoginOTPResponse struct {
	Response
	Entity X19LoginOTPEntity `json:"entity"`
}

type X19LoginOTPEntity struct {
	OTP          int    `json:"otp"`
	OTPToken     string `json:"otp_token"`
	AID          int    `json:"aid"`
	LockTime     int    `json:"lock_time"`
	OpenOTP      int    `json:"open_otp"`
	VerifyStatus int    `json:"verify_status"`
}

func (c *Client) X19AuthenticateWithCookie(cookieStr string) error {
	// 解析Cookie
	var cookieData CookieData
	err := json.Unmarshal([]byte(cookieStr), &cookieData)
	if err != nil {
		return fmt.Errorf("解析Cookie失败: %v", err)
	}
	// 解析 sauth_json
	var sauthData SauthData
	err = json.Unmarshal([]byte(cookieData.SauthJSON), &sauthData)
	if err != nil {
		return fmt.Errorf("解析 sauth_json 失败: %v", err)
	}

	// 发送认证请求
	req, err := http.NewRequest("POST", c.X19ReleaseJSON.CoreServerURL+"/login-otp", strings.NewReader(cookieStr))
	if err != nil {
		return err
	}

	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, err := readResponseBody(resp)
	if err != nil {
		return err
	}
	var loginResp X19LoginOTPResponse
	if err := json.Unmarshal(respBody, &loginResp); err != nil {
		return fmt.Errorf("解析登录响应失败: %v, 响应内容: %s", err, string(respBody))
	}

	if loginResp.Code != 0 {
		return fmt.Errorf("登录失败 (code: %d): %s", loginResp.Code, loginResp.Message)
	}
	if loginResp.Entity.OTPToken == "" {
		return fmt.Errorf("登录响应缺少 otp_token")
	}

	/*
		var sauthMap map[string]any
		if err := json.Unmarshal([]byte(cookieData.SauthJSON), &sauthMap); err != nil {
			return fmt.Errorf("解析 sauth_json 失败: %v", err)
		}

		getString := func(key string) (string, error) {
			val, ok := sauthMap[key]
			if !ok {
				return "", fmt.Errorf("sauth_json 缺少字段 %s", key)
			}
			str, ok := val.(string)
			if !ok {
				return "", fmt.Errorf("sauth_json 字段 %s 类型错误", key)
			}
			return str, nil
		}

		sdkUID, err := getString("sdkuid")
		if err != nil {
			return err
		}
		sessionID, err := getString("sessionid")
		if err != nil {
			return err
		}
		udid, err := getString("udid")
		if err != nil {
			return err
		}
		deviceID, err := getString("deviceid")
		if err != nil {
			return err
		}
	*/

	saData := map[string]any{
		"os_name":       "windows",
		"os_ver":        "Microsoft Windows 10",
		"mac_addr":      "B8975A4AD616",
		"udid":          "BFEBFBFF000306A9C78C00D8",
		"app_ver":       x19DefaultVersion,
		"sdk_ver":       "",
		"network":       "",
		"disk":          "C78C00D8",
		"is64bit":       "1",
		"video_card1":   "Video_card1",
		"video_card2":   "",
		"video_card3":   "",
		"video_card4":   "",
		"launcher_type": "PC_java",
		"pay_channel":   "4399pc",
		"dotnet_ver":    "4.8.0",
		"cpu_type":      "Intel(R) Xeon(R) CPU i32100 3.10GHz",
		"ram_size":      "8553332736",
		"device_width":  "1920",
		"device_height": "1080",
		"os_detail":     "10",
	}
	saDataJSON, err := json.Marshal(saData)
	if err != nil {
		return fmt.Errorf("序列化 sa_data 失败: %v", err)
	}

	/*
		aimInfo := map[string]string{
			"code_1":  `{"code":"AS","names":{"en":"Asia"}}`,
			"code_2":  `{"iso_code":"CN","names":{"en":"China"}}`,
			"code_3":  `{"iso_code":"51","names":{"en":"Sichuan"}}`,
			"code_4":  `{"id":5101,"names":{"en":"Chengdu"}}`,
			"isp":     `{"id":10086,"names":{"en":""}}`,
			"aim":     "100.100.100.100",
			"country": "CN",
			"tz":      "+0800",
			"tzid":    "",
		}
		aimInfoJSON, err := json.Marshal(aimInfo)
		if err != nil {
			return fmt.Errorf("序列化 aim_info 失败: %v", err)
		}

		saAuthJSON := map[string]any{
			"gameid":        "x19",
			"login_channel": "netease",
			"app_channel":   "netease",
			"platform":      "pc",
			"sdkuid":        sdkUID,
			"sessionid":     sessionID,
			"sdk_version":   "4.10.0",
			"udid":          udid,
			"deviceid":      deviceID,
			"aim_info":     sauthData.AimInfo,
			"client_login_sn": sauthData.ClientLoginSN,
			"gas_token":       sauthData.GasToken,
			"source_platform": "pc",
			"ip":              sauthData.IP,
			"get_access_token": "1",
		}
		saAuthJSONBytes, err := json.Marshal(saAuthJSON)
		if err != nil {
			return fmt.Errorf("序列化 sauth_json 失败: %v", err)
		}
	*/
	authData := map[string]any{
		"sa_data":    string(saDataJSON),
		"sauth_json": cookieData.SauthJSON,
		"version": map[string]any{
			"version":      x19DefaultVersion,
			"launcher_md5": nil,
			"updater_md5":  nil,
		},
		"sdkuid":             nil,
		"aid":                strconv.Itoa(loginResp.Entity.AID),
		"hasMessage":         false,
		"hasGmail":           false,
		"otp_token":          loginResp.Entity.OTPToken,
		"otp_pwd":            nil,
		"lock_time":          loginResp.Entity.LockTime,
		"env":                nil,
		"min_engine_version": nil,
		"min_patch_version":  nil,
		"unisdk_login_json":  nil,
		"verify_status":      loginResp.Entity.VerifyStatus,
		"token":              nil,
		"is_register":        true,
		"entity_id":          nil,
	}

	authPayloadBytes, err := json.Marshal(authData)
	if err != nil {
		return fmt.Errorf("序列化认证载荷失败: %v", err)
	}
	authPayload := string(authPayloadBytes)
	encryptedAuthPayload, err := X19HttpEncrypt(authPayloadBytes)
	if err != nil {
		return fmt.Errorf("加密认证载荷失败: %v", err)
	}
	authReq, err := http.NewRequest("POST", c.X19ReleaseJSON.CoreServerURL+"/authentication-otp", bytes.NewReader(encryptedAuthPayload))
	if err != nil {
		return fmt.Errorf("创建请求失败: %v", err)
	}
	authReq.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	authReq.Header.Set("Accept-Encoding", "gzip")
	authReq.Header.Set("Content-Type", "application/json")
	authReq.Header.Set("user-id", "")
	authReq.Header.Set("user-token", CalculateDynamicToken("/authentication-otp", authPayload, ""))

	authResp, err := http.DefaultClient.Do(authReq)
	if err != nil {
		return fmt.Errorf("发送请求失败: %v", err)
	}
	defer authResp.Body.Close()

	authRespBody, err := readResponseBody(authResp)
	if err != nil {
		return fmt.Errorf("读取响应失败: %v", err)
	}

	decryptedAuthResp, err := X19HttpDecrypt(authRespBody)
	if err != nil {
		return fmt.Errorf("解密响应失败: %v", err)
	}

	validAuthRespJSON := GetValidJSON(decryptedAuthResp)
	var loginRespData LoginResponse
	if err := json.Unmarshal(validAuthRespJSON, &loginRespData); err != nil {
		return fmt.Errorf("解析登录响应失败: %v", err)
	}
	if loginRespData.Code != 0 {
		return fmt.Errorf("登录失败 (code: %d): %s", loginRespData.Code, loginRespData.Message)
	}

	// 设置用户凭证
	c.SetCredentials(loginRespData.Entity.EntityID, loginRespData.Entity.Token)
	c.Seed = loginRespData.Entity.Seed

	// 获取用户详情
	userDetail, err := c.GetUserDetail()
	if err != nil {
		return fmt.Errorf("获取用户信息失败: %v", err)
	}
	c.UserDetail = &userDetail.Entity
	return nil
}

var OSName = "android"

// 生成租赁服认证v2数据
func (c *Client) GenerateRentalGameAuthV2(serverID, clientKey string) ([]byte, error) {
	uid, err := c.GetUserIDInt()
	if err != nil {
		return nil, err
	}

	authv2 := map[string]any{
		"bit":           "64",
		"clientKey":     clientKey,
		"displayName":   c.UserDetail.Name,
		"engineVersion": c.EngineVersion,
		"netease_sid":   fmt.Sprintf("%s:RentalGame", serverID),
		"os_name":       OSName,
		"patchVersion":  c.G79LatestVersion,
		"uid":           uid,
	}

	return json.Marshal(authv2)
}

// 生成大厅游戏认证v2数据（netease_sid: roomID:LobbyGame）
func (c *Client) GenerateLobbyGameAuthV2(roomID, clientKey string) ([]byte, error) {
	uid, err := c.GetUserIDInt()
	if err != nil {
		return nil, err
	}

	authv2 := map[string]any{
		"bit":           "64",
		"clientKey":     clientKey,
		"displayName":   c.UserDetail.Name,
		"engineVersion": c.EngineVersion,
		"netease_sid":   fmt.Sprintf("%s:LobbyGame", roomID),
		"os_name":       OSName,
		"patchVersion":  c.G79LatestVersion,
		"uid":           uid,
	}

	return json.Marshal(authv2)
}

// 生成网络游戏认证v2数据（netease_sid: roomID:NetworkGame）
func (c *Client) GenerateNetworkGameAuthV2(roomID, clientKey string) ([]byte, error) {
	uid, err := c.GetUserIDInt()
	if err != nil {
		return nil, err
	}

	authv2 := map[string]any{
		"bit":           "64",
		"clientKey":     clientKey,
		"displayName":   c.UserDetail.Name,
		"engineVersion": c.EngineVersion,
		"netease_sid":   fmt.Sprintf("%s:NetworkGame", roomID),
		"os_name":       OSName,
		"patchVersion":  c.G79LatestVersion,
		"uid":           uid,
	}

	return json.Marshal(authv2)
}

// 发送认证v2请求
func (c *Client) SendAuthV2Request(authv2Data []byte) ([]byte, error) {
	api := "/authentication-v2"

	encryptedData, err := G79HttpEncrypt(authv2Data)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", c.G79ReleaseJSON.AuthServerURL+api, strings.NewReader(hex.EncodeToString(encryptedData)))
	if err != nil {
		return nil, err
	}

	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("user-id", c.UserID)

	token := CalculateDynamicToken(api, string(authv2Data), c.UserToken)
	req.Header.Set("user-token", hex.EncodeToString([]byte(token)))

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	respBody, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	encryptedResp, err := hex.DecodeString(string(respBody))
	if err != nil {
		return nil, err
	}

	decryptedResp, err := G79HttpDecrypt(encryptedResp)
	if err != nil {
		return nil, err
	}

	return GetValidJSON(decryptedResp), nil
}
