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

---

### Q29 (判断)
Go のメソッドは、構造体だけでなく任意の型（例えば `type MyInt int`）に対しても定義できる。

- (A) Yes  
- (B) No  

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

1. `w` と `r` はポインタ同士を相互に参照する循環構造で、実際の読み書きはすべて内部バッファが行う  
2. `r` はサーバー設定の構造体で、`w` はリクエストの中身を読み取るためのストリーム  
3. `w` はレスポンス用の Writer、`r` はクライアントからのリクエスト情報を持つ
4. `w` はリクエスト用の Writer、`r` はクライアントへのレスポンス情報を持つ

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

1. 依存ライブラリを手動でコピーし、すべてモノリポ化するためのフォルダ  
2. スクリプトや設定ファイル（Dockerfile やCI/CD用YAMLなど）を集約し、`main.go` は `apps/` ディレクトリに置く  
3. 実行可能ファイル（`main` パッケージ）を配置して複数のCLIツールやサブアプリケーションを管理しやすくする  
4. 画像やCSSファイル、ビルド成果物などを バージョン管理下で保管しておくための領域

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
`context.WithTimeout(ctx, duration)` を使って一定時間後にキャンセルされるコンテキストを得た場合、タイムアウト後のゴルーチンはどうなるでしょうか？

1. タイムアウトが来た瞬間に、ランタイムがゴルーチンを強制終了させる  
2. ゴルーチンが `<-ctx.Done()` をチェックすれば、キャンセルを受け取って自主的に終了できる  
3. `context.WithTimeout` はデバッグ専用のAPIであり、実行時には何の影響もない  
4. Go は timeout/cancel という概念をサポートしていないため、実行結果は不定

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
- 問: `x.Compare(y)` が正なら x のほうが大きいとみなし、そうでなければ y を返す。**この (穴埋め)**: 何を実装すればいい？

*(紙面ではヒントを出す想定：たとえば `type MyInt int` が `Compare(other any) int` を持つ、など。)*

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

以下のGinハンドラで、リクエストコンテキストを受け取る引数は何と書くか？ 空欄( A ) を埋めよ。

```go
r.POST("/hello", func( (A) *gin.Context) {
    name := (A).Query("name")
    (A).String(200, "Hello %s", name)
})
```

- ヒント：Ginのハンドラは通常 `func(c *gin.Context)` の形をとる。

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
