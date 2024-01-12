from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request

from yacut import app, db
from yacut.core import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.settings import (
    BAD_SHORT_LINK, BODY_IS_NONE,
    CUSTOM_ID_MAX_LEN, CUSTOM_ID_MIN_LEN,
    ID_NOT_FOUND, SHORT_LINK_EXIST, URL_REQUIRED
)


@app.route('/api/id/<string:short_id>/', methods=('GET', ))
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=('POST', ))
def create_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(BODY_IS_NONE)
    custom_id = data.get('custom_id')
    url = data.get('url')
    if not url:
        raise InvalidAPIUsage(URL_REQUIRED)
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(SHORT_LINK_EXIST)
        if len(custom_id) > CUSTOM_ID_MAX_LEN or len(custom_id) < CUSTOM_ID_MIN_LEN:
            raise InvalidAPIUsage(BAD_SHORT_LINK)
        if not custom_id.isalnum():
            raise InvalidAPIUsage(BAD_SHORT_LINK)
    else:
        custom_id = get_unique_short_id()
        while URLMap.query.filter_by(short=custom_id).first():
            custom_id = get_unique_short_id()
    data['custom_id'] = custom_id
    urlmap = URLMap()
    if URLMap.query.filter_by(original=url).first() is not None:
        urlmap = URLMap.query.filter_by(original=url).first()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    response = urlmap.to_dict()
    response['short_link'] = urljoin(request.host_url, response.get('short_link'))
    return jsonify(response), HTTPStatus.CREATED
