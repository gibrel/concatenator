# pyminplate

Boilerplate mínimo para iniciar projetos Python com boas práticas e tooling moderno.

## O que vem pronto

- **Gerenciador de dependências**: `pyproject.toml`
- **Layout do código**: `src/`
- **Testes**: `pytest` (configurado no `pyproject.toml`)
- **Lint/format**: `ruff`
- **Type check**: `mypy`
- **Python**: >= 3.12.12
- **Estrutura**: `domain/`, `services/` e `core/`
- **CLI**: comando `pyminplate`

## Estrutura do projeto

```text
pyminplate/
├── src/
│   └── pyminplate/
│       ├── core/
│       │   ├── config.py
│       │   ├── exceptions.py
│       │   ├── logger.py
│       │   └── paths.py
│       ├── domain/
│       ├── services/
│       └── cli.py
├── tests/
├── pyproject.toml
├── Makefile
└── .editorconfig
```

## Como usar

### 1) Criar ambiente virtual e instalar dependências

```bash
make deps
```

### 2) Executar o CLI

```bash
make run
```

### 3) Rodar testes

```bash
make test
```

### 4) Lint, format e type check

```bash
make format
make lint
make type
```

## Customização

- Ajuste metadados do projeto em `pyproject.toml`.
- Acrescente regras em `src/pyminplate/domain` e `src/pyminplate/services`.
- Centralize configurações em `src/pyminplate/core`.

## Licença

The Unlicense. Consulte o arquivo [LICENSE](LICENSE).
