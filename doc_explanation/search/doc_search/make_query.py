import MeCab
from nltk.corpus import wordnet

__all__ = ["get_search_words"]


def extract_nouns(text):
    """文章から単語を抽出する関数"""
    mecab = MeCab.Tagger("-Ochasen")
    nouns = [line.split()[2] for line in mecab.parse(text).splitlines() if ("名詞" in line.split()[-1]) and ("非自立" not in line.split()[-1])]
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
    keywords = extract_nouns(text)

    n_2 = n_grams(keywords, 2)
    n_3 = n_grams(keywords, 3)

    if n_2 == n_3:
        return keywords
    search_words = n_2 + n_3
    return search_words
