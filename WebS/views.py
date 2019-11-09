from flask import render_template
from WebS import app


@app.route('/')
@app.route('/mainPage')
def show_words():
    lines=[]
    with open(str('data/mainNews.txt'), 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line[:-2]
            lines.append(line)
    return render_template('mainPage.html',
                           lines=lines)

