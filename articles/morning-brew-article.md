---
title: "コーヒーを入れている間にAIが開発準備を完了させる - Claude Code用/morning-brewスキルを作った"
emoji: "☕"
type: "tech"
topics: ["claudecode", "ai", "開発効率化", "cli", "python"]
published: false
---

## TL;DR

朝起きて頭が働かない時間、コーヒーを入れている間にClaude Codeが：

- GitHub/Slackから情報を収集
- 昨日の作業の続き（worktree）を検出
- 「今日何する？」と聞いてくる
- 選択したらworktree作成、Issue調査、エディタ起動まで自動でやってくれる

そんな `/morning-brew` スキルを作りました。

## 朝の開発準備、面倒じゃないですか？

毎朝の開発開始時、こんなことしていませんか？

1. Slackを開いて昨日の通知を確認
2. GitHubでレビュー依頼を確認
3. 自分のPRの状態を確認
4. アサインされたIssueを確認
5. 「さて、今日は何からやろうか...」と考える
6. ブランチを切って、worktreeを作って...

**これ、全部AIにやらせればよくない？**

## /morning-brew の動作イメージ

```bash
$ claude
> /morning-brew
```

すると、こんな感じで情報を集めてくれます：

```
情報を収集中...

今日何をする？

○ 続き: fix/post-summary-card-replacement（worktree準備済）
○ 続き: fix/sample-campaign-pattern（worktree準備済）
○ [Sales] #2581 プレキャン設定でパターンを解除できない
○ [Sales] #2600 商品分析の投稿一覧をPostSummaryCardに置換
○ レビュー依頼PRを処理
○ Other
```

選択すると：

```
準備完了！

選択: [Sales] #2581 プレキャン設定でパターンを解除できない
Worktree: ./make-server-worktrees/fix-issue-2581
Issue.md: 作成済み（関連コード調査済み）
エディタ: Zedで開きました

コーヒー飲んで始めよう ☕
```

**コーヒーを入れて戻ってきたら、もう作業開始できる状態になっている。**

## 技術的な仕組み

### Claude Codeのスキル機能

Claude Codeには「スキル」という拡張機能があります。`SKILL.md` というMarkdownファイルで定義し、`/スキル名` で呼び出せます。

```
~/.claude/skills/morning-brew/
├── SKILL.md              # スキル定義
└── scripts/morning_brew.py  # 情報収集スクリプト
```

### SKILL.md の構造

```yaml
---
name: morning-brew
description: |
  毎朝の開発キックオフ・ブリーフィング。
  設定した複数ソース（GitHub/GitLab/Slack）から情報を収集し、
  次のアクションを提案・選択させる。
license: MIT
user-invocable: true
allowed-tools: Bash(git:*) Bash(gh:*) Read Write AskUserQuestion mcp__slack__*
---

# /morning-brew

## 実行手順

### Phase 1: 情報収集
python3 ~/.claude/skills/morning-brew/scripts/morning_brew.py --json

### Phase 2: Slack情報収集
mcp__slack__conversations_history を実行...

### Phase 3: アクション選択
AskUserQuestionで候補を提示...

### Phase 4: 選択後のアクション
worktree作成、Issue.md生成、エディタ起動...
```

**ポイント**: `allowed-tools` でこのスキルが使えるツールを制限できます。安全性を担保しつつ、必要な権限だけを与えられます。

### 情報収集スクリプト（Python）

`gh` CLIと `git` コマンドを活用して情報を収集します：

```python
@dataclass
class ActionCandidate:
    type: str      # "issue", "pr_review", "worktree_continue"
    priority: int  # 1 = 最優先
    title: str
    description: str
    data: Dict[str, Any]

class GitHubSource:
    def fetch_my_prs(self) -> List[PullRequest]:
        result = subprocess.run(
            ['gh', 'pr', 'list', '--author', '@me', '--json', '...'],
            capture_output=True
        )
        ...

    def fetch_assigned_issues(self) -> List[Issue]:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--assignee', '@me', '--json', '...'],
            capture_output=True
        )
        ...

class WorktreeDetector:
    def detect_worktrees(self) -> List[Worktree]:
        # git worktree list でアクティブなworktreeを検出
        ...
```

### Issueの関連PR検索

**Issueだけ見ても実際の進捗がわからない問題**を解決するため、各Issueに関連するPRを自動検索します。

```
#### Issues（関連PR情報付き）
| Issue | 関連PR | 状態 |
|-------|--------|------|
| [Sales] #2603 MCC導線用ページ | 🟣2merged | ⚠️クローズ忘れ？ |
| [Sales] #2600 PostSummaryCard置換 | PR未作成 | 新規着手 |
| [Sales] #2581 パターン解除 | 🟣1merged | ⚠️クローズ忘れ？ |
```

**クロスリポジトリ対応**: IssueがSalesリポジトリにあり、PRがmake-serverリポジトリにあるケースも検索できます。

