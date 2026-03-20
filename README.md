# GIF Tools Web

Split GIFs into frames, edit them, rejoin into a new GIF — all in the browser.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000

## Deploy to Render (free)

1. Push this folder to a GitHub repo
2. Go to https://render.com and sign up (free)
3. Click **New → Web Service**
4. Connect your GitHub repo
5. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
6. Click **Deploy** — you'll get a public URL like `https://gif-tools.onrender.com`

## Deploy to Railway (free tier)

1. Push this folder to a GitHub repo
2. Go to https://railway.app and sign up
3. Click **New Project → Deploy from GitHub**
4. Select your repo — Railway auto-detects the Procfile
5. Done! You'll get a public URL instantly.

## Project structure

```
gif_tools_web/
  app.py              ← Flask backend
  requirements.txt    ← Python dependencies
  Procfile            ← For Railway/Render
  templates/
    index.html        ← The whole frontend
  uploads/            ← Temp upload storage (auto-created)
  outputs/            ← Temp output storage (auto-created)
```
