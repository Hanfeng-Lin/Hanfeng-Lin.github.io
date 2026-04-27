---
title: 'Cloudflare DDNS + VLESS REALITY + Sunshine 远程唤醒全记录'
date: 2026-04-26
permalink: /posts/2026/04/home-pc-as-china-bridge/
tags:
  - Networking
  - Cloudflare
  - Xray
  - REALITY
  - WSL
  - Sunshine
  - Wake-on-LAN
---

> 本文记录了我如何把一台位于美国南部、跑在 Comcast 家庭宽带后的 Windows + WSL1 台式机，改造为一台可以从中国国内的 iPad/手机直连的"私人专线服务器"。涉及的技术栈包括 Cloudflare DDNS、Xray (VLESS + REALITY)、Comcast/Netgear 网关 DMZ、Wake-on-LAN，以及最后一公里的 Sunshine/Moonlight 远程串流。文章不是一份"教程"，而是一份**踩坑日志**——按时间顺序记录了为什么每一步要这么做，以及背后的决策逻辑。
>
> ⚠️ 文中的域名、UUID、密钥、IP、MAC 等已全部替换为占位符，请按自己的环境替换。

## 0. 起点：我有什么、想要什么

**已有的资源：**

- 一台位于美国南部某城市的台式 PC（AMD Radeon 集显，Windows 11，已装 WSL1 Ubuntu）。
- Comcast Xfinity 家庭宽带，住宅动态公网 IP（`73.x.x.x` 这种 Comcast 常见段）。
- 自己拥有（retail 零售）的猫路由一体机：Netgear CG3000D。CG3000D 本身只是一台普通的 DOCSIS cable 网关，**并非 Comcast 定制硬件**——但它接入 Xfinity 线路并完成激活后，会被运营商远程推送一套 provisioning 配置，于是登录界面变成了 Comcast 蓝、默认凭据也跟着被改写。这就是后面所有"为什么 admin/password 进不去"故事的根源。
- 后接的二级路由：TP-Link WR841N（一台老旧的百兆 N 标准路由器）。
- 一个在 Cloudflare Registrar 买的域名（下文统一记作 `example.org`）。
- 客户端：iPad（Shadowrocket）、Android 手机（v2rayNG）、笔记本（v2rayN）。

**想要做到的事：**

1. 国内的 iPad 能稳定刷 Google / Gemini，而不是看着进度条转圈。
2. 不依赖 VPS——这台美国 PC 本来就闲着，让它当出口节点。
3. 流量隐蔽，不要让运营商一眼看穿是代理。
4. 出门在外时，可以远程把这台 PC **从关机状态唤醒**，并通过 Moonlight 串流。
5. 整套系统在我不在家的时候**自我维护**：断电重启后能自动恢复，IP 变了能自动同步。

下面就是这套东西从无到有、从"勉强能通"到"工业级稳定"的全过程。

---

## 1. 协议选型：为什么放弃 WireGuard，选了 VLESS + REALITY

最初的备选是三条路：

| 方案 | 优点 | 缺点 |
|---|---|---|
| WireGuard | 内核态、延迟极低 | 特征明显，跨境容易被识别封端口 |
| Cloudflare Tunnel + WS+TLS | 不需要公网 IP，不需要做端口转发 | 国内访问 Cloudflare 节点不稳定，易丢包 |
| **VLESS + REALITY (TCP 直连)** | 借用大站 TLS 指纹，几乎无法识别；速度由家宽决定 | 需要公网 IP + 端口转发 |

我最初想"图省事"先用 Cloudflare Tunnel，因为它绕过了我对路由器是否有公网 IP 的不确定性。事实证明这是个**正确的中间步骤**——它让我先把服务跑起来、调通客户端，再去解决物理链路问题。但它也确实是后期的瓶颈，最终还是要换成 REALITY 直连。

**REALITY 的核心思路：** 它不是再做一个新协议，而是当探测者扫描你 443 端口时，让你的服务器**实时把流量转发给真实的 `www.microsoft.com`**，于是探测者拿到的是货真价实的微软证书；只有持有正确私钥的客户端会被识别出来并接进代理隧道。这意味着：

- 不需要自己申请证书。
- GFW 看到的是"一个美国住宅 IP 在和微软通信"，权重极高。
- 微软完全感知不到你（你的服务器只是在它面前装得像个微软服务器）。

---

