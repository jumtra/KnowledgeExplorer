import PySimpleGUI as sg

from knowledge_explorer import knowledge_explorer


def main():
    layout = [
        [sg.Text("ドキュメント説明AI")],
        [sg.Text("質問"), sg.InputText(key="question", size=(100, 1))],
        [sg.Text("フォルダパス"), sg.InputText(key="data_path")],
        [sg.Text("回答に使用するドキュメントの最大数"), sg.Slider(range=(1, 20), default_value=10, orientation="h", key="max_doc")],
        [sg.Text("回答に使用する文章の最大数"), sg.Slider(range=(1, 30), default_value=15, orientation="h", key="max_results")],
        [sg.Text("回答の生成数"), sg.Slider(range=(1, 5), default_value=1, orientation="h", key="generate_num")],
        [sg.Button("実行"), sg.Button("リセット")],
        [sg.Text("出力")],
        [sg.Output(size=(135, 20), key="output")],
    ]

    window = sg.Window("ドキュメント説明AI", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "実行":
            question = values["question"]
            data_path = values["data_path"]
            max_doc = int(values["max_doc"])
            max_results = int(values["max_results"])
            generate_num = int(values["generate_num"])

            if question and data_path:
                try:
                    output_text = knowledge_explorer(
                        data_path=data_path, question=question, max_doc=max_doc, max_results=max_results, generate_num=generate_num
                    )
                    window["output"].update(output_text)
                except Exception as e:
                    window["output"].update(f"エラーが発生しました。\n{e}")
        elif event == "リセット":
            window["question"].update("")
            window["max_doc"].update(5)
            window["max_results"].update(15)
            window["generate_num"].update(1)
            window["output"].update("")

    window.close()


if __name__ == "__main__":
    main()
