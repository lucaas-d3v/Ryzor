![Ryzor Logo](assets/Ryzor_Banner.png)

---

# Ryzor

**Ryzor** is a command-line tool (CLI) for **file organization, backup, and management** by type/extension.  
Focused on productivity and visual feedback (Rich). Still in development — **not production-ready**.

---

## Highlights
- Automatically organize files by user-defined types/extensions.
- Safe backup and preview before destructive operations.
- Rich terminal interface with progress bars and logs.
- Simple JSON-based configuration (`extensions.json`).

---

## Quickstart

```bash
# clone and install (recommended)
git clone https://github.com/lucaas-d3v/Ryzor
cd Ryzor
pip install -r requirements.txt
pip install .
```

Check available commands:
```bash
ryzor help
```

---

## Installation (detailed)

### pip (recommended)
```bash
git clone https://github.com/lucaas-d3v/Ryzor
cd Ryzor
pip install -r requirements.txt
pip install .
```

### Manual install (dependencies only)
```bash
pip install rich==13.9.4 pyfiglet==0.8.post1 send2trash==1.8.3
# run repair utilities
ryzor repair --dependences
```

> Tip: use a virtualenv to isolate dependencies.

---

## Usage — Examples

### Organize files
```bash
ryzor organize -p ./my_files -d ./organized
```

### Recursive mode
```bash
ryzor organize -p ./source -d ./dest --recursive
```

### Define extensions for a type
```bash
ryzor define -t Images -exts .jpg .png .gif .webp
```

### List extensions
```bash
ryzor list -e_exts
```

### Remove extension from a type (with preview)
```bash
ryzor remove -t Images -exts .gif
```

### Remove type without preview (force)
```bash
ryzor remove -t "Unwanted Type" --no-preview -y
```

### Repair configs / dependencies
```bash
ryzor repair
ryzor repair --config
ryzor repair --dependences
```

---

## Config file (extensions.json)
Simple structure mapping types to extensions:
```json
{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
  "Archives": [".zip", ".rar", ".7z", ".tar.gz"]
}
```

---

## Project structure
```
.
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   ├── cli.py
│   ├── t.py
│   ├── modules/
│   │   ├── definer.py
│   │   ├── file_manager.py
│   │   ├── lister_manager.py
│   │   ├── logger.py
│   │   ├── remover.py
│   │   ├── repair_manager.py
│   │   └── utils.py
│   └── data/
│       └── extensions.json
└── tests/
    └── generator.py
```

---

## Core dependencies
- Python 3.11+
- rich
- pyfiglet
- send2trash

(check `requirements.txt` for pinned versions).

---

## Tests
- Currently: **no automated tests implemented**.  
- Manual tests with `python tests/generator.py`.

---

## Security & Limitations
- File operations require caution (always check previews).
- JSON persistence (fine for local use, not scalable).
- Missing robust validation and testing (on roadmap).

---

## Roadmap (short-term)
- Add unit/integration tests
- Improve input validation
- CI workflow (GitHub Actions)
- Plugin system / cloud integrations

---

## Contributing
1. Fork → branch (`feature/x`) → commit → PR.
2. Follow PEP8, write tests, and document changes.
3. Use issues to discuss major proposals.

---

## License
This repository **does not yet have a license**.

---

## Support
- Open GitHub issues: https://github.com/lucaas-d3v/Ryzor

---

*Ryzor — organize your files with simplicity and safety.*
