# `concatenator`

![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-Unlicense-black.svg)
![Style](https://img.shields.io/badge/code%20style-ruff-red)
![Type Checking](https://img.shields.io/badge/type%20checking-mypy-blueviolet)
![Status](https://img.shields.io/badge/status-alpha-orange)

A ferramenta de linha de comando `concatenator` é uma  escrita em Python para percorrer diretórios recursivamente e consolidar o conteúdo de múltiplos arquivos de texto em um único arquivo final.

O projeto é voltado para inspeção de repositórios, auditoria de código, documentação técnica, análise de projetos e qualquer cenário em que seja útil visualizar o conteúdo completo de uma árvore de arquivos de forma organizada e rastreável.

---

## ⚡ Quickstart

```bash
concatenator . \
  --include-extensions .py .md .toml \
  --ignore-extensions .png .jpg .pdf \
  --ignore-directories .git .venv node_modules \
  --max-file-size 200000 \
  --skip-binary
```

Esse comando cobre o caso mais comum: inclui apenas arquivos de texto úteis, ignora diretórios de tooling e arquivos grandes/binários, reduzindo ruído e tempo de execução.

---

## 📚 Índice

- [Quickstart](#-quickstart)
- [Principais características](#-principais-características)
- [Para quem é](#-para-quem-é)
- [Princípios do projeto](#-princípios-do-projeto)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Uso básico](#️-uso-básico)
- [Opções do CLI](#️-opções-do-cli)
- [Semântica dos filtros](#-semântica-dos-filtros)
- [Formatação do conteúdo](#-formatação-do-conteúdo)
- [Comportamento importante](#-comportamento-importante)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Testes](#-testes)
- [Qualidade de código](#-qualidade-de-código)
- [Extensibilidade](#-extensibilidade)
- [Contribuições](#-contribuições)
- [Licença](#-licença)

---

## ✨ Principais características

- Varredura recursiva de diretórios
- Inclusão e exclusão de arquivos por extensão
- Ignorar diretórios específicos
- Detecção e exclusão de arquivos binários
- Limite máximo de tamanho por arquivo
- Cabeçalhos e rodapés customizáveis
- Saída em Markdown por padrão
- Configuração totalmente via CLI
- Código modular, tipado e extensível

---

## 🎯 Para quem é

O `concatenator` é útil para:

- Desenvolvedores que precisam auditar ou revisar repositórios
- Geração de documentação consolidada
- Análise de projetos legados
- Preparação de conteúdo para indexadores, buscadores ou LLMs
- Inspeção rápida de árvores de arquivos grandes

---

## 🧭 Princípios do projeto

- Fazer uma coisa e fazê-la bem
- Comportamento previsível e explícito
- Nenhuma configuração oculta
- Código legível e fácil de manter
- Extensível sem acoplamento ao CLI

---

## 📦 Requisitos

- Python **>= 3.12**
- Compatível com Linux, macOS e Windows

---

## 🚀 Instalação

### Desenvolvimento local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Ou utilizando o `Makefile`:

```bash
make deps
```

### Build e instalação local

```bash
make install
```

### Uso sem instalação

```bash
make run "$ARGS"
```

---

## ▶️ Uso básico

```bash
concatenator ./pasta-alvo
```

Por padrão, o comando gera um arquivo `output.md` no diretório atual contendo o conteúdo de todos os arquivos elegíveis encontrados, com caminhos exibidos a partir da pasta alvo (ex.: `/pasta-alvo/src/projeto/arquivo.py`).

---

## ⚙️ Opções do CLI

### Definir arquivo de saída

```bash
concatenator ./pasta-alvo -o ./saida/resultado.md
```

### Incluir apenas determinadas extensões

```bash
concatenator ./pasta-alvo \
  --include-extensions .py .md .toml
```

### Ignorar extensões específicas

```bash
concatenator ./pasta-alvo \
  --ignore-extensions .png .jpg .pdf .zip
```

### Ignorar diretórios

```bash
concatenator ./pasta-alvo \
  --ignore-directories .git .venv node_modules
```

### Detectar encoding automaticamente

```bash
concatenator ./pasta-alvo --detect-encoding
```

> ⚠️ Essa opção ativa detecção automática quando a leitura em UTF-8 falha e pode impactar a performance.

### Ignorar arquivos binários

```bash
concatenator ./pasta-alvo --skip-binary
```

### Limitar o tamanho máximo dos arquivos

```bash
concatenator ./pasta-alvo --max-file-size 50000
```

### Inspecionar sem escrita (dry run)

```bash
concatenator ./pasta-alvo --dry-run
```

### Listar arquivos incluídos sem gerar saída

```bash
concatenator ./pasta-alvo --list-files
```

---

## 🧭 Semântica dos filtros

### Precedência (ordem de aplicação)

1. **Ignorar diretórios**: diretórios excluídos são removidos da varredura antes de qualquer arquivo ser avaliado.
2. **Include extensions**: quando informado, funciona como *allowlist* (apenas essas extensões passam).
3. **Ignore extensions**: sempre bloqueia, mesmo que a extensão esteja na lista de inclusão.

### `ignore-directories`: nome vs caminho relativo

O filtro aceita **nomes de diretório** ou **caminhos relativos à pasta raiz informada**:

- **Nome**: ignora qualquer pasta com esse nome em qualquer nível.
  - Ex.: `--ignore-directories .git build` ignora todas as pastas `.git` e `build`.
- **Caminho relativo**: ignora apenas o caminho exato a partir da raiz.
  - Ex.: `--ignore-directories docs/generated` ignora somente `./docs/generated`.

> Dica: se você quer ignorar apenas uma subpasta específica, use o caminho relativo. Para ignorar qualquer pasta com o mesmo nome, use apenas o nome.

### Exemplos rápidos

```bash
# 1) Apenas .py e .md, mas sempre exclui .md se estiver em ignore-extensions
concatenator . --include-extensions .py .md --ignore-extensions .md

# 2) Ignora qualquer "dist", inclusive "docs/dist"
concatenator . --ignore-directories dist

# 3) Ignora apenas a pasta raiz específica "docs/dist"
concatenator . --ignore-directories docs/dist
```

---

## 🧩 Formatação do conteúdo

Cada arquivo incluído recebe um cabeçalho e um rodapé configuráveis:

```bash
--header-text "### {path}\n\n````{extension_name}"
--footer-text "````\n\n// End of {path}\n"
```

Para adicionar marcadores markdownlint-disable (MD010) em inserções `Makefile`, utilize:

```bash
concatenator ./pasta-alvo --markdownlint-disable-md010
# ou
concatenator ./pasta-alvo --mdlint-md010
```

Variáveis disponíveis:

- `{path}` → caminho do arquivo
- `{extension_name}` → extensão do arquivo sem o ponto (ou nome do arquivo se não houver extensão)

---

## 🧠 Comportamento importante

- Caminhos tratados com `pathlib` (multiplataforma)
- Extensões normalizadas (`.PY` → `.py`)
- Diretórios ignorados por nome ou caminho relativo
- Arquivos ilegíveis ignorados com segurança
- Fallback automático de encoding
- Detecção automática de encoding é opcional e pode impactar a performance
- Arquivos sem extensão usam o nome do arquivo como `extension_name` (ex.: `Makefile`)
- Metadados do pacote priorizam `description` do `pyproject.toml` (PEP 621)
- Resumo final exibe quantidade de arquivos incluídos, ignorados e tempo total

---

## Estrutura do projeto

```text
concatenator/
├── src/
│   └── concatenator/
│       ├── core/
│       │   ├── config.py      # Configuração central (Settings)
│       │   ├── exceptions.py
│       │   ├── logger.py      # Logging padronizado
│       │   └── paths.py
│       ├── services/
│       │   ├── condenser.py   # Lógica principal de condensação
│       │   ├── filters.py     # Filtros de arquivos e diretórios
│       │   └── readers.py     # Leitura e detecção de binários
│       ├── metadata.py        # Leitura de metadados do pacote
│       └── cli.py
├── tests/
├── pyproject.toml
├── README.md
├── Makefile
├── .editorconfig
└── LICENSE
```

---

## 🧪 Testes

```bash
make test
```

Para checar cobertura mínima (>= 80%):

```bash
make coverage
```

---

## 🧹 Qualidade de código

```bash
make format
make lint
make type

# ou então para lint + format + typecheck + test
make pre-commit
```

---

## 🔧 Extensibilidade

O `concatenator` foi projetado para ser facilmente estendido:

- Filtros → `services/filters.py`
- Leitores → `services/readers.py`
- Regras de negócio → `services/`
- Configuração → `core/config.py`

---

## 🤝 Contribuições

Contribuições são bem-vindas.
Issues, sugestões e pull requests ajudam a melhorar o projeto.

---

## 📄 Licença

The Unlicense.
Consulte o arquivo [LICENSE](./LICENSE).
