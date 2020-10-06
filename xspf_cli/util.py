import sys
import os
import copy
import mutagen
from xspf_lib import Track


def save_playlist(playlist, path):
    """util function because Playlist.write is currently broken."""
    data = playlist.xml_string()
    with open(path, "w") as f:
        f.write(data)


def ensure_playlist_exists(playlist_path):
    if not os.path.isfile(playlist_path):
        print("playlist \"{}\" must exists".format(playlist_path))
        sys.exit(1)


def _get_first(unsafe_list):
    if len(unsafe_list) > 0:
        return unsafe_list[0]

    return None


def get_track_from_file(file_path):
    meta_data = mutagen.File(file_path, easy=True)

    if meta_data is None:
        return None

    return Track(
        location=file_path,
        title=_get_first(meta_data["title"]),
        creator=_get_first(meta_data["artist"]),
        album=_get_first(meta_data["album"]),
    )


def update_metadata(track):
    file_path = _get_first(track.location)

    if file_path is None:
        return track

    meta_data = mutagen.File(file_path, easy=True)

    if meta_data is None:
        return track

    new_track = copy.copy(track)

    title = _get_first(meta_data["title"])
    creator = _get_first(meta_data["artist"])
    album = _get_first(meta_data["album"])

    new_track.title = title
    new_track.creator = creator
    new_track.album = album

    return new_track

