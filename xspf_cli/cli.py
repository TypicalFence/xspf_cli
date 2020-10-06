import sys
import os
import types
import click
from xspf_lib import Playlist, Track
import xspf_cli.util as util


@click.group()
@click.argument("playlist", type=click.Path(dir_okay=False))
@click.pass_context
def xspf(ctx, playlist):
    """A handy xspf cli."""
    ctx.ensure_object(types.SimpleNamespace)
    ctx.obj.playlist = playlist


@xspf.command()
@click.option('--title')
@click.option('--creator')
@click.option('--annotation')
@click.pass_context
def create(ctx, title, creator, annotation):
    """Creates a new playlist."""
    playlist_path = ctx.obj.playlist

    if os.path.isfile(playlist_path):
        print("playlist \"{}\" already exists".format(playlist_path))
        sys.exit(1)

    playlist = Playlist(title=title, creator=creator, annotation=annotation)

    util.save_playlist(playlist, playlist_path)


@xspf.command()
@click.argument("track", type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def add(ctx, track):
    """add a track to a playlist."""
    playlist_path = ctx.obj.playlist

    util.ensure_playlist_exists(playlist_path)

    playlist = Playlist.parse(playlist_path)
    track = util.get_track_from_file(track)

    if track is None:
        print("can't add track: invalid file")
        sys.exit(1)

    playlist.trackList.append(track)
    util.save_playlist(playlist, playlist_path)


@xspf.command()
@click.argument("track_number", type=click.INT)
@click.pass_context
def remove(ctx, track_number):
    """Removes a track from a playlist."""
    playlist_path = ctx.obj.playlist

    util.ensure_playlist_exists(playlist_path)

    playlist = Playlist.parse(playlist_path)

    if len(playlist.trackList) >= track_number - 1:
        del playlist.trackList[track_number - 1]
    else:
        sys.exit(1)

    util.save_playlist(playlist, playlist_path)

@xspf.command()
@click.pass_context
def update_metadata(ctx):
    """Updates the meta data of the tracks based on tags of the files."""
    playlist_path = ctx.obj.playlist

    util.ensure_playlist_exists(playlist_path)

    playlist = Playlist.parse(playlist_path)
    playlist.trackList = list(map(util.update_metadata, playlist.trackList))

    util.save_playlist(playlist, playlist_path)


@xspf.command()
@click.pass_context
def show(ctx):
    """Displays the playlist."""
    playlist_path = ctx.obj.playlist

    util.ensure_playlist_exists(playlist_path)

    playlist = Playlist.parse(playlist_path)

    for idx, track in enumerate(playlist.trackList):
        print("[{}]\t{} - {}".format(
            idx + 1, track.creator, track.title))