## 2. 第一阶段：Cloudflare DDNS 把动态 IP 锁住

Comcast 的家宽是动态 IP——重启猫之后会变。要让国内的客户端始终能找到家，需要 DDNS。

### 2.1 为什么不用 DuckDNS

最早想用免费的 DuckDNS，但 `*.duckdns.org` 这个公共后缀在国内被广泛用于搭代理，已经被 GFW 重点关照过了。解析它经常拿到错的 IP。**自己买个域名**才是干净的选择——`.org` 域名第一年大约几美元，托管到 Cloudflare 一切免费。

### 2.2 在 Cloudflare 上添加 A 记录的关键细节

- **类型**：A（不是 AAAA）。
- **名称**：`home`，所以完整地址是 `home.example.org`。
- **TTL**：选 **2 分钟**。家宽 IP 变了之后，全国的 DNS 缓存最多 2 分钟就会刷新。Cloudflare 默认 5 分钟（Auto），对 DDNS 来说稍微长了点。
- **Proxy status**：**灰色云朵 (DNS Only)**。这一项至关重要——后面要用 REALITY，必须是灰云朵让流量直接打到家里的真实 IP；橙云朵（CDN 模式）会让 Cloudflare 拆解你的包，导致 REALITY 握手失败。


---

## 3. 第二阶段：双重 NAT 与 Comcast 网关的较量

DDNS 解析对了之后，自己手机连过来发现……完全连不上。原因就是物理链路：

```
Internet → Netgear CG3000D (10.1.10.1) → TP-Link (10.1.10.10) → PC (192.168.0.x)
```

这是典型的 **Double NAT**：流量进美国家里要过两道关卡。在 TP-Link 上做端口转发完全没用，因为 Netgear 这一关就把流量挡住了。`ipconfig` 显示 TP-Link 的 WAN 口拿到的是 `10.1.10.10`——这是个**私有地址**，完全不在公网上。

### 3.1 进 Netgear 后台的"祖传密码"

虽然 CG3000D 是 Netgear 自家的零售设备，但接入 Xfinity 后被推送了运营商的配置档，于是 `admin/password` 不再生效。物理硬复位也没让 Wi-Fi 名变化（说明 Comcast 的 provisioning 在重启后又把配置推回来了，根本没真正复位成功）。Xfinity App 也看不到这台设备——App 只管 Comcast 自家租给用户的 xFi Gateway，对零售第三方硬件无能为力。

最后试到这组才进去：

- **用户名**：`cusadmin`
- **密码**：`highspeed`

这是 Comcast 推送给商用/cable 类网关的 **provisioning 默认凭据**——不是 Netgear 出厂的，而是运营商配置档里的。这一对组合在网上很难直接搜到，但确实是 Comcast Business 线路上很多型号的"万能钥匙"。

### 3.2 DMZ vs Bridge Mode：选 DMZ 更稳

进入 Netgear 后台之后有两条路：

- **Bridge Mode**：让 Netgear 完全变成"纯猫"，由 TP-Link 拨号拿公网 IP。最彻底，但被 Comcast provisioning 后的配置档有时会因为开启桥接而拨号失败。
- **DMZ**：让 Netgear 把所有外部流量无脑转发给指定的内网 IP。

我选了 **DMZ + 直接把 PC 插在 Netgear 的 LAN 口**（绕过 TP-Link 这个百兆瓶颈）。这样：

- PC 直接拿到 `10.1.10.10`（Netgear 的 DHCP 分的）。
- DMZ 目标设为 `10.1.10.10`。
- 公网流量打到 Netgear → DMZ → 直接给 PC。
- 中间不再过那台只能跑 100Mbps 的 TP-Link。

**重要细节**：在 Netgear 后台还要做以下两件事：

1. **关闭 Smart Packet Detection**：默认开启的"智能包检测"会拦截高频握手（REALITY 协议的特征之一），跨海连接稳定性会显著提升。
2. **取消勾选 Disable Ping on WAN**：调试期间留着，方便用 `ping.chinaz.com` 这类工具验证全国可达性。正式跑稳之后再勾上。

> 顺便一提：理想情况下还应该在 LAN 设置里做 **Address Reservation**，把 PC 的 MAC 永久绑定到 `10.1.10.10`，防止关机后租约失效导致 IP 被分给别人。但这台被 Comcast provisioning 过的 CG3000D 固件里根本找不到这个选项——LAN 设置页向下翻到底就结束了（猜测是运营商的配置档把 retail 固件原本可能有的某些菜单也阉割了）。这个"缺口"在 Wake-on-LAN 阶段会变成大坑，**第 7 节会用一个广播地址的小技巧绕过它**。

