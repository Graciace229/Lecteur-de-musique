import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur de Musique")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")
        
        # Initialiser pygame mixer
        pygame.mixer.init()
        
        # Variables
        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        pygame.mixer.music.set_volume(self.volume)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre de l'application
        title = tk.Label(main_frame, text="🎵 Mon Lecteur Audio", 
                        font=("Arial", 24, "bold"),
                        bg="#1e1e2e", fg="#cdd6f4")
        title.pack(pady=(0, 20))
        
        # Info du morceau en cours
        self.song_info = tk.Label(main_frame, text="Aucun morceau sélectionné",
                                 font=("Arial", 14),
                                 bg="#313244", fg="#cdd6f4",
                                 pady=15, padx=20, relief=tk.RAISED)
        self.song_info.pack(fill=tk.X, pady=(0, 20))
        
        # Frame des contrôles
        controls_frame = tk.Frame(main_frame, bg="#1e1e2e")
        controls_frame.pack(pady=20)
        
        # Boutons de contrôle
        btn_style = {
            "font": ("Arial", 12),
            "bg": "#89b4fa",
            "fg": "white",
            "relief": tk.RAISED,
            "bd": 3,
            "width": 10,
            "cursor": "hand2"
        }
        
        self.prev_btn = tk.Button(controls_frame, text="⏮ Précédent",
                                  command=self.previous_song, **btn_style)
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = tk.Button(controls_frame, text="▶ Play",
                                  command=self.play_pause, **btn_style)
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.next_btn = tk.Button(controls_frame, text="⏭ Suivant",
                                  command=self.next_song, **btn_style)
        self.next_btn.grid(row=0, column=2, padx=5)
        
        self.stop_btn = tk.Button(controls_frame, text="⏹ Stop",
                                  command=self.stop, **btn_style)
        self.stop_btn.grid(row=0, column=3, padx=5)
        
        # Volume
        volume_frame = tk.Frame(main_frame, bg="#1e1e2e")
        volume_frame.pack(pady=20)
        
        tk.Label(volume_frame, text="🔊 Volume:", 
                font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack(side=tk.LEFT, padx=5)
        
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100,
                                      orient=tk.HORIZONTAL, command=self.change_volume,
                                      bg="#313244", fg="#cdd6f4",
                                      highlightthickness=0, length=200)
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT)
        
        # Frame de la playlist
        playlist_frame = tk.Frame(main_frame, bg="#1e1e2e")
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        tk.Label(playlist_frame, text="📋 Playlist", 
                font=("Arial", 14, "bold"),
                bg="#1e1e2e", fg="#cdd6f4").pack(anchor=tk.W)
        
        # Listbox avec scrollbar
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_box = tk.Listbox(playlist_frame, 
                                       yscrollcommand=scrollbar.set,
                                       bg="#313244", fg="#cdd6f4",
                                       selectbackground="#89b4fa",
                                       font=("Arial", 11),
                                       height=10)
        self.playlist_box.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_box.yview)
        
        self.playlist_box.bind('<Double-Button-1>', lambda e: self.play_selected())
        
        # Boutons de gestion de playlist
        playlist_btn_frame = tk.Frame(main_frame, bg="#1e1e2e")
        playlist_btn_frame.pack(pady=10)
        
        add_btn = tk.Button(playlist_btn_frame, text="➕ Ajouter fichiers",
                           command=self.add_songs, **btn_style)
        add_btn.grid(row=0, column=0, padx=5)
        
        remove_btn = tk.Button(playlist_btn_frame, text="➖ Supprimer",
                              command=self.remove_song, **btn_style)
        remove_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = tk.Button(playlist_btn_frame, text="🗑 Vider playlist",
                             command=self.clear_playlist, **btn_style)
        clear_btn.grid(row=0, column=2, padx=5)
    
    def add_songs(self):
        files = filedialog.askopenfilenames(
            title="Sélectionner des fichiers audio",
            filetypes=(("Fichiers audio", "*.mp3 *.wav *.ogg"), ("Tous", "*.*"))
        )
        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))
    
    def remove_song(self):
        try:
            selected = self.playlist_box.curselection()[0]
            self.playlist_box.delete(selected)
            del self.playlist[selected]
            if selected == self.current_index:
                self.stop()
        except:
            pass
    
    def clear_playlist(self):
        self.playlist_box.delete(0, tk.END)
        self.playlist.clear()
        self.stop()
    
    def play_selected(self):
        try:
            selected = self.playlist_box.curselection()[0]
            self.current_index = selected
            self.play_song()
        except:
            pass
    
    def play_song(self):
        if self.current_index >= 0 and self.current_index < len(self.playlist):
            song_path = self.playlist[self.current_index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.play_btn.config(text="⏸ Pause")
            
            # Mettre à jour l'info du morceau
            try:
                audio = MP3(song_path)
                title = os.path.basename(song_path)
                try:
                    tags = ID3(song_path)
                    if 'TIT2' in tags:
                        title = str(tags['TIT2'])
                except:
                    pass
                self.song_info.config(text=f"♪ {title}")
            except:
                self.song_info.config(text=f"♪ {os.path.basename(song_path)}")
            
            # Sélectionner dans la playlist
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
    
    def play_pause(self):
        if not self.is_playing:
            if self.current_index == -1 and len(self.playlist) > 0:
                self.current_index = 0
            self.play_song()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.config(text="⏸ Pause")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(text="▶ Play")
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_btn.config(text="▶ Play")
        self.song_info.config(text="Aucun morceau sélectionné")
    
    def next_song(self):
        if len(self.playlist) > 0:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()
    
    def previous_song(self):
        if len(self.playlist) > 0:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()
    
    def change_volume(self, val):
        self.volume = float(val) / 100
        pygame.mixer.music.set_volume(self.volume)

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()