


from typing import Callable

from main.api.foundation.endpoint import Endpoint


class HttpRequester:
    def __init__(
            self, 
            request_spec: dict, 
            endpoint: Endpoint, 
            response_spec: Callable
        ) -> None:

        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec