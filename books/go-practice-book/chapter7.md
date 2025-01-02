---
title: "第7章：応用：簡単なWebサーバ & API 入門"
free: true
---

# 第7章 応用：簡単なWebサーバ & API 入門

## 7.1 はじめに

### 7.1.1 Webサーバの概念をざっくり理解する

現代の多くのサービスは、HTTPという通信プロトコルを使って、クライアント（ブラウザやモバイルアプリ）とサーバ（WebサーバやAPIサーバ）間でデータをやり取りしています。Go言語は標準ライブラリである`net/http`を使うことで、比較的シンプルにHTTPサーバを立ち上げられるのが特徴です。

- **最小限のコード量でWebサーバが動く**  
- **並行処理が得意**なので、大量のリクエストに対しても比較的スケーラブル  
- **バイナリ配布しやすい**ため、Dockerイメージ化や本番デプロイも手軽  

本章では、**「Goで最小限のWebサーバを立ち上げる」** → **「REST APIを作る」** → **「短期実装例としてTodoリストWeb版を組む」**という流れで学習します。もしファイルやDB連携まで踏み込む余裕があれば、より実用的な応用例にも触れてみましょう。

### 7.1.2 何ができるようになるか

- `net/http`パッケージの活用方法  
  - `http.ListenAndServe` や `http.HandleFunc` を使ってポートを開き、HTTPリクエストを受付  
- **JSONの入出力**を通じて、Goと外部のプログラムやブラウザとデータ交換  
- **HTTPメソッド（GET/POST/PUT/DELETE）**を使った簡単なREST APIの構築  
- **TodoリストWeb版**や、在庫管理のようなミニWebアプリの作成  
  - メモリ上やファイル上にデータを保存したり、可能であればDBに連携したりする

### 7.1.3 この章の学習で必要になる基礎知識

- 第1章～第3章の**基本文法・データ構造・関数**  
- 第4章～第5章で触れた**エラーハンドリング**や**並行処理**（後者は使うかどうかオプション）  
- JSON処理 (`encoding/json` など) はこれまであまり扱っていないかもしれませんが、基本は「構造体とのマッピング」をイメージしておけば大丈夫です。

---

## 7.2 `net/http` を使った最小限のWebサーバ

### 7.2.1 まずは「Hello, Web!」

Go言語でWebサーバを立ち上げるもっとも簡単な例は、以下のようなコードです。

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    // ハンドラを登録
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello, Web!")
    })

    // サーバを起動 (ポート8080でListen)
    // 第1引数: ":8080" → ホスト名省略でポート指定のみ
    // 第2引数: ハンドラ(通常はnilでデフォルトServeMuxを使う)
    http.ListenAndServe(":8080", nil)
}
```

このファイルを`hello.go`などとして保存し、`go run hello.go`すると、以下のような挙動が得られます。

- ターミナルにエラーが出なければサーバが起動。ブラウザで `http://localhost:8080` にアクセス  
- ページに「Hello, Web!」という文字列が表示

#### 7.2.1.1 `http.HandleFunc` の動き

- `http.HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request))`  
- `pattern` が`"/"` の場合、**ルートパス**を示す。ここでは「どんなURLでも受け付ける」ような意味合いを持つ。  
- `handler` には、**レスポンスの書き込み先**を表す`http.ResponseWriter`と、**リクエスト情報**を表す`*http.Request`が渡される。

この関数を使い、複数のパスを登録すると、例えば`"/hello"`では「Hello!」と返し、`"/bye"`では「Goodbye!」と返す、といった複数ルーティングが実現します。

```go
http.HandleFunc("/hello", helloHandler)
http.HandleFunc("/bye", byeHandler)
```

### 7.2.2 レスポンスをJSONで返す

**Web API**として最もよく使われるデータ形式がJSON（JavaScript Object Notation）です。Go言語では、標準ライブラリの`encoding/json`が用意されており、構造体やマップをJSON文字列に変換できます。

