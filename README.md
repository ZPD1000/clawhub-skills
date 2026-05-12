# 🦞 ClawHub 热门技能推荐网站

定期更新最新热门 OpenClaw 技能，让你的 AI 助手真正能打！

## 🌐 在线访问

- **GitHub Pages**: https://zpd1000.github.io/clawhub-skills/
- **国内访问**: http://39.102.49.68:8898/

## 📋 功能特性

- 🔥 **Top 10 热门技能** - 按下载量和星标排序
- 🆕 **新上架技能** - 最新发布
- ⭐ **编辑推荐** - 官方推荐
- 💡 **我的推荐** - 根据场景定制推荐
- 📱 **响应式设计** - 手机/平板/电脑完美适配
- 🎨 **精美 UI** - 渐变背景、卡片式布局

## 🚀 本地部署

### 1. 克隆仓库

```bash
git clone https://github.com/ZPD1000/clawhub-skills.git
cd clawhub-skills
```

### 2. 启动本地服务

```bash
# Python 简单服务器
python3 -m http.server 8898

# 或使用 Node.js
npx serve .
```

### 3. 访问

打开浏览器访问 `http://localhost:8898/`

## 🔄 自动更新

### 设置定时任务

```bash
# 添加 cron 任务（每周五 9:00 自动更新）
crontab -e

# 添加以下内容
0 9 * * 5 python3 /path/to/update_skills.py
```

### 手动更新

```bash
python3 update_skills.py
```

## 📁 文件结构

```
clawhub-skills/
├── index.html          # 主页面
├── update_skills.py    # 自动更新脚本
└── README.md           # 说明文档
```

## 🛠️ 技术栈

- **HTML5 + CSS3** - 响应式布局
- **JavaScript** - 交互功能
- **Python** - 自动更新脚本
- **GitHub Pages** - 静态托管

## 📊 技能分类

| 分类 | 说明 |
|------|------|
| 🔍 搜索/研究 | Tavily Search, Multi Search Engine, SearXNG |
| 📈 效率/学习 | Self-Improving Agent, Auto-Updater |
| ⏰ 自动化 | Proactive Agent |
| 🤖 开发 | Agent Browser, Skill Vetter |
| 🐦 X/Twitter 自动化 | TweetClaw |
| 🌤️ 生活 | Weather |

## 📝 更新日志

- **2026-03-28** - 第 13 周更新
  - 添加自动更新脚本
  - 设置 systemd 服务自启动
  - 部署到 GitHub Pages

- **2026-03-20** - 第 12 周更新
  - 初始版本发布
  - Top 10 热门技能
  - 编辑推荐功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**🦞 Made with ❤️ for OpenClaw Community**
