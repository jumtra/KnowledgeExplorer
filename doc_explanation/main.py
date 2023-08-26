from doc_explanation.answer.model.ctranslate import CtranslatedModel
from doc_explanation.answer.prompt import prompt2
from doc_explanation.common.config_manager import ConfigManager
from doc_explanation.search.doc_search.search import sentence_search
from doc_explanation.search.vec_search.search import VectorSearch

path_folder = "data/sample"
config_manager = ConfigManager.from_yaml(config_yaml_path="config.yaml", config_dir="doc_explanation/config")
question = "データ品質向上のために取り組んでいることを教えてください。"
s = sentence_search(path_folder=path_folder, text=question,max_doc = 5)

kb = VectorSearch(list_sentence=s.list_sentence, embedding_model="all-MiniLM-L6-v2")

list_result = kb.search_relevant_chunks(text=question, max_results=15)
list_text = [result.text for result in list_result]

result = "".join([t + "\n" for t in list_text])

model = CtranslatedModel(config_manager=config_manager)

prompt = prompt2.format(question=question, result=result)
text = model.generate(prompt=prompt)
print(f"質問：{question}")
print(f"\n検索結果：{result}")
print(f"\n回答：")
print(text.split("###回答:")[-1])
