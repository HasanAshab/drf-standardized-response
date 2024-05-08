# DRF Standardized Response
Standarize your API responses

## Table of Contents

- [Installation](#installation)
- [How It Works](#how-it-works)
- [Customizing](#customizing)
  - [Custom Wrapper Key](#custom-wrapper-key)
  - [Excluded Fields From Wrapping](#excluded-fields-from-wrapping)
  - [Wrapping Paginated Response](#wrapping-paginated-response)
  - [Disable Standardization On View](#disable-standardization-on-view)
  - [Custom Response Standarizer](#custom-response-standarizer)
- [DRF-Spectacular Integration](#drf-spectacular-integration)
- [Contributing](#contributing)


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

Now, your API responses will be standardized.

## How It Works
The package takes care of standardization all responses returned by views.

*    if you return a `string` response, it will be wrapped in a `message` key. For example:
```python
class MyView(APIView):
    def get(self, request):
        return Response("Thanks for using DRF Standardized Response")
```

The response will be:

```json
{
    "success": true,
    "message": "Thanks for using DRF Standardized Response"
}
```

*    If your response data contains `message`, it will override the standardized message.

```python
class MyView(APIView):
    def get(self, request):
        return Response({"message": "Thanks for using DRF Standardized Response"})
```

The response will be:

```json
{
    "success": true,
    "message": "Thanks for using DRF Standardized Response"
}
```

<br>

*    if you return a `dict` response, it will be wrapped in a `data` key. For demostration, we will return a user profile.  

```python
class MyView(APIView):
    def get(self, request):
        user = request.user
        data = UserProfileSerializer(user).data
        return Response(data)
```

The response will be:

```json
{
    "success": true,
    "message": "OK",
    "data": { # user profile },
}
```

<br>

*    if you return a `list` or `tuple` response, it will be wrapped in a `data` key. For demostration, we will return a list of user profiles.

```python
class MyView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = UserProfileSerializer(users, many=True).data
        return Response(data)
```

The response will be:

```json
{
    "success": true,
    "message": "OK",
    "data": [ # list of user profiles ],
}
```

## Customizing
### Custom Wrapper Key
You can customize the key used to wrap the response data. By default, the key is `data`. To change it, set the `DEFAULT_WRAPPER_KEY` in pkg settings.

```python
DRF_STANDARDIZED_RESPONSE = {
    "DEFAULT_WRAPPER_KEY": "results",
}
```

Or you can change it per view basis using the `wrapper_key` argument in the view:

```python
class MyView(APIView):
    wrapper_key = "results"
```

### Excluded Fields From Wrapping
You can exclude fields from wrapping. By default, the fields are `links`. To customize it, Set the `DEFFAULT_WRAPPING_EXCLUDED_FIELDS` in pkg settings.

```python
DRF_STANDARDIZED_RESPONSE = {
    "DEFFAULT_WRAPPING_EXCLUDED_FIELDS": ["links", "meta"],
}
``` 

Or you can change it per view basis using the `wrapping_excluded_fields` argument in the view:

```python
class MyView(APIView):
    wrapping_excluded_fields = ["links", "meta"]
```

### Wrapping Paginated Response
By default, paginated responses are not wrapped. To customize this behavior, Set the `WRAP_PAGINATED_RESPONSE` in pkg settings.

```python
DRF_STANDARDIZED_RESPONSE = {
    "WRAP_PAGINATED_RESPONSE": True,
}
```

### Disable Standardization On View
You can disable standardization on a view by setting the `should_strandardize` property to `False`.

```python
class MyView(APIView):
    should_strandardize = False
```

### Custom Response Standarizer
You can also provide your own response standarizer to format response to your desired format. By default, the standarizer is `drf_standardized_response.response_standarizer.ResponseStandardizer`, which is well suitable for most projects.

But if you need that, set the `RESPONSE_STANDARDIZER_CLASS` in pkg settings.

```python
DRF_STANDARDIZED_RESPONSE = {
    "RESPONSE_STANDARDIZER_CLASS": "your_app.response_standarizer.CustomResponseStandardizer",
}
```

## DRF-Spectacular Integration
If you plan to use `drf-spectacular` to generate an OpenAPI 3 schema, 

install with pip:
```bash
pip install drf-standardized-response[openapi].
```

After that, Set the default schema class to the one provided by the package

```python
REST_FRAMEWORK = {
    # other settings
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_response.openapi.AutoSchema"
}
```

Alternatively, you can use the `drf_standardized_response.openapi.mixins.StandardizedAutoSchemaMixin` mixin to your own schema class. (useful when using with [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors)).

Now, the OpenAPI schema will be generated with the standardized response format.

### Disable Schema Standardization On Serializer
You can disable openapi schema standardization on a serializer by setting the `should_standardize_schema` property to `False` on `Meta`.

```python
class MySerializer(serializers.Serializer):
    class Meta:
        should_standardize_schema = False
```

### Contributing
Contributions are more than welcome! Please open an issue if you have any questions or suggestions.