# GIF Tools

A Python/Flask web app for splitting animated GIFs into frames and reassembling them after editing.

**Live app →** [gif-tools.onrender.com](https://gif-tools.onrender.com/)

## Tech Stack

- **Backend:** Python 3, Flask, Pillow (PIL)
- **Frontend:** Vanilla HTML/CSS/JS (single-page, no framework)
- **Hosting:** Render.com (free tier)
- **Also available as:** Windows EXE (PyInstaller) and desktop GUI (tkinter)

## Project Structure
gif-tools/
├── app.py              # Flask backend — split & rejoin endpoints
├── requirements.txt    # Python dependencies
├── Procfile            # Render/Railway deployment config
├── BingSiteAuth.xml    # Bing Webmaster verification
└── templates/
└── index.html      # Full frontend (HTML + CSS + JS)

## Run Locally

```bash
git clone https://github.com/GavVan46/gif-tools.git
cd gif-tools
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

## How It Works

1. **Split endpoint** — accepts a GIF upload, uses Pillow to iterate over frames, saves each as a PNG, bundles them into a ZIP alongside a `frame_durations.txt` file that records each frame's display time in milliseconds.

2. **Rejoin endpoint** — accepts a set of PNG uploads plus the durations file, reconstructs the animation with Pillow's `save()` using `append_images` and `duration` parameters.

All processing happens server-side. Uploaded files are stored temporarily and cleaned up after the response is sent.

## Deployment

The app is configured for Render.com via the `Procfile`. To deploy your own instance:

1. Fork this repo
2. Create a new Web Service on Render pointing to your fork
3. Set the build command to `pip install -r requirements.txt`
4. Set the start command to `gunicorn app:app`

## Contributing

Issues and PRs are welcome. If you have ideas for new features (batch processing, format conversion, etc.), open an issue first to discuss.

## License

This project is open source. See the repo for details.
