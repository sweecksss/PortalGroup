def theme(request):
    """Поточна тема оформлення — світла або темна, зберігається в сесії."""
    return {'theme': request.session.get('theme', 'light')}
