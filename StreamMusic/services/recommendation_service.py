"""
services/recommendation_service.py

Princípio aplicado: Open/Closed Principle (OCP)
   - RecommendationService delega para IRecommendationStrategy
   - Novas estratégias são adicionadas sem alterar esta classe

Princípio aplicado: Dependency Inversion Principle (DIP)
   - Depende de IRecommendationStrategy (abstração), não de implementações concretas
   - A estratégia concreta é injetada de fora (via set_strategy)

Padrão de Projeto: Strategy Pattern
   - A estratégia pode ser trocada em tempo de execução via set_strategy()
"""

from typing import List, Optional
from interfaces.abstractions import IRecommendationStrategy
from services.catalog_service import MusicCatalogService


class RecommendationService:
    """
    Serviço de recomendação que delega para uma estratégia intercambiável.

    OCP: aberto para extensão (novas estratégias), fechado para modificação.
    DIP: depende de IRecommendationStrategy, nunca de classes concretas.
    """

    def __init__(
        self,
        catalog_service: MusicCatalogService,
        strategy: IRecommendationStrategy,
    ):
        # DIP: ambas as dependências são injetadas como abstrações
        self._catalog = catalog_service
        self._strategy: IRecommendationStrategy = strategy

    def set_strategy(self, strategy: IRecommendationStrategy) -> None:
        """
        Permite trocar a estratégia em tempo de execução.
        OCP: sem alterar esta classe, o comportamento muda completamente.
        """
        self._strategy = strategy

    def get_current_strategy_name(self) -> str:
        return self._strategy.strategy_name()

    def recommend(self, user_history: List[str]) -> List[dict]:
        """Delega para a estratégia atual."""
        catalog = self._catalog.catalog_as_dicts()
        return self._strategy.recommend(catalog, user_history)
