"""
strategies/recommendation.py

Princípio aplicado: Open/Closed Principle (OCP)
   - O sistema está ABERTO para extensão (novas estratégias) e
     FECHADO para modificação (código existente não é alterado)
   - Para adicionar uma nova estratégia, basta criar uma nova classe
     que implemente IRecommendationStrategy

Padrão de Projeto: Strategy Pattern
   - Permite trocar o algoritmo de recomendação em tempo de execução
"""

from typing import List
from interfaces.abstractions import IRecommendationStrategy


class PopularRecommendationStrategy(IRecommendationStrategy):
    """
    Estratégia 1: Recomenda as músicas mais tocadas do catálogo.
    OCP: adicionada sem modificar nenhum código existente.
    """

    def recommend(self, music_catalog: List[dict], user_history: List[str]) -> List[dict]:
        # Ordena por número de plays (desc) e exclui o que o usuário já ouviu
        not_heard = [m for m in music_catalog if m["title"] not in user_history]
        sorted_by_plays = sorted(not_heard, key=lambda m: m["plays"], reverse=True)
        return sorted_by_plays[:5]

    def strategy_name(self) -> str:
        return "🔥 Recomendação Popular (mais tocadas)"


class GenreRecommendationStrategy(IRecommendationStrategy):
    """
    Estratégia 2: Recomenda músicas do gênero mais ouvido pelo usuário.
    OCP: adicionada sem modificar nenhum código existente.
    """

    def recommend(self, music_catalog: List[dict], user_history: List[str]) -> List[dict]:
        if not user_history:
            # Sem histórico: retorna as 5 primeiras do catálogo
            return music_catalog[:5]

        # Descobre o gênero mais frequente no histórico do usuário
        heard_music = [m for m in music_catalog if m["title"] in user_history]
        genre_count: dict = {}
        for music in heard_music:
            genre = music["genre"]
            genre_count[genre] = genre_count.get(genre, 0) + 1

        if not genre_count:
            return music_catalog[:5]

        favorite_genre = max(genre_count, key=genre_count.get)

        # Filtra catálogo pelo gênero favorito, excluindo já ouvidas
        recommendations = [
            m for m in music_catalog
            if m["genre"] == favorite_genre and m["title"] not in user_history
        ]
        return recommendations[:5]

    def strategy_name(self) -> str:
        return "🎵 Recomendação por Gênero (baseada no seu histórico)"
