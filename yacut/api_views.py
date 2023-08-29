from flask import jsonify, request
from . import app
from .models import URLMap, db
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('В теле отсуствует обязательное поле!')
    data['original'] = data.pop('url')
    data['short'] = data.get('custom_id', get_unique_short_id())
    if URLMap.query.filter_by(short=data['short']).first():
        raise InvalidAPIUsage('В базе данных уже есть такой вариант ссылки!')
    links = URLMap()
    links.from_dict(data)
    db.session.add(links)
    db.session.commit()
    return jsonify({'links': links.to_dict()}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_id(short_id):
    print(short_id)
    links = URLMap.query.filter_by(short=short_id).first()
    print(links)
    if links is not None:
        return jsonify({'links': links.to_dict()}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
