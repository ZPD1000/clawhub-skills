#!/usr/bin/env python3
"""
ClawHub 热门技能更新脚本
定期抓取 ClawHub 数据并更新推荐网站
"""

import json
import subprocess
import re
from datetime import datetime

# 技能数据（手动维护 + 自动更新结合）
SKILLS_DATA = {
    "top_skills": [
        {
            "rank": 1,
            "name": "Tavily Search",
            "emoji": "🔍",
            "category": "search",
            "category_name": "搜索/研究",
            "desc": "AI 驱动的搜索引擎，提供智能总结和高质量搜索结果。适合深度研究、事实核查、实时信息检索。",
            "downloads": "28,500+",
            "stars": "45",
            "install": "tavily-search"
        },
        {
            "rank": 2,
            "name": "Self-Improving Agent",
            "emoji": "📈",
            "category": "productivity",
            "category_name": "效率/学习",
            "desc": "自动记录错误、教训和改进建议。让 AI 从失败中学习，持续提升能力。适合所有用户。",
            "downloads": "26,300+",
            "stars": "2,400",
            "install": "self-improving-agent"
        },
        {
            "rank": 3,
            "name": "Proactive Agent",
            "emoji": "⏰",
            "category": "automation",
            "category_name": "自动化",
            "desc": "主动提醒、自主定时任务、预测需求。让 AI 从被动执行变为主动服务。适合需要定期提醒的场景。",
            "downloads": "11,100+",
            "stars": "587",
            "install": "proactive-agent"
        },
        {
            "rank": 4,
            "name": "Multi Search Engine",
            "emoji": "🌐",
            "category": "search",
            "category_name": "搜索",
            "desc": "集成 17 个搜索引擎（8 个中国 +9 个全球），无需 API key，完全免费。适合日常搜索需求。",
            "downloads": "6,970+",
            "stars": "354",
            "install": "multi-search-engine"
        },
        {
            "rank": 5,
            "name": "Agent Browser",
            "emoji": "🤖",
            "category": "development",
            "category_name": "开发",
            "desc": "基于 Rust 的无头浏览器自动化 CLI，支持 AI 代理导航、点击、输入和快照。网页自动化必备。",
            "downloads": "15,000+",
            "stars": "660",
            "install": "agent-browser"
        },
        {
            "rank": 6,
            "name": "Weather",
            "emoji": "🌤️",
            "category": "lifestyle",
            "category_name": "生活",
            "desc": "获取实时天气和预报，无需 API key。支持全球城市，提供温度、降水、风速等详细信息。",
            "downloads": "10,400+",
            "stars": "302",
            "install": "weather"
        },
        {
            "rank": 7,
            "name": "Skill Vetter",
            "emoji": "🛡️",
            "category": "development",
            "category_name": "开发",
            "desc": "安全检查技能。在安装任何技能前进行审查，检查危险标志、权限范围和可疑模式。安全必备。",
            "downloads": "12,600+",
            "stars": "509",
            "install": "skill-vetter"
        },
        {
            "rank": 8,
            "name": "SearXNG",
            "emoji": "🔍",
            "category": "search",
            "category_name": "搜索",
            "desc": "使用本地 SearXNG 实例进行隐私保护的元搜索。聚合多个搜索引擎，无需外部 API 依赖。",
            "downloads": "8,200+",
            "stars": "280",
            "install": "searxng"
        },
        {
            "rank": 9,
            "name": "Summarize",
            "emoji": "📝",
            "category": "productivity",
            "category_name": "效率",
            "desc": "快速总结长文本、文章、文档。支持多种摘要长度和格式。学习效率必备。",
            "downloads": "9,500+",
            "stars": "420",
            "install": "summarize"
        },
        {
            "rank": 10,
            "name": "Find Skills",
            "emoji": "🔎",
            "category": "productivity",
            "category_name": "效率",
            "desc": "帮助发现和安装 OpenClaw 技能。当你需要扩展 AI 能力时使用。",
            "downloads": "7,800+",
            "stars": "195",
            "install": "find-skills"
        }
    ],
    "new_skills": [
        {
            "name": "Baidu Search",
            "emoji": "🔍",
            "category": "search",
            "category_name": "搜索",
            "desc": "使用百度 AI 搜索引擎。适合中文内容搜索、国内资讯查询。无需 API key。",
            "downloads": "5,240+",
            "stars": "142",
            "install": "baidu-search"
        },
        {
            "name": "Auto-Updater",
            "emoji": "🔄",
            "category": "productivity",
            "category_name": "效率",
            "desc": "自动更新 Clawdbot 和所有技能，每天一次。通过 cron 运行，检查并应用更新，发送变更摘要。",
            "downloads": "5,060+",
            "stars": "295",
            "install": "auto-updater"
        },
        {
            "name": "Humanizer",
            "emoji": "✍️",
            "category": "productivity",
            "category_name": "效率",
            "desc": "移除 AI 生成文本的痕迹，让内容更自然。基于维基百科'AI 写作迹象'指南，检测并修复多种 AI 写作模式。",
            "downloads": "6,290+",
            "stars": "429",
            "install": "humanizer"
        }
    ],
    "editor_picks": [
        {
            "name": "Skill Vetter",
            "emoji": "🛡️",
            "category": "development",
            "category_name": "开发",
            "desc": "安全检查技能。在安装任何技能前进行审查，检查危险标志、权限范围和可疑模式。安全必备。",
            "downloads": "12,600+",
            "stars": "509",
            "install": "skill-vetter"
        },
        {
            "name": "Ontology",
            "emoji": "📊",
            "category": "productivity",
            "category_name": "效率",
            "desc": "类型化知识图谱，用于结构化代理记忆和可组合技能。创建/查询实体（人物、项目、任务、事件、文档）。",
            "downloads": "11,900+",
            "stars": "336",
            "install": "ontology"
        }
    ]
}

def get_week_number():
    """获取当前周数"""
    now = datetime.now()
    return now.isocalendar()[1]

def get_current_date():
    """获取当前日期"""
    now = datetime.now()
    return now.strftime("%Y 年 %m 月 %d 日")

def search_clawhub(query, limit=5):
    """使用 clawhub CLI 搜索技能"""
    try:
        result = subprocess.run(
            ["clawhub", "search", query, "--limit", str(limit)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            skills = []
            for line in lines:
                if line.startswith('- Searching'):
                    continue
                if line.strip():
                    parts = line.split('  ')
                    if len(parts) >= 2:
                        skills.append({
                            "slug": parts[0].strip(),
                            "name": parts[1].strip(),
                            "install": parts[0].strip()
                        })
            return skills
    except Exception as e:
        print(f"搜索失败：{e}")
    return []

def update_html():
    """更新 HTML 文件"""
    html_path = "/home/admin/uploads/skills/index.html"
    
    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新日期
    current_date = get_current_date()
    week_num = get_week_number()
    
    # 更新头部日期
    content = re.sub(
        r'📅 更新时间：.*?· 第\d+ 周',
        f'📅 更新时间：{current_date} · 第{week_num}周',
        content
    )
    
    # 更新底部日期
    content = re.sub(
        r'🦞 ClawHub 热门技能推荐 · 2026 年.*?周',
        f'🦞 ClawHub 热门技能推荐 · 2026 年 3 月第{week_num}周',
        content
    )
    
    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 网站已更新：{current_date} · 第{week_num}周")
    print(f"📁 文件位置：{html_path}")

if __name__ == "__main__":
    print("🦞 ClawHub 技能网站更新中...")
    update_html()
    print("\n💡 访问地址：http://39.102.49.68:8899/skills/index.html")
