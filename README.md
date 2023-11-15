# Make Playlist With...



https://github.com/jphacks/OL_2305/assets/41145723/b224f95f-6cab-486d-8de9-272e532ebc85


![1_3 1 1](https://github.com/jphacks/OL_2305/assets/41145723/d62c30f1-e5eb-47a7-bbb2-dc94f3267a42)
![2_3 1 2](https://github.com/jphacks/OL_2305/assets/41145723/2c37e092-3926-4f13-aade-062ea76c9d6a)
![3_3 2 1](https://github.com/jphacks/OL_2305/assets/41145723/ceeac70b-da78-43e5-84b0-f86f2852839f)
![4_3 2 2](https://github.com/jphacks/OL_2305/assets/41145723/b08a17fa-77d7-43c0-9989-656a3f6cb21c)
![5_3 2 3](https://github.com/jphacks/OL_2305/assets/41145723/6816acb7-d4c2-460e-84dd-7d2a8b3ba679)
![6_3 4 1](https://github.com/jphacks/OL_2305/assets/41145723/6f8f558e-a4db-4d86-b861-7ff8dd6e5cb6)


[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要
音楽 × Tech  
曲のテンポやデータ分析によるクラスタリングを通して新たなプレイリストを作成するwebアプリケーション
### 背景(製品開発のきっかけ、課題等）
大学に行くまでの通学路で基本的に音楽を聴くことが多いのですが、自分の歩調、テンポに合った曲のプレイリストがほしいなと感じました。しかし、お気に入りの曲やプレイリストから曲のテンポを調べて一々新しいプレイリストに追加していくという作業があまりにも面倒だなと思い、またSpotify APIで曲のデータを取ることができると知り、自動的にプレイリストを作成するアプリケーションがあれば、面白そうだなと感じたことがきっかけです。
#### 
### 製品説明（具体的な製品の説明）
### 特長
#### 1. 特長1　自分のアカウントでフォローしているプレイリストや、作成したプレイリストに入っている曲をBPM別に分類分けできます！
#### 2. 特長2　URLをテキストフォームに貼り付けるも可能で、それも分類分けすることができます！
#### 3. 特長3　BPMで分類分けしたプレイリストリズムが似ているため、ランニングやウォーキングに向いています！

### 解決出来ること
### 今後の展望
クラスタリング結果の可視化や、クラスター数を自由に変更できるようにしたり、他のIoTデバイスと連携してウォーキングやドライブといった場面に対して、最適なプレイリストや曲を選定してくれるようにしたいと考えています。また、ランダムな曲を抽出してBPM分け、クラスタリングして分類分けする機能も追加することで、新しい自分に合う曲を見つけられるようにもなると思います。
### 注力したこと（こだわり等）
* 分類わけしたいプレイリストを複数選択可能にしたことです!
* Spotifyのログイン機能を作成したことです！（作るのに時間が非常にかかりました）

## 開発技術
### 活用した技術
#### API・データ
* Spotify API

#### フレームワーク・ライブラリ・モジュール
* Flask
* scikit-learn
* umap

#### デバイス
* 
* 

### 独自技術
#### ハッカソンで開発した独自機能・技術
* クラスタリングを用いて曲の分類を行った
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。


## 使い方
#Windows 版

```
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:SPOTIPY_CLIENT_ID=insert_your_client_id_here
$env:SPOTIPY_CLIENT_SECRET=insert_your_cclient_secret_here
$env:SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080'
venv/bin/python app.py
```

または venv/bin/python app.py
venv\Scripts\python.exe app.py

#Mac/Linux 版

```
python -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
export SPOTIPY_CLIENT_ID=insert_your_client_id_here
export SPOTIPY_CLIENT_SECRET=insert_your_client_secret_here
export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080'
venv/bin/python app.py
```
