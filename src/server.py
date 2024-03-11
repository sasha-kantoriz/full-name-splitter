from flask import Flask, request, jsonify
from splitter import splitter


app = Flask(__name__)


@app.route('/')
def entrypoint():
    full_name = request.args.get('full_name')
    if full_name is None:
        return jsonify({'status': 'Error: Missing payload', 'message': '"full_name" query argument is required.'})
    first_name, last_name = splitter(full_name)
    return jsonify({'first_name': first_name, 'last_name': last_name})
