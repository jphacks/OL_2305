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
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


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
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template('index.html')



@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

####################
@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    #####################
    make_playlist(spotify)
    
    return spotify.current_user_playlists()


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

#####################

@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))