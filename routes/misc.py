from flask import Blueprint, render_template, request, redirect, Response, send_from_directory, abort, send_file, flash, url_for, session
import os, requests, interpreter
from config import Config

misc_bp = Blueprint('misc', __name__)

@misc_bp.route('/static/uploads/<filename>')
def serve_file(filename):
    output = interpreter.interpreter(filename)
    if output:
        return output
    else:
        return send_from_directory('static/uploads', filename)


@misc_bp.route('/images')
def get_image():
    image = request.args.get('image')
    image_path = os.path.join('static/uploads', image)
    
    if os.path.isfile(image_path):
        return send_file(image_path)

    return abort(404, "Image not found") 


@misc_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')


@misc_bp.route('/preview_post', methods=['POST'])
def preview_post():
    title = request.form.get("title", "")
    content = request.form.get("content", "")
    template = f"""
    <div class="post">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """
    from flask import render_template_string
    return render_template_string(template, title=title)


@misc_bp.route('/fetch')
def fetch():
    url = request.args.get('url', '').strip()
    if not url:
        return "Missing url parameter", 400
    

    if url.startswith(f"http://{Config.HOST}:{Config.PORT}/post/"):
        return redirect(url)
    try:
        r = requests.get(url, timeout=5, verify=False)
        return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "text/html"))
    except Exception as e:
        return f"Error fetching URL: {e}", 500
