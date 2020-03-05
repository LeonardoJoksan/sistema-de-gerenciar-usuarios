from flask import Blueprint, jsonify, request
professores_app = Blueprint(
    'professores_app',
    __name__,
    template_folder='templates')

professores_db = []