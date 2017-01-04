"""Configuration for this app's routes."""


def includeme(config):
    """Configuration for this app's routes."""
    config.add_static_view('static', 'gist_app:static')
    config.add_route('list', '/')
    config.add_route('detail', '/profile/{id:\d+}')
    config.add_route('create', '/new-profile')
    config.add_route('edit', '/profile/{id:\d+}/edit')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('delete', '/delete/{id:\d+}')
    config.add_route('api_list', '/api/profiles')
