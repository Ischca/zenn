---
title: "第2章：スライスとマップを使いこなす"
free: true
---

# 第2章　スライスとマップを使いこなす

## 2.1 はじめに

前章では、Go 言語の基本構文・変数・定数などを学習し、簡単なコードを動かすところまで体験しました。  
しかし、プログラムが複雑になるにつれ、**可変長のリストや連想配列（キーと値）**を扱う場面が増えます。Go 言語にはそれぞれ**スライス (slice)** と **マップ (map)** という組込みのデータ構造が用意されており、大量のデータや柔軟なデータ管理を行う際に非常に便利です。

- **スライス (slice)**: 可変長配列のようなもの。`append` で要素追加が容易。  
- **マップ (map)**: 連想配列。`map[KeyType]ValueType` の形式で定義し、キーを使った探索や追加・削除をO(1)近い速度で行える。  

本章では、以下を重点的に解説します。

1. スライスと配列の違い  
2. スライスで柔軟に要素を追加・削除する仕組み (`append`, `len`, `cap` など)  
3. マップでキーと値を関連付けし、検索・更新する方法 (`m[key] = value`)  
4. 代表的なアルゴリズム例（合計・平均・最大値など）  
5. 章末に演習課題を明確な指示形で提示し、スライスとマップを組み合わせた小規模アプリを作る

さらに、**演習課題の前**に**紙面で回答できるミニテスト**を設けることで、学んだ内容の理解度を自己確認できるようにします。

---

## 2.2 配列とスライス

### 2.2.1 配列の基礎

#### 2.2.1.1 配列とは

Go 言語にも配列が存在しますが、**「要素数が固定」のコレクション**であり、実務ではあまり使われません。`[5]int` のように書くと要素数5個のint配列で、変更不可な長さを持ちます。

```go
var arr [5]int
arr[0] = 10
fmt.Println(arr[0]) // 10
fmt.Println(len(arr)) // 5
```

- 固定長ゆえに、可変サイズへの対応が難しい。  
- Go では「スライス」を実質的な可変配列として使うのが一般的。

---

### 2.2.2 スライスの生成と操作

#### 2.2.2.1 スライスとは

**スライス (slice)** は、可変長であり `append` を使って要素を自由に追加できる仕組みです。  
```go
var s []int
s = append(s, 10)
s = append(s, 20)
fmt.Println(s) // [10 20]
```

- `len(s)` は長さ、`cap(s)` は容量。容量が足りなくなると再アロケーションが起きる。

#### 2.2.2.2 スライスの作り方

1. **空スライス**:  
   ```go
   var s []int // nilのスライス
   // appendすれば普通に使える
   ```
2. **make**:  
   ```go
   s := make([]int, 3, 5) // len=3, cap=5
   ```
3. **リテラル**:  
   ```go
   s := []int{1,2,3}
   ```

#### 2.2.2.3 参照渡し

スライスは内部に「配列ポインタ＋長さ＋容量」の情報を持ち、関数に渡すとその参照を共有します。よって「別の関数内で書き換えたつもりが呼び出し元も変わる」ことが起こるので、意図がないなら新しくコピーを作るなど注意が必要。

```go
func changeFirst(arr []int) {
    arr[0] = 999
}
```

- この `arr` は引数としてコピーされるが、内部配列を共有する点にご注意。

---

### 2.2.3 サブスライス `s[a:b]`

`s[a:b]` は `s` の部分区間 `[a, b)` を抽出し、同じ内部配列を共有するサブスライスを返す。  
```go
s := []int{10,20,30,40,50}
sub := s[1:4] // 20,30,40
sub[0] = 999
fmt.Println(s)   // [10,999,30,40,50]
```
- `sub` は `s[1]`～`s[3]` の範囲を参照している。

---

## 2.3 マップ（連想配列）

### 2.3.1 基本構文

#### 2.3.1.1 マップの宣言

```go
var m map[string]int       // nilマップ
m = make(map[string]int)   // 初期化
m["Alice"] = 80
fmt.Println(m["Alice"]) // 80
```

- `map[KeyType]ValueType` の形でキー型と値型を指定。

#### 2.3.1.2 リテラル

