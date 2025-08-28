"""Arquivo principal do Ryzor"""

from pathlib import Path
import shutil as sh
import json
import os
from modules import definer as df
from logger import log
from logger import barra_carregamento_com_callback    

def continuar(y: bool = False) -> bool:
    """
    Para evitar chamadas duplicadas, criei continuar() para perguntar ao usuário se quer confirmar a ação.
    """

    if y:
        return True

    aproveds = ["y", "s", "yes", "sim", "ok"]
    
    log("Deseja continuar? (s/n): ", code=10, end="")
    c = input().lower().strip()

    return c in aproveds

sep = os.sep  # pega separador do sistema

def execute(mudancas: dict[str, str], callback=None, backup:bool = False, verbose:bool =False):
    """
    Executa copiar/mover arquivos de acordo com o dicionário mudancas.
    """

    try:
        total = len(mudancas)
            
        for i, (arquivo, destino) in enumerate(mudancas.items(), start=1):
            _arquivo = Path(arquivo)
            _destino = Path(destino)

            if _arquivo.resolve() == _destino.resolve():
                continue

            # Criar diretório de destino se não existir
            _destino.parent.mkdir(parents=True, exist_ok=True)

            # Executa ação real
            if backup:
                sh.copy2(_arquivo, _destino)
            else:
                sh.move(_arquivo, _destino)

            # CRÍTICO: Chamar callback APÓS a operação
            if callback:
                callback(
                    atual=i,
                    total=total,
                    nome_arquivo=_destino.name,
                    acao="Copiando" if backup else "Movendo"
                )

        return True

    except Exception as e:
        print(f"[DEBUG] Erro em execute: {e}")
        return False

def realocate_files(
        entrada: Path, saida: Path,
        backup: bool = False,
        no_preview: bool = False,
        verbose: bool = False,
        y: bool = False
    ) -> bool:
    
    """ Função principal, papel: fazer backup/organizar os arquivo
    Função principal do Ryzor

    args:
        entrada: caminho de entrada dos arquivos a serem organizados/backup.
        saida: caminho de saída onde os arquivos seram levados ao fim do processo.
        backup: informa será feito o backup pu apenas organização.
        no_preview: informa se o usuário quer desativar o preview de tudo antes da ação.
        verbose: informa será o usuário quer ssber literalmente tudo, caminhos completos e demais.
        y: pré-responde sim para a ação escolhida.
        
    returns:
        retorna False caso o caminho seja um caminho ou n exista, etc, ou True caso tudo ocorra como esperado.
    """

    if not entrada.exists():
        """
        Medida de segurança caso o diretório informado não exista.
        """
        return False

    if not entrada.is_dir():
        """
        Medida de segurança caso o caminho especificado não seja um diretório.
        """
        return False

    if not saida.exists():
        """
        Medida de segurança caso a saida não exista.
        """
        saida.mkdir(parents=True, exist_ok=True)

    if not saida.is_dir():
        """
        Medida de segurança, caso a saida não seja um diretório.
        """
        return False

    def not_in_backup_folder(arquivo: Path) -> bool:
        return "backup" not in [p.lower() for p in arquivo.parts[:-1]]
    
    def buscar_arquivos_generator():
        '''Generator que faz a busca real dos arquivos'''
        contador = 0
        for arquivo in entrada.rglob("*"):
            if arquivo.is_file() and not_in_backup_folder(arquivo):
                contador += 1
                yield arquivo, contador  # Retorna arquivo e total atual
    
    # Chama a barra passando o generator como callback
    arquivos = barra_carregamento_com_callback(buscar_arquivos_generator)
    
    try:
        arquivos_a_mudar = {}

        try:
            tipos_de_arquivos = df.ler_extensoes()

        except (FileNotFoundError, json.JSONDecodeError) as e:
            log(f"Erro ao carregar JSON: {e}", code=9)
            return False

        if not isinstance(tipos_de_arquivos, dict):
            log("JSON não é um dicionário válido", code=9)
            return False

        if not verbose:
            log(f"Começando em {entrada.resolve()} ...", code=4)  # CORREÇÃO 2: Mostrar entrada, não cwd()
            log(f"Modo: {'Backup' if backup else 'Organização'}", code=10)
            log(f"Total de modificaçoes: {len(arquivos)}", code=8)  # CORREÇÃO 3: Remover +1
            log(f"\t    Atual {'-' * 17} Pós-mudanças\n", code=11) if not no_preview else print()

        else:
            log(f"Começando em {entrada} ...", code=4)
            log(f"Modo: {'Backup' if backup else 'Organização'}", code=10)
            log("Verbose: On", code=10)
            log(f"Total de modificaçoes: {len(arquivos)}", code=8)  # CORREÇÃO 3: Remover +1
            log(f"\t    Atual {'-' * 17} Pós-mudanças\n", code=11) if not no_preview else print()

        for arquivo in arquivos:
            pasta_destino = Path(saida / arquivo.suffix[1:])

            for tipo, extensoes in tipos_de_arquivos.items():
                if any(arquivo.suffix.lower().endswith(ext) for ext in extensoes):
                    pasta_destino = Path(saida / tipo)
                    break
            else:
                pasta_destino = Path(f"{saida}/Sem_Extensões")

            pasta_destino.mkdir(parents=True, exist_ok=True)
            destino = pasta_destino / arquivo.name

            # CORREÇÃO 4: Simplificar - não precisa repetir código para backup/organização
            if not no_preview:
                if verbose:
                    log(f"{arquivo} -> {destino}")
                else:
                    log(f"{sep.join(arquivo.parts[-2:])} -> {sep.join(destino.parts[-2:])}")

            arquivos_a_mudar[str(arquivo)] = str(destino)

        # CORREÇÃO 5: Mover else para fora do for loop
        if continuar(y):
            from logger import barra_progresso
            barra_progresso(arquivos_a_mudar, backup=backup)
            return True
        else:
            log("Cancelando...", code=10)
            return False

    except Exception as e:
        log(f"Erro: {e}", code=9)
        return False