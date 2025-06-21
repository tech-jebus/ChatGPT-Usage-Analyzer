# ChatGPT Usage Analyzer

A Python script to analyze and visualize your ChatGPT conversation data exported from OpenAI.

---

## Features

- Parses your `conversations.json` export file  
- Counts total chats, messages, and estimates token usage per model  
- Plots detailed daily usage graphs for messages, tokens, and chats  
- Shows monthly labels on the timeline for clarity  
- Highlights usage trends over time  

---

## Requirements

Python 3.8 or higher and these packages:

- `tiktoken`  
- `matplotlib`  
- `numpy`  

Install with:
```bash
pip install tiktoken matplotlib numpy
```

---

## Usage

1. Clone repository
```bash
git clone https://...
```
3. Export your ChatGPT data from OpenAI Settings > Data Controls > Export  
4. Extract the `conversations.json` file into the script’s folder
6. Run the script with:
```bash
python counter.py
```
4. The script prints stats and shows usage graphs  

---

## How It Works

- Loads your conversation history JSON  
- Tokenizes messages using OpenAI’s official tokenizers (`tiktoken`)  
- Aggregates data by day for detailed time-series analysis  
- Uses `matplotlib` to plot interactive graphs with monthly timeline labels  

---

## Notes

- Token counts are estimates based on message content only  
- System messages and metadata aren’t included in tokens  
- For personal use only — don’t share your conversations publicly  

---

## License

MIT License — feel free to use and modify  
