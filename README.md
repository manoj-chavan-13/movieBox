<div align="center">

# movieBox OTT Platform

**Production-Grade Enterprise Cloud Cinema & Media Distribution Portal**

[![Python Flask](https://img.shields.io/badge/Backend-Python_Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://flask.palletsprojects.com/)
[![AWS S3 Cloud](https://img.shields.io/badge/Storage-AWS_S3_Vaults-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/s3/)
[![Tailwind CSS](https://img.shields.io/badge/Frontend-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![HTTP 206 Buffering](https://img.shields.io/badge/Protocol-HTTP_206_Lossless-00C7B7?style=for-the-badge)](https://tools.ietf.org/html/rfc7233)

</div>

**movieBox** is an enterprise-grade Over-The-Top (OTT) cinema streaming platform engineered to showcase high-fidelity 4K movie trailers and promotional artwork. Built with modern content-first UX architecture, dynamic client-side DOM filtering, and instant HTTP 206 range request buffering powered directly by Amazon Web Services (AWS S3) cloud vaults.

## ✨ Enterprise Architecture & Feature Suite

### 🎬 1. Cinematic Public Showcase (`/`)
* **Widescreen Premiere Billboard (460px):** Balanced widescreen hero display featuring dynamic spotlight titles, synopsis formatting, and curated 2026 specs (Dolby Atmos, 4K UHD, Lossless Audio).
* **Smart Search & Hero Auto-Collapse:** Integrated real-time library discovery (`⌘K` shortcut). When a search query is initiated, the hero billboard automatically collapses to maximize viewport space for instant discovery.
* **Netflix & Prime Exact Video Engine:** Minimalist player overlay featuring Netflix-style red spinning loaders, interactive scrubbing progress bars, volume adjustment sliders, 10s skip controls, and full keyboard navigation (`Space`, `Esc`, `←`, `→`).

### 🎛️ 2. Studio Curation Console (`/admin`)
* **Real-Time Asset Ingest Deck:** Drag-and-drop ingestion zone with instant client-side asset preview badges (color-coded Video vs Poster chips, precise KB/MB size calculators, and 1-click selection resets).
* **Cloud Library Manifest Table:** Live inventory index displaying verified stream availability status pills, file sizes, and instant **Rename** & **Delete** cloud mutations synchronized directly across S3 objects.
* **Boto3 Cloud Credential Management:** Securely configure and persist target AWS S3 Bucket Name, AWS Region, and Access Keys.

### 🌗 3. Universal 4-Tier Dual Theme System
* **Titanium Light Theme (`#F0F3F8`):** Clean pearlescent light mode designed for high-contrast executive presentations.
* **OLED Executive Obsidian Dark (`#07090E`):** True pitch-black OLED void engineered with a 4-tier Z-axis depth hierarchy (Tier 0 Canvas, Tier 1 Frosted Glass Headers, Tier 2 Elevated Indigo-Slate Decks, Tier 3 Recessed Wells) and razor-thin luminous glass borders (`border-white/[0.08]`).
* **Zero Flickering Init:** Synchronized `localStorage` injection right inside `<head>` prevents wrong-theme flashing during reloads or routing.

## 📂 System Directory Structure

```text
movieBox/
├── app.py               # Core WSGI Server, S3 Boto3 API & HTTP 206 Range Streamer
├── requirements.txt     # Python Dependencies (flask, boto3)
├── movies_catalog.json  # Persisted Asset Manifest Index
├── config.json          # Target AWS Cloud Storage Credentials
├── README.md            # Platform Documentation
├── static/
│   └── style.css        # Bespoke Glassmorphism & Keyframe Animation Rules
└── templates/
    ├── index.html       # Public Showcase Gallery & Cinema Trailer Player
    └── admin.html       # Studio Ingest Console & Manifest Dashboard
```

## 🚀 Quickstart Deployment Guide

### Step 1: Install Python Engine
Ensure Python 3.9+ is installed on your environment. Install required backend packages:

```powershell
pip install -r requirements.txt
```

### Step 2: Initialize WSGI Server
Launch the production web server instance:

```powershell
python app.py
```
The platform will launch instantly on **`http://localhost:3000`**.

### Step 3: Studio Workflow & Curation
1. Open the Studio Management Deck at **`http://localhost:3000/admin`**.
2. Under **Cloud Storage Target**, enter your AWS S3 Bucket Name and Region, then save configuration.
3. Under **Asset Batch Upload**, drag matching pairs of trailer videos (`.mp4`) and promotional posters (`.jpg/.png`) named identically (e.g., `gladiator.mp4` and `gladiator.jpg`).
4. Click **Ingest Media to S3 Vault**. Your assets are immediately chunked and indexed into the active manifest.
5. Launch Showcase **`http://localhost:3000`** to experience instant 4K buffering!

## 🔒 Security & Performance Notes
* **HTTP 206 Partial Content:** Video buffers are requested in byte chunks via Flask generator responses, eliminating browser memory spikes and enabling instant timeline seeking.
* **S3 Security:** Media URLs utilize secure server-side proxies, preventing direct bucket exposure or public CORS policy errors.
