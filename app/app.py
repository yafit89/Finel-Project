from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import boto3
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@mysql-service/photo_viewer"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
s3_client = boto3.client('s3', region_name='us-east-1')

@app.route('/')
def index():
    photos = []
    try:
        bucket_name = os.getenv("S3_BUCKET", "yafit-s3-bucket")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            photos.append(obj['Key'])
    except Exception as e:
        print(f"Error retrieving photos: {e}")

    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        bucket_name = os.getenv("S3_BUCKET", "yafit-s3-bucket")
        s3_client.upload_fileobj(file, bucket_name, file.filename)
        return f"Uploaded {file.filename} successfully!"
    return "No file uploaded.", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)