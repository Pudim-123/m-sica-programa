"""
services/playlist_service.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - PlaylistService tem UMA responsabilidade: gerenciar playlists dos usuários

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Depende da abstração MusicCatalogService e da interface IPlaylistManager
   - Não sabe como as músicas são armazenadas fisicamente

Princípio aplicado: Composição
   - PlaylistService É COMPOSTO de MusicCatalogService (tem-um, não é-um)
"""

from typing import List, Optional
from interfaces.abstractions import IPlaylistManager
from models.playlist import Playlist
from models.music import Music
from services.catalog_service import MusicCatalogService


class PlaylistService(IPlaylistManager):
    """
    Serviço responsável pela criação e gestão de playlists.

    Composição: PlaylistService usa MusicCatalogService internamente
                (exemplo de composição sobre herança).
    """

    def __init__(self, catalog_service: MusicCatalogService):
        # DIP: recebe a dependência injetada, não instancia diretamente
        # Composição: PlaylistService TEM UM MusicCatalogService
        self._catalog: MusicCatalogService = catalog_service
        self._playlists: List[Playlist] = []

    def create_playlist(self, name: str, owner: str = "Usuário") -> str:
        """Cria uma nova playlist se o nome não estiver em uso."""
        if self._find_playlist(name):
            return f"❌ Já existe uma playlist chamada '{name}'."
        playlist = Playlist(name=name, owner=owner)
        self._playlists.append(playlist)
        return f"✅ Playlist '{name}' criada com sucesso!"

    # Implementação de IPlaylistManager
    def add_music_to_playlist(self, playlist_name: str, music_title: str) -> str:
        """Busca a música no catálogo e a adiciona à playlist."""
        playlist = self._find_playlist(playlist_name)
        if not playlist:
            return f"❌ Playlist '{playlist_name}' não encontrada."

        music = self._catalog.find_by_title(music_title)
        if not music:
            return f"❌ Música '{music_title}' não encontrada no catálogo."

        try:
            playlist.add_track(music)
            return f"✅ '{music.title}' adicionada à playlist '{playlist_name}'."
        except ValueError as e:
            return f"❌ {e}"

    def list_playlists(self) -> List[dict]:
        return [p.to_dict() for p in self._playlists]

    def get_playlist(self, name: str) -> Optional[Playlist]:
        return self._find_playlist(name)

    def _find_playlist(self, name: str) -> Optional[Playlist]:
        for p in self._playlists:
            if p.name.lower() == name.lower():
                return p
        return None
