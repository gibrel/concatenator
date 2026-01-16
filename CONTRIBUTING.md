# Contribuindo para o concatenator

Obrigado por considerar contribuir! Este documento descreve o fluxo para abrir issues, enviar pull requests e manter a qualidade do projeto.

## Como começar

1. Faça um fork do repositório e crie uma branch a partir de `main`.
2. Crie e ative um ambiente virtual.
3. Instale as dependências de desenvolvimento:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Padrões de código e qualidade

Antes de abrir um PR, execute:

```bash
python -m ruff check .
python -m mypy src
python -m pytest --cov
```

O CI executa exatamente os mesmos comandos em Linux, macOS e Windows.

## Commits convencionais

Utilizamos **Conventional Commits** para manter histórico consistente e facilitar notas de release.
Formato esperado:

```text
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé(s) opcional(is)]
```

Exemplos:

- `feat: adicionar filtro por extensão`
- `fix(cli): corrigir caminho relativo`
- `docs: atualizar README`

## Versionamento e releases

- O projeto segue **SemVer (Semantic Versioning)**.
- Releases são tagueadas como `vX.Y.Z` (ex.: `v0.1.0`).
- A cada release, o `CHANGELOG.md` deve ser atualizado e as notas de release são geradas a partir dos commits convencionais.

Fluxo sugerido:

1. Atualize versão e changelog.
2. Garanta que o CI esteja verde.
3. Crie a tag: `git tag vX.Y.Z && git push origin vX.Y.Z`.
4. Publique a release com as notas derivadas dos commits convencionais.

## Abrindo um Pull Request

- Descreva claramente o problema e a solução.
- Referencie issues relacionadas.
- Inclua testes para novas funcionalidades ou correções.

Obrigado por contribuir! 🎉
