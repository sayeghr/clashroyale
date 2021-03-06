'''
MIT License

Copyright (c) 2017 kyb3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

class RequestError(Exception):
    '''Base class for all errors'''
    pass

class StatusError(RequestError):
    '''Base class for all errors except NotResponding'''
    def __init__(self, resp, data):
        self.response = resp
        self.code = getattr(resp, 'status', None) or getattr(resp, 'status_code')
        self.method = getattr(resp, 'method', None)
        self.reason = resp.reason
        if isinstance(data, dict):
            self.error = data.get('error')
            if 'message' in data:
                self.error = data.get('message')
        else:
            self.error = data
        self.fmt = '{0.reason} ({0.code}): {0.error}'.format(self)
        super().__init__(self.fmt)

class NotResponding(RequestError):
    '''Raised if the API request timed out'''
    def __init__(self):
        self.code = 504
        self.error = 'API request timed out, please be patient.'
        super().__init__(self.error)

class NotFoundError(StatusError):
    '''Raised if the player/clan is not found.'''
    pass

class ServerError(StatusError):
    '''Raised if the api service is having issues'''
    pass

class Unauthorized(StatusError):
    '''Raised if you passed an invalid token.'''
    pass

class NotTrackedError(StatusError):
    '''Raised if the requested clan is not tracked'''
    pass

class RatelimitError(StatusError):
    '''Raised if ratelimit is hit'''
    pass

class RatelimitErrorDetected(RequestError):
    '''Raised when a ratelimit error is detected'''
    def __init__(self, retry_when):
        self.code = 429
        self.retry_when = retry_when
        self.reason = self.error = 'Too many requests detected, retry in ' + str(self.retry_when)
        self.fmt = '{0.reason} ({0.code}): {0.error}'.format(self)
        super().__init__(self.fmt)