package g79client

import (
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/google/uuid"
)

// 认证相关结构体
type LoginEntity struct {
	EntityID string `json:"entity_id"`
	Token    string `json:"token"`
}

type LoginResponse struct {
	Response
	Entity LoginEntity `json:"entity"`
}

// {'HostNum': 200, 'ServerHostNum': 8000, 'TempServerStop': 0, 'CdnUrl': 'https://g79.gdl.netease.com/', 'H5VersionUrl': 'https://g79.update.netease.com/cdnversion/obt_h5version.json', 'SeadraUrl': 'https://pub-api.seadra.netease.com', 'HomeServerUrl': 'https://g79mclobthome.minecraft.cn', 'HomeServerGrayUrl': 'https://g79mclobthomegray.nie.netease.com:9443', 'WebServerUrl': 'https://g79mclobt.minecraft.cn', 'WebServerGrayUrl': 'https://g79mclobtgray.nie.netease.com:9443', 'CoreServerUrl': 'https://g79obtapigtcoregray.minecraft.cn', 'CoreServerGrayUrl': 'https://g79obtapigtcoregray.minecraft.cn', 'TransferServerUrl': 'https://g79.update.netease.com/transferserver_obt_new.list', 'TransferServerHttpUrl': 'https://g79transfernew.nie.netease.com', 'TransferServerNewHttpUrl': 'https://g79mcltransfer.minecraft.cn', 'MomentUrl': 'https://x19-pyq.webcgi.163.com/', 'ForumUrl': 'https://mcpel-web.16163.com', 'AuthServerUrl': 'https://g79authobt.minecraft.cn', 'ChatServerUrl': 'https://x19.update.netease.com/chatserver.list', 'PathNUrl': 'https://impression.update.netease.com/lighten/atlas_x19_hangzhou-{isp}.txt', 'PePathNUrl': 'https://impression.update.netease.com/lighten/atlas_g79_hangzhou-{isp}.txt', 'PathNIpv6Url': 'https://impression.update.netease.com/lighten/x19/cnv6.txt', 'PePathNIpv6Url': 'https://impression.update.netease.com/lighten/g79/cnv6.txt', 'LinkServerUrl': 'https://g79.update.netease.com/linkserver_obt.list', 'ApiGatewayUrl': 'https://g79apigatewayobt.minecraft.cn', 'ApiGatewayWeiXinUrl': 'https://g79apigatewayobtweixin.minecraft.cn', 'ApiGatewayGrayUrl': 'https://g79apigatewaygrayobt.nie.netease.com', 'communityHost': 'https://news-api.16163.com/app/g79/api', 'WelfareUrl': 'https://mc.163.com/pe/client/', 'DCWebUrl': 'https://x19apigatewayobt.nie.netease.com', 'RentalTransferUrl': 'https://mcrealms.update.netease.com/isp_map_production.json', 'MgbSdkUrl': 'https://mgbsdk.matrix.netease.com'}
type ReleaseJSON struct {
	CoreServerURL            string `json:"CoreServerUrl"`
	AuthServerURL            string `json:"AuthServerUrl"`
	WebServerUrl             string `json:"WebServerUrl"`
	ApiGatewayUrl            string `json:"ApiGatewayUrl"`
	TransferServerUrl        string `json:"TransferServerUrl"`
	TransferServerNewHttpUrl string `json:"TransferServerNewHttpUrl"`
}

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
func (c *Client) AuthenticateWithCookie(cookieStr string) error {
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
	err = c.performPEAuthWithCookie(&sauthData)
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

// 获取最新版本
func (c *Client) GetLatestVersion() (string, error) {
	return GetGlobalLatestVersion()
}

// 获取服务器配置
func (c *Client) GetReleaseJSON() (*ReleaseJSON, error) {
	return GetGlobalReleaseJSON()
}

// 使用Cookie执行PE认证
func (c *Client) performPEAuthWithCookie(sauthData *SauthData) error {
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
		"app_ver":       c.LatestVersion,
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
		"message":        fmt.Sprintf("%sapple%s%s%s", c.EngineVersion, c.LatestVersion, messagePart, seed),
		"patch_version":  c.LatestVersion,
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

	encryptedPayload, err := HttpEncrypt(peauthJSON)
	if err != nil {
		return err
	}

	// 发送认证请求
	req, err := http.NewRequest("POST", c.ReleaseJSON.CoreServerURL+"/pe-authentication", strings.NewReader(hex.EncodeToString(encryptedPayload)))
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

	decryptedResp, err := HttpDecrypt(encryptedResp)
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
		"patchVersion":  c.LatestVersion,
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
		"patchVersion":  c.LatestVersion,
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
		"patchVersion":  c.LatestVersion,
		"uid":           uid,
	}

	return json.Marshal(authv2)
}

// 发送认证v2请求
func (c *Client) SendAuthV2Request(authv2Data []byte) ([]byte, error) {
	api := "/authentication-v2"

	encryptedData, err := HttpEncrypt(authv2Data)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", c.ReleaseJSON.AuthServerURL+api, strings.NewReader(hex.EncodeToString(encryptedData)))
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

	decryptedResp, err := HttpDecrypt(encryptedResp)
	if err != nil {
		return nil, err
	}

	return GetValidJSON(decryptedResp), nil
}
