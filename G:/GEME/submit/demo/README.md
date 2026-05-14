# GEME Playground

Interactive browser-based demo. Feed text, inject noise, watch the frame economy evolve in real time.

## Run

```bash
pip install streamlit
streamlit run geme_playground.py
```

## What you can do

- **Type text** 鈥?watch GEME build a frame economy from your words
- **Inject noise** 鈥?see anomaly spike as predictions fail
- **Run induction** 鈥?trigger adaptive forgetting and self-observation
- **Watch doubt** 鈥?push the system until it doubts itself (L6)

## Dashboard shows

- Frame count, prediction activity, accuracy, anomaly score
- Frame weight visualization (colored bars = frame economy)
- Anomaly and accuracy over time (line chart)
- Layer distribution (L1鈥揕6 bar chart)
