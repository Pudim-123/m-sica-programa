"""
models/music.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - A classe Music tem UMA responsabilidade: representar os dados de uma música
   - Não processa, não reproduz, não salva — apenas armazena informações
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Music:
    """
    Entidade de domínio: Música.
    Responsabilidade única: guardar os atributos de uma música.
    """
    title: str
    artist: str
    genre: str
    duration_seconds: int
    plays: int = 0

    def duration_formatted(self) -> str:
        """Retorna duração no formato mm:ss — única lógica de apresentação permitida."""
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def increment_play(self) -> None:
        """Registra uma reprodução."""
        self.plays += 1

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "duration": self.duration_formatted(),
            "plays": self.plays,
        }
