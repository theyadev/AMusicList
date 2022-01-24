import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from main.models import Song, Staff
from datetime import datetime

cid = "d6a59bc79081474284e4114981b0bd14"
secret = "b18a56fe8b4840b0bda4b83a8d533fb5"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def importAlbumsFromPlaylist(playlist_id = "5S8SJdl1BDc0ugpkEvFsIL"):
    playlist = sp.playlist(playlist_id)
    for track in playlist['tracks']['items']:
        importTracksFromAlbum(track['track']['album']['id'])

def importTracksFromAlbum(album_id):
    album = sp.album(album_id)

    album_name = album['name']
    album_release = album['release_date']
    album_image = album['images'][0]['url']

    album_tracks = sp.album_tracks(album_id)


    for track in album_tracks['items']:
        song_name = track['name']
        length = track['duration_ms'] // 1000

        artists = []

        for artist in track['artists']:
            name: str = artist['name']

            myStaff = Staff.objects.filter(name=name)
            
            if len(myStaff) > 0: 
                artist = myStaff[0]
            else:
                artist = importArtistFromDict(artist)

            artists.append(artist)

        song = Song.objects.filter(title=song_name)

        if len(song) == 0:
            song = Song()
        else:
            song = song[0]

        song.title = song_name
        song.imageUrl = album_image
        song.release_date = album_release
        song.album_name = album_name
        song.length = length

        song.save()

        for staff in artists:
            print(song)
            if not song.staffs.filter(pk=artist.pk).exists():
                song.staffs.add(staff)

        song.save()

def importArtistFromDict(artist_dict):
    id: str = artist_dict["id"]
    name: str = artist_dict['name']
    spotify_link: str = artist_dict['external_urls']['spotify']
    
    artist_res = sp.artist(id)

    if artist_res['images'] != []: image: str = artist_res['images'][0]['url']
    else: image = ""

    description = f"{spotify_link}"

    newStaff = Staff(name=name, imageUrl=image, description=description)

    newStaff.save()

    return newStaff

importAlbumsFromPlaylist("68agWSb6PQPIe8DUk0LNIP")