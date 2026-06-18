"""
models/user.py

Princípio aplicado: Liskov Substitution Principle (LSP)
   - PremiumUser pode substituir FreeUser em qualquer ponto do sistema
     sem quebrar o comportamento esperado
   - Ambos implementam IUser e honram o mesmo contrato

Princípio aplicado: Single Responsibility Principle (SRP)
   - Cada classe de usuário só representa o perfil e as permissões do usuário
   - Não faz download, não toca música — apenas responde QUEM é e O QUE PODE fazer
"""

from interfaces.abstractions import IUser


class FreeUser(IUser):
    """
    Usuário da conta gratuita.
    Pode ouvir e criar playlists, mas não pode baixar músicas.
    """

    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_account_type(self) -> str:
        return "Free"

    def can_download(self) -> bool:
        # LSP: FreeUser retorna False — contrato honrado
        return False

    def __str__(self) -> str:
        return f"{self._name} [Free]"


class PremiumUser(IUser):
    """
    Usuário da conta premium.
    LSP: substitui FreeUser em qualquer lugar sem quebrar o sistema.
    A única diferença está no retorno de can_download() e get_account_type().
    """

    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_account_type(self) -> str:
        return "Premium ★"

    def can_download(self) -> bool:
        # LSP: PremiumUser retorna True — o sistema só verifica can_download()
        return True

    def __str__(self) -> str:
        return f"{self._name} [Premium ★]"
