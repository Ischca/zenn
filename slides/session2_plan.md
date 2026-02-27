# 第2回スライド作成: プロジェクトに定着させる

## Context

第1回「Claude Code ことはじめ」（19枚/20分）のスライドが完成済み。
第2回のテーマは「プロジェクトに定着させる」で、コンテキスト / CLAUDE.md / スラッシュコマンド / Skills / Hooks を扱う。
パワポが正。python-pptx で `.pptx` を生成し、同時に `session2_content.md` も作成する。

## 成果物

1. `slides/Claude_session2.pptx` — python-pptx で生成（第1回と同じデザインシステム）
2. `slides/session2_content.md` — スライド内容 + 台本

## 全体構成（19枚 / 20分）

**ナラティブ**: 教える → 呼び出す → 自動化する

### PART タグライン
- PART 1: 「毎回の説明、もう要らない」
- PART 2: 「同じ指示、何度も書かない」
- PART 3: 「人間が忘れても、Hooksが動く」

## スライド一覧

| # | タイトル | タイプ | 時間 |
|---|---------|--------|------|
| 01 | Claude Code プロジェクトに定着させる | タイトル | 0:30 |
| 02 | 全3回のロードマップ | コンテンツ | 0:30 |
| 03 | PART 1 — コンテキストとCLAUDE.md | セクション区切り | 0:15 |
| 04 | Claude Codeは何を見ているか | コンテンツ | 1:15 |
| 05 | なぜ「忘れる」のか | コンテンツ | 1:15 |
| 06 | CLAUDE.mdとは | コンテンツ | 1:00 |
| 07 | CLAUDE.mdに書くべき内容 | コンテンツ（コード例） | 1:15 |
| 08 | CLAUDE.mdの始め方と育て方 | コンテンツ | 1:00 |
| 09 | デモ — CLAUDE.md & /init | デモ | 1:30 |
| 10 | コンテキスト管理チェックリスト | コンテンツ（まとめ表） | 0:45 |
| 11 | PART 2 — スラッシュコマンド & Skills | セクション区切り | 0:15 |
| 12 | 組み込みスラッシュコマンド | コンテンツ（表） | 1:00 |
| 13 | カスタムスラッシュコマンド & Skills | コンテンツ（比較表） | 1:15 |
| 14 | スキルの2タイプと実例 | コンテンツ（コード例） | 1:15 |
| 15 | デモ — Skills | デモ | 1:00 |
| 16 | PART 3 — Hooks | セクション区切り | 0:15 |
| 17 | Hooksとは | コンテンツ（図+コード） | 1:30 |
| 18 | Hooksの実践例 | コンテンツ（コード例×3） | 1:30 |
| 19 | まとめ / 次回予告 | まとめ | 1:00 |

合計: 約18:15（バッファ1:45）

## 実装手順

### Step 1: session2_content.md を作成
- 各スライドの内容（ビジュアル要素の説明）と台本を記載
- 第1回のフォーマットに合わせる
- ソース記事の内容を反映（下記参照）

### Step 2: python-pptx で pptx を生成
- 第1回（`Claude_session1.pptx`）からデザイントークン（色・フォント・レイアウト）を踏襲
- inline script metadata で `uv run` 実行可能にする
- 生成スクリプトは一時利用（生成後はpptxが正）

### Step 3: 生成スクリプトを削除
- pptx 生成後、スクリプトは不要なので削除

## ソース記事（内容の参照元）

| PART | 記事 |
|------|------|
| PART 1 | `articles/cc-guide-context-management.md` |
| PART 2 | `articles/cc-guide-skill-design.md` |
| PART 3 | `articles/cc-guide-quality-gate.md` |
| 補助 | `articles/cc-guide-insights.md` |

## デザインシステム（第1回から踏襲）

- BG_DARK: `#1B1918`
- BG_SECTION: `#231F1D`
- ACCENT (Claude Orange): `#D97757`
- TEXT_WHITE: `#FAF9F5`
- TEXT_LIGHT: `#C5C3BB`
- HIGHLIGHT (Blue): `#6A9BCC`
- GREEN: `#7BC9A0`
- フォント: Hiragino Sans / Helvetica Neue / SF Mono
- スライドサイズ: 13.333 x 7.5 inches

## 検証

- `uv run slides/generate_session2.py` でエラーなく19枚生成
- 生成された pptx を開いてレイアウト崩れがないか確認
- 台本の内容がソース記事と矛盾しないか確認
