"""
build-index.py — 重建 DeepThink 索引页

扫描 /mnt/user-data/outputs/deepthink/ 下的所有 .html 报告(排除 index.html 自己),
提取每个报告的标题/原始问题/日期/置信度,按 mtime 倒序排,生成 index.html。

用法:
    python build-index.py

可选环境变量:
    DEEPTHINK_OUTPUT_DIR  指定输出目录(默认 /mnt/user-data/outputs/deepthink)
"""
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from html import escape

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "index.html"
OUTPUT_DIR = Path(os.environ.get("DEEPTHINK_OUTPUT_DIR", "/mnt/user-data/outputs/deepthink"))
INDEX_PATH = OUTPUT_DIR / "index.html"


def extract_meta(html_text: str) -> dict:
    """从一份分析报告 HTML 中提取关键元数据。"""
    meta = {"title": "", "question": "", "date": "", "conf_pct": None, "conf_label": ""}

    # h1 标题
    m = re.search(r"<h1[^>]*>(.+?)</h1>", html_text, re.DOTALL)
    if m:
        # 去掉嵌套标签,只保留文字
        meta["title"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()

    # 原始问题:<span class="key">分析问题</span><span class="val">...</span>
    m = re.search(
        r'<span class="key">分析问题</span><span class="val">(.+?)</span>',
        html_text, re.DOTALL,
    )
    if m:
        meta["question"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()

    # 生成日期
    m = re.search(
        r'<span class="key">生成日期</span><span class="val">(.+?)</span>',
        html_text, re.DOTALL,
    )
    if m:
        meta["date"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()

    # 置信度百分比 + label
    m = re.search(r'<span class="conf-percent[^"]*">(\d+)%</span>', html_text)
    if m:
        meta["conf_pct"] = int(m.group(1))
    m = re.search(r'<span class="conf-label">(.+?)</span>', html_text)
    if m:
        meta["conf_label"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()

    return meta


def conf_class(pct):
    if pct is None:
        return "mid"
    if pct >= 70:
        return ""  # good (default green)
    if pct >= 40:
        return "mid"
    return "low"


def render_card(file_path: Path, meta: dict) -> str:
    """渲染单张报告卡片的 HTML。"""
    href = escape(file_path.name)
    title = escape(meta["title"] or file_path.stem)
    question = escape(meta["question"] or "—")
    date = escape(meta["date"] or "—")
    pct = meta["conf_pct"]
    pct_html = f'<span class="pct">{pct}%</span>' if pct is not None else '<span class="pct">—</span>'
    label = escape(meta["conf_label"] or "")
    cls = conf_class(pct)
    dot_cls = f"dot {cls}".strip()

    confidence_block = f"""<span class="card-confidence">
          <span class="{dot_cls}"></span>
          {pct_html}
          <span>{label}</span>
        </span>"""

    return f"""    <a class="card" href="{href}" target="_blank" rel="noopener">
      <div class="card-title">{title}</div>
      <p class="card-question">{question}</p>
      <div class="card-meta">
        <span class="card-date">{date}</span>
        {confidence_block}
      </div>
    </a>"""


def render_empty_state() -> str:
    return """  <div class="empty">
    <div class="icon">📭</div>
    <h2>暂无报告</h2>
    <p>使用 DeepThink 完成第一个问题分析,报告会出现在这里。</p>
  </div>"""


def render_grid(cards: list) -> str:
    if not cards:
        return render_empty_state()
    return '  <div class="grid">\n' + "\n".join(cards) + "\n  </div>"


def main():
    # 准备输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 读模板
    if not TEMPLATE_PATH.exists():
        print(f"❌ 模板缺失: {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # 扫描报告
    reports = []
    for f in OUTPUT_DIR.glob("*.html"):
        if f.name == "index.html":
            continue
        try:
            html_text = f.read_text(encoding="utf-8", errors="ignore")
            meta = extract_meta(html_text)
            mtime = f.stat().st_mtime
            reports.append((f, meta, mtime))
        except Exception as e:
            print(f"⚠️  跳过 {f.name}: {e}", file=sys.stderr)

    # 按 mtime 倒序(最新在前)
    reports.sort(key=lambda x: x[2], reverse=True)

    # 渲染卡片
    cards = [render_card(f, meta) for f, meta, _ in reports]
    content_html = render_grid(cards)

    # 统计信息
    total = len(reports)
    if reports:
        last_mtime = datetime.fromtimestamp(reports[0][2])
        last_updated = last_mtime.strftime("%Y-%m-%d")
    else:
        last_updated = "—"

    # 替换占位符
    output = template
    output = output.replace("{{TOTAL_COUNT}}", str(total))
    output = output.replace("{{LAST_UPDATED}}", last_updated)
    output = output.replace("{{CONTENT}}", content_html)

    # 写入
    INDEX_PATH.write_text(output, encoding="utf-8")
    print(f"✅ 索引已更新: {INDEX_PATH}")
    print(f"   共 {total} 份报告")
    if reports:
        print(f"   最近: {reports[0][1].get('title', reports[0][0].name)} ({last_updated})")


if __name__ == "__main__":
    main()
