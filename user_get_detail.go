package g79client

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// 用户详情结构体
type UserEntity struct {
	EntityID Uncertain `json:"entity_id"`
	Name     string    `json:"name"`
	Level    Uncertain `json:"level"`
}

type UserDetailResponse struct {
	Response
	Entity UserEntity `json:"entity"`
}

// 获取用户详情
func (c *Client) GetUserDetail() (*UserDetailResponse, error) {
	api := "/pe-user-detail/get"

	requestData := map[string]interface{}{}

	jsonData, err := json.Marshal(requestData)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", c.ReleaseJSON.CoreServerURL+api, strings.NewReader(string(jsonData)))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	req.Header.Set("User-Agent", "WPFLauncher/0.0.0.0")
	req.Header.Set("user-id", c.UserID)

	token := CalculateDynamicToken(api, string(jsonData), c.UserToken)
	req.Header.Set("user-token", token)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	respBody, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	var userDetailResp UserDetailResponse
	if err := json.Unmarshal(respBody, &userDetailResp); err != nil {
		return nil, fmt.Errorf("解析用户详情响应失败: %v, 响应内容: %s", err, string(respBody))
	}
	return &userDetailResp, nil
}
