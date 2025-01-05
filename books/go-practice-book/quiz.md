---
title: "総合ミニテスト：全範囲復習"
free: true
---

# 総合ミニテスト：全範囲復習

## Level 1（基礎確認）

**難易度**: 初歩～やや易しい。  
**対象トピック**: Go の基本構文、`package main` / `func main()`, 変数/定数、型の概念、if/for の基礎など。

### Q1 (選択)
Go 言語で「実行可能プログラム」を書くとき、必須なのはどれか。

1. ファイル名を `main.go` にしておく
2. `package main` と `func main()` を定義する
3. メイン関数の中で必ず何らかの処理 (print文など) を含める
4. プロジェクトに `import "fmt"` を記述し、実行時に出力を行う

---

### Q2 (選択)
次のコードの説明として正しいものはどれか。

```go
var name string
name = 123
fmt.Println(name)
```

1. Go では、変数をいったん宣言すれば、同じスコープ内で何度でも再代入が可能
2. このコードはコンパイルエラーになる。`name` が `string` なのに `123` (整数) を代入しており、型が不一致だから
3. `fmt.Println` で複数の引数を与えれば、スペース区切りで表示されるので、もし別の変数を足しても簡単に出力できる
4. `var name = 123` と書けば、暗黙の型推論で `name` が int となり、エラーなく `123` と出力するプログラムになる

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

### Q4 (判断)
Go では「定数 (const)」に一度値を代入したら、後から変更できる。

- **(A)** Yes  
- **(B)** No  

---

### Q5 (選択)
Go の `if` 文に関する次の説明のうち、**最も適切なもの**はどれでしょうか。

1. Go の `if` 文は、条件を `( )` で囲む必要があり、さらに一文だけのブロックなら `{ }` を省略できる  
2. Go の `if` 文では初期化文を書くことができるが、その場合は `;` で区切る必要がある
3. Go の `if` 文では、`0` は `false`、それ以外の数値は `true` として扱われる  
4. Go の `if` 文では `( )` は必須ではなく、むしろ省略するのが一般的で、ブロックの括弧 `{ }` は常に必要である  

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

1. `int` は環境依存で32か64か決まるが、通常の数値演算では問題になりにくいのでそのまま使うことが多い
2. Go のコンパイラは整数演算をすべて 64 ビット幅として振る舞うため、`int` を使うと常に倍精度演算が走る  
3. Go では実行時に `int` のビット幅を動的に切り替えられる仕組みがあり、プログラム内でサイズが変化する  
4. 複数アーキテクチャの互換を保つため、Go の `int` はメモリ配置が 2 バイト刻みになるよう自動調整される  

---

### Q9 (穴埋め: 短答)
Go 言語は**（____）型付け言語**と呼ばれる。  
- ヒント: 実行時ではなく**コンパイル時**に型が確定し、型エラーを早期に検出する仕組み。

---

### Q10 (判断)
Go で `:=` を使った短縮宣言は、関数の外（パッケージレベル）でも同様に使える。

- (A) Yes  
- (B) No  

---

## Level 2（中程度・応用寄り）

**難易度**: 入門内容を理解したうえで、スライス、マップ、関数の初歩などを復習。  
**対象トピック**: スライス(`append`, `len`, `cap`)、マップ(追加・更新・削除、nilマップ)、関数・引数、テストの初歩。

### Q11 (選択)
以下のスライスについて、`len` と `cap` の値を正しく説明したものはどれか。

```go
s := make([]int, 3, 5)
```

1. `len(s) = 5, cap(s) = 3` となり、長さ5・容量3のスライスができる 
2. `len(s) = 3, cap(s) = 5` になり、長さ3・容量5のスライスができる
3. Go のスライスは要素数が増減すると自動で `len` と `cap` が再計算されるため、この宣言直後の値は常に不定  
4. この書き方はコンパイルエラーになる

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

1. `delete(m, "Alice")` を呼び出すと指定キーごとエントリを取り除ける
2. `m["Alice"] = 0` と代入すれば、Go ランタイムが“0 値”を検出し自動的にマップからキーを排除する  
3. `m = make(map[string]int)` と再生成するのが一般的で、不要キーだけ消す操作は無駄が多いので推奨されない  
4. Go のマップはイミュータブル（不変）構造なので、削除には一旦新しいマップを作って必要なキーのみコピーする  

