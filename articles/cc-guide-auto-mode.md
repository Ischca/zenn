---
title: "Claude Code「Auto Mode」の正しい使い方を調べたら、一次ソースが見つからなかった"
emoji: "🔍"
type: "tech"
topics: ["claudecode", "ai", "cli", "開発ツール"]
published: false
---

## はじめに

2026年3月12日前後から、Claude Codeに「Auto Mode」なるResearch Previewが追加されたという話が流れてきました。
操作ごとにClaudeがリスクを判断し、低リスクなら自動承認、高リスクなら人間に確認を求めるモードだそうです。

使おうとして調べたところ、有効化方法の情報がネット上で割れていました。

- `claude --enable-auto-mode`
- `claude --permission-mode auto`

どちらが正しいのか。公式ソースを当たってみた記録です。

## Auto Modeの背景

Claude Codeのpermission modeは、これまで4つありました。

| モード | 動作 |
|--------|------|
| `default` | ツール初回使用時に許可を求める |
| `acceptEdits` | ファイル編集を自動承認 |
| `plan` | 読み取り専用、変更不可 |
| `bypassPermissions` | 全許可をスキップ |

`default`だと、20ステップを超えるあたりから承認ボタンを押す作業が本体になってきます。
`bypassPermissions`（`--dangerously-skip-permissions`）は全チェックが外れるので、事故が怖い。

Auto Modeはこの間を埋めるモードとして登場した、という触れ込みです。

## 出回っている情報

### `claude --enable-auto-mode`

複数のニュースサイトやSNSがこのフラグを紹介しています。

- [Awesome Agents](https://awesomeagents.ai/news/claude-code-auto-mode-research-preview/)
- [StartupHub.ai](https://www.startuphub.ai/ai-news/startup-news/2026/claude-code-auto-mode-simplifies-dev-workflow)
- [VKTR](https://www.vktr.com/ai-technology/claude-code-gets-auto-mode-for-longer-coding-sessions/)
- X（Twitter）やThreads上の複数の投稿

ただし、これらの記事は互いに同じ情報を参照し合っている節があり、大元の一次ソースが辿れません。

### `claude --permission-mode auto`

既存の`--permission-mode`フラグの延長として推測された情報です。
`defaultMode`の値として`"auto"`が使えるなら`--permission-mode auto`も動くはず、という理屈ですが、直接的なソースは見つかりませんでした。

## 公式ソースに当たった結果

確認したのは以下の4箇所です。

### 1. 公式ドキュメント（Permissions）

[Configure permissions - Claude Code Docs](https://code.claude.com/docs/en/permissions)

`defaultMode`の選択肢として記載されているのは`default`、`acceptEdits`、`plan`、`dontAsk`、`bypassPermissions`の5つです。`auto`はありません。

ただし、Research Previewの段階ではドキュメントが追いつかないことも珍しくありません。

### 2. CHANGELOG.md

[GitHub CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

Auto Modeの追加日とされる3月12日リリースのv2.1.74を確認しました。「1 flag change, 17 CLI changes, 2 system prompt changes」とありますが、auto modeへの直接的な言及はありません。

主な変更点は`/context`コマンドの改善、`autoMemoryDirectory`設定の追加、ストリーミングレスポンスのメモリリーク修正などです。

### 3. Anthropic公式ブログ

ニュース記事が引用元として挙げている以下の2つを確認しました。

- [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) — 2025年9月の記事。チェックポイント機能やサブエージェントの話で、Auto Modeには触れていない
- [Making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) — サンドボックス機能の解説が中心。Auto Modeの記載なし

Auto Mode単体の発表記事は見つかりませんでした。

### 4. GitHub Issues

[Issue #33587](https://github.com/anthropics/claude-code/issues/33587)で「auto mode temporarily unavailable」というバグが報告されています。報告者は`defaultMode: "auto"`やShift+Tabでの有効化を試みています。

ただし、Research Previewへのアクセス権を持たないユーザーが試して弾かれている可能性があります。「`defaultMode: "auto"`が正しい設定方法だ」と断定する根拠にはなりません。

## 整理

| 項目 | 状況 |
|------|------|
| Auto Modeという機能の存在 | 複数のニュースサイトが報道。ただし一次ソースは不明 |
| `claude --enable-auto-mode` | サードパーティ記事のみ。公式で確認できず |
| `claude --permission-mode auto` | 推測に基づく情報。公式で確認できず |
| `defaultMode: "auto"` | GitHub Issueで使用例あり。動作は未確認 |
| 公式ブログでの発表 | 見つからず |
| CHANGELOGでの記載 | 見つからず |
| 公式ドキュメントでの記載 | 見つからず |

## 現時点での判断

正直なところ、「これが正解」と断定できる情報は見つかりませんでした。

一部ユーザー向けのResearch Previewなので、公式ドキュメントやCHANGELOGに載っていなくても不思議ではありません。段階的なロールアウトで、アクセス権のあるユーザーにだけ機能が見えている可能性があります。

一方で、ニュース記事の情報が互いに循環参照している点は気になります。`--enable-auto-mode`というフラグの出典が追えない以上、鵜呑みにはできません。

リサーチプレビューへのアクセス権がある方は、以下を試してみるのが現実的です。

```bash
# 既存のpermission modeの延長として
claude --permission-mode auto

# ニュース記事で紹介されているフラグ
claude --enable-auto-mode
```

settings.jsonで設定する場合はこの形式です。

```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

セッション中はShift+Tabでモードを切り替えられるので、サイクルの中にauto modeが出てくるかどうかで、アクセス権の有無がわかるはずです。

## 管理者向け: 無効化の方法

組織としてAuto Modeを制限する場合は、managed settingsで`disableAutoMode`を設定します。

| OS | パス |
|----|------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux/WSL | `/etc/claude-code/managed-settings.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` |

```json
{
  "disableAutoMode": "disable"
}
```

## おわりに

`--dangerously-skip-permissions`と通常モードの間を埋めるという方向性自体は待ち望んでいたものです。

ただ、有効化方法の情報が割れており、公式の一次ソースも見つかりません。
Research Previewが広く開放されてドキュメントが整備された段階で、改めて検証するつもりです。

---

**補足（2026-03-13）**: この記事はResearch Preview段階での調査です。状況が変わっている可能性があるため、最新の公式ドキュメントも併せて確認してください。
