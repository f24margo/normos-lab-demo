import gradio as gr
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from core.inference import InferenceEngine
from core.verb_registry import VerbRegistry

engine = InferenceEngine()
history = []

MODALITY_COLORS = {
    "OBL": "#E67E22",
    "PERM": "#2ECC71",
    "PROH": "#E74C3C",
    "POW": "#3498DB",
    None: "#BDC3C7",
}

def _as_dict(step):
    if isinstance(step, dict):
        return step
    if hasattr(step, "model_dump"):
        return step.model_dump()
    if hasattr(step, "dict"):
        return step.dict()
    return {"label": str(step), "step_type": None, "modality": None}

def build_decision_graph(trace_steps, verdict, deciding_verb, modality):
    """Ланцюг виводу: init → verb_match → computation → verdict"""
    fig, ax = plt.subplots(figsize=(11, 3.5))
    G = nx.DiGraph()

    nodes, colors = [], []

    nodes.append("Запит")
    colors.append("#95A5A6")

    for raw in trace_steps:
        step = _as_dict(raw)
        st = step.get("step_type")
        if st == "coverage":
            continue  # покриття — тільки в badges
        if st == "init":
            nodes.append("Ініціалізація")
            colors.append("#BDC3C7")
        elif st == "verb_match":
            lemma = deciding_verb or step.get("matched_verb") or "глагол"
            mod = modality or step.get("modality")
            nodes.append(f"{lemma}")
            colors.append(MODALITY_COLORS.get(mod, "#BDC3C7"))
        elif st == "computation":
            nodes.append("Обчислення")
            colors.append(MODALITY_COLORS.get(modality or step.get("modality"), "#BDC3C7"))
        elif st == "oov":
            nodes.append("OOV")
            colors.append("#E74C3C")

    v_short = verdict if len(verdict) < 26 else verdict[:23] + "…"
    nodes.append(v_short)
    colors.append(MODALITY_COLORS.get(modality, "#F39C12"))

    # дедуп сусідів
    clean_n, clean_c = [], []
    for n, c in zip(nodes, colors):
        if clean_n and clean_n[-1] == n:
            continue
        clean_n.append(n)
        clean_c.append(c)

    G.add_nodes_from(range(len(clean_n)))
    for i in range(len(clean_n) - 1):
        G.add_edge(i, i + 1)

    pos = {i: (i * 2.2, 0) for i in range(len(clean_n))}
    nx.draw(
        G, pos,
        labels={i: clean_n[i] for i in range(len(clean_n))},
        node_color=clean_c,
        node_size=2800,
        font_size=9,
        arrows=True,
        ax=ax,
        edge_color="#7F8C8D",
    )
    ax.set_title("Граф ухвалення рішення")
    ax.set_ylim(-0.8, 0.8)
    plt.tight_layout()
    return fig

def render_badges(verbs_found):
    if not verbs_found:
        return "— (немає збігів / OOV)"
    lines = []
    for item in verbs_found:
        if isinstance(item, dict):
            lines.append(f"• {item.get('lemma')} ({item.get('modality')})")
        else:
            lines.append(f"• {item}")
    return f"Знайдено {len(verbs_found)}:\n" + "\n".join(lines)

def run_inference(agent, query_text, uploaded_file):
    text = (query_text or "").strip()
    try:
        if uploaded_file is not None:
            if isinstance(uploaded_file, str):
                with open(uploaded_file, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            elif hasattr(uploaded_file, "name"):
                with open(uploaded_file.name, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            else:
                text = uploaded_file.decode("utf-8", errors="ignore")
        if not text:
            text = f"{agent} може прийняти рішення"

        result = engine.infer(text)
    except Exception as e:
        return f"Помилка: {e}", "", "", "—", None, "\n".join(history[-12:])

    trace_steps = result.get("trace", [])
    verdict = result.get("result", "—")
    deciding = result.get("deciding_verb") or result.get("verb")
    modality = result.get("modality")
    verbs_found = result.get("verbs_found") or []

    trace_text = "\n".join(_as_dict(s).get("label", "") for s in trace_steps)
    fig = build_decision_graph(trace_steps, verdict, deciding, modality)
    badges = render_badges(verbs_found)

    entry = f"{datetime.now().strftime('%H:%M:%S')} | {agent} | {verdict}"
    if result.get("oov"):
        entry += " | OOV"
    history.append(entry)

    reg_total = VerbRegistry().count()
    meta = f"deciding: {deciding} | modality: {modality} | oov: {result.get('oov')} | found: {len(verbs_found)} з {reg_total}"
    return verdict, meta, trace_text, badges, fig, "\n".join(history[-12:])

with gr.Blocks(title="NormOS v2") as demo:
    gr.Markdown("# ⚖️ NormOS v2 — Decision Graph")
    gr.Markdown("Словник (badges) ≠ ланцюг виводу (граф). Вирішальний глагол — один.")

    with gr.Row():
        with gr.Column(scale=1):
            agent = gr.Dropdown(["Рада", "Голова", "Секретар"], value="Рада", label="Суб'єкт")
            query = gr.Textbox(label="Запит", lines=3, placeholder="Забороняється проводити збори...")
            file = gr.File(label="Документ (TXT)", file_types=[".txt"])
            btn = gr.Button("🚀 Запустити вивід", variant="primary")
        with gr.Column(scale=2):
            result_text = gr.Textbox(label="Вердикт")
            meta_text = gr.Textbox(label="Метадані")
            trace_text = gr.Textbox(label="Trace", lines=8)

    with gr.Row():
        badges_text = gr.Textbox(label="📚 Знайдені глаголи (lemma + modality)", lines=12)
        graph_plot = gr.Plot(label="🔗 Граф ухвалення рішення")

    history_output = gr.Textbox(label="Історія", lines=5)

    btn.click(
        run_inference,
        inputs=[agent, query, file],
        outputs=[result_text, meta_text, trace_text, badges_text, graph_plot, history_output],
    )

if __name__ == "__main__":
    demo.launch()
