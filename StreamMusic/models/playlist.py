"""
models/playlist.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - A classe Playlist tem UMA responsabilidade: representar e gerenciar
     a coleção de músicas que compõe uma playlist
   - Não sabe nada sobre usuários, download ou recomendações
"""

from typing import List, Optional
from .music import Music


class Playlist:
    """
    Entidade de domínio: Playlist.
    Responsabilidade única: manter e expor uma lista ordenada de músicas.
    """

    def __init__(self, name: str, owner: str):
        self._name = name
        self._owner = owner
        self._tracks: List[Music] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def tracks(self) -> List[Music]:
        return list(self._tracks)  # retorna cópia — encapsulamento

    def add_track(self, music: Music) -> None:
        """Adiciona uma música se ela ainda não estiver na playlist."""
        if any(t.title == music.title for t in self._tracks):
            raise ValueError(f"'{music.title}' já está na playlist '{self._name}'.")
        self._tracks.append(music)

    def get_track(self, title: str) -> Optional[Music]:
        """Busca uma música pelo título."""
        for track in self._tracks:
            if track.title.lower() == title.lower():
                return track
        return None

    def total_duration(self) -> int:
        return sum(t.duration_seconds for t in self._tracks)

    def total_duration_formatted(self) -> str:
        total = self.total_duration()
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02d}:{seconds:02d}"

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "owner": self._owner,
            "tracks": [t.to_dict() for t in self._tracks],
            "total_duration": self.total_duration_formatted(),
        }
