"""
ui/terminal_ui.py

Princípio aplicado: Single Responsibility Principle (SRP)
   - TerminalUI tem UMA responsabilidade: gerenciar a interação com o terminal
   - Não contém lógica de negócio — apenas chama os serviços e formata a saída

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Recebe todos os serviços como abstrações / injeção de dependência
"""

import os
from typing import List
from interfaces.abstractions import IUser
from models.user import FreeUser, PremiumUser
from services.catalog_service import MusicCatalogService
from services.playlist_service import PlaylistService
from services.player_service import PlayerService
from services.download_service import DownloadService
from services.recommendation_service import RecommendationService
from strategies.recommendation import PopularRecommendationStrategy, GenreRecommendationStrategy


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\n  Pressione ENTER para continuar...")


class TerminalUI:
    """
    Interface de terminal do Streamify.
    SRP: só gerencia I/O do terminal e coordena chamadas aos serviços.
    """

    def __init__(self):
        # DIP: instancia apenas os serviços concretos aqui (raiz de composição)
        self._catalog_svc = MusicCatalogService()
        self._playlist_svc = PlaylistService(self._catalog_svc)
        self._player_svc = PlayerService(self._catalog_svc)
        self._download_svc = DownloadService(self._catalog_svc)
        self._rec_svc = RecommendationService(
            self._catalog_svc,
            PopularRecommendationStrategy(),   # estratégia padrão
        )

        # Usuário atual (começa como Free — pode ser trocado)
        self._current_user: IUser = FreeUser("Visitante")

    # ──────────────────────────────── HEADER ─────────────────────────────────

    def _print_header(self) -> None:
        print("\n" + "═" * 45)
        print("  ♫  S T R E A M I F Y")
        print("═" * 45)
        print(f"  Usuário: {self._current_user}")
        print("═" * 45)

    def _print_menu(self) -> None:
        self._print_header()
        print("""
  1  →  Criar playlist
  2  →  Adicionar música à playlist
  3  →  Ver playlists
  4  →  Reproduzir música
  5  →  Fazer download offline
  6  →  Ver recomendações
  7  →  Ver catálogo de músicas
  8  →  Trocar usuário
  0  →  Sair
""")
        print("─" * 45)

    # ──────────────────────────────── OPÇÕES ─────────────────────────────────

    def _criar_playlist(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── CRIAR PLAYLIST ──\n")
        name = input("  Nome da playlist: ").strip()
        if name:
            result = self._playlist_svc.create_playlist(name, self._current_user.get_name())
            print(f"\n  {result}")
        else:
            print("  ❌ Nome inválido.")
        pause()

    def _adicionar_musica(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── ADICIONAR MÚSICA À PLAYLIST ──\n")

        playlists = self._playlist_svc.list_playlists()
        if not playlists:
            print("  ❌ Nenhuma playlist criada ainda. Crie uma primeiro.")
            pause()
            return

        print("  Playlists disponíveis:")
        for i, p in enumerate(playlists, 1):
            print(f"    {i}. {p['name']} ({len(p['tracks'])} músicas)")

        playlist_name = input("\n  Nome da playlist: ").strip()
        if not playlist_name:
            return

        self._mostrar_catalogo_resumido()
        music_title = input("\n  Título da música: ").strip()
        if music_title:
            result = self._playlist_svc.add_music_to_playlist(playlist_name, music_title)
            print(f"\n  {result}")
        pause()

    def _ver_playlists(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── MINHAS PLAYLISTS ──\n")

        playlists = self._playlist_svc.list_playlists()
        if not playlists:
            print("  Nenhuma playlist criada ainda.")
            pause()
            return

        for p in playlists:
            print(f"  📋 {p['name']}  (dono: {p['owner']}, duração: {p['total_duration']})")
            if p["tracks"]:
                for t in p["tracks"]:
                    print(f"      ♪ {t['title']} — {t['artist']}  [{t['duration']}]")
            else:
                print("      (playlist vazia)")
            print()
        pause()

    def _reproduzir_musica(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── REPRODUZIR MÚSICA ──\n")
        self._mostrar_catalogo_resumido()
        title = input("\n  Título da música: ").strip()
        if title:
            result = self._player_svc.play_music(title)
            print(result)
        pause()

    def _fazer_download(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── DOWNLOAD OFFLINE ──\n")
        self._mostrar_catalogo_resumido()
        title = input("\n  Título da música para download: ").strip()
        if title:
            # LSP em ação: passa self._current_user — Free ou Premium, não importa
            result = self._download_svc.download(title, self._current_user)
            print(f"\n  {result}")

        downloaded = self._download_svc.list_downloads()
        if downloaded:
            print(f"\n  📁 Biblioteca offline ({len(downloaded)} músicas):")
            for d in downloaded:
                print(f"     • {d}")
        pause()

    def _ver_recomendacoes(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── RECOMENDAÇÕES ──\n")

        # Escolha de estratégia (OCP: sem alterar serviços, troca comportamento)
        print("  Escolha a estratégia:")
        print("    1 → Por Popularidade")
        print("    2 → Por Gênero (baseado no histórico)")
        escolha = input("\n  Opção: ").strip()

        if escolha == "1":
            self._rec_svc.set_strategy(PopularRecommendationStrategy())
        elif escolha == "2":
            self._rec_svc.set_strategy(GenreRecommendationStrategy())
        else:
            print("  ❌ Opção inválida.")
            pause()
            return

        history = self._player_svc.get_history()
        recommendations = self._rec_svc.recommend(history)

        print(f"\n  Estratégia: {self._rec_svc.get_current_strategy_name()}\n")
        if not recommendations:
            print("  Sem recomendações disponíveis no momento.")
        else:
            print("  🎧 Recomendadas para você:\n")
            for i, m in enumerate(recommendations, 1):
                print(f"    {i}. {m['title']} — {m['artist']}  [{m['genre']}]  🔊 {m['plays']} plays")
        pause()

    def _ver_catalogo(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── CATÁLOGO COMPLETO ──\n")
        catalog = self._catalog_svc.get_all()
        for m in catalog:
            print(f"  ♪ {m.title:<28} {m.artist:<20} [{m.genre}]  {m.duration_formatted()}")
        pause()

    def _trocar_usuario(self) -> None:
        clear_screen()
        self._print_header()
        print("\n  ── TROCAR USUÁRIO ──\n")
        print("  1 → Conta Free")
        print("  2 → Conta Premium ★")
        opcao = input("\n  Tipo de conta: ").strip()

        if opcao not in ("1", "2"):
            print("  ❌ Opção inválida.")
            pause()
            return

        nome = input("  Nome do usuário: ").strip()
        if not nome:
            print("  ❌ Nome inválido.")
            pause()
            return

        # LSP: sistema aceita qualquer IUser — Free ou Premium
        if opcao == "1":
            self._current_user = FreeUser(nome)
        else:
            self._current_user = PremiumUser(nome)

        # Reset do histórico e downloads ao trocar de usuário
        self._player_svc.clear_history()
        print(f"\n  ✅ Bem-vindo(a), {self._current_user}!")
        pause()

    def _mostrar_catalogo_resumido(self) -> None:
        """Exibe catálogo compacto para seleção rápida."""
        catalog = self._catalog_svc.get_all()
        print("  Músicas disponíveis no catálogo:\n")
        for m in catalog:
            print(f"    • {m.title} — {m.artist}  [{m.genre}]")

    # ──────────────────────────────── LOOP PRINCIPAL ─────────────────────────

    def run(self) -> None:
        """Loop principal da aplicação."""
        actions = {
            "1": self._criar_playlist,
            "2": self._adicionar_musica,
            "3": self._ver_playlists,
            "4": self._reproduzir_musica,
            "5": self._fazer_download,
            "6": self._ver_recomendacoes,
            "7": self._ver_catalogo,
            "8": self._trocar_usuario,
        }

        while True:
            clear_screen()
            self._print_menu()
            choice = input("  Escolha uma opção: ").strip()

            if choice == "0":
                clear_screen()
                print("\n  👋 Obrigado por usar o Streamify! Até logo.\n")
                break
            elif choice in actions:
                actions[choice]()
            else:
                print("\n  ❌ Opção inválida. Tente novamente.")
                pause()
