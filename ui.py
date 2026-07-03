import gradio as gr

from app import execute_graph

def chat(query):
    execute_graph(query)

ui = gr.Interface(
    fn=chat,
    inputs=[gr.Textbox(lines=2, placeholder="Ask About news")],
    outputs=[gr.Textbox(lines=100)],
    title="Personal AI Assistant",
    description="Type anything you like",
)

ui.launch()