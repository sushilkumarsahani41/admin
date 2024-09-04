from functools import wraps
from django.http import JsonResponse

API_KEY = 'gCW0z7uTiZqbNwoYQsDvE2gAPxdHfXciazPmCzPneXpn444glZ'  # Replace with your fixed API key

def api_key_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get('Authorization')  # Or wherever you expect the API key
        if api_key != f"Bearer {API_KEY}":
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
