import gradio as gr

def medBot(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

gr.ChatInterface(
    medBot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),
    title="Appollo Hospital MedBot",
    description="Ask MedBot any question",
    theme="",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    retry_btn="Retry",
    undo_btn="Delete Previous",
    clear_btn="Clear",
    
).launch()