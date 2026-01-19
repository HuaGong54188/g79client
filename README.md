# 前言

该项目第一作者始终是 `Yeah114`

由于网易我的世界已经更新了3.7版本，因此，该存储库在进行认证时会提示 `客户端版本过低，请升级客户端` ，因此你应该应该参考下方内容进行更改

1.出现该问题的原因是因为自动更新到了最新的3.7版本，但Sign部分为过时的，所以我们应更改这部分的相关内容(当然，你也可以通过修改代码继续使用原本的3.6进行登录，经过观测目前可行，对此不做多述)

# G79Client Go 模块

这是一个用 Go 重写的网易我的世界 G79 客户端库，原始功能来自 Python 版本的 `t.py`。

## 功能特性

- ✅ HTTP 加密/解密 (AES-CBC)
- ✅ 动态 Token 计算
- ✅ 网易 PE 认证流程
- ✅ 租赁服搜索和连接
- ✅ 用户信息获取和昵称修改
- ✅ 认证链信息生成

## 安装

```bash
go get github.com/Yeah114/g79client
```

## 使用示例

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/Yeah114/g79client"
)

func main() {
    err := g79client.RunG79Client()
    if err != nil {
        log.Fatalf("运行失败: %v", err)
    }
    fmt.Println("运行完成!")
}
```

## 模块结构

- `crypto.go` - 加密解密功能
- `auth.go` - 认证相关功能  
- `client.go` - HTTP 客户端和 API 调用
- `main.go` - 主要业务逻辑
- `example/` - 使用示例

## 依赖

- `github.com/google/uuid` - UUID 生成

## 编译和运行

```bash
# 编译
go build -v ./...

# 运行示例
go run example/main.go
```

## 与原版 Python 代码的对比

| 功能 | Python (t.py) | Go (g79client) |
|------|---------------|----------------|
| 加密算法 | ✅ | ✅ |
| 认证流程 | ✅ | ✅ |
| 租赁服操作 | ✅ | ✅ |
| 用户管理 | ✅ | ✅ |
| 代码精简 | - | ✅ |
| 类型安全 | - | ✅ |
| 性能优化 | - | ✅ |
