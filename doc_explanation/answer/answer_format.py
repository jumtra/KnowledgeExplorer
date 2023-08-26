def format_return(question: str, list_result, list_answer) -> str:
    return_text = f"質問：{question}" + "".join([f"\n回答{i+1}: " + text for i, text in enumerate(list_answer)])
    formatted_results = [
        f"\n検索結果{i+1}：" + """【参照元：{file_name}】{search_text}""".format(search_text=dict_result["text"], file_name=dict_result["file_name"])
        for i, dict_result in enumerate(list_result)
    ]
    return_text += "\n" + "-" * 10 + "検索結果" + "-" * 10 + "".join(formatted_results)
    return return_text
