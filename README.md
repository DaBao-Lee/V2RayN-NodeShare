# 🌐 V2RayN Node Share

> A self-updating, base64-encoded free proxy subscription for **v2rayN / v2rayNG / NekoBox / FlClash / Shadowrocket**, built by crawling public Chinese node-sharing sites and merging their latest drops into one de-duplicated list.

**Subscription URL** — paste this into any client that accepts a base64 subscription:

```
https://raw.githubusercontent.com/DaBao-Lee/V2RayN-NodeShare/main/base64
```

The file is a standard subscription body: one single base64 string that decodes to newline-separated share links (`vless://…`, `trojan://…`, `ss://…`, …). Clients decode it automatically; you do **not** need to import the individual links by hand.

---

## 📑 Contents

- [What's inside the subscription](#-whats-inside-the-subscription)
- [中文快速上手](#-中文快速上手)
- [Import guide by client](#-import-guide-by-client)
- [Clash / Mihomo users](#-clash--mihomo-users)
- [How the list is produced](#-how-the-list-is-produced)
- [Run the crawler yourself](#-run-the-crawler-yourself)
- [Update policy and freshness](#-update-policy-and-freshness)
- [Troubleshooting and FAQ](#-troubleshooting-and-faq)
- [Security and privacy notes](#-security-and-privacy-notes)
- [More free node sources](#-more-free-node-sources)
- [Client downloads](#-client-downloads)
- [Recommended routing and DNS setup](#-recommended-routing-and-dns-setup)
- [Support this project](#-support-this-project)

---

## 📦 What's inside the subscription

The published list is the newest batch from every upstream, merged and de-duplicated, so its exact contents rotate daily. What stays stable is its **shape**:

**Format**

- One base64 blob that decodes to newline-separated share links — the canonical subscription body v2rayN / v2rayNG / NekoBox / Shadowrocket expect. No per-link importing needed.
- Link families you can run into in any batch: `vless://` (usually the majority, Reality handshakes included), `trojan://`, `ss://`, `anytls://`, `hysteria2://`, `vmess://`, and the occasional `socks://`. Which ones appear depends on what the sources published that day.
- Each link keeps the upstream `#name` fragment, typically a region label plus the source site, so the client's server list reads like `US美国(mibei77.com 米贝节点分享)`.

**Transport**

- Overwhelmingly TLS-based and usually on 443-like ports, which is what lets the traffic sit on top of ordinary HTTPS on restrictive networks.
- WebSocket is the most common wrapper; a portion of the VLESS set uses Reality; Hysteria2 and AnyTLS are newer cores-only protocols.
- A share of the links carry `insecure=1` / skip-cert verification — read [Security and privacy notes](#-security-and-privacy-notes) before trusting those.

**Geography**

- Labels cover the usual free-node pool: the United States and Europe (Germany, Netherlands, France, Poland, …), East and South-East Asia (Hong Kong China, Japan, Taiwan China, Singapore, Malaysia, …), plus Russia, Canada, India and one-off locations.
- A region label is the upstream operator's own tag, not a verified geolocation lookup, and free nodes change hosts constantly — trust the latency test over the name.

**What is not promised**

- No bandwidth, uptime or IP-quality guarantee, and no guarantee that any node unblocks a specific streaming or AI service. Free shared IP pools get flagged and rotated continuously.

---

## 🀄 中文快速上手

1. 复制订阅地址：`https://raw.githubusercontent.com/DaBao-Lee/V2RayN-NodeShare/main/base64`
2. **v2rayN（Windows）**：`订阅服务器地址` → 粘贴 → 确定；然后 `服务器` → `测速` → 全部测速，右键延迟最低的节点 `设为活动服务器`。
3. **v2rayNG / NekoBox（Android）**：右上角订阅菜单 → `添加订阅` → 粘贴 URL → 保存后下拉刷新，再执行一次测速。
4. **Shadowrocket / Stash（iOS）**：`添加订阅` → 类型选默认，粘贴 URL 即可。
5. 用**规则模式 / 分应用代理**，不要开全局：让国内流量直连，只让需要代理的域名走节点，速度和兼容性都会更好。
6. 连不上时先做三件事：更新订阅 → 换节点 → 换协议（`hysteria2` 不通就切 `vless`/`trojan`）。免费节点失效是常态，不是你的网络坏了。

---

## 💻 Import guide by client

| Client | Platform | How to add |
|--------|----------|------------|
| **v2rayN** | Windows | `订阅` → `添加订阅服务器` → paste URL → `服务器` → `测速` |
| **v2rayNG** | Android | Subscription screen → `+` → paste URL → refresh → speed test |
| **NekoBox / Hiddify** | Android / iOS / desktop | Profiles → add subscription URL |
| **FlClash** | Android / desktop | Config → add remote profile with the URL |
| **Shadowrocket** | iOS | `订阅` → `添加订阅` → paste URL |
| **Stash / Surge** | iOS | Needs a YAML config — see [Clash users](#-clash--mihomo-users) |
| **sing-box** | All | Use a `url` subscription block pointing at the same URL, or import per-protocol |

After importing, always run a **latency test** and pick the lowest working node. Free node lists are ordered by source, not by quality.

---

## 🧩 Clash / Mihomo users

The published `base64` file is a **share-link subscription**, which Clash-family clients cannot consume directly — they need a YAML config with `proxies:` / `proxy-groups:`.

Two options:

1. **Use the daily Clash Meta YAML from this repo.** Each crawler run also downloads the upstream Clash config, committed under `nodes_output/*_clash.yaml`. Browse [the folder on GitHub](https://github.com/DaBao-Lee/V2RayN-NodeShare/tree/main/nodes_output) and open the newest file, or fetch it raw:
   ```
   https://raw.githubusercontent.com/DaBao-Lee/V2RayN-NodeShare/main/nodes_output/<site>_<n>_<date>_..._clash.yaml
   ```
   ⚠️ The filename changes every day, so copy the URL from the folder listing rather than pinning it in a client.
2. **Convert the subscription locally** with any link→YAML tool (e.g. `subconverter`, `v2ray-rules-dat` + a generator template) and add your own rules.

Kernel support caveat: `anytls://` and VLESS-Reality need a recent mihomo / sing-box core. Older Clash kernels drop those nodes without warning, which makes a subscription look "partly broken".

---

## ⚙️ How the list is produced

```
V2RayN-NodeShare/
├── node_get.py          # crawler: fetch → extract links → download → merge → base64
├── nodes_output/        # raw daily drops from each source (.txt share links + .yaml Clash)
│   ├── yudou789_1_..._v2ray.txt   /  yudou789_1_..._clash.yaml
│   └── mibei77_1_..._v2ray.txt    /  mibei77_1_..._clash.yaml
├── base64               # ← the published subscription (merged + de-duplicated, base64)
├── update.bat           # git add -A → dated commit → push
└── README.md
```

`node_get.py` runs this pipeline:

1. **Clean** `nodes_output/` (all `.txt` / `.yaml` / `.yml`) so a run never mixes stale days together.
2. **Crawl** the listing pages of [`yudou789.top`](https://www.yudou789.top/) and [`mibei77.com`](https://www.mibei77.com/category/jiedian), taking the two newest posts from each.
3. **Extract** both subscription links from each post body. Upstream pages often glue the `.txt` and `.yaml` URLs together with no whitespace, so the parser splits on every `http` occurrence before matching — otherwise one regex swallows both links into garbage.
4. **Download** each `.txt` (V2Ray / Shadowrocket / NekoBox style) and each `.yaml` (Clash Meta) into `nodes_output/`.
5. **Merge and publish**: decode every `.txt` (some sources already serve plaintext), de-duplicate share links while preserving first-seen order, base64-encode the whole set, and write it to `base64` in the repo root. If a run yields nothing, the previous `base64` is left untouched rather than blanked.
6. **Publish** with `update.bat`, which stages everything, commits with a timestamped message, and pushes.

There is no GitHub Actions here: updates are pushed from a local machine whenever the crawler is re-run.

---

## 🔁 Run the crawler yourself

```bash
pip install requests beautifulsoup4
python node_get.py
```

Knobs worth knowing inside [node_get.py](node_get.py):

| Name | Default | Purpose |
|------|---------|---------|
| `NodeCrawler(output_directory=...)` | `nodes_output` | Where raw drops land |
| `crawler.run(limit=...)` / `crawl_*(limit=...)` | `2` | Newest posts per source |
| `BASE64_OUTPUT_FILE` | `<repo root>/base64` | Published subscription path |
| `TIMEOUT_SECONDS` | `10` | Per-request HTTP timeout |
| `clean_existing_nodes(...)` | called first in `__main__` | Wipe previous run's files |
| `write_base64_subscription(...)` | step 3 of `run()` | Merge + encode only, no crawling |

If you want the merge step without re-crawling (files already in `nodes_output/`):

```bash
python -c "import node_get; node_get.write_base64_subscription()"
```

---

## 🕒 Update policy and freshness

- Nodes are refreshed whenever the crawler runs — realistically **once a day**, since both upstream sites publish a fresh batch daily.
- Every published set is the **latest two posts of each source**, so a single batch stays reachable for roughly two days before it rolls off.
- GitHub raw responses are cached by CDN and by clients for a few minutes. After an update, force a re-import (or wait) rather than assuming the list is stale.
- Free nodes die fast. Only a fraction of any batch stays alive for long — re-measure latency instead of trusting yesterday's pick, and keep a second source as backup.

---

## ❓ Troubleshooting and FAQ

**Imported the subscription but nothing connects.**
Most often the client is pinned to a dead node. Re-import, run a full latency test, and switch the active server. Then check that your client version supports the protocol families in use (AnyTLS and Reality need recent builds).

**Everything is slow / 0 ms / red.**
Free shared IP pools are frequently flagged by the services you want. Try a different region, prefer port 443 TLS nodes on congested networks, and avoid `hysteria2`/QUIC where UDP is shaped.

**`hysteria2` and `socks` nodes fail but `vless` works.**
Expected on captive networks: QUIC and plain SOCKS get dropped, TLS-on-443 does not.

**What does `insecure=1` in some links mean?**
The client skips TLS certificate verification for that node. It keeps the tunnel encrypted but cannot prove who is at the other end — fine for casual browsing, wrong for anything secret. Prefer nodes with a real `sni=` and valid certificates.

**Some nodes have no name.**
Upstream occasionally omits the `#fragment`. The link still works, it just shows up unlabelled in the server list.

**Will these play 4K or unblock Netflix?**
Sometimes, on the faster nodes — but no node is guaranteed to unblock a specific service, and free IP pools get flagged quickly. Sort by latency, then test the handful of low-delay nodes against the service you actually care about.

**Duplicate nodes across days?**
De-duplication is on the exact share link, so a node whose parameters changed counts as new. Same name + different host/port = different entry, by design.

**The `base64` file looks like gibberish when I open it.**
Correct — it is base64. Decode it locally if you want to read the raw links:
```bash
python -c "import base64;print(base64.b64decode(open('base64').read()).decode()[:400])"
```

**Why are some upstream posts behind a "hidden content" block?**
Those sites gate their newest links. The crawler reads the hidden block when present and falls back to the visible article body, so a post with an unlocked link can still be harvested.

---

## 🔒 Security and privacy notes

- **Free nodes are shared infrastructure.** The operator of the exit server can see your connection metadata and, without further encryption above the proxy, the hosts and contents of your traffic. Treat a free node as a *route*, not as a VPN provider with a privacy promise.
- **Nothing here is audited.** Links are scraped from third-party aggregators; upstream pages may also carry ads and redirects. This repo does not host or control the exit servers.
- **Don't use these nodes for credentials, banking, or anything you would not show a stranger**, and prefer sites that enforce HTTPS of their own.
- **Skip-cert links (`insecure=1`, `skip-cert-verify`)** disable identity checking. Count them, and know which ones you are using.
- **Use rule / per-app mode rather than global proxying** — less traffic through someone else's server, fewer leaks, better speed.
- Availability, speed, and unblocking behaviour are **not guaranteed**. Everything is provided as-is, with no warranty and no SLA.

---

## 📡 More free node sources

Diversify so one dead upstream does not end your connectivity:

| Provider | Link |
|----------|------|
| 🎯 85la | <https://www.85la.com/> |
| 🐣 xiaoqie | <https://lovetoshare.top/> |
| 🧠 kejiwangluo | <https://www.xinye.eu.org/> |
| 🐙 yudoutu | <https://www.yudou123.top/> |
| ⚡ runfacishan | <https://d.zrf.me/vless-base64> |
| 🌀 ripaojiedian | <https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub> |

The last two are ready-to-paste subscription URLs; the rest are sites that publish daily posts.

---

## 🎥 YouTube-based node providers

Creators who regularly publish links and walkthroughs — useful when a scraped list goes stale:

| 🎬 Channel | 🔗 Link |
|------------|---------|
| 🌊 Yudou | [@yudou](https://www.youtube.com/@yudou) |
| 🚀 ZYFXS | [@ZYFXS](https://www.youtube.com/@ZYFXS) |
| ⚡ Kuaizui | [@kuaizui](https://www.youtube.com/@kuaizui) |
| 🔐 SFZY666 | [@SFZY666](https://www.youtube.com/@SFZY666) |
| 🧠 Andy_Web3 | [@Andy_Web3](https://www.youtube.com/@Andy_Web3) |
| 🧭 Independent Thinking | [@独立思维-online](https://www.youtube.com/@独立思维-online) |
| 📦 Resource Sharing Hub | [@ziyuanfenxiangba](https://www.youtube.com/@ziyuanfenxiangba) |

Subscription links are usually in the video description.

**Featured tutorials**

- [Use Cloudflare Worker To Generate V2ray VLESS Nodes](https://www.youtube.com/watch?v=OOwRoP_SWzk) — run your own exit instead of trusting strangers
- [v2rayN 电脑和手机使用教程，手把手演示](https://www.youtube.com/watch?v=F02YldyO6sk) — desktop + mobile setup
- [最新版 V2rayN 使用教程：导入节点的 4 个方法](https://www.youtube.com/watch?v=Axtc-pfua5w&pp=0gcJCfcAhR29_xXO) — import methods and node groups
- [2025 新版 v2rayN 使用教程，功能优化](https://www.youtube.com/watch?v=M0xbnQTPCCc) — newer build features

---

## 💻 Client downloads

| Platform | Build |
|----------|-------|
| 💻 Windows | [v2rayN releases](https://github.com/2dust/v2rayN/releases) |
| 🐧 Linux | [v2rayN for Linux](https://github.com/2dust/v2rayN/releases) |
| 📱 Android | [v2rayNG](https://github.com/2dust/v2rayNG/releases) |
| 🍎 iOS | Search **Shadowrocket** or **Stash** in the App Store (usually requires an Apple ID from a non-CN region) |
| 🖥 Cross-platform GUI | [FlClash](https://github.com/chen08209/FlClash/releases), [Hiddify](https://github.com/hiddify/hiddify-next/releases) |

> Download clients only from their official repositories. Third-party "v2rayN" builds are a common malware vector, and a tampered client can read every subscription you import.

---

## ⚙️ Recommended routing and DNS setup

**Routing.** Use per-app routing / rule mode instead of global proxy. Domestic traffic goes direct; only the domains you actually need proxied leave through the node. This is the single biggest speed and compatibility win, especially for messaging apps and AI sites.

**DNS.** Split DNS keeps Chinese domains resolving locally and international ones resolving through the proxy, which removes most "the node works but sites hang" cases:

```json
"dns": {
  "hosts": {
    "dns.google": "8.8.8.8",
    "dns.pub": "119.29.29.29",
    "dns.alidns.com": "223.5.5.5",
    "geosite:category-ads-all": "127.0.0.1"
  },
  "servers": [
    {
      "address": "https://1.1.1.1/dns-query",
      "domains": ["geosite:geolocation-!cn"],
      "expectIPs": ["geoip:!cn"]
    },
    "8.8.8.8",
    {
      "address": "114.114.114.114",
      "port": 53,
      "domains": ["geosite:cn", "geosite:category-games@cn"],
      "expectIPs": ["geoip:cn"],
      "skipFallback": true
    },
    {
      "address": "localhost",
      "skipFallback": true
    }
  ]
}
```

**Rule datasets** used by the config above and by most clients:

- 📍 geoip.dat — [download](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat)
- 🌐 geosite.dat — [download](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat)
- 📃 direct-list.txt — [download](https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt)
- 🔐 proxy-list.txt — [download](https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/proxy-list.txt)

---

## 🙌 Support this project

- 🌟 **Star** the repository — it keeps the list discoverable for the next person
- 🍴 **Fork** it to run your own crawler on your own schedule, and open a PR if you add a source
- 🐛 **Open an issue** when the subscription serves nothing usable for a whole day, or when an upstream page changes its markup
- 💬 Share it with people who need it

### 📚 Reference repositories

- 🔗 [2dust/v2rayN](https://github.com/2dust/v2rayN) — the Windows client this list targets
- 🔗 [ripaojiedian/freenode](https://github.com/ripaojiedian/freenode) — long-running free node repo
- 🔗 [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) — geoip / geosite datasets
- 🔗 [shaoyouvip/free](https://github.com/shaoyouvip/free), [johnan0528/v2ray-rules-dat-1](https://github.com/johnan0528/v2ray-rules-dat-1)

---

*Nodes are aggregated from public sources for interoperability testing and personal use. The crawler script and lists are provided as-is, without warranty of availability, speed, or fitness for any purpose.*
