"""Arquivo para geração de arquivos para teste rápido"""

import random as r                                      
import os as s

extensoes = [".py", ".java", ".r", ".rs", ".js", ".cs", ".img", ".jpg"]
s.makedirs("tests/arquivos", exist_ok=True)

for i in range(1, 100):
    with open(f"tests/arquivos/arquivo_{i}{r.choice(extensoes)}", "w") as w:
        w.write(" ")

else:
    print("feito")