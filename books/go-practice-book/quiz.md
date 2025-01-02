---
title: "総合ミニテスト：全範囲復習"
---

# 総合ミニテスト：全範囲復習

## Level 1（基礎確認）

**難易度**: 初歩～やや易しい。  
**対象トピック**: Go の基本構文、`package main` / `func main()`, 変数/定数、型の概念、if/for の基礎など。

### Q1 (選択)
Go 言語で「実行可能プログラム」を書くとき、必須なのはどれか。

1. **`package main` と `func main()` が必須**  
2. ファイル名を `go_program.gx` にする  
3. `import "os"` を必ず書く  
4. どのファイルでもいいが `//main()` コメントがある

---

### Q2 (選択)
次のコードの説明として正しいものはどれか。

```go
var name string
name = 123
fmt.Println(name)
```

1. `name` は `string` だが `123` は数値 → コンパイルエラー  
2. `123` を文字列として自動的に `"123"` に変換 → 正常に動く  
3. 実行時に警告が出るが動く  
4. コードは無限ループになる

---

### Q3 (穴埋め)
以下のコードで `x` に `10` を初期値として与えたい。ただし、Go の**短縮宣言** (`:=`) を使う。

```go
func main() {
    _____
    fmt.Println(x) // 10
}
```

- ヒント: `:=` は「宣言 + 初期化 + 型推論」の書き方。

---

### Q4 (判断: True/False)
Go では「定数 (const)」に一度値を代入したら、後から変更できる。

- **(A)** True  
- **(B)** False  

---

### Q5 (選択)
Go の `if` 文において、条件部分を `( )` で囲む書き方について、慣習的にどう扱うか。

1. 必須ではないが、付けるとコンパイル警告になる  
2. 付けても構わないが、省略するのが推奨  
3. 付けないとコンパイルエラーになる  
4. Go では if が存在しない

---

### Q6 (単純記述)
Go の `for` ループで、`i := 0; i < 5; i++` のように書いた場合、実際には **何回** ループが回るか？  
- 解答欄: _______ 回

---

### Q7 (穴埋め)
以下の `switch` 文で「x が 1 の時、2 の時、どちらでもない時」を出力したい。空欄 (A)(B)(C) を埋める。

```go
switch x {
( A ) 1:
    fmt.Println("one")
( B ) 2:
    fmt.Println("two")
( C ):
    fmt.Println("other")
}
```

- ヒント: Go では `( )` は不要。`default:` を書くのが「どれにも該当しない」場合のハンドル。

---

### Q8 (選択)
Go の整数型 `int` は、プラットフォームによって32ビット or 64ビットになる可能性があるが、その違いに一般的にどう対処するか？

1. 明示的に `int32` や `int64` を必ず使う  
2. 初心者は細かいことを気にせずに `int` を使っても問題ない  
3. 32ビット OS 上では Go が自動的に64ビットのエミュレーションを行う  
4. Go では常に64ビット固定

---

### Q9 (穴埋め: 短答)
Go 言語は**（____）型付け言語**と呼ばれる。  
- ヒント: 実行時ではなく**コンパイル時**に型が確定し、型エラーを早期に検出する仕組み。

---

### Q10 (判断: True/False)
Go で `:=` を使った短縮宣言は、関数の外（パッケージレベル）でも同様に使える。

- (A) True  
- (B) False  

---

## Level 2（中程度・応用寄り）

**難易度**: 入門内容を理解したうえで、スライス、マップ、関数の初歩などを復習。  
**対象トピック**: スライス(`append`, `len`, `cap`)、マップ(追加・更新・削除、nilマップ)、関数・引数、テストの初歩。

### Q11 (選択)
以下のスライスについて、`len` と `cap` の値を正しく説明したものはどれか。

```go
s := make([]int, 3, 5)
```

1. `len(s) = 3, cap(s) = 5`  
2. `len(s) = 5, cap(s) = 3`  
3. `len(s) = 3, cap(s) = 3`  
4. `len(s) = 0, cap(s) = 5`

---

