# 総合ミニテスト 解答編（Level 1～3）

## Level 1（基礎確認）

### Q1 (選択)
**問題**: Go 言語で「実行可能プログラム」を書くときに必須なのは？  
**解答**: **(1) `package main` と `func main()` が必須**  

- **解説**: Go でバイナリを生成し実行するプログラムは、`package main` + エントリーポイント `func main()` のセットが必要です。ファイル名やインポートなどは関係ありません。

---

### Q2 (選択)
**問題**: 次のコードについて正しい説明は？
```go
var name string
name = 123
fmt.Println(name)
```
**解答**: **(1)** `123` は数値なので型が合わず、コンパイルエラーになる

- **解説**: `name` が `string` 型なのに `123` (整数) を代入しようとすると、Go の厳格な型チェックによりコンパイルエラー。自動で `"123"` になるわけではありません。

---

### Q3 (穴埋め)
**問題**: コード内で `x` に `10` を初期値として与える際、Go の短縮宣言 (`:=`) を使う。  
```go
func main() {
    _____
    fmt.Println(x) // 10
}
```
**解答例**:
```go
x := 10
```

- **解説**: `:=` によって「宣言 + 型推論 + 初期化」を同時に行う書き方。ここで x は `int` となる。

---

### Q4 (判断: True/False)
**問題**: Go で `const` に一度値を代入したら、その後変更できる？  
**解答**: **(B) False**（変更不可）

- **解説**: Go の `const` は再代入できない。コンパイル時にエラーとなる。

---

### Q5 (選択)
**問題**: Go の `if` 文で条件に `( )` を付けるかどうか？
**解答**: **(2)** 付けても構わないが、省略するのが推奨

- **解説**: 慣習的に `if x > 0 { ... }` のように `( )` は省略します。付けるとエラーにはなりませんが、Go の公式スタイルとは離れるので推奨されません。

---

### Q6 (単純記述)
**問題**: `for i := 0; i < 5; i++ { ... }` は何回ループするか？  
**解答**: **5回**

- **解説**: i=0,1,2,3,4 の計5回。

---

### Q7 (穴埋め: switch)
**問題**: 
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
**解答例**:
- (A) → `case`
- (B) → `case`
- (C) → `default:`

完成:
```go
switch x {
case 1:
    fmt.Println("one")
case 2:
    fmt.Println("two")
default:
    fmt.Println("other")
}
```

- **解説**: Go の switch で case に当てはまらなければ `default` が実行される。

---

### Q8 (選択)
**問題**: `int` がプラットフォーム依存(32 or 64bit)だが、一般的にどうするか？  
**解答**: **(2) `int` でOK**

- **解説**: 初心者は細かく `int32` / `int64` を使い分けるより、まず `int` を使って問題ありません。

---

### Q9 (穴埋め: 単答)
**問題**: Go は「______型付け言語」？  
**解答**: **静的型付け**（「静的型付け言語」）

- **解説**: 実行前にコンパイルで型を確定させ、不整合をエラーにする仕組み。

---

### Q10 (判断: True/False)
**問題**: `:=` はパッケージレベルでも同様に使えるか？  
**解答**: **(B) False**

- **解説**: `:=` は**関数内**でのみ使用可能。パッケージスコープで `:=` はコンパイルエラー。

---

## Level 2（中程度）

### Q11 (選択: スライスの len と cap)
**問題**:
```go
s := make([]int, 3, 5)
```
`len(s)` と `cap(s)` の値は？

**解答**: **(1) len=3, cap=5**

- **解説**: make([]int, 3, 5) は「長さ3 / 容量5」のスライス。`s[0..2]` が使われ、あと2個まで伸びても再アロケーション不要。

---

### Q12 (穴埋め)
**問題**: スライスに要素を追加する関数。  
```go
nums := []int{}
nums = _____(nums, 10)
nums = _____(nums, 20)
```
**解答**: **append**

```go
nums = append(nums, 10)
nums = append(nums, 20)
```

---

### Q13 (選択: マップの削除)
**問題**: Go のマップで `"Alice"` を削除  
**解答**: **(3) `delete(m, "Alice")`**

- **解説**: Go でマップの要素を削除する組込み関数は `delete(map, key)`。

---

### Q14 (選択: nil マップ)
**問題**: どの宣言が `nil` になる？
1. `myMap := map[string]int{}`  
2. `myMap := make(map[string]int)`  
3. `var myMap map[string]int`  
4. すべて nil にはならない