```go
package main

import (
    "encoding/json"
    "net/http"
)

type Message struct {
    Text string `json:"text"`
    Code int    `json:"code"`
}

func main() {
    http.HandleFunc("/json", func(w http.ResponseWriter, r *http.Request) {
        // レスポンスをJSONで返す例
        w.Header().Set("Content-Type", "application/json; charset=utf-8")
        msg := Message{
            Text: "Hello, JSON World!",
            Code: 200,
        }
        // 構造体をJSONにエンコードして書き込み
        json.NewEncoder(w).Encode(msg)
    })
    http.ListenAndServe(":8080", nil)
}
```

ブラウザやHTTPクライアントで `http://localhost:8080/json` にアクセスすると、`{"text":"Hello, JSON World!","code":200}` のようなレスポンスが得られます。`curl`コマンドなどで確認してみましょう。

```bash
curl -i http://localhost:8080/json
```

#### 7.2.2.1 ポイント

- `w.Header().Set("Content-Type", "application/json; charset=utf-8")` として**レスポンスのContent-Type**を明示的に指定すると、クライアント側で扱いやすくなります。  
- `json.NewEncoder(w).Encode(...)` は、Goの構造体やマップを一気にJSONに変換して`w`に書き込んでくれる便利メソッド。  
- JSONキーと構造体フィールド名を一致させるには、上記のように**タグ**（`` `json:"text"` ``）で指定します。タグが無い場合はデフォルトで大文字始まりのフィールドがJSONキーにも大文字で出力されるため、注意が必要です。

---

## 7.3 簡単なREST APIを組む

### 7.3.1 REST APIって何？

**REST API（Representational State Transfer API）**とは、HTTPメソッド（GET/POST/PUT/DELETEなど）とURLを組み合わせてリソース（データ）に操作を行う形式のWebサービス設計手法です。例えばTodoアプリなら以下のようなAPIがあるかもしれません。

- `GET /todos` : Todoの一覧を取得  
- `POST /todos` : 新しいTodoを追加  
- `PUT /todos/{id}` : 既存のTodoを更新（完了にするなど）  
- `DELETE /todos/{id}` : 指定のTodoを削除

Go言語でこれを実装する場合、**URLのパスやHTTPメソッドごとにハンドラを分ける**か、あるいは**1つのハンドラでメソッドを判定**して振り分ける方法があります。

### 7.3.2 HTTPメソッドの判別

`http.Request`オブジェクトには、`r.Method` というフィールドがあり、"GET" などの文字列が格納されています。例えば「同じURLでメソッドだけ変える」場合、次のように記述します。

```go
func todoHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        // Todo一覧を返す
    case http.MethodPost:
        // Todoを新規作成
    case http.MethodPut:
        // Todoを更新
    case http.MethodDelete:
        // Todoを削除
    default:
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}
```

そして、メイン関数で `http.HandleFunc("/todos", todoHandler)` のように紐づけます。

### 7.3.3 JSONリクエストを解析する

`POST` や `PUT` などでは、クライアント側からJSONデータが送られてくることがあります。Go言語では`r.Body`を`json.NewDecoder(r.Body).Decode(&構造体)`で受け取るだけでOKです。

```go
func todoHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodPost:
        // JSONを構造体にパース
        var newTodo Todo
        err := json.NewDecoder(r.Body).Decode(&newTodo)
        if err != nil {
            http.Error(w, "Invalid JSON", http.StatusBadRequest)
            return
        }
        // newTodo をリストに追加
        // ...
    }
}
```

#### 7.3.3.1 どこにデータを保存する？

- **メモリ上のスライスやマップ**に持つだけなら、実装がシンプル（プログラム終了で消える）  
- **ファイルに保存**するなら、`os.Create`や`os.OpenFile`などでテキストやJSONを読み書き  
- **DB（MySQL, PostgreSQL など）**を使うなら、`database/sql` や ORM(GORMなど)を組み合わせる

本章ではオプション的な扱いですが、DB連携までできると“本物のバックエンド”らしくなります。ただし、**短期集中**で学ぶなら、まずは**メモリ上に保持**（プログラム再起動でデータ消える）でも十分API開発の流れは体験できます。