### Q12 (穴埋め)
スライスに要素を追加するための標準ライブラリ関数は何か？下記の空欄に当てはまるのは。

```go
nums := []int{}
nums = _____(nums, 10)
nums = _____(nums, 20)
```

---

### Q13 (選択)
Go のマップ `map[string]int` で、あるキー `"Alice"` を削除するにはどう書くか。

1. `m["Alice"] = nil`  
2. `m.Delete("Alice")`  
3. `delete(m, "Alice")`  
4. `clear(m, "Alice")`

---

### Q14 (選択)
次のマップ宣言で、`myMap` が `nil` になるケースはどれか。

1. `myMap := map[string]int{}`  
2. `myMap := make(map[string]int)`  
3. `var myMap map[string]int`  
4. すべて `nil` にはならない

---

### Q15 (選択)
以下の関数宣言において、戻り値が `(int, error)` になっているのはなぜか。

```go
func doSomething(a, b int) (int, error) {
    // 中略
}
```

1. C 言語風に戻り値を1つだけ返す方法がGoにはないから  
2. Go では複数の戻り値を返すのが一般的で、エラーを第2戻り値で表す慣習がある  
3. Go には `error` 型が存在せずエラーは int で示すが、ここでは擬似的に書いているだけ  
4. 戻り値を2つ書くとコンパイルエラー

---

### Q16 (穴埋め)
以下の関数を完成させて、`nums` スライスの合計を返すようにしたい。

```go
func sumSlice(nums []int) int {
    total := 0
    for __, val := range nums {
        total += val
    }
    return total
}
```

- 空欄を埋めよ（range 文の書き方）。

---

### Q17 (穴埋め)
Go で**複数の戻り値**を返す関数を書くとき、どのようなシンタックスを使うか。

- 例: `(int, bool)` のように丸カッコで括った形式を答える。  
- 解答例: `func sample(x int) (??? , ???) { ... }`

---

### Q18 (選択)
Go のテスト (`go test`) でテスト関数を書く際の命名規則は何か。

1. テストファイル名を `_test.go` とし、関数名を `TestXxx(t *testing.T)` の形にする  
2. テストファイル名を `test_???_go` とし、関数名は何でもよい  
3. `main.go` の中に `func testMain()` を書けば自動的にテストされる  
4. Go では標準テスト機能が無い

---

### Q19 (選択)
`s := []int{10, 20, 30, 40, 50}` とし、`sub := s[1:4]` とした場合、`sub` は何を指すか。

1. `[10,20,30]`  
2. `[20,30,40]`  
3. `[30,40,50]`  
4. `[10,20,30,40]`

---

### Q20 (判断: True/False)
Go のマップにおいて、キーを追加・更新する操作 `m[key] = value` は同じ書き方で行える。

- (A) True  
- (B) False  

---

## Level 3（中級～やや上級への入り口）

**難易度**: 関数の応用、メソッド、構造体、インターフェースや（軽く）並行処理の入り口などを含む。これまでの内容をさらに踏み込んだ形。

### Q21 (選択)
Go の構造体 (struct) について、正しい説明はどれか。

1. フィールドをまとめたカスタム型であり、`type Person struct { Name string; Age int }` のように定義する  
2. 構造体は必ずクラス継承の仕組みを使って派生させる  
3. Go では構造体は存在せず、代わりに配列で管理する  
4. フィールドはすべて公開され、非公開にできない

---

### Q22 (選択)
以下のメソッド宣言で `(p Person)` と `(p *Person)` が異なる理由は何か。

```go
func (p Person) ChangeName(newName string) {
    p.Name = newName
}
func (p *Person) UpdateAge(newAge int) {
    p.Age = newAge
}
```

1. 値レシーバ `(p Person)` は構造体のコピーを操作するため、呼び出し元には反映されない  
2. ポインタレシーバ `(p *Person)` は元データを直接書き換える可能性がある  
3. 上2つを合わせた説明が正しい  
4. Go にはポインタレシーバと値レシーバの区別はない

---

