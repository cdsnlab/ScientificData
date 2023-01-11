# from flask_mail import Mail, Message
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

def read_json():
    file_path = "./data/content.json"
    with open(file_path, 'r') as file:
        data = json.load(file)    
    return data


@app.route('/')
@app.route('/home')
def home():   
    data = read_json()        
    if session.get('id') is None:
        return render_template('basic_template.html', data=data['home'])
    else:
        return render_template('/admin/edit_basic_template.html', data=data['home'])
        # return redirect(url_for('admin_home')) 

@app.route('/contact')
def contact():
    data = read_json()        
    if session.get('id') is None:
        return render_template('basic_template.html', data=data['contact'])
    else:
        return render_template('/admin/edit_basic_template.html', data=data['contact'])
        # return redirect(url_for('admin_contact'))
    
    
@app.route('/login_confirm', methods=['POST'])
def login_confirm():
    f = open("./password.txt", 'r')
    lines = f.readlines()
    pw = lines[0]
    f.close()
    id_ = request.form['id_']
    pw_ = request.form['pw_']
    if id_ == 'admin' and pw_ == pw:
        session['id'] = id_
        return redirect(url_for('home'))
    else:
        return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/admin')
def admin():
    return render_template('/admin/login.html')


@app.route('/edit', methods=['POST'])
def edit():
    data = read_json()
    page = request.form['page']
    data[page] = request.form
    
    file_path = "./data/content.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent="\t")
    return render_template(f'/admin/result_basic.html', data=data[page])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# @app.route('/form_recv', methods=['POST'])
# def form_recv():
#     if request.method == 'POST':
#         data = request.form
#     else:
#         data ={}
#     msg = Message("[SD] Request for sharing dataset from " + data['name'], \
#             sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
#     msg.body = f"email address: {data['email']} \nmessage:\n  {data['message']}"
#     mail.send(msg)
#     return render_template('form_recv.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    # app.run(host="0.0.0.0", port='80', debug=True)




# file_path = "./data/content.json"

# with open(file_path, 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent="\t")