---

## 4. 第三阶段：Xray 服务端配置（VLESS + REALITY）

环境是 WSL1。注意 WSL1 不是真正的 Linux 内核，它是 Windows 上的系统调用翻译层——这意味着 `ss` 命令会报 `Cannot open netlink socket`、`systemctl` 不可用、TCP_FASTOPEN 这类内核 socket 选项不被支持。但对 Xray 跑在用户态来说，这些都不是 deal-breaker。

### 4.1 生成 REALITY 密钥对

```bash
xray x25519
# 输出：
# PrivateKey: YOUR_PRIVATE_KEY_HERE
# Password (PublicKey): YOUR_PUBLIC_KEY_HERE
```

私钥写进服务端 config，公钥填到客户端。两边 `shortIds` 必须严格一致。

### 4.2 服务端 `config.json`

```json
{
  "log": {
    "access": "/var/log/xray/access.log",
    "error": "/var/log/xray/error.log",
    "loglevel": "info"
  },
  "inbounds": [
    {
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
            "flow": "xtls-rprx-vision"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "www.microsoft.com:443",
          "xver": 0,
          "serverNames": ["www.microsoft.com", "microsoft.com"],
          "privateKey": "YOUR_PRIVATE_KEY_HERE",
          "shortIds": ["xxxxxxxx"]
        },
        "sockopt": {
          "tcpFastOpen": true,
          "tproxy": "off"
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {
        "domainStrategy": "UseIPv4"
      },
      "tag": "direct"
    },
    {
      "protocol": "blackhole",
      "tag": "blocked"
    }
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "blocked"
      }
    ]
  }
}
```

### 4.3 配置中的几个关键决定

- **`flow: xtls-rprx-vision`**：REALITY 的灵魂。它会主动给数据包做 padding 和分块，让流量特征看起来像正常的 TLS 浏览。
- **`dest: www.microsoft.com:443` + `serverNames: [...]`**：伪装目标。微软流量极大、合规，GFW 不敢轻易封。这里也可以换 `www.apple.com` 或 `www.amazon.com`。
- **`domainStrategy: UseIPv4`**：强制出口走 IPv4。Gemini 这类 Google 服务非常喜欢优先尝试 IPv6 解析，如果走了 IPv6 但握手失败，浏览器要等好几秒才降级到 IPv4——这几秒就是你看到的"白屏"。
- **`tcpFastOpen: true`**：在普通 Linux 上能减少一次 RTT。WSL1 启动时会报 `failed to set TCP_FASTOPEN256 > protocol not available`，**这条是 Info 级别，可以忽略**，Xray 会自动跳过。

### 4.4 客户端配置（Shadowrocket / v2rayNG）

| 字段 | 值 | 备注 |
|---|---|---|
| 类型 | VLESS | |
| 服务器 | `home.example.org` | 直连模式下解析到 73.x.x.x |
| 端口 | 443 | |
| UUID | `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` | 严格匹配服务端 |
| 流控 | `xtls-rprx-vision` | |
| 传输方式 | tcp | |
| 安全 | reality | |
| SNI | `www.microsoft.com` | 与服务端 `serverNames` 一致 |
| PublicKey | `YOUR_PUBLIC_KEY_HERE` | |
| ShortId | `xxxxxxxx`（与服务端一致即可，建议自己生成 8 位 16 进制） | |
| Fingerprint (uTLS) | chrome | 跨境必须，不能选 none |

---

## 5. 链路打通的标志

在 WSL1 跑 `sudo tail -f /var/log/xray/access.log`，国内点击连接的瞬间应该看到：

```
2026/04/25 23:30:16 from 223.x.x.x:9871 accepted tcp:mesu.apple.com:443 [direct]
2026/04/25 23:30:16 [Info] proxy/vless/inbound: firstLen = 55
2026/04/25 23:30:16 [Info] proxy/freedom: connection opened to tcp:mesu.apple.com:443, ...
```

`accepted` + `connection opened` 两行就证明：