### Q23 (穴埋め: メソッド)

```go
type Rect struct {
    Width  int
    Height int
}

func (r Rect) Area() int {
    return r.Width * r.Height
}

func (r *Rect) (A)(w int, h int) {
    r.Width = w
    r.Height = h
}
```

- (A) に当てはまるメソッド名は、例えば `Resize` など自由だが、「**値レシーバ vs ポインタレシーバ**」に着目して書き換える関数をどう呼ぶか意図が伝わる名称を。

---

### Q24 (選択)
Go の並行処理で、ゴルーチンを起動するキーワードはどれか。

1. `defer`  
2. `go`  
3. `switch`  
4. `run`

---

### Q25 (選択)
Go のインターフェースはどのように実装が判断されるか。

1. 明示的に `implements InterfaceName` と書く  
2. 構造体が「インターフェースが要求するメソッドを全て持っていれば」暗黙的に実装とみなされる  
3. `interface{}` は何でも受け取れるが実装判定はできない  
4. インターフェースはJavaやC#だけにある概念で、Goには存在しない

---

### Q26 (単純回答)
Go における「`error`型」は何を表すためのもの？短い説明で：

- 解答欄: ___

*(例: 関数が失敗時の理由を返すための型、など)*

---

### Q27 (選択)
以下の並行処理コードで、チャネル `results` が `make(chan string)` として作られている。受信するにはどう書くか？

```go
msg := <- results
```

1. これは受信ブロックを表し、`results` から文字列が送られてくるまで待つ  
2. これは送信ブロックを表し、msg が入るまで待つ  
3. Go では `<-` 演算子は存在しない  
4. これはデッドロックを必ず起こす

---

### Q28 (穴埋め)
以下の関数を完成させ、**並行**に動くゴルーチンを1つ起動し、「Hello from goroutine」と出力したい。

```go
func main() {
    __ sayHello() // ここでゴルーチン起動
    fmt.Println("Hello from main")
}

func sayHello() {
    fmt.Println("Hello from goroutine")
}
```

- (__) に `go` を書くなど。  

---

### Q29 (判断: True/False)
Go のメソッドは、構造体だけでなく任意の型（例えば `type MyInt int`）に対しても定義できる。

- (A) True  
- (B) False  

---

### Q30 (短答)
Go で「複数の戻り値 `(result, error)`」を返す慣習は、**エラーをスローせずに明示的に取り扱う**ための設計意図である。  
- 質問: Go では「例外(Exception)」の仕組みは基本的に使わず、代わりに何を使うか？  
- 解答欄: ____

*(ヒント: `(T, error)` のように返す / `panic` もあるが一般的ではない)*

---

## Level4（上級並行処理・ジェネリクス初歩 など）

**対象トピック例**: 
- 並行処理の実践（`select`、`sync` パッケージの使い方など）  
- `context` によるキャンセル  
- ジェネリクスの基礎（型パラメータ・constraints）  
- エラーハンドリングの応用

### Q31 (選択)
以下のコードは複数のチャネルを同時に待つために書かれています。どの構文が正しいか？

```go
select {
( A )
    fmt.Println("got from dataCh:", v)
( B )
    fmt.Println("timeout!")
}
```

1. (A) `v := <-dataCh:` 、 (B) `time.After(5 * time.Second):`  
2. (A) `v = dataCh:` 、 (B) `time.After(5 * time.Second) > 0:`  
3. (A) `case dataCh-> v:` 、 (B) `case timeout:`  
4. (A) `if dataCh != nil` 、 (B) `default:`

---

### Q32 (選択)
Go の並行処理で「WaitGroup」を使う目的は何か？

1. すべてのゴルーチンが終了するまでメイン関数が終わらないようにするため  
2. ゴルーチンを終了強制するため  
3. “シングルトン”パターンを実装するため  
4. `select` 構文で使わないとコンパイルエラーになる

---

