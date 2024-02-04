import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

URL_SPOTIFY = ""

SPOTIFY_CLIENT_ID = config_data["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config_data["SPOTIFY_CLIENT_SECRET"]


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
