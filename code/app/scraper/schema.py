from marshmallow import Schema, fields

class ScraperSchema(Schema):
    uuid = fields.Str(required=True)
    source_type = fields.Str()
    title = fields.Str()
    start_uuid = fields.Str()
    parent_uuid = fields.Str()
    step = fields.Str()
    cycle = fields.Str()
    keyword_to_search = fields.Str()
    keyword_match = fields.Str()
    urls = fields.Str()

class UserSchema(Schema):
    uuid = fields.Str()
    email = fields.Email(required=True)