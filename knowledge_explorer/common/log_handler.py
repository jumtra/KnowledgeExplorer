from logging import FileHandler, Formatter, StreamHandler, getLogger
from pathlib import Path


def add_log_handler(output_dir):
    """
    同じログファイルに出力する'verbose_logger'と'simple_logger'という2種類のロガーを作成します。
    'verbose_logger'は実行時間、ログレベル、モジュール名、関数名とメッセージを出力するロガーです。

    Parameters
    ----------
    output_dir : ログファイルを配置するディレクトリ
    """
    verbose_fmt = Formatter("%(asctime)s %(levelname)-6s %(name)s %(lineno)d [%(funcName)s] %(message)s")
    verbose_logger = getLogger()
    verbose_logger.setLevel("DEBUG")
    handler = StreamHandler()
    handler.setFormatter(verbose_fmt)
    verbose_logger.addHandler(handler)
    log_file = Path(f"{output_dir}/main.log")
    if log_file.exists():
        try:
            log_file.unlink()
        except OSError as e:
            print(f"Error:{ e.strerror}")
    handler = FileHandler(log_file, mode="a", encoding="utf8")
    handler.setLevel("DEBUG")
    handler.setFormatter(verbose_fmt)
    verbose_logger.addHandler(handler)
    verbose_logger.info(f"log_file = {log_file}")
    return verbose_logger
