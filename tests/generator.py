"""Arquivo para geração de arquivos para teste rápido"""

import random as r                                      
import os as s  
import json
from pathlib import Path

def ler_extensoes() -> dict[str, list[str]]:
    base_dir = Path(__file__).parent
    json_path = base_dir / "data" / "extensions.json"

    json_path.parent.mkdir(parents=True, exist_ok=True)

    with json_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    return data


try:
    tipos_de_arquivos = ler_extensoes()
    tipos_de_arquivos = tipos_de_arquivos.values()

except:
    tipos_de_arquivos = [
    '.fx', '.ffx', '.rar', '.targz', '.mcpack', '.mcaddon', '.mcworld', '.py', '.cs', '.zip',
    '.7z', '.msi', '.exe','.txt', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods', '.csv', '.ppt', '.pptx', '.odp', '.pdf', '.xps', '.tex', '.ltx', '.rtf', '.md', '.html', '.htm', '.epub', '.mobi', '.log', '.json', '.xml','.ico', '.jpg', '.cur', '.jpeg', '.sfk', '.avif', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webm', '.webp', '.heic', '.heif', '.dds', '.exr', '.raw', '.svg', '.ai', '.eps', '.cdr','.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.wmv', '.3gp', '.mpg', '.ogv', '.m4v', '.mts', '.ts', '.divx',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.alac', '.aiff', '.opus', '.amr', '.dsd', '.pcm', '.aax', '.ra',
    '.veg', '.vf', '.aep', '.aepx', '.prproject', '.pproj', '.ppj', '.drp', '.db', '.fcpxml', '.fcpbundle', '.imovieproj', '.kdenlive', '.mlt', '.osp', '.xsed', '.vpr'
    ]

s.makedirs("/home/lucas2078/Ryzor/tests/arquivos", exist_ok=True)

for i in range(1, 10):
    with open(f"tests/arquivos/arquivo_{i}{r.choice(list(tipos_de_arquivos))}", "w") as w:
        w.write(" ")

else:
    print("feito")