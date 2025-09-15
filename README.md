![Logo do Ryzor](assets/Ryzor_Banner.png)

---

# Ryzor

Ryzor é uma ferramenta de **linha de comando (CLI)** para organização, backup e gerenciamento de arquivos por tipo/extensão. O projeto está em desenvolvimento e **não está pronto para uso em produção**.

---

## Visão Geral

- **Objetivo principal:** Automatizar a organização e backup de arquivos em diretórios, categorizando-os por tipos/extensões definidos pelo usuário.
- **Funcionalidades atuais:**
  - Definir e editar tipos de arquivos/extensões
  - Organizar e realizar backup de arquivos entre diretórios
  - Listar arquivos e extensões com modo recursivo
  - Remover tipos/extensões com preview
  - Reparar e restaurar configurações padrão
  - Interface CLI rica com feedback visual usando Rich
  - Barra de progresso e logs detalhados
- **Persistência de dados:** Arquivos JSON (`extensions.json`) armazenam as definições de tipos e extensões.

---

## Instalação

### Via pip (Recomendado)
```bash
# Clone o repositório
git clone <repo-url>
cd Ryzor

# Instale as dependências
pip install -r requirements.txt

# Instale o pacote
pip install .

# Use diretamente o comando
ryzor help
```

### Instalação manual
```bash
# Instale apenas as dependências
pip install rich==13.9.4 pyfiglet==0.8.post1 send2trash==1.8.3

# Execute via Python
ryzor repair --dependences ou -dp
```

---

## Estrutura do Projeto

```
.
├── pyproject.toml           # Configuração do projeto e build
├── requirements.txt         # Dependências
├── README.md               # Documentação principal
├── src/
│   ├── cli.py              # Ponto de entrada CLI
│   ├── t.py                # Script utilitário
│   ├── modules/
│   │   ├── definer.py      # Gerenciamento de definições
│   │   ├── file_manager.py # Operações de arquivos
│   │   ├── lister_manager.py # Listagem de arquivos
│   │   ├── logger.py       # Interface e logging
│   │   ├── remover.py      # Remoção de tipos/extensões
│   │   ├── repair_manager.py # Restauração/reparo
│   │   ├── utils.py        # Utilitários gerais
│   │   └── data/
│   │       └── extensions.json
│   ├── data/
│   │   └── extensions.json # Configurações de extensões
│   └── protected/
│       └── extensions_default.json # Backup padrão
└── tests/
    └── generator.py        # Geração de arquivos de teste
```

---

## Comandos Disponíveis

### Organização de Arquivos
```bash
# Organizar arquivos por tipo
ryzor organize -p ./meus_arquivos -d ./organizados

# Organizar com modo recursivo
ryzor organize -p ./origem -d ./destino --recursive
```

### Gerenciamento de Tipos/Extensões
```bash
# Definir novas extensões para um tipo
ryzor define -t Imagens -exts .jpg .png .gif .webp

# Listar todas as extensões definidas
ryzor list -e_exts

# Listar arquivos em um diretório
ryzor list -p ./meus_arquivos --verbose

# Remover extensões de um tipo
ryzor remove -t Imagens -exts .gif

# Remover tipo completo
ryzor remove -t "Tipo Indesejado" --no-preview -y
```

### Reparo e Manutenção
```bash
# Reparar módulos e configurações
ryzor repair
```

---

## Dependências Principais

### Runtime
- **Python 3.11+** (obrigatório)
- **[Rich 13.9.4](https://pypi.org/project/rich/)** - Interface visual rica no terminal
- **[pyfiglet 0.8.post1](https://pypi.org/project/pyfiglet/)** - Geração de banners ASCII
- **[send2trash 1.8.3](https://pypi.org/project/send2trash/)** - Envio seguro para lixeira

### Build e Empacotamento
- **setuptools** - Sistema de build
- **wheel** - Criação de pacotes

### Bibliotecas Padrão Utilizadas
- `pathlib`, `shutil`, `os` - Manipulação de arquivos e diretórios
- `json` - Persistência de configurações
- `argparse` - Parsing de argumentos CLI
- `typing` - Tipagem estática

---

## Configuração

### Arquivo de Extensões (extensions.json)
```json
{
  "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
  "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Vídeos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
  "Compactados": [".zip", ".rar", ".7z", ".tar.gz"]
}
```

### Configuração de Build (pyproject.toml)
O projeto inclui configuração completa para empacotamento via setuptools, com entrypoint configurado como `ryzor = src.cli:main`.

---

## Testes

### Geração de Arquivos de Teste
```bash
# Execute o gerador de arquivos de teste
python tests/generator.py
```

### Status de Testes
- ⚠️ **Testes automatizados:** Não implementados
- ✅ **Testes manuais:** Via generator.py
- 🔄 **Roadmap:** Implementação de testes unitários e de integração planejada

---

## Segurança e Limitações

### Considerações de Segurança
- Sem autenticação ou controle de acesso
- Dependências externas podem ter vulnerabilidades se desatualizadas
- Operações de arquivo requerem permissões adequadas do sistema

### Limitações Conhecidas
- Falta de validação robusta de inputs do usuário
- Sem tratamento avançado de erros para cenários extremos
- Persistência limitada a arquivos JSON (não escalável para grandes volumes)

---

## Troubleshooting

### Problemas Comuns

**Módulos não encontrados:**
```bash
ryzor repair
```

**Dependências não instaladas:**
```bash
pip install -r requirements.txt

# ou

ryzor repair --dependences ou -dp
```

**Erros de permissão:**
- Execute como usuário com permissões adequadas
- Verifique permissões de leitura/escrita nos diretórios

**Arquivos de configuração corrompidos:**
```bash
ryzor repair --config ou -cfg
```

---

## Roadmap

### Prioridade Alta
1. ✅ **Implementar testes automatizados**
2. ✅ **Melhorar validação de inputs do usuário**
3. ✅ **Documentação externa completa**

### Prioridade Média
4. **Automatizar processo de deploy e CI/CD**
5. **Suporte a plugins/extensões personalizadas**
6. **Interface web complementar**

### Prioridade Baixa
7. **Internacionalização (i18n)**
8. **Integração com serviços de nuvem**
9. **Modo daemon para monitoramento contínuo**

---

## Contribuição

### Como Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Código
- Siga o padrão **PEP8** para formatação
- Adicione testes para novas funcionalidades
- Documente suas alterações adequadamente
- Use type hints sempre que possível

---

## Status do Projeto

### Estado Atual
- ⚠️ **Desenvolvimento ativo** - Versão intermediária funcional
- ❌ **Não pronto para produção**
- ✅ **Funcionalidades core implementadas**
- ⚠️ **Falta de testes automatizados**

### Estabilidade
- **Core CLI:** Estável
- **Operações de arquivo:** Estável com limitações
- **Interface Rich:** Estável
- **Configuração JSON:** Estável

---

## Licença

Este projeto ainda não possui uma licença definida. Considere definir uma licença apropriada antes de releases públicas.

---

## Suporte

Para reportar bugs, solicitar features ou obter ajuda:
- 📧 **Issues:** Use o sistema de issues do GitHub
- 📖 **Documentação:** Consulte este README e a documentação técnica
- 🔧 **Troubleshooting:** Consulte a seção de resolução de problemas acima

---

*Ryzor - Organize seus arquivos com estilo e eficiência.*
