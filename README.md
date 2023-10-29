# サンプル（プロダクト名）

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要
### 音楽 × Tech 
### 曲のテンポやデータ分析によるクラスタリングを通して新たなプレイリストを作成する「Make Playlist With...」
### 背景(製品開発のきっかけ、課題等）
#### 
### 製品説明（具体的な製品の説明）
### 特長
#### 1. 特長1
#### 2. 特長2
#### 3. 特長3

### 解決出来ること
### 今後の展望
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
* matplotlib

#### デバイス
* 
* 

### 独自技術
#### ハッカソンで開発した独自機能・技術
* 独自で開発したものの内容をこちらに記載してください
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
* 
* 

###　使い方

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
