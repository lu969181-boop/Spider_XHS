#!/usr/bin/env python3
"""
小红书自动发布脚本
用法: python3 post.py <图片文件名> <关键词>
示例: python3 post.py 骑手图.jpg 京东外卖
"""

import sys
import os
import random

# 确保从 Spider_XHS 目录运行，保证 JS 文件路径正确
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from apis.xhs_creator_apis import XHS_Creator_Apis


# ── 内容模板库 ─────────────────────────────────────────────────────────────────

TITLE_TEMPLATES = {
    "京东外卖": [
        "打工人必囤！{kw}30分钟送到家，再也不用忍饿开会了",
        "发现宝藏外卖平台｜{kw}全职骑手配送，真的太安心了",
        "午饭再也不踩雷！{kw}这波品质外卖让我彻底回头",
        "懒人福音｜{kw}一键下单，加热餐箱送达比堂食还香",
        "外卖选错平台真的亏！试过{kw}就不想换了",
    ],
    "default": [
        "真的不踩雷｜{kw}亲测好用分享给你们",
        "发现宝藏！{kw}这个细节让我直接回购",
        "打工人必看｜{kw}让我的生活效率翻倍",
        "强烈安利！{kw}用了就停不下来",
        "种草预警｜{kw}真实体验分享来了",
    ]
}

DESC_TEMPLATES = {
    "京东外卖": """姐妹们！今天必须来给{kw}安利一下 🙋

作为一个对外卖品质极度敏感的打工人，我测评过好多平台，{kw}真的是我近期发现的最大惊喜 ✨

📦 【配送体验】
全职骑手+五险一金，不是临时工那种，配送稳定性直接拉满！30分钟极速达，加热餐箱保温，到手还是热乎的 🔥

🍱 【餐品品质】
合作的都是品牌商家，食材新鲜有保障，不会点到那种不知名小店翻车

💰 【价格力道】
新用户有专属优惠，老用户也有积分兑换，性价比超高！

🛡️ 【安心保障】
消毒餐箱、专属工号可查，整个配送流程透明可追溯，吃得放心

说真的，自从用了{kw}，工作日午饭再也不用担心了。点进去试一次，你懂的～ 😌

你们平时点外卖最在意什么？评论区聊聊👇

#{kw}# #外卖推荐# #打工人必备# #品质生活# #外卖好物# #懒人福音# #午餐推荐#""",

    "default": """大家好！今天来分享{kw}的真实使用体验 ✨

作为一个爱研究好物的博主，这次真的发现宝藏了！

✅ 【亮点一】
真实好用，完全超出预期，细节处理得非常到位

✅ 【亮点二】
性价比超高！同类产品横向对比，{kw}在这个价位段完全碾压

✅ 【亮点三】
体验感很丝滑，上手零门槛，新手友好型

✅ 【亮点四】
品质有保障，用了一段时间没有任何翻车，放心推荐

✅ 【亮点五】
售后服务也很好，真正的用户至上理念

坦白说，我已经给好几个朋友安利了，反馈都非常好。感兴趣的姐妹可以冲一波，不会后悔的～ 😊

你们有用过{kw}吗？有什么想聊的欢迎评论区留言👇

#{kw}# #好物推荐# #真实测评# #种草# #生活好物# #安利# #干货分享#"""
}

TOPIC_MAP = {
    "京东外卖": ["京东外卖", "外卖推荐", "打工人", "品质外卖", "懒人必备"],
    "default": ["好物推荐", "真实测评", "种草", "生活好物", "安利"]
}


def generate_content(keyword: str) -> dict:
    """根据关键词生成爆款标题和正文"""
    # 选模板库（精确匹配或 default）
    title_pool = TITLE_TEMPLATES.get(keyword, TITLE_TEMPLATES["default"])
    desc_pool = DESC_TEMPLATES.get(keyword, DESC_TEMPLATES["default"])
    topic_pool = TOPIC_MAP.get(keyword, TOPIC_MAP["default"])

    title = random.choice(title_pool).format(kw=keyword)
    desc = desc_pool.format(kw=keyword)
    topics = topic_pool[:5]  # 最多取 5 个话题

    return {"title": title, "desc": desc, "topics": topics}


def read_cookie(cookie_path: str) -> str:
    with open(cookie_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    if len(sys.argv) != 3:
        print("用法: python3 post.py <图片文件名> <关键词>")
        print("示例: python3 post.py 骑手图.jpg 京东外卖")
        sys.exit(1)

    img_filename = sys.argv[1]
    keyword = sys.argv[2]

    # 路径拼装
    img_path = os.path.expanduser(f"~/Desktop/照片/{img_filename}")
    cookie_path = os.path.join(SCRIPT_DIR, "cookie.txt")

    # 校验图片
    if not os.path.exists(img_path):
        print(f"❌ 图片不存在: {img_path}")
        sys.exit(1)

    # 读取图片
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    print(f"✅ 图片加载成功: {img_path} ({len(img_bytes) // 1024} KB)")

    # 读取 cookie
    cookies_str = read_cookie(cookie_path)
    print(f"✅ Cookie 读取成功（长度 {len(cookies_str)} 字符）")

    # 生成内容
    content = generate_content(keyword)
    print(f"\n📝 生成内容预览")
    print(f"标题: {content['title']}")
    print(f"话题: {content['topics']}")
    print(f"正文（前100字）: {content['desc'][:100]}...")

    # 构建 noteInfo
    note_info = {
        "title": content["title"],
        "desc": content["desc"],
        "postTime": None,       # 立即发布
        "location": None,       # 不设地点
        "type": 0,              # 公开
        "media_type": "image",
        "topics": content["topics"],
        "images": [img_bytes],
    }

    print("\n🚀 开始发布到小红书...")
    try:
        api = XHS_Creator_Apis()
        success, msg, res = api.post_note(note_info, cookies_str)
    except Exception as e:
        print(f"❌ 发布异常: {e}")
        sys.exit(1)

    if success:
        note_id = res.get("data", {}).get("id", "未知")
        print(f"✅ 发布成功！笔记 ID: {note_id}")
        print(f"   链接: https://www.xiaohongshu.com/explore/{note_id}")
    else:
        print(f"❌ 发布失败: {msg}")
        print(f"   完整响应: {res}")
        sys.exit(1)


if __name__ == "__main__":
    main()
