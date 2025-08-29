"""Arquivo principal do Ryzor"""

from pathlib import Path
import shutil as sh
import json
import os
from modules import definer as df
from logger import log, log_mudancas
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

            # Executa ação real
            if backup:
                _destino.parent.mkdir(parents=True, exist_ok=True)
                sh.copy2(_arquivo, _destino)
            else:
                _destino.parent.mkdir(parents=True, exist_ok=True)
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
    ) -> bool | None:
    
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
                yield arquivo.resolve(), contador  # Retorna arquivo e total atual
    
    # Chama a barra passando o generator como callback
    arquivos = barra_carregamento_com_callback(buscar_arquivos_generator, sep, verbose)
    
    if arquivos is None:
        exit()

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
 
        for arquivo in arquivos:
            pasta_destino = Path(saida / arquivo.suffix[1:])

            for tipo, extensoes in tipos_de_arquivos.items():
                if any(arquivo.suffix.lower().endswith(ext) for ext in extensoes):
                    pasta_destino = Path(saida / tipo)
                    break
            else:
                pasta_destino = Path(f"{saida}/Sem_Extensões")

            destino = pasta_destino / arquivo.name

            arquivos_a_mudar[str(arquivo)] = str(destino)
        log_mudancas(arquivos_a_mudar, sep, verbose=verbose, backup=backup)

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