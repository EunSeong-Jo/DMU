# app.py (Flask)
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.DataFrame({'이름': ['김철수', '이영희'], '점수': [85, 92]})
    return render_template('index.html', tables=[df.to_html()])

if __name__ == '__main__':
    app.run(debug=True)
