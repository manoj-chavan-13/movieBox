import os
import re
import json
import boto3
from flask import Flask, render_template, request, jsonify, Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = "moviebox_trailer_platform_secret"

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
CATALOG_FILE = os.path.join(BASE_DIR, "movies_catalog.json")
LOCAL_MEDIA_DIR = os.path.join(BASE_DIR, "static", "media")
os.makedirs(LOCAL_MEDIA_DIR, exist_ok=True)

VIDEO_EXTS = [".mp4", ".webm", ".mov", ".mkv", ".avi"]
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp"]

def get_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "bucket_name": "",
        "region": "us-east-1",
        "access_key": "",
        "secret_key": ""
    }

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def get_catalog():
    if os.path.exists(CATALOG_FILE):
        try:
            with open(CATALOG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_catalog(catalog):
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2)

def get_s3_client():
    cfg = get_config()
    session_kwargs = {}
    if cfg.get("region"):
        session_kwargs["region_name"] = cfg["region"]
    if cfg.get("access_key") and cfg.get("secret_key"):
        session_kwargs["aws_access_key_id"] = cfg["access_key"]
        session_kwargs["aws_secret_access_key"] = cfg["secret_key"]
    return boto3.client("s3", **session_kwargs)

@app.route("/")
def index():
    return render_template("index.html", config=get_config())

@app.route("/admin")
def admin():
    return render_template("admin.html", config=get_config())

@app.route("/api/config", methods=["GET", "POST"])
def handle_config():
    if request.method == "GET":
        return jsonify(get_config())
    
    data = request.json or {}
    cfg = {
        "bucket_name": data.get("bucket_name", "").strip(),
        "region": data.get("region", "us-east-1").strip(),
        "access_key": data.get("access_key", "").strip(),
        "secret_key": data.get("secret_key", "").strip()
    }
    save_config(cfg)
    return jsonify({"status": "success", "config": cfg})

@app.route("/api/movies")
def get_movies():
    cfg = get_config()
    bucket = cfg.get("bucket_name")
    catalog = get_catalog()
    
    # Try fetching from S3 if bucket configured
    if bucket:
        try:
            s3 = get_s3_client()
            resp = s3.list_objects_v2(Bucket=bucket)
            contents = resp.get("Contents", [])
            
            all_keys = [obj["Key"] for obj in contents]
            
            movies_dict = {}
            for key in all_keys:
                base, ext = os.path.splitext(key)
                ext_lower = ext.lower()
                if base not in movies_dict:
                    clean_title = re.sub(r'[-_]', ' ', base).title()
                    movies_dict[base] = {
                        "id": base,
                        "title": clean_title,
                        "video_url": None,
                        "poster_url": None,
                        "has_video": False,
                        "has_poster": False,
                        "size_mb": 0
                    }
                if ext_lower in VIDEO_EXTS:
                    movies_dict[base]["video_url"] = f"/s3_media/{key}"
                    movies_dict[base]["has_video"] = True
                    for obj in contents:
                        if obj["Key"] == key:
                            movies_dict[base]["size_mb"] = round(obj.get("Size", 0) / (1024*1024), 2)
                            break
                elif ext_lower in IMAGE_EXTS:
                    movies_dict[base]["poster_url"] = f"/s3_media/{key}"
                    movies_dict[base]["has_poster"] = True
            
            # Merge with existing catalog
            for base_id, item in movies_dict.items():
                if item["has_video"] or item["has_poster"]:
                    catalog[base_id] = item
            save_catalog(catalog)
        except Exception:
            # If S3 connection fails, fallback seamlessly to saved catalog
            pass

    # Convert catalog dict to sorted list
    movie_list = [m for _, m in sorted(catalog.items()) if m.get("has_video") or m.get("has_poster")]
    
    return jsonify({"status": "success", "bucket": bucket or "Local Config Catalog", "movies": movie_list})

