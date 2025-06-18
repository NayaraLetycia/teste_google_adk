import time
import os
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurações
ARQUIVO_MONITORADO = 'dados.xlsx'
REPO_DIR = os.path.dirname(os.path.abspath(__file__))  # Pasta do repositório
GIT_REMOTE = 'origin'  # Nome do remote
GIT_BRANCH = 'main'    # Branch

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.basename(event.src_path) == ARQUIVO_MONITORADO:
            print(f"\n🔥 Arquivo {ARQUIVO_MONITORADO} alterado! Fazendo push...")
            try:
                repo = Repo(REPO_DIR)
                repo.git.add(ARQUIVO_MONITORADO)
                repo.index.commit("Auto-commit: dados.xlsx atualizado")
                origin = repo.remote(name=GIT_REMOTE)
                origin.push(GIT_BRANCH)
                print("✅ Push automático concluído! GitHub Actions será acionado.")
            except Exception as e:
                print(f"❌ Erro no push automático: {str(e)}")

if __name__ == "__main__":
    print(f"👀 Monitorando {ARQUIVO_MONITORADO} (Ctrl+C para sair)...")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=REPO_DIR)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer
