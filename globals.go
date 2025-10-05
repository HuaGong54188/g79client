package g79client

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

// ChatServerEntry represents a single chat server configuration returned by NetEase.
type ChatServerEntry struct {
	IP         string    `json:"IP"`
	IspEnabled Uncertain `json:"Isp_Enabled"`
	CTCCHost   string    `json:"ctcc_host"`
	CMCCHost   string    `json:"cmcc_host"`
	CUCCHost   string    `json:"cucc_host"`
	Port       int       `json:"Port"`
}

// LinkServerEntry 描述一个 Link 服务器节点。
type LinkServerEntry struct {
	Status     Uncertain `json:"status"`
	IspEnabled Uncertain `json:"Isp_Enabled"`
	IP         string    `json:"ip"`
	ServerType string    `json:"ServerType"`
	ID         Uncertain `json:"id"`
	Port       Uncertain `json:"port"`
}

// TransferServerEntry 描述一个传输服务器节点。
type TransferServerEntry struct {
	Status        Uncertain `json:"status"`
	IP            string    `json:"ip"`
	ISPEnabled    Uncertain `json:"Isp_Enabled"`
	BatchNew      Uncertain `json:"batchNew"`
	Batch         Uncertain `json:"batch"`
	ID            Uncertain `json:"id"`
	SignalWebPort Uncertain `json:"SignalWebPort"`
	ServerType    string    `json:"ServerType"`
	WebPort       Uncertain `json:"WebPort"`
	Ports         []int     `json:"ports"`
}

var (
	globalLatestVersion   string
	globalReleaseJSON     *G79ReleaseJSON
	globalChatServers     []ChatServerEntry
	globalLinkServers     []LinkServerEntry
	globalTransferServers []TransferServerEntry

	latestMu     sync.RWMutex
	releaseMu    sync.RWMutex
	chatServerMu sync.RWMutex
	linkMu       sync.RWMutex
	transferMu   sync.RWMutex
)

func init() {
	// 在包初始化时尝试预取；失败则忽略，后续调用会再次尝试
	_, _ = GetGlobalLatestVersion()
	_, _ = GetGlobalG79ReleaseJSON()
	_, _ = GetGlobalChatServers()
	_, _ = GetGlobalLinkServers()
	_, _ = GetGlobalTransferServers()
}

func GetGlobalLatestVersion() (string, error) {
	latestMu.RLock()
	if globalLatestVersion != "" {
		v := globalLatestVersion
		latestMu.RUnlock()
		return v, nil
	}
	latestMu.RUnlock()

	latestMu.Lock()
	defer latestMu.Unlock()
	if globalLatestVersion != "" {
		return globalLatestVersion, nil
	}
	v, err := fetchLatestVersion()
	if err != nil {
		return "", err
	}
	globalLatestVersion = v
	return v, nil
}

func fetchLatestVersion() (string, error) {
	resp, err := http.Get("https://g79.update.netease.com/patch_list/production/g79_rn_patchlist")
	if err != nil {
		return "", err
	}

	body, err := readResponseBody(resp)
	if err != nil {
		return "", err
	}

	var patchInfo PatchInfo
	if err := json.Unmarshal(body, &patchInfo); err != nil {
		return "", err
	}

	if len(patchInfo.IOS) == 0 {
		return "", fmt.Errorf("no iOS version info found")
	}

	return patchInfo.IOS[len(patchInfo.IOS)-1], nil
}

func GetGlobalG79ReleaseJSON() (*G79ReleaseJSON, error) {
	releaseMu.RLock()
	if globalReleaseJSON != nil {
		v := globalReleaseJSON
		releaseMu.RUnlock()
		return v, nil
	}
	releaseMu.RUnlock()

	releaseMu.Lock()
	defer releaseMu.Unlock()
	if globalReleaseJSON != nil {
		return globalReleaseJSON, nil
	}
	v, err := fetchG79ReleaseJSON()
	if err != nil {
		return nil, err
	}
	globalReleaseJSON = v
	return v, nil
}



func fetchG79ReleaseJSON() (*G79ReleaseJSON, error) {
	resp, err := http.Get("https://g79.update.netease.com/serverlist/ios_release.0.25.json")
	if err != nil {
		return nil, err
	}

	body, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	var releaseJSON G79ReleaseJSON
	if err := json.Unmarshal(body, &releaseJSON); err != nil {
		return nil, err
	}

	return &releaseJSON, nil
}

// GetGlobalChatServers returns the cached global chat server list, populating it on first use.
func GetGlobalChatServers() ([]ChatServerEntry, error) {
	chatServerMu.RLock()
	if globalChatServers != nil {
		v := make([]ChatServerEntry, len(globalChatServers))
		copy(v, globalChatServers)
		chatServerMu.RUnlock()
		return v, nil
	}
	chatServerMu.RUnlock()

	chatServerMu.Lock()
	defer chatServerMu.Unlock()
	if globalChatServers != nil {
		v := make([]ChatServerEntry, len(globalChatServers))
		copy(v, globalChatServers)
		return v, nil
	}

	list, err := fetchChatServers()
	if err != nil {
		return nil, err
	}
	globalChatServers = list
	return list, nil
}

// RefreshChatServers forces a refresh of the cached chat server list.
func RefreshChatServers() ([]ChatServerEntry, error) {
	list, err := fetchChatServers()
	if err != nil {
		return nil, err
	}
	chatServerMu.Lock()
	globalChatServers = list
	chatServerMu.Unlock()
	return list, nil
}

func fetchChatServers() ([]ChatServerEntry, error) {
	releaseJSON, err := GetGlobalG79ReleaseJSON()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("GET", releaseJSON.ChatServerURL, nil)
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

	var list []ChatServerEntry
	if err := json.Unmarshal(body, &list); err != nil {
		return nil, err
	}
	return list, nil
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
	releaseJSON, err := GetGlobalG79ReleaseJSON()
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

// GetGlobalTransferServers 获取传输服务器列表（全局只拉取一次，后续复用缓存）。
func GetGlobalTransferServers() ([]TransferServerEntry, error) {
	transferMu.RLock()
	if globalTransferServers != nil {
		v := make([]TransferServerEntry, len(globalTransferServers))
		copy(v, globalTransferServers)
		transferMu.RUnlock()
		return v, nil
	}
	transferMu.RUnlock()

	transferMu.Lock()
	defer transferMu.Unlock()
	if globalTransferServers != nil {
		v := make([]TransferServerEntry, len(globalTransferServers))
		copy(v, globalTransferServers)
		return v, nil
	}

	list, err := fetchTransferServers()
	if err != nil {
		return nil, err
	}
	globalTransferServers = list
	return list, nil
}

// RefreshTransferServers 强制刷新传输服务器列表缓存。
func RefreshTransferServers() ([]TransferServerEntry, error) {
	list, err := fetchTransferServers()
	if err != nil {
		return nil, err
	}
	transferMu.Lock()
	globalTransferServers = list
	transferMu.Unlock()
	return list, nil
}

func fetchTransferServers() ([]TransferServerEntry, error) {
	releaseJSON, err := GetGlobalG79ReleaseJSON()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("GET", releaseJSON.TransferServerUrl, nil)
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

	var list []TransferServerEntry
	if err := json.Unmarshal(body, &list); err != nil {
		return nil, err
	}
	return list, nil
}