@app.route("/api/upload", methods=["POST"])
def upload_files():
    cfg = get_config()
    bucket = cfg.get("bucket_name")
    catalog = get_catalog()
        
    files = request.files.getlist("files")
    if not files or files[0].filename == "":
        return jsonify({"status": "error", "message": "No files selected."}), 400
        
    uploaded_count = 0
    s3 = None
    if bucket:
        try:
            s3 = get_s3_client()
        except Exception:
            pass

    try:
        for f in files:
            if f and f.filename:
                base, ext = os.path.splitext(f.filename)
                ext_lower = ext.lower()
                clean_title = re.sub(r'[-_]', ' ', base).title()
                
                if base not in catalog:
                    catalog[base] = {
                        "id": base,
                        "title": clean_title,
                        "video_url": None,
                        "poster_url": None,
                        "has_video": False,
                        "has_poster": False,
                        "size_mb": 0
                    }

                # Read body once
                body = f.read()
                size_mb = round(len(body) / (1024 * 1024), 2)
                
                # Determine URL storage (S3 or Local)
                media_url = None
                if bucket and s3:
                    mimetype = f.content_type or "application/octet-stream"
                    if ext_lower in [".mp4"]: mimetype = "video/mp4"
                    elif ext_lower in [".webm"]: mimetype = "video/webm"
                    elif ext_lower in [".jpg", ".jpeg"]: mimetype = "image/jpeg"
                    elif ext_lower in [".png"]: mimetype = "image/png"
                    
                    s3.put_object(Bucket=bucket, Key=f.filename, Body=body, ContentType=mimetype)
                    media_url = f"/s3_media/{f.filename}"
                else:
                    # Save locally if S3 not configured
                    local_path = os.path.join(LOCAL_MEDIA_DIR, f.filename)
                    with open(local_path, "wb") as out_f:
                        out_f.write(body)
                    media_url = f"/static/media/{f.filename}"
                
                if ext_lower in VIDEO_EXTS:
                    catalog[base]["video_url"] = media_url
                    catalog[base]["has_video"] = True
                    catalog[base]["size_mb"] = size_mb
                elif ext_lower in IMAGE_EXTS:
                    catalog[base]["poster_url"] = media_url
                    catalog[base]["has_poster"] = True
                    
                uploaded_count += 1
                
        save_catalog(catalog)
        storage_type = f"S3 bucket '{bucket}'" if (bucket and s3) else "Local Config Catalog ('movies_catalog.json')"
        return jsonify({"status": "success", "message": f"Successfully uploaded {uploaded_count} files and saved video/poster links to {storage_type}."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/delete", methods=["POST"])
def delete_movie():
    cfg = get_config()
    bucket = cfg.get("bucket_name")
    catalog = get_catalog()
    base_id = request.json.get("id")
    
    if not base_id:
        return jsonify({"status": "error", "message": "Missing movie id."}), 400
        
    try:
        # Delete from S3 if applicable
        if bucket:
            try:
                s3 = get_s3_client()
                resp = s3.list_objects_v2(Bucket=bucket, Prefix=base_id)
                keys_to_delete = [{'Key': obj['Key']} for obj in resp.get("Contents", [])]
                if keys_to_delete:
                    s3.delete_objects(Bucket=bucket, Delete={'Objects': keys_to_delete})
            except Exception:
                pass
                
        # Delete local files if any
        for ext in VIDEO_EXTS + IMAGE_EXTS:
            p = os.path.join(LOCAL_MEDIA_DIR, base_id + ext)
            if os.path.exists(p):
                try: os.remove(p)
                except Exception: pass
                
        if base_id in catalog:
            del catalog[base_id]
            save_catalog(catalog)
            
        return jsonify({"status": "success", "message": f"Deleted movie media files and config links for '{base_id}'."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/s3_media/<path:key>")
def serve_s3_media(key):
    cfg = get_config()
    bucket = cfg.get("bucket_name")
    if not bucket:
        return "Bucket not configured", 400
        
    try:
        s3 = get_s3_client()
        range_header = request.headers.get("Range")
        get_kwargs = {"Bucket": bucket, "Key": key}
        status_code = 200
        
        if range_header:
            get_kwargs["Range"] = range_header
            status_code = 206
            
        try:
            s3_response = s3.get_object(**get_kwargs)
        except s3.exceptions.ClientError as e:
            if range_header and "InvalidRange" in str(e):
                del get_kwargs["Range"]
                s3_response = s3.get_object(**get_kwargs)
                status_code = 200
            else:
                raise e
                
        headers = {}
        if "ContentType" in s3_response:
            headers["Content-Type"] = s3_response["ContentType"]
        if "ContentLength" in s3_response:
            headers["Content-Length"] = str(s3_response["ContentLength"])
        if "ContentRange" in s3_response:
            headers["Content-Range"] = s3_response["ContentRange"]
        headers["Accept-Ranges"] = "bytes"
        
        def generate():
            for chunk in iter(lambda: s3_response["Body"].read(65536), b""):
                yield chunk
                
        return Response(generate(), status=status_code, headers=headers)
    except Exception as e:
        return f"Error loading media from S3: {e}", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
