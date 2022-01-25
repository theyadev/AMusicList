from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
from os import getenv

from main.models import Song, Staff

load_dotenv()

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getenv("SPOTIFY_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = Spotify(client_credentials_manager=client_credentials_manager)


def importAlbumsFromPlaylist(playlist_id="5S8SJdl1BDc0ugpkEvFsIL"):
    playlist = sp.playlist(playlist_id)
    for track in playlist["tracks"]["items"]:
        importTracksFromAlbum(track["track"]["album"]["id"])


def importTracksFromAlbum(album_id):
    album = sp.album(album_id)

    album_name = album["name"]
    album_release = album["release_date"]
    album_image = album["images"][0]["url"]

    album_tracks = sp.album_tracks(album_id)

    for track in album_tracks["items"]:
        length = track["duration_ms"] // 1000

        importTrack(
            title=track["name"],
            length=length,
            artist_dicts=track["artists"],
            image_url=album_image,
            release_date=album_release,
            album_name=album_name,
        )


def importTrack(title, length, artist_dicts, image_url, release_date, album_name):
    artists = []

    for artist in artist_dicts:
        try:
            artist = Staff.objects.get(name=artist["name"])
        except Staff.DoesNotExist:
            artist = importArtistFromDict(artist)

        artists.append(artist)

    try:
        song = Song.objects.get(title=title)
    except Song.DoesNotExist:
        song = Song()

    song.title = title
    song.imageUrl = image_url
    song.release_date = release_date
    song.albumName = album_name
    song.length = length

    song.save()

    print(song.title)

    for staff in artists:
        if not song.staffs.filter(pk=artist.pk).exists():
            song.staffs.add(staff)

    song.save()


def importArtistFromDict(artist_dict):
    id: str = artist_dict["id"]
    name: str = artist_dict["name"]
    spotify_link: str = artist_dict["external_urls"]["spotify"]

    artist_res = sp.artist(id)

    if artist_res["images"] != []:
        image: str = artist_res["images"][0]["url"]
    else:
        image = ""

    newStaff = Staff(name=name, imageUrl=image, description=spotify_link)

    newStaff.save()

    return newStaff
