"""
Prerequisites

    pip3 install spotipy Flask Flask-Session

    // from your [app settings](https://developer.spotify.com/dashboard/applications)
    export SPOTIPY_CLIENT_ID=client_id
    export SPOTIPY_CLIENT_SECRET=client_secret
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
    // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
    OPTIONAL
    // in development environment for debug output
    export FLASK_ENV=development
    // so that you can invoke the app outside of the file's directory include
    export FLASK_APP=/path/to/spotipy/examples/app.py

    // on Windows, use `SET` instead of `export`

Run app.py

    python3 app.py OR python3 -m flask run
    NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
        (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)
"""

import os
from flask import Flask, request, render_template, session, redirect, url_for
from celery import Celery
from flask_session import Session
import spotipy
import time
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# import umap
import umap.umap_ as umap
#
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

# Celery configuration
# Local
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Render
# app.config['CELERY_BROKER_URL'] = 'redis://red-ckuj4bjamefc738qi0v0:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://red-ckuj4bjamefc738qi0v0:6379/0'


# session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('signin.html', auth_url=auth_url)

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    # return render_template('index.html') # ユーザのプレイリストの一覧 BPM or クラスタ　実行ボタン > # Loading.html > # Succseess.html
    playlistID =getUserPlaylistID(spotify)
    print(playlistID)
    return render_template('index.html',playlists=playlistID) 

@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

###################
class PlaylistTask:
    def __init__(self, auth_info, howto, playlists):
        self.auth_info = auth_info
        self.howto = howto
        self.playlists = playlists
####################
@app.route('/loading', methods=['POST'])
def playlists():
    URL = request.form['URL']
    list = request.form.getlist('check[]')
    if URL != "":
       playlists = [URL, * list]
    else:
       playlists = list
    howto = request.form['howto']


    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    # 同期
    # make_playlist_douki(spotify)
    # return render_template('success.html')

    # 非同期
    spotify_auth_info = auth_manager.get_access_token()
        
    make_playlist.delay(spotify_auth_info, howto, playlists)
    # task = PlaylistTask(spotify_auth_info, howto, playlists)
    # make_playlist.delay(task)

    return render_template('success.html')

def make_playlist_douki(spotify):
  tracks = []
  ids = []

  username = spotify.me()["id"]
  print(username)
  
  # global original_play_list 
  
  # original_play_list = 'https://open.spotify.com/playlist/617F6ctM5ZbmaVeHs5IlWN?si=b1352e2d95194496'

  
  
  
  def set_playlist_tempo_track(playlist):
    print('loading')
    results = spotify.playlist_tracks(playlist, limit=100)
    addTracks(results)
    
  def set_likedSong_tempo_track():
    print('loading liked songs')
    results = spotify.current_user_saved_tracks(limit=50)
    addTracks(results)
  
  def getTempo(track_url, spotify):
    return round(spotify.audio_features(track_url)[0]['tempo'])


  def create_play_list(list_name):
    list_data = spotify.user_playlists(user = username)
    #print(list_data['items'])
    flag = True
    for i in range(len(list_data['items'])):
        # print(list_data['items'][i]['name'])
        play_list_name = list_data['items'][i]['name']
        if play_list_name == list_name:
          flag = False
          # print(list_data['items'][i]['external_urls']['spotify'])
          url = list_data['items'][i]['external_urls']['spotify']
        else:
          pass
    if flag:
        spotify.user_playlist_create(username, name = list_name)
        list_data = spotify.user_playlists(user = username)
        url = list_data['items'][0]['external_urls']['spotify']
    return url
        
             
  def addTracks(results):
      
    ids.extend(results['items'])
      
    while results['next']:
      results = spotify.next(results)
      ids.extend(results['items'])
          
  def removeSameID(ids):
    for id in ids:
      if not id['track']['id'] in tracks:
        tracks.append(id['track']['id'])

    print('test')
    
  start = 70 # BPMのどこからプレイリストを作るか
  end = 200 # BPMのどこまでプレイリストを作るか
  dur = 10 # プレイリストの間隔
    
  # set_likedSong_tempo_track() # お気に入りの曲を含めるか

  # set_playlist_tempo_track(original_play_list) # プレイリストを含めるか

  addBPM_Playlist(start, end, dur, playlists) # プレイリストの作成

  return 0


@celery.task
def make_playlist_copy(auth_info):
   spotify = spotipy.Spotify(auth=auth_info['access_token'])
   username = spotify.me()["id"]
   print(username)
   print("made")
   return 0


@celery.task
def make_playlist(auth_info, howto, playlists):
  spotify = spotipy.Spotify(auth=auth_info['access_token'])
  tracks = []
  ids = []

  username = spotify.me()["id"]
  print(username)
  
  # global original_play_list 
  
  # original_play_list = 'https://open.spotify.com/playlist/617F6ctM5ZbmaVeHs5IlWN?si=b1352e2d95194496'

  
  
  
  def set_playlist_tempo_track(playlist):
    print('loading')
    results = spotify.playlist_tracks(playlist, limit=100)
    addTracks(results)
    
  def set_likedSong_tempo_track():
    print('loading liked songs')
    results = spotify.current_user_saved_tracks(limit=50)
    addTracks(results)
  
  def getTempo(track_url, spotify):
    return round(spotify.audio_features(track_url)[0]['tempo'])


  def create_play_list(list_name):
    list_data = spotify.user_playlists(user = username)
    #print(list_data['items'])
    flag = True
    for i in range(len(list_data['items'])):
        # print(list_data['items'][i]['name'])
        play_list_name = list_data['items'][i]['name']
        if play_list_name == list_name:
          flag = False
          # print(list_data['items'][i]['external_urls']['spotify'])
          url = list_data['items'][i]['external_urls']['spotify']
        else:
          pass
    if flag:
        spotify.user_playlist_create(username, name = list_name)
        list_data = spotify.user_playlists(user = username)
        url = list_data['items'][0]['external_urls']['spotify']
    return url
        
  
  def addBPM_Playlist(start, end, dur, playlists):
    def addTracks(results):
      ids.extend(results['items'])
      while results['next']:
          results = spotify.next(results)
          ids.extend(results['items'])
    def removeSameID(ids):
      for id in ids:
          if not id['track']['id'] in tracks:
              tracks.append(id['track']['id'])
    def set_playlist_track(playlist):
      results = spotify.playlist_tracks(playlist, limit=100)
      print('loading: ' + spotify.playlist(playlist)['name'])
      addTracks(results)
    for playlist in playlists:
        set_playlist_track(playlist)

    
    removeSameID(ids)

    removeSameID(ids)
            
    bpmDict = {}
    count = 0
        
    name = 'likedSongs_BPM0-' + str(start)
    print('making : BPM0-' + str(start))
    bpmDict[count] = [0, name]
    
    count += 1
    create_play_list(name)
    
    for tempo in range(start, end, dur):
      min_tempo = tempo 
      max_tempo = tempo + 10
      print('making : BPM'+str((min_tempo + 1)) + '-' + str(max_tempo))
      name = 'likedSongs_BPM' + str((min_tempo + 1)) + '-' + str(max_tempo)
      create_play_list(name)
      bpmDict[count] = [min_tempo, name]
      count += 1
          
    name = 'likedSongs_BPM' + str((end + 1)) + '-' 
    create_play_list(name)
    print('making : BPM' + str((end + 1)) + '-' )
    
    bpmDict[count] = [end, name]
    
    counter = 0
      
    for url in tracks:
      tempo = getTempo(url, spotify)
      
      for i in range(1, len(bpmDict.keys())):
          
        if bpmDict[i-1][0] < tempo <= bpmDict[i][0]:
          spotify.user_playlist_add_tracks(username, create_play_list(bpmDict[i-1][1]), [url])
          # print('add: '+ getArtists(url, spotify) + ' - ' + getTrack(url, spotify) + ' in ' + bpmDict[i-1][1])
          print(str(counter) + ' : ' + str(tempo) + ' in ' + bpmDict[i-1][1])
          break
        
        if i == len(bpmDict.keys())-1:
          spotify.user_playlist_add_tracks(username, create_play_list(bpmDict[i][1]), [url])
          # print('add: '+ getArtists(url, spotify) + ' - ' + getTrack(url, spotify) + ' in ' + bpmDict[i][1])
          print(str(counter) + ' : ' + str(tempo) + ' in ' + bpmDict[i-1][1])
        
      counter += 1
  ##################
  def addCLS_Playlist(playlists):
    def set_playlist_track(playlist):
      results = spotify.playlist_tracks(playlist, limit=100)
      print('loading: ' + spotify.playlist(playlist)['name'])
      addTracks(results)
    def addTracks(results):
      ids.extend(results['items'])
      while results['next']:
          results = spotify.next(results)
          ids.extend(results['items'])

    ##############
    def getTrackFeatures(id):
      meta = spotify.track(id)
      features = spotify.audio_features(id)
      name = meta['name']
      album = meta['album']['name']
      artist = meta['album']['artists'][0]['name']
      release_date = meta['album']['release_date']
      length = meta['duration_ms']
      popularity = meta['popularity']
      key = features[0]['key']
      mode = features[0]['mode']
      danceability = features[0]['danceability']
      acousticness = features[0]['acousticness']
      energy = features[0]['energy']
      instrumentalness = features[0]['instrumentalness']
      liveness = features[0]['liveness']
      loudness = features[0]['loudness']
      speechiness = features[0]['speechiness']
      tempo = features[0]['tempo']
      time_signature = features[0]['time_signature']
      valence = features[0]['valence']
      track = [name, album, artist, release_date, length, popularity, key, mode, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence, id]
      return track
    #############
    # set_likedSong_track()
    for playlist in playlists:
        set_playlist_track(playlist)
    removeSameID(ids)
    data = []
    for url in tracks:
        print(url)
        time.sleep(0.5)
        track = getTrackFeatures(url)
        data.append(track)
    df = pd.DataFrame(data, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'key', 'mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence', 'id'])
    df_features = df.drop(['name', 'album', 'artist', 'release_date', 'popularity', 'id', 'key', 'length', 'time_signature'], axis=1)
    # pprint(df_features)
    ss = preprocessing.StandardScaler()
    a_standardscaler = ss.fit_transform(df_features)
    a_ss = pd.DataFrame(a_standardscaler)
    a_ss = a_ss.set_axis(['mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness',  'speechiness', 'tempo', 'valence'], axis=1)
    # pprint(a_ss)
    fig = plt.figure()
    for i in range(2,11):
        kmeanModel = KMeans(n_clusters=i, random_state=42)
        kmeanModel.fit(a_standardscaler)
        clusters = kmeanModel.labels_
        # クラスターごとに何サンプルあるか
        for j in range(i):
            num = list(clusters).count(j)
            print(f'Cluster {j}: n = {num}')
        mapper = umap.UMAP(random_state=42)
        embedding = mapper.fit_transform(a_ss)
        plt.subplot(3, 3, i-1 )
        plt.scatter(embedding[:, 0], embedding[:, 1],
            c=clusters, cmap='Accent', alpha=0.7, s=5)
        plt.title('UMAP plot_cluster : ' + str(i))
    plt.show()
    k = 5
    kmeanModel = KMeans(n_clusters=k, random_state=42)
    kmeanModel.fit(a_standardscaler)
    clusters = kmeanModel.labels_
    df['cluster'] = clusters
    # pprint(df)
    for row in df.itertuples():
        for i in range(k):
            filename = 'clustering' + str(i+1) + ' in ' + str(k)
            create_play_list(filename)
            if row.cluster == i:
                spotify.user_playlist_add_tracks(username, create_play_list(filename), [row.id])
                print('add: ' + row.name + ' - ' + row.artist + ' in ' + filename)
                break

  ##################


  def addTracks(results):
      
    ids.extend(results['items'])
      
    while results['next']:
      results = spotify.next(results)
      ids.extend(results['items'])
          
  def removeSameID(ids):
    for id in ids:
      if not id['track']['id'] in tracks:
        tracks.append(id['track']['id'])

    print('test')
    
  start = 70 # BPMのどこからプレイリストを作るか
  end = 200 # BPMのどこまでプレイリストを作るか
  dur = 10 # プレイリストの間隔
    
  # set_likedSong_tempo_track() # お気に入りの曲を含めるか

  # set_playlist_tempo_track(original_play_list) # プレイリストを含めるか

  # addBPM_Playlist(start, end, dur, playlists) # プレイリストの作成

  match howto:
        case "BPM":
          addBPM_Playlist(start, end, dur, playlists) # プレイリストの作成
        case "CLS":
          addCLS_Playlist(playlists) # プレイリストの作成
        case _:
            return "Something's wrong with the internet"

  return 0

#CSSのキャッシュ対策
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
#名前、ジャケット、ID、が入っているリストを返す
def getUserPlaylistID(spotify):
    username = spotify.me()["id"]
    playlists = []
    playlistID = []
    result = spotify.user_playlists(username)
    playlists.extend(result['items'])
    while result['next']:
        result = spotify.next(result)
        playlists.extend(result['items'])
    for playlist in playlists:
        playlistID.append([playlist['name'], playlist['id']])
    return playlistID
#####################


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))