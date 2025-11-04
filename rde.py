from flask import Flask, request, redirect, jsonify
import string, random

app = Flask(__name__)

# Store short links in memory (use a database in production)
url_map = {}

def generate_short_code(length=6):
    """Generate a random short code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return '''
        <h2>Local Short Link Generator</h2>
        <form action="/shorten" method="post">
            <input type="text" name="url" placeholder="Enter URL" size="40" required>
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    short_code = generate_short_code()
    url_map[short_code] = url
    short_url = f"http://localhost:5000/{short_code}"
    return f'Short link created: <a href="{short_url}">{short_url}</a><br><br><a href="/">Back</a>'

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to the original URL"""
    if short_code in url_map:
        return redirect(url_map[short_code])
    else:
        return "Short link not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