---

## 7.4 短期実装例：TodoリストWeb版

### 7.4.1 アプリの仕様

- **クライアント**: ブラウザからアクセス。または`curl`などで動作確認。  
- **データ構造**: `Todo`構造体を用意し、`ID`, `Title`, `Done`（完了フラグ）などを保持  
- **APIの概要**:  
  1. `GET /todos` → Todo一覧をJSONで返す  
  2. `POST /todos` → 新しいTodoを追加（JSONボディに `{ "title": "..."} ` など）  
  3. `PUT /todos/{id}` → 指定IDのTodoを更新（完了状態にする等）  
  4. `DELETE /todos/{id}` → 指定IDのTodoを削除  
- **データ保存**: メモリ上のスライス（例: `var todos []Todo`）にする。プログラムを終了すると初期化されるが、今回は短期学習を目的としているため問題なし。

### 7.4.2 コード構成（例）

- `main.go` : メイン関数とサーバ起動処理  
- `todo.go` : `Todo`構造体の定義、サポート関数（ID生成など）  
- `handlers.go` : `/todos` に紐づくハンドラ群 (`getAllTodosHandler`, `createTodoHandler`, etc.)

今回は書籍の紙面の都合上、**すべてのコードをここに載せると長大になる**ため、大まかな流れを示し、**詳細コードはGitHubで公開**する形式にします。  
書籍本文では、**ハンドラ部分**や**JSON処理**のポイントを中心に説明し、**細かなユーティリティコード**は割愛またはリンクにまとめる、という構成が現実的でしょう。

#### 7.4.2.1 例：`todo.go`（部分）

```go
package main

import (
    "sync"
    "atomic"
)

// Todoデータを表す構造体
type Todo struct {
    ID    int    `json:"id"`
    Title string `json:"title"`
    Done  bool   `json:"done"`
}

// スライスと同期制御 (シンプルにsync.Mutexやsync.RWMutexを使う例)
var (
    todos   = []Todo{}
    todosMu sync.Mutex
)

// ID生成用 (例: 原始的に1ずつインクリメント)
var lastID int32

func nextID() int {
    return int(atomic.AddInt32(&lastID, 1))
}
```

> **解説**:  
> - `sync.Mutex` や `sync.RWMutex` を使い、複数リクエストが同時アクセスしても安全に配列を操作できるようにする。  
> - `atomic.AddInt32` で ID をスレッドセーフにインクリメント。実務ならDBのAUTO_INCREMENTやUUIDを使ったりする方法が一般的。

#### 7.4.2.2 例：`handlers.go`（部分）

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"
    "strings"
)

func todosHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        handleGetAllTodos(w, r)
    case http.MethodPost:
        handleCreateTodo(w, r)
    default:
        http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
    }
}

func todoHandler(w http.ResponseWriter, r *http.Request) {
    // URLパスからIDを取り出す (例: "/todos/123" → ID=123)
    // 本来はルーティングを細かく設定する方が好ましいが、ここでは最小実装例
    parts := strings.Split(r.URL.Path, "/")
    if len(parts) < 3 {
        http.Error(w, "Invalid URL", http.StatusBadRequest)
        return
    }
    idStr := parts[2]
    id, err := strconv.Atoi(idStr)
    if err != nil {
        http.Error(w, "Invalid ID", http.StatusBadRequest)
        return
    }

    switch r.Method {
    case http.MethodGet:
        handleGetTodoByID(w, r, id)
    case http.MethodPut:
        handleUpdateTodo(w, r, id)
    case http.MethodDelete:
        handleDeleteTodo(w, r, id)
    default:
        http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
    }
}

// ... (handleGetAllTodos, handleCreateTodoなどの具体実装はGitHub参照)
```

#### 7.4.2.3 例：`main.go`（部分）

```go
package main

import "net/http"

func main() {
    // ルーティングの設定
    http.HandleFunc("/todos", todosHandler) // GET, POST
    http.HandleFunc("/todos/", todoHandler) // GET(by id), PUT, DELETE

    // サーバ起動
    println("Starting server on :8080...")
    http.ListenAndServe(":8080", nil)
}
```

### 7.4.3 確認方法

1. **起動**: `go run main.go todo.go handlers.go` のように複数ファイルを同時コンパイル・実行  
2. **GET /todos**  
   - `curl -X GET http://localhost:8080/todos`  
   - `[]` が返ってきたらOK（最初は空）  
3. **POST /todos**  
   - `curl -X POST -H "Content-Type: application/json" -d '{"title":"Buy milk"}' http://localhost:8080/todos`  
   - 成功すると`{"id":1,"title":"Buy milk","done":false}`のようなJSONが返る  
4. **PUT /todos/1**  
   - `curl -X PUT -H "Content-Type: application/json" -d '{"done":true}' http://localhost:8080/todos/1`  
   - `{"id":1,"title":"Buy milk","done":true}` と更新後のデータが返る想定  
5. **DELETE /todos/1**  
   - `curl -X DELETE http://localhost:8080/todos/1`  
   - 削除が完了すれば`{ "result":"ok" }`やステータスコード 204(No Content)などを返すように実装する場合が多い

ブラウザ拡張（REST client）や`Postman`、`Insomnia`などを使っても動作確認がしやすいです。エラーが発生したりデータが更新されない場合は、**ハンドラの分岐ミス**や**IDの取り扱い**を再度チェックしてみましょう。

---

## 7.5 (オプション) ファイル or DB連携

### 7.5.1 ファイル保存のイメージ

プログラムを終了してもTodoを保持したい場合、JSONファイルに書き出しておくのが簡単です。例えば、`handleCreateTodo`や`handleUpdateTodo`で操作が成功した後に、`saveToFile()`を呼び出し、`todos`スライスをファイルに書き出します。

```go
func saveToFile() error {
    f, err := os.Create("todos.json")
    if err != nil {
        return err
    }
    defer f.Close()

    enc := json.NewEncoder(f)
    return enc.Encode(todos)
}
```

- サーバ起動時に `loadFromFile()` のような関数を呼んで読み込めば、前回の状態を復元できます。  
- ただし、同時に複数リクエストが走っているときは、**ファイルの書き込みタイミング**で競合を起こす可能性があり、しっかりとMutexなどの排他制御を行うか、より高度なデータベースを使う必要があるでしょう。

### 7.5.2 データベース接続 (やや上級)

Go言語でDBを扱うには `database/sql` や GORM 等のORMを利用します。本書の第6章あたりまでに学んだスキルがあれば導入可能ですが、**短期集中**で進める場合は相応の時間を取って学習する必要があります。

- **学習メリット**: 実務により近い状態でAPIサーバを作れる  
- **デメリット**: SQLの基礎や接続設定など、新たな学習コストが生じる  

もし興味があれば、第8章 or 第9章の後に独自に調べてみましょう。

---

## 7.6 章末課題

ここでは、本章で学んだ**Webサーバ**や**REST API**の基礎を応用するための課題を用意しました。**短期であっても、手を動かして課題を解く**ことでグッと理解が深まります。

### 7.6.1 バグ入りコードのデバッグ＆修正

**添付のGitHubリポジトリ**（あるいは書籍付録）の「`webapi_buggy.go`」をダウンロードし、以下の問題点を修正してください。

1. **起動はするが、特定のAPI（`PUT /todos/:id`）がエラーになる**  
   - エラーメッセージやログ出力を頼りに、原因を特定し修正する。  
2. **JSONレスポンスを返す際にContent-Typeが設定されていない**  
   - ブラウザやクライアントがJSONと認識しない問題を解消する。  
3. **IDを数値にパースしている箇所でpanicが発生**  
   - URLパスが正しくない場合、もしくは数字以外の値が来た場合に落ちないようにする。

修正後、`curl`やブラウザ拡張を使って**各エンドポイントが正しく動作する**ことを確認してください。**エラーが発生しそうなパターン**（IDが文字列、ボディが空、など）も試してみましょう。

### 7.6.2 改造課題：Todoリストにフィルタリング機能を追加

自分で実装したTodoリストWeb版（7.4節参照）に、以下の機能を拡張してください。**一部だけでもOKです。**

1. **GET /todos?done=true**  
   - URLクエリパラメータ `done` が指定された場合、完了済み (`Done == true`) のTodoだけを返すようにする。  
   - `r.URL.Query().Get("done")` などでクエリを取得可能。  
2. **優先度フィールドの追加**  
   - `Priority int` フィールドをTodoに追加し、`POST /todos`や`PUT /todos/:id`で優先度を指定できるようにする。  
   - (任意) `GET /todos?priority=1` など、同様にクエリで絞り込み。  
3. **動作確認**  
   - `"title":"Learn Go", "priority":2` をPOSTし、再度GET /todos で表示。  
   - 必要に応じてブラウザでJSONを整形表示する拡張を導入すると見やすい。

### 7.6.3 さらに発展（自由課題）

- **認証機能**: CookieやJWTでユーザを識別する仕組みを追加し、他人のTodoを操作できないようにする。  
- **フロントエンド連携**: Vue.jsやReactなどの簡単なSPAを組み合わせ、TodoをWeb画面で操作できるようにしてみる。GoのHTMLテンプレートを使ってもOK。  
- **並行処理**: 大量のリクエストを送ってみたり、ゴルーチンを使って定期的にバックグラウンドタスク（期限切れTodoの自動処理など）を走らせる。  

---

## 7.7 まとめ & 次へのステップ

### 7.7.1 本章で学んだこと

1. **`net/http` を使った最小限のWebサーバ**  
   - `http.HandleFunc` や `http.ListenAndServe` を用い、ポートを指定してリクエストを受け付ける。  
   - レスポンスは `http.ResponseWriter` に書き込む。JSONを返すときは `encoding/json` を活用しよう。

2. **REST API の基本**  
   - HTTPメソッド（GET/POST/PUT/DELETE）を使い分け、リソース(Todoなど)を操作する。  
   - `r.Method` で判別しつつ、URLパスやクエリパラメータからIDやフィルタ条件を取り出す。  
   - リクエストボディにJSONが入っていれば `json.NewDecoder(r.Body).Decode(...)` でGoの構造体に変換。

3. **短期実装例：TodoリストWeb版**  
   - メモリ上のスライスにデータを保持し、各ハンドラで操作。  
   - (オプション) ファイルやDBに保存すればより実用的に。

### 7.7.2 どこまで踏み込むべきか？

本章はオプション扱いで、**時間があれば**学んでほしい内容です。Web開発に強い関心がある方は、ぜひ**第8章や第9章**（あるいは本書の付録、さらなる書籍・オンライン資料）でDB連携や認証、Docker化などにも挑戦してみてください。

- **Webフレームワーク(Gin/Echoなど)**  
  - 標準ライブラリでも十分動きますが、大規模化するとフレームワークを使ったほうがルーティングやミドルウェア管理が整理される。  
- **クラウドデプロイ**  
  - HerokuやRender、AWSなどにアップしてインターネットからアクセスできるようにすると、学習モチベーションが一気に上がる。  
- **テストコード**  
  - 第4章や第5章で学んだテスト手法をAPIにも適用し、**ハンドラをテストする**仕組みを導入すると、コード品質が上がる。

### 7.7.3 実務・就職で活かすために

Go言語でWebサーバやREST APIを扱えるようになると、**バックエンドエンジニア**としての入り口に立ったと言えます。実務の現場では、これらに加えて以下のスキルが求められることが多いでしょう。

1. **複数環境へのデプロイ (CI/CD)**  
   - テストを自動化し、コードがプッシュされるたびに本番やステージングへデプロイする。  
   - 第8章以降でLintやCIの話が出てくるので、ぜひそちらも参考に。  

2. **セキュリティ**  
   - SQLインジェクションやCSRF、XSSなどの脆弱性対策。  
   - Go言語は型が厳格なので比較的安全性は高いが、HTTPレイヤーの攻撃を防ぐには知識が必要。

