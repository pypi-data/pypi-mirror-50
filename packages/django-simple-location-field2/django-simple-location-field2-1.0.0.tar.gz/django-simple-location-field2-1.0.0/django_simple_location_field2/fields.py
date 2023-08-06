from django.db import models
from .location import Location
from django.utils.encoding import smart_text


class LocationField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 42
        super(LocationField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super(LocationField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        if not value or value == "None":
            return None
        if isinstance(value, Location):
            return value
        if isinstance(value, list):
            return Location(value[0], value[1])
        value_parts = value.rsplit(",")
        try:
            latitude = value_parts[0]
        except IndexError:
            latitude = "0.0"
        try:
            longitude = value_parts[1]
        except IndexError:
            longitude = "0.0"
        return Location(latitude, longitude)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return smart_text(value)
