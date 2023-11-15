from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/',  methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    user_notes = Note.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, user_notes=user_notes)

@views.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully'})
        else:
            return jsonify({'message': 'Unauthorized to delete this note'})
    else:
        return jsonify({'message': 'Note not found'})
