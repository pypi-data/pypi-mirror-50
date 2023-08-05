RED-Metrics-Tracker
===================
Simple RED Metrics tracker able to instrument flask views using prometheus metrics.


Install
=======

With `pip`, of course::

    pip install red-metrics-tracker


Instrumenting
=============

Tracking all methods and exceptions for all requests on a view::

    app = flask.Flask(__name__)

    @app.route("/endpoint")
    @FlaskRedMetricsTracker.track()
    def do_things():
         ...
         return "OK"

Limiting metrics tracking to specific methods::

    @app.route("/endpoint", methods=["POST", "GET", "PUT", "DELETE"])
    @FlaskRedMetricsTracker.track(methods=["POST", "DELETE"])
    def do_things():
         ...
         return "OK"

Limiting to specific exceptions::

    @app.route("/endpoint/<condition>")
    @FlaskRedMetricsTracker.track(exceptions=MySpecialException)
    def do_things():
         ...
         if condition == "throw":
            raise MySpecialException
         return "OK"

Filters may be combined, of course::

    @app.route("/endpoint/<condition>", methods=["POST", "GET", "DELETE"])
    @FlaskRedMetricsTracker.track(methods=["GET", "POST"]exceptions=MySpecialException)
    def do_things():
         ...
         if condition == "throw":
            raise MySpecialException
         return "OK"


Exposition
==========

Feel free to use `prometheus_client` to run an http_server serving a `/metrics` endpoint at its
configured port.

For the people who'd like the `/metrics` endpoint to be part of their flask app, there's a blueprint
for that::

    import flask
    from red import metrics_blueprint

    app = flask.Flask(__name__)
    app.register_blueprint(metrics_blueprint)

Metrics are now available at you app's url under the `/metrics` endpoint.
