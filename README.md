# DRF Standardized Response
A set of custom validators for validating date and datetime fields for Django.

## Installation

1. Install the package using pip:

```bash
pip install drf-standardized-response
```

2. Add `drf_standardized_response` to `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    ...,
    "drf_standardized_response",
]
```

3. Add renderer for all API views
```python
"DEFAULT_RENDERER_CLASSES": [
    ...,
    "drf_standardized_response.renderers.StandardizedJSONRenderer",
    ...,
]
```
## Usage