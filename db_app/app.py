from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import boto3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@mysql-service/photo_viewer"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
s3_client = boto3.client('s3', region_name='us-east-1')

@app.route('/')
def index():
    return "Welcome to Photo Viewer"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

