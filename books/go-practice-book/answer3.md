# 解答

## ミニテスト(1)

> **対象範囲**: 関数、構造体、メソッド、可視性  
> **形式**: 選択問題、穴埋め問題など

---

### 1-1. 選択問題：関数とローカル変数

#### 問題（再掲・変更後）
1. 「Go言語で複数の戻り値を返す関数として最も一般的で正しい書き方はどれか」  
   - (A) `func divide(a, b int) int, error { ... }`  
   - (B) `func divide(a, b int) (int, error) { ... }`  
   - (C) `func divide(a, b int) (int)(error) { ... }`  ← 意図的に文法的におかしい形  
   - (D) `func divide(a, b int) error, int { ... }`  

2. 以下のコードでは、`if` ブロックの中で宣言した変数 `y` を外で使おうとしてエラーになります。なぜか？  
   ```go
   func example() {
       x := 10
       if x > 5 {
           y := x * 2
       }
       fmt.Println(y) // ??
   }
   ```
   - (A) `y` はブロックのスコープ内でしか有効でないため  
   - (B) Go にはif文が存在しないため  
   - (C) ローカル変数はすべてグローバルになるため  
   - (D) 実行時にパニックが発生するため  

#### 解答

1. **答え**: **(B)**  
   - (B) の `(int, error)` が **Go で一般的に使われる「複数の戻り値」** の形。  
   - (C) は明らかに文法的に不正 (`(int)(error)`)。(A) と (D) もカンマの位置が間違っている。  

2. **答え**: **(A)**  
   - 変数 `y` はブロック `{}` 内だけ有効なスコープを持つため、`if` を抜けた後で `y` にアクセスしようとするとコンパイルエラーになる。

---

### 1-2. 選択問題：メソッド（値レシーバとポインタレシーバ）

#### 問題（再掲）
以下の `UpdateName` メソッドは値レシーバで定義されています。

```go
type Person struct {
    Name string
    Age  int
}

func (p Person) UpdateName(newName string) {
    p.Name = newName
}
```

このときの挙動について正しい選択肢はどれか。

- (A) `p.Name` は必ず更新され、呼び出し元の `Person` にも反映される  
- (B) `p.Name` はコピーを操作しているため、元の `Person` は変わらない  
- (C) このコードはコンパイルエラーになる（メソッドは常にポインタレシーバが必要だから）  
- (D) `UpdateName` が実行されると自動的に Age も変更される  

#### 解答

- **答え**: **(B)**  
  - 値レシーバ（`(p Person)`) の場合、メソッド内の `p` は構造体のコピーであり、呼び出し元のデータは更新されません。

---

### 1-3. 穴埋め問題: 可視性（大文字/小文字）とメソッド

#### 問題（再掲）
```go
type (Ａ) struct {
    Name  string
    Score int
}

func (s (Ａ)) (Ｂ) {
    fmt.Printf("Name=%s, Score=%d\n", s.Name, s.Score)
}

func (s *(Ａ)) (Ｃ) {
    s.Score += 10
}
```

**(Ａ)** には構造体名、(Ｂ)(Ｃ) にはメソッド名を大文字/小文字で書き分けること。

#### 解答

- (Ａ) → `Student` (大文字開始: 外部公開の構造体にしたい場合)  
- (Ｂ) → `PrintInfo` (大文字開始: パッケージ外から呼べるメソッド)  
- (Ｃ) → `calcScore` (小文字開始: 内部でのみ使うメソッド)

最終形:

```go
type Student struct {
    Name  string
    Score int
}

func (s Student) PrintInfo() {
    fmt.Printf("Name=%s, Score=%d\n", s.Name, s.Score)
}

func (s *Student) calcScore() {
    s.Score += 10
}
```

---

### 1-4. 穴埋め問題: 関数の複数戻り値

#### 問題（再掲）
```go
func divide(a, b int) (Ｄ, Ｅ) {
    if b == 0 {
        return (Ｆ), errors.New("division by zero")
    }
    return a / b, nil
}
```

