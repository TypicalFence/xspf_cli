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
    playlist.trackList.append(Track(location=track))
    util.save_playlist(playlist, playlist_path)



