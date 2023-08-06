from json import load, dump


def collection_json():
    """Returns JSON skeleton for Postman schema."""
    collection_json = {
        "info": {
            "name": "Test_collection",
            "description": "Generic text used for documentation.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [],
    }
    return collection_json


def atomic_request():
    """Returns an atomic Postman request dictionary."""

    request = {
        "name": "test request",
        "request": {
            "method": "GET",
            "header": [
                {
                    "key": "Content-Type",
                    "name": "Content-Type",
                    "value": "application/json",
                    "type": "text",
                }
            ],
            "url": {
                "raw": "{{target_url}}endpoint",
                "host": ["{{target_url}}endpoint"],
            },
            "description": "This description can come from docs strings",
        },
        "response": [],
    }
    return request


def basic_JSON(collection_name, app, api_json=collection_json()):
    """Formats the Postman collection with 'collection_name' and doc string from Sanic app.

    Returns JSON dictionary."""
    api_json["info"]["name"] = collection_name
    api_json["info"]["description"] = app.__doc__
    return api_json


# blueprint routes
def get_blueprints(app):
    """Returns a dict of blueprints."""
    return app.blueprints


def get_blueprint_docs(blueprints, blueprint):
    """Returns doc string for blueprint."""
    doc_string = blueprints[blueprint].__doc__
    return doc_string


def get_blueprint_routes(blueprints, blueprint):
    """Return a list of routes."""
    routes = blueprints[blueprint].routes
    return routes


def get_blueprint_route_name(route):
    """Returns route name."""
    name = route[1]
    return name


def get_doc_string(route):
    """Return doc string for function in blueprint route."""
    return route[0].__doc__


def get_route_method(route):
    """Return route CRUD method (GET, POST, etc) from route."""
    return route[2][0]


def get_url_prefix(blueprints, blueprint):
    prefix = blueprints[blueprint].version + blueprints[blueprint].url_prefix
    return prefix


# build the json from blueprints
def add_blueprint_folders(api_json, blueprints):
    """Converts each blueprint into a dictionary with a name, item =[], and description.

    These dictionaries become Postman folders. The "item" dict will contain the endpoins
    for each blueprint.

    Returns a list of dictionary items."""
    for blueprint in blueprints:
        postman_folder = {}
        postman_folder["name"] = blueprint
        postman_folder["item"] = []
        postman_folder["description"] = get_blueprint_docs(blueprints, blueprint)
        api_json["item"].append(postman_folder)
    return api_json


def format_blueprint_request(blueprints, blueprint, route):
    """Populates atomic_request dictionary with route metatdata.

    Assumes route is a list of route items, e.g, function, url, methods

    Returns a postman formatted dictionary request item."""
    request = atomic_request()
    request["name"] = get_blueprint_route_name(route)
    request["request"]["method"] = get_route_method(route)
    request["request"]["url"]["raw"] = (
        "{{target_url}}" + get_url_prefix(blueprints, blueprint) + request["name"]
    )
    request["request"]["url"]["host"] = [request["request"]["url"]["raw"]]
    request["request"]["description"] = get_doc_string(route)
    return request


def populate_blueprints(api_json, blueprints):
    """Populates endpoints for each blueprint folder."""
    for blueprint in blueprints:
        items = []
        for route in get_blueprint_routes(blueprints, blueprint):
            items.append(format_blueprint_request(blueprints, blueprint, route))
        api_json["item"].append(
            {
                "name": blueprint,
                "description": get_blueprint_docs(blueprints, blueprint),
                "item": items,
            }
        )

    return api_json


# app routes
def get_app_routes(app):
    """Return routes in main app."""
    routes = {}
    for route in app.router.routes_names:
        if "." not in route:
            routes[route] = app.router.routes_names[route]
    return routes


def get_app_route_name(routes, route):
    """Return app route name."""
    name = routes[route][0]
    return name


def get_app_route_url(routes, route):
    """Return app route name."""
    name = routes[route][1].name
    return name


def get_app_route_methods(routes, route):
    """Return CRUD methods for routes in main app."""
    methods = list(routes[route][1].methods)
    return methods


def get_app_route_doc_string(routes, route, method):
    """Returns doc string for embedded route functions."""
    try:
        doc = routes[route][1][0].handlers[method].__doc__
    except AttributeError:
        doc = routes[route][1][0].__doc__
    return doc


def format_app_request(routes, route, method):
    """Populates atomic_request dictionary with route metatdata.

    Returns a postman formatted dictionary request item."""
    request = atomic_request()
    request["name"] = get_app_route_name(routes, route)
    request["request"]["method"] = method
    request["request"]["url"]["raw"] = "{{target_url}}" + get_app_route_url(
        routes, route
    )
    request["request"]["url"]["host"] = [request["request"]["url"]["raw"]]
    request["request"]["description"] = get_app_route_doc_string(routes, route, method)
    return request


def add_app_requests(api_json, app):
    """Add requests defined in main to api JSON dict."""
    routes = get_app_routes(app)
    for route in routes:
        methods = get_app_route_methods(routes, route)
        for method in methods:
            request = format_app_request(routes, route, method)
            api_json["item"].append(request)
    return api_json


# export JSON
def save_as_json(collection_name, filename="postman_collection.json"):
    """Write dict to JSON file."""

    with open(filename, "w") as file:
        dump(collection_name, file, indent=4)


def generate_json(
    collection_name, app, filename="postman_collection.json", existing_file=None
):
    """Generates json script from Sanic docs.

    Parameters
    ----------
    collection_name: str
        title of collection
    app: Sanic class
        Sanic app
    filename: str (optional)
        location of output file
    existing_file: str (optional)
        location of existing file, used to copy previous postman_id key
    """
    # build basic json schema
    collection = basic_JSON(collection_name, app)
    # populate blueprint requests
    collection = populate_blueprints(collection, app)
    # populate main app requests
    add_app_requests(collection, app)
    # save dict to JSON file
    save_as_json(collection)

