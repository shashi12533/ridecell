from flask import request
from flask_restful import Resource
from flask_restful.utils import unpack, OrderedDict
from config import get_config
from werkzeug.wrappers import Response as ResponseBase

CONFIG = get_config()



class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask

        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        for decorator in self.method_decorators:
            meth = decorator(meth)

        try:
            increment(total_requests)
        except Exception as exc:
            pass

        # this is where actual method starts
        
        resp = meth(*args, **kwargs)
        
        # this is where actual method ends

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        mediatype = request.accept_mimetypes.best_match(representations,
                                                        default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp
