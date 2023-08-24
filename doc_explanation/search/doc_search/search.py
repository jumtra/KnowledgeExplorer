from dataclasses import dataclass, field
from pathlib import Path

from doc_explanation.common.read_md import read_md
from doc_explanation.search.vec_search.preprocess import split_markdown_in_topic_chunks


@dataclass
class Document:
    """ドキュメントの情報を格納するデータクラス"""

    contents: str
    count: int
    path_file: str
    is_target: bool


@dataclass
class SearchedDocument:
    """検索クエリを含むドキュメントを保存するデータクラス"""

    list_docs: list[Document]
    max_docs: int
    is_exist: bool = True

    def __post_init__(self):
        list_count = []
        list_docs = []
        for docs in self.list_docs:
            if docs.is_target:
                list_count.append(docs.count)
                list_docs.append(docs)
        self.list_docs = list_docs

        # 検索ワードを含むドキュメントが存在しない場合
        if len(list_count) == 0:
            self.is_exist = False
            return

        # 検索ワードを含むドキュメントがmax_docsよりも少ない場合
        if len(list_docs) <= self.max_docs:
            self.list_top_docs = list_docs
            return

        th_count = sorted(list_count)[self.max_docs - 1]
        list_top_docs = []
        for docs in self.list_docs:
            if docs.count >= th_count:
                list_top_docs.append(docs)
            if len(list_top_docs) >= self.max_docs:
                break
        self.list_top_docs = list_top_docs
        return


@dataclass
class ChunkedSentence:
    """チャンクされた文章を保存するデータクラス"""

    title: str
    body: str
    count: int

    def __post_init__(self):
        self.text = self.title +" - "+ self.body
        self.div = self.title.split(" - ")[0]


@dataclass
class Sentence:
    """検索ワードにを含む文章を保存するデータクラス"""

    list_words: list[str]
    list_doc: list[Document]
    list_sentence: list[ChunkedSentence] = field(default_factory=list)

    def __post_init__(self):
        list_target_text = []
        for doc in self.list_doc:
            for chunked_sentence in split_markdown_in_topic_chunks(doc.contents):
                title = chunked_sentence["title"]
                body = chunked_sentence["body"]
                count = self.count_words(title=title, body=body)
                if count > 0:
                    list_target_text.append(ChunkedSentence(title=title, body=body, count=count))
        self.list_sentence = list_target_text

    def count_words(self, title: str, body: str) -> int:
        """文中の検索ワード数の含まれる数を数える"""
        count = 0
        for word in self.list_words:
            count += title.count(word)
            count += body.count(word)
        return count


def doc_search(path_folder: str, list_words: list[str]) -> SearchedDocument:
    """path_folderからtextの内容を含むmdファイルを抽出"""

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
