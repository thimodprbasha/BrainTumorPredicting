from flask import Flask
from flask_cors import CORS
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, request, json
from werkzeug.utils import secure_filename
from dectection import engine

app = Flask(__name__)
uploads = './uploads/temp_image'
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = uploads

# Allowed file type
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


def check_path_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
       os.makedirs(app.config['UPLOAD_FOLDER'])


def response_config(data, status_code, mime_type):
    return app.response_class(
        response=json.dumps(data),
        status=status_code,
        mimetype=mime_type
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_temp_files():
    if not os.listdir(uploads) == []:
        files = [f for f in os.listdir(uploads) if os.path.isfile(os.path.join(uploads, f))]
        for file in files:
            os.remove(os.path.join(uploads, file))



@app.route('/api/detect-tumor', methods=['POST'])
def get_tumor_properties():
    try:
        if 'file' not in request.files:
            data = {
                'Message': 'Image not found!'
            }
            return response_config(data, 404, 'application/json')

        for image in request.files.getlist('file'):
            if image.filename == '':
                data = {
                    'Message': 'No selected image!'
                }
                return response_config(data, 404, 'application/json')

            if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    temp_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(temp_image)
            
            else:
                data = {
                    'Message': 'Invalid image type!'
                }
                return response_config(data, 404, 'application/json')

        res = engine(app.logger)

        remove_temp_files()
        return response_config(res, 200, 'application/json')
    
    except Exception as e:
        app.logger.error('Error : ', str(e))
        data = {
            'Message': str(e)
            }
        remove_temp_files()
        return response_config(data, 505, 'application/json')


if __name__ == '__main__':
    check_path_exists()
    remove_temp_files()
    app.run(port=8000, debug=False)