---

### Q14 (選択)
次のマップ宣言で、`myMap` が `nil` になるケースはどれか。

1. `var myMap map[string]int` だけで初期化しないと、nil マップになる
2. `myMap = make(map[string]int)` と書いても、最初の代入時に内部的に nil チェックが行われて実体化されないことがある  
3. Go では `map[string]int{}` を書いてもマップ本体が遅延評価されるので、アクセスするまで実態がnilとして扱われる  
4. 宣言のしかたに関係なく、Go のマップはどのタイミングでも書き込み可能なので nil チェックは不要 

---

### Q15 (選択)
以下の関数宣言において、戻り値が `(int, error)` になっているのはなぜか。

```go
func doSomething(a, b int) (int, error) {
    // 中略
}
```

1. Go では複数の戻り値を返せるため、正常結果とエラーを同時に返すのがよくあるスタイル
2. `error` は暗黙的に `int` と互換性があり、0 ならエラー無し、負数なら警告、正数なら致命的エラーを表す  
3. カンマ区切りで書く戻り値は、実は引数として渡される仕組みであり、最後にまとめて処理される  
4. Go ではエラーを返す場合でも `panic` が実行されるため、実質 `(int, error)` はダミー定義に近い  

---

### Q16 (穴埋め)
以下の関数 `sumPositive` は、渡された `nums` スライスの要素のうち、**正の数**だけを合計して返したいという要求があります。空欄( A ) を埋めるとしたら、どの書き方が最も正しいでしょうか？

```go
func sumPositive(nums []int) int {
    total := 0
    for (A) {
        if val > 0 {
            total += val
        }
    }
    return total
}
```

1. `for val in nums:`  
2. `for _, val := range nums`  
3. `for i, val in range nums`  
4. `for i := 0; i < len(nums); i++`

---

### Q17 (穴埋め)
Go で**複数の戻り値**を返す関数を書くとき、どのようなシンタックスを使うか。

```go
func sample(x int) ___ {
    println("Hello")
}
```

---

### Q18 (選択)
Go のテスト (`go test`) でテスト関数を書く際の命名規則は何か。

1. テストファイル名を `test_???_go` とし、関数名は何でもよい  
2. `main.go` の中に `func testMain()` を書けば自動的にテストされる  
3. テストファイル名を `_test.go` とし、関数名を `TestXxx(t *testing.T)` の形にしなければならない  
4. Go では標準テスト機能が無い

---

### Q19 (選択)
`s := []int{10, 20, 30, 40, 50}` とし、`sub := s[1:4]` とした場合、`sub` は何を指すか。

1. `[10,20,30]`  
2. `[20,30,40]`  
3. `[30,40,50]`  
4. `[10,20,30,40]`

---

### Q20 (判断)
Go のマップにおいて、キーを追加・更新する操作 `m[key] = value` は同じ書き方で行える。

- (A) Yes  
- (B) No  

---

## Level 3（中級～やや上級への入り口）

**難易度**: 関数の応用、メソッド、構造体、インターフェースや（軽く）並行処理の入り口などを含む。これまでの内容をさらに踏み込んだ形。

### Q21 (選択)
Go の構造体 (struct) について、正しい説明はどれか。

1. `type Person struct { Name string; Age int }` のように、複数のフィールドをひとまとめにできる
2. Go の構造体はコンパイル時にクラスへ変換され、すべてのフィールドにコンストラクタが自動生成される  
3. フィールド名をすべて大文字にしないと、同じパッケージ内でも構造体のメモリ領域にアクセスできない  
4. 構造体のフィールドにスライスを入れるときは別途 `makeStructSlice(...)` を呼び出すため、標準型を直接使えない  

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

1. 値レシーバでは構造体のコピーを操作し、ポインタレシーバならオリジナルを更新できる
2. ポインタレシーバは内部的にメモリマップを直接いじるため、一度でも `nil` が入ると二度と再利用できなくなる  
3. 値レシーバでメソッドを書くと、メソッド呼び出し中にガーベッジコレクタが動いても安全だが、ポインタだと危険  
4. 動作結果は同じだがコンパイラが選択する命令セットが異なり、最適化の都合でポインタレシーバの方が数倍遅い  

