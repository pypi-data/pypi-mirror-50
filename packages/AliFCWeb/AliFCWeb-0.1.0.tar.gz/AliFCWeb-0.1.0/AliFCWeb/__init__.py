__version__ = '0.1.0'

from .fcweb import (
    fcIndex, get, post, put, delete
)

from .response import ResponseEntity

from .utils import (
    responseFormat, pathMatch, getBodyAsJson, getBodyAsStr
)