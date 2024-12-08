import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import backup_manager

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, monitored_file, backup_dir, num_backups, logger, extension):
        super().__init__()
        self.monitored_file = monitored_file
        self.backup_dir = backup_dir
        self.num_backups = num_backups
        self.logger = logger
        self.extension = extension

    def _do_backup(self, reason="alteração"):
        self.logger.info(f"Detectada {reason} do arquivo. Criando backup...")
        backup_path = backup_manager.create_backup(self.monitored_file, self.backup_dir)
        self.logger.info(f"Backup criado: {backup_path}")
        backup_manager.rotate_backups(self.backup_dir, self.num_backups, self.extension)
        self.logger.info("Backups rotacionados.")

    def on_modified(self, event):
        if event.src_path == self.monitored_file:
            self._do_backup("alteração (on_modified)")

    def on_created(self, event):
        if event.src_path == self.monitored_file:
            self._do_backup("criação (on_created)")

    def on_any_event(self, event):
        # Loga todos os eventos para diagnóstico
        self.logger.info(f"Evento detectado pelo watchdog: {event.event_type} em {event.src_path}")

def start_watchdog(monitored_file, backup_dir, num_backups, logger, extension):
    dir_to_watch = os.path.dirname(monitored_file)
    handler = FileChangeHandler(monitored_file, backup_dir, num_backups, logger, extension)
    observer = Observer()
    observer.schedule(handler, path=dir_to_watch, recursive=False)
    observer.start()
    logger.info("Monitoramento iniciado com watchdog. Pressione Ctrl+C para parar.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