```go
scores := map[string]int{
    "Alice": 80,
    "Bob":   90,
}
fmt.Println(scores["Bob"]) // 90
```

---

### 2.3.2 追加・更新・削除

```go
scores["Alice"] = 80 // 追加
scores["Alice"] = 85 // 上書き
delete(scores, "Alice") // 削除
```

- 調べる時: `value, ok := scores["Alice"]`  
  - ok=true ならキーあり、false ならキーなし。

### 2.3.3 順序が保証されない

マップはキーの順序を保持しない。もし順番に取り出したいなら、キーをスライスに集めてソートしてから取り回す必要がある。

```go
for k, v := range scores {
    // 順序は不定
}
```

### 2.3.4 nil マップに注意

```go
var phoneBook map[string]string
phoneBook["Alice"] = "111-222" // パニック
```
- `phoneBook` がnilのままだと書き込み不可。必ず `make(map[string]string)` やリテラル `{}` で初期化する。

---

## 2.4 代表的な操作例と簡易アルゴリズム

スライスやマップを使いこなすうえでよく出てくる**簡単な集計や検索のアルゴリズム**を確認します。

### 2.4.1 合計・平均・最大値（スライス）

- **合計**:
  ```go
  func sum(arr []int) int {
      total := 0
      for _, v := range arr {
          total += v
      }
      return total
  }
  ```
- **平均**:
  ```go
  func average(arr []int) float64 {
      if len(arr) == 0 {
          return 0
      }
      return float64(sum(arr)) / float64(len(arr))
  }
  ```
- **最大値**:
  ```go
  func max(arr []int) int {
      m := arr[0]
      for _, v := range arr {
          if v > m {
              m = v
          }
      }
      return m
  }
  ```

### 2.4.2 線形探索

```go
func findIndex(arr []int, target int) int {
    for i, v := range arr {
        if v == target {
            return i
        }
    }
    return -1
}
```
要素数Nに対してO(N)の探索。Nが大きいと時間がかかる点は注意。

---

## 2.5 ミニテスト — スライスとマップの復習

### 2.5.1 対象範囲

- **スライス**の基本 (`append`, `len`, `cap`, `nil`スライスなど)  
- **マップ**の基本 (`make(map[KeyType]ValueType)`, 追加・更新・削除、`nil`マップなど)  
- スライス/マップ特有の挙動（参照渡し、順序保証の有無 etc.）  

問題形式は大きく分けて**選択式**と**穴埋め式**を用意しています。

---

### 2.5.2 選択式問題

以下の文を読んで、最も正しい選択肢を1つ選んでください。

1. Go のスライスを宣言しただけ (`var s []int`) の状態はどうなるか？  
   - (A) 長さ3・容量3のスライスが生成される  
   - (B) `s` は nil のままなので、要素を追加するとエラーになる  
   - (C) `s` は nil のままだが、 `append` で要素を追加して使うことができる  

2. `append` を使ってスライスに要素を足す際、どのような動作が起きるか？  
   - (A) 要素数 (len) は増え、必要に応じて内部で容量 (cap) が再確保される  
   - (B) スライスの容量 (cap) は常に固定で変わらない  
   - (C) `append` は常に新しいスライスを返すわけではなく、場合によっては同じ配列を使うこともある  

*(ヒント: “常に”“必ず”という表現には注意しながら、Go のスライス挙動を思い出してください。)*

### 2.5.3 スライスの参照渡し

3. 関数にスライスを引数で渡すとき、以下のうち実際に起こることはどれか？  
   - (A) スライスは毎回丸ごとコピーされ、関数内で変更しても呼び出し元に影響はない  
   - (B) スライスは内部で同じ配列を参照するため、関数内でスライスの要素を変更すると呼び出し元にも反映される  
   - (C) 関数内からはスライスの要素にアクセスできない  

4. 下記コードで `sub` が参照している要素に何か変更を加えた場合、元の `nums` はどうなるか？  

   ```go
   nums := []int{10, 20, 30, 40, 50}
   sub  := nums[1:4] // 20, 30, 40
   ```
   - (A) sub は完全な独立コピーのため、nums とは無関係  
   - (B) sub は nums と同じ領域を共有しているため、変更すれば nums も変わる  
   - (C) コンパイルエラーが起きる  