- 国内手机的请求穿过了 GFW、海底光缆。
- Comcast 把它路由到了我家。
- Netgear 的 DMZ 把它丢给了 PC。
- Windows 防火墙放行了 443。
- Xray 正确识别了 REALITY 握手。
- 出口走 IPv4 freedom 协议成功连接到 Apple 服务器。

第一条 `accepted tcp:mesu.apple.com:443` 是 iPad 后台自发的检查更新请求——这意味着 iOS 系统已经把代理"用起来了"。

---

## 6. 性能调优：300ms 延迟下的"长肥网络"问题

美国 ↔ 中国的物理延迟在 200-300ms 之间，属于 LFN（Long-Fat Network）。这种链路的特点是：**单包损失代价极高**，一旦丢包就要等 300ms 才知道，TCP 拥塞控制还会主动减速。

### 6.1 MTU 1500 → 1400：避开"大包静默丢弃"

VLESS + REALITY 会在原始数据包外面套一层加密头。如果原始 MSS 已经接近 1500（标准以太网 MTU），加上头之后会变成 1520+，超过链路 MTU 后会被中间路由器**直接丢弃而不通知**（很多跨境节点为了效率不发 ICMP 分片需求）。

**症状**：握手包能过（小包），但加载 Gemini 这种 JS 重型网页时打不开——浏览器卡在 "Identifier '...' has already been declared" 这种 SyntaxError，因为 JS 脚本只下了一半。

**修复**（管理员 PowerShell）：

```powershell
# 先看你的网卡叫什么
netsh interface ipv4 show subinterfaces

# 把 MTU 调到 1400，留出 100 字节给加密层
netsh interface ipv4 set subinterface "以太网" mtu=1400 store=persistent
```

客户端的虚拟网卡（TUN 模式下）也要同步：在 v2rayNG 里把 TUN MTU 设为 **1280**（比物理网卡更小，预留余量）。

### 6.2 Windows TCP 接收窗口

```powershell
# 自动调整 TCP 接收窗口，让发送方能在收到 ACK 前发送更多数据
netsh int tcp set global autotuninglevel=normal
# 启用直接缓存访问，减少 CPU 处理小包的开销
netsh int tcp set global dca=enabled
```

WSL1 没法开 BBR，但 Windows 这一层的优化能把跨海传输的实际吞吐量从几 Mbps 拉到 20+ Mbps。

### 6.3 Gemini 专属：禁用 QUIC

Google 全家桶（包括 Gemini）默认走 QUIC（UDP 443）。但跨境 UDP 在国内几乎全是丢包重灾区。两种解决：

1. **客户端层面**：在 Shadowrocket 的规则里加 `DEST-PORT,443,REJECT` 针对 UDP，或者关闭"启用 UDP 转发"。
2. **浏览器层面**：Chrome 地址栏 `chrome://flags`，搜 `quic`，设为 Disabled。

被禁掉之后浏览器会立即降级到 TCP（HTTPS），跑在你已经调好的 REALITY 通道上。

---

## 7. 第四阶段：Sunshine + Wake-on-LAN 远程串流

代理跑稳之后，下一个目标是出门也能用——**电脑关机时把它叫醒，串流回桌面**。

### 7.1 BIOS 设置

WoL 的核心是：**关机时网卡依然通电监听**。

- **BIOS**：开启 `Wake on LAN`，关闭 `ErP Ready`（ErP 会在关机时切断网卡供电）。

### 7.2 网关 ARP 缓存的"失忆症"——用广播地址绕过

电脑关机后没有 IP 协议栈，路由器在 10-15 分钟后会清掉 ARP 表，于是不知道 `10.1.10.10` 对应哪块网卡，魔术包送不到。在能做 Address Reservation 的固件上，这个问题不存在；但前面提过，**这台被 Comcast provisioning 过的 CG3000D 固件里根本没有这个选项**——所以 DMZ 在长时间关机后会"忘记"目标。

**解法**：在 Netgear 端口转发里加一条**指向广播地址**的规则：

| 字段 | 值 |
|---|---|
| 协议 | UDP |
| 外部端口 | 9 |
| 内部 IP | `10.1.10.255`（局域网广播地址） |
| 内部端口 | 9 |

这样唤醒包来了之后，Netgear 直接在 LAN 里"群发"，所有网卡都收到，但**只有 MAC 地址匹配 `XX:XX:XX:XX:XX:XX` 的那块网卡会被唤醒**。这套方法即使关机一个月也照样有效，因为它根本不依赖 ARP 表。

