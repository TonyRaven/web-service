from flask import Flask,request,jsonify,abort,redirect,url_for,render_template,send_file, flash
import pickle
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import pandas as pd
app = Flask(__name__, static_folder='static',static_url_path = "/static")
with open('knn.pkl','rb') as model_file:
    knn = pickle.load(model_file)
@app.route('/')
def hello_world():
    return '<h1>Hello, dear kek!</h1>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % (username)

def mean(nums):
    return float(sum(nums)/max(len(nums),1))

@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = mean(nums)
    print(nums)
    return str(nums_mean)

@app.route('/iris/<params>')
def iris(params):
    params = params.split(',')
    params = [float(num) for num in params]
    with open('knn.pkl','rb') as model_file:
        knn = pickle.load(model_file)

    return str(knn.predict([params]))


@app.route('/show_image')
def show_image():
    return '<img src="/static/setosa.jpg">'


@app.route('/iris_post',methods=['POST'])
def add_message():
    try:
        content = request.get_json()
        params = content['flower'].split(',')
        params = [float(num) for num in params]
        preds = knn.predict([params])
        predict = {'class':str(preds[0])}
        return jsonify(predict)
    except:
        return redirect(url_for('bad_request'))

@app.route('/badrequest400')
def bad_request():
    abort(400)

app.config.update(dict(
    SECRET_KEY="powerful key",
    WTF_SCRF_SECRET_KEY = "a csrf secret key"
))


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        df = pd.read_csv(f,header=None)
        predict = knn.predict(df)
        filename = form.name.data + '.txt'
        result = pd.DataFrame(predict)
        result.to_csv(filename,index=False)
        #return 'Well done'
        # f.save(os.path.join(
        #      filename
        # ))
        #return str(form.name)
        return send_file(filename,mimetype = 'text/csv',attachment_filename=filename,as_attachment=True)
    return render_template('submit.html', form=form)



UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + 'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''