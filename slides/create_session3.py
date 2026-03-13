# /// script
# requires-python = ">=3.12"
# dependencies = ["python-pptx"]
# ///
"""Generate Claude_session3.pptx matching session1/2 design."""

from pptx import Presentation
from pptx.util import Pt, Emu, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Design tokens ──────────────────────────────────────────
BG_MAIN   = RGBColor(0x1B, 0x19, 0x18)
BG_SECTION = RGBColor(0x23, 0x1F, 0x1D)
CARD_BG   = RGBColor(0x2D, 0x29, 0x26)
CARD_BG2  = RGBColor(0x3A, 0x36, 0x32)
CARD_BG3  = RGBColor(0x30, 0x2D, 0x29)
CARD_BG4  = RGBColor(0x2C, 0x2A, 0x26)

ACCENT    = RGBColor(0xD9, 0x77, 0x57)  # terracotta
ACCENT2   = RGBColor(0x6A, 0x9B, 0xCC)  # blue
ACCENT3   = RGBColor(0x7B, 0xC9, 0xA0)  # green
RED       = RGBColor(0xE0, 0x70, 0x70)

WHITE     = RGBColor(0xFA, 0xF9, 0xF5)
BODY      = RGBColor(0xE0, 0xDE, 0xD8)
MUTED     = RGBColor(0xB0, 0xAE, 0xA5)
MUTED2    = RGBColor(0xC5, 0xC3, 0xBB)
DARK_MUTED = RGBColor(0x6B, 0x69, 0x63)
STRIPE_C  = RGBColor(0x2D, 0x29, 0x26)
LINE_C    = RGBColor(0x4A, 0x47, 0x42)

FONT_JP = "Hiragino Sans"
FONT_EN = "Helvetica Neue"
FONT_CODE = "SF Mono"

SLIDE_W = 12192000
SLIDE_H = 6858000
TOTAL_SLIDES = 19

# ── Helpers ────────────────────────────────────────────────

def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill=None, name=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if name:
        shape.name = name
    return shape


def add_rounded_rect(slide, left, top, width, height, fill=None, name=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if name:
        shape.name = name
    shape.adjustments[0] = 0.04
    return shape


def _set_font(run, font_name, size, bold=False, color=WHITE):
    run.font.name = font_name
    run.font.size = size
    run.font.bold = bold
    run.font.color.rgb = color


def add_textbox(slide, left, top, width, height, text, font=FONT_JP,
                size=Pt(16), bold=False, color=WHITE, align=PP_ALIGN.LEFT,
                name=None, line_spacing=None):
    txbox = slide.shapes.add_textbox(left, top, width, height)
    txbox.fill.background()
    if name:
        txbox.name = name
    tf = txbox.text_frame
    tf.word_wrap = True

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.space_after = Pt(line_spacing)
        run = p.add_run()
        run.text = line
        _set_font(run, font, size, bold, color)
    return txbox


def add_part_label(slide, text):
    return add_textbox(slide, Emu(731520), Emu(365760), Emu(8000000), Emu(274320),
                       text, font=FONT_EN, size=Emu(152400), bold=True, color=ACCENT)


def add_slide_title(slide, text, y=Emu(548640)):
    return add_textbox(slide, Emu(731520), y, Emu(10000000), Emu(548640),
                       text, font=FONT_JP, size=Emu(355600), bold=True, color=WHITE)


def add_page_num(slide, num):
    return add_textbox(slide, Emu(SLIDE_W - 1200000), Emu(SLIDE_H - 400000),
                       Emu(900000), Emu(274320),
                       f"{num} / {TOTAL_SLIDES}", font=FONT_EN,
                       size=Emu(139700), color=MUTED, align=PP_ALIGN.RIGHT)


def add_footer(slide, text, y=Emu(6200000)):
    card = add_shape(slide, Emu(731520), y, Emu(10728960), Emu(457200), fill=CARD_BG4)
    accent = add_shape(slide, Emu(731520), y, Emu(54864), Emu(457200), fill=ACCENT)
    tb = add_textbox(slide, Emu(914400), y + Emu(91440), Emu(10400000), Emu(365760),
                     text, font=FONT_JP, size=Emu(177800), bold=True, color=ACCENT)
    return card, accent, tb


def add_divider(slide, left, top, width):
    line = slide.shapes.add_connector(
        1, left, top, left + width, top
    )
    line.line.color.rgb = LINE_C
    line.line.width = Pt(0.75)
    return line


def add_code_block(slide, left, top, width, height, text):
    card = add_rounded_rect(slide, left, top, width, height, fill=RGBColor(0x1B, 0x19, 0x18))
    tb = add_textbox(slide, left + Emu(137160), top + Emu(91440),
                     width - Emu(274320), height - Emu(182880),
                     text, font=FONT_CODE, size=Emu(152400), color=BODY)
    return card, tb


def new_slide(prs):
    layout = prs.slide_layouts[6]  # Blank
    return prs.slides.add_slide(layout)


# ── Slide builders ─────────────────────────────────────────

def build_title_slide(prs):
    """Slide 01: Title."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    # Decorative elements
    ring = slide.shapes.add_shape(MSO_SHAPE.DONUT, Emu(8382000), Emu(-1143000),
                                   Emu(5486400), Emu(5486400))
    ring.line.fill.background()
    ring.fill.background()
    ring.line.color.rgb = RGBColor(0x3A, 0x36, 0x32)
    ring.line.width = Pt(2)

    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(9144000), Emu(2743200),
                                     Emu(2286000), Emu(2286000))
    circle.line.fill.background()
    circle.fill.solid()
    circle.fill.fore_color.rgb = ACCENT

    arc = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(7620000), Emu(1600200),
                                  Emu(3200400), Emu(3200400))
    arc.line.fill.background()
    arc.fill.solid()
    arc.fill.fore_color.rgb = ACCENT

    small = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(457200), Emu(5486400),
                                    Emu(914400), Emu(914400))
    small.line.fill.background()
    small.fill.background()
    small.line.color.rgb = RGBColor(0x3A, 0x36, 0x32)
    small.line.width = Pt(2)

    # Accent bar
    add_shape(slide, Emu(731520), Emu(1371600), Emu(54864), Emu(3200400), fill=ACCENT)

    # Dots
    for i, x in enumerate([1097280, 1371600, 1645920]):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(x), Emu(1097280),
                                      Emu(91440), Emu(91440))
        dot.line.fill.background()
        dot.fill.solid()
        dot.fill.fore_color.rgb = ACCENT

    # Stripe
    add_shape(slide, Emu(10058400), Emu(5486400), Emu(1828800), Emu(91440), fill=STRIPE_C)

    # Title
    add_textbox(slide, Emu(1097280), Emu(1371600), Emu(6400800), Emu(1554480),
                "Claude Code\n大規模開発に挑む",
                font=FONT_JP, size=Emu(660400), bold=True, color=WHITE)

    # Subtitle
    add_textbox(slide, Emu(1097280), Emu(3109920), Emu(6400800), Emu(548640),
                "〜 MCP / worktree / サブエージェント 〜",
                font=FONT_JP, size=Emu(304800), color=ACCENT)

    # Divider
    add_divider(slide, Emu(1097280), Emu(3840480), Emu(2743200))

    # Meta
    add_textbox(slide, Emu(1097280), Emu(4023360), Emu(6400800), Emu(457200),
                "社内勉強会  |  第3回 / 全3回  |  20 min",
                font=FONT_EN, size=Emu(203200), color=MUTED)


def build_roadmap_slide(prs):
    """Slide 02: Roadmap (3 cards)."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_textbox(slide, Emu(736600), Emu(457200), Emu(7620000), Emu(635000),
                "全3回のロードマップ", font=FONT_JP, size=Emu(406400), bold=True, color=WHITE)

    card_w = Emu(3429000)
    card_h = Emu(3937000)
    card_y = Emu(1270000)
    gap = Emu(228600)

    card_data = [
        {"num": "1", "label": "第1回（済）", "title": "理解する",
         "desc": "基本 / コミュニケーション / Plan Mode",
         "accent": MUTED, "card_fill": CARD_BG3, "label_color": MUTED},
        {"num": "2", "label": "第2回（済）", "title": "プロジェクトに\n定着させる",
         "desc": "コンテキスト・CLAUDE.md・\nSkills・Hooks",
         "accent": MUTED, "card_fill": CARD_BG3, "label_color": MUTED},
        {"num": "3", "label": "第3回（今日）", "title": "大規模開発に挑む",
         "desc": "MCP / worktree / サブエージェント",
         "accent": ACCENT, "card_fill": CARD_BG2, "label_color": ACCENT},
    ]

    for i, d in enumerate(card_data):
        x = Emu(736600) + i * (card_w + gap)

        add_rounded_rect(slide, x, card_y, card_w, card_h, fill=d["card_fill"])
        add_shape(slide, x, card_y, card_w, Emu(63500), fill=d["accent"])

        num_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + Emu(228600), card_y + Emu(304800),
                                            Emu(609600), Emu(609600))
        num_shape.line.fill.background()
        num_shape.fill.solid()
        num_shape.fill.fore_color.rgb = d["accent"]
        tf = num_shape.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = d["num"]
        _set_font(run, FONT_EN, Emu(254000), True, WHITE)

        add_textbox(slide, x + Emu(965200), card_y + Emu(355600), Emu(2286000), Emu(508000),
                    d["label"], font=FONT_JP, size=Emu(203200), bold=True, color=d["label_color"])

        add_textbox(slide, x + Emu(228600), card_y + Emu(1143000), Emu(2984500), Emu(1143000),
                    d["title"], font=FONT_JP, size=Emu(279400), bold=True, color=WHITE)

        add_divider(slide, x + Emu(228600), card_y + Emu(2476500), Emu(2984500))

        add_textbox(slide, x + Emu(228600), card_y + Emu(2654300), Emu(2984500), Emu(1016000),
                    d["desc"], font=FONT_JP, size=Emu(190500), color=MUTED2)

    add_textbox(slide, Emu(736600), Emu(5500000), Emu(10728960), Emu(457200),
                "今日のゴール: 複数タスクの並列処理や外部サービス連携など、大規模な開発に対応できるようになる",
                font=FONT_JP, size=Emu(203200), bold=True, color=ACCENT)

    add_page_num(slide, 2)


