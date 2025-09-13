package g79client

import (
	"encoding/json"
	"net/http"
	"sync"
)

// 传输服务器条目
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
	globalTransferServers []TransferServerEntry
	transferMu            sync.RWMutex
)

func init() {
	// 尝试预取；失败忽略，后续调用会再次尝试
	_, _ = GetGlobalTransferServers()
}

// GetGlobalTransferServers 获取传输服务器列表（全局只拉取一次，后续复用缓存）
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

// RefreshTransferServers 强制刷新传输服务器列表缓存
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
	releaseJSON, err := GetGlobalReleaseJSON()
	if err != nil {
		return nil, err
	}
	url := releaseJSON.TransferServerUrl
	req, err := http.NewRequest("GET", url, nil)
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
