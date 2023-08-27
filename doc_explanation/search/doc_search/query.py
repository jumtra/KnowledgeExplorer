from logging import getLogger

from janome.tokenizer import Tokenizer
from nltk.corpus import wordnet

logger = getLogger(__name__)


def extract_nouns(text):
    """文章から単語を抽出する関数"""
    t = Tokenizer()
    nouns = [token.surface for token in t.tokenize(text) if "名詞" in token.part_of_speech and not "非自立" in token.part_of_speech]
    return nouns


def n_grams(lst: list[str], n: int) -> list[str]:
    """n_gramを作成する関数"""
    if len(lst) < n:
        return lst
    return ["".join(lst[i : i + n]) for i in range(len(lst) - n + 1)]


def extract_synonyms(word: str) -> set[str]:
    """同義語・類義語抽出関数"""
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)


def get_search_words(text: str) -> list[str]:
    """質問文から検索ワードを抽出する関数"""
    logger.info("検索クエリを生成")
    keywords = extract_nouns(text)

    n_2 = n_grams(keywords, 2)
    n_3 = n_grams(keywords, 3)
    n_4 = n_grams(keywords, 4)

    if len(n_2) == len(n_3) == len(n_4) == 0:
        return keywords

    search_words = keywords + n_2 + n_3 + n_4
    return search_words