```python
def _fetch_linked_prs(self, issue_repo, issue_number, issue_url):
    # 全リポジトリでIssueへの参照を検索
    search_terms = [
        f"{repo_short}#{issue_number}",  # Sales#2581
        f"{issue_repo}#{issue_number}",   # appbrew/Sales#2581
        issue_url,                         # 完全URL
    ]
```

これにより：
- **全PRがMERGED** → クローズ忘れの可能性大
- **OPENなPRあり** → 作業継続中
- **PR未作成** → 新規着手が必要

### 優先度ルール

収集した情報を以下の優先度でソートします：

1. **作業中のworktree** - 前日の続きを最優先
2. **レビュー依頼PR** - 他の人をブロックしないように
3. **自分のPR（要対応）** - CHANGES_REQUESTED等
4. **アサインされたIssue** - 新規作業

### 設定ファイル

`~/.claude/morning-brew/config.json` で情報ソースを設定：

```json
{
  "sources": {
    "github": {
      "enabled": true,
      "repos": ["myorg/repo1", "myorg/repo2"],
      "fetch_prs": true,
      "fetch_issues": true
    },
    "slack": {
      "enabled": true,
      "tracked_channels": [
        {"id": "C029JJJFK43", "name": "#daily_dx"}
      ]
    }
  },
  "detection": {
    "worktrees": {
      "enabled": true,
      "paths": ["~/*-worktrees", "./*-worktrees"]
    }
  },
  "post_actions": {
    "issue": {
      "create_worktree": true,
      "create_issue_md": true,
      "open_editor": "zed"
    }
  }
}
```

## AskUserQuestion の活用

Claude Codeの `AskUserQuestion` ツールを使うと、対話的に選択肢を提示できます：

```markdown
### Phase 3: アクション選択
candidatesから選択肢を構築し、AskUserQuestionで提示：

今日何をする？

○ 続き: fix/sample-campaign-pattern（worktree準備済）
○ [Sales] #2581 プレキャン設定でパターンを解除できない
○ レビュー依頼PRを処理
○ Other
```

これにより、CLIでありながらGUIのような操作感を実現しています。

## 選択後の自動準備（post_actions）

Issueを選択した場合の自動処理：

```markdown
### type: "issue" の場合

1. **create_worktree=true の場合**
   - ブランチ名を生成（例: fix/issue-2581-pattern-reset）
   - git worktree add {path} -b {branch} を実行

2. **create_issue_md=true の場合**
   - gh issue view でIssue詳細を取得
   - 関連コードを調査（Grep, Glob）
   - Issue.md を生成してworktreeに配置

3. **open_editor が設定されている場合**
   - zed {worktree_path} でエディタを起動
```

Issue.mdには以下が含まれます：

- Issue本文
- 関連するコードの場所
- 調査結果と実装方針の提案

**コードを読んで理解する時間も短縮できます。**

## なぜ「コーヒーを入れている間」なのか

朝の脳はまだ完全に起動していません。その状態で：

- 何から始めるか判断する
- 情報を収集・整理する
- 環境をセットアップする

これらは**認知負荷が高い**作業です。

一方、AIは：
- 判断は苦手だが、情報収集は得意
- 定型作業の自動化は得意
- 「選択肢を提示する」のは得意

**人間は選ぶだけ。準備はAIがやる。**

これが「コーヒーを入れている間にAIに準備させる」というコンセプトです。

## カスタマイズのポイント

### 配布可能なコア vs 個人設定

このスキルは以下のように分離設計しています：

| 部分 | 内容 | 配布 |
|------|------|------|
| **コア** | 情報収集、優先度付け、候補生成 | 可能 |
| **post_actions** | worktree作成、エディタ起動など | 個人設定 |

`post_actions` は `config.json` で設定するため、スキル本体を配布しても各自の環境・好みに合わせてカスタマイズできます。

### GitLab対応

現在はGitHub中心ですが、設計上はGitLabにも対応可能です：

```json
{
  "sources": {
    "gitlab": {
      "enabled": true,
      "host": "gitlab.example.com",
      "repos": ["group/project"]
    }
  }
}
```

## まとめ

`/morning-brew` は：

- 朝の情報収集・判断の負荷を軽減
- worktree検出で「昨日の続き」をスムーズに
- 選択 → 自動準備で即座に作業開始可能
- 設定ファイルで個人カスタマイズ可能

**朝の15分を、コーヒータイムに変えましょう。**

---

## リンク

- [Claude Code](https://claude.ai/code) - Anthropic公式のCLIツール
- 実装コード: （GitHub公開予定）

## 参考

- Claude Codeのスキル機能は `~/.claude/skills/` にグローバルスキルとして配置可能
- `gh` CLI: GitHub公式のコマンドラインツール
- MCP (Model Context Protocol): Slackなど外部サービスとの連携プロトコル
