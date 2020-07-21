import os
from flask import Flask, jsonify, request, render_template
from autocomplete import generate_completions
from model import getModel

app = Flask(__name__)
PORT = 13000
datapath = os.path.join(os.path.dirname(__file__), 'sample_conversations.json')
trie = getModel(datapath)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def get_autocomplete_results():
    query = request.args.get('query')
    try:
        max_results = int(request.args.get('max_results'))
    except:
        max_results = None
    results = generate_completions(trie, query, max_results=max_results)
    return jsonify({'Completions': results})

if __name__ == '__main__':
    app.run(debug=True, port=PORT)