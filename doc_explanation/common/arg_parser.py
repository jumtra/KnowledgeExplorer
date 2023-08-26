from argparse import ArgumentParser


def common_parser() -> ArgumentParser:
    """main.pyで使用するargparser"""
    parser = ArgumentParser(description="src/main.pyで使用するargparser")
    parser.add_argument("--data_path", type=str, default="data/sample", help="ドキュメントが存在するディレクトリの絶対パスを指定")
    parser.add_argument("--question", type=str, default="データ品質向上のために取り組んでいることについて教えてください。", help="質問内容")
    parser.add_argument("--max_results", type=int, default=None, help="検索結果から参照する最大文章数")
    parser.add_argument("--max_doc", type=int, default=None, help="検索結果から参照する最大ドキュメント数")
    parser.add_argument("--generate_num", type=int, default=None, help="回答の生成数")

    return parser.parse_args()