def build_section_slide(prs, part_num, title, subtitle, slide_num):
    """Section divider slide."""
    slide = new_slide(prs)
    set_bg(slide, BG_SECTION)

    line_y = Emu(SLIDE_H // 2)
    add_divider(slide, Emu(731520), line_y, Emu(1828800))
    add_divider(slide, Emu(SLIDE_W - 731520 - 1828800), line_y, Emu(1828800))

    add_textbox(slide, Emu(0), Emu(2000000), Emu(SLIDE_W), Emu(457200),
                f"PART {part_num}", font=FONT_EN, size=Emu(228600), bold=True,
                color=ACCENT, align=PP_ALIGN.CENTER)

    add_textbox(slide, Emu(0), Emu(2600000), Emu(SLIDE_W), Emu(762000),
                title, font=FONT_JP, size=Emu(508000), bold=True,
                color=WHITE, align=PP_ALIGN.CENTER)

    add_textbox(slide, Emu(0), Emu(3500000), Emu(SLIDE_W), Emu(457200),
                subtitle, font=FONT_JP, size=Emu(304800),
                color=MUTED2, align=PP_ALIGN.CENTER)

    add_page_num(slide, slide_num)


def build_mcp_intro_slide(prs):
    """Slide 04: What is MCP."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 1 — MCP")
    add_slide_title(slide, "MCPとは")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                "MCP = Model Context Protocol",
                font=FONT_EN, size=Emu(254000), bold=True, color=ACCENT)

    add_textbox(slide, Emu(731520), Emu(1600000), Emu(10000000), Emu(365760),
                "外部サービスとの連携プロトコル。Claude Codeの能力を外に拡張する",
                font=FONT_JP, size=Emu(203200), color=MUTED)

    add_divider(slide, Emu(731520), Emu(2050000), Emu(10728960))

    # Connection diagram
    connections = [
        ("Figma", "デザインからコンポーネント生成", ACCENT),
        ("Chrome", "ブラウザ操作・E2Eデバッグ", ACCENT2),
        ("Jira", "チケット管理の自動化", ACCENT3),
        ("Context7", "ドキュメント取得", RGBColor(0xCC, 0xAA, 0x55)),
    ]

    y = Emu(2200000)
    for service, desc, color in connections:
        # Claude Code box
        add_rounded_rect(slide, Emu(731520), y, Emu(2200000), Emu(365760), fill=CARD_BG)
        add_textbox(slide, Emu(831520), y + Emu(68580), Emu(2000000), Emu(274320),
                    "Claude Code", font=FONT_EN, size=Emu(152400), bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER)

        # Arrow
        add_textbox(slide, Emu(3000000), y + Emu(22860), Emu(1200000), Emu(320000),
                    "← MCP →", font=FONT_EN, size=Emu(139700), color=color,
                    align=PP_ALIGN.CENTER)

        # Service box
        add_rounded_rect(slide, Emu(4200000), y, Emu(1600000), Emu(365760), fill=CARD_BG)
        add_textbox(slide, Emu(4300000), y + Emu(68580), Emu(1400000), Emu(274320),
                    service, font=FONT_EN, size=Emu(152400), bold=True, color=color,
                    align=PP_ALIGN.CENTER)

        # Description
        add_textbox(slide, Emu(6100000), y + Emu(68580), Emu(5000000), Emu(274320),
                    desc, font=FONT_JP, size=Emu(177800), color=BODY)

        y += Emu(457200)

    # Points
    add_divider(slide, Emu(731520), Emu(4200000), Emu(10728960))

    points = [
        "Claude Codeはクライアントとして任意のMCPサーバーに接続",
        ".mcp.json をコミットすれば、チーム全員が同じMCPサーバーを利用可能",
        "MCPの結果もコンテキストを消費する",
    ]
    py = Emu(4400000)
    for p in points:
        add_textbox(slide, Emu(914400), py, Emu(10000000), Emu(274320),
                    f"•  {p}", font=FONT_JP, size=Emu(190500), color=BODY)
        py += Emu(365760)

    add_page_num(slide, 4)


def build_mcp_judgment_slide(prs):
    """Slide 05: When to use / not use MCP."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 1 — MCP")
    add_slide_title(slide, "MCPを使う / 使わない判断")

    half_w = Emu(5200000)

    # Left: use
    lx = Emu(731520)
    add_textbox(slide, lx, Emu(1200000), half_w, Emu(365760),
                "使うべき場面", font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT3)

    use_items = [
        ("複雑な操作の連携が必要", "Figmaデザイン → コンポーネント生成"),
        ("ブラウザ操作が必要", "Chrome DevTools MCP"),
        ("外部サービスとの深い統合", "Slack、Jira、Notionなど"),
    ]
    uy = Emu(1650000)
    for title, desc in use_items:
        add_rounded_rect(slide, lx, uy, half_w, Emu(500000), fill=CARD_BG)
        add_textbox(slide, lx + Emu(137160), uy + Emu(68580), half_w - Emu(274320), Emu(274320),
                    title, font=FONT_JP, size=Emu(190500), bold=True, color=WHITE)
        add_textbox(slide, lx + Emu(137160), uy + Emu(300000), half_w - Emu(274320), Emu(274320),
                    desc, font=FONT_JP, size=Emu(152400), color=MUTED)
        uy += Emu(548640)

    # Right: don't use
    rx = Emu(6160000)
    add_textbox(slide, rx, Emu(1200000), half_w, Emu(365760),
                "使わないほうがよい場面", font=FONT_JP, size=Emu(228600), bold=True, color=RED)

    nouse_items = [
        ("CLIで十分な場合", "gh、aws、kubectl、psqlなど"),
        ("コンテキスト圧迫が懸念", "大量データの取得は要注意"),
        ("権限管理が複雑になるとき", "過剰な権限はセキュリティリスク"),
    ]
    ny = Emu(1650000)
    for title, desc in nouse_items:
        add_rounded_rect(slide, rx, ny, half_w, Emu(500000), fill=CARD_BG)
        add_textbox(slide, rx + Emu(137160), ny + Emu(68580), half_w - Emu(274320), Emu(274320),
                    title, font=FONT_JP, size=Emu(190500), bold=True, color=WHITE)
        add_textbox(slide, rx + Emu(137160), ny + Emu(300000), half_w - Emu(274320), Emu(274320),
                    desc, font=FONT_JP, size=Emu(152400), color=MUTED)
        ny += Emu(548640)

    add_footer(slide, "→ gh（GitHub CLI）は、GitHub MCPサーバーよりも多くのケースで適している")
    add_page_num(slide, 5)


