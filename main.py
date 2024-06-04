from subprocess import PIPE, Popen
from loguru import logger


def run_core_file():
    try:
        Popen(args=["start", "python", "src/core/core.py"], shell=True, stdout=PIPE)
        return True
    except Exception as ex:
        logger.exception(ex)
        return False


if __name__ == "__main__":
    logger.info("Запуск основного приложения")
    if run_core_file():
        logger.info("Файл исполняется в отдельном терминале")
    else:
        logger.error("Что то поломалось")
else:
    logger.error("Данный файл не запускается как модуль")
    raise ModuleNotFoundError("")
