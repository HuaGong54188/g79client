package g79client

import (
	"net/http"
	"strconv"
	"time"
)

var EngineVersion = "3.5.5.278500"

func Refetch() {
	_, _ = RefreshTransferServers()
	_, _ = RefreshLinkServers()
	_, _ = RefreshChatServers()
	packList, _ := RefreshPackList()
	neteasePack, ok := packList["netease"]
	if ok {
		EngineVersion = neteasePack.Version
	}
}

func init() {
	Refetch()
	go func() {
		for {
			time.Sleep(time.Second * 60)
			Refetch()
		}
	}()
}

// Client 结构体
type Client struct {
	UserID           string
	UserToken        string
	Seed             string
	ReleaseJSON      *ReleaseJSON
	EngineVersion    string
	LatestVersion    string
	UserDetail       *UserDetailEntity
	peUserLoginAfter *PeUserLoginAfterResponse
	httpClient       *http.Client
}

// 创建新的客户端
func NewClient() (*Client, error) {
	c := &Client{
		EngineVersion: EngineVersion,
		httpClient:    &http.Client{},
	}
	var err error
	c.LatestVersion, err = GetGlobalLatestVersion()
	if err != nil {
		return nil, err
	}
	c.ReleaseJSON, err = GetGlobalReleaseJSON()
	if err != nil {
		return nil, err
	}
	return c, nil
}

// 设置用户凭证
func (c *Client) SetCredentials(userID, userToken string) {
	c.UserID = userID
	c.UserToken = userToken
}

// 获取用户ID的整数形式
func (c *Client) GetUserIDInt() (int64, error) {
	return strconv.ParseInt(c.UserID, 10, 64)
}
