"""Utils Module for Ryzor"""

from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import shutil as sh
import json
from typing import Optional

# pasta onde este módulo vive (src/modules)
MODULE_DIR = Path(__file__).resolve().parent

# tenta importar rich, mas não quebra se não existir
console = None
try:
    from rich.console import Console
    console = Console()
except Exception:
    console = None

class Utils:
    def __init__(self) -> None:
        super().__init__()

    def execute_changes(
        self,
        mudancas: dict[str, str],
        callback=None,
        backup: bool = False,
        verbose: bool = False,
        overwrite: bool = False,
        erro: bool = False,
    ):
        """
        Executa copiar/mover arquivos de acordo com o dicionário mudancas.
        Retorna (True, None) em sucesso ou (False, Exception) em falha.
        """
        try:
            total = len(mudancas)
            for i, (arquivo, destino) in enumerate(mudancas.items(), start=1):
                _arquivo = Path(arquivo)
                _destino = Path(destino)

                if _arquivo.resolve() == _destino.resolve():
                    continue

                _destino.parent.mkdir(parents=True, exist_ok=True)

                if backup:
                    sh.copy2(_arquivo, _destino)
                else:
                    # se overwrite == True, remove destino antes de mover
                    if overwrite and _destino.exists():
                        if _destino.is_dir():
                            sh.rmtree(_destino)
                        else:
                            _destino.unlink()
                    sh.move(_arquivo, _destino)

                if callback:
                    callback(
                        atual=i,
                        total=total,
                        nome_arquivo=_destino.name,
                        acao="Copying" if backup else "Moving",
                    )
            return True, None
        except Exception as e:
            return False, e

    @staticmethod
    def continue_action(mensagem: str = "Do you want to continue? (y/n): ", y: bool = False) -> bool:
        """
        Pergunta ao usuário se quer continuar. Se y=True, retorna True imediatamente.
        Usa busca binária no conjunto de respostas aprovadas.
        """
        if y:
            return True

        aproveds = [
    # Português (variações, gírias, abreviações)
    "sim", "s", "ss", "claro", "claroq", "claro!", "beleza", "beleza!", "belezaaa", "ok", "okey",
    "okey!", "ta", "tá", "tamo", "tamo junto", "tá bom", "vai", "vai sim", "pode", "pode sim",
    "pode crer", "pode crêr", "pode", "podee", "certo", "certinho", "combinado", "combina",
    "confirmo", "confirmado", "confirmada", "fechado", "fechou", "blz", "show", "show de bola",
    "de boa", "coé", "coé!", "simbora", "simbora!", "partiu", "tô dentro", "to dentro", "tô",
    "to", "okkk", "yess", "yesss",

    # English
    "yes", "y", "yeah", "yep", "yup", "sure", "sure!", "surething", "sure thing", "of course",
    "ofc", "definitely", "def", "absolutely", "abso", "affirmative", "roger", "roger that",
    "copy", "copy that", "10-4", "gotcha", "got it", "i'm in", "im in", "count me in", "sounds good",
    "works", "works for me", "okey dokey", "okeydokey", "okie", "okie dokie", "aye", "yass",
    "yasss", "bet", "fo sho", "fo' sho", "sureee", "yessir", "yesssss", "thumbs up", "👍",

    # Spanish
    "sí", "si", "sip", "s", "claro", "vale", "vale!", "vale sim", "por supuesto", "claro que sí",
    "claro que si", "de acuerdo", "ok", "okey", "dale", "dale!", "vamos", "va", "va bien", "sí señor",
    "sí señora", "sí claro", "sí sim",

    # French
    "oui", "ouais", "d'accord", "d accord", "bien sûr", "biensur", "ok", "ok!", "ça marche", "ca marche",
    "certainement", "absolument", "oui oui",

    # German
    "ja", "j", "klar", "klar!", "natürlich", "sicher", "ok", "okay", "jawohl", "einverstanden",

    # Italian
    "sì", "si", "certo", "va bene", "ok", "d'accordo", "sempre", "sissì", "sisi", "ovvio",

    # Russian (cyrillic + translit)
    "да", "da", "конечно", "konechno", "угу", "угу!", "ладно", "ладно!", "ок", "окей",

    # Japanese
    "はい", "hai", "うん", "un", "ええ", "ee", "もちろん", "mochiron", "了解", "りょうかい", "ryoukai",

    # Korean
    "네", "네!", "예", "예!", "응", "ㅇ", "ㅇㅇ", "그래", "geurae", "알겠어", "algesso",

    # Chinese (Mandarin simplified + pinyin)
    "是", "shì", "对", "对的", "duì", "好的", "hǎo de", "行", "xíng", "可以", "kěyǐ", "没问题", "méiwèntí",

    # Hindi
    "हाँ", "haan", "हां", "ha", "ठीक है", "theek", "ठीक", "thik", "बिलकुल", "bilkul", "जी", "ji",

    # Urdu
    "ہاں", "haan", "جی", "ji", "بالکل", "bilkul", "ٹھیک ہے", "theek hai",

    # Bengali
    "হ্যাঁ", "hya", "haan", "ঠিক আছে", "thik ache", "ঠিক", "thik",

    # Punjabi
    "ਹਾਂ", "haan", "ਜੀ", "ji", "ਠੀਕ ਹੈ", "theek hai",

    # Tamil
    "ஆம்", "aam", "ஆமாம்", "aamaam", "சரி", "sari", "அவை", "avai",

    # Telugu
    "అవును", "avunu", "సరే", "sare",

    # Malayalam
    "ആം", "aam", "ശരി", "shari", "സരി", "sari",

    # Gujarati
    "હા", "ha", "હાં", "haan", "સારું", "saru",

    # Thai
    "ใช่", "chai", "ได้", "dai", "โอเค", "ok", "ตกลง", "toklong",

    # Vietnamese
    "vâng", "vang", "đúng", "dung", "được", "duoc", "ok", "ok!", "ừ", "u",

    # Indonesian / Malay
    "ya", "iya", "iyah", "oke", "ok", "baik", "setuju", "sip", "boleh", "boleh!", "betul",

    # Turkish
    "evet", "evet!", "tamam", "tamam!", "olur", "olur!", "tabii", "peki",

    # Persian / Farsi
    "بله", "bale", "آره", "areh", "باشه", "bashe", "حتما", "hatman",

    # Arabic (several variants + translit)
    "نعم", "naʿam", "naam", "aywa", "awa", "ايه", "aiwa", "بلى", "bala", "تمام", "tamam", "حاضر", "hader",

    # Hebrew
    "כן", "ken", "בסדר", "beseder", "בהחלט", "behechlet", "אוקיי", "ok", "איי", "aye",

    # Swahili
    "ndio", "ndiyo", "sawa", "sawa!", "poa", "sipas", "hakuna matata", "sawa sawa",

    # Zulu / Xhosa / Afrikaans
    "yebo", "yebo!", "ja", "ja!", "nje", "siyavuma", "siyavuma!", "okay", "oke", "okei", "okeii",

    # Dutch
    "ja", "jaja", "ja!", "zeker", "zeker!", "oké", "oke", "goed", "goed!", "prima",

    # Polish
    "tak", "tak!", "jasne", "jasne!", "okej", "dobrze", "zgoda", "zgadzam się",

    # Czech / Slovak
    "ano", "ano!", "jasně", "jasne", "dobře", "ok", "souhlasím",

    # Hungarian
    "igen", "igen!", "rendben", "oké", "ok", "persze", "persze!", "természetesen",

    # Romanian
    "da", "da!", "bine", "bine!", "desigur", "sigur", "sigur!", "ok",

    # Greek
    "ναι", "nai", "ναι!", "nai!", "εντάξει", "entaksei", "βεβαίως", "vevaios",

    # Bulgarian / Serbian / Croatian / Bosnian
    "да", "da", "да!", "da!", "добре", "dobre", "у реду", "u redu", "ok", "okej",

    # Ukrainian
    "так", "tak", "так!", "tak!", "звісно", "zvisno", "ок", "ok",

    # Latvian / Lithuanian / Estonian
    "jā", "ja", "taip", "taip!", "taip", "ok", "gera", "gerai",

    # Filipino / Tagalog
    "oo", "oo!", "opo", "opo!", "sige", "sige!", "sige na", "sige na!", "ayos", "ayos!",

    # Catalan / Galician / Basque
    "sí", "si", "sí!", "si!", "d'acord", "dacord", "vale", "ok", "ondo", "aduna",

    # Irish / Scottish Gaelic / Welsh
    "sea", "sea!", "tha", "tha!", "ie", "ie!", "ie!", "ie", "ie!", "iee", "ieee", "ia",

    # Esperanto / Latin
    "jes", "sic", "ita", "ita vero", "certe", "certe!", "affirmo",

    # Hawaiian / Maori
    "ae", "ae!", "ō", "aeae", "āe", "ka pai", "ka pai!", "ok",

    # Haitian Creole / Patois
    "wi", "wi!", "ok", "oke", "dakò", "dako", "se vre", "se vre!",

    # Yiddish
    "יאָ", "yo", "yoy", "כן", "ken", "אַיי", "aye",

    # Central Asian languages (Kazakh, Uzbek, Azerbaijani variants)
    "иә", "ia", "ha", "ha!", "xa", "xa!", "xa xa",

    # Slang / informal / internet
    "yess", "yesss", "yepper", "yep!", "yah", "ya", "ya!", "yas", "yas!", "gotu", "got u",
    "im in", "i'm in", "countmein", "count me in", "on it", "on it!", "roger", "rogerthat", "10-4",
    "copied", "copied!", "okok", "okok!", "k", "kk", "kkk", "kk!", "kkk!", "mmhmm", "mmhm",
    "fine", "surebro", "surebro!", "solid", "solid!", "worksforme", "works for me", "goahead",
    "go ahead", "letsgo", "let's go", "let's do it", "lets do it", "i agree", "iagree",

    # Emojis / reactions (strings you may want to treat as "yes")
    "👍", "👌", "✅", "🤝", "🙌", "💯", "✔️",

    # Misc short affirmatives
    "y", "s", "o", "1", "ok!", "yes!", "si!", "da!", "oui!", "ja!", "hai!", "네!", "はい!",
]

        while True:
            try:
                # usa input com prompt direto (compatível com scripts)
                c = input(mensagem).lower().strip()
            except (KeyboardInterrupt, EOFError):
                # usuário cancelou via Ctrl+C/Ctrl+D
                return False

            if c == "":
                # repete a pergunta se vazio
                continue

            return Utils.binaria_search(aproveds, c)

    @staticmethod
    def binaria_search(lista: list[str], item: str) -> bool:
        """
        Busca binária simples numa cópia ordenada da lista.
        """
        lista_ordenada = sorted(lista)
        inicio = 0
        fim = len(lista_ordenada) - 1

        while inicio <= fim:
            meio = (fim + inicio) // 2
            if lista_ordenada[meio] == item:
                return True
            elif lista_ordenada[meio] > item:
                fim = meio - 1
            else:
                inicio = meio + 1

        return False

    @staticmethod
    def show_module_missing(module_name: Optional[str] = None, modules_names: Optional[list[str]] = None) -> None:
        """
        Prints missing module(s) message.
        """
        if modules_names:
            for module in modules_names:
                print("em show modules")
                print(f"[Debug] Error: Module {module} not found in ryzor files...")

            print("[Debug] Try `ryzor repair`")
            return

        if module_name:
            print(f"[Debug] Error: Module {module_name} not found in ryzor files, try `ryzor repair`")
        
        print("[Debug] Cancelling...")
        return

    def validate_modules(self) -> bool:
        """
        Verifica dependências externas e existência dos módulos internos sem importá-los,
        evitando import circular.
        """
        missing_modules: list[str] = []

        # checa pacote externo
        if importlib.util.find_spec("send2trash") is None:
            missing_modules.append("send2trash")

        # checa arquivos internos em src/modules (evita importar-os)
        expected_internal = ["definer.py", "file_manager.py", "logger.py", "utils.py"]
        for f in expected_internal:
            if not (MODULE_DIR / f).exists():
                missing_modules.append(f.replace(".py", ""))

        if not missing_modules:
            return True

        self.show_module_missing(modules_names=missing_modules)
        return False