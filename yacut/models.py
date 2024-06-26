from datetime import datetime

from yacut import db
from yacut.settings import CUSTOM_ID_MAX_LEN, ORIGINAL_LINK_MAX_LEN

POST_PARAMS = {
    'url': 'original',
    'custom_id': 'short'
}


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LEN), nullable=False)
    short = db.Column(db.String(CUSTOM_ID_MAX_LEN), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short
        )

    def from_dict(self, data):
        for field in POST_PARAMS:
            if field in data:
                setattr(self, POST_PARAMS[field], data[field])
