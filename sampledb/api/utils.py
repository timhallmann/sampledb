from functools import wraps
import json
import typing

import flask
from flask.views import MethodView
import werkzeug
import werkzeug.exceptions


class Resource(MethodView):
    @classmethod
    def as_view(cls, name: typing.Any, *class_args: typing.Any, **class_kwargs: typing.Any) -> typing.Any:
        return super(Resource, _resource_decorator(cls)).as_view(name, *class_args, **class_kwargs)


def _resource_decorator(cls: typing.Type[Resource]) -> typing.Type[Resource]:
    for method in ['get', 'head', 'post', 'put', 'delete']:
        if hasattr(cls, method) and callable(getattr(cls, method)):
            setattr(cls, method, _resource_method_decorator(getattr(cls, method)))
    return cls


def _resource_method_decorator(f: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Any], typing.Any]:
    @wraps(f)
    def decorator(*args: typing.Any, **kwargs: typing.Any) -> werkzeug.Response:
        flask.request.on_json_loading_failed = _on_json_loading_failed_replacement  # type: ignore
        try:
            response_data = f(*args, **kwargs)
            if isinstance(response_data, werkzeug.Response):
                response = response_data
            else:
                status = 200
                headers = {}
                if isinstance(response_data, tuple) and 1 <= len(response_data) <= 3:
                    message = response_data[0]
                    if len(response_data) >= 2:
                        status = response_data[1]
                    if len(response_data) >= 3:
                        headers = response_data[2]
                else:
                    message = response_data
                if message is None:
                    response = flask.current_app.response_class(
                        message,
                        status=status,
                        headers=headers
                    )
                else:
                    response = _make_json_response(
                        message,
                        status=status,
                        headers=headers
                    )
        except werkzeug.exceptions.HTTPException:
            raise
        except Exception:
            response = _make_json_response(
                obj={'message': 'Internal Server Error'},
                status=500
            )
        return response
    return decorator


def _make_json_response(
        obj: typing.Any,
        status: int = 200,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None
) -> werkzeug.Response:
    if headers is None:
        headers = {}

    indent = None
    separators = (",", ":")
    if flask.current_app.config["JSONIFY_PRETTYPRINT_REGULAR"] or flask.current_app.debug:
        indent = 2
        separators = (", ", ": ")

    return typing.cast(werkzeug.Response, flask.current_app.response_class(
        response=f"{json.dumps(obj=obj, indent=indent, separators=separators)}\n",
        mimetype=flask.current_app.config["JSONIFY_MIMETYPE"],
        status=status,
        headers=headers
    ))


def _on_json_loading_failed_replacement(_e: Exception) -> typing.NoReturn:
    flask.abort(_make_json_response(
        obj={'message': 'Failed to decode JSON object'},
        status=400
    ))
