"""
interfaces/abstractions.py

Princípio aplicado: Interface Segregation Principle (ISP)
   - Interfaces pequenas e específicas ao invés de uma interface "God"
   - Cada interface define um contrato mínimo e coeso

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Módulos de alto nível dependem dessas abstrações, não de implementações concretas
"""

from abc import ABC, abstractmethod
from typing import List


# ISP: Interface específica para reprodução de mídia
class IPlayable(ABC):
    """Contrato para qualquer coisa que possa ser reproduzida."""

    @abstractmethod
    def play(self) -> str:
        pass


# ISP: Interface específica para download
class IDownloadable(ABC):
    """Contrato para qualquer coisa que possa ser baixada offline."""

    @abstractmethod
    def download(self, music_title: str) -> str:
        pass


# ISP: Interface específica para gerenciamento de playlists
class IPlaylistManager(ABC):
    """Contrato para gerenciar playlists."""

    @abstractmethod
    def create_playlist(self, name: str) -> str:
        pass

    @abstractmethod
    def add_music_to_playlist(self, playlist_name: str, music_title: str) -> str:
        pass

    @abstractmethod
    def list_playlists(self) -> List[dict]:
        pass


# ISP: Interface específica para sistema de recomendação (Strategy)
class IRecommendationStrategy(ABC):
    """
    Contrato para estratégias de recomendação.

    Princípio aplicado: Open/Closed Principle (OCP)
       - Novas estratégias podem ser adicionadas sem alterar código existente
       - Basta implementar esta interface
    """

    @abstractmethod
    def recommend(self, music_catalog: List[dict], user_history: List[str]) -> List[dict]:
        pass

    @abstractmethod
    def strategy_name(self) -> str:
        pass


# ISP: Interface específica para autenticação de usuário
class IUser(ABC):
    """Contrato base para todos os tipos de usuário."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_account_type(self) -> str:
        pass

    @abstractmethod
    def can_download(self) -> bool:
        pass