3. **チーム開発の流れ**  
   - GitHubフローやPull Request、コードレビューの文化。  
   - 大規模プロジェクトでは、API設計やドキュメント化(SwaggerやOpenAPIなど)も重要。

---

## 7.8 参考リソース & 次の学習ステップ

- **Go公式ドキュメント**  
  - [net/httpパッケージ](https://pkg.go.dev/net/http)  
  - [encoding/jsonパッケージ](https://pkg.go.dev/encoding/json)  
- **Webフレームワーク**  
  - [Gin](https://gin-gonic.com/) / [Echo](https://echo.labstack.com/) など、チュートリアルが豊富  
- **データベース連携**  
  - [database/sql パッケージ](https://pkg.go.dev/database/sql)  
  - [GORM](https://gorm.io/) (ORMライブラリ)

**上記の文献を参照し、今回のTodoリストWeb版をさらに拡張**してみると、Go言語でのバックエンド開発の理解が一層深まるはずです。

---

# 第7章 まとめ

1. **Go言語は標準ライブラリだけでHTTPサーバが実装可能**  
   - `http.HandleFunc` や `http.ListenAndServe` で最小限のコード量。  
   - JSONレスポンスやURLのルーティングもシンプルに書ける。

2. **REST APIの作り方**  
   - HTTPメソッド（GET/POST/PUT/DELETE）とパスを組み合わせて、リソースを操作する設計。  
   - `r.Method` や `strings.Split(r.URL.Path, "/")` を使った実装例を紹介。

3. **短期実装例：TodoリストWeb版**  
   - メモリ上にスライスを持ち、IDの発行とCRUD操作をハンドラで実装。  
   - `curl` や Postmanで呼び出して動作確認を行い、Web APIの基礎を学ぶ。

4. **(オプション) ファイルやDB連携**  
   - 短期で終わらせたいなら、まずはメモリ上でOK。  
   - 実運用を目指すなら、JSONファイル・DBへの永続化やトランザクション管理などが必須。

5. **章末課題**  
   - バグ入りコードのデバッグ＆修正  
   - フィルタリング機能や優先度などの追加要素でアプリを拡張  
   - 余裕があれば認証やフロントエンド連携、ゴルーチンによる非同期タスクなども挑戦可

---

## エピローグ

本章では、「Go言語で**簡単なWebサーバ & API**を作る」プロセスを駆け足で体験しました。ここに**テスト・並行処理・エラー処理**などこれまで学んだ要素を取り入れれば、**小～中規模のバックエンド**であれば十分に実装できる素地が整います。

もちろん、実務レベルで考えると、**複雑な認証・セキュリティ対策・大規模データベース運用・負荷分散**など、より高度な知識が必要となりますが、**いきなり全部を学ぶのはハードルが高い**のも事実。まずは本章のTodoアプリのように小さく作り、動くものを作った上で段階的に機能や設計を深めていくのがおすすめです。

**次のステップ**としては、第8章で解説する「LintツールやCIの導入」や、記憶を定着させる「スペースドリピティション」等の学習法を採り入れれば、**Webアプリ開発スキルをより高い品質と効率で引き上げられる**でしょう。  
そして、最終的な**第9章のまとめテスト**では、Go言語の基礎だけでなく、このWeb開発パートで学んだ知識も総合的に問われます。ぜひ、ここで学んだ内容を活用して、自分なりの**小さなWebサービスを作り、動かし、改良する楽しさ**を味わっていただければと思います。

> **本章の学習を通じて**、あなたは「Go言語でWebサーバを立ち上げ、JSONを返すAPIを構築し、簡単なDB連携（あるいはファイル保存）までを体験する」スキルを得ました。  
> これらは**バックエンドエンジニア**としての第一歩とも言える重要な経験ですので、ぜひ何度もハンドラをいじってリクエストを送ってみるなど、**手を動かす学習**を続けてください。

本章はオプション扱いですが、**Go言語の可能性**を感じるうえで非常に面白いテーマでもあります。どうぞ引き続き学習を楽しんでください。
