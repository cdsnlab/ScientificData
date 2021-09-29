from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)