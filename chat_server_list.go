package g79client

import (
	"encoding/json"
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

var (
	globalChatServers []ChatServerEntry
	chatServerMu      sync.RWMutex
)

func init() {
	// Attempt to warm the cache at startup; ignore errors as callers will retry.
	_, _ = GetGlobalChatServers()
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
	releaseJSON, err := GetGlobalReleaseJSON()
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
