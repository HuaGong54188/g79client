package g79client

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

var (
	globalLatestVersion string
	globalReleaseJSON   *ReleaseJSON

	latestMu  sync.RWMutex
	releaseMu sync.RWMutex
)

func init() {
	// 在包初始化时尝试预取；失败则忽略，后续调用会再次尝试
	_, _ = GetGlobalLatestVersion()
	_, _ = GetGlobalReleaseJSON()
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

func GetGlobalReleaseJSON() (*ReleaseJSON, error) {
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
	v, err := fetchReleaseJSON()
	if err != nil {
		return nil, err
	}
	globalReleaseJSON = v
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

func fetchReleaseJSON() (*ReleaseJSON, error) {
	resp, err := http.Get("https://g79.update.netease.com/serverlist/ios_release.0.25.json")
	if err != nil {
		return nil, err
	}

	body, err := readResponseBody(resp)
	if err != nil {
		return nil, err
	}

	var releaseJSON ReleaseJSON
	if err := json.Unmarshal(body, &releaseJSON); err != nil {
		return nil, err
	}

	return &releaseJSON, nil
}
