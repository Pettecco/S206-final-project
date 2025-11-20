# Ultimate Tic-Tac-Toe — Repositório de teste (PyTest)

Projeto usado para a disciplina de Qualidade de Software: contém uma implementação concorrente (threads) do jogo Ultimate Tic-Tac-Toe com interface PyQt5 e integração com MySQL. O objetivo deste repositório é servir como base para escrever testes com `pytest`.

Como rodar:

1. Crie e ative um virtualenv (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Subir banco MySQL (opcional — Docker Compose já configurado):

```bash
# cria .env a partir do exemplo (opcional)
cp .env.example .env
# sobe o banco (inicializa schema em database/schema.sql)
docker compose up -d
```

4. Rode a aplicação:

```bash
python3 TicTacToeSemaphore.py
```

Arquivos importantes

- `src/` — código do jogo (UI e lógica)
- `database/schema.sql` — esquema inicial do banco (usado pelo `docker-compose.yml`)
- `docker-compose.yml` — serviço `db` (MySQL) que inicializa o schema
- `requirements.txt` — dependências usadas no ambiente