def build_mcp_config_slide(prs):
    """Slide 06: MCP configuration."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 1 — MCP")
    add_slide_title(slide, "MCPの設定方法")

    # Project level
    add_textbox(slide, Emu(731520), Emu(1200000), Emu(5000000), Emu(365760),
                "プロジェクトレベル（チーム共有）",
                font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT)

    add_code_block(slide, Emu(731520), Emu(1650000), Emu(5486400), Emu(1600000),
                   '// .mcp.json（リポジトリルートに配置）\n{\n  "mcpServers": {\n    "context7": {\n      "command": "npx",\n      "args": [\n        "-y",\n        "@anthropic/mcp-server-context7"\n      ]\n    }\n  }\n}')

    add_textbox(slide, Emu(731520), Emu(3350000), Emu(5486400), Emu(274320),
                "→ コミットすれば、チーム全員がMCPサーバーを利用可能",
                font=FONT_JP, size=Emu(177800), bold=True, color=ACCENT)

    # User level
    add_textbox(slide, Emu(6500000), Emu(1200000), Emu(5000000), Emu(365760),
                "ユーザーレベル（個人設定）",
                font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT2)

    add_textbox(slide, Emu(6500000), Emu(1650000), Emu(5000000), Emu(548640),
                "~/.claude/settings.json に設定すると\n全プロジェクトで使える",
                font=FONT_JP, size=Emu(203200), color=BODY)

    add_divider(slide, Emu(731520), Emu(3800000), Emu(10728960))

    # Comparison table
    add_textbox(slide, Emu(731520), Emu(3950000), Emu(5000000), Emu(365760),
                "設定の使い分け", font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

    col_w = [Emu(3600000), Emu(2800000), Emu(4328960)]
    col_x = [Emu(731520)]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    headers = ["場所", "共有範囲", "用途"]
    hy = Emu(4400000)
    for hdr, cx, cw in zip(headers, col_x, col_w):
        add_shape(slide, cx, hy, cw, Emu(365760), fill=CARD_BG2)
        add_textbox(slide, cx + Emu(91440), hy + Emu(68580), cw - Emu(182880), Emu(274320),
                    hdr, font=FONT_JP, size=Emu(177800), bold=True, color=ACCENT)

    rows = [
        (".mcp.json", "チーム全体", "プロジェクト固有のMCP"),
        ("~/.claude/settings.json", "自分だけ", "個人利用のMCP"),
    ]
    for i, (loc, scope, usage) in enumerate(rows):
        ry = hy + Emu(365760) + Emu(i * 370000)
        for j, (cell, cx, cw) in enumerate(zip([loc, scope, usage], col_x, col_w)):
            add_shape(slide, cx, ry, cw, Emu(365760), fill=CARD_BG if i % 2 == 0 else CARD_BG3)
            fn = FONT_CODE if j == 0 else FONT_JP
            fc = WHITE if j == 0 else BODY
            add_textbox(slide, cx + Emu(91440), ry + Emu(68580), cw - Emu(182880), Emu(274320),
                        cell, font=fn, size=Emu(177800), color=fc)

    add_page_num(slide, 6)


def build_mcp_criteria_slide(prs):
    """Slide 07: MCP adoption criteria."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 1 — MCP")
    add_slide_title(slide, "MCP導入の判断基準")

    # Decision table
    add_textbox(slide, Emu(731520), Emu(1200000), Emu(5000000), Emu(365760),
                "判断フロー", font=FONT_JP, size=Emu(228600), bold=True, color=MUTED)

    col_w = [Emu(5000000), Emu(5728960)]
    col_x = [Emu(731520), Emu(731520 + 5000000)]

    headers = ["状況", "推奨"]
    hy = Emu(1650000)
    for hdr, cx, cw in zip(headers, col_x, col_w):
        add_shape(slide, cx, hy, cw, Emu(400000), fill=CARD_BG2)
        add_textbox(slide, cx + Emu(137160), hy + Emu(91440), cw - Emu(274320), Emu(274320),
                    hdr, font=FONT_JP, size=Emu(190500), bold=True, color=ACCENT)

    criteria = [
        ("CLIで十分", "CLI使用（gh、aws、kubectlなど）"),
        ("複雑な操作の連携が必要", "MCP検討"),
        ("ブラウザ操作が必要", "MCP使用（Chrome DevTools）"),
        ("大量データの取得", "CLIまたはサブエージェントで分離"),
        ("権限管理が複雑", "慎重に検討、または使用しない"),
    ]
    for i, (situation, recommendation) in enumerate(criteria):
        ry = hy + Emu(400000) + Emu(i * 380000)
        for j, (cell, cx, cw) in enumerate(zip([situation, recommendation], col_x, col_w)):
            add_shape(slide, cx, ry, cw, Emu(365760), fill=CARD_BG if i % 2 == 0 else CARD_BG3)
            fc = WHITE if j == 0 else BODY
            add_textbox(slide, cx + Emu(137160), ry + Emu(68580), cw - Emu(274320), Emu(274320),
                        cell, font=FONT_JP, size=Emu(177800), color=fc)

    add_divider(slide, Emu(731520), Emu(3800000), Emu(10728960))

    # 3 principles
    add_textbox(slide, Emu(731520), Emu(3950000), Emu(5000000), Emu(365760),
                "導入時の3原則", font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

    principles = [
        ("1", "最小権限", "必要最小限の権限だけを与える", ACCENT),
        ("2", "操作ログ", "実行内容を確認できるようにしておく", ACCENT2),
        ("3", "承認フロー", "重要な操作は自動実行せず承認を挟む", ACCENT3),
    ]

    px = Emu(731520)
    card_w = Emu(3429000)
    for i, (num, title, desc, color) in enumerate(principles):
        cx = px + i * (card_w + Emu(228600))
        add_rounded_rect(slide, cx, Emu(4400000), card_w, Emu(1200000), fill=CARD_BG)
        add_shape(slide, cx, Emu(4400000), card_w, Emu(54864), fill=color)

        num_s = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx + Emu(137160), Emu(4550000),
                                        Emu(365760), Emu(365760))
        num_s.line.fill.background()
        num_s.fill.solid()
        num_s.fill.fore_color.rgb = color
        tf = num_s.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = num
        _set_font(run, FONT_EN, Emu(203200), True, WHITE)

        add_textbox(slide, cx + Emu(594360), Emu(4550000), Emu(2700000), Emu(365760),
                    title, font=FONT_JP, size=Emu(203200), bold=True, color=WHITE)

        add_textbox(slide, cx + Emu(137160), Emu(5000000), card_w - Emu(274320), Emu(457200),
                    desc, font=FONT_JP, size=Emu(177800), color=BODY)

    add_page_num(slide, 7)


