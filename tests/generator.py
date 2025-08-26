"""Arquivo para geração de arquivos para teste rápido"""

import random as r                                      
import os as s

tipos_de_arquivos = [
    '.fx', '.ffx', '.rar', '.targz', '.mcpack', '.mcaddon', '.mcworld', '.py', '.cs', '.zip',
    '.7z', '.msi', '.exe','.txt', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods', '.csv', '.ppt', '.pptx', '.odp', '.pdf', '.xps', '.tex', '.ltx', '.rtf', '.md', '.html', '.htm', '.epub', '.mobi', '.log', '.json', '.xml','.ico', '.jpg', '.cur', '.jpeg', '.sfk', '.avif', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webm', '.webp', '.heic', '.heif', '.dds', '.exr', '.raw', '.svg', '.ai', '.eps', '.cdr','.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.wmv', '.3gp', '.mpg', '.ogv', '.m4v', '.mts', '.ts', '.divx',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.alac', '.aiff', '.opus', '.amr', '.dsd', '.pcm', '.aax', '.ra',
    '.veg', '.vf', '.aep', '.aepx', '.prproject', '.pproj', '.ppj', '.drp', '.db', '.fcpxml', '.fcpbundle', '.imovieproj', '.kdenlive', '.mlt', '.osp', '.xsed', '.vpr'
    ]

s.makedirs("/home/lucas2078/Ryzor/tests/arquivos", exist_ok=True)

for i in range(1, 200):
    with open(f"tests/arquivos/arquivo_{i}{r.choice(tipos_de_arquivos)}", "w") as w:
        w.write(" ")

else:
    print("feito")