import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from main.models import Song, Staff
from datetime import datetime

cid = "d6a59bc79081474284e4114981b0bd14"
secret = "b18a56fe8b4840b0bda4b83a8d533fb5"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


playlist = sp.playlist("5S8SJdl1BDc0ugpkEvFsIL")

for track in playlist['tracks']['items']:
    song_name = track['track']['name']
    image = track['track']['album']['images'][0]['url']
    release_date = track["added_at"]

    artists = []


    for artist in track['track']['artists']:
        name: str = artist['name']

        myStaff = Staff.objects.filter(name=name)
        
        if len(myStaff) > 0: 
            artists.append(myStaff[0])
            continue
        
        id: str = artist["id"]
        spotify_link: str = artist['external_urls']['spotify']
        

        artist_res = sp.artist(id)

        if artist_res['images'] != []: image: str = artist_res['images'][0]['url']
        else: image = ""

        DESCRIPTION = f"{spotify_link}"

        newStaff = Staff(name= name, imageUrl=image, description=DESCRIPTION)

        newStaff.save()

        artists.append(newStaff)
        
    # newSong = Song(title=song_name, imageUrl=image, releaseDate=release_date, updatedDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    newSong = Song.objects.filter(title=song_name)[0]

    for staff in artists:
        newSong.staffs.add(staff)
    
    newSong.save()