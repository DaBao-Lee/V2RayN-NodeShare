# 🌐 V2RayN Node Share

Premium subscription links offering **fast**, **stable**, and **secure** network connectivity — perfect for streaming, AI applications, and everyday use.

---

## 🔗 Subscription Options

Get started instantly with these high-speed links, optimized for different use cases.

### 🔹 Standard Nodes (4K+)

👉 [Subscribe Now](https://raw.githubusercontent.com/DaBao-Lee/V2RayN-NodeShare/main/base64)  
🌍 Servers deployed in **Singapore** and **Hong Kong**, offering low latency and excellent reliability.

**Best suited for:**
- 📺 Streaming platforms like **YouTube**, **Netflix**, **Disney+**, etc.  
- 🌐 Web browsing, office tools, and general productivity

---

### 🤖 AI-Optimized Nodes (AI+)

👉 [Subscribe for AI](https://raw.githubusercontent.com/DaBao-Lee/V2RayN-NodeShare/main/base64-AI)  
🧠 Specially tuned for intelligent platforms and applications, with balanced speed and latency.

**Recommended for:**
- 💬 Chatbots & AI tools: **ChatGPT**, **Copilot**, **Gemini**, **Grok**, and more  
- ⚙️ Enhancing AI workflows and development environments

---

## 🌟 Additional Free Node Providers

Diversify your connectivity by exploring other active sources:

| Provider Name | Subscription Link |
|---------------|-------------------|
| 🌀 ripaojiedian | https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub |
| ⚡ runfacishan | https://d.zrf.me/vless-base64 |
| 🐙 yudoutu      | https://www.yudou123.top/ |
| 🎯 85la         | https://www.85la.com/ |
| 🧠 kejiwangluo | https://www.xinye.eu.org/ |
| 🐣 xiaoqie     | https://lovetoshare.top/ |

---

## 💻 Client Software Downloads

Quickly set up your client on any device using the latest builds:

| Platform        | Download Link |
|-----------------|----------------|
| 💻 Windows       | [v2rayN for Windows](https://github.com/2dust/v2rayN/releases) |
| 🐧 Linux (.deb)  | [v2rayN for Linux](https://github.com/2dust/v2rayN/releases) |
| 📱 Android APK   | [v2rayNG for Android](https://github.com/2dust/v2rayNG/releases) |

> ⚙️ **Pro Tip:** Use per-app routing instead of global proxy mode.  
> This ensures greater compatibility and efficiency, especially for messaging apps, AI models, and video platforms.

---

## ✨ Key Features

- ✅ 100% free, no ads or paywalls  
- 🔄 Regular updates and active maintenance  
- 💡 Cross-platform support  
- 🚀 Optimized performance for both media consumption and AI workloads  

---

## 📦 Useful Resources

Enhance your setup with these configuration files:

- 📍 geoip.dat: [Download](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geoip.dat)  
- 🌐 geosite.dat: [Download](https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat)  
- 📃 direct-list.txt: [Download](https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt)  
- 🔐 proxy-list.txt: [Download](https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/proxy-list.txt)

---

## 🛠 Example DNS Configuration

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

## 🙌 Support This Project

Found this project useful? Help keep it thriving:

- 🌟 **Star** the repository to help it gain visibility  
- 🍴 **Fork** it to contribute or customize for your own use  
- 💬 Share it with others who might benefit

### 📚 Reference Repositories

Explore related repositories to deepen your understanding:

- 🔗 [shaoyouvip/free](https://github.com/shaoyouvip/free)
- 🔗 [ripaojiedian/freenode](https://github.com/ripaojiedian/freenode)
- 🔗 [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)  
- 🔗 [johnan0528/v2ray-rules-dat-1](https://github.com/johnan0528/v2ray-rules-dat-1)

Your support helps keep the project alive and evolving 🚀

Let me know if you'd like a version tailored for another platform or usage scenario 🚀
