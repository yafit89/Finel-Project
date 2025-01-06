from flask import Blueprint, render_template, request, redirect, url_for
from app.models import StringEntry
from app import db
import boto3
from botocore.exceptions import NoCredentialsError

main = Blueprint("main", __name__)

BUCKET_NAME = "my-s3-bucket-for-ui-images1"
OBJECT_NAME = "aws_image.png"

def fetch_image_from_s3():
    s3 = boto3.client("s3")
    try:
        s3.download_file(BUCKET_NAME, OBJECT_NAME, f"app/static/{OBJECT_NAME}")
        return f"{OBJECT_NAME}"
    except NoCredentialsError:
        return None

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("string_input")
        if content:
            new_entry = StringEntry(content=content)
            db.session.add(new_entry)
            db.session.commit()
        return redirect(url_for("main.index"))

    strings = StringEntry.query.all()
    image_path = fetch_image_from_s3()

    return render_template("index.html", strings=strings, image_path=image_path)
