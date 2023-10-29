# Make Playlist With...

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要
音楽 × Tech  
曲のテンポやデータ分析によるクラスタリングを通して新たなプレイリストを作成するwebアプリケーション
### 背景(製品開発のきっかけ、課題等）
大学に行くまでの通学路で基本的に音楽を聴くことが多いのですが、自分の歩調、テンポに合った曲のプレイリストがほしいなと感じました。しかし、お気に入りの曲やプレイリストから曲のテンポを調べて一々新しいプレイリストに追加していくという作業があまりにも面倒だなと思い、またSpotify APIで曲のデータを取ることができると知り、自動的にプレイリストを作成するアプリケーションがあれば、面白そうだなと感じたことがきっかけです。
#### 
### 製品説明（具体的な製品の説明）
### 特長
#### 1. 特長1
#### 2. 特長2
#### 3. 特長3

### 解決出来ること
### 今後の展望
クラスタリング結果の可視化や、クラスター数を自由に変更できるようにしたり、他のIoTデバイスと連携してウォーキングやドライブといった場面に対して、最適なプレイリストや曲を選定してくれるようにしたいと考えています。
### 注力したこと（こだわり等）
* 
* 

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
