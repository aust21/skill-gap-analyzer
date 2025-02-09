from flask import Flask, request, g


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = "3d0afe0201361e1d3bc722e94fa110d23f2242a4a10509d2"


    from .views import views
    app.register_blueprint(views, url_prefix="/")
    
    @app.before_request
    def before_request():
        g.current_route = request.endpoint
    
    return app