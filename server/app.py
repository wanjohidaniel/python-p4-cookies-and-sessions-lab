#!/usr/bin/env python3

import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get(id)
    if article is None:
        return make_response(jsonify({'error': 'article not found'}), 404)

    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1

    if session['page_views'] <= 3:
        return make_response(jsonify(article.to_dict()), 200)
    else:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

@app.route('/clear', methods=['GET'])
def clear_session():
    session.clear()
    return make_response(jsonify({'message': 'session cleared'}), 200)

if __name__ == '__main__':
    app.run(port=5555)