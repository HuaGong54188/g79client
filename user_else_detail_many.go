package g79client

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// -------------------- 强类型响应定义 --------------------

// 他人详情成长信息
type ElseDetailGrowth struct {
	ChatBubbleID    Uncertain `json:"chat_bubble_id"`
	Decorate        []any     `json:"decorate"`
	Exp             Uncertain `json:"exp"`
	IsVIP           Uncertain `json:"is_vip"`
	IsVIPExpr       Uncertain `json:"is_vip_expr"`
	Lv              Uncertain `json:"lv"`
	MsgBackgroundID Uncertain `json:"msg_background_id"`
	NeedExp         Uncertain `json:"need_exp"`
}

// 他人详情实体
type ElseDetailEntity struct {
	ChatBubbleID         Uncertain        `json:"chat_bubble_id"`
	FrameID              string           `json:"frame_id"`
	HeadImage            string           `json:"headImage"`
	HeadImageType        Uncertain        `json:"headImageType"`
	ID                   Uncertain        `json:"id"`
	MomentID             Uncertain        `json:"moment_id"`
	MsgBackgroundID      Uncertain        `json:"msg_background_id"`
	Nickname             string           `json:"nickname"`
	OnlineStatus         Uncertain        `json:"online_status"`
	OnlineType           Uncertain        `json:"online_type"`
	PeGrowth             ElseDetailGrowth `json:"pe_growth"`
	PublicFlag           Uncertain        `json:"public_flag"`
	RechargeBenefitLevel Uncertain        `json:"recharge_benefit_level"`
	RechargeVIPInfo      map[string]any   `json:"recharge_vip_info"`
	RechargeVIPLevel     Uncertain        `json:"recharge_vip_level"`
	Signature            string           `json:"signature"`
	StaticURL            string           `json:"static_url"`
}

// 批量他人详情响应
type UserElseDetailManyResponse struct {
	Response
	Entities   []ElseDetailEntity `json:"entities"`
	Details    string             `json:"details"`
	SummaryMD5 string             `json:"summary_md5"`
}

// 获取他人详情（批量）
func (c *Client) GetUserElseDetailMany(uids []string) (*UserElseDetailManyResponse, error) {
	api := "/user-else-detail-many/"

	requestData := map[string]interface{}{
		"is_need_recharge_benefit": 1,
		"uids":                     strings.Join(uids, ";"),
	}

	jsonData, err := json.Marshal(requestData)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", c.ReleaseJSON.ApiGatewayUrl+api, strings.NewReader(string(jsonData)))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
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

	var result UserElseDetailManyResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return nil, fmt.Errorf("解析他人详情(批量)失败: %v", err)
	}
	return &result, nil
}