def build_worktree_intro_slide(prs):
    """Slide 09: What is Git worktree."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 2 — worktree")
    add_slide_title(slide, "Git worktreeとは")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                "同じリポジトリから複数の作業ディレクトリを作成する機能",
                font=FONT_JP, size=Emu(228600), bold=True, color=MUTED)

    # Directory structure visualization
    add_code_block(slide, Emu(731520), Emu(1700000), Emu(5200000), Emu(1800000),
                   "my-project/（メイン）\n├── .git/\n└── src/\n\nmy-project-feature-a/（worktree A）\n└── src/  ← Issue #123 の作業\n\nmy-project-bugfix/（worktree B）\n└── src/  ← Issue #456 の作業")

    # Features
    add_textbox(slide, Emu(6200000), Emu(1700000), Emu(5000000), Emu(365760),
                "特徴", font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

    features = [
        "各worktreeは独立したファイル状態を持つ",
        "同じGit履歴を共有する",
        "ブランチ切り替え不要（stash も不要）",
    ]
    fy = Emu(2150000)
    for f in features:
        add_textbox(slide, Emu(6400000), fy, Emu(5000000), Emu(274320),
                    f"•  {f}", font=FONT_JP, size=Emu(190500), color=BODY)
        fy += Emu(365760)

    add_divider(slide, Emu(731520), Emu(3800000), Emu(10728960))

    # Claude Code compatibility
    add_textbox(slide, Emu(731520), Emu(3950000), Emu(10000000), Emu(365760),
                "Claude Codeとの相性", font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT)

    compat = [
        "各worktreeで独立したClaude Codeセッションを起動できる",
        "あるworktreeでの変更が別のworktreeに影響しない",
    ]
    cy = Emu(4400000)
    for c in compat:
        add_textbox(slide, Emu(914400), cy, Emu(10000000), Emu(274320),
                    f"•  {c}", font=FONT_JP, size=Emu(190500), color=BODY)
        cy += Emu(365760)

    add_footer(slide, "→ 各worktreeで独立したClaude Codeセッションを起動し、並列で作業を進める")
    add_page_num(slide, 9)


def build_issuemd_slide(prs):
    """Slide 10: worktree + ISSUE.md."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 2 — worktree")
    add_slide_title(slide, "worktree + ISSUE.md")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                'ISSUE.md = worktreeの「地図」',
                font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT)

    # ISSUE.md example
    add_code_block(slide, Emu(731520), Emu(1650000), Emu(5200000), Emu(2000000),
                   "# Issue #123\n\n## タイトル\nAPIのタイムアウトエラーを修正\n\n## 本文\n直近のデプロイ以降、一部のAPIで\nタイムアウトが発生している。\n接続先の設定変更が原因の可能性。\n\n## Comments\n...（ghコマンドで取得）")

    # Benefits table
    add_textbox(slide, Emu(6200000), Emu(1200000), Emu(5000000), Emu(365760),
                "なぜ有効か", font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

    benefits = [
        ("方向性が明確", "「何をすべきか」がISSUE.mdに\n書いてある", ACCENT),
        ("自動化しやすい", "worktree作成 + ISSUE.md生成を\nスクリプト化", ACCENT2),
        ("干渉がない", "各worktreeは独立したファイル状態", ACCENT3),
        ("すぐ始められる", "「ISSUE.mdを読んで計画を立てて」\nの一言で開始", RGBColor(0xCC, 0xAA, 0x55)),
    ]

    by = Emu(1650000)
    for title, desc, color in benefits:
        add_rounded_rect(slide, Emu(6200000), by, Emu(5260960), Emu(500000), fill=CARD_BG)
        add_shape(slide, Emu(6200000), by, Emu(54864), Emu(500000), fill=color)
        add_textbox(slide, Emu(6400000), by + Emu(45720), Emu(2000000), Emu(274320),
                    title, font=FONT_JP, size=Emu(177800), bold=True, color=color)
        add_textbox(slide, Emu(8200000), by + Emu(45720), Emu(3000000), Emu(457200),
                    desc, font=FONT_JP, size=Emu(152400), color=BODY)
        by += Emu(548640)

    add_footer(slide, '→ 「ISSUE.mdを読んで計画を立てて」の一言で作業を開始')
    add_page_num(slide, 10)


def build_workflow_slide(prs):
    """Slide 11: Practical workflow."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 2 — worktree")
    add_slide_title(slide, "実践ワークフロー")

    # Script
    add_textbox(slide, Emu(731520), Emu(1100000), Emu(5000000), Emu(365760),
                "セットアップスクリプト", font=FONT_JP, size=Emu(203200), bold=True, color=ACCENT)

    add_code_block(slide, Emu(731520), Emu(1500000), Emu(5486400), Emu(2800000),
                   '#!/bin/bash\n# start-issue.sh\nISSUE_NUMBER=$1\nWORKTREE_DIR="../issue-${ISSUE_NUMBER}"\n\n# worktree作成\ngit worktree add "$WORKTREE_DIR" \\\n  -b "issue-${ISSUE_NUMBER}"\n\n# ISSUE.md生成\ncd "$WORKTREE_DIR"\n{\n  echo "# Issue #${ISSUE_NUMBER}"\n  gh issue view "$ISSUE_NUMBER"\n  echo "## Comments"\n  gh issue view "$ISSUE_NUMBER" --comments\n} > ISSUE.md')

    add_textbox(slide, Emu(731520), Emu(4400000), Emu(5486400), Emu(365760),
                "使い方: ./start-issue.sh 123",
                font=FONT_CODE, size=Emu(177800), color=ACCENT)

    # Workflow steps
    add_textbox(slide, Emu(6500000), Emu(1100000), Emu(5000000), Emu(365760),
                "ワークフロー", font=FONT_JP, size=Emu(203200), bold=True, color=WHITE)

    steps = [
        ("1", "Issue選択", MUTED),
        ("2", "スクリプトで\nworktree + ISSUE.md作成", ACCENT),
        ("3", "Claude Code起動", MUTED),
        ("4", "「ISSUE.mdを読んで\n計画を立てて」", ACCENT),
        ("5", "計画レビュー", MUTED),
        ("6", "実装", MUTED),
        ("7", "PR作成", MUTED),
        ("8", "worktree削除", MUTED),
    ]

    sy = Emu(1500000)
    for num, label, color in steps:
        num_s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(6500000), sy,
                                        Emu(320000), Emu(320000))
        num_s.line.fill.background()
        num_s.fill.solid()
        num_s.fill.fore_color.rgb = color
        tf = num_s.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = num
        _set_font(run, FONT_EN, Emu(152400), True, WHITE)

        add_textbox(slide, Emu(6900000), sy + Emu(22860), Emu(4500000), Emu(320000),
                    label, font=FONT_JP, size=Emu(165100), color=BODY)

        sy += Emu(400000)

    add_page_num(slide, 11)


def build_demo_slide(prs, title, slide_num):
    """Demo slide (minimal text)."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_textbox(slide, Emu(0), Emu(2200000), Emu(SLIDE_W), Emu(762000),
                "DEMO", font=FONT_EN, size=Emu(762000), bold=True,
                color=ACCENT, align=PP_ALIGN.CENTER)

    add_textbox(slide, Emu(0), Emu(3200000), Emu(SLIDE_W), Emu(457200),
                title, font=FONT_JP, size=Emu(254000),
                color=MUTED, align=PP_ALIGN.CENTER)

    add_page_num(slide, slide_num)


