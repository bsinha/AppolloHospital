import gradio as gr
from chatEngine import healthBot

def medBot(message, history):
        print(history)
        return healthBot(message=message)

gr.ChatInterface(
    medBot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me any question related to Appollo Hospital", container=False, scale=7),
    title="Appollo Hospital MedBot",
    description="Ask MedBot any question",
    theme="",
    examples=["Hello", "Tell me something about Serum test", "Do we have any medicinal report?"],
    cache_examples=True,
    retry_btn="Retry",
    undo_btn="Delete Previous",
    clear_btn="Clear",
    
).launch(share=True)