---

### Q23
以下の `Rect` 構造体には `Width` / `Height` があり、メソッド `Area()` は定義済みです。新たに「特定の幅・高さに更新する」処理をしたいが、呼び出し元にも反映されるようにしたい。どうメソッドを定義すればよいでしょうか？

```go
type Rect struct {
    Width  int
    Height int
}

func (r Rect) Area() int {
    return r.Width * r.Height
}
```

1. 
  ```go
  func (r Rect) SetSize(w, h int) {
    r.Width = w
    r.Height = h
  }
  ```

2. 
```go
func (r *Rect) SetSize(w, h int) {
    r.Width = w
    r.Height = h
}
```

3. 
```go
func (r Rect) SetSize(w, h int) Rect {
    r.Width = w
    r.Height = h
    return r
}
```

4. 
```go
func (r *Rect) SetSize(w, h float64) {
    r.Width = int(w)
    r.Height = int(h)
}
```

---

### Q24 (選択)
Go でゴルーチンを起動するキーワードとして正しいのはどれですか？

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
Go における `error` は「(T, error)」で返す慣習がありますが、以下のように**いくつかの段階**（ファイルを開く → JSON デコード → さらに構造体を検証）で失敗するかもしれないコードがあるとします。どの方法が最も一般的でしょうか？

1. すべてのエラーを `panic` にし、recover でまとめてハンドリング  
2. 各段階で `(T, error)` を返し、呼び出し元が `if err != nil { return ... }` する  
3. Go はエラー概念を持たないため、C言語的に 0/1 を戻す  
4. デバッグ時のみ fmt.Println(...) でエラーを表示し、本番は何もチェックしない

---

### Q27 (選択)
以下の並行処理コードで、チャネル `results` が `make(chan string)` として作られている。正しい説明はどれか。

```go
msg := <- results
```

1. これは受信ブロックを表し、`results` から文字列が送られてくるまで待つ  
2. これは送信ブロックを表し、msg が入るまで待つ  
3. Go では `<-` 演算子は存在しない  
4. これはデッドロックを必ず起こす

---

### Q28 (穴埋め)
以下の `worker` 関数を**並行**に3つ起動し、それぞれが特定の仕事をする。一方、メイン関数が先に終わってしまうとプログラム全体が終了してしまう。Go で待ち合わせるにはどうすべきでしょうか？

```go
func main() {
    for i := 0; i < 3; i++ {
        go worker(i)
    }
    // ここでどうやって「3つのworkerすべて終了」を待てるか？
    fmt.Println("all done")
}
```

1. time.Sleep(5 * time.Second) で大体待つ  
2. sync.WaitGroup を使って Add(3), Done(), Wait() を組み合わせる  
3. 3つの global bool 変数を worker で true にして main でfor{}でチェック  
4. net.Conn を使って Socket通信し、closeを検知する
---

### Q29 (判断)
Go のメソッドは、構造体だけでなく任意の型（例えば `type MyInt int`）に対しても定義できる。

- (A) Yes  
- (B) No  

---

### Q30 (短答)
Go で「複数の戻り値 `(result, error)`」を返す設計の背景として、「例外をスローせず明示的に扱う」方針があります。では、エラーをどうやって呼び出し側に伝え、処理するのが一般的でしょうか？

1. 例外発生時はコンパイラがエラーコードを埋め込み、実行停止する  
2. `(result, err)` を返し、呼び出し側が `if err != nil { ... }` で対処する  
3. `panic` を起こし、recover しなければ即プロセス終了  
4. Go にはエラーと例外の概念が存在しない

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

