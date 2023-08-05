import buzz
import connexion
import flask
import functools
import http


class ConnexionBuzz(buzz.Buzz, connexion.ProblemException):
    headers = None
    status_code = http.HTTPStatus.BAD_REQUEST

    def __init__(self, message, *format_args, **format_kwds):
        super().__init__(message=message, *format_args, **format_kwds)

        connexion.ProblemException.__init__(
            self=self,
            status=self.status_code,
            title=message,
            type=repr(self))

    @property
    def description(self):
        return self.message

    def jsonify(self, description=None, headers=None):
        """
        Returns a representation of the error in a jsonic form that is
        compatible with flask's error handling.

        Keyword arguments allow custom error handlers to override parts of the
        exception when it is jsonified
        """
        description = description or self.description

        headers = headers or self.headers

        response = flask.jsonify({
            'code': repr(self),
            'description': description,
        })

        response.status_code = self.status_code

        if headers is not None:
            response.headers = headers

        return response

    @staticmethod
    def build_error_handler(*tasks):
        """
        Provides a generic error function that packages
        a connexion_buzz exception so that it can be handled
        nicely by the flask error handler::

            app.register_error_handler(
                ConnexionBuzz, ConnexionBuzz.build_error_handler(),
            )

        Additionally, extra tasks may be applied to the error prior to
        packaging::

            app.register_error_handler(
                ConnexionBuzz,
                build_error_handler(print, lambda e: foo(e)),
            )

        This latter example will print the error to stdout and also call the
        foo() function with the error prior to packaging it for flask's handler
        """

        def _handler(error, tasks=[]):
            [t(error) for t in tasks]

            response = error.jsonify()
            return response, response.status_code, error.headers

        return functools.partial(_handler, tasks=tasks)
