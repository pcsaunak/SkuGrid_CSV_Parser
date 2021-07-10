import imghdr
import os
import Parse_CSV_Update

from flask import Flask, render_template, request, send_from_directory, send_file, session
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']

app.config['UPLOAD_PATH'] = '/tmp/'
app.config['OUTPUT_PATH'] = '/tmp/'


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    session['filename'] = secure_filename(uploaded_file.filename)
    filename = session['filename']

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            print("Invalide file type ... uploading not done")
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/process_csv')
def process_csv():
    print("File Name: " + session['filename'])
    if len(session['filename']) <= 0:
        return "File Not Present. Hit back button of browser and first upload the CSV file."

    print("Starting Parsing of CSV File")
    print(app.config['UPLOAD_PATH'] + session['filename'])
    return Parse_CSV_Update.startProgram(app.config['UPLOAD_PATH'],session['filename'])


@app.route('/getPlotCSV')  # this is a job for GET, not POST
def plot_csv():
    print("Inside Plot CSV")
    if len(session['filename']) <= 0:
        return "Updated File not present. First upload file, press process CSV and updated CSV file will be created."

    return send_file(app.config['OUTPUT_PATH'] + session['filename']+'_output.csv',
                     mimetype='text/csv',
                     attachment_filename=session['filename'].rsplit('.', 1)[0]+'_output.csv',
                     as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
