from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from dotenv import load_dotenv
from os import getenv

from songs.models import Song, Artist, Album

load_dotenv()

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getenv("SPOTIFY_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = Spotify(client_credentials_manager=client_credentials_manager)


def importAlbumsFromLoved():
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8080/",
            scope="user-library-read",
        )
    )

    for i in range(1, 21):
        results = sp.current_user_saved_tracks(limit=50, offset=50 * i - 50)
        for item in results["items"]:
            importTracksFromAlbum(item["track"]["album"]["id"])


def importAlbumsFromPlaylist(playlist_id: str = "5S8SJdl1BDc0ugpkEvFsIL"):
    """
    Import every track from every album present in the playlist

    keyword arguments:
    playlist_id - Spotify id of the playlist
    """

    playlist = sp.playlist(playlist_id)
    for track in playlist["tracks"]["items"]:
        importTracksFromAlbum(track["track"]["album"]["id"])


def importTracksFromAlbum(album_id: str):
    """
    Import every track from an album in the database

    keyword arguments:
    album_id - Spotify id of the album
    """

    album = sp.album(album_id)

    album_spotify_id = album["id"]
    album_name = album["name"]
    album_release = album["release_date"]
    album_image = album["images"][0]["url"]

    if Album.objects.filter(spotifyId=album_spotify_id).exists():
        albumModel = Album.objects.get(spotifyId=album_spotify_id)
    else:
        albumModel = Album()

    albumModel.name = album_name
    albumModel.releaseDate = album_release
    albumModel.spotifyId = album_spotify_id
    albumModel.imageUrl = album_image

    try:
        albumModel.save()
    except:
        return

    for artist in album["artists"]:
        try:
            artist = Artist.objects.get(spotifyId=artist["id"])
        except Artist.DoesNotExist:
            artist = importArtistFromDict(artist)

        albumModel.artists.add(artist)

    albumModel.save()

    album_tracks = sp.album_tracks(album_id)

    print(albumModel.name)

    for track in album_tracks["items"]:
        length = track["duration_ms"] // 1000

        if Song.objects.filter(spotifyId=track["id"]).exists():
            song = Song.objects.get(spotifyId=track["id"])
        else:
            song = importTrack(
                spotify_id=track["id"],
                title=track["name"],
                length=length,
                artist_dicts=track["artists"],
                image_url=album_image,
                release_date=album_release,
                preview_url=track["preview_url"]
            )

        albumModel.songs.add(song)

        albumModel.save()

def importAlbumFromTrack(track_id: str):
    track = sp.track(track_id)

    importTracksFromAlbum(track["album"]['id'])


def importTrack(
    spotify_id: str,
    title: str,
    length: int,
    artist_dicts: list[dict],
    image_url: str,
    release_date: str,
    preview_url: str
):
    """
    Import a track in the database.

    keyword arguments:
    title - Song title
    length - Song length in seconds
    artist_dicts - A list of artist dict from spotipy
    image_url - Url to the song/album cover
    release_date - Song release date
    album_name - Album where we can find the song
    """

    artists = []

    for artist in artist_dicts:
        try:
            artist = Artist.objects.get(spotifyId=artist["id"])
        except Artist.DoesNotExist:
            artist = importArtistFromDict(artist)

        artists.append(artist)

    try:
        song = Song.objects.get(spotifyId=spotify_id)
    except Song.DoesNotExist:
        song = Song()

    song.spotifyId = spotify_id
    song.title = title
    song.imageUrl = image_url
    song.release_date = release_date
    song.length = length
    song.previewUrl = preview_url

    song.save()

    for artist in artists:
        if not song.artists.filter(pk=artist.pk).exists():
            song.artists.add(artist)

    song.save()

    return song


def importArtistFromDict(artist_dict: dict):
    """
    Import an artist in the database based on a dict

    keyword arguments:
    artist_dict - An artist from spotipy
    """

    id: str = artist_dict["id"]
    name: str = artist_dict["name"]
    spotify_link: str = artist_dict["external_urls"]["spotify"]

    artist_res = sp.artist(id)

    if artist_res["images"] != []:
        image: str = artist_res["images"][0]["url"]
    else:
        image = ""

    newArtist = Artist(
        spotifyId=id, name=name, imageUrl=image, description=spotify_link
    )

    newArtist.save()

    return newArtist
