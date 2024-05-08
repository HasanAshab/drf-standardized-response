from django.test.client import RequestFactory
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse
from drf_standardized_response.settings import package_settings


class StandardizedSchemaMixin:
    def _get_response_for_code(
        self, serializer, status_code, media_types=None, direction="response"
    ):
        dummy_request = RequestFactory().get(self.path)
        self._response_standardizer = (
            package_settings.RESPONSE_STANDARDIZER_CLASS(
                view=self._view,
                request=dummy_request,
            )
        )

        response = super()._get_response_for_code(
            serializer, status_code, media_types, direction
        )
        if not (content := response.get("content")):
            return response
        if "application/json" not in content:
            return response

        schema = content["application/json"]["schema"]
        reference = schema.get("$ref", schema.get("items", {}).get("$ref"))
        if not reference:
            return response
        if "ErrorResponse" in reference:
            return response

        if isinstance(serializer, OpenApiResponse):
            serializer = serializer.response
        serializer_meta = getattr(serializer, "Meta", {})

        if not (
            getattr(serializer_meta, "should_standardize_schema", True)
            and self._response_standardizer.should_standardize()
        ):
            return response

        formatted_schema = self._standardize_response_schema(reference)
        content["application/json"]["schema"] = formatted_schema
        return response

    def _standardize_response_schema(self, reference):
        dummy_response = Response(status=200)
        standardized_schema = {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
            },
        }

        if not self._response_standardizer.should_wrap(dummy_response):
            return {
                "allOf": [
                    {"$ref": reference},
                    standardized_schema,
                ]
            }

        schema_name = reference.split("/")[-1]
        schema_key = (schema_name, "schemas")
        schema = self.registry._components[schema_key].schema
        unwrapped_fields = (
            self._response_standardizer.get_wrapping_excluded_fields()
        )
        unwrapped_data = {
            field: schema["properties"].pop(field, None)
            for field in unwrapped_fields
            if field is not None
        }

        standardized_schema["properties"].update(unwrapped_data)
        standardized_schema["properties"]["data"] = schema

        return standardized_schema
