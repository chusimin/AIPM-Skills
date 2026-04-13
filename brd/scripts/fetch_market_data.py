#!/usr/bin/env python3
# fetch_market_data.py — BRD/MRD 通用市场数据爬虫
# 功能：给定关键词，从 DuckDuckGo HTML 搜索接口采集原声数据，
#      按来源平台自动打索引前缀（X/R/Z/H/W），输出到 ./market_data/。

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少依赖，请先运行：pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

DDG_HTML_URL = "https://html.duckduckgo.com/html/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 域名 → 索引前缀映射
DOMAIN_PREFIX = {
    "x.com": "X",
    "twitter.com": "X",
    "reddit.com": "R",
    "old.reddit.com": "R",
    "zhihu.com": "Z",
    "xiaohongshu.com": "H",
    "xhslink.com": "H",
    "producthunt.com": "P",
    "hackernews.com": "N",
    "news.ycombinator.com": "N",
    "medium.com": "M",
    "juejin.cn": "J",
    "csdn.net": "C",
    "weibo.com": "B",
}
DEFAULT_PREFIX = "W"  # Web 通用


def get_prefix(url: str) -> str:
    """根据 URL 域名返回索引前缀。"""
    try:
        host = urlparse(url).netloc.lower()
        host = host.replace("www.", "")
        for domain, prefix in DOMAIN_PREFIX.items():
            if domain in host:
                return prefix
        return DEFAULT_PREFIX
    except Exception:
        return DEFAULT_PREFIX


def ddg_search(keyword: str, max_results: int = 15) -> list:
    """调用 DuckDuckGo HTML 搜索接口，返回结果列表。"""
    params = {"q": keyword, "kl": "cn-zh"}
    try:
        resp = requests.post(DDG_HTML_URL, data=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[警告] DuckDuckGo 搜索失败: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for result in soup.select("div.result")[:max_results]:
        title_el = result.select_one("a.result__a")
        snippet_el = result.select_one("a.result__snippet")
        if not title_el:
            continue
        url = title_el.get("href", "")
        title = title_el.get_text(strip=True)
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
        if url:
            results.append({"title": title, "url": url, "snippet": snippet})
    return results


def fetch_page_text(url: str, max_chars: int = 1500) -> str:
    """抓取网页正文片段（用于佐证原声）。失败则返回空串。"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return ""
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{2,}", "\n", text)
    return text[:max_chars]


def collect(keywords: list, max_per_keyword: int = 10, deep_fetch: bool = True) -> list:
    """按关键词列表采集数据，自动去重、打索引前缀。"""
    all_items = []
    seen_urls = set()
    prefix_counter = {}

    for kw in keywords:
        print(f"[搜索] {kw}", file=sys.stderr)
        results = ddg_search(kw, max_results=max_per_keyword)
        time.sleep(1.5)  # 礼貌延时

        for r in results:
            if r["url"] in seen_urls:
                continue
            seen_urls.add(r["url"])

            prefix = get_prefix(r["url"])
            prefix_counter[prefix] = prefix_counter.get(prefix, 0) + 1
            idx = f"{prefix}{prefix_counter[prefix]}"

            item = {
                "id": idx,
                "keyword": kw,
                "title": r["title"],
                "url": r["url"],
                "snippet": r["snippet"],
                "excerpt": "",
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            if deep_fetch:
                excerpt = fetch_page_text(r["url"])
                item["excerpt"] = excerpt
                time.sleep(0.8)

            all_items.append(item)

    return all_items


def write_outputs(items: list, out_dir: str):
    """写入 JSON + Markdown 两种格式。"""
    os.makedirs(out_dir, exist_ok=True)

    # JSON
    json_path = os.path.join(out_dir, "raw_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # Markdown
    md_path = os.path.join(out_dir, "raw_data.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 原始数据采集结果\n\n")
        f.write(f"> 采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> 数据条数：{len(items)}\n")
        f.write(f"> 索引前缀说明：X=X/Twitter, R=Reddit, Z=知乎, H=小红书, "
                f"P=ProductHunt, N=HackerNews, M=Medium, J=掘金, C=CSDN, B=微博, W=其他网页\n\n")
        f.write("---\n\n")
        f.write("## 结论引用规则\n\n")
        f.write("在 BRD/MRD 报告中，每个结论后面应挂数据索引，例如：\n")
        f.write("`核心痛点是信息过载 [X3, R1, W5]`\n\n")
        f.write("---\n\n")

        for item in items:
            f.write(f"### [{item['id']}] {item['title']}\n\n")
            f.write(f"- **搜索关键词**：{item['keyword']}\n")
            f.write(f"- **来源 URL**：{item['url']}\n")
            f.write(f"- **采集时间**：{item['fetched_at']}\n\n")
            if item["snippet"]:
                f.write(f"**搜索摘要**：\n\n> {item['snippet']}\n\n")
            if item["excerpt"]:
                excerpt_clean = item["excerpt"].replace("\n", "\n> ")
                f.write(f"**正文节选**：\n\n> {excerpt_clean}\n\n")
            f.write("---\n\n")

    print(f"[完成] JSON: {json_path}", file=sys.stderr)
    print(f"[完成] MD:   {md_path}", file=sys.stderr)
    print(f"[完成] 共采集 {len(items)} 条数据", file=sys.stderr)
    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(
        description="BRD/MRD 通用市场数据爬虫（DuckDuckGo + 网页正文提取）"
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="搜索关键词（可多个，用空格分隔）",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=10,
        help="每个关键词最多采集结果数（默认 10）",
    )
    parser.add_argument(
        "--out",
        default="./market_data",
        help="输出目录（默认 ./market_data）",
    )
    parser.add_argument(
        "--no-deep",
        action="store_true",
        help="跳过正文抓取（只保留搜索摘要，速度更快）",
    )
    args = parser.parse_args()

    print(f"[启动] 关键词：{args.keywords}", file=sys.stderr)
    items = collect(
        keywords=args.keywords,
        max_per_keyword=args.max,
        deep_fetch=not args.no_deep,
    )
    if not items:
        print("[错误] 未采集到任何数据，请检查网络或更换关键词", file=sys.stderr)
        sys.exit(2)
    write_outputs(items, args.out)


if __name__ == "__main__":
    main()
