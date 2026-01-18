import gradio as gr
from dotenv import load_dotenv
from pyngrok import ngrok

from answer import answer_question

ngrok.set_auth_token("37chSt4EGeXgyS84vKF9xFxaIQr_5hWbDmuSWBbgT7MF3hCx3")

load_dotenv(override=True)


def format_context(context):
    result = "<h2 style='color: #ff7800;'>الدليل المرجعي للرد</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>المصدر: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result


def chat(history):
    last_message = history[-1]["content"]
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)


def main():
    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="خدمة العملاء اوتولاين", theme=theme) as ui:
        gr.Markdown("#سكرتير اوتولاين الذكي , بساعد بالمبيعات و جميع الأسءلة يلي تخص المكينات")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 المحادثة", height=600, type="messages", show_copy_button=True
                )
                message = gr.Textbox(
                    label="سؤالك",
                    placeholder="اسألني اي شي عن اوتولاين",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="المحتوى الدليلي المستخرج",
                    value="*الدليل المرجعي للرد *",
                    container=True,
                    height=600,
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    public_url = ngrok.connect(7860).public_url
    print(f"🔗 Public Link: {public_url}")

    ui.launch(inbrowser=True , auth=("autoline", "123456"))


if __name__ == "__main__":
    main()
