#Windows 版

```
venv\Scripts\activate
pip install -r requirements.txt
$env:SPOTIPY_CLIENT_ID=insert_your_client_id_here
$env:SPOTIPY_CLIENT_SECRET=insert_your_cclient_secret_here
$env:SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080'
$env:FLASK_ENV='development'
$env:FLASK_APP='/path/to/spotipy/examples/app.py'
flask --app app --debug run --host=0.0.0.0 --port=8080
venv/bin/python app.py
```

#Mac/Linux 版

```
venv\Scripts\activate
pip install -r requirements.txt
export SPOTIPY_CLIENT_ID=insert_your_client_id_here
export SPOTIPY_CLIENT_SECRET=insert_your_client_secret_here
export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080'
export FLASK_ENV='development'
export FLASK_APP='/path/to/spotipy/examples/app.py'
flask --app app --debug run --host=0.0.0.0 --port=8080
venv/bin/python app.py
```
