from flask import Flask, Response, render_template_string
from app.camera import generate_frames
import os

app = Flask(__name__, static_folder="static")

# Read the HTML UI
with open(os.path.join("static", "index.html"), "r", encoding="utf-8") as f:
    UI_HTML = f.read()


@app.route("/")
def index():
    return render_template_string(UI_HTML)


@app.route("/video_feed")
def video_feed():
    """MJPEG stream endpoint."""
    camera_index = int(os.environ.get("CAMERA_INDEX", 0))
    return Response(
        generate_frames(camera_index),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    # Run on all interfaces so Docker can expose it
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
