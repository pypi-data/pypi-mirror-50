from bottle import Bottle


class BottleResource(object):
    name = 'bottle_resource'
    api = 2

    def _fetch_api_routes(self):
        return ((key, getattr(value, '_route_config'), value) for key, value in self.__class__.__dict__.items() if
                hasattr(value, '_route_config'))

    def setup(self, app: Bottle = None):
        for api_name, route_config, api_callback in self._fetch_api_routes():
            api_callback._instance = self
            route_config['callback'] = api_callback
            app.route(**route_config)

    def apply(self, api_callback, context=None):

        def wrapper(func):
            def view_func(*args, **kwargs):
                if hasattr(func, '_route_config'):
                    return func(getattr(func, '_instance'), *args, **kwargs)
                return func(*args, **kwargs)

            return view_func

        return wrapper(api_callback)

    def __call__(self, api_callback):
        return self.apply(api_callback)


def api(path, method: str = 'GET', name: str = None, apply=None, skip=None, **config):
    def api_decorator(view_callback):
        view_callback._route_config = {
            'path': path, 'method': method, 'name': name, 'apply': apply, 'skip': skip,
            **config
        }
        return view_callback

    return api_decorator


def api_get(path, name=None, apply=None, skip=None, **config):
    return api(path, 'GET', name, apply, skip, **config)


def api_post(path, name=None, apply=None, skip=None, **config):
    return api(path, 'POST', name, apply, skip, **config)


def api_put(path, name=None, apply=None, skip=None, **config):
    return api(path, 'PUT', name, apply, skip, **config)


def api_patch(path, name=None, apply=None, skip=None, **config):
    return api(path, 'PATCH', name, apply, skip, **config)


def api_delete(path, name=None, apply=None, skip=None, **config):
    return api(path, 'DELETE', name, apply, skip, **config)
