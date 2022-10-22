from distutils.log import error
import os
from time import process_time_ns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

load_dotenv()

CLIENT_ID = os.environ.get('AUTH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('AUTH_CLIENT_SECRET')
SCOPES="app-remote-control,playlist-read-private,streaming,user-read-playback-state,user-modify-playback-state,user-read-currently-playing"

TARGET_DEVICE_NAME = os.environ.get('TARGET_DEVICE_NAME')
TARGET_PLAYLIST_NAME = os.environ.get('TARGET_PLAYLIST_NAME')

PLAYBACK_VOLUME = os.environ.get("PLAYBACK_VOLUME")
if(PLAYBACK_VOLUME == None):
    PLAYBACK_VOLUME = 20
else:
    PLAYBACK_VOLUME = int(PLAYBACK_VOLUME)

print("""
 _____             _   _  __            ___  _                      
/  ___|           | | (_)/ _|          / _ \| |                     
\ `--. _ __   ___ | |_ _| |_ _   _    / /_\ | | __ _ _ __ _ __ ___  
 `--. | '_ \ / _ \| __| |  _| | | |   |  _  | |/ _` | '__| '_ ` _ \ 
/\__/ | |_) | (_) | |_| | | | |_| |   | | | | | (_| | |  | | | | | |
\____/| .__/ \___/ \__|_|_|  \__, |   \_| |_|_|\__,_|_|  |_| |_| |_|
      | |                     __/ |                                 
      |_|                    |___/                                  
                                                          by blaczko

""")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://127.0.0.1:9090",
                                               scope=SCOPES))

print("Devices")
playback_device = None
devices = sp.devices()
for item in devices["devices"]:
    if(item['name'] == TARGET_DEVICE_NAME):
        playback_device = item
    print(f"- {item['name']}")
print("")

print("Playlists")
playback_playlist = None
playlists = sp.current_user_playlists()['items']
for item in playlists:
    if(item['name'] == TARGET_PLAYLIST_NAME):
        playback_playlist = item
    print(f"- {item['name']}")
print("")

if(TARGET_DEVICE_NAME == None or TARGET_PLAYLIST_NAME == None):
    print("Set the TARGET_DEVICE_NAME and TARGET_PLAYLIST_NAME env vars")
    exit()

if(playback_device == None):
    print(f"Failed to find device: [ {TARGET_DEVICE_NAME} ]")

if(playback_playlist == None):
    print(f"Failed to find playlist: [ {TARGET_PLAYLIST_NAME} ]")
    exit()

sp.shuffle(
    device_id=playback_device["id"],
    state=True
)

# volume control sometimes throws a SpotifyException, reason: VOLUME_CONTROL_DISALLOW
# sp.volume(
#     device_id=playback_device["id"],
#     volume_percent=PLAYBACK_VOLUME
# )

sp.start_playback(
    device_id=playback_device["id"],
    context_uri='spotify:playlist:' + playback_playlist["id"],
    offset={"position": random.randint(0, int(playback_playlist["tracks"]["total"]) - 1)}
)