**解答**: **(3)**

- **解説**: `var myMap map[string]int` は `nil` マップ。`map[string]int{}` と `make(map[string]int)` は空だがnilではない。書き込み可。

---

### Q15 (選択: 複数戻り値 `(int, error)` の理由)
**問題**:
```go
func doSomething(a, b int) (int, error) {...}
```
何故 `(int, error)` とするか？  
**解答**: **(2)** Go は複数戻り値を返すのが一般的で、エラーを第2戻り値で表す慣習がある

- **解説**: 代表的パターンとして `(T, error)`。Go ではこれが例外の代わりになっている。

---

### Q16 (穴埋め: sumSlice)
```go
func sumSlice(nums []int) int {
    total := 0
    for __, val := range nums {
        total += val
    }
    return total
}
```
**解答**:  
```go
for _, val := range nums {
    total += val
}
```
- **解説**: range スライスで `for _, val := range nums`。

---

### Q17 (穴埋め: 複数戻り値のシンタックス)
**問題**: Go で複数戻り値 `(int, bool)` を返すには？

**解答例**:  
```go
func sample(x int) (int, bool) {
    // ...
}
```

- **解説**: `(型, 型, ...)` の形で複数並べる。

---

### Q18 (選択: Go のテストファイル)
**問題**: テスト関数の書き方  
**解答**: **(1) `_test.go` + `TestXxx(t *testing.T)`**

- **解説**: Go で `go test` する際、テストファイル名は `_test.go` で終わり、テスト関数は `Test◯◯` が通例。

---

### Q19 (選択: スライスの部分範囲)
**問題**:
```go
s := []int{10, 20, 30, 40, 50}
sub := s[1:4]
```
**解答**: **(2) [20,30,40]**

- **解説**: s[1], s[2], s[3] → 20, 30, 40

---

### Q20 (判断: True/False: マップ追加・更新)
**問題**: Go のマップ `m[key] = value` は追加と更新で同じ書き方？

**解答**: **(A) True**  

- **解説**: もし `key` が存在しなければ追加、存在すれば上書き。異なる操作だが記法は同じ。

---

## Level 3（中級～やや上級入り口）

### Q21 (選択: 構造体とは)
```go
type Person struct { Name string; Age int }
```
**解答**: **(1) フィールドをまとめたカスタム型**

- **解説**: Go の構造体はフィールドを束ねるための型。継承はサポートしていないし、すべてが公開されるわけでもない（大文字/小文字で可視性を制御できる）。

---

### Q22 (選択: 値レシーバとポインタレシーバ)
**問題**:
```go
func (p Person) ChangeName(...) { ... }
func (p *Person) UpdateAge(...) { ... }
```
何が違う？

**解答**: **(3) 値レシーバはコピー、ポインタレシーバは元を直接変更**

- **解説**: (1) と (2) を合わせた説明が正解。値レシーバではメソッド内の変更が呼び出し元に反映されない。ポインタなら反映される。

---

### Q23 (穴埋め: メソッド)
```go
func (r *Rect) (A)(w int, h int) {
    r.Width = w
    r.Height = h
}
```
**解答例**: `Resize`

- **解説**: 任意の名前だが、意味の通る名称をつける。レシーバが `*Rect` なので、呼び出し元の `Width/Height` を変えられるメソッド。

---

### Q24 (選択: ゴルーチン起動)
**解答**: **(2) `go` キーワード**

- **解説**: `go funcName(...)` と書くと、その関数を並行に起動するゴルーチンとなる。

---

### Q25 (選択: インターフェースの実装)
**解答**: **(2) 暗黙の実装 (全メソッドを持っていればOK)**

- **解説**: Go では「interface」を満たすかどうかを宣言的に書かず、メソッド一致で判断する。

---

### Q26 (単純回答: `error`型)
**問題**: `error`型は何を表すためのもの？  
**解答例**: 「関数や処理が失敗した理由やエラー状態を表すために使う型」

- **解説**: Go は例外ではなく `(T, error)` の形式でエラーを返す設計。

---

### Q27 (選択: チャネル受信)
**解答**: **(1)** 受信ブロックを表し、`results` から値が送られてくるまで待つ

- **解説**: `<- ch` は**受信**。`ch <- x` が送信。Go のチャネルで `<-` の左右が異なる。

---

### Q28 (穴埋め: ゴルーチンで sayHello)
```go
go sayHello()
```
- **解説**: ゴルーチン起動キーワードは `go`。

---

### Q29 (判断: True/False: メソッドのレシーバは任意の型)
**解答**: **(A) True**

- **解説**: Go では自作の型（ `type MyInt int`）など、ほぼ任意の型にメソッドを定義できる。

---

### Q30 (短答: 複数戻り値 `(result, error)` の設計意図)
**解答例**:
- 「例外をスローせず、`(T, error)` の戻り値によって明示的にエラーを扱うため。」

- **解説**: Go は `panic` もあるが通常は非推奨。エラーの多くは `(normalResult, err)` の形で返し、呼び出し元が `if err != nil` を明示的に書く設計が主流。

---

## **Level 4 (Q31～Q40)**

### Q31 (選択: `select` で複数チャネル待ち)

**問題 (再掲)**:
```go
select {
( A )
    fmt.Println("got from dataCh:", v)
( B )
    fmt.Println("timeout!")
}
```

**解答**:  
- (A) → `case v := <-dataCh:`  
- (B) → `case <-time.After(5 * time.Second):`

**理由**:  
- `select { case v := <-dataCh: ... case <-time.After(...): ... }` というパターンが代表的。`v = dataCh:` のような書き方はエラーです。

---

### Q32 (選択: WaitGroup)

**問題 (再掲)**: Go の並行処理で `WaitGroup` を使う目的は？  
**解答**: **(1)** 「メイン関数が終わる前に全ゴルーチンが終了するまで待つため」

**解説**:  
- `sync.WaitGroup` によって「起動するゴルーチンの数をAddし、Doneを呼んでWaitする」仕組みが得られる。ゴルーチン終了を待たずにメインが終わるとプログラム自体が終了してしまうのを防げる。

---

### Q33 (記述: デッドロック修正)

**問題 (再掲)**: コード補足付きの「URLの数だけ送信するのに1回しか受信していない」バグ。  
**解答例**:

- **回答**: 「`len(urls)` 回だけ `res := <- results` を行う（ループで3回受信）すればOK」  
  - 例:  
    ```go
    for i := 0; i < len(urls); i++ {
        res := <-results
        fmt.Println(res)
    }
    ```  
  - または `WaitGroup` を使ってゴルーチンが終わるのを待つ方法なども考えられるが、単純には「送信分だけ受信する」ロジックが大切。

**解説**:  
- ゴルーチンが3回 `results <- ...` を行うなら、メイン側も3回 `<-results` しなければチャネルが詰まり、デッドロックになる。

---

### Q34 (穴埋め: context)

**問題 (再掲)**:
```go
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

**解答**: **(A) `ctx.Done()`**

**解説**:  
- `ctx.Done()` は「キャンセルやタイムアウトが通知されるチャネル」。`case <-ctx.Done(): return` としておけば、キャンセル時にループを抜けられる。

---

### Q35 (選択: ジェネリクス基礎)

```go
func max[T any](a, b T) T {
    if a > b { ... } ...
}
```

**解答**: **(1)** 「`>` を使える型制約を指定していないためエラー」

**解説**:  
- `any` はすべての型を受け付けるが `>` 演算子が定義される保証はない。`constraints.Ordered` などで比較可能型と縛る必要がある。

---

### Q36 (穴埋め: constraints.Ordered)

**問題 (再掲)**:
```go
func maxVal[T (B)](x, y T) T {
    if x > y {
        return x
    }
    return y
}
```
**解答**: **(B) → `constraints.Ordered`**

```go
func maxVal[T constraints.Ordered](x, y T) T { ... }
```

---

### Q37 (選択: カスタム制約)

**解答**: **(1)** 「`type MyConstraint interface { ~int|~float64 }` のようにインターフェースで定義」

**解説**:  
- Go 1.18～ で `~` を使い、型パラメータの底型を指定するなど自作の constraint を定義できる。  
- (2) は誤り（標準ライブラリのみとは限らない）。

---

### Q38 (記述: ラップエラー `%w`)

**問題**: `fmt.Errorf("wrap: %w", err)` で元のエラーを包む利点を1行で述べる。

**解答例**:  
- 「上位レイヤーで `errors.Is` / `errors.As` を使って、包まれた元エラーを判定できるようになる。」

**解説**:  
- `%w` でラップする → `errors.Is` / `errors.As` により原因となるエラーを遡って調べられる。

---

### Q39 (穴埋め: sync.Mutex)

```go
var mu sync.Mutex
var count int

func increment() {
    mu.(C)()
    count++
    mu.(D)()
}
```

**解答**:  
- (C) → `Lock`  
- (D) → `Unlock`

```go
mu.Lock()
count++
mu.Unlock()
```

---

### Q40 (選択: `select` + `default:`)

**解答**: **(1)** 「`default:` に進む場合があり、チャネル操作がブロックせずにスキップされる」

**解説**:  
- `select { case ...: case ...: default: ... }` の場合、いずれのcaseも準備できていないなら `default:` が即実行される → チャネルのブロックを回避。  
- (2) は誤り（最優先ではなく、他のcaseが直ちにreadyならそちらが選ばれる）。(4) はタイムアウトと関係ない。

---

## **Level 5 (Q41～Q50)**

### Q41 (選択: net/http)

```go
http.HandleFunc("/", handler)
____.ListenAndServe(":8080", nil)
```

**解答**: `http.ListenAndServe(":8080", nil)`

**解説**:  
- Go の最小Webサーバは `http.HandleFunc` でハンドラ登録後、`http.ListenAndServe`。ハンドラは `nil` でデフォルトのServeMuxを使う。

---

### Q42 (選択: ハンドラのシグネチャ)

**解答**: **(2)** `w` がレスポンス（Writer）で `r` がリクエスト情報

**解説**:  
- `func(w http.ResponseWriter, r *http.Request)` が基本形。`w.Write(...)` でレスポンスを書き出す。

---

### Q43 (穴埋め: Go module)

```bash
cd myproject
___ init example.com/myproject
```

**解答**: **`go`**  

```bash
go init example.com/myproject
```

(*厳密には `go mod init example.com/myproject`*)

---

### Q44 (選択: ディレクトリ構造で `cmd/`)

**解答**: **(2)** 実行可能ファイル（`main` パッケージ）を置く場所

**解説**:  
- 多くのプロジェクト構成例で `cmd/xxx/` ディレクトリに実行ファイル用のmainパッケージを置く。ライブラリは `pkg/` や `internal/` に置く例が多い。

---

### Q45 (選択: Docker マルチステージビルド)

**解答**: **(1)** 「1つ目のステージで `go build`、2つ目でバイナリだけをコピーし小さいイメージを作る」

**解説**:  
- これがよくあるDockerfileのマルチステージ構成。`go build` 用に大きなイメージを使い、その後小さいランタイムイメージにバイナリだけ移す。

---

### Q46 (短答: テストカバレッジ)

**解答例**:  
- 「テストで実際に実行されたコード行の割合（カバレッジ）を確認できる。」

**解説**:  
- `go test -cover` で関数や行がどのくらいテストされているか%表示してくれる。

---

### Q47 (選択: context.WithTimeout)

**解答**: **(3)** 「キャンセルが発生したら `<-ctx.Done()` を見て自主的に終了する」

**解説**:  
- Go のコンテキストは「強制終了」ではなく「キャンセルシグナル」。受け取るゴルーチンが `select { case <-ctx.Done(): return }` として協調的に停止する。

---

### Q48 (選択: ジェネリクス多型パラメータ)

**解答**: **(2) `func combine[T, U](a T, b U) string { ... }`**

**解説**:  
- 複数の型パラメータがあるなら `[T, U]` のようにカンマ区切り。`(a T, b U)` で受け取る。

---

### Q49 (穴埋め: interface + generics)

**問題**の例:
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
**解答**: 「`T` が `Comparable` を実装し、`Compare(other any) int` を提供する必要がある。具体的には `Compare` メソッドを定義する。」

- **解説**: たとえば  
  ```go
  type MyInt int
  func (m MyInt) Compare(o any) int {
      other, ok := o.(MyInt)
      if !ok { /* handle error */ }
      if m > other { return 1 }
      if m < other { return -1 }
      return 0
  }
  ```
  のように書くことで `maxOf` で比較できる。

---

### Q50 (選択: reflect)

**解答**: **(1)** 「ランタイム時に型情報を取得し、動的にフィールドを読み書きできる。」

**解説**:  
- `reflect` パッケージは**Java の Reflection のように**ランタイムで型を検査する仕組み。Go独自のAPIでフィールド名やタグを取得し、値を変更したりできる。
