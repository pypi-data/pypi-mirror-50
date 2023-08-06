import os
import sys
import time
import vlc
import youtube_dl
from . import spotipy
from .spotipy import util
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from typing import Tuple


# Prints formatted logs to the console if debug is True
def log(msg: str, debug: bool = True) -> None:
    if debug:
        print("\033[92m>> " + msg + "\033[0m")


# Prints formatted errors to the console
def error(msg: str) -> None:
    print("\033[91m[ERROR]: " + msg + "\033[0m")
    sys.exit(1)


# VLC window playing the videos
class VLCWindow:
    def __init__(self, debug: bool = False, vlc_args: str = "",
            fullscreen: bool = False) -> None:
        self._debug = debug
        self._fullscreen = fullscreen

        # VLC Instance
        if self._debug: vlc_args += " --verbose 1"
        else: vlc_args += " --quiet"
        try:
            self._instance = vlc.Instance(vlc_args)
        except NameError:
            error("VLC is not installed")
        self.video_player = self._instance.media_player_new()

    # Plays/Pauses the VLC player
    def play(self) -> None:
        self.video_player.play()

    def pause(self) -> None:
        self.video_player.pause()

    def toggle_pause(self) -> None:
        if self.video_player.is_playing():
            self.pause()
        else:
            self.play()

    # Getting the video url with youtube-dl for VLC to play
    def get_url(self, name: str, ydl_opts: dict) -> str:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info("ytsearch:" + name, download=False)
        return info['entries'][0]['url']

    # Starts a new video on the VLC player
    def start_video(self, url: str) -> None:
        log("Starting video", self._debug)
        # Media instance
        Media = self._instance.media_new(url)
        self.video_player.set_media(Media)
        self.video_player.audio_set_mute(True)
        self.video_player.set_fullscreen(self._fullscreen)

    # Set the position of the VLC media playing
    def set_position(self, ms: int) -> None:
        self.video_player.set_time(ms)


# Dbus player with the Spotify properties (for Linux)
class DbusPlayer:
    def __init__(self, player: VLCWindow, debug: bool = False) -> None:
        # Configuring loop
        DBusGMainLoop(set_as_default=True)

        # Main player properties
        self.artist = ""
        self.title = ""
        self.is_playing = False
        self._debug = debug
        self.player = player

        # DBus internal properties
        self._session_bus = dbus.SessionBus()
        self._bus_name = "org.mpris.MediaPlayer2.spotify"
        self._disconnecting = False

        try:
            self._obj = self._session_bus.get_object(
                    self._bus_name,
                    '/org/mpris/MediaPlayer2')
        except dbus.exceptions.DBusException:
            error("No spotify session running")
        self._properties_interface = dbus.Interface(
                self._obj,
                dbus_interface="org.freedesktop.DBus.Properties")
        self._introspect_interface = dbus.Interface(
                self._obj,
                dbus_interface="org.freedesktop.DBus.Introspectable")
        self._media_interface = dbus.Interface(
                self._obj,
                dbus_interface='org.mpris.MediaPlayer2')
        self._player_interface = dbus.Interface(
                self._obj,
                dbus_interface='org.mpris.MediaPlayer2.Player')
        self._introspect = self._introspect_interface.get_dbus_method(
                'Introspect',
                dbus_interface=None)
        self._loop = GLib.MainLoop()
        self._signals = {}

        self.do_connect()
        self._refresh_metadata()

    # Proper disconnect when the program ends
    def __del__(self) -> None:
        self.do_disconnect()
    
    # Connects to the dbus signals
    def do_connect(self) -> None:
        log("Connecting", self._debug)
        if self._disconnecting is False:
            introspect_xml = self._introspect(self._bus_name, '/')
            if 'TrackMetadataChanged' in introspect_xml:
                self._signals['track_metadata_changed'] = self._session_bus.add_signal_receiver(
                        self._refresh_metadata,
                        'TrackMetadataChanged',
                        self._bus_name)
            self._properties_interface.connect_to_signal(
                    'PropertiesChanged',
                    self._on_properties_changed)

    # Disconnects from the dbus signals
    def do_disconnect(self) -> None:
        log("Disconnecting", self._debug)
        self._disconnecting = True
        for signal_name, signal_handler in list(self._signals.items()):
            signal_handler.remove()
            del self._signals[signal_name]

    # Waits for changes in dbus properties, exits with Ctrl+C
    def wait(self) -> None:
        log("Starting loop", self._debug)
        try:
            self._loop.run()
        except KeyboardInterrupt:
            log("Quitting main loop", self._debug)
            self._loop.quit()
            sys.exit(0)

    # Returns the artist and title out of a raw metadata object
    def _formatted_metadata(self, metadata: dict) -> Tuple[str,str]:
        return metadata['xesam:artist'][0], metadata['xesam:title']

    # Refreshes the metadata and status of the player (artist, title)
    def _refresh_metadata(self) -> None:
        _metadata = self._properties_interface.Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata"
        )
        try:
            self.artist, self.title = self._formatted_metadata(_metadata)
        except IndexError:
            error("No song currently playing")
            self.do_disconnect()

        _status = str(self._properties_interface.Get(
            'org.mpris.MediaPlayer2.Player',
            'PlaybackStatus')).lower()
        self.is_playing = self.bool_status(_status)

    # Consistency with the web API status variable and ease of use using booleans
    def bool_status(self, status: str) -> bool:
        if status == 'stopped' or status == 'paused':
            return False
        else:
            return True

    # Function called from dbus on property changes
    def _on_properties_changed(self, interface: dbus.String,
            properties: dbus.Dictionary, signature: dbus.Array) -> None:
        # If the song is different, break the loop
        if dbus.String('Metadata') in properties:
            _metadata = properties[dbus.String('Metadata')]
            _artist, _title = self._formatted_metadata(_metadata)
            if _artist != self.artist or _title != self.title:
                log("New video", self._debug)
                self._refresh_metadata()
                self._loop.quit()

        # The song was Paused/Played
        if dbus.String('PlaybackStatus') in properties:
            _status = str(properties[dbus.String('PlaybackStatus')]).lower()
            _status = self.bool_status(_status)
            if _status != self.is_playing:
                log("Paused/Played video", self._debug)
                self.is_playing = _status
                self.player.toggle_pause()