### 2.5.4 マップの基礎

5. `var scores map[string]int` と書いただけの状態で、 `scores["Alice"] = 80` を行うとどうなるか？  
   - (A) "Alice" が80に登録される  
   - (B) パニック（runtime error）が起きる  
   - (C) 何も起きずに無視される  

6. 次のコードで、どのような出力が期待されるか？  
   ```go
   mymap := map[string]int {
       "X": 10,
       "Y": 20,
   }
   delete(mymap, "X")
   fmt.Println(mymap)
   ```
   - (A) 出力は `map[X:10 Y:20]`  
   - (B) 出力は `map[Y:20]`  
   - (C) 出力は `map[X:10]`  

### 2.5.5 マップの順序保証

7. マップを `for k, v := range mymap { ... }` で反復したときのキー順序はどうなるか？  
   - (A) 追加した順序を常に保持する  
   - (B) キーが文字列なら ASCII コード順に自動ソートされる  
   - (C) 順序は保証されないので、実行するたび異なる順序になる可能性がある  

---

## 2. 穴埋め式問題

ここでは**コード中に空欄**があり、それを埋める形でGo の文法や関数名を確認します。

### 2.5.6 スライスの操作

```go
func main() {
    var nums []int
    // ① numsに 10, 20, 30 を順に追加しよう
    nums = (A)(nums, 10)
    nums = (A)(nums, 20)
    nums = (A)(nums, 30)

    // ② nums の長さと容量を表示
    fmt.Println("len=", len(nums), "cap=", (B)(nums))
}
```

- (A) : スライスに要素を追加するときに使う標準ライブラリ関数の呼び出し (※引数や書き方に注意)  
- (B) : スライスの容量を取得するための標準ライブラリ関数

### 2.5.7 スライスから部分区間を取り出す

```go
func subSliceDemo() {
    data := []int{5,10,15,20,25,30}
    // 以下のコードで「10,15,20」を取り出して sub に入れたい
    // ただし data[? : ?] という形で空欄を埋めてください
    sub := data[(C):(D)]
    fmt.Println(sub)
}
```

- (C), (D) に適切な数字を入れて `[10,15,20]` を参照させる。  

### 2.5.8 マップへの書き込みと検索

```go
func mapDemo() {
    (E) := make(map[string]int)
    // ① "Alice" 80 を登録
    (E)["Alice"] = 80

    // ② "Bob" を検索し、見つからない場合はメッセージ表示
    score, ok := (E)["Bob"]
    if !ok {
        fmt.Println("Bob not found")
    } else {
        fmt.Println("Bob:", score)
    }
}
```

- (E) : 変数名`grades`など何でもよいが、「省略なし」で同じところを埋める（全部同じ地名を埋める形で）。  
- ヒント：ここでは「`grades := make(map[string]int)`」のように省略記法か「var grades map[string]int」として「grades = make(map[string]int)」か、いずれでもOKだが、行数を合わせるには短い書き方が自然。

---

## 2.6 章末課題

ミニテストが終わったら、実際に**コードを動かして**スライスやマップを使う経験を積みましょう。ここでは**断定的に明確な指示形**で課題を出します。読者は「指示どおりに関数やメイン関数を組み立てる」だけで完成するので、迷うことなく取り組めるはずです。

### 2.6.1 課題1：電話帳（マップ編）

#### 指示

1. **変数宣言**:  
   ```go
   var phoneBook map[string]string
   phoneBook = make(map[string]string) // nilを防ぐ
   ```
2. **関数**:  
   - `func AddEntry(book map[string]string, name, phone string)`  
     - `book[name] = phone` を実行して電話番号を登録する。  
   - `func DeleteEntry(book map[string]string, name string)`  
     - `delete(book, name)` で削除する。  
   - `func PrintPhone(book map[string]string, name string)`  
     - `phone, ok := book[name]` で検索し、ok==true なら番号表示、false なら「登録されていません」と表示。  