def build_subagent_intro_slide(prs):
    """Slide 14: What are sub-agents."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 3 — サブエージェント")
    add_slide_title(slide, "サブエージェントとは")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                "独立したコンテキストで動く専門エージェント",
                font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT)

    # Flow diagram
    # Main agent box
    main_y = Emu(1800000)
    add_rounded_rect(slide, Emu(731520), main_y, Emu(4400000), Emu(457200), fill=CARD_BG2)
    add_textbox(slide, Emu(831520), main_y + Emu(91440), Emu(4200000), Emu(274320),
                "メインエージェント", font=FONT_JP, size=Emu(203200), bold=True, color=WHITE,
                align=PP_ALIGN.CENTER)

    # Arrow down
    add_textbox(slide, Emu(2500000), main_y + Emu(457200), Emu(800000), Emu(365760),
                "指示 ▼", font=FONT_JP, size=Emu(152400), color=ACCENT, align=PP_ALIGN.CENTER)

    # Sub-agent box
    sub_y = main_y + Emu(914400)
    add_rounded_rect(slide, Emu(731520), sub_y, Emu(4400000), Emu(800000), fill=CARD_BG)
    add_shape(slide, Emu(731520), sub_y, Emu(54864), Emu(800000), fill=ACCENT2)
    add_textbox(slide, Emu(914400), sub_y + Emu(68580), Emu(4000000), Emu(274320),
                "サブエージェント（独立コンテキスト）",
                font=FONT_JP, size=Emu(190500), bold=True, color=ACCENT2)
    add_textbox(slide, Emu(914400), sub_y + Emu(365760), Emu(4000000), Emu(365760),
                "数十ファイルを検索・分析...",
                font=FONT_JP, size=Emu(177800), color=BODY)

    # Arrow up
    add_textbox(slide, Emu(2500000), sub_y + Emu(800000), Emu(800000), Emu(365760),
                "▲ 要約だけ返る", font=FONT_JP, size=Emu(152400), color=ACCENT3, align=PP_ALIGN.CENTER)

    # Result box
    result_y = sub_y + Emu(1280000)
    add_rounded_rect(slide, Emu(731520), result_y, Emu(4400000), Emu(457200), fill=CARD_BG2)
    add_textbox(slide, Emu(831520), result_y + Emu(91440), Emu(4200000), Emu(274320),
                "メインのコンテキストを圧迫しない",
                font=FONT_JP, size=Emu(190500), bold=True, color=ACCENT3,
                align=PP_ALIGN.CENTER)

    # Right side: key points
    add_textbox(slide, Emu(5600000), Emu(1800000), Emu(6000000), Emu(365760),
                '本質: コンテキストの分離', font=FONT_JP,
                size=Emu(254000), bold=True, color=WHITE)

    key_points = [
        "サブエージェントに委譲したタスクは\n独立して処理される",
        "作業結果の要約だけが\nメイン会話に返される",
        "メイン会話のコンテキストを消費しない",
    ]
    ky = Emu(2300000)
    for kp in key_points:
        add_rounded_rect(slide, Emu(5600000), ky, Emu(5860960), Emu(548640), fill=CARD_BG)
        add_textbox(slide, Emu(5800000), ky + Emu(68580), Emu(5460960), Emu(457200),
                    kp, font=FONT_JP, size=Emu(177800), color=BODY)
        ky += Emu(640000)

    add_footer(slide, "→ 大量のファイル検索や広範な調査をしてもメインの作業に影響しない")
    add_page_num(slide, 14)


def build_builtin_subagents_slide(prs):
    """Slide 15: Built-in sub-agents."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 3 — サブエージェント")
    add_slide_title(slide, "組み込みサブエージェント")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                "3つの組み込みサブエージェント",
                font=FONT_JP, size=Emu(228600), bold=True, color=MUTED)

    # 3 cards for each sub-agent
    agents = [
        ("Explore", "Haiku（高速）", "読み取り専用",
         "コードベースの検索・分析に特化。\n高速・軽量で、ファイルの\n読み取りと検索のみ。", ACCENT),
        ("Plan", "—", "読み取り専用",
         "Planモード中の調査に使われる。\n第1回で紹介したPlanモードの\n裏で動いている。", ACCENT2),
        ("general-purpose", "Sonnet", "全ツール利用可",
         "複雑なマルチステップタスク向け。\nファイルの読み書き、\nコマンド実行が可能。", ACCENT3),
    ]

    card_w = Emu(3429000)
    card_h = Emu(3200000)
    start_x = Emu(731520)
    start_y = Emu(1700000)
    gap = Emu(228600)

    for i, (name, model, mode, desc, color) in enumerate(agents):
        cx = start_x + i * (card_w + gap)

        add_rounded_rect(slide, cx, start_y, card_w, card_h, fill=CARD_BG)
        add_shape(slide, cx, start_y, card_w, Emu(54864), fill=color)

        # Name
        add_textbox(slide, cx + Emu(182880), start_y + Emu(182880), card_w - Emu(365760), Emu(457200),
                    name, font=FONT_EN, size=Emu(279400), bold=True, color=color)

        # Model & Mode
        add_textbox(slide, cx + Emu(182880), start_y + Emu(700000), card_w - Emu(365760), Emu(274320),
                    f"モデル: {model}", font=FONT_JP, size=Emu(165100), color=MUTED)
        add_textbox(slide, cx + Emu(182880), start_y + Emu(980000), card_w - Emu(365760), Emu(274320),
                    f"モード: {mode}", font=FONT_JP, size=Emu(165100), color=MUTED)

        add_divider(slide, cx + Emu(182880), start_y + Emu(1350000), card_w - Emu(365760))

        # Description
        add_textbox(slide, cx + Emu(182880), start_y + Emu(1500000), card_w - Emu(365760), Emu(1500000),
                    desc, font=FONT_JP, size=Emu(177800), color=BODY, line_spacing=4)

    add_footer(slide, "→ Claudeが状況に応じて自動的に使い分ける", y=Emu(5200000))
    add_page_num(slide, 15)


