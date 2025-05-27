from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

def find_most_common_word(file_content):
    words = re.findall(r'\w+', file_content.lower())
    word_counts = Counter(words)
    if not word_counts:
        return None, 0
    most_common = word_counts.most_common(1)[0]
    return most_common

@app.route('/', methods=['GET', 'POST'])
def index():
    most_common_word = None
    frequency = 0
    error = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error = "Файл не загружен"
        else:
            file = request.files['file']
            if file.filename == '':
                error = "Файл не выбран"
            else:
                try:
                    content = file.read().decode('utf-8')
                    most_common_word, frequency = find_most_common_word(content)
                except Exception as e:
                    error = f"Ошибка обработки файла: {e}"

    return render_template('index.html',
                         most_common_word=most_common_word,
                         frequency=frequency,
                         error=error)

if __name__ == '__main__':
    app.run()