3. **メイン関数**:
   1. `phoneBook` を初期化  
   2. `AddEntry` を使って "Alice","111-2222" や "Bob","333-4444" を追加  
   3. `PrintPhone(phoneBook,"Alice")` を呼ぶ → 番号が表示される  
   4. `DeleteEntry(phoneBook,"Bob")` → "Bob" のデータが消える  
   5. `PrintPhone(phoneBook,"Bob")` → 「登録されていません」などを表示

#### 仕上がり

- 実行してみて、「Alice の番号が正しく出るか」「Bob を消したら削除されるか」を確認しよう。  
- 余力があれば、`PrintAll` 関数も追加し、全エントリを一覧表示してもよい。

---

### 2.6.2 課題2：スライス操作と「在庫管理」

#### 指示

1. **構造**: スライス（`[]string`) で「商品コード」を保持し、それに対応するマップ（`map[string]int`）で「在庫数」を管理する方式を取る。  
2. **変数宣言**:
   ```go
   var items []string
   var stock map[string]int
   stock = make(map[string]int)
   ```
3. **関数**:
   - `func AddItem(items []string, stock map[string]int, code string, qty int) ([]string, map[string]int)`  
     1. `items` に `code` が未登録なら `append` で追加  
     2. `stock[code] += qty` で在庫を加算  
     3. 新たな `items` と `stock` を返す（スライスは参照を返す方がいいが、明示的にリターンさせる形が分かりやすい）  
   - `func PrintStock(items []string, stock map[string]int)`  
     - `for _, code := range items` でループし、 `stock[code]` の数量を表示
4. **メイン関数**:
   1. `items, stock` を初期化  
   2. `items, stock = AddItem(items, stock, "A100", 10)`  
   3. `items, stock = AddItem(items, stock, "B200", 5)`  
   4. `PrintStock(items, stock)` → 各在庫が表示される  
   5. `items, stock = AddItem(items, stock, "A100", 3)` → A100が 13 個になるか確認  
   6. 再度 `PrintStock` し、更新された在庫を表示

#### 仕上がり

- 実行すると、「商品コード」と「在庫数」が表示され、**初回登録＋追加登録**が正常に動くのを確認する。  
- 追加機能として、「引数 `qty` がマイナスの場合は消費や返品扱いにする」と拡張しても面白い。

---

### 2.6.3 バグ入りコード演習

#### 指示

- **ファイル**: `buggy_map.go` というファイルに、下記のようなバグ入りコードがある。
  ```go
  package main

  import "fmt"

  func main() {
      var gradeMap map[string]int
      addGrade(gradeMap,"John",80)
      fmt.Println("John's grade:", gradeMap["John"])
  }

  func addGrade(m map[string]int, name string, grade int) {
      m[name] = grade
  }
  ```
  - **バグ**: `var gradeMap map[string]int` の状態で `nil` のまま書き込みしようとしてパニックが起こる。  
  - **修正**: `gradeMap = make(map[string]int)` のように初期化する

#### 完了条件

1. **パニックが起きず**、正常に "John's grade: 80" と表示される。  
2. 「nil マップに書き込みはできない」という根本原因を理解する。

---

## 2.7 まとめ

1. **スライス**: 可変長配列代わりに使う仕組みで、`append` で要素を追加可能。内部的には配列への参照・長さ・容量を持つため、参照渡しやサブスライスの性質に注意。  
2. **マップ**: 連想配列。`map[KeyType]ValueType` でキーと値を保管し、`m[key] = val` で追加・更新、`delete(m,key)` で削除。順序は保証されず、`nil`マップは書き込み不可。  
3. **簡易アルゴリズム**: 合計・平均・最大値などをスライスで計算する例、マップで検索やキー存在確認 (`_, ok := m[key]`) の例。  
4. **章末課題**: 指示を明確にした電話帳アプリ・在庫管理などを作り、**スライスとマップの使い方を総合的に復習**。さらに**バグ入り演習**で`nil`マップのパニックを修正する体験を積む。

このように**スライスとマップ**を習得すれば、Go でのデータ操作が飛躍的にやりやすくなります。次の章(第3章)で学ぶ**関数・構造体・メソッド**などの概念と組み合わせれば、複雑なデータをきちんと整理し、わかりやすいプログラムを短い期間で書けるようになるでしょう。ぜひ**ミニテスト**や**課題**を通じて、手を動かして理解を深めてみてください。