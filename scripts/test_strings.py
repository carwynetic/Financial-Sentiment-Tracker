import re
import matplotlib.pyplot as plt

with open(r'd:\Vscode-luyện code\Financial Sentiment Tracker (FinBERT Powered)\scripts\generate_academic_architecture.py', 'r', encoding='utf-8') as f:
    code = f.read()

fig, ax = plt.subplots()

# Find all occurrences of ax.text
for line in code.splitlines():
    if 'ax.text(' in line:
        # extract string argument
        parts = line.split(',')
        if len(parts) >= 3:
            raw_text = ','.join(parts[2:]).strip()
            # find what is between first quote and matching quote
            if raw_text.startswith(('"', "'", 'r"', "r'")):
                try:
                    val = eval(raw_text.split(',')[0]) if ',' in raw_text else eval(raw_text)
                    if isinstance(val, str) and '$' in val:
                        t = ax.text(0, 0, val)
                        fig.canvas.draw()
                        t.remove()
                except Exception as e:
                    print('ERROR in line:', line.strip(), '==>', e)

print('Test complete.')
