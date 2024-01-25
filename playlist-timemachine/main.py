import datetime as dt
from bs4 import BeautifulSoup
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

URL_BILLBOARD = "https://www.billboard.com/charts/hot-100/"
URL_SPOTIFY = ""

try:
    with open(".secret.json", "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)

SPOTIFY_CLIENT_ID = config_data["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config_data["SPOTIFY_CLIENT_SECRET"]


# date_input = input(
#    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date_input = "2023-12-12"
date = dt.datetime.strptime(date_input, "%Y-%m-%d")
print(date)

# Billboard part
url = f"{URL_BILLBOARD}{date_input}"
response = requests.get(url)

if response.status_code == 200:
    tracks = []
    artists = []
    html_text = response.text
    soup = BeautifulSoup(response.text, 'html.parser')

    songs_name = soup.select(selector="li h3.c-title")
    artists_name = soup.select(
        'li.o-chart-results-list__item span.c-label.a-no-trucate')

    for song in songs_name:
        tracks.append(song.get_text(strip=True))
    for artist in artists_name:
        artists.append(artist.get_text(strip=True))

    for track, artist in zip(tracks, artists):
        print(f"{track} - {artist}")

else:
    print(f"Failed to retrieve the page {
          url}. Status Code: {response.status_code}")


# Spotify part
auth_base = spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://example.com", scope="playlist-modify-private")
auth_base.get_access_token()
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials
    (client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


year = date.year
month = date.month
day = date.day

urls = []
track_ids = []

for track in tracks:
    print(track)
    index = tracks.index(track)
    artist = artists[index]
    results = spotify.search(q=f"{track}%2520{artist}")
    if "tracks" in results and "items" \
            in results["tracks"] and results["tracks"]["items"]:
        hit = results["tracks"]["items"][0]
        track_id = hit["uri"]
        track_ids.append(track_id)
        spotify_url = hit['external_urls']['spotify']
        urls.append(spotify_url)

print(track_ids)
print(urls)

user_id = spotify.current_user()["id"]
playlist = spotify.user_playlist_create(user=user_id,
                                        name=f"{date_input} Billboard 100", public=False)

result = spotify.user_playlist_add_tracks(
    user=user_id, playlist_id=playlist["id"], tracks=urls)
print(result)
