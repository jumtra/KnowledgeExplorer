import fire
import gradio as gr
from knowledge_explorer import knowledge_explorer


def clear():
    return None, None


def submit(question, data_path, max_doc, max_results, generate_num):
    text = knowledge_explorer(data_path=data_path, question=question, max_doc=max_doc, max_results=max_results, generate_num=generate_num)
    return text


def app():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
        ドキュメント説明AI
        """
        )
        question = gr.Textbox(label="質問", elem_id="input", placeholder="ドキュメントへの質問を入力してください。")
        data_path = gr.Textbox(label="フォルダパス", elem_id="data", placeholder="ドキュメントの絶対パスを指定してください。")
        with gr.Accordion(label="詳細な設定", open=False):
            max_doc = gr.Slider(minimum=1, maximum=20, value=10, step=1, label="回答に使用するドキュメントの最大数", interactive=True)
            max_results = gr.Slider(minimum=1, maximum=30, value=15, step=1, label="回答に使用する文章の最大数", interactive=True)
            generate_num = gr.Slider(minimum=1, maximum=5, value=1, step=1, label="回答の生成数", interactive=True)
        outputbox = gr.Textbox(label="出力", elem_id="outputbox")
        submit_btn = gr.Button("実行", variant="primary")
        clear_btn = gr.Button("リセット", variant="primary")

        submit_btn.click(fn=submit, inputs=[question, data_path, max_doc, max_results, generate_num], outputs=outputbox)
        clear_btn.click(fn=clear, inputs=None, outputs=[question, outputbox])

        demo.launch(server_name="0.0.0.0", share=False)


def main():
    fire.Fire(app())


if __name__ == "__main__":
    main()
