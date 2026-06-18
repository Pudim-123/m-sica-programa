"""
services/download_service.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - DownloadService tem UMA responsabilidade: gerenciar downloads offline

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Recebe IUser (abstração) — não importa se é Free ou Premium

Princípio aplicado: Liskov Substitution Principle (LSP)
   - O serviço usa IUser.can_download() para verificar permissão
   - Funciona com qualquer implementação de IUser (Free ou Premium)
   - PremiumUser substitui FreeUser sem quebrar esta lógica
"""

from typing import List
from interfaces.abstractions import IDownloadable, IUser
from services.catalog_service import MusicCatalogService


class DownloadService(IDownloadable):
    """
    Serviço responsável pelo download de músicas offline.
    Implementa IDownloadable (ISP: interface específica para download).

    LSP: opera sobre IUser — aceita Free e Premium transparentemente.
         A lógica de permissão está encapsulada em IUser.can_download().
    """

    def __init__(self, catalog_service: MusicCatalogService):
        # DIP: dependência injetada via construtor
        self._catalog = catalog_service
        self._downloaded: List[str] = []  # simula biblioteca offline

    def download(self, music_title: str, user: IUser) -> str:
        """
        Realiza o download se o usuário tiver permissão.

        LSP em ação: 'user' pode ser FreeUser ou PremiumUser —
        o código não precisa saber qual é; apenas chama can_download().
        """
        # LSP: polimorfismo — a verificação funciona para qualquer IUser
        if not user.can_download():
            return (
                f"❌ Download negado para {user.get_name()}.\n"
                f"   Conta {user.get_account_type()} não inclui downloads offline.\n"
                f"   ➜  Faça upgrade para Premium para desbloquear este recurso!"
            )

        music = self._catalog.find_by_title(music_title)
        if not music:
            return f"❌ Música '{music_title}' não encontrada no catálogo."

        if music_title in self._downloaded:
            return f"ℹ️  '{music_title}' já está na sua biblioteca offline."

        self._downloaded.append(music_title)
        return (
            f"✅ Download concluído!\n"
            f"   🎵 {music.title} - {music.artist}\n"
            f"   📁 Salvo na biblioteca offline de {user.get_name()}."
        )

    def list_downloads(self) -> List[str]:
        return list(self._downloaded)
