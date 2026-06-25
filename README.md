# movieBox - Cinema Trailer Streaming Platform (New Task)

**movieBox** is a high-end, light-themed professional web application designed to upload and stream **4-5 movie trailer videos** and **3-4 promotional movie posters** directly from **AWS S3 Cloud Storage**.

---

## 🌟 Key Capabilities

1. **HTTP 206 Partial Content Video Streaming**: Built-in HTTP `Range` request handler (`/s3_media/<key>`) using `boto3`. This allows HTML5 `<video>` players to seek, buffer, and play high-definition `.mp4` movie trailers streamed cleanly from private S3 buckets without 403 access issues.
2. **Dedicated Admin Portal (`/admin`)**:
   - Configure AWS S3 Bucket Name, Region, and Access Credentials.
   - Batch upload movie trailer video files (`.mp4`, `.webm`, `.mov`) and matching poster images (`.jpg`, `.png`).
   - Manage existing S3 movie library overview table with item size inspection and deletion.
3. **Executive Light Aesthetics**: Pure professional light theme (`#f8fafc` background, crisp Inter typography, widescreen modal video player).

---

## 📂 Project Structure (`movieBox/`)

```text
movieBox/
├── app.py               # Core Flask backend (supporting / and /admin routes + HTTP 206 video streaming)
├── requirements.txt     # Dependencies (flask, boto3)
├── config.json          # Saved S3 credentials
├── README.md            # Setup guide
├── static/
│   └── style.css        # High-end light professional theme CSS
└── templates/
    ├── index.html       # Public Homepage (/) with widescreen video player gallery
    └── admin.html       # Admin Management Console (/admin)
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Start the Streaming Platform
```powershell
python app.py
```
The application server will start on port **`5080`**.

### 3. Workflow Guide
1. Open **`http://127.0.0.1:5080/admin`** in your web browser.
2. Under **1. AWS S3 Configuration**, enter your **S3 Bucket Name** and **Region**, then click **Save Cloud Credentials**.
3. Under **2. Upload Trailers & Posters**, select your 4-5 video trailer files (e.g. `avatar.mp4`, `inception.mp4`) and 3-4 promotional poster images (`avatar.jpg`, `inception.jpg`), then click **Upload Files to S3 Bucket**.
4. Navigate to Homepage **`http://127.0.0.1:5080/`** to view your sleek cinema showcase! Click any movie card to play the trailer video in widescreen cinema mode.
