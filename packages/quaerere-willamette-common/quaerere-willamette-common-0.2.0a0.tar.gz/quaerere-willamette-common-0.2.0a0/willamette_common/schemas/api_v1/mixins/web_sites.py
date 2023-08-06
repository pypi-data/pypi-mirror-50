__all__ = ['WebSiteFieldsMixin']

from marshmallow import fields


class WebSiteFieldsMixin:
    url = fields.Url(required=True)
    inLanguage = fields.String()
