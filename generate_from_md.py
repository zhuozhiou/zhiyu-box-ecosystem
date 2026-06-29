# -*- coding: utf-8 -*-
from pathlib import Path
import html, re

ROOT = Path('/Users/zhuozhiou/Library/Mobile Documents/iCloud~md~obsidian/Documents/ob')
MD = ROOT / '01-Projects/P3-知遇盒子/知遇盒子-盒子生态.md'
OUT = ROOT / 'github-pages-site/index.html'
text = MD.read_text(encoding='utf-8')
# strip frontmatter
text = re.sub(r'^---\n.*?\n---\n\n?', '', text, flags=re.S)
lines = text.splitlines()

def inline(s):
    s = html.escape(s.strip())
    s = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def is_table_line(s):
    return s.strip().startswith('|') and s.strip().endswith('|')

def split_table_row(s):
    return [c.strip() for c in s.strip().strip('|').split('|')]

body = []
i = 0
open_ul = False
open_section = False

def close_ul():
    global open_ul
    if open_ul:
        body.append('</ul>')
        open_ul = False

def close_section():
    global open_section
    close_ul()
    if open_section:
        body.append('</section>')
        open_section = False

while i < len(lines):
    line = lines[i]
    s = line.strip()
    if not s:
        close_ul(); i += 1; continue
    if s == '---':
        close_section(); body.append('<div class="divider"></div>'); i += 1; continue
    if s.startswith('# '):
        close_section(); body.append(f'<h1 class="doc-title">{inline(s[2:])}</h1>'); i += 1; continue
    if s.startswith('## '):
        close_section(); open_section = True
        sid = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '-', s[3:]).strip('-')
        body.append(f'<section class="section" id="{html.escape(sid)}"><h2>{inline(s[3:])}</h2>')
        i += 1; continue
    if s.startswith('### '):
        close_ul(); body.append(f'<h3>{inline(s[4:])}</h3>'); i += 1; continue
    if s.startswith('#### '):
        close_ul(); body.append(f'<h4>{inline(s[5:])}</h4>'); i += 1; continue
    if is_table_line(s):
        close_ul()
        rows = []
        while i < len(lines) and is_table_line(lines[i].strip()):
            rows.append(split_table_row(lines[i])); i += 1
        if len(rows) >= 2:
            header = rows[0]
            data = rows[2:] if all(re.match(r'^:?-{2,}:?$', c.replace(' ', '')) for c in rows[1]) else rows[1:]
            body.append('<div class="table-wrap"><table>')
            body.append('<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in header) + '</tr></thead>')
            body.append('<tbody>')
            for r in data:
                body.append('<tr>' + ''.join(f'<td>{inline(c).replace("&lt;br&gt;", "<br>")}</td>' for c in r) + '</tr>')
            body.append('</tbody></table></div>')
        continue
    if s.startswith('- '):
        if not open_ul:
            body.append('<ul>'); open_ul = True
        body.append(f'<li>{inline(s[2:])}</li>')
        i += 1; continue
    # indented sub-list lines are rendered as notes
    if s and (line.startswith('  - ') or line.startswith('\t- ')):
        if not open_ul:
            body.append('<ul>'); open_ul = True
        body.append(f'<li class="subitem">{inline(s[2:])}</li>')
        i += 1; continue
    close_ul()
    body.append(f'<p>{inline(s)}</p>')
    i += 1
close_section()
content = '\n'.join(body)

# Extract title/company for hero
hero_title = '知遇盒子 盒子生态'
company = '知遇知行（深圳）科技有限公司'

html_doc = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(hero_title)} - 详细报告版</title>
<style>
:root{{--bg:#f4f7fb;--card:#fff;--ink:#102233;--muted:#5d6b7c;--line:#d8e2ee;--accent:#12395d;--accent2:#2a6ca3;--soft:#edf4fb;--soft2:#f8fbfe;--shadow:0 14px 36px rgba(16,34,51,.06)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:linear-gradient(180deg,#eaf2fa 0,#f4f7fb 220px,#f4f7fb 100%);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;line-height:1.72}}
.page{{max-width:1180px;margin:0 auto;padding:32px 22px 72px}}.hero{{border:1px solid var(--line);border-radius:30px;padding:42px;background:radial-gradient(circle at top right,#d7e8f8 0,#eff6fc 36%,#fff 100%);box-shadow:0 24px 60px rgba(18,57,93,.08)}}
.kicker{{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--accent2);font-weight:900}}h1{{margin:12px 0 8px;font-size:52px;line-height:1.06;letter-spacing:-.035em}}.subtitle{{font-size:18px;color:var(--muted);max-width:980px}}
.meta{{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}}.chip{{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;color:var(--accent);box-shadow:0 6px 18px rgba(16,34,51,.05)}}
.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}}.kpi{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:var(--shadow)}}.kpi .label{{font-size:12px;color:var(--muted);letter-spacing:.14em;text-transform:uppercase;font-weight:900}}.kpi .value{{font-size:26px;font-weight:950;color:var(--accent);margin-top:6px}}
.doc-title{{display:none}}.section{{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px;margin-top:18px;box-shadow:var(--shadow)}}.section h2{{margin:0 0 12px;font-size:22px;color:var(--accent)}}.section h3{{margin:20px 0 8px;font-size:17px;color:#1d4c75}}.section h4{{margin:16px 0 6px;font-size:15px;color:#2a5f8d}}p{{margin:0 0 10px}}ul{{margin:8px 0 12px;padding:0;list-style:none}}li{{position:relative;padding-left:18px;margin:8px 0}}li:before{{content:"";position:absolute;left:0;top:.82em;width:8px;height:8px;border-radius:999px;background:linear-gradient(135deg,var(--accent2),#8fc5ff)}}li.subitem{{margin-left:18px;color:var(--muted)}}
.table-wrap{{width:100%;overflow-x:auto;margin:12px 0 18px;border-radius:16px}}table{{min-width:760px;width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}}th,td{{padding:12px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}}th{{background:var(--soft);text-align:left;color:var(--accent);font-size:13px}}tr:last-child td{{border-bottom:none}}.divider{{height:1px;background:var(--line);margin:18px 0}}.footer{{margin-top:20px;text-align:center;color:var(--muted);font-size:12px}}
@media(max-width:900px){{.page{{padding:16px}}.hero,.section{{padding:18px}}h1{{font-size:38px}}.kpis{{grid-template-columns:1fr 1fr}}}}@media(max-width:560px){{.kpis{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="page">
<section class="hero">
  <div class="kicker">GitHub Pages / Detailed Report</div>
  <h1>知遇盒子<br>盒子生态</h1>
  <div class="subtitle">{html.escape(company)} - 面向高知识密度、强场景需求、具备支付能力行业用户的即插即用 AI 智能硬件终端产品。</div>
  <div class="meta"><span class="chip">法务盒子</span><span class="chip">IP 内容盒子</span><span class="chip">跨境电商盒子</span><span class="chip">深圳创新创业大赛参赛稿</span><span class="chip">自动同步版</span></div>
</section>
<div class="kpis"><div class="kpi"><div class="label">总用户数</div><div class="value">568 户</div></div><div class="kpi"><div class="label">处理案件</div><div class="value">16,701 件</div></div><div class="kpi"><div class="label">Token 消费</div><div class="value">48,433 元</div></div><div class="kpi"><div class="label">省代</div><div class="value">3 个</div></div></div>
{content}
<div class="footer">知遇盒子 盒子生态 · GitHub Pages 自动同步版 · 更新来源：Obsidian Markdown</div>
</div>
</body>
</html>'''
OUT.write_text(html_doc, encoding='utf-8')
print(OUT)
print('contains Yuli:', 'Yuli' in html_doc or '陈裕玲' in html_doc)
print('contains 系列产品:', '知遇盒子系列产品' in html_doc)
