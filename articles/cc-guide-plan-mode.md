---
title: "Claude Code実践ガイド: 計画ファースト（Planモード）の進め方"
emoji: "📋"
type: "tech"
topics: ["claudecode", "ai", "cli", "開発ツール"]
published: false
---

## はじめに

いきなりコードを書かせるか、まず計画を立てさせるか。Claude Codeには選択肢があります。計画を立てさせた方が手戻りが減ることが多いので、私はPlanモードを頻繁に使っています。この記事では、Planモードの仕組みと使いどころを整理します。

## Planモードとは

Planモードは、Claude Codeの実行モードの一つで、コードの分析と計画立案に特化した動作をします。

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では次のように説明されています：

> Planモードは、読み取り専用の操作でコードベースを分析して計画を作成するようClaudeに指示します。コードベースの探索、複雑な変更の計画、またはコードの安全なレビューに最適です。

通常モードではClaudeはファイルの読み書き、コマンドの実行など様々な操作ができますが、Planモードでは「読み取りと調査」に限定されます。

## Planモードで使えるツール

[公式ドキュメント](https://claudelog.com/mechanics/plan-mode/)では、Planモードでアクセス可能なツールを以下のように説明しています：

**使えるツール（読み取り・調査系）**
- Read - ファイルとコンテンツの閲覧
- LS - ディレクトリ一覧
- Glob - ファイルパターン検索
- Grep - コンテンツ検索
- Task - 調査エージェント
- WebFetch - Webコンテンツ分析
- WebSearch - Web検索

**使えないツール（変更系）**
- Edit/MultiEdit - ファイル編集
- Write - ファイル作成
- Bash - コマンド実行（読み取り専用以外）

つまりPlanモードでは「調査と計画はできるが、実際の変更はできない」状態になります。

## Extended Thinkingとの関係

Claude Codeには「Extended Thinking（拡張思考）」という機能もあります。Planモードと混同しやすいですが、別の概念です。

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では次のように説明されています：

> Extended Thinkingはデフォルトで有効になっており、出力トークン予算の一部（最大31,999トークン）を、Claudeが複雑な問題をステップバイステップで推論するために確保します。

- **Extended Thinking**：「深く考える」機能。内部で推論を重ねてから回答する。
- **Planモード**：「変更せず調査・計画に専念する」モード。使えるツールが制限される。

両者は補完的に働きます。Planモードで調査しながら、Extended Thinkingで深く考える、という組み合わせが可能です。

[Anthropicのベストプラクティス](https://www.anthropic.com/engineering/claude-code-best-practices)では、Extended Thinkingのトリガーについて次のように述べています：

> 「think」という言葉を使ってExtended Thinkingモードをトリガーすることを推奨します。これにより、Claudeに代替案をより徹底的に評価するための追加の計算時間が与えられます。これらの特定のフレーズは、システム内で増加する思考バジェットのレベルに直接マッピングされています：「think」<「think hard」<「think harder」<「ultrathink」

## なぜ計画から始めるべきか

[Anthropicのベストプラクティス](https://www.anthropic.com/engineering/claude-code-best-practices)では、推奨ワークフローを以下のように説明しています：

> 1. 関連ファイル、画像、URLを読むようClaudeに依頼します。一般的なポインター（「ロギングを処理するファイルを読んで」）または特定のファイル名（「logging.pyを読んで」）のいずれかを提供しますが、まだコードを書かないように明示的に伝えます。
>
> 2. 特定の問題にどうアプローチするか計画を立てるようClaudeに依頼します。「think」という言葉を使ってExtended Thinkingモードをトリガーすることを推奨します。
>
> 3. Claudeにコードで解決策を実装するよう依頼します。
>
> 4. Claudeに結果をコミットしてPRを作成するよう依頼します。
>
> **ステップ1-2は重要です—これらがないと、Claudeは直接コーディングに飛び込む傾向があります。**

計画なしで実装を始めると、以下の問題が発生しやすくなります：
- 前提の認識がズレていて、根本から作り直し
- 影響範囲を見落として、後から修正が必要
- 対応漏れが発生して、追加作業が発生

計画段階で「何を」「なぜ」「どうやって」を合意しておけば、これらの問題を防げます。

## Planモードの使い方

### セッション中に切り替える

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)では次のように説明されています：

> セッション中にPlanモードをオンにするには、**Shift+Tab**を使用してパーミッションモードを切り替えます。
>
> 通常モードの場合、**Shift+Tab**は最初にAuto-Acceptモードに切り替わります（ターミナル下部に`⏵⏵ accept edits on`と表示）。次の**Shift+Tab**でPlanモードに切り替わります（`⏸ plan mode on`と表示）。

### Planモードでセッションを開始する

```bash
claude --permission-mode plan
```

### ヘッドレスモードでPlanモードを使う

```bash
claude --permission-mode plan -p "認証システムを分析して改善提案をして"
```

### デフォルトでPlanモードを有効にする

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## 実践的なワークフロー

### 複雑なリファクタリングの計画

[公式ドキュメント](https://code.claude.com/docs/en/common-workflows)の例：

```
claude --permission-mode plan

> 認証システムをOAuth2に移行する必要がある。詳細な移行計画を作成して。
```

Claudeは現在の実装を分析し、包括的な計画を作成します。フォローアップで詳細化できます：

```
> 後方互換性についてはどうする？
> データベースマイグレーションはどう扱うべき？
```

計画に納得したら、Planモードを解除して実装に移ります。

### 全ての実装作業で計画から始める

小さな修正でも、まず「どこをどう変えるか」を確認させることを習慣化します。

```
> この機能を追加したい。まず計画を立てて。実装はまだしないで。
```

計画を確認し、問題なければ実装を許可します。

## 計画で確認すべき項目

計画段階で以下を明確にしておきます：

- **ゴール**：何を達成したいか
- **背景・制約**：なぜこの変更が必要か
- **受け入れ基準**：どうなったら「完了」と言えるか
- **禁止事項**：やってはいけないこと
- **想定外の扱い**：計画外の問題が見つかったときの対処方針

## まとめ

- Planモードは読み取り専用の操作でコードベースを分析・計画するモード
- Extended Thinkingとは別の概念（Planモード＝ツール制限、Extended Thinking＝深い思考）
- 計画から始めることで手戻りを防げる
- `Shift+Tab`または`--permission-mode plan`で有効化
- 全ての実装で「計画→確認→実装」の流れを習慣化する
