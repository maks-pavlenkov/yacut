import re
from flask import jsonify, request
from http import HTTPStatus
from .error_handlers import InvalidAPIUsage
from .models import URLMap, db
from .views import get_unique_short_id
from . import app


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if data.get('custom_id') is None or not data.get('custom_id'):
        data['short'] = get_unique_short_id()
    else:
        data['short'] = data.get('custom_id')
        if 'custom_id' in data and len(data['custom_id']) > 0 and not re.fullmatch(r'[a-zA-Z0-9]{1,16}', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    data['original'] = data.pop('url')
    if URLMap.query.filter_by(short=data['short']).first():
        raise InvalidAPIUsage(f'Имя "{data["short"]}" уже занято.')
    links = URLMap()
    links.from_dict(data)
    db.session.add(links)
    db.session.commit()
    return jsonify({
        'url': links.to_dict()['original'],
        'short_link': 'http://localhost/' + links.to_dict()['short']
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_id(short_id):
    links = URLMap.query.filter_by(short=short_id).first()
    if links is not None:
        return jsonify({'url': links.to_dict()['original']}), 200
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
