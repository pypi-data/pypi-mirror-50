__all__ = ['WebPageFieldsMixin']

from marshmallow import fields


class WebPageFieldsMixin:
    text = fields.String()
    url = fields.Url(required=True)
    web_site_key = fields.String(required=True)