### 7.3 测试流程

1. 关机，观察机箱后面的网口指示灯——绿/橙灯应该还在微弱闪烁。
2. 手机断 Wi-Fi，切换到 5G，**关闭 v2rayNG**（唤醒包不需要走代理）。
3. 用 WoL App（如 PingTools）填：
   - 域名：`home.example.org`
   - MAC：`XX:XX:XX:XX:XX:XX`
   - 端口：UDP 9
4. 等 1-2 分钟，看 `access.log` 是否开始跳动。

---

## 8. 第五阶段：Sunshine 配置与 Moonlight 跨境串流

Sunshine 是 Moonlight 的开源服务端，本身已经做了完善的加密握手，**不需要再套一层代理**——套了反而延迟翻倍。

### 8.1 关键配置点

- **网络绑定**：在 `https://localhost:47990` 的 Settings → Network 里，确保 Network Interface 绑定的是 Realtek（或者留空让它自动）。
- **加密**：`LAN Encryption Mode` 设为 Disabled，能减轻手机端解码负担（外网流量本身已经 Sunshine 加密）。
- **防火墙**：因为以太网换 Wi-Fi 时 Windows 会把网络识别成"公用"，必须放行所有配置文件：

```powershell
New-NetFirewallRule -DisplayName "Sunshine-TCP" -Direction Inbound -Action Allow `
    -Protocol TCP -LocalPort 47984,47989,47990,48010 -Profile Any
New-NetFirewallRule -DisplayName "Sunshine-UDP" -Direction Inbound -Action Allow `
    -Protocol UDP -LocalPort 47998,47999,48000,48002,48010 -Profile Any
```

### 8.2 局域网搜不到？手动添加

Moonlight 的自动发现走 mDNS 广播，跨网段（手机在 Wi-Fi、PC 在以太网）经常失败。直接点 Moonlight 右上角"+"手动输入 `10.1.10.10`，电脑屏幕会立刻弹 4 位 PIN 配对码。

### 8.3 跨境串流的现实

300ms 延迟下不要追求高画质：

- 码率：5-10 Mbps（不是 50 Mbps，Comcast 上行带宽会哭）。
- 分辨率：先从 720p 60fps 起步。
- 编码：强制 HEVC（H.265），同等画质带宽小一半。

### 8.4 一个反直觉的故障

第一次连成功后，进了登录界面又断开了。日志报：

```
Error: [code: 1610] 这个产品的配置数据已损坏。请与技术支持人员联系。
failed to set display mode!
```

Sunshine 在串流前会尝试**修改主机显示器分辨率以匹配客户端**（比如把 1080p@120 改成 480p@30 减带宽）。在多显示器、AMD 集显、远程关闭物理显示器的场景下，这个修改经常失败。两个解决方向：

1. 在 Sunshine 设置里关掉 "Use Display Device Settings" 之类的选项。
2. 加一个 HDMI 显卡欺骗器（Dummy Plug）或者装 IDD Sample Driver 虚拟显示器，让系统始终认为有一块"正经的"显示器在线。

---

## 9. 第六阶段：自动化——让这套系统自我维护

到这里所有功能都跑通了，但**只在我手动启动 WSL 终端、手动 `xray run` 的前提下**。如果家里突然停电、Windows 自动更新重启了就寄。

### 9.1 WSL 守护脚本 `/root/daemon.sh`

```bash
#!/bin/bash
mkdir -p /var/log/xray

# 1. 同步 IP 到 Cloudflare
/bin/bash /root/cf-ddns.sh >> /var/log/ddns_update.log 2>&1

# 2. Xray 进程保活
if ! pgrep -x "xray" > /dev/null; then
    /usr/local/bin/xray run -config /usr/local/etc/xray/config.json \
        >> /var/log/xray/error.log 2>&1 &
fi

# 3. 日志轮转：超过 100MB 就清空
find /var/log/xray/ -name "*.log" -size +100M -exec truncate -s 0 {} \;
```

### 9.2 WSL1 的 cron 必须手动启动

WSL1 没有 systemd，`cron` 不会随 Windows 启动而自启。`crontab -e` 的内容很简单：

```cron
*/2 * * * * /bin/bash /root/daemon.sh > /dev/null 2>&1
```

每 2 分钟跑一次：`*/1` 太频繁会让 cron 自己累、`*/5` 太慢导致 IP 变了之后掉线时间长。