1. (A) `case v := <-dataCh:` 、 (B) `case <-time.After(5 * time.Second):`  
2. (A) `v := <-dataCh:` 、 (B) `<-time.After(5 * time.Second):`  
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
}
```

**質問**:  
「`urls` が3つあるのに、受信 (`<-results`) が1回しか行われず、そのままメイン関数が終了を待たずに？ → 実はデッドロック」といった不備がある。**どう直せばデッドロックを防げるか**を簡潔に答えてください。

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

1. `any` はあらゆる型を受け取れるが、`>` 演算子が使える型とは限らないためコンパイルエラー
2. Go のジェネリクスはすべて数値比較が可能な仕様なので、本来 `a > b` は許されるが `return b` が未定義になる  
3. `T` がインターフェースの場合は比較できず、具体型の場合のみ比較できるがコンパイラは型を判定しない  
4. ジェネリクスを使うときは `map[T]T` のような構文を必ず書く必要があるので、この例は誤用  

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
`fmt.Errorf("wrap: %w", err)` で元のエラーを包む利点を1行で述べよ。

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

1. `default:` がある場合、チャネルが準備されていなくても即座に抜けられるためブロックを回避できる
2. `default:` を書くとすべてのチャネル受信が無効化され、次のコード行に強制ジャンプが行われる  
3. `select` が並行に複数の受信を待てなくなるので、必ずひとつのチャネルしか扱えない構造になる  
4. `default` はswitch文専用のキーワードなので、`select` で使うとコンパイルエラーになる

---

## Level5（高度な設計・Web・大規模開発視点）

**対象トピック例**: Webハンドラ / `net/http` / ディレクトリ構造 / モジュール管理 / Contextやジェネリクス応用 / Docker活用など

### Q41 (選択: net/http)
Go の Gin フレームワークを使って「複数のグループ ( `/api/v1/*` と `/api/v2/*` )」を定義し、それぞれ別のミドルウェアを適用したいとします。以下のコード例ではどう書けば、`/api/v1/users` と `/api/v2/items` それぞれに違うミドルウェアを適用できるでしょうか？

(1)
```go
r := gin.Default()
r.Group("/api")
r.Group("/v1")
r.Group("/v2")

// ... define routes ...
r.Run()
```

(2)
```go
r := gin.Default()
v1 := r.Group("/api/v1", v1Middleware)
{
    v1.GET("/users", usersHandler)
}
v2 := r.Group("/api/v2", v2Middleware)
{
    v2.GET("/items", itemsHandler)
}
r.Run()
```

(3)
```go
r := gin.Default()
r.Use("/api/v1", v1Middleware)
r.Use("/api/v2", v2Middleware)
r.Run()
```

(4)
```go
r := gin.New()
r.Prefix("/api").Prefix("/v1").Use(v1Middleware)
r.Prefix("/api").Prefix("/v2").Use(v2Middleware)
r.Run()
```

---

### Q42 (選択: Handlerのシグネチャ)
`http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {...})` の引数 `w` と `r` は何？

1. `w` と `r` はポインタ同士を相互に参照する循環構造で、実際の読み書きはすべて内部バッファが行う  
2. `r` はサーバー設定の構造体で、`w` はリクエストの中身を読み取るためのストリーム  
3. `w` はレスポンス用の Writer、`r` はクライアントからのリクエスト情報を持つ
4. `w` はリクエスト用の Writer、`r` はクライアントへのレスポンス情報を持つ

---

### Q43 (穴埋め: Go module)
モジュール管理で `go.mod` を生成するには `go mod init ...` が定番ですが、**複数のモジュールパス**を同じリポジトリ内で別々に設定したいケースがあります。たとえば subディレクトリごとに異なる `go.mod` を置きたい場合、正しく進めるには？

1. リポジトリ直下で `go mod init rootModule` すればサブディレクトリも自動で別モジュールになる  
2. 各サブディレクトリに cd して `go mod init <modulePath>` を行い、マルチモジュール構成にする  
3. sub1/ sub2/ のフォルダ名を vendor/ に変えればモジュール分割される  
4. Gitのサブモジュールを導入してモジュール管理するとGoが自動推論する
---

### Q44 (選択: ディレクトリ構造)
小規模～中規模Goプロジェクトの一般的なディレクトリ構造例で「`cmd/` ディレクトリ」の役割は何か？

1. 依存ライブラリを手動でコピーし、すべてモノリポ化するためのフォルダ  
2. スクリプトや設定ファイル（Dockerfile やCI/CD用YAMLなど）を集約し、`main.go` は `apps/` ディレクトリに置く  
3. 実行可能ファイル（`main` パッケージ）を配置して複数のCLIツールやサブアプリケーションを管理しやすくする  
4. 画像やCSSファイル、ビルド成果物などを バージョン管理下で保管しておくための領域

---

### Q45 (選択: Docker + Go)
Go には `init` 関数があり、パッケージ読み込み時に自動実行されます。プロジェクト内に多数のパッケージがあり、それぞれ複数 `init` を書いていたとします。その場合の挙動や注意点として正しいのはどれでしょうか？

1. すべての init 関数はソースファイルの記述順に呼ばれるため、後から書いた順番で優先して実行される  
2. init は main 関数より後に呼ばれるので実行順序を制御できる  
3. Go は `init` 関数が複数ある場合、コンパイルエラーになる  
4. パッケージ間の依存関係 (import順) が決まった後、各パッケージの init が順に呼ばれるが、多用すると読みづらくなる

---

### Q46 (短答: テストカバレッジ)
`go test -cover` で実行すると何がわかる？

- 解答欄: ___

*(例：テストで実行されたコードの割合を確認できる)*

---

### Q47 (選択: context.WithTimeout)
`context.WithTimeout(ctx, duration)` を使って一定時間後にキャンセルされるコンテキストを得た場合、タイムアウト後のゴルーチンはどうなるでしょうか？

1. タイムアウトが来た瞬間に、ランタイムがゴルーチンを強制終了させる  
2. ゴルーチンが `<-ctx.Done()` をチェックすれば、キャンセルを受け取って自主的に終了できる  
3. `context.WithTimeout` はデバッグ専用のAPIであり、実行時には何の影響もない  
4. Go は timeout/cancel という概念をサポートしていないため、実行結果は不定

---

### Q48 (選択: ジェネリクス応用)
Go のジェネリクスで「型パラメータを2つ受け取り、それぞれに異なる制約」を付与したいケースがあります。以下の空欄を埋める正しい構文は何ですか？

```go
import "golang.org/x/exp/constraints"

func combine[???](x T, y U) bool {
    // T は Ordered(比較可能)
    // U は 何でも可
    return x > T(0) // など比較使用
}
```

1. `[T constraints.Ordered | U any]`  
2. `[T constraints.Ordered, U any]`  
3. `[T, U constraints.Ordered]`  
4. `[constraints.Ordered T, any U]`

---

### Q49 (穴埋め: interface + generics)
以下に `Comparable` インターフェースと `maxOf[T Comparable]` 関数があるが、**複数種類の型**（int版, string版 など）を統合的に扱いたいとします。「どんな実装方法」が望ましいか？

```go
type Comparable interface {
    Compare(other any) int
}

func maxOf[T Comparable](x, y T) T {
    if x.Compare(y) > 0 { return x }
    return y
}
```

1. 演算子オーバーロードを定義し、`x > y` を直接書けるようにする  
2. それぞれの型 (MyInt, MyString etc.) が Compare(o any) メソッド内で自分の型にアサートし、大小比較を実装する  
3. Reflection でおおざっぱに `val := reflect.ValueOf(x)` → compare any し、空文字なら負数等  
4. panic していれば maxOf が呼ばれた時点で強制終了する

---

### Q50 (選択: reflect活用)
Go のリフレクション (`reflect`) を使うと何ができるでしょうか？

1. 実行中にソースコードを再コンパイルして、新たな関数を動的に生成する  
2. Go のバイナリ全体を逆アセンブルして、アセンブリ言語に変換して表示する  
3. ランタイム時に型の情報を取得し、動的にフィールド値やメソッドを読み書きできる  
4. Go の型に対して、例外のスローを自在に挿入して例外ハンドラをカスタマイズできる  

---

### Q51 (選択：Gin の基本ルート設定)
Go の Gin フレームワークで最もシンプルなWebサーバを起動し、`GET /ping` にアクセスすると `"pong"` を返す例のコードとして正しいものはどれでしょうか？  

1. 
```go
r := gin.Default()  
r.GET("/ping", func(c *gin.Context) {  
    c.JSON(200, gin.H{"message": "pong"})  
})  
r.Run()  
```

2. 
```go
r := gin.New()  
r.HttpGet("/ping", "pong")  
r.Listen(":8080")  
```

3. 
```go
http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {  
    fmt.Fprintln(w, "pong")  
})  
http.ListenAndServe(":8080", nil)  
```

4. 
```go
gin.Start("/ping", "pong")  
```

---

### Q52 (穴埋め：Ginハンドラの引数)
Gin でPOSTリクエストを受け取り、JSON をパースしてレスポンスを返したい。以下の例で、(A) には典型的にどんな名前を使い、そして JSON をどうバインドするのが一般的か？

```go
r.POST("/api", func((A) *gin.Context) {
    var req struct {
        ID   int    `json:"id"`
        Name string `json:"name"`
    }
    // JSONバインドして ID, Name を取得 → c.JSON で返す
})
```

1. func(r *gin.Context), r.BindForm(req)  
2. func(c *gin.Context), c.ShouldBindJSON(&req)  
3. func(ctx *http.Request), ctx.ParseMultipartForm(...)  
4. func(aaa *gin.Data), ?

---

### Q53 (選択：JSONバインド)
Gin でクライアントが送ってきた JSON ボディを自動的に構造体にバインドする際によく使われるメソッドはどれか？

1. `c.ShouldBindJSON(&obj)`
2. `c.QueryObject(&obj)`
3. `c.DecodeJSON(obj)`
4. `json.NewDecoder(c).Decode(obj)`

---

### Q54 (短答：ステータスコードとJSON)

Gin のハンドラ内で「ステータスコード201 を返しつつ JSON ボディ」を送りたい。1行の書き方を示せ。

- 例：`c._____(201, gin.H{"id": newID})`

---

### Q55 (選択：URIパラメータ)

以下のように `GET /users/:id` を定義したルートから、`id` を取得したい場合、ハンドラでどう書く？

```go
r.GET("/users/:id", func(c *gin.Context) {
    // IDを取り出して表示
})
```

1. `id := c.Query(":id")`
2. `id := c.Param("id")`
3. `id := c.FormValue("id")`
4. `id, ok := c.Get("id")`

---

### Q56 (穴埋め：ルートグルーピング)

Gin で複数のルートに同じPrefixを付けたい場合、以下のように書ける。空欄 ( B ) を埋めてください。

```go
r := gin.Default()

api := r.(B)("/api")
{
    api.GET("/ping", pingHandler)
    api.POST("/users", createUserHandler)
}

r.Run(":8080")
```

- ヒント： `/api/ping`、`/api/users` といったルートになるようにする。

---

### Q57 (選択：ミドルウェアの追加)

Gin でグローバルミドルウェア（例：ロギングやリカバリ）を有効にする際の方法はどれか？

1. `r.Use(myMiddleware)`  
2. `gin.SetMiddleware(myMiddleware)`  
3. `http.HandleMiddleware(myMiddleware)`  
4. `myMiddleware(r)`

---

### Q58 (穴埋め：DBとGin ハンドラ)

以下の関数例では `db *sql.DB` を受け取り、それをクロージャで使うようにしている。空欄( C ) を埋めよ。

```go
func main() {
    db, _ := sql.Open("mysql", "...")

    r := gin.Default()
    r.GET("/items", getItemsHandler(db))
    r.Run()
}

func getItemsHandler( (C) ) gin.HandlerFunc {
    return func(c *gin.Context) {
       // ここで db.Query(...) など使う
    }
}
```

---

### Q59 (選択：クエリ文字列 vs JSONボディ)

Gin でクエリパラメータ（`GET /something?name=foo`）を取得するには？

1. `c.PostForm("name")`
2. `c.Query("name")`
3. `c.ShouldBindQuery(name)`
4. `c.BindURI(&name)`

---

### Q60 (短答：400 BadRequest)

以下のシーンで **400 BadRequest** としてレスポンスを返す一行を示せ。メッセージ `"Invalid input"` を JSON で返したい。

```go
// ...
// c.???(??? , gin.H{"error": "Invalid input"})
```

*(ヒント： code=400, JSON body={"error": "..."} )*
