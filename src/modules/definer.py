"""Arquivo responsável por geranciar o comando 'define' """

import json
from pathlib import Path
from typing import Iterable, List, Union

class Definer:
    def __init__(self):
        pass

    def _normalize_extensions_input(self, exts: Union[str, Iterable]) -> List[str]:
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

    def salvar_extensoes(self, data: dict[str, list[str]]):
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

    def ler_extensoes(self, ) -> dict[str, list[str]]:
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)

        with json_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        return data

    def escrever_extensoes(self, extensoes: dict[str, list[str]], overwrite: bool = False) -> bool:
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "extensions.json"

        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            try:
                data = self.ler_extensoes()

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
            print(f"[Ryzor] Erro de permissão: {e}")
            return False
        except Exception as e:
            print(f"[Ryzor] Erro inesperado ao escrever JSON: {e}")
            return False


    def definer(self, type_arg: Union[str, Iterable[str]], extensions_suported: Union[str, Iterable], overwrite: bool = False):
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

        exts = self._normalize_extensions_input(extensions_suported)

        data_to_add: dict[str, list[str]] = {}

        if len(tipos) == 1:
            
            data_to_add[tipos[0]] = exts
        elif len(tipos) == len(exts):
            
            for t, e in zip(tipos, exts):
                data_to_add[t] = [e] if isinstance(e, str) else list(e)
        else:
            for t in tipos:
                data_to_add[t] = list(exts)

        if self.escrever_extensoes(data_to_add, overwrite):
            print(f"[Ryzor] extensões {data_to_add} adicionadas com sucesso")
        else:
            print("[Ryzor] Falha ao salvar extensões")
