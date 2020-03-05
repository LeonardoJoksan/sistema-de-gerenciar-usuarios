from flask import Blueprint, jsonify, request
alunos_app = Blueprint(
    'alunos_app',
    __name__,
    template_folder='templates')

alunos_db = []