import re
import unicodedata


def remove_noise(text: str) -> str:
    """ノイズ除去"""
    text = re.sub(r"【.*】", "", text)
    text = re.sub(r"（.*）", "", text)
    text = re.sub(r"「.*」", "", text)
    text = re.sub(r"[［］\[\]]", " ", text)  # ［］の除去
    text = re.sub(r"[@＠]\w+", "", text)  # メンションの除去
    text = re.sub(r"https?:\/\/.*?[\r\n ]", "", text)  # URLの除去
    text = re.sub(r"　", " ", text)  # 全角空白の除去
    text = text.replace("\u200b", "")
    text = text.replace("/", "")
    text = text.replace("\n", "")
    text = text.replace("-", "")
    text = text.replace(" ", "")
    text = remove_unicode(text = text)
    return text


def remove_unicode(text: str, form="NFKC") -> str:
    normalized_text = unicodedata.normalize(form, text)
    return normalized_text
