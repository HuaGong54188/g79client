package g79client

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// PeUserLoginAfterResponse 表示 /pe-user-login-after 接口的响应体。
type PeUserLoginAfterResponse struct {
	Response
	Entity PeUserLoginAfterEntity `json:"entity"`
}

// PeUserLoginAfterEntity 描述登录后返回的玩家状态信息。
type PeUserLoginAfterEntity struct {
	HasMessage          bool                           `json:"hasMessage"`
	RestCurrencyTime    Uncertain                      `json:"rest_currency_time"`
	RemainReviseNameCnt Uncertain                      `json:"remain_revise_name_cnt"`
	UsedName            string                         `json:"used_name"`
	MomentID            string                         `json:"moment_id"`
	PublicFlag          bool                           `json:"public_flag"`
	CanPostVideo        bool                           `json:"can_post_video"`
	NeedPhoneBind       bool                           `json:"need_phone_bind"`
	IsPhoneBind         Uncertain                      `json:"is_phone_bind"`
	UpdateTimeStamp     Uncertain                      `json:"update_time_stamp"`
	IsNewReward         Uncertain                      `json:"is_new_reward"`
	IsPhoneAccount      Uncertain                      `json:"is_phone_account"`
	BanChatExpiredAt    Uncertain                      `json:"ban_chat_expired_at"`
	ActivityBonus       []any                          `json:"activity_bonus"`
	SingleGameEffect    []any                          `json:"single_game_special_effect"`
	BanItemInfo         []any                          `json:"ban_item_info"`
	OnlineStatus        Uncertain                      `json:"online_status"`
	WechatWishItem      Uncertain                      `json:"wechat_wish_item"`
	MyImageURL          string                         `json:"my_image_url"`
	MailDelList         []any                          `json:"mail_del_list"`
	FavoriteIIDStatus   Uncertain                      `json:"favorite_iid_status"`
	IsBind              bool                           `json:"is_bind"`
	WechatInfo          *PeUserLoginAfterWechatInfo    `json:"wechat_info"`
	WechatWishItemID    string                         `json:"wechat_wish_item_id"`
	SocialSetting       *PeUserLoginAfterSocialSetting `json:"social_setting"`
}

// PeUserLoginAfterWechatInfo 描述微信相关信息。
type PeUserLoginAfterWechatInfo struct {
	BindReward  *PeUserLoginAfterBindReward `json:"bind_reward"`
	WechatH5URL string                      `json:"wechat_h5_url"`
}

// PeUserLoginAfterBindReward 描述微信绑定奖励。
type PeUserLoginAfterBindReward struct {
	URL string    `json:"url"`
	NB  Uncertain `json:"nb"`
	TP  Uncertain `json:"tp"`
}

// PeUserLoginAfterSocialSetting 描述社交设置。
type PeUserLoginAfterSocialSetting struct {
	UnderageMode              bool      `json:"underage_mode"`
	BlockStrangers            bool      `json:"block_strangers"`
	BlockAllMessages          bool      `json:"block_all_messages"`
	BlockRepostedAndCommented bool      `json:"block_reposted_and_commented"`
	MessageVisibility         Uncertain `json:"message_visibility"`
}

// GetPeUserLoginAfter 请求 /pe-user-login-after 接口并缓存响应。
func (c *Client) GetPeUserLoginAfter() (*PeUserLoginAfterResponse, error) {
	if c.peUserLoginAfter != nil {
		return c.peUserLoginAfter, nil
	}

	if c.ReleaseJSON == nil {
		release, err := c.GetReleaseJSON()
		if err != nil {
			return nil, err
		}
		c.ReleaseJSON = release
	}

	api := "/pe-user-login-after"
	payload := map[string]any{
		"client_type": "cocos",
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", c.ReleaseJSON.ApiGatewayUrl+api, strings.NewReader(string(body)))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("user-id", c.UserID)

	token := CalculateDynamicToken(api, string(body), c.UserToken)
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

	var result PeUserLoginAfterResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return nil, fmt.Errorf("解析 pe-user-login-after 响应失败: %v, 响应内容: %s", err, string(respBody))
	}

	c.peUserLoginAfter = &result
	return &result, nil
}
