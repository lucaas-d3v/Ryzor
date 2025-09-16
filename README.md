![Logo do Ryzor](assets/Ryzor_Banner.png)  

---

Ryzor

Ryzor is a command-line tool (CLI) for file organization, backup, and management by type/extension. The project is under development and not ready for production use.


---

Overview

Main goal: Automate file organization and backup into directories, categorizing them by user-defined types/extensions.

Current features:

Define and edit file types/extensions

Organize and back up files between directories

List files and extensions with recursive mode

Remove types/extensions with preview

Repair and restore default settings

Rich CLI interface with visual feedback using Rich

Progress bar and detailed logs


Data persistence: JSON files (extensions.json) store type and extension definitions.



---

Installation

Via pip (Recommended)

# Clone the repository
git clone https://github.com/lucaas-d3v/Ryzor
cd Ryzor

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .

# Use the command directly
ryzor help

Manual installation

# Install only dependencies
pip install rich==13.9.4 pyfiglet==0.8.post1 send2trash==1.8.3

# Run via Python
ryzor repair --dependences or -dp


---

Project Structure

.
├── pyproject.toml           # Project and build configuration
├── requirements.txt         # Dependencies
├── README.md                # Main documentation
├── src/
│   ├── cli.py               # CLI entry point
│   ├── t.py                 # Utility script
│   ├── modules/
│   │   ├── definer.py       # Type definitions management
│   │   ├── file_manager.py  # File operations
│   │   ├── lister_manager.py # File listing
│   │   ├── logger.py        # Interface and logging
│   │   ├── remover.py       # Type/extension removal
│   │   ├── repair_manager.py # Restore/repair
│   │   ├── utils.py         # General utilities
│   │   └── data/
│   │       └── extensions.json
│   ├── data/
│   │   └── extensions.json  # Extension configurations
│   └── protected/
│       └── extensions_default.json # Default backup
└── tests/
    └── generator.py         # Test file generator


---

Available Commands

File Organization

# Organize files by type
ryzor organize -p ./my_files -d ./organized

# Organize with recursive mode
ryzor organize -p ./source -d ./destination --recursive

Type/Extension Management

# Define new extensions for a type
ryzor define -t Images -exts .jpg .png .gif .webp

# List all defined extensions
ryzor list -e_exts

# List files in a directory
ryzor list -p ./my_files --verbose

# Remove extensions from a type
ryzor remove -t Images -exts .gif

# Remove entire type
ryzor remove -t "Unwanted Type" --no-preview -y

Repair and Maintenance

# Repair modules and configurations
ryzor repair


---

Main Dependencies

Runtime

Python 3.11+ (required)

Rich 13.9.4 - Rich terminal UI

pyfiglet 0.8.post1 - ASCII banner generation

send2trash 1.8.3 - Safe file deletion


Build & Packaging

setuptools - Build system

wheel - Package creation


Standard Libraries

pathlib, shutil, os - File and directory handling

json - Configuration persistence

argparse - CLI argument parsing

typing - Static typing



---

Configuration

Extensions File (extensions.json)

{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
  "Compressed": [".zip", ".rar", ".7z", ".tar.gz"]
}

Build Configuration (pyproject.toml)

The project includes full packaging setup with setuptools, with entrypoint configured as ryzor = src.cli:main.


---

Testing

Test File Generation

# Run the test file generator
python tests/generator.py

Test Status

⚠️ Automated tests: Not implemented

✅ Manual tests: Via generator.py

🔄 Roadmap: Unit and integration tests planned



---

Security & Limitations

Security Considerations

No authentication or access control

External dependencies may have vulnerabilities if outdated

File operations require proper system permissions


Known Limitations

Lacks robust user input validation

No advanced error handling for edge cases

Persistence limited to JSON files (not scalable for large datasets)



---

Troubleshooting

Common Issues

Modules not found:

ryzor repair

Dependencies not installed:

pip install -r requirements.txt

# or

ryzor repair --dependences or -dp

Permission errors:

Run as a user with appropriate permissions

Check read/write access to directories


Corrupted configuration files:

ryzor repair --config or -cfg


---

Roadmap

High Priority

1. ✅ Implement automated tests


2. ✅ Improve user input validation


3. ✅ Complete external documentation



Medium Priority

4. Automate deploy and CI/CD pipeline


5. Support for custom plugins/extensions


6. Complementary web interface



Low Priority

7. Internationalization (i18n)


8. Cloud service integration


9. Daemon mode for continuous monitoring




---

Contribution

How to Contribute

1. Fork the repository


2. Create a feature branch (git checkout -b feature/new-feature)


3. Commit your changes (git commit -am 'Add new feature')


4. Push to the branch (git push origin feature/new-feature)


5. Open a Pull Request



Code Standards

Follow PEP8 style guidelines

Add tests for new features

Properly document your changes

Use type hints whenever possible



---

Project Status

Current State

⚠️ Active development - Functional intermediate version

❌ Not production-ready

✅ Core features implemented

⚠️ Lack of automated tests


Stability

Core CLI: Stable

File operations: Stable with limitations

Rich interface: Stable

JSON configuration: Stable



---

License

This project does not yet have a defined license. Consider adding one before public releases.


---

Support

For bug reports, feature requests, or help:

📧 Issues: Use GitHub Issues system

📖 Documentation: Check this README and technical docs

🔧 Troubleshooting: See the troubleshooting section above



---

Ryzor - Organize your files with style and efficiency.