def build_custom_subagent_slide(prs):
    """Slide 16: Creating custom sub-agents."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 3 — サブエージェント")
    add_slide_title(slide, "カスタムサブエージェントの作り方")

    # Directory structure
    add_textbox(slide, Emu(731520), Emu(1100000), Emu(5000000), Emu(365760),
                ".claude/agents/ にMarkdownファイルを配置",
                font=FONT_JP, size=Emu(203200), bold=True, color=ACCENT)

    add_code_block(slide, Emu(731520), Emu(1500000), Emu(3800000), Emu(640080),
                   ".claude/agents/\n├── code-reviewer.md\n├── debugger.md\n└── test-runner.md")

    # Config example
    add_textbox(slide, Emu(731520), Emu(2300000), Emu(5000000), Emu(365760),
                "設定ファイルの構造", font=FONT_JP, size=Emu(203200), bold=True, color=WHITE)

    add_code_block(slide, Emu(731520), Emu(2700000), Emu(5486400), Emu(2743200),
                   "---\nname: code-reviewer\ndescription: コードレビューの専門家。\n             コード変更後に積極的にレビュー。\ntools: Read, Grep, Glob, Bash\nmodel: sonnet\n---\n\nあなたはシニアコードレビューアーです。\n\n呼び出されたときは以下を実行する。\n1. git diffで最近の変更を確認\n2. 変更されたファイルに焦点を当てる\n3. 即座にレビューを開始")

    # Fields table (right side)
    add_textbox(slide, Emu(6500000), Emu(1100000), Emu(5000000), Emu(365760),
                "主なフィールド", font=FONT_JP, size=Emu(203200), bold=True, color=WHITE)

    col_w = [Emu(1600000), Emu(800000), Emu(3060960)]
    col_x = [Emu(6500000)]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    headers = ["フィールド", "必須", "説明"]
    hy = Emu(1500000)
    for hdr, cx, cw in zip(headers, col_x, col_w):
        add_shape(slide, cx, hy, cw, Emu(365760), fill=CARD_BG2)
        add_textbox(slide, cx + Emu(91440), hy + Emu(68580), cw - Emu(182880), Emu(274320),
                    hdr, font=FONT_JP, size=Emu(165100), bold=True, color=ACCENT)

    fields = [
        ("name", "Yes", "一意の識別子"),
        ("description", "Yes", "Claudeが委譲判断に使う"),
        ("tools", "No", "利用可能なツール"),
        ("model", "No", "sonnet / opus / haiku"),
    ]
    for i, (field, req, desc) in enumerate(fields):
        ry = hy + Emu(365760) + Emu(i * 340000)
        for j, (cell, cx, cw) in enumerate(zip([field, req, desc], col_x, col_w)):
            add_shape(slide, cx, ry, cw, Emu(320000), fill=CARD_BG if i % 2 == 0 else CARD_BG3)
            fn = FONT_CODE if j == 0 else FONT_JP
            fc = ACCENT if j == 0 else BODY
            add_textbox(slide, cx + Emu(91440), ry + Emu(45720), cw - Emu(182880), Emu(274320),
                        cell, font=fn, size=Emu(165100), color=fc)

    add_footer(slide, "→ descriptionが重要。Claudeはこの説明を見て委譲先を判断する",
               y=Emu(5700000))
    add_page_num(slide, 16)


def build_skill_vs_subagent_slide(prs):
    """Slide 17: Skill vs Sub-agent."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_part_label(slide, "PART 3 — サブエージェント")
    add_slide_title(slide, "スキル vs サブエージェント")

    add_textbox(slide, Emu(731520), Emu(1200000), Emu(10000000), Emu(365760),
                "どちらもClaudeの能力を拡張するが、動作が異なる",
                font=FONT_JP, size=Emu(203200), color=MUTED)

    # Comparison table
    col_w = [Emu(2600000), Emu(4064480), Emu(4064480)]
    col_x = [Emu(731520)]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    headers = ["", "スキル", "サブエージェント"]
    hy = Emu(1700000)
    for hdr, cx, cw in zip(headers, col_x, col_w):
        add_shape(slide, cx, hy, cw, Emu(365760), fill=CARD_BG2)
        add_textbox(slide, cx + Emu(91440), hy + Emu(68580), cw - Emu(182880), Emu(274320),
                    hdr, font=FONT_JP, size=Emu(190500), bold=True, color=ACCENT)

    rows = [
        ("コンテキスト", "メイン会話内", "独立したコンテキスト"),
        ("結果の扱い", "そのまま会話に残る", "要約だけが返る"),
        ("向いている作業", "知識参照、軽量なワークフロー", "大量の探索、並列実行"),
        ("配置場所", ".claude/skills/", ".claude/agents/"),
    ]
    for i, (label, skill, agent) in enumerate(rows):
        ry = hy + Emu(365760) + Emu(i * 370000)
        for j, (cell, cx, cw) in enumerate(zip([label, skill, agent], col_x, col_w)):
            add_shape(slide, cx, ry, cw, Emu(365760), fill=CARD_BG if i % 2 == 0 else CARD_BG3)
            fn = FONT_CODE if j > 0 and i == 3 else FONT_JP
            fc = WHITE if j == 0 else BODY
            fb = j == 0
            add_textbox(slide, cx + Emu(91440), ry + Emu(68580), cw - Emu(182880), Emu(274320),
                        cell, font=fn, size=Emu(177800), bold=fb, color=fc)

    add_divider(slide, Emu(731520), Emu(3600000), Emu(10728960))

    # Usage criteria
    add_textbox(slide, Emu(731520), Emu(3750000), Emu(5000000), Emu(365760),
                "使い分けの基準", font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

    criteria = [
        ("1〜3ファイルの作業", "→ スキル", ACCENT),
        ("数十ファイルの探索", "→ サブエージェント", ACCENT2),
        ("結果を会話で直接使いたい", "→ スキル", ACCENT),
        ("メインのコンテキストを守りたい", "→ サブエージェント", ACCENT2),
    ]
    cy = Emu(4200000)
    for task, result, color in criteria:
        add_textbox(slide, Emu(914400), cy, Emu(5000000), Emu(274320),
                    f"•  {task}", font=FONT_JP, size=Emu(177800), color=BODY)
        add_textbox(slide, Emu(5800000), cy, Emu(5000000), Emu(274320),
                    result, font=FONT_JP, size=Emu(177800), bold=True, color=color)
        cy += Emu(340000)

    add_footer(slide, "→ スキル = 手順書、サブエージェント = 専門チームメンバー",
               y=Emu(5800000))
    add_page_num(slide, 17)


def build_review_slide(prs):
    """Slide 18: Series review."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_slide_title(slide, "全3回の振り返り", y=Emu(365760))

    add_textbox(slide, Emu(731520), Emu(914400), Emu(10000000), Emu(365760),
                "3回で学んだClaude Codeの全体像",
                font=FONT_JP, size=Emu(228600), bold=True, color=MUTED)

    # 3 session cards
    sessions = [
        ("1", "理解する",
         "基本操作とコミュニケーション\nPlan Modeで計画から始める\n「指示」「判断」「確認」が\n人間の出番", ACCENT),
        ("2", "定着させる",
         "CLAUDE.mdで「常識」を教える\nSkillsで繰り返しの指示を\nテンプレート化\nHooksで品質チェックを自動化", ACCENT2),
        ("3", "大規模開発に挑む",
         "MCPで外部サービスとつなぐ\nworktreeで並列作業を実現\nサブエージェントで\nコンテキストを守る", ACCENT3),
    ]

    card_w = Emu(3429000)
    card_h = Emu(3200000)
    start_x = Emu(731520)
    start_y = Emu(1371600)
    gap = Emu(228600)

    for i, (num, title, desc, color) in enumerate(sessions):
        cx = start_x + i * (card_w + gap)

        add_rounded_rect(slide, cx, start_y, card_w, card_h, fill=CARD_BG)
        add_shape(slide, cx, start_y, card_w, Emu(54864), fill=color)

        # Number
        num_s = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx + Emu(182880), start_y + Emu(182880),
                                        Emu(548640), Emu(548640))
        num_s.line.fill.background()
        num_s.fill.solid()
        num_s.fill.fore_color.rgb = color
        tf = num_s.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = num
        _set_font(run, FONT_EN, Emu(254000), True, WHITE)

        # Title
        add_textbox(slide, cx + Emu(182880), start_y + Emu(822960), card_w - Emu(365760), Emu(457200),
                    title, font=FONT_JP, size=Emu(228600), bold=True, color=WHITE)

        # Description
        add_textbox(slide, cx + Emu(182880), start_y + Emu(1371600), card_w - Emu(365760), Emu(1600000),
                    desc, font=FONT_JP, size=Emu(177800), color=BODY, line_spacing=4)

    # Summary line
    add_textbox(slide, Emu(731520), Emu(4800000), Emu(10728960), Emu(457200),
                "理解する → 定着させる → スケールさせる",
                font=FONT_JP, size=Emu(279400), bold=True, color=ACCENT,
                align=PP_ALIGN.CENTER)

    add_page_num(slide, 18)


def build_summary_slide(prs):
    """Slide 19: Summary."""
    slide = new_slide(prs)
    set_bg(slide, BG_MAIN)

    add_slide_title(slide, "まとめ / シリーズ総括", y=Emu(365760))

    add_textbox(slide, Emu(731520), Emu(914400), Emu(10000000), Emu(365760),
                "3つの持ち帰り", font=FONT_JP, size=Emu(254000), bold=True, color=MUTED)

    takeaways = [
        ("1", 'MCPは「CLIで足りないとき」の選択肢',
         "CLIで十分ならCLI。\n複雑な連携やブラウザ操作が\n必要なときにMCPを検討", ACCENT),
        ("2", "worktree + ISSUE.mdで\n並列作業を仕組み化する",
         "Issue番号を渡すだけで\n作業環境が整う。\nClaude Codeとの相性が非常にいい", ACCENT2),
        ("3", "サブエージェントで\nコンテキストを守る",
         "大量の探索はサブエージェントに\n委譲し、メインのコンテキストを\n保全する", ACCENT3),
    ]

    card_w = Emu(3429000)
    card_h = Emu(2743200)
    start_x = Emu(731520)
    start_y = Emu(1371600)
    gap = Emu(228600)

    for i, (num, title, desc, color) in enumerate(takeaways):
        cx = start_x + i * (card_w + gap)

        add_rounded_rect(slide, cx, start_y, card_w, card_h, fill=CARD_BG)
        add_shape(slide, cx, start_y, card_w, Emu(54864), fill=color)

        num_s = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx + Emu(182880), start_y + Emu(182880),
                                        Emu(548640), Emu(548640))
        num_s.line.fill.background()
        num_s.fill.solid()
        num_s.fill.fore_color.rgb = color
        tf = num_s.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = num
        _set_font(run, FONT_EN, Emu(254000), True, WHITE)

        add_textbox(slide, cx + Emu(182880), start_y + Emu(822960), card_w - Emu(365760), Emu(640080),
                    title, font=FONT_JP, size=Emu(190500), bold=True, color=WHITE)

        add_textbox(slide, cx + Emu(182880), start_y + Emu(1554480), card_w - Emu(365760), Emu(1097280),
                    desc, font=FONT_JP, size=Emu(177800), color=BODY)

    # Series summary
    add_textbox(slide, Emu(731520), Emu(4400000), Emu(10728960), Emu(457200),
                "シリーズ全体の覚え方:  理解する → 定着させる → スケールさせる",
                font=FONT_JP, size=Emu(228600), bold=True, color=ACCENT)

    add_divider(slide, Emu(731520), Emu(4900000), Emu(10728960))

    add_textbox(slide, Emu(731520), Emu(5050000), Emu(10728960), Emu(457200),
                "まず使ってみて、プロジェクトに合わせて育てていってください",
                font=FONT_JP, size=Emu(203200), color=MUTED)

    add_page_num(slide, 19)


# ── Main ───────────────────────────────────────────────────

def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # Slide 01: Title
    build_title_slide(prs)

    # Slide 02: Roadmap
    build_roadmap_slide(prs)

    # Slide 03: Section — PART 1
    build_section_slide(prs, 1, "MCP", "CLIで足りないとき、つなぐ", 3)

    # Slide 04: MCP intro
    build_mcp_intro_slide(prs)

    # Slide 05: MCP judgment
    build_mcp_judgment_slide(prs)

    # Slide 06: MCP config
    build_mcp_config_slide(prs)

    # Slide 07: MCP criteria
    build_mcp_criteria_slide(prs)

    # Slide 08: Section — PART 2
    build_section_slide(prs, 2, "worktree", "並列で、ブレずに進める", 8)

    # Slide 09: worktree intro
    build_worktree_intro_slide(prs)

    # Slide 10: ISSUE.md
    build_issuemd_slide(prs)

    # Slide 11: Workflow
    build_workflow_slide(prs)

    # Slide 12: Demo — worktree + ISSUE.md
    build_demo_slide(prs, "worktree + ISSUE.md", 12)

    # Slide 13: Section — PART 3
    build_section_slide(prs, 3, "サブエージェント", "分業で、コンテキストを守る", 13)

    # Slide 14: Sub-agent intro
    build_subagent_intro_slide(prs)

    # Slide 15: Built-in sub-agents
    build_builtin_subagents_slide(prs)

    # Slide 16: Custom sub-agents
    build_custom_subagent_slide(prs)

    # Slide 17: Skill vs Sub-agent
    build_skill_vs_subagent_slide(prs)

    # Slide 18: Series review
    build_review_slide(prs)

    # Slide 19: Summary
    build_summary_slide(prs)

    prs.save("slides/Claude_session3.pptx")
    print(f"✓ slides/Claude_session3.pptx を生成しました（全{TOTAL_SLIDES}スライド）")


if __name__ == "__main__":
    main()
