import os
import pygame
import random


FADE_MS = 1000


class SoundManager:
    """
    Handles the game background music.

    Attributes:
        music_folder (str): The path to the music folder
        tracks (List[str]): A list of music tracks
        current_track (int): The index of the current track
        playing (bool): Whether music is currently playing
        remaining_tracks (List[str]): Tracks yet to be played
        volume (float): Current volume level (0.0 to 1.0)

    Methods:
        start_music: Start playing music with optional fade-in
        handle_music_end: Handle the end of a track with optional fade-in
        set_volume: Set the music volume (0.0 to 1.0)
        pause: Pause the currently playing music
        resume: Resume the paused music
        stop_music: Stop the currently playing music with optional fade-out
    """

    def __init__(self, music_folder="game\music"):
        """Initialize the sound manager with optional custom music folder."""
        pygame.mixer.init()
        self.music_folder = music_folder
        self.tracks = []
        self.current_track = 0
        self.playing = False
        self.remaining_tracks = []
        self.volume = 1.0
        self.last_played_track = None
        self.play_count = {}
        self._load_music_tracks()
        self._setup_events()
        pygame.mixer.music.set_volume(self.volume)


    def _load_music_tracks(self):
        """Load all music tracks from the music folder."""
        if not os.path.exists(self.music_folder):
            raise FileNotFoundError(f"Music folder not found: {self.music_folder}")
        for file in os.listdir(self.music_folder):
            if file.lower().endswith('.mp3'):
                track_path = os.path.join(self.music_folder, file)
                if os.path.exists(track_path):
                    self.tracks.append(track_path)
                    self.play_count[track_path] = 0
        if not self.tracks:
            raise FileNotFoundError("No valid music tracks found")


    def _setup_events(self):
        """Set up the end of track event handler."""
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)


    def _reset_playlist(self):
        """Reset the playlist when all tracks have been played at least once."""
        self.remaining_tracks = [track for track in self.tracks if self.play_count[track] < 2]
        if not self.remaining_tracks:
            self.play_count = {track: 0 for track in self.tracks}
            self.remaining_tracks = self.tracks.copy()
        random.shuffle(self.remaining_tracks)
        # Ensure last played track isn't first in new playlist
        if self.last_played_track and self.remaining_tracks and self.remaining_tracks[0] == self.last_played_track:
            random.shuffle(self.remaining_tracks)


    def start_music(self, fade_ms=FADE_MS):
        """Start playing music with optional fade-in."""
        if not self.tracks:
            return
        try:
            first_track = self.tracks[0]
            pygame.mixer.music.load(first_track)
            pygame.mixer.music.play(fade_ms=fade_ms)
            self.playing = True
            self.last_played_track = first_track
            self.play_count[first_track] = 1
            self._reset_playlist()
        except pygame.error as e:
            print(f"Error playing music: {e}")
            self.playing = False


    def handle_music_end(self, fade_ms=FADE_MS):
        """Handle the end of a track with optional fade-in."""
        if not self.playing:
            return
        if not self.remaining_tracks:
            self._reset_playlist()
        try:
            next_track = self.remaining_tracks.pop()
            # Ensure we don't play the same track twice in a row
            while next_track == self.last_played_track and self.remaining_tracks:
                self.remaining_tracks.append(next_track)
                next_track = self.remaining_tracks.pop()

            pygame.mixer.music.load(next_track)
            pygame.mixer.music.play(fade_ms=fade_ms)
            self.last_played_track = next_track
            self.play_count[next_track] += 1
        except pygame.error as e:
            print(f"Error playing next track: {e}")
            self.playing = False


    def set_volume(self, volume):
        """Set the music volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)


    def pause(self):
        """Pause the currently playing music."""
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False


    def resume(self):
        """Resume the paused music."""
        if not self.playing:
            pygame.mixer.music.unpause()
            self.playing = True


    def stop_music(self, fade_ms=FADE_MS):
        """Stop the currently playing music with optional fade-out."""
        self.playing = False
        pygame.mixer.music.fadeout(fade_ms)


    def is_playing(self):
        """Check if music is currently playing."""
        return bool(pygame.mixer.music.get_busy())
