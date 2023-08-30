from pathlib import Path

from knowledge_explorer.answer.answer_format import format_return
from knowledge_explorer.answer.model.ctranslate import CtranslatedModel
from knowledge_explorer.answer.prompt import PROMPT
from knowledge_explorer.common.arg_parser import common_parser
from knowledge_explorer.common.config_manager import ConfigManager
from knowledge_explorer.common.log_handler import add_log_handler
from knowledge_explorer.search.doc_search.query import get_search_words
from knowledge_explorer.search.doc_search.search import sentence_search
from knowledge_explorer.search.vec_search.search import VectorSearch

__all__ = ["knowledge_explorer"]


def set_args(config_manager: ConfigManager, data_path: str, max_doc: int, max_results: int, generate_num: int) -> ConfigManager:
    config_manager.config.input.data_path = data_path
    if max_doc is not None:
        config_manager.config.search.doc_search.max_doc = max_doc
    if max_results is not None:
        config_manager.config.search.vec_search.max_results = max_results
    if generate_num is not None:
        config_manager.config.generate.generate_num = generate_num

    return config_manager


def knowledge_explorer(data_path: str, question: str, max_doc: int, max_results: int, generate_num: int) -> str:
    logger = add_log_handler(".")
    config_manager = ConfigManager.from_yaml(config_yaml_path="config.yaml", config_dir="knowledge_explorer/config")

    # set argparse
    config_manager = set_args(config_manager=config_manager, data_path=data_path, max_doc=max_doc, max_results=max_results, generate_num=generate_num)

    path_folder = Path(config_manager.config.input.data_path)
    logger.info(f"質問：{question}")
    list_words = get_search_words(question)

    # 早期リターン
    if len(list_words) == 0:
        return_text = "検索クエリを生成できませんでした。質問文章を変更してください。"
        logger.info(return_text)
        return return_text

    log_text = "検索クエリ："
    for word in list_words:
        log_text += word + " "
    logger.info(log_text)

    searched_sentences = sentence_search(path_folder=path_folder, list_words=list_words, max_doc=config_manager.config.search.doc_search.max_doc)

    # 早期リターン
    if searched_sentences.is_not_exist:
        return_text = "検索結果が存在しません。"
        logger.info(return_text)
        return return_text

    searched_vectors = VectorSearch(
        list_sentence=searched_sentences.list_sentence, embedding_model=config_manager.config.search.vec_search.embedding_model
    )

    list_result = searched_vectors.search_relevant_chunks(text=question, max_results=config_manager.config.search.vec_search.max_results)
    # 早期リターン
    if len(list_result) == 0:
        return_text = "質問の参考になる文章が存在しませんでした。"
        logger.info(return_text)
        return return_text

    list_result = [{"text": result.text, "num": result.num, "file_name": result.file_name} for result in list_result]
    list_text = [dict_result["text"] for dict_result in list_result]

    result = "".join([t + "\n" for t in list_text])

    # 回答生成
    model = CtranslatedModel(config_manager=config_manager)

    prompt = PROMPT.format(question=question, result=result)
    list_answer = []
    for _ in range(config_manager.config.generate.generate_num):
        text = model.generate(prompt=prompt).split("###回答:")[-1]
        if text != "":
            list_answer.append(text)
    logger.info(f"\n検索結果：{result}")

    if len(list_answer) == 0:
        return_text = "回答は生成されませんでした。"
        logger.info(f"\n回答：{return_text}")
        list_answer.append(return_text)

    else:
        for i, text in enumerate(list_answer):
            logger.info(f"\n回答{i}：" + text)

    return_text = format_return(question=question, list_answer=list_answer, list_result=list_result)
    logger.info(return_text)
    return return_text
