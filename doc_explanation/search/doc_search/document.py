from dataclasses import dataclass


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
