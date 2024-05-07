from rest_framework.renderers import JSONRenderer as DefaultJSONRenderer
from .settings import package_settings


class StandardizedJSONRenderer(DefaultJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        response_standardizer = package_settings.RESPONSE_STANDARDIZER_CLASS(
            view=renderer_context["view"],
            request=renderer_context["request"],
        )
        if response_standardizer.should_standardize():
            data = response_standardizer.standardize(
                renderer_context["response"]
            )

        return super().render(data, accepted_media_type, renderer_context)
