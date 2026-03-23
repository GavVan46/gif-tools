"""
GIF Tools Web — Flask Backend
==============================
pip install flask pillow
python app.py
"""

import os
import glob
import uuid
import zipfile
import shutil
from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")




@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/sitemap.xml")
def sitemap():
    return render_template("sitemap.xml"), 200, {"Content-Type": "application/xml"}

@app.route("/split", methods=["POST"])
def split():
    if "gif" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["gif"]
    if not file.filename.lower().endswith(".gif"):
        return jsonify({"error": "Please upload a .gif file"}), 400

    # Save uploaded GIF to a temp location
    session_id = uuid.uuid4().hex
    gif_path   = os.path.join(UPLOAD_FOLDER, f"{session_id}.gif")
    file.save(gif_path)

    # Split into frames
    frames_dir = os.path.join(OUTPUT_FOLDER, session_id)
    os.makedirs(frames_dir, exist_ok=True)

    try:
        gif = Image.open(gif_path)
        frame_count = 0
        durations   = []

        try:
            while True:
                frame = gif.convert("RGBA")
                frame.save(os.path.join(frames_dir, f"frame_{frame_count:04d}.png"))
                durations.append(gif.info.get("duration", 100))
                frame_count += 1
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        gif.close()  # close before deleting on Windows

        # Save timings
        with open(os.path.join(frames_dir, "frame_durations.txt"), "w") as f:
            f.write("\n".join(str(d) for d in durations))

        # Zip everything up
        zip_path = os.path.join(OUTPUT_FOLDER, f"{session_id}_frames.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for fn in sorted(os.listdir(frames_dir)):
                zf.write(os.path.join(frames_dir, fn), fn)

        # Cleanup temp files
        os.remove(gif_path)
        shutil.rmtree(frames_dir)

        return send_file(zip_path, as_attachment=True,
                         download_name="gif_frames.zip",
                         mimetype="application/zip")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/rejoin", methods=["POST"])
def rejoin():
    if "frames" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    loop_map = {"forever": 0, "once": 1, "2": 2, "3": 3, "5": 5}
    loop = loop_map.get(request.form.get("loop", "forever"), 0)

    session_id = uuid.uuid4().hex
    frames_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(frames_dir, exist_ok=True)

    try:
        files = request.files.getlist("frames")

        # Separate duration file from image frames
        durations      = None
        frame_files    = []

        for f in files:
            if f.filename == "frame_durations.txt":
                content   = f.read().decode("utf-8")
                durations = [int(l.strip()) for l in content.splitlines() if l.strip()]
            elif f.filename.lower().endswith(".png"):
                dest = os.path.join(frames_dir, f.filename)
                f.save(dest)
                frame_files.append(f.filename)

        frame_files = sorted(frame_files)

        if not frame_files:
            return jsonify({"error": "No PNG frames found in upload"}), 400

        if durations is None:
            durations = [100] * len(frame_files)
        while len(durations) < len(frame_files):
            durations.append(durations[-1] if durations else 100)

        frames = [Image.open(os.path.join(frames_dir, fn)).convert("RGBA")
                  for fn in frame_files]

        out_path = os.path.join(OUTPUT_FOLDER, f"{session_id}_output.gif")
        frames[0].save(
            out_path,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=loop,
            duration=durations,
            disposal=2,
        )

        shutil.rmtree(frames_dir)

        return send_file(out_path, as_attachment=True,
                         download_name="output.gif",
                         mimetype="image/gif")

    except Exception as e:
        shutil.rmtree(frames_dir, ignore_errors=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
