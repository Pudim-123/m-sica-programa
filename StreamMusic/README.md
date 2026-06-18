# 🎵 Streamify — Sistema de Streaming de Música

Projeto acadêmico em Python demonstrando os princípios SOLID  
com um sistema de streaming de música executado no terminal.

---

## 📁 Estrutura de Pastas

```
Musicfy/
├── main.py                          ← Ponto de entrada
├── README.md
│
├── interfaces/
│   ├── __init__.py
│   └── abstractions.py              ← ISP + DIP: interfaces segregadas
│
├── models/
│   ├── __init__.py
│   ├── music.py                     ← SRP: entidade Música
│   ├── playlist.py                  ← SRP: entidade Playlist
│   └── user.py                      ← SRP + LSP: FreeUser e PremiumUser
│
├── services/
│   ├── __init__.py
│   ├── catalog_service.py           ← SRP + DIP
│   ├── playlist_service.py          ← SRP + DIP + Composição
│   ├── player_service.py            ← SRP + DIP
│   ├── download_service.py          ← SRP + DIP + LSP
│   └── recommendation_service.py   ← OCP + DIP (Strategy Pattern)
│
├── strategies/
│   ├── __init__.py
│   └── recommendation.py            ← OCP: estratégias intercambiáveis
│
└── ui/
    ├── __init__.py
    └── terminal_ui.py               ← SRP: apenas I/O do terminal
```

---

## ▶️ Como Executar

```bash
# Sem dependências externas — apenas Python 3.8+
python main.py
```

---

## 🏗️ Princípios SOLID Aplicados

### S — Single Responsibility Principle

| Classe / Módulo        | Única Responsabilidade                         |
|------------------------|------------------------------------------------|
| `Music`                | Armazenar dados de uma música                 |
| `Playlist`             | Manter uma coleção ordenada de músicas        |
| `FreeUser/PremiumUser` | Representar perfil e permissões do usuário    |
| `MusicCatalogService`  | Gerenciar o catálogo global de músicas        |
| `PlaylistService`      | Criar e gerenciar playlists                   |
| `PlayerService`        | Simular reprodução de músicas                 |
| `DownloadService`      | Gerenciar downloads offline                   |
| `RecommendationService`| Coordenar a estratégia de recomendação        |
| `TerminalUI`           | Gerenciar I/O do terminal                     |

---

### O — Open/Closed Principle

O sistema de recomendações usa o **Strategy Pattern**:
- `IRecommendationStrategy` define o contrato
- `PopularRecommendationStrategy` e `GenreRecommendationStrategy` são implementações
- Para adicionar uma nova estratégia, **não se modifica nenhum código existente**,
  basta criar uma nova classe que implemente a interface

```python
# Nova estratégia sem tocar em nada existente:
class MoodRecommendationStrategy(IRecommendationStrategy):
    def recommend(self, catalog, history): ...
    def strategy_name(self): return "Por Humor"
```

---

### L — Liskov Substitution Principle

`PremiumUser` e `FreeUser` ambos implementam `IUser`.  
O `DownloadService` recebe `IUser` — nunca sabe se é Free ou Premium:

```python
def download(self, music_title: str, user: IUser) -> str:
    if not user.can_download():   # polimorfismo puro
        return "❌ Acesso negado..."
```

Substituir `FreeUser` por `PremiumUser` não quebra nenhuma lógica.

---

### I — Interface Segregation Principle

Ao invés de uma interface monolítica, foram criadas interfaces específicas:

| Interface                   | Responsabilidade           |
|-----------------------------|----------------------------|
| `IPlayable`                 | Reprodução de mídia        |
| `IDownloadable`             | Download offline           |
| `IPlaylistManager`          | Gestão de playlists        |
| `IRecommendationStrategy`   | Algoritmo de recomendação  |
| `IUser`                     | Perfil e permissões        |

---

### D — Dependency Inversion Principle

Todos os serviços recebem suas dependências via injeção (construtor):

```python
# PlaylistService depende da abstração MusicCatalogService
class PlaylistService(IPlaylistManager):
    def __init__(self, catalog_service: MusicCatalogService):
        self._catalog = catalog_service  # injetado de fora

# RecommendationService depende da abstração IRecommendationStrategy
class RecommendationService:
    def __init__(self, catalog_service, strategy: IRecommendationStrategy):
        self._strategy = strategy  # nunca instancia concreto internamente
```

---

## 🧩 Exemplo de Composição

`PlaylistService` é **composto** por `MusicCatalogService` (tem-um, não é-um):

```python
class PlaylistService(IPlaylistManager):
    def __init__(self, catalog_service: MusicCatalogService):
        self._catalog = catalog_service   # composição
```

Isso mantém baixo acoplamento: `PlaylistService` colabora com o catálogo  
sem herdar seus detalhes de implementação.

---

## 👤 Tipos de Usuário

| Funcionalidade       | Free | Premium ★ |
|----------------------|------|-----------|
| Criar playlists      | ✅   | ✅        |
| Ouvir músicas        | ✅   | ✅        |
| Ver recomendações    | ✅   | ✅        |
| Download offline     | ❌   | ✅        |

---

## 🎯 Estratégias de Recomendação

| Estratégia          | Algoritmo                                          |
|---------------------|----------------------------------------------------|
| Popular             | Ordena por número de plays, exclui já ouvidas      |
| Por Gênero          | Identifica gênero favorito do histórico e filtra   |
