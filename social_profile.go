package g79client

// SocialProfile 描述社交相关接口返回的统一用户档案。
type SocialProfile struct {
	ID                   Uncertain             `json:"id"`
	Nickname             string                `json:"nickname"`
	Signature            string                `json:"signature"`
	HeadImage            string                `json:"headImage"`
	FrameID              string                `json:"frame_id"`
	MomentID             string                `json:"moment_id"`
	PublicFlag           Uncertain             `json:"public_flag"`
	PEGrowth             SocialProfileGrowth   `json:"pe_growth"`
	UserGameInfo         map[string]any        `json:"user_game_info"`
	FriendRecommend      Uncertain             `json:"friend_recommend"`
	FriendApply          Uncertain             `json:"friend_apply"`
	Tag                  []SocialProfileTag    `json:"tag"`
	IsDeveloper          bool                  `json:"is_developer"`
	Mark                 string                `json:"mark"`
	RechargeBenefitLevel Uncertain             `json:"recharge_benefit_level"`
	IsFriend             bool                  `json:"is_friend"`
	TodayLiked           []any                 `json:"today_liked"`
	StatisData           []SocialProfileStat   `json:"statis_data"`
	HomepageBG           Uncertain             `json:"homepage_bg"`
	VisitCardBG          Uncertain             `json:"visit_card_bg"`
	CityNo               Uncertain             `json:"city_no"`
	RechargeVIPLevel     Uncertain             `json:"recharge_vip_level"`
	RechargeVIPInfo      map[string]any        `json:"recharge_vip_info"`
	LBSInfo              *SocialProfileLBSInfo `json:"lbs_info"`
}

// SocialProfileGrowth 表示成长信息。
type SocialProfileGrowth struct {
	Lv         Uncertain `json:"lv"`
	Exp        Uncertain `json:"exp"`
	NeedExp    Uncertain `json:"need_exp"`
	Decorate   []any     `json:"decorate"`
	IsVIP      Uncertain `json:"is_vip"`
	IsVIPExpr  Uncertain `json:"is_vip_expr"`
	ChatBubble Uncertain `json:"chat_bubble_id"`
}

// SocialProfileTag 表示用户标签。
type SocialProfileTag struct {
	TagID   Uncertain `json:"tag_id"`
	TagName string    `json:"tag_name"`
	Likes   Uncertain `json:"likes"`
}

// SocialProfileStat 表示统计数据。
type SocialProfileStat struct {
	Type    Uncertain `json:"type"`
	Value   Uncertain `json:"value"`
	Visible Uncertain `json:"visible"`
}

// SocialProfileLBSInfo 表示地理位置。
type SocialProfileLBSInfo struct {
	Province string `json:"province"`
	City     string `json:"city"`
	Area     string `json:"area"`
}
