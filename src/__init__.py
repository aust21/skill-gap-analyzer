from flask import Flask, request, g
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def create_app():
    app = Flask(__name__, static_folder='frontend/static',
                template_folder='frontend/templates')
    app.config['SECRET_KEY'] = "3d0afe0201361e1d3bc722e94fa110d23f2242a4a10509d2"


    from .frontend.views import views
    app.register_blueprint(views, url_prefix="/")
    
    @app.before_request
    def before_request():
        g.current_route = request.endpoint
    
    return app