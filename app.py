from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import re
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Model ──────────────────────────────────────────────────────────────────────

class URL(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    original   = db.Column(db.String(2048), nullable=False)
    shortened  = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks     = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<URL {self.shortened}>'

# ── Helpers ────────────────────────────────────────────────────────────────────

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(shortened=code).first():
            return code

def is_valid_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template('history.html', urls=urls)

@app.route('/shorten', methods=['POST'])
def shorten():
    data         = request.get_json()
    original_url = (data.get('url') or '').strip()

    if not original_url:
        return jsonify({'error': 'Please enter a URL.'}), 400

    # Auto-prepend scheme if missing
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL. Please enter a valid web address.'}), 400

    # Re-use existing record if URL was already shortened
    existing = URL.query.filter_by(original=original_url).first()
    if existing:
        short_url = request.host_url + existing.shortened
        return jsonify({'short_url': short_url, 'code': existing.shortened})

    code    = generate_short_code()
    new_url = URL(original=original_url, shortened=code)
    db.session.add(new_url)
    db.session.commit()

    short_url = request.host_url + code
    return jsonify({'short_url': short_url, 'code': code})

@app.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(shortened=code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original)

@app.route('/api/stats')
def stats():
    total  = URL.query.count()
    clicks = db.session.query(db.func.sum(URL.clicks)).scalar() or 0
    return jsonify({'total': total, 'clicks': clicks})

@app.route('/delete/<int:url_id>', methods=['DELETE'])
def delete_url(url_id):
    url = URL.query.get_or_404(url_id)
    db.session.delete(url)
    db.session.commit()
    return jsonify({'success': True})

# ── Init ───────────────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)