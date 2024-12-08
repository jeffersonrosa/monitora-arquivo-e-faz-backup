import os
import sys
import logging
from datetime import datetime
import time
from threading import Thread

import backup_manager
import file_monitor
import utils

from rich.logging import RichHandler

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# Fallback baseado em loop (checando a cada X segundos) para casos em que o watchdog não detecta:
ENABLE_FALLBACK_CHECK = True
FALLBACK_INTERVAL = 10  # segundos

class BrazilianFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime("%d/%m/%Y|%H:%M:%S|")

formatter = BrazilianFormatter("%(message)s")
handler = RichHandler(markup=True, rich_tracebacks=True)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)

def create_default_config():
    default_config = {
        "last_monitored_file": "",
        "backup_directory": "",
        "number_of_backups": 3
    }
    utils.save_config(CONFIG_PATH, default_config)
    return default_config

def choose_file():
    """Função para interagir com o usuário e escolher um arquivo."""
    choice = input("Deseja digitar o caminho completo do arquivo (C) ou escolher a partir de uma pasta (P)? ").strip().lower()
    if choice == 'c':
        file_path = input("Informe o caminho completo do arquivo a monitorar: ").strip()
        if not utils.file_exists(file_path):
            logger.error("Arquivo informado não existe. Encerrando.")
            sys.exit(1)
        return file_path
    elif choice == 'p':
        folder_path = input("Informe o caminho da pasta: ").strip()
        if not os.path.isdir(folder_path):
            logger.error("A pasta informada não existe. Encerrando.")
            sys.exit(1)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            logger.error("Não há arquivos nessa pasta.")
            sys.exit(1)
        print("Arquivos disponíveis:")
        for i, f in enumerate(files, start=1):
            print(f"{i}. {f}")
        while True:
            try:
                num = int(input("Digite o número do arquivo a monitorar: ").strip())
                if 1 <= num <= len(files):
                    chosen_file = os.path.join(folder_path, files[num-1])
                    return chosen_file
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida.")
    else:
        print("Opção inválida. Tente novamente.")
        return choose_file()

def interactive_setup(config):
    logger.info("Carregando configurações...")

    last_file = config.get("last_monitored_file", "")
    backup_dir = config.get("backup_directory", "")
    num_backups = config.get("number_of_backups", 3)

    # Se existe um último arquivo e ele é válido
    if last_file and utils.file_exists(last_file):
        print(f"Último arquivo monitorado: {last_file}")
        resp = input("Deseja continuar monitorando este arquivo? (S/n) ").strip().lower()
        if resp == 'n':
            # Escolhe um novo arquivo
            last_file = choose_file()
    else:
        if not last_file:
            print("Nenhum arquivo configurado anteriormente.")
        last_file = choose_file()

    print("Deseja usar a pasta padrão 'backup' no mesmo diretório do arquivo monitorado?")
    resp = input("(S para usar a padrão, N para especificar outra pasta): ").strip().lower()
    if resp == 'n':
        # Pede o nome da pasta, que será criada ao lado do arquivo monitorado
        backup_name = input("Digite o nome da pasta de backup (será criada no mesmo diretório do arquivo): ").strip()
        parent_dir = os.path.dirname(last_file)
        custom_backup = os.path.join(parent_dir, backup_name)
        backup_dir = backup_manager.ensure_backup_dir(custom_backup)
    else:
        backup_dir = os.path.join(os.path.dirname(last_file), "backup")
        backup_dir = backup_manager.ensure_backup_dir(backup_dir)

    print(f"Quantidade atual de backups armazenados: {num_backups}")
    resp = input("Deseja alterar a quantidade de backups? (S/n) ").strip().lower()
    if resp == 's':
        try:
            new_num = int(input("Digite a nova quantidade de backups: ").strip())
            if new_num > 0:
                num_backups = new_num
        except ValueError:
            logger.error("Valor inválido. Mantendo a quantidade anterior.")

    config["last_monitored_file"] = last_file
    config["backup_directory"] = backup_dir
    config["number_of_backups"] = num_backups
    utils.save_config(CONFIG_PATH, config)
    return config

def fallback_check(monitored_file, backup_dir, num_backups, extension):
    """Fallback: Checa periodicamente se o arquivo mudou e faz backup se necessário."""
    logger.info("Fallback de checagem ativado. Verificando alterações no arquivo periodicamente.")
    last_mtime = os.path.getmtime(monitored_file)
    while True:
        time.sleep(FALLBACK_INTERVAL)
        # Verifica se o arquivo ainda existe
        if not utils.file_exists(monitored_file):
            logger.error("Arquivo monitorado não existe mais. Encerrando fallback.")
            break
        current_mtime = os.path.getmtime(monitored_file)
        if current_mtime != last_mtime:
            logger.info("Detectada alteração (fallback). Criando backup...")
            backup_path = backup_manager.create_backup(monitored_file, backup_dir)
            logger.info(f"Backup criado: {backup_path}")
            backup_manager.rotate_backups(backup_dir, num_backups, extension)
            logger.info("Backups rotacionados.")
            last_mtime = current_mtime

def main():
    config = utils.load_config(CONFIG_PATH)
    if not config:
        logger.info("Nenhum arquivo de configuração encontrado. Criando configuração padrão.")
        config = create_default_config()

    config = interactive_setup(config)

    monitored_file = config["last_monitored_file"]
    backup_dir = config["backup_directory"]
    num_backups = config["number_of_backups"]

    if not utils.file_exists(monitored_file):
        logger.error("Arquivo monitorado não existe. Encerrando.")
        sys.exit(1)

    backup_manager.ensure_backup_dir(backup_dir)

    _, extension = os.path.splitext(monitored_file)
    if not extension:
        extension = ""

    logger.info(f"Monitorando: {monitored_file}")
    logger.info(f"Backups em: {backup_dir}")
    logger.info(f"Armazenar até {num_backups} backups.")
    logger.info("Use watchdog: True")
    logger.info(f"Extensão do arquivo monitorado: {extension}")

    # Inicia o watchdog em uma thread separada
    watchdog_thread = Thread(target=file_monitor.start_watchdog, args=(monitored_file, backup_dir, num_backups, logger, extension), daemon=True)
    watchdog_thread.start()

    if ENABLE_FALLBACK_CHECK:
        fallback_check(monitored_file, backup_dir, num_backups, extension)
    else:
        watchdog_thread.join()

if __name__ == "__main__":
    main()
