"""
 * NOME: Adenilton Ribeiro
 * DATA: 09/05/2025
 * PROJETO: Sistema de Inspeção de Pás Eólicas
 * VERSAO: 1.0.0
 * DESCRICAO: - Funções auxiliares reutilizáveis por múltiplos módulos
 *            - Formatação de timestamp, validações e logs
 *            - Organização de mensagens para depuração e diagnóstico
 * LINKS: - datetime (Python docs): https://docs.python.org/3/library/datetime.html
 *        - logging (Python docs): https://docs.python.org/3/library/logging.html
"""

# utils/helpers.py
import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

# ========================================================================================================
# Configurações do pendrive
PENDRIVE_NAME = "COMPOSITES"  # Nome do pendrive (label de volume)
PENDRIVE_MOUNT_POINT = f"/media/rasp/{PENDRIVE_NAME}"
PASTA_LOG_PENDRIVE = os.path.join(PENDRIVE_MOUNT_POINT, "data_logger")

# Mantém referência ao último logger para poder recriar
_last_logger = None

# ========================================================================================================
# Salvar a depuração e diagnóstico
def setup_logger(nome_arquivo_base="VCI_logger", pasta_log=PASTA_LOG_PENDRIVE, force_new=False):
    global _last_logger

    # Se já existe logger e não é para forçar novo, reaproveita
    if _last_logger and not force_new:
        return _last_logger

    # Cria pasta dos logs caso não exista
    # Cria pasta no pendrive (se existir)
    try:
        os.makedirs(pasta_log, exist_ok=True)
    except FileNotFoundError:
        logger.warning(f"Pendrive {PENDRIVE_MOUNT_POINT} nao esta montado!")
        pasta_log = "data_logger"  # fallback para pasta local
        os.makedirs(pasta_log, exist_ok=True)

    # Timestamp para o arquivo de log (ex: VCI_logger_2025-06-23_18-00-00.log)
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo_log = f"{nome_arquivo_base}_{agora}.log"
    caminho_log = os.path.join(pasta_log, nome_arquivo_log)

    # Cria um logger nomeado, separado do logger raiz
    logger = logging.getLogger("VCI")
    logger.setLevel(logging.DEBUG)  # capta tudo (DEBUG+)

    # Remove handlers antigos (caso já existam)
    logger.handlers.clear()

    # Formatter para arquivo (sem cor)
    formatter_arquivo = logging.Formatter(
        '%(asctime)s %(levelname)-8s | %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

    # Formatter colorido para console usando colorlog
    formatter_console = ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)-8s | %(message)s",
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG':    'bold_cyan',
            'INFO':     'bold_green',
            'WARNING':  'bold_yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_white,bg_red',
        }
    )

    # Handler arquivo grava tudo (INFO+)
    file_handler = logging.FileHandler(caminho_log, mode='a')
    file_handler.setLevel(logging.INFO)  # captura só INFO para arquivo
    file_handler.setFormatter(formatter_arquivo)
    logger.addHandler(file_handler)

    # Handler console só INFO+
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # sem DEBUG no console
    console_handler.setFormatter(formatter_console)
    logger.addHandler(console_handler)

    _last_logger = logger

    return logger