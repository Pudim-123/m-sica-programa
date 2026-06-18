"""
services/catalog_service.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - MusicCatalogService tem UMA responsabilidade: gerenciar o catálogo global de músicas
   - Não gerencia usuários, playlists ou recomendações

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Trabalha com a abstração Music (modelo de domínio), não com detalhes de persistência
"""

from typing import List, Optional
from models.music import Music


class MusicCatalogService:
    """
    Serviço responsável pelo catálogo de músicas disponíveis na plataforma.
    Responsabilidade única: CRUD de músicas no catálogo global.
    """

    def __init__(self):
        self._catalog: List[Music] = []
        self._populate_default_catalog()

    def _populate_default_catalog(self) -> None:
        """Pré-popula o catálogo com músicas de exemplo."""
        default_songs = [
            Music("Blinding Lights",      "The Weeknd",      "Pop",        200, plays=980),
            Music("Shape of You",         "Ed Sheeran",      "Pop",        234, plays=870),
            Music("Bohemian Rhapsody",    "Queen",           "Rock",       354, plays=760),
            Music("Smells Like Teen Spirit","Nirvana",       "Rock",       301, plays=640),
            Music("God's Plan",           "Drake",           "Hip-Hop",    198, plays=820),
            Music("HUMBLE.",              "Kendrick Lamar",  "Hip-Hop",    177, plays=710),
            Music("Levitating",           "Dua Lipa",        "Pop",        203, plays=690),
            Music("bad guy",              "Billie Eilish",   "Pop",        194, plays=750),
            Music("Hotel California",     "Eagles",          "Rock",       391, plays=580),
            Music("SICKO MODE",           "Travis Scott",    "Hip-Hop",    312, plays=620),
            Music("Watermelon Sugar",     "Harry Styles",    "Pop",        174, plays=540),
            Music("Lose Yourself",        "Eminem",          "Hip-Hop",    326, plays=670),
            Music("Back in Black",        "AC/DC",           "Rock",       255, plays=500),
            Music("As It Was",            "Harry Styles",    "Pop",        167, plays=890),
            Music("Industry Baby",        "Lil Nas X",       "Hip-Hop",    212, plays=730),
        ]
        self._catalog.extend(default_songs)

    def get_all(self) -> List[Music]:
        return list(self._catalog)

    def find_by_title(self, title: str) -> Optional[Music]:
        for music in self._catalog:
            if music.title.lower() == title.lower():
                return music
        return None

    def find_by_genre(self, genre: str) -> List[Music]:
        return [m for m in self._catalog if m.genre.lower() == genre.lower()]

    def add_music(self, music: Music) -> None:
        if self.find_by_title(music.title):
            raise ValueError(f"Música '{music.title}' já existe no catálogo.")
        self._catalog.append(music)

    def catalog_as_dicts(self) -> List[dict]:
        """Retorna catálogo como lista de dicts (útil para estratégias de recomendação)."""
        return [m.to_dict() | {"plays": m.plays} for m in self._catalog]
