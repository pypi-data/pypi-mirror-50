# deezloader

This project has been created to download songs, albums or playlists with Spotify or Deezer link from Deezer.

# Disclaimer

	- I am not responsible for the usage of this program by other people.
	- I do not recommend you doing this illegally or against Deezer's terms of service.
	- This project is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

* ### OS Supported ###
	![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
	![macOS Support](https://img.shields.io/badge/macOS-Support-brightgreen.svg)

* ### Installation ###
	pip3 install deezloader

### Initialize

```python
import deezloader

downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD", "YOUR ARL TOKEN DEEZER") #how get arl token https://www.youtube.com/watch?v=pWcG9T3WyYQ the video is not mine
```

### Download song

Download track by Spotify link

```python
downloa.download_trackspo(
	"Insert the Spotify link of the track to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=False,
	recursive_download=False
	interface=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
```

Download track by Deezer link
```python
downloa.download_trackdee(
	"Insert the Spotify link of the track to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=False,
	recursive_download=False
	interface=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
```

### Download album
Download album by Spotify link
```python
downloa.download_albumspo(
	"Insert the Spotify link of the album to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=True,
	recursive_download=True,
	interface=True,
	zips=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
#zips=True create a zip with all album songs
```

Download album from Deezer link
```python
downloa.download_albumdee(
	"Insert the Spotify link of the album to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=True,
	recursive_download=True,
	interface=True,
	zips=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
#zips=True create a zip with all album songs
```

### Download playlist

Download playlist by Spotify link
```python
downloa.download_playlistspo(
	"Insert the Spotify link of the album to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=True,
	recursive_download=True,
	interface=True,
	zips=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
#zips=True create a zip with all album songs
```

Download playlist from Deezer link
```python
downloa.download_playlistdee(
	"Insert the Spotify link of the album to download",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=True,
	recursive_download=True,
	interface=True,
	zips=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
#zips=True create a zip with all album songs
```

### Download name

Download by name
```python
downloa.download_name(
	artist="Eminem",
	song="Berzerk",
	output="SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality="MP3_320",
	recursive_quality=False,
	recursive_download=False,
	interface=True
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#interface=False if you want too see no download progress
```