# 第3回スライド作成: 大規模開発に挑む

## Context

第1回「Claude Code ことはじめ」（19枚/20分）、第2回「プロジェクトに定着させる」（19枚/20分）が完成済み。
第3回のテーマは「大規模開発に挑む」で、MCP / worktree / サブエージェントを扱う。シリーズ最終回。
パワポが正。python-pptx で `.pptx` を生成し、同時に `session3_content.md` も作成する。

## 成果物

1. `slides/Claude_session3.pptx` — python-pptx で生成（第1回・第2回と同じデザインシステム）
2. `slides/session3_content.md` — スライド内容 + 台本

## 全体構成（19枚 / 20分）

**ナラティブ**: つなぐ → 並列化する → 分業する

### PART タグライン
- PART 1: 「CLIで足りないとき、つなぐ」
- PART 2: 「並列で、ブレずに進める」
- PART 3: 「分業で、コンテキストを守る」

## スライド一覧

| # | タイトル | タイプ | 時間 |
|---|---------|--------|------|
| 01 | Claude Code 大規模開発に挑む | タイトル | 0:30 |
| 02 | 全3回のロードマップ | コンテンツ | 0:30 |
| 03 | PART 1 — MCP | セクション区切り | 0:15 |
| 04 | MCPとは | コンテンツ | 1:15 |
| 05 | MCPを使う / 使わない判断 | コンテンツ（比較表） | 1:15 |
| 06 | MCPの設定方法 | コンテンツ（コード例） | 1:00 |
| 07 | MCP導入の判断基準 | コンテンツ（まとめ表） | 0:45 |
| 08 | PART 2 — worktree | セクション区切り | 0:15 |
| 09 | Git worktreeとは | コンテンツ | 1:15 |
| 10 | worktree + ISSUE.md | コンテンツ | 1:15 |
| 11 | 実践ワークフロー | コンテンツ（コード例） | 1:15 |
| 12 | デモ — worktree + ISSUE.md | デモ | 1:00 |
| 13 | PART 3 — サブエージェント | セクション区切り | 0:15 |
| 14 | サブエージェントとは | コンテンツ | 1:15 |
| 15 | 組み込みサブエージェント | コンテンツ（表） | 1:15 |
| 16 | カスタムサブエージェントの作り方 | コンテンツ（コード例） | 1:15 |
| 17 | スキル vs サブエージェント | コンテンツ（比較表） | 1:00 |
| 18 | 全3回の振り返り | コンテンツ | 1:00 |
| 19 | まとめ / シリーズ総括 | まとめ | 1:00 |

合計: 約18:00（バッファ2:00）

## 実装手順

### Step 1: session3_content.md を作成
- 各スライドの内容（ビジュアル要素の説明）と台本を記載
- 第1回・第2回のフォーマットに合わせる
- ソース記事の内容を反映

### Step 2: python-pptx で pptx を生成
- 第2回（`create_session2.py`）からデザイントークン・ヘルパー関数を踏襲
- inline script metadata で `uv run` 実行可能にする

### Step 3: 生成スクリプトを削除
- pptx 生成後、スクリプトは不要なので削除

## ソース記事（内容の参照元）

| PART | 記事 |
|------|------|
| PART 1 | `articles/cc-guide-mcp-usage.md` |
| PART 2 | `articles/cc-guide-worktree-workflow.md` |
| PART 3 | `articles/cc-guide-subagent-design.md` |

## デザインシステム（第1回・第2回から踏襲）

- BG_DARK: `#1B1918`
- BG_SECTION: `#231F1D`
- ACCENT (Claude Orange): `#D97757`
- TEXT_WHITE: `#FAF9F5`
- TEXT_LIGHT: `#C5C3BB`
- HIGHLIGHT (Blue): `#6A9BCC`
- GREEN: `#7BC9A0`
- フォント: Hiragino Sans / Helvetica Neue / SF Mono
- スライドサイズ: 13.333 x 7.5 inches
