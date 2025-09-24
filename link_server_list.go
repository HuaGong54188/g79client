package g79client

import (
	"encoding/json"
	"net/http"
	"sync"
)

// LinkServerEntry 描述一个 Link 服务器节点。
type LinkServerEntry struct {
	Status     Uncertain `json:"status"`
	IspEnabled Uncertain `json:"Isp_Enabled"`
	IP         string    `json:"ip"`
	ServerType string    `json:"ServerType"`
	ID         Uncertain `json:"id"`
	Port       Uncertain `json:"port"`
}

var (
	globalLinkServers []LinkServerEntry
	linkMu            sync.RWMutex
)

func init() {
	// 预拉取一次，失败忽略，后续调用会再尝试。
	_, _ = GetGlobalLinkServers()
}

// GetGlobalLinkServers 获取全局 Link 服务器列表，如果已有缓存直接返回副本。
func GetGlobalLinkServers() ([]LinkServerEntry, error) {
	linkMu.RLock()
	if globalLinkServers != nil {
		list := make([]LinkServerEntry, len(globalLinkServers))
		copy(list, globalLinkServers)
		linkMu.RUnlock()
		return list, nil
	}
	linkMu.RUnlock()

	linkMu.Lock()
	defer linkMu.Unlock()
	if globalLinkServers != nil {
		list := make([]LinkServerEntry, len(globalLinkServers))
		copy(list, globalLinkServers)
		return list, nil
	}

	list, err := fetchLinkServers()
	if err != nil {
		return nil, err
	}
	globalLinkServers = list
	return list, nil
}

// RefreshLinkServers 强制刷新缓存。
func RefreshLinkServers() ([]LinkServerEntry, error) {
	list, err := fetchLinkServers()
	if err != nil {
		return nil, err
	}
	linkMu.Lock()
	globalLinkServers = list
	linkMu.Unlock()
	return list, nil
}

func fetchLinkServers() ([]LinkServerEntry, error) {
	releaseJSON, err := GetGlobalReleaseJSON()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("GET", releaseJSON.LinkServerURL, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", "libhttpclient/1.0.0.0")
	req.Header.Set("Accept-Encoding", "gzip")
	req.Header.Set("content-type", "text/plain")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	var list []LinkServerEntry
	if err := json.Unmarshal(body, &list); err != nil {
		return nil, err
	}
	return list, nil
}
