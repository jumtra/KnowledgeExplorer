from dataclasses import dataclass, field

from doc_explanation.common.remove_noise import remove_noise

from .document import Document
from .preprocess import split_markdown_in_topic_chunks


@dataclass
class ChunkedSentence:
    """チャンクされた文章を保存するデータクラス"""

    title: str
    body: str
    num: int
    count: int
    file_name: str

    def __post_init__(self):
        self.text = remove_noise(self.body)
        self.meta = self.title + "<sep>" + self.body
        self.div, self.title = self.title.split(" - ")


@dataclass
class Sentence:
    """検索ワードを含む文章を保存するデータクラス"""

    list_words: list[str]
    list_doc: list[Document]
    list_sentence: list[ChunkedSentence] = field(default_factory=list)
    is_not_exist: bool = True

    def __post_init__(self):
        list_target_text = []
        if len(self.list_doc) == 0:
            return
        for doc in self.list_doc:
            for num, chunked_sentence in enumerate(split_markdown_in_topic_chunks(doc.contents)):
                title = chunked_sentence["title"]
                body = chunked_sentence["body"]
                count = self.count_words(title=title, body=body)
                if count > 0:
                    file_name = doc.path_file.split("/")[-1]
                    list_target_text.append(ChunkedSentence(title=title, body=body, file_name=file_name, num=num, count=count))
        self.list_sentence = list_target_text
        if len(self.list_sentence) > 0:
            self.is_not_exist = False

    def count_words(self, title: str, body: str) -> int:
        """文中の検索ワード数の含まれる数を数える"""
        count = 0
        for word in self.list_words:
            count += title.count(word)
            count += body.count(word)
        return count
