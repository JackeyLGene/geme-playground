"""
GEME Playground 鈥?interactive demo for general audience.
Run: streamlit run geme_playground.py
"""
import math, random
import streamlit as st
from geme import GEME

st.set_page_config(page_title="GEME: Self-Referential Prism", layout="wide")
st.title("GEME: Self-Referential Prism")

MODE = st.sidebar.radio("Choose a demo:", [
    "Cat on Mat 鈥?Six-Layer Pipeline",
    "Surprise Detection 鈥?Narrative Twist",
    "Human vs Machine 鈥?Structural Signature",
])

# 鈹€鈹€ Shared State 鈹€鈹€
if 'g' not in st.session_state:
    st.session_state.g = GEME(memory_cap=16)
    st.session_state.g.memory.preserve_sig = True
    st.session_state.g.memory.quantum_mode = True
    st.session_state.log = []

# ===================================================================
# MODE 1: Cat on Mat 鈥?Six-Layer Pipeline
# ===================================================================
if MODE.startswith("Cat on Mat"):
    st.subheader("Feed text word by word through the six-layer pipeline")

    text = st.text_input("Your sentence:", "the cat sat on the mat")
    words = text.split()

    if st.button("Step Through Pipeline") or 'cat_step' in st.session_state:
        if 'cat_step' not in st.session_state:
            st.session_state.cat_step = 0
            st.session_state.cat_g = GEME(memory_cap=12)
            st.session_state.cat_g.memory.preserve_sig = True
            st.session_state.cat_g.memory.quantum_mode = True

        step = st.session_state.cat_step
        g = st.session_state.cat_g

        if step < len(words):
            g.input(words[step])
            st.session_state.cat_step += 1
            st.info(f"Fed '{words[step]}' (word {step+1}/{len(words)})")

        m = g.metrics()
        cols = st.columns(6)
        layers = m.get('layers', {})
        cols[0].metric("L1 Entities", layers.get('L1', 0))
        cols[1].metric("L2 Assoc.", layers.get('L2', 0))
        cols[2].metric("L3 Bridge", layers.get('L3', 0))
        cols[3].metric("L4 Pred.Err", m['L4_frame_count'])
        cols[4].metric("Predictions", m['pred_total'])
        cols[5].metric("Anomaly", f"{g.anomaly_score():.2f}")

        # Frame display
        st.caption("Active frames in the economy:")
        frames = sorted(g.memory.frames, key=lambda f: -f.weight)
        for f in frames[:8]:
            label = f"F{f.fid}: **{f.sig[:25]}** (L{f.layer}) w={f.weight:.1f}"
            if '鈹€鈹€' in (f.sig_full or ''): label += " 馃敆"
            if 'self' in (f.sig or ''): label += " 馃獮"
            if 'pred_err' in (f.sig or ''): label += " 鈿狅笍"
            st.write(label)

        if st.button("Reset"): del st.session_state.cat_step

# ===================================================================
# MODE 2: Surprise Detection
# ===================================================================
elif MODE.startswith("Surprise"):
    st.subheader("Feed a predictable story, then inject a twist")

    predictable = st.text_area("Predictable sentences (one per line):",
        "the cat sat on the mat\nthe dog slept by the fire\nthe sun shone through the window\nshe poured a cup of tea\nhe opened the newspaper")
    twist = st.text_input("Twist sentence:", "the newspaper read her name and tomorrow's date")

    if st.button("Run Story"):
        g = GEME(memory_cap=12)
        g.memory.preserve_sig = True
        g.memory.quantum_mode = True

        results = []
        # Train on predictable
        for _ in range(5):
            for line in predictable.strip().split('\n'):
                if line.strip():
                    g.input(line.strip())
            g.memory.induction_clean()

        # Test: predictable + twist
        for i, line in enumerate(predictable.strip().split('\n')):
            if line.strip():
                g.input(line.strip())
                results.append((line.strip()[:40], g.anomaly_score(), g.metrics()['pred_total']))

        g.input(twist)
        results.append((f"鉃★笍 {twist[:40]}", g.anomaly_score(), g.metrics()['pred_total']))

        for text, anomaly, preds in results:
            bar = "鈻? * int(anomaly * 20)
            color = "red" if anomaly > 0.6 else "green" if anomaly < 0.4 else "orange"
            st.markdown(f"`:{color}[{bar}]` {anomaly:.2f} 鈥?{text}")

# ===================================================================
# MODE 3: Human vs Machine
# ===================================================================
elif MODE.startswith("Human"):
    st.subheader("Compare frame-economic signatures of two texts")

    col1, col2 = st.columns(2)
    with col1:
        text_a = st.text_area("Text A (e.g. human)", "The cat sat on the mat. It was a quiet afternoon. She watched the birds outside the window.", height=150)
    with col2:
        text_b = st.text_area("Text B (e.g. machine)", "The feline positioned itself upon the floor covering. The temporal period was characterized by tranquility. She observed the avian creatures beyond the fenestration.", height=150)

    if st.button("Compare"):
        results = {}
        for label, text in [("A", text_a), ("B", text_b)]:
            g = GEME(memory_cap=16)
            g.memory.preserve_sig = True
            g.memory.quantum_mode = True
            words = text.split()
            windows = [words[i:i+5] for i in range(0, len(words)-4, 2)]
            for _ in range(5):
                for w in windows:
                    g.input(' '.join(w))
                g.memory.induction_clean()
            m = g.metrics()
            results[label] = m

        cols = st.columns(5)
        for metric, label in [('pred_total', 'Predictions'), ('structural_entropy', 'Entropy'),
                               ('frame_count', 'Frames'), ('L4_frame_count', 'L4 Activity'),
                               ('I(phi;X)', 'I(phi;X)')]:
            with cols.pop(0):
                va = results['A'].get(metric, 0)
                vb = results['B'].get(metric, 0)
                delta = va - vb
                direction = "A higher" if delta > 0 else "B higher"
                st.metric(label, f"{delta:+.1f}", direction)

        st.caption("GEME's prediction count often differs between human and machine text even when word length and vocabulary are matched (see S7).")
