package g79client

import (
	"encoding/json"
	"net/http"
	"sync"
)

const g79PackListURL = "https://g79.update.netease.com/pack_list/production/g79_packlist_2"

// PackListEntry 描述单个平台的安装包信息。
type PackListEntry struct {
	URL      string `json:"url"`
	Text     string `json:"text"`
	Version  string `json:"version"`
	MinVer   string `json:"min_ver"`
}

var (
	globalPackList map[string]PackListEntry
	packListMu     sync.RWMutex
)

func init() {
	// 预取一次，忽略错误，后续调用会自动重试。
	_, _ = GetGlobalPackList()
}

// GetGlobalPackList 获取全局 g79 packlist 配置，首次调用会自动拉取并缓存。
func GetGlobalPackList() (map[string]PackListEntry, error) {
	packListMu.RLock()
	if globalPackList != nil {
		v := clonePackList(globalPackList)
		packListMu.RUnlock()
		return v, nil
	}
	packListMu.RUnlock()

	packListMu.Lock()
	defer packListMu.Unlock()
	if globalPackList != nil {
		return clonePackList(globalPackList), nil
	}

	list, err := fetchPackList()
	if err != nil {
		return nil, err
	}
	globalPackList = list
	return clonePackList(list), nil
}

// RefreshPackList 强制刷新 g79 packlist 缓存。
func RefreshPackList() (map[string]PackListEntry, error) {
	list, err := fetchPackList()
	if err != nil {
		return nil, err
	}
	packListMu.Lock()
	globalPackList = list
	packListMu.Unlock()
	return clonePackList(list), nil
}

func fetchPackList() (map[string]PackListEntry, error) {
	req, err := http.NewRequest("GET", g79PackListURL, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("content-type", "text/plain")
	req.Header.Set("cache-control", "no-cache")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	var list map[string]PackListEntry
	if err := json.Unmarshal(body, &list); err != nil {
		return nil, err
	}
	return list, nil
}

func clonePackList(src map[string]PackListEntry) map[string]PackListEntry {
	if src == nil {
		return nil
	}
	dst := make(map[string]PackListEntry, len(src))
	for k, v := range src {
		dst[k] = v
	}
	return dst
}
