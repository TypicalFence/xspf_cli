import sys
import os

def save_playlist(playlist, path):
    """util function because Playlist.write is currently broken."""
    with open(path, "w") as f:
        f.write(playlist.xml_string())


def ensure_playlist_exists(playlist_path):
    if not os.path.isfile(playlist_path):
        print("playlist \"{}\" must exists".format(playlist_path))
        sys.exit(1)
