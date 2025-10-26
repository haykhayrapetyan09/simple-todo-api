from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage
tasks = []

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api')
def api_info():
    return jsonify({
        'service': 'Simple Todo API',
        'version': '1.0',
        'endpoints': {
            'GET /api': 'API info',
            'GET /api/health': 'Health check',
            'GET /api/tasks': 'List all todo tasks',
            'POST /api/tasks': 'Create a todo task',
            'DELETE /api/tasks/<id>': 'Delete a todo task'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'count': len(tasks),
        'tasks': tasks
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = {
        'id': len(tasks) + 1,
        'title': data.get('title', 'Untitled'),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
