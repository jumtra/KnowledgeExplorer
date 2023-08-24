import ctranslate2
import transformers

from doc_explanation.search.doc_search.search import sentence_search
from doc_explanation.search.vec_search.search import VectorSearch

path_folder = "data/test"
question = "データ品質向上のために取り組んでいることを教えてください。"
s = sentence_search(path_folder=path_folder, text=question)

kb = VectorSearch(list_sentence=s.list_sentence, embedding_model="all-MiniLM-L6-v2")

list_result = kb.search_relevant_chunks(text=question, max_results=15)
list_text = [result.text for result in list_result]

result = "".join([t + "\n" for t in list_text])

model_name = "rinna/japanese-gpt-neox-3.6b-instruction-ppo"
model_name = "rinna/bilingual-gpt-neox-4b-instruction-sft"
# model_name = "Jumtra/rinna-v1-tune-ep3"
ct2_model = "mymodel2"

generator = ctranslate2.Generator(ct2_model)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, use_fast=False)
prompt = """ユーザー：あなたは、提示された検索結果を元に、質問に対する回答を行うAIです。
次の質問に検索結果を参考に答えてください。
必ず検索結果の内容のみを用いて回答してください。

質問：プライバシー保護対策はどのように進められていますか？

検索結果：情報セキュリティ対策は、データの収集や提供を常に監視し、情報の機密性や完全性を確保するために実施されています。
検索結果には、個人情報を含む大量のデータが含まれる場合があり、このような情報の収集は、プライバシーとセキュリティのリスクを引き起こす可能性があります。
プライバシー保護対策の一環として、検索結果からの個人情報の収集を防止し、また、検索結果を加工する場合は、個人情報が完全に表示されないような手法を検討する必要があります。
プライバシー保護対策とデータ品質向上策を継続的に実施し、プロジェクト全体の信頼性を保つ努力も行っています。
また、データ品質や更新頻度の変化がクラスタリングやPCAの結果に与える影響を評価し、それに応じて戦略を微調整する検討も行っています。
情報セキュリティに関する専門的なスキルの向上を図るため、検索結果に関するトレーニングや研修を提供する組織やプロバイダーを特定し、そのような組織やプロバイダーから専門家の支援を受けることもできます。
また、個別の顧客情報を適切に保護するための方法や、プライバシーポリシーを策定するといった具体的な戦略を策定することもできます。


システム：情報セキュリティ対策は、データの収集や提供を監視し、情報の機密性や完全性を確保するための取り組みです。
大量のデータが含まれる場合、個人情報を含む可能性があり、これはプライバシーやセキュリティのリスクを引き起こす可能性があります。
プライバシー保護のためには、個人情報の収集を防止し、情報を加工する際には個人情報が表示されないような方法を検討する必要があります。
また、データ品質向上策としても取り組み、プロジェクト全体の信頼性を保つ努力が行われています。
さらに、クラスタリングやPCAの結果に影響を与える変化に対応するために戦略が微調整されています。
情報セキュリティのスキル向上を図るためには、関連する組織やプロバイダーからトレーニングや研修を受けることが可能です。
また、個別の顧客情報の保護方法やプライバシーポリシーの策定など、具体的な戦略を考えることも重要です。

ユーザー：
質問:
{question}
検索結果:
{result}
システム:""".format(
    question=question, result=result
)
tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(prompt, add_special_tokens=False))

results = generator.generate_batch(
    [tokens],
    max_length=2048,
    sampling_topk=50,
    sampling_temperature=0.8,
)

text = tokenizer.decode(results[0].sequences_ids[0])

print(f"質問：{question}")
print(f"\n検索結果：{result}")
print(f"\n回答：")
print(text.split("システム:")[-1])
