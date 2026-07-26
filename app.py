import gradio as gr
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from core.inference import InferenceEngine

engine = InferenceEngine()
history = []

def run_inference(agent, has_vote, has_quorum, query_text, uploaded_file):
    text = query_text.strip() if query_text else ""
    
    if uploaded_file is not None:
        try:
            text = uploaded_file.decode("utf-8")
        except:
            text = str(uploaded_file)
    
    if not text:
        text = f"{agent} може прийняти рішення"
    
    result = engine.infer(text)
    
    # Граф
    fig, ax = plt.subplots(figsize=(10, 5))
    G = nx.DiGraph()
    nodes = ["Запит", "Суб'єкт", "Голосування", "Кворум", result['result']]
    G.add_nodes_from(nodes)
    G.add_edges_from([
        ("Запит", "Суб'єкт"),
        ("Суб'єкт", "Голосування"),
        ("Голосування", "Кворум"),
        ("Кворум", result['result'])
    ])
    
    pos = nx.spring_layout(G, seed=42)
    node_colors = ["lightgray", "lightblue", "yellow", "orange", "#2ECC71" if "Дозволено" in result['result'] else "#E74C3C"]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2200, font_size=10, arrows=True, ax=ax)
    plt.title("Нормативний граф переходів")
    
    history.append(f"{datetime.now().strftime('%H:%M:%S')} | {agent} | {result['result']}")
    history_text = "\n".join(history[-10:])
    
    return result['result'], "\n".join(result['trace']), fig, history_text

with gr.Blocks(title="NormOS MVP") as demo:
    gr.Markdown("# ⚖️ NormOS — Нормативний Двигун")
    gr.Markdown("### Повнофункціональний демо-дашборд")
    
    with gr.Row():
        with gr.Column(scale=1):
            agent = gr.Dropdown(["Рада", "Голова", "Секретар"], value="Рада", label="Суб'єкт")
            vote = gr.Checkbox(value=True, label="Факт голосування")
            quorum = gr.Checkbox(value=True, label="Кворум")
            query = gr.Textbox(label="Власний запит", placeholder="Голова зобов'язаний підписати рішення...")
            file = gr.File(label="Завантажити документ (TXT)", file_types=[".txt"])
            btn = gr.Button("🚀 Запустити вивід", variant="primary")
        
        with gr.Column(scale=2):
            result_text = gr.Textbox(label="Вердикт")
            trace_text = gr.Textbox(label="Трасування", lines=8)
    
    graph_plot = gr.Plot()
    
    gr.Markdown("### Історія")
    history_output = gr.Textbox(lines=8)
    
    btn.click(
        run_inference,
        inputs=[agent, vote, quorum, query, file],
        outputs=[result_text, trace_text, graph_plot, history_output]
    )

demo.launch()
