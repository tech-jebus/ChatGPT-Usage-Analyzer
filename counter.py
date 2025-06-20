import json
from collections import defaultdict
from datetime import datetime
import tiktoken
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import NullLocator

# Model to tokenizer mapping
model_tokenizer_map = {
    'gpt-4o': 'gpt-4o',
    'gpt-4': 'gpt-4',
    'gpt-4-5': 'gpt-4',
    'gpt-3.5-turbo': 'gpt-3.5-turbo',
    'gpt-4o-mini': 'cl100k_base',
    'gpt-4-1-mini': 'cl100k_base',
    'text-davinci-002-render-sha': 'p50k_base',
    'o3-mini': 'cl100k_base',
    'o4-mini': 'cl100k_base',
    'o3-mini-high': 'cl100k_base',
    'o1': 'cl100k_base',
    'research': 'cl100k_base'
}

# Initialize tokenizer encoders
encoders = {}
for alias in set(model_tokenizer_map.values()):
    try:
        encoders[alias] = tiktoken.get_encoding(alias)
    except Exception:
        encoders[alias] = tiktoken.get_encoding("cl100k_base")

# Load conversation data
with open('conversations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


# Initialize daily counters
daily_messages = defaultdict(int)
daily_tokens = defaultdict(int)
daily_chats = defaultdict(int)

chat_start_dates = []

total_messages = 0
total_tokens = 0

for chat in data:
    earliest_time = None
    if 'mapping' in chat:
        messages = chat['mapping'].values()
        for msg in messages:
            if msg.get("message"):
                parts = msg["message"].get("content", {}).get("parts", [])
                content = parts[0] if isinstance(parts, list) and parts and isinstance(parts[0], str) else ""
                model = msg["message"].get("metadata", {}).get("model_slug")
                time = msg["message"].get("create_time")

                if not time:
                    continue

                dt = datetime.fromtimestamp(time)
                day_key = dt.date()

                if earliest_time is None or time < earliest_time:
                    earliest_time = time

                total_messages += 1

                if model:
                    tokenizer_alias = model_tokenizer_map.get(model, "cl100k_base")
                    encoder = encoders[tokenizer_alias]
                    tokens = len(encoder.encode(content))
                else:
                    tokens = 0

                total_tokens += tokens
                daily_messages[day_key] += 1
                daily_tokens[day_key] += tokens

    if earliest_time:
        dt_start = datetime.fromtimestamp(earliest_time).date()
        daily_chats[dt_start] += 1

# Get sorted unique days with activity
days = sorted(set(list(daily_messages.keys()) + list(daily_chats.keys())))

messages_per_day = [daily_messages.get(d, 0) for d in days]
tokens_per_day = [daily_tokens.get(d, 0) for d in days]
chats_per_day = [daily_chats.get(d, 0) for d in days]

# Convert dates for matplotlib
days_num = mdates.date2num(days)

def plot_daily(x, y, title, ylabel, color):
    """Helper function to plot daily metrics"""
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot_date(x, y, '-', color=color, linewidth=1)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True)

    # Major ticks every month with labels like "Jan 2024"
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    # Remove minor ticks to avoid clutter
    ax.xaxis.set_minor_locator(NullLocator())

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Plot Messages
plot_daily(days_num, messages_per_day, "Messages Per Day", "Messages", "blue")

# Plot Tokens
plot_daily(days_num, tokens_per_day, "Tokens Per Day", "Tokens", "green")

# Plot Chats Started
plot_daily(days_num, chats_per_day, "Chats Started Per Day", "Chats", "orange")
