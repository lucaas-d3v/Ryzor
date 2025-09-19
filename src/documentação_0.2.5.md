
# Ryzor — Documentação Técnica

## Sumário

- Visão Geral
- Estrutura de Arquivos
- Análise de Código por Arquivo
- APIs e Endpoints
- Banco de Dados e Persistência
- Configuração
- Instalação
- Uso
- Testes
- Segurança
- Deploy
- Troubleshooting
- Roadmap
- Contribuição
- Dependências Principais
- Ações Recomendadas
- Arquivos Ignorados

---

## Visão Geral

Ryzor é uma ferramenta de linha de comando (CLI) para organização, backup e gerenciamento de arquivos por tipo/extensão. O projeto está em desenvolvimento e **não está pronto para produção**.

- **Automatiza** a organização e backup de arquivos em diretórios, categorizando-os por tipos/extensões definidos pelo usuário.
- **Persistência** via arquivos JSON.
- **Interface CLI** rica, com feedback visual usando Rich.

---

## Estrutura de Arquivos

```
.
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── t.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── definer.py
│   │   ├── file_manager.py
│   │   ├── lister_manager.py
│   │   ├── logger.py
│   │   ├── remover.py
│   │   ├── repair_manager.py
│   │   ├── utils.py
│   │   └── data/
│   │       └── extensions.json
│   ├── data/
│   │   └── extensions.json
│   └── protected/
│       └── extensions_default.json
├── tests/
│   └── generator.py
```

---

## Análise de Código por Arquivo

### pyproject.toml
- **Propósito:** Configuração do projeto Python (build, dependências, entrypoint).
- **Dependências:** `rich`, `pyfiglet`, `send2trash`, `setuptools`, `wheel`.
- **Entrypoint:** `ryzor = src.cli:main`

### requirements.txt
- **Propósito:** Lista de dependências para instalação via pip.
- **Conteúdo:**  
  ```
  rich==13.9.4
  pyfiglet==0.8.post1
  send2trash==1.8.3
  ```

### README.md
- **Propósito:** Documentação básica, exemplos de uso, dependências e status do projeto.


### cli.py
- **Propósito:** Ponto de entrada da CLI. Gerencia argumentos, inicializa módulos e executa comandos.
- **Principais imports:** `argparse`, `rich.console.Console`, módulos internos.
- **Funções/Classes:**
  - `main()`: Inicializa CLI, valida módulos, instancia gerenciadores e configura argumentos.
- **Exemplo de uso:**
  ```sh
  ryzor organize -p ./meus_arquivos -d ./organizados
  ```

### definer.py
- **Propósito:** Gerencia definição de tipos/extensões.
- **Classe:** `DefinitionManager`
  - `normalize_extensions_input(exts)`: Normaliza entrada de extensões.
  - `save_extensions(data)`: Salva extensões em JSON.
  - `read_extensions(json_path)`: Lê extensões do JSON.

### file_manager.py
- **Propósito:** Gerencia operações de arquivos (organização, backup, renomeação).
- **Classe:** `FileController`
  - `rename(file, qtd)`: Gera nome único para arquivo.
  - `relocate_files(...)`: Organiza/backup de arquivos entre diretórios.

### lister_manager.py
- **Propósito:** Listagem de arquivos e extensões.
- **Classe:** `Viewer`
  - `show_files(conteudo, verbose)`: Exibe arquivos.
  - `list_files(caminho, recursive_mode, verbose)`: Lista arquivos.
  - `list_extensions()`: Lista extensões definidas.

### logger.py
- **Propósito:** Gerencia saída visual no terminal (Rich), temas, banners, logs.
- **Classe:** `ConsoleManager`
  - Métodos para exibir banners, logs, tabelas, progresso, etc.

### remover.py
- **Propósito:** Gerencia remoção de tipos/extensões.
- **Classe:** `DeletionManager`
  - `remove_extensions(type, extensions, no_preview, y)`: Remove extensões/tipos.

### repair_manager.py
- **Propósito:** Restauração/reparo de arquivos de configuração e módulos.
- **Classe:** `Restorer`
  - Métodos para restaurar arquivos padrão, reinstalar dependências, etc.

### utils.py
- **Propósito:** Utilitários gerais, validação de módulos, mensagens de erro.
- **Funções:**  
  - `show_module_missing(module_name, modules_names)`
  - `_validate_modules()`

### t.py
- **Propósito:** Script utilitário para leitura e cópia de conteúdos de módulos.
- **Observação:** Não faz parte do fluxo principal.

### extensions.json & extensions.json
- **Propósito:** Armazenam mapeamento de tipos de arquivos e extensões.
- **Exemplo de schema:**
  ```json
  {
    "Effects": [".fx", ".ffx", ...],
    "Compactados": [".rar", ".zip", ...],
    ...
  }
  ```

### generator.py
- **Propósito:** Gera arquivos de teste com extensões variadas para simular cenários de uso.

---

## APIs e Endpoints

- **Não há endpoints HTTP/REST.**  
  Toda a interação é via CLI.

---

## Banco de Dados e Persistência

- **Persistência:**  
  - Arquivos JSON (extensions.json) para tipos/extensões.
  - Não utiliza banco de dados relacional ou NoSQL.

---

## Configuração

- **Configuração principal:**  
  - pyproject.toml (build, dependências, entrypoint)
  - requirements.txt (dependências)
  - Arquivos JSON para tipos/extensões.

---

## Instalação

```sh
# Clone o repositório
git clone <repo-url>
cd Ryzor

# Instale as dependências
pip install -r requirements.txt
# ou
pip install rich pyfiglet send2trash

# No mesmo diretório do pyproject.toml.
pip install . 
```    

---

## Uso

```sh
# Organizar arquivos
ryzor organize -p ./meus_arquivos -d ./organizados

# Definir novas extensões
ryzor define -t Imagens -exts .jpg .png .gif

# Listar extensões
ryzor list -e_exts

# Remover extensões
ryzor remove -t Imagens -exts .gif
```

---

## Testes

- **Automatizados:** Não implementados.
- **Manual:** Use generator.py para gerar arquivos de teste.

---

## Segurança

- **Sem autenticação ou controle de acesso.**
- **Riscos:**  
  - Remoção acidental de arquivos/tipos.
  - Falta de validação robusta de inputs.
  - Dependências externas podem ser exploradas se desatualizadas.

---

## Deploy

- **Não há processo de deploy automatizado.**
- **Uso local:** Executar via Python 3.11+.

---

## Troubleshooting

- **Problemas comuns:**
  - Módulos não encontrados: execute `ryzor repair`.
  - Dependências não instaladas: `pip install -r requirements.txt`.
  - Erros de permissão: execute como usuário com permissões adequadas.

---

## Roadmap

1. Implementar testes automatizados.
2. Melhorar validação de inputs.
3. Adicionar documentação externa completa.
4. Suporte a plugins/extensões.
5. Internacionalização (i18n).

---

## Contribuição

- Fork, branch, pull request.
- Siga o padrão PEP8.
- Adicione testes para novas funcionalidades.
- Documente suas alterações.

---

## Dependências Principais (Top 10)

1. **rich** — Saída visual no terminal.
2. **pyfiglet** — Geração de banners ASCII.
3. **send2trash** — Envio seguro de arquivos para lixeira.
4. **setuptools** — Build e empacotamento.
5. **wheel** — Build de pacotes.
6. **pathlib** — Manipulação de caminhos.
7. **shutil** — Operações de arquivos.
8. **argparse** — Parsing de argumentos CLI.
9. **json** — Persistência de dados.
10. **typing** — Tipagem estática.

**Riscos conhecidos:**  
- Dependências externas não fixadas podem introduzir breaking changes.
- Falta de testes automatizados.

---

## Ações Recomendadas

1. **Crítico:** Implementar testes automatizados para evitar regressões.
2. **Alto:** Adicionar validação robusta de inputs do usuário.
3. **Médio:** Documentar todos os comandos e opções CLI detalhadamente.
4. **Médio:** Automatizar o deploy e setup do ambiente.
5. **Baixo:** Adicionar suporte a internacionalização (i18n).

---

## Arquivos Ignorados

- **Por .gitignore:**  
  - `.venv/`, `venv/`, `env/`, `ENV/`, build, `dist/`, `*.egg-info/`, `.eggs/`, .vscode, `.idea/`, `*.iml`, `*.log`, `*.pyc`, `__pycache__/`, `tests/arquivos/`, arquivos temporários.
- **Por extensão:**  
  - `.png` (ex: Ryzor_Banner.png), `.pyc`, `.log`, etc.
- **Por tamanho:**  
  - Nenhum arquivo > 500 KB detectado.
- **Binários:**  
  - Não há binários analisados.
- **Outros:**  
  - Scripts utilitários fora do escopo principal (ex: t.py).

---

**Observações Técnicas:**  
- O projeto segue boas práticas de modularização, mas carece de testes e validação de entradas.
- Uso de Rich para CLI é um diferencial visual.
- Persistência simples via JSON facilita portabilidade, mas limita escalabilidade.

---
