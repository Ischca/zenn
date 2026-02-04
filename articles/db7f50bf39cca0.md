---
title: "Tsuzura ― アイデアから公開までをAIで駆け抜けるドキュメントワークスペース"
emoji: "📦"
type: "idea"        # article / idea / tech
topics: ["googlecloud", "vertexai", "pubsub", "firestore", "hackathon", "ai", "aiエージェント"]
published: false
---

## TL;DR
- 非エンジニアでもアイデアを入力するだけでAIが資料・FAQ・PRを生成し、レビュー→マージまで案内するワークスペース
- Vertex AIで生成、Firestoreでタスク状態を永続化、Pub/Subで非同期処理、Cloud Runでフロント/バックエンドをホスト
- 3分デモ動画: [YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## プロダクト概要
新しいプロダクトをゼロから形にしていくクリエイターが、思いついた瞬間に AI と共創できる――Tsuzura はそんな人たちのためのワークスペースです。アイデアを入力すると Vertex AI が設計書やアーキテクチャ図、ローンチストーリーまで伝えるための素材を一気に編み上げ、提示してくれます。クリエイターは完成像をイメージしながら、AIと対話してアイデアを磨き込むだけでよくなります。

裏側では生成されたファイルをGit管理し、Pull Request機能によりレビューとマージができます。画面の変更は保存時に自動的にPR化されることで変更履歴が透明になり、チームの合意形成も数クリックで完了します。手作業でのコピペや導線づくりに時間を奪われることなく、創造性と意思決定に集中できるワークフローを提供します。

## システム構成
```mermaid
graph TD
    subgraph Client
        U[User Browser]
    end
    subgraph Frontend
        FE[Next.js App<br/>Cloud Run]
    end
    subgraph Backend
        BE[Go Backend<br/>Cloud Run]
    end
    subgraph GCP[Google Cloud]
        VS[Vertex AI]
        FS[Firestore]
        PS[Pub/Sub]
        Repo[(Bare Git Repo)]
    end
    U -->|HTTPS| FE
    FE -->|REST /api/*| BE
    BE -->|AI task store| FS
    BE -->|Queue publish/subscribe| PS
    BE -->|Generate content| VS
    BE -->|libgit2| Repo
```

## デモ
- プロダクト: _Cloud Run URL_
- デモ動画: _YouTube URL_
- GitHub: [https://github.com/ischca/tsuzura](https://github.com/ischca/tsuzura)

## 使用技術
- Vertex AI Prediction: 生成モデル (text-bison 等)
- Firestore: `agentTasks` コレクションで状態永続化
- Pub/Sub: `agent-tasks` トピックで非同期ワークフロー
- Cloud Run: フロントエンド（Next.js）/バックエンド（Go）
- Terraform: API enable、Pub/Sub、サービスアカウント構築
