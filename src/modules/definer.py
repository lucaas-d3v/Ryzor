"""Arquivo responsável por geranciar o comando 'define' """

import json
from pathlib import Path
from typing import Iterable, List, Union

class DefinitionManager:
    def __init__(self):
        pass

    def normalize_extensions_input(self, exts: Union[str, Iterable]) -> List[str]:
        """
        Garante que o input de extensões vire uma lista de strings correta.
        Aceita: lista, tupla, string '.xml', string '[".xml",".py"]' ou '.xml,.py'.
        """
        
        if isinstance(exts, (list, tuple)):
            return [str(x) for x in exts]
        
        if isinstance(exts, str):
            s = exts.strip()
        
            if (s.startswith("[") and s.endswith("]")):
                try:
                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return [str(x) for x in parsed]
                except Exception:
            
                    pass
            
            if "," in s:
                parts = [p.strip().strip('"').strip("'") for p in s.split(",") if p.strip()]
                return parts

            return [s]

        return [str(exts)]

    def save_extensions(self, data: dict[str, list[str]]):
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

    def read_extensions(self, json_path: Path) -> dict[str, list[str]]:
        base_dir = Path(__file__).parent
        
        if not json_path:
            JSON_PATH = base_dir / "data" / "extensions.json"

        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

        with JSON_PATH.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        return data

    def write_extensions(self, extensoes: dict[str, list[str]], overwrite: bool = False) -> bool:
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            try:
                data = self.read_extensions()

                if not isinstance(data, dict):
                    data = {}
            
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            add = {}
            for tipo, _extensoes in extensoes.items():
                # garante que _extensoes é lista
                novos = _extensoes if isinstance(_extensoes, list) else [ _extensoes ]
                if overwrite or (tipo not in data):
                    add[tipo] = novos
                else:
                    # mescla mantendo ordem e sem duplicatas
                    atuais = list(data.get(tipo, []))
                    for ext in novos:
                        if ext not in atuais:
                            atuais.append(ext)
                    add[tipo] = atuais

            data.update(add)

            with json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return True

        except PermissionError as e:
            print(f"[Ryzor] Permission error: {e}")
            return False
        except Exception as e:
            print(f"[Ryzor] Unexpected error writing JSON: {e}")
            return False


    def define_type(self, type_arg: Union[str, Iterable[str]], extensions_suported: Union[str, Iterable], overwrite: bool = False):
        """
        type_arg: string 'Codigos' ou lista de tipos ['Codigos','Imagens']
        extensions_suported: lista ou string que representa extensões
        exemplos válidos:
            - ".xml"
            - ".xml .py"  (se usar nargs='+')
            - '[".xml", ".py"]' (string JSON)
            - [".xml", ".py"]
        """

        if isinstance(type_arg, (list, tuple)):
            tipos = [str(t) for t in type_arg]
        else:
            tipos = [str(type_arg)]

        exts = self.normalize_extensions_input(extensions_suported)

        data_to_add: dict[str, list[str]] = {}

        if len(tipos) == 1:
            
            data_to_add[tipos[0]] = exts
        elif len(tipos) == len(exts):
            
            for t, e in zip(tipos, exts):
                data_to_add[t] = [e] if isinstance(e, str) else list(e)
        else:
            for t in tipos:
                data_to_add[t] = list(exts)

        if self.write_extensions(data_to_add, overwrite):
            print(f"[Ryzor] extensions {data_to_add} added successfully")
        else:
            print("[Ryzor] Failed to save extensions")