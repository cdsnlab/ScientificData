from flask_mail import Mail, Message
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/form_recv', methods=['POST'])
def form_recv():
    if request.method == 'POST':
        data = request.form
    else:
        data ={}
    msg = Message("[SD] Request for sharing dataset from " + data['name'], \
            sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"email address: {data['email']} \nmessage:\n  {data['message']}"
    mail.send(msg)
    return render_template('form_recv.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    # app.run(host="0.0.0.0", port='80', debug=True)