### 9.3 Windows 任务计划程序：登录时点火

让 Windows 在登录时自动启动 WSL、自动开 cron、自动跑一次 `daemon.sh`：

**关键参数：**

- 触发器：登录时 + 延迟 30 秒（等网络驱动起来）。
- 操作 → 程序：`C:\Users\<You>\Documents\wsl_autostart.bat`
- 操作 → 起始于：`C:\Users\<You>\Documents`（**不要加引号**）。

### 9.4 wsl_autostart.bat

```bat
@echo off
start wt -p "Ubuntu" wsl -u root tail -f /var/log/xray/access.log ^; ^
split-pane -V -p "Ubuntu" wsl -u root tail -f /var/log/xray/error.log ^; ^
split-pane -H -p "Ubuntu" wsl -u root sh -c "service cron start \; /bin/bash /root/daemon.sh \; exec /bin/bash"
```

`.bat` 里用 `^;` 是把分号转义传给 wt，`.bat` 里写的 `^` 是行延续符——两层转义不能漏。

---

## 10. 完整的"开机即用"流程

到这里，整个系统的工作流是：

```
[出门在外的我]
  ↓ 手机 5G 发送 WoL Magic Packet 到 home.example.org:9
[Cloudflare DDNS]
  ↓ 解析到 73.x.x.x（家宽公网 IP）
[Comcast 网关]
  ↓ UDP 9 转发到 10.1.10.255 局域网广播
[Realtek 网卡]
  ↓ MAC 匹配，唤醒主板
[Windows 启动]
  ↓ netplwiz 自动登录（无需 PIN）
  ↓ 等待 30 秒（网络栈、WSL 启动）
  ↓ 任务计划程序触发 wsl_autostart.bat
[Windows Terminal 弹出三分栏]
  ↓ access.log + error.log + 控制台
[控制台执行 wsl_startup.sh]
  ↓ service cron start
  ↓ daemon.sh 同步 DDNS、拉起 Xray
[此时国内的 iPad]
  ↓ Shadowrocket 连接 home.example.org:443
  ↓ REALITY 握手成功，access.log 开始滚动
[此时移动设备]
  ↓ Moonlight 连接 home.example.org
  ↓ 4 位 PIN 配对（首次）
  ↓ 480p/720p HEVC 串流，码率 5-10Mbps
```

整套系统在我不在家的时候完全自我维护。哪怕家里停电重启、Comcast 给我换了 IP、Windows 强制更新了，只要电源恢复 + 网线还插着，2 分钟内一切都会回到正轨。

---

## 11. 一些回头看的反思

**这套方案适合什么人？** 已经有美国住宅宽带、且至少**能控制网关**（DMZ 或桥接权限）的人。如果你只能用公寓提供的统一网络、拿不到公网 IP，老老实实用 Cloudflare Tunnel + 优选 IP 才是正途。

**REALITY 真的"无敌"吗？** 不是。它只是把"探测者扫描"和"识别代理流量"这两件事的难度提到了非常高。但如果你的 IP 出现在某些"已知代理"数据库里、或者每天产生 TB 级流量，照样会被人工干预。**克制流量、别开 P2P 下载，是这种家用方案能长期跑下去的前提**。

**为什么不用现成的 GUI 工具一键部署？** 因为我想搞清楚每一层在做什么。半年后这套东西出问题时，"不知道哪里坏了"的恐惧远比"花一个周末手动配"要痛苦得多。

---

*感谢 Gemini 在整个调试过程中的耐心陪练。这种"边问边搭"的方式让我第一次切实感受到大模型作为协作伙伴而非搜索引擎的价值——它不会嘲笑我把 WLAN 和"以太网 3"搞混，也不会在我连续问八遍"为什么 SNI 是微软"时失去耐心。*

*同时感谢 Claude（Opus 4.7，1M context）把那份将近一万行、四十多万字的 Gemini 对话日志一口气咀嚼下来，按时间顺序梳理出因果链，删掉重复的死胡同，识别出哪些"祖传密码"和"广播地址 trick"是真正值得记录的亮点，再帮我做完隐私脱敏。把"原始日志"变成"博客"这件事本身——挑选叙事节奏、决定哪些坑该详写哪些一笔带过、给每个章节起标题——是这次写作里我最不想自己做的部分，也是它做得最好的部分。*
