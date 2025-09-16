![Logo do Ryzor](assets/Ryzor_Banner.png)  
  
---

###Ryzor

Ryzor is a command-line (CLI) tool for organizing, backing up, and managing files by type/extension. The project is under development and is not ready for production use.


---

###Overview

Main goal: Automate organization and backup of files in directories, categorizing them by user-defined types/extensions.

Current features:

Define and edit file types/extensions

Organize and perform backups of files between directories

List files and extensions with recursive mode

Remove types/extensions with preview

Repair and restore default configurations

Rich CLI interface with visual feedback using Rich

Progress bar and detailed logs


Data persistence: JSON files (extensions.json) store the type and extension definitions.



---

###Installation

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

###Manual installation

# Install only the dependencies
pip install rich==13.9.4 pyfiglet==0.8.post1 send2trash==1.8.3

# Run via Python
ryzor repair --dependences or -dp


---

###Project Structure

.
├── pyproject.toml           # Project and build configuration
├── requirements.txt         # Dependencies
├── README.md                # Main documentation
├── src/
│   ├── cli.py               # CLI entry point
│   ├── t.py                 # Utility script
│   ├── modules/
│   │   ├── definer.py       # Definitions management
│   │   ├── file_manager.py  # File operations
│   │   ├── lister_manager.py# File listing
│   │   ├── logger.py        # Interface and logging
│   │   ├── remover.py       # Remove types/extensions
│   │   ├── repair_manager.py# Restore/repair
│   │   ├── utils.py         # General utilities
│   │   └── data/
│   │       └── extensions.json
│   ├── data/
│   │   └── extensions.json  # Extensions configurations
│   └── protected/
│       └── extensions_default.json # Default backup
└── tests/
    └── generator.py         # Test files generator


---

###Available Commands

File Organization

# Organize files by type
ryzor organize -p ./my_files -d ./organized

# Organize with recursive mode
ryzor organize -p ./source -d ./destination --recursive

Types/Extensions Management

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

###Main Dependencies

Runtime

Python 3.11+ (required)

Rich 13.9.4 - Rich terminal interface

pyfiglet 0.8.post1 - ASCII banner generation

send2trash 1.8.3 - Safe move to trash


###Build and Packaging

setuptools - Build system

wheel - Package creation


###Standard Libraries Used

pathlib, shutil, os - File and directory manipulation

json - Configuration persistence

argparse - CLI argument parsing

typing - Static typing



---

###Configuration

Extensions File (extensions.json)

{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
  "Archives": [".zip", ".rar", ".7z", ".tar.gz"]
}

Build Configuration (pyproject.toml)

The project includes a full configuration for packaging via setuptools, with entrypoint configured as ryzor = src.cli:main.


---

###Tests

Test Files Generation

# Run the test files generator
python tests/generator.py

Test Status

⚠️ Automated tests: Not implemented

✅ Manual tests: Via generator.py

🔄 Roadmap: Unit and integration tests planned



---

Security and Limitations

Security Considerations

No authentication or access control

External dependencies may have vulnerabilities if outdated

File operations require appropriate system permissions


Known Limitations

Lack of robust validation for user inputs

No advanced error handling for extreme scenarios

Persistence limited to JSON files (not scalable for large volumes)



---

###Troubleshooting

Common Issues

Module not found:

ryzor repair

Dependencies not installed:

pip install -r requirements.txt

# or

ryzor repair --dependences or -dp

Permission errors:

Run as a user with appropriate permissions

Check read/write permissions on directories


Corrupted configuration files:

ryzor repair --config or -cfg


---

###Roadmap

High Priority

1. ✅ Implement automated tests


2. ✅ Improve user input validation


3. ✅ Complete external documentation



###Medium Priority

4. Automate deploy and CI/CD process


5. Support for custom plugins/extensions


6. Complementary web interface



###Low Priority

7. Internationalization (i18n)


8. Integration with cloud services


9. Daemon mode for continuous monitoring




---

###Contribution

How to Contribute

1. Fork the repository


2. Create a branch for your feature (git checkout -b feature/new-feature)


3. Commit your changes (git commit -am 'Adds new feature')


4. Push to the branch (git push origin feature/new-feature)


5. Open a Pull Request



Code Standards

Follow PEP8 formatting

Add tests for new features

Document your changes properly

Use type hints whenever possible



---

###Project Status

Current State

⚠️ Active development - Intermediate functional version

❌ Not production ready

✅ Core features implemented

⚠️ Lack of automated tests


###Stability

Core CLI: Stable

File operations: Stable with limitations

Rich interface: Stable

JSON configuration: Stable



---

###License

This project does not currently have a defined license. Consider adding an appropriate license before public releases.


---

###Support

To report bugs, request features, or get help:

📧 Issues: Use the GitHub issues system

📖 Documentation: Refer to this README and technical docs

🔧 Troubleshooting: See the troubleshooting section above



---

Ryzor — Organize your files with style and efficiency.

