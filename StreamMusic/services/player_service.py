"""
services/player_service.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - PlayerService tem UMA responsabilidade: simular a reprodução de músicas
   - Não gerencia playlists, downloads ou usuários

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Depende de MusicCatalogService (abstração de acesso ao catálogo)
   - Mantém o histórico de reprodução do usuário atual
"""

import time
from typing import List, Optional
from interfaces.abstractions import IPlayable
from services.catalog_service import MusicCatalogService
from models.music import Music


class PlayerService(IPlayable):
    """
    Serviço responsável pela reprodução de músicas.
    Implementa IPlayable (ISP: interface específica para reprodução).
    """

    def __init__(self, catalog_service: MusicCatalogService):
        # DIP: dependência injetada
        self._catalog = catalog_service
        self._history: List[str] = []          # histórico de títulos reproduzidos
        self._current_music: Optional[Music] = None

    def play_music(self, title: str) -> str:
        """Simula a reprodução de uma música."""
        music = self._catalog.find_by_title(title)
        if not music:
            return f"❌ Música '{title}' não encontrada no catálogo."

        self._current_music = music
        music.increment_play()
        self._history.append(title)

        return self._render_player(music)

    def _render_player(self, music: Music) -> str:
        """Monta a interface visual do player no terminal."""
        bar = "█" * 20 + "░" * 0
        lines = [
            "",
            "  ┌─────────────────────────────────────┐",
            f"  │  ♪  Tocando agora                   │",
            f"  │  {music.title:<35} │",
            f"  │  {music.artist:<35} │",
            f"  │  Gênero: {music.genre:<27} │",
            f"  │  Duração: {music.duration_formatted():<26} │",
            f"  │  [{bar}] {music.duration_formatted()} │",
            "  └─────────────────────────────────────┘",
        ]
        return "\n".join(lines)

    def play(self) -> str:
        """Implementação de IPlayable: reproduz a música atual."""
        if self._current_music:
            return self._render_player(self._current_music)
        return "❌ Nenhuma música selecionada."

    def get_history(self) -> List[str]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()
