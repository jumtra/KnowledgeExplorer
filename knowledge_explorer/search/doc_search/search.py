from logging import getLogger
from pathlib import Path

from knowledge_explorer.common.read_md import read_md

from .document import Document, SearchedDocument
from .sentence import Sentence

logger = getLogger(__name__)


def doc_search(path_folder: str, list_words: list[str], max_doc: int) -> SearchedDocument:
    """path_folderから検索クエリを含むmdファイルを抽出"""

    logger.info("ドキュメントを検索")
    list_docs = []
    for path_file in Path(path_folder).glob("**/*.md"):
        docs = read_md(path_file)
        count = 0
        is_target = False
        for word in list_words:
            if word in docs:
                logger.info(f"検索対象に{path_file}を追加")
                count += docs.count(word)
                is_target = True
        list_docs.append(Document(contents=docs, path_file=str(path_file), count=count, is_target=is_target))

    logger.info("検索終了")
    return SearchedDocument(list_docs=list_docs, max_docs=max_doc)


def sentence_search(path_folder: str, list_words: list[str], max_doc: int = 5) -> Sentence:
    """"""

    searched_doc = doc_search(path_folder=path_folder, list_words=list_words, max_doc=max_doc)
    sentence = Sentence(list_words=list_words, list_doc=searched_doc.list_top_docs)
    return sentence