# Web player with the Spotify properties (other OS than Linux)
class WebPlayer:
    def __init__(self, player: VLCWindow, username: str, client_id: str,
            client_secret: str, redirect_uri: str, debug: bool = False) -> None:
        # Main player properties
        self.artist = ""
        self.title = ""
        self.position = 0
        self.is_playing = False
        self._debug = debug
        self.player = player

        # Checking that all parameters are passed
        if not username: error(
                "You must pass your username as an argument. "
                "Run `spotify-videos --help` for more info.")
        if not client_id: error(
                "You must pass your client ID as an argument. "
                "Run `spotify-videos --help` for more info.")
        if not client_secret: error(
                "You must pass your client secret as an argument. "
                "Run `spotify-videos --help` for more info.")

        # Creation of the Spotify token
        self._token = util.prompt_for_user_token(
                username,
                scope = 'user-read-currently-playing',
                client_id = client_id,
                client_secret = client_secret,
                redirect_uri = redirect_uri
        )
        if self._token:
            log("Authorized correctly", self._debug)
            self._spotify = spotipy.Spotify(auth = self._token)
        else:
            error("Can't get token for " + username)

        self._spotify.trace = False
        self._refresh_metadata()

    # Returns the artist, title and position from raw metadata
    def _formatted_metadata(self, metadata: dict) -> Tuple[str,str,int]:
        return metadata['item']['artists'][0]['name'], \
               metadata['item']['name'], \
               metadata['progress_ms']

    # Refreshes the metadata and status of the player (artist, title, position)
    def _refresh_metadata(self) -> None:
        try:
            _metadata = self._spotify.current_user_playing_track()
            self.artist, self.title, self.position = self._formatted_metadata(_metadata)
            self.is_playing = _metadata['is_playing']
        except TypeError:
            error("No spotify session running")

    # Returns the position in milliseconds of the player
    def get_position(self) -> int:
        self._refresh_metadata()
        return self.position

    # Waits until a new song is played, checking for changes every second
    def wait(self) -> None:
        try:
            while True:
                time.sleep(1)
                _artist = self.artist
                _title = self.title
                _is_playing = self.is_playing
                _position = self.position
                self._refresh_metadata()

                if self.is_playing != _is_playing:
                    log("Paused/Played video", self._debug)
                    self.player.toggle_pause()

                # Changes position if the difference is considered
                # enough to be a manual skip (>= 3secs, <0 secs)
                diff = self.position - _position
                if diff >= 3000 or diff < 0:
                    log("Position changed", self._debug)
                    self.player.set_position(self.position)

                if self.artist != _artist or self.title != _title:
                    log("Song changed", self._debug)
                    break
        except KeyboardInterrupt:
            log("Quitting from web player loop", self._debug)
            sys.exit(0)

