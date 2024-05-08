from drf_standardized_errors.openapi import AutoSchema as BaseAutoSchema
from .mixins import StandardizedSchemaMixin


class AutoSchema(StandardizedSchemaMixin, BaseAutoSchema):
    pass
