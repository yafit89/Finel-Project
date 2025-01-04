import os
from flask import Flask, render_template, send_file
import json
from flask_mysqldb import MySQL
import boto3
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "mysql-service")  # Default to Kubernetes service name
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "password")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "photo_viewer")

mysql = MySQL(app)

# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET", "yafit-s3-bucket")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
s3_client = boto3.client('s3', region_name=S3_REGION)

# Function to load the configuration file
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config.get("welcome_message", "Welcome to the Photo Viewer!")
    except FileNotFoundError:
        logging.warning(f"Configuration file '{config_path}' not found.")
        return "Welcome to the Photo Viewer!"

# Function to get photos from a local folder
def get_local_photos(folder_path="photos"):
    try:
        if os.path.exists(folder_path):
            return [
                file for file in os.listdir(folder_path)
                if file.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
        else:
            logging.warning(f"Folder '{folder_path}' does not exist.")
            return []
    except Exception as e:
        logging.error(f"Error retrieving files from folder: {e}")
        return []

# Function to get photos from MySQL
def get_photos_from_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT image_key FROM images")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Error fetching photos from MySQL: {e}")
        return []

# Function to get presigned URLs for S3 images
def get_s3_urls(image_keys):
    try:
        return [
            s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET, 'Key': key}, ExpiresIn=3600)
            for key in image_keys
        ]
    except Exception as e:
        logging.error(f"Error generating S3 URLs: {e}")
        return []

@app.route("/")
def index():
    logging.info("Accessing index route.")
    folder_path = os.getenv("PHOTO_FOLDER", "photos")

    welcome_message = load_config()
    local_photos = get_local_photos(folder_path)
    db_photos = get_photos_from_db()
    s3_urls = get_s3_urls(db_photos)

    return render_template("index.html", welcome_message=welcome_message, local_photos=local_photos, s3_photos=s3_urls)

@app.route("/photo/<path:photo_key>")
def photo(photo_key):
    logging.info(f"Accessing photo: {photo_key}")
    folder_path = os.getenv("PHOTO_FOLDER", "photos")
    file_path = os.path.join(folder_path, photo_key)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    logging.error(f"Photo not found: {photo_key}")
    return "Error: Photo not found.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)