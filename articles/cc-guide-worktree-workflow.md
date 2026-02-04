---
title: "Claude Code実践ガイド: ISSUE.md + worktreeワークフロー"
emoji: "🌳"
type: "tech"
topics: ["claudecode", "ai", "cli", "開発ツール", "git"]
published: false
---

## はじめに

ブランチを切り替えるたびにstashする、という作業を面倒に感じたことはないでしょうか。
Git worktreeを使うとその手間が減ります。
Claude Codeと組み合わせると並列作業がしやすくなります。
この記事では、worktreeとISSUE.mdを使ったワークフローを整理します。

## Git worktreeとは

Git worktreeは、同じリポジトリから複数の作業ディレクトリを作成できるGitの機能です。

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では次のように説明されています。

> Git worktreeを使うと、同じリポジトリから複数のブランチを別々のディレクトリに同時にチェックアウトできます。各worktreeは独立したファイル状態を持つ独自の作業ディレクトリを持ちながら、同じGit履歴を共有します。

通常、1つのリポジトリでは1つのブランチしかチェックアウトできません。
worktreeを使えば複数のブランチを同時に開いて作業できます。

## Claude Codeとworktreeの組み合わせ

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では、Claude Codeとworktreeの組み合わせを以下のように説明しています。

> 複数のタスクを同時に作業する必要があり、Claude Codeインスタンス間で完全なコード分離が必要な場合に使用します。
>
> 各worktreeは独自の独立したファイル状態を持っているため、並列のClaude Codeセッションに最適です。1つのworktreeで行われた変更は他に影響せず、Claudeインスタンスが互いに干渉するのを防ぎます。

つまり以下のような並列作業が可能になります。

- worktree A で Issue #123 を作業（Claude Code インスタンス A）
- worktree B で Issue #456 を作業（Claude Code インスタンス B）

## ISSUE.mdとは

ISSUE.mdは、このシリーズで紹介する独自のプラクティスです。
worktree作成時に、対象Issueの情報をISSUE.mdファイルとして配置します。

ISSUE.mdに含める情報は以下です。

- Issueのタイトルと本文
- 関連するディスカッションコメント
- 関連Issue/PRへのリンク
- 追加のコンテキスト（設計メモ、制約など）

これにより、Claude Codeを起動したときに「このworktreeで何をすべきか」が明確になります。

## なぜこのワークフローが有効か

### 自動化しやすい

worktree作成とISSUE.md生成をスクリプト化できます。
Issue番号を渡すだけで作業環境が整います。

### 方向性が明確

ISSUE.mdを読めば「何をすべきか」がわかります。
Claude Codeに「ISSUE.mdを読んで、計画を立てて」と指示するだけで作業を開始できます。

### 並列作業が可能

複数のworktreeで複数のClaude Codeインスタンスを動かせます。
1つのIssueの作業中に別のIssueも進められます。

### 干渉がない

各worktreeは独立したファイル状態を持つため、あるworktreeでの変更が別のworktreeに影響しません。

## worktreeの基本操作

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)から、基本操作を引用します。

### 新しいworktreeを作成

```bash
# 新しいブランチでworktreeを作成
git worktree add ../project-feature-a -b feature-a

# 既存のブランチでworktreeを作成
git worktree add ../project-bugfix bugfix-123
```

### worktreeでClaude Codeを実行

```bash
# worktreeに移動
cd ../project-feature-a

# Claude Codeを起動
claude
```

### worktreeの管理

```bash
# 全worktreeを一覧表示
git worktree list

# 作業完了後にworktreeを削除
git worktree remove ../project-feature-a
```

## ISSUE.mdの生成

`gh`コマンドを使ってIssue情報を取得し、ISSUE.mdを生成します。

```bash
#!/bin/bash
# start-issue.sh

ISSUE_NUMBER=$1
WORKTREE_DIR="../issue-${ISSUE_NUMBER}"

# worktree作成
git worktree add "$WORKTREE_DIR" -b "issue-${ISSUE_NUMBER}"

# ISSUE.md生成
cd "$WORKTREE_DIR"
{
  echo "# Issue #${ISSUE_NUMBER}"
  echo ""
  gh issue view "$ISSUE_NUMBER"
  echo ""
  echo "## Comments"
  gh issue view "$ISSUE_NUMBER" --comments
} > ISSUE.md

# Claude Codeを起動（新しいターミナルで）
echo "worktree created: $WORKTREE_DIR"
echo "Run: cd $WORKTREE_DIR && claude"
```

使用例です。
```bash
./start-issue.sh 123
```

## Claude Codeでの作業開始

worktreeに移動してClaude Codeを起動したら、以下のように指示します。

```
ISSUE.mdを読んで、このIssueに対応するための計画を立てて。
実装はまだしないで。
```

計画を確認し、問題なければ実装を許可します。

## 注意点

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では以下の注意点が挙げられています。

> 新しい各worktreeでプロジェクトのセットアップに従って開発環境を初期化することを忘れないでください。スタックによって以下が含まれます：
> - JavaScriptプロジェクト：依存関係のインストール（`npm install`、`yarn`）
> - Pythonプロジェクト：仮想環境のセットアップまたはパッケージマネージャでのインストール
> - その他の言語：プロジェクトの標準セットアッププロセスに従う

worktreeは独立したファイル状態を持つため、`node_modules`などは各worktreeで個別にインストールが必要です。

## 実践的なワークフロー

1. Issue選択：取り組むIssueを決める
2. worktree作成：`start-issue.sh`でworktreeとISSUE.mdを生成
3. 環境セットアップ：依存関係のインストール
4. Claude Code起動：worktreeでclaude起動
5. 計画確認：ISSUE.mdを読ませて計画を立てさせる
6. 実装：計画に問題なければ実装
7. PR作成：Claude CodeにPR作成を依頼
8. クリーンアップ：マージ後にworktreeを削除

## まとめ

- Git worktreeは同じリポジトリから複数の作業ディレクトリを作成できる機能
- ISSUE.mdはIssue情報をまとめたファイルで、作業の方向性を明確にする
- worktree + ISSUE.mdで自動化しやすく、並列作業が可能になる
- `gh`コマンドでISSUE.md生成をスクリプト化できる
- 各worktreeで依存関係のインストールが必要なことに注意
