from dataclasses import dataclass, field
from pathlib import Path

from doc_explanation.common.read_md import read_md

from .document import Document, SearchedDocument
from .query import get_search_words
from .sentence import Sentence


def doc_search(path_folder: str, list_words: list[str]) -> SearchedDocument:
    """path_folderから検索クエリを含むmdファイルを抽出"""

    list_docs = []
    for path_file in Path(path_folder).glob("**/*.md"):
        docs = read_md(path_file)
        count = 0
        is_target = False
        for word in list_words:
            if word in docs:
                count += docs.count(word)
                is_target = True
        list_docs.append(Document(contents=docs, path_file=str(path_file), count=count, is_target=is_target))

    return SearchedDocument(list_docs=list_docs, max_docs=5)


def sentence_search(path_folder: str, text: str):
    """"""
    list_words = get_search_words(text)
    searched_doc = doc_search(path_folder=path_folder, list_words=list_words)

    sentence = Sentence(list_words=list_words, list_doc=searched_doc.list_top_docs)

    return sentence
