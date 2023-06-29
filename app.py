from flask import Flask, render_template, request
import predict
from urllib.parse import urlparse
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['input_url']
        parsed_url = urlparse(user_input).netloc
        if not parsed_url:
            return render_template("notfound.html")
        predicted_values = predict.predict(user_input)
        return render_template('result.html', results = predicted_values)
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
