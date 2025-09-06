![Logo do Ryzor](assets/Ryzor_icon.png)

# Ryzor

Ryzor é uma ferramenta de **linha de comando (CLI)** para organização, backup e gerenciamento de arquivos por tipo/extensão. O projeto ainda está em desenvolvimento e **não está pronto para uso em produção**.

---

## Visão Geral

- **Objetivo principal:** Automatizar a organização e backup de arquivos em diretórios, categorizando-os por tipos/extensões definidos pelo usuário.
- **Funcionalidades atuais:**
  - Definir e editar tipos de arquivos/extensões.
  - Listar arquivos e extensões.
  - Remover tipos/extensões.
  - Interface CLI amigável e visualmente rica com Rich.
  - Barra de progresso e feedback visual.
- **Persistência de dados:** Arquivos JSON (`extensions.json`) armazenam as definições de tipos e extensões.

---

## Estrutura do Projeto

```

.
├── src/
│   ├── cli.py           # Ponto de entrada CLI
│   ├── logger.py        # Logging e UI
│   ├── modules/
│   │   ├── definer.py
│   │   ├── file\_manager.py
│   │   ├── lister.py
│   │   ├── remover.py
│   │   └── data/extensions.json
├── tests/
│   └── generator.py     # Geração de arquivos de teste
└── ryzor.txt            # Documentação interna

````

---

## Exemplo de Uso

```sh
# Organizar arquivos
python src/cli.py organize -p ./meus_arquivos -d ./organizados

# Definir novas extensões
python src/cli.py define -t Imagens -exts .jpg .png .gif

# Listar extensões
python src/cli.py list -e_exts

# Remover extensões
python src/cli.py remove -t Imagens -exts .gif
````

---

## Dependências

* Python 3.11+
* [Rich](https://pypi.org/project/rich/)
* [pyfiglet](https://pypi.org/project/pyfiglet/)
* Bibliotecas padrão: `pathlib`, `shutil`, `os`, `json`, `argparse`, `pprint`, `typing`

Instalação das dependências:

```sh
pip install rich pyfiglet
```

---

## Status

* Projeto funcional, mas **em estágio intermediário**:

  * Sem testes automatizados.
  * Sem validação robusta de inputs.
  * Não pronto para produção.
  * Sem documentação externa completa.

---

> Recomenda-se colocar as imagens em uma pasta `assets` dentro do projeto.

---

## Licença

Este projeto ainda não possui uma licença definida.
