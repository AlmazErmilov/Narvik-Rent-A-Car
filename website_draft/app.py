from flask import Flask, send_from_directory, abort
import os

# Path to the static folder (correcting the path)
static_folder_path = os.path.dirname(os.path.abspath(__file__))

# Print the static folder path for debugging
print(f"Static folder path: {static_folder_path}")

app = Flask(__name__, static_folder=static_folder_path)

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        app.logger.error(f"Error: {e}")
        abort(404)

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
    