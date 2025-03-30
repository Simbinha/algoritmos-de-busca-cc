from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from algoritmoBuscaGraph import (
    bfs, dfs, ucs, dls, iddfs, greedy_best_first_search as greedy, a_star
)

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    algorithm = data.get('algorithm')
    
    result = None
    
    if algorithm == 'bfs':
        result = bfs(start, end)
    elif algorithm == 'dfs':
        result = dfs(start, end)
    elif algorithm == 'ucs':
        result = ucs(start, end)
    elif algorithm == 'dls':
        limit = data.get('limit', 3)
        result = dls(start, end, limit)
    elif algorithm == 'iddfs':
        max_depth = data.get('maxDepth', 10)
        result = iddfs(start, end, max_depth)
    elif algorithm == 'greedy':
        result = greedy(start, end)
    elif algorithm == 'astar':
        result = a_star(start, end)
    
    if result:
        return jsonify(result)
    return jsonify({"error": "Caminho não encontrado"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