### Q33 (記述)
以下の関数はゴルーチンを複数起動し、それぞれが計算結果をチャネルに送信します。メイン関数側は**URL の数だけ受信**して結果を集約するアイデアです。**「受信回数が不十分でデッドロックになる」**バグがある場合、どのように直せばよいか簡潔に書いてください。

```go
// 以下は複数のゴルーチンを起動し、それぞれが計算結果をチャネル results に送る例
// main関数側は本来「URLの数だけ受信」して結果を集約するつもりだが、受信回数が足りないためデッドロックが起きるバグがある

func main() {
    urls := []string{
        "http://example.com/a",
        "http://example.com/b",
        "http://example.com/c",
    }
    results := make(chan string) // 送られる結果は文字列と仮定

    // ゴルーチンを起動
    for _, url := range urls {
        go func(u string) {
            // 何か処理 (ダウンロードなど)
            results <- "Result from " + u
        }(url)
    }

    // ここで受信が足りない
    // 例: 1回しか受信していない -> 残りの送信が詰まってデッドロック
    res := <-results
    fmt.Println(res)

    // 修正策を考えて回答する
}
```

**質問**:  
「`urls` が3つあるのに、受信 (`<-results`) が1回しか行われず、そのままメイン関数が終了を待たずに？ → 実はデッドロック」といった不備がある。**どう直せばデッドロックを防げるか**を簡潔に答えてください。

**ヒント**: 
- ゴルーチンが `results <- ...` を3回送信するが、受信が1回しかないと、残り2回目/3回目の送信が詰まってデッドロックになる。  
- 修正：たとえば `for i := 0; i < len(urls); i++ { ... }` で複数回受信するなど方法はいくつかある。

---

### Q34 (穴埋め: context)
以下のコードはキャンセル可能なコンテキストを使ってゴルーチンを停止したい例です。

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    go work(ctx)
    // しばらくして
    cancel()
}

func work(ctx context.Context) {
    for {
        select {
        case <- (A):
            return
        default:
            // 作業を続行
        }
    }
}
```

- (A) に何を入れるか？

---

### Q35 (選択: ジェネリクス基礎)
以下のジェネリック関数がコンパイルエラーになる理由は？

```go
func max[T any](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

1. `>` 演算子を使える型 (constraints.Orderedなど) を指定していないから  
2. Go にジェネリクスは存在しないから  
3. `any` は interface{} の別名なので比較不可  
4. 上記コードは正しく動き、エラーにはならない

---

### Q36 (穴埋め: ジェネリクス)
以下のように「型パラメータ `T` が`constraints.Ordered` な場合のみ `>` 演算子を使う」関数を完成させよ。

```go
func maxVal[T (B)](x, y T) T {
    if x > y {
        return x
    }
    return y
}
```
- (B) に当てはまるものは何か？
  - ヒント: `constraints.` から始まる型制約。

---

### Q37 (選択: カスタム制約)
Go で自作の制約 (constraint) を定義する場合の書き方は？

1. `type MyConstraint interface { ~int|~float64 }` のようにインターフェースで定義  
2. constraints は標準ライブラリのみでカスタム不可  
3. constraintを作るには `constraint MyConstraint = "T"` と書く  
4. ジェネリクスで制約は使わない

---

### Q38 (記述: エラーハンドリング応用)
Go のエラーは `(T, error)` の形が主流だが、「ラップエラー (`%w`)」 や `errors.Is` / `errors.As` による原因判定が可能である。  
**Q**: `fmt.Errorf("wrap: %w", err)` で元のエラーを包む利点を1行で述べよ。

---

### Q39 (穴埋め: sync.Mutex)
以下は共有データに排他ロックをかける例です。

```go
var mu sync.Mutex
var count int

func increment() {
    mu.(C)()
    count++
    mu.(D)()
}
```
- (C) と (D) は何を呼び出す？

---

### Q40 (選択: `select` + `default` )
並行処理で `select` 文に `default:` 節を入れるとどうなるか？

1. チャネル操作がブロックせず、すぐ `default:` に進む場合がある  
2. 他のcaseが用意されていても強制的に`default:` が最優先  
3. default:は存在しないキーワード  
4. select がタイムアウトを判断する

---

## Level5（高度な設計・Web・大規模開発視点）

**対象トピック例**: Webハンドラ / `net/http` / ディレクトリ構造 / モジュール管理 / Contextやジェネリクス応用 / Docker活用など

### Q41 (選択: net/http)
Go で**最小限のWebサーバ**を起動するにはどうするか？

```go
http.HandleFunc("/", handler)
____.ListenAndServe(":8080", nil)
```
1. `package nethttp`  
2. `http`  
3. `server`  
4. `router`

---

### Q42 (選択: Handlerのシグネチャ)
`http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {...})` の引数 `w` と `r` は何？

1. `w` は「クライアントから来たリクエスト本体」、`r` は「サーバへのレスポンス」  
2. `w` がレスポンス書き込み先 (Writer), `r` がリクエスト情報  
3. 特に意味はなく、任意の変数  
4. Go にはWebサーバ機能がない

---

### Q43 (穴埋め: Go module)
Go モジュール化で `go.mod` を作るには？

```bash
cd myproject
___ init example.com/myproject
```
- 何を入れれば `go.mod` が生成されるか？

---

### Q44 (選択: ディレクトリ構造)
小規模～中規模Goプロジェクトの一般的なディレクトリ構造例で「`cmd/` ディレクトリ」の役割は何か？

1. ライブラリをまとめる場所  
2. 実行可能ファイル（mainパッケージ）を置く場所  
3. 外部のサードパーティライブラリが入る場所  
4. Dockerfileを保管するディレクトリ

---

### Q45 (選択: Docker + Go)
GoのバイナリをDockerコンテナで動かす際、マルチステージビルドの典型例とは？

1. 1つ目のステージで `go build`、2つ目のステージでバイナリだけコピーして最小イメージ化  
2. Dockerfileを2つ用意して同時にビルド  
3. `docker-run main.go` で自動的に2ステージ  
4. GoはDocker非対応

---

### Q46 (短答: テストカバレッジ)
`go test -cover` で実行すると何がわかる？

- 解答欄: ___

*(例：テストで実行されたコードの割合を確認できる)*

---

### Q47 (選択: context.WithTimeout)
`context.WithTimeout` を使うと「一定時間でキャンセルされるコンテキスト」が得られるが、タイムアウト後にゴルーチンがどうなるか？

1. 自動でpanicが発生してプログラムが終了  
2. すべてのgoroutineが強制終了  
3. そのコンテキストを見ているゴルーチンが `<-ctx.Done()` を受信すれば自主的に終了する  
4. とくに何も起きない

---

### Q48 (選択: ジェネリクス応用)
以下のジェネリック関数で、複数の型パラメータを使うときの正しい書き方は？

```go
func combine[T, U](a T, b U) string {
    // ...
}
```
1. `func combine(T, U)(a T, b U) string { ... }`  
2. `func combine[T, U](a T, b U) string { ... }`  
3. `func combine[T; U](a T, b U) string { ... }`  
4. `func combine(a T, b U) string [T, U]`

---

### Q49 (穴埋め: interface + generics)
```go
type Comparable interface {
    Compare(other any) int
}

func maxOf[T Comparable](x, y T) T {
    if x.Compare(y) > 0 {
        return x
    }
    return y
}
```
- このように、ジェネリクスでインターフェースを**型パラメータの制約**として使用できる。  
- 質問: `x.Compare(y)` が正なら x のほうが大きいとみなし、そうでなければ y を返す。**この (穴埋め)**: 何を実装すればいい？

*(紙面ではヒントを出す想定：たとえば `type MyInt int` が `Compare(other any) int` を持つ、など。)*

---

### Q50 (選択: reflect活用)
Go の反射 (`reflect`) を使うと何ができるか？

1. ランタイム時に型の情報を取得し、動的にフィールドを読み書きできる  
2. コード上のすべての変数名が自動的に暗号化される  
3. OSのカーネル機能を直接呼び出す  
4. JavaのReflection APIをインポートする

---
