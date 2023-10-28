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
