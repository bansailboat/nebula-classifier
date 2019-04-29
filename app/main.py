from app import app
from flask import (
    render_template,
    flash,
    request,
    redirect,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

import os


UPLOAD_FOLDER = "./app/static/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = (
    50 * 1024 * 1024
)  # Limits size of uploaded file to 50MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    filename, inf_cmd = None, None

    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            inference = (
                f'python -m scripts.label_image \
                        --graph=tf_files/retrained_graph.pb  \
                        --image={app.config["UPLOAD_FOLDER"]}/{filename}'
            )
            inf_cmd = os.popen(inference).read()

            return render_template("index.html", filename=filename, inf_cmd=inf_cmd)

    return render_template("index.html")