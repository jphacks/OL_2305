from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv(".env")

original_play_list = 'https://open.spotify.com/playlist/617F6ctM5ZbmaVeHs5IlWN?si=b1352e2d95194496'

# sys.path.append("../spotify")
# from ..createPlaylist import create_play_list
# from ..spotifyApi_module import getTempo

app = Flask(__name__)

app.secret_key = "nL3K31BeuP79mN"
app.config['SESSION_COOKIE_NAME'] = 'Im a Cookie'
TOKEN_INFO = "token_info"

# ARTIST = ""

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
  sp_oauth = create_spotify_oauth()
  auth_url = sp_oauth.get_authorize_url()
  # global ARTIST 
  # ARTIST = request.form['artist']
  return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
  sp_oauth = create_spotify_oauth()
  session.clear()
  code = request.args.get('code')
  print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
  print(code)
  print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
  # クッキーにトークンを保存
  token_info = sp_oauth.get_access_token(code)
  # token_info = sp_oauth.get_access_token()
  session[TOKEN_INFO] = token_info
  return redirect(url_for('loading', _external=True))

@app.route('/loading')
def loading():
  try:
    token_info = get_token()
  except:
    print("user not logged in")
    return redirect(url_for("/", _external=False))
  
  # 変数spotifyがトークンで認証したユーザの認証情報
  spotify = spotipy.Spotify(auth = token_info['access_token'])

  make_playlist(spotify)
  return render_template('success.html')
  
  # result = sp.search(q='artist:' + ARTIST, type='artist')


  # artist_list = []
  # name_list = []
  # for artist in result["artists"]["items"]:
  #   if artist["images"] == []:
  #     img = "img/empty.png"
  #   else:
  #     img = artist["images"][0]["url"]
    
  #   item = [artist["name"], img]
  #   artist_list.append(item)

  # return render_template("result.html",artist_list=artist_list)
  

def make_playlist(spotify):
  tracks = []
  ids = []

  username = spotify.me()["id"]
  print(username)
  
  # global original_play_list 
  
  original_play_list = 'https://open.spotify.com/playlist/617F6ctM5ZbmaVeHs5IlWN?si=b1352e2d95194496'

  
  
  
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
        

  def addBPM_Playlist(min_tempo, max_tempo, dur):

    removeSameID(ids)
            
    bpmDict = {}
    start = min_tempo
    end = max_tempo 
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

  set_playlist_tempo_track(original_play_list) # プレイリストを含めるか

  addBPM_Playlist(start, end, dur) # プレイリストの作成

  return 0

def get_token():
  token_info = session.get(TOKEN_INFO, None)
  if not token_info:
    raise "exception"
  now = int(time.time())

  #トークンの期限を確認して、失効している場合はリフレッシュトークンを使って新しいものを要求する
  is_expired = token_info['expires_at'] - now < 60
  if (is_expired):
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
  return token_info


# 認証用オブジェクト
def create_spotify_oauth():
  return SpotifyOAuth(
    client_id= os.environ.get("client_id"),
    client_secret= os.environ.get("client_secret"),
    redirect_uri=url_for('redirectPage', _external=True),
    scope="user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private"
  )


if __name__ == "__main__":
    app.run(debug=True)
