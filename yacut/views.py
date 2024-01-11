from urllib.parse import urljoin

from flask import abort, flash, render_template, redirect, request

from settings import SHORT_LINK_EXIST
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.core import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    TEMPLATE = 'index.html'
    form = URLMapForm()
    form.message = None
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        print(original_link, custom_id)
        if URLMap.query.filter_by(short=custom_id).first():
            flash(SHORT_LINK_EXIST)
            return render_template(TEMPLATE, form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
            while URLMap.query.filter_by(short=custom_id).first():
                custom_id = get_unique_short_id()
        urlmap = URLMap(
            original=original_link,
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        form.message = urljoin(request.base_url, custom_id)
    return render_template(TEMPLATE, form=form)


@app.route('/<string:link>', methods=['GET'])
def redirect_view(link=None):
    urlmap = URLMap.query.filter_by(short=link).first()
    if urlmap:
        original_link = urlmap.original
        return redirect(original_link)
    abort(404)