#### 解答

- (Ｄ) → `int`  
- (Ｅ) → `error`  
- (Ｆ) → `0`

完成形:
```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

---

## ミニテスト(2) — （インターフェースとジェネリクス）

### 2-1. 選択問題：インターフェース

#### 問題（再掲）
1. 「Go のインターフェースで暗黙の実装」とは何か  
   - (A) インターフェースを実装する際に“明示的な宣言不要”で、メソッドが一致すれば自動的に実装認定  
   - (B) インターフェース名と構造体名を一致させないといけない  
   - (C) Go では 1 つの型は複数のインターフェースを実装できない  

2. 以下の型があったとき、`var r Reader` に代入できるのはどれか（複数選択可）。

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type MyFile struct {}
func (f MyFile) Read(p []byte) (n int, err error) { return 0, nil }

type Writer interface {
    Write(p []byte) (n int, err error)
}

type MyBuffer struct {}
func (b MyBuffer) Write(p []byte) (n int, err error) { return 0, nil }
```

- (A) `MyFile`
- (B) `MyBuffer`
- (C) `Writer`
- (D) `Reader`

#### 解答

1. **答え**: (A)  
   - 暗黙の実装 = 型がインターフェースが要求するメソッドをすべて持っているかどうかをコンパイラが見て、自動的に implements とみなす仕組み。  
2. **答え**: (A) だけ  
   - `MyFile` は `Read` を実装 → `Reader` に代入可  
   - `MyBuffer` は `Write` しか持たないので `Reader` としては不可  
   - (C)(D) は型でなくインターフェース名

---

### 2-2. 選択問題：ジェネリクス

#### 問題（再掲）
1. 以下の関数がコンパイルエラーになる理由は？  
   ```go
   func max[T any](x, y T) T {
       if x > y {
           return x
       }
       return y
   }
   ```
   - (A) Go では複数戻り値の形 `(T, error)` にしないといけない  
   - (B) `>` 演算子を使う型であることを指定していないため  
   - (C) `any` は旧 `interface{}` と同じなので、エラーにはならない  

2. 「constraints.Ordered」とは何か  
   - (A) 比較演算子が使える型をまとめた制約  
   - (B) Go のビルド時にファイルを並び替える仕組み  
   - (C) すべてのジェネリクス関数に必須の宣言  

#### 解答

1. **答え**: (B)  
   - `any` では `>` 演算子が保証されないため、コンパイラがエラーを出す。  
2. **答え**: (A)  
   - `constraints.Ordered` は、整数・浮動小数点・文字列など “大小比較演算ができる型” をまとめた型制約。

---

### 2-3. 穴埋め問題：インターフェース＋ジェネリクス

#### 問題（再掲）
```go
type Comparable interface {
    (Ｇ)(other any) bool
}

func maxC[T (Ｈ)](x, y T) T {
    if x.(Ｇ)(y) {
        return x
    }
    return y
}
```

#### 解答

- (Ｇ) → `IsGreaterThan`（例）  
- (Ｈ) → `Comparable`

完成形:
```go
type Comparable interface {
    IsGreaterThan(other any) bool
}

func maxC[T Comparable](x, y T) T {
    if x.IsGreaterThan(y) {
        return x
    }
    return y
}
```

---

### 2-4. 穴埋め問題：ジェネリック Filter

#### 問題（再掲）
```go
func Filter[(Ｊ)](arr []T, pred func(T) bool) []T {
    var result []T
    for _, v := range arr {
        if (Ｋ)(v) {
            result = append(result, v)
        }
    }
    return result
}
```

#### 解答

- (Ｊ) → `T any`  
- (Ｋ) → `pred`

最終形:
```go
func Filter[T any](arr []T, pred func(T) bool) []T {
    var result []T
    for _, v := range arr {
        if pred(v) {
            result = append(result, v)
        }
    }
    return result
}
```

---
