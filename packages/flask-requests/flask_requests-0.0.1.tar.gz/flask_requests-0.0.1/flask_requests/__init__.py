from typing import Tuple, Any

from flask import request
from pampy import match, _


def get_data(*keys: str, data_source: request = request) -> Tuple[Any, ...]:
    """
    if mimetype is 'application/x-www-form-urlencoded', front end html example:
        action: request url
        name: name is necessary, name is ImmutableMultiDict item key
        <form role="form" action="/download-file/"
                  target="_self"
                  accept-charset="UTF-8"
                  method="POST"
                  autocomplete="off"
                  enctype="application/x-www-form-urlencoded">
            <textarea name="comment"></textarea>
            <input ..../>
        </form>
    :return:
    """
    matched = match(request.mimetype,
                    'application/x-www-form-urlencoded', tuple(data_source.form.get(key, '') for key in keys),
                    'application/json', tuple(data_source.json.get(i) for i in keys),
                    _, None
                    )
    if not matched:
        raise NotImplementedError(f'{request.mimetype} is not implemented')
    return matched


