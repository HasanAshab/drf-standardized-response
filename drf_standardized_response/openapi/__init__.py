from drf_spectacular.openapi import AutoSchema as BaseAutoSchema
from .mixins import StandardizedSchemaMixin


class AutoSchema(StandardizedSchemaMixin, BaseAutoSchema):
    pass
