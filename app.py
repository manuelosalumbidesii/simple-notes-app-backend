from flask import Flask, request, jsonify
import uuid
from util import read_notes, write_notes

app = Flask(__name__)

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = read_notes()
    return jsonify(notes), 200

@app.route('/api/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    notes = read_notes()
    note = next((n for n in notes if n['id'] == note_id), None)
    if note:
        return jsonify(note), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/api/notes', methods=['POST'])
def add_note():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        new_note = {
            'id': str(uuid.uuid4()),
            'title': data.get('title'),
            'content': data.get('content')
        }
        notes = read_notes()
        notes.append(new_note)
        write_notes(notes)
        return jsonify(new_note), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    notes = read_notes()
    for note in notes:
        if note['id'] == note_id:
            note['title'] = data.get('title', note['title'])
            note['content'] = data.get('content', note['content'])
            write_notes(notes)
            return jsonify(note), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    notes = read_notes()
    new_notes = [note for note in notes if note['id'] != note_id]
    if len(new_notes) == len(notes):
        return jsonify({'error': 'Note not found'}), 404
    write_notes(new_notes)
    return jsonify({'message': 'Note deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
