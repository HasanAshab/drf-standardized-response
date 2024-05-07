from http.client import responses
from .settings import package_settings


class ResponseStandardizer:
    def __init__(self, view, request):
        self.view = view
        self.request = request

    def get_wrapper_key(self):
        return getattr(
            self.view, "wrapper_key", package_settings.DEFFAULT_WRAPPER_KEY
        )

    def get_wrapping_excluded_fields(self):
        return getattr(
            self.view,
            "wrapping_excluded_fields",
            package_settings.DEFFAULT_WRAPPING_EXCLUDED_FIELDS,
        )

    def get_standard_message(self, response):
        return responses[response.status_code]

    def is_successful_response(self, response):
        return 199 < response.status_code < 400

    def is_paginated_response(self, response):
        pagination = getattr(
            self.view,
            "pagination_class",
            None,
        )
        return pagination is not None and self.request.method == "GET"

    def should_standardize(self):
        return getattr(
            self.view,
            "should_strandardize",
            True,
        )

    def should_wrap(self, response):
        if (
            not package_settings.WRAP_PAGINATED_RESPONSE
            and self.is_paginated_response(response)
        ):
            return False

        if not self.is_successful_response(response):
            return False

        return True

    def standardize(self, response):
        wrapper_key = self.get_wrapper_key()
        is_successful = self.is_successful_response(response)
        standard_message = self.get_standard_message(response)
        standardized_data = {} if response.data is None else response.data

        if isinstance(standardized_data, str):
            standardized_data = {"message": standardized_data}
        elif self.should_wrap(response):
            if isinstance(standardized_data, dict):
                unwrapped_data = {}
                for field in self.get_wrapping_excluded_fields():
                    try:
                        unwrapped_data[field] = standardized_data.pop(field)
                    except KeyError:
                        continue

                standardized_data = {
                    wrapper_key: standardized_data,
                    **unwrapped_data,
                }
            elif isinstance(standardized_data, (list, tuple)):
                standardized_data = {
                    wrapper_key: standardized_data,
                }

        if isinstance(standardized_data, dict):
            if "success" not in standardized_data:
                standardized_data["success"] = is_successful
            if "message" not in standardized_data:
                standardized_data["message"] = standard_message

        return standardized_data
