import os
import pygame
import random


class SoundManager:
    """
    Handles the game background music.

    Attributes:
    - music_folder (str): The path to the music folder.
    - tracks (list): A list of music tracks.
    - current_track (int): The index of the current track.

    Methods:
    - _load_music_tracks(): Load all music tracks from the music folder.
    - _setup_events(): Set up the end of track event handler.
    - start_music(): Start playing music from the first track.
    - handle_music_end(): Handle the end of a track by playing the next one.
    - stop_music(): Stop the currently playing music.
    """

    def __init__(self):
        pygame.mixer.init()
        self.music_folder = "game\music"
        self.tracks = self._load_music_tracks()
        self.current_track = 0
        self.playing = False
        self.remaining_tracks = []
        self._setup_events()


    def _load_music_tracks(self):
        """Load all music tracks from the music folder."""
        tracks = []
        if os.path.exists(self.music_folder):
            for file in os.listdir(self.music_folder):
                if file.lower().endswith('.mp3'):
                    track_path = os.path.join(self.music_folder, file)
                    tracks.append(track_path)
        return tracks


    def _setup_events(self):
        """Set up the end of track event handler."""
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)


    def start_music(self):
        """Start playing music from the first track."""
        if self.tracks:
            # Always start with the first track
            pygame.mixer.music.load(self.tracks[0])
            pygame.mixer.music.play()
            self.playing = True
            # Prepare the remaining tracks playlist (excluding first track)
            self.remaining_tracks = self.tracks[1:]
            random.shuffle(self.remaining_tracks)


    def handle_music_end(self):
        """Handle the end of a track by playing the next random track."""
        if not self.playing:
            return
        # If remaining_tracks is empty, refill it with all tracks except the first
        if not self.remaining_tracks:
            self.remaining_tracks = self.tracks[1:]
            random.shuffle(self.remaining_tracks)
        # Get the next track and remove it from remaining_tracks
        next_track = self.remaining_tracks.pop()
        pygame.mixer.music.load(next_track)
        pygame.mixer.music.play()


    def stop_music(self):
        """Stop the currently playing music."""
        self.playing = False
        pygame.mixer.music.stop()
