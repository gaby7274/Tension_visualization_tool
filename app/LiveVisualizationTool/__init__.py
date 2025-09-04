from flask import Blueprint

bp = Blueprint('liveVisualizationTool', __name__)

from app.LiveVisualizationTool import routes   