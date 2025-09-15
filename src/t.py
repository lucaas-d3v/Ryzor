from pprint import pprint
import pyperclip
from pathlib import Path
import os

# Verificar diretório atual e arquivos disponíveis
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:")
for file in os.listdir("."):
    if file.endswith(".py"):
        print(f"  {file}")

print("\n" + "-"*30 + "\n")

# Lista corrigida (adicionei .py no lister_manager)
a = ["definer.py", "file_manager.py", "lister_manager.py", "logger.py", "remover.py", "repair_manager.py", "utils.py"]

contents = ""
for i in a:
    try:
        with open("src/modules/" + i, "r", encoding="utf-8") as f:
            content = f.read()
            contents += "f\n\n{'-' * 10}\n\n" + f"arquivo: {i}\n\n" + content + f"\n\n{'-' * 10}\n\n"
        print(f"✓ Lido: {i}")
    except FileNotFoundError:
        print(f"✗ Não encontrado: {i}")

print(contents)
pyperclip.copy(contents)