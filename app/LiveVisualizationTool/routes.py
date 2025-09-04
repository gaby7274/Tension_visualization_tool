from app.LiveVisualizationTool import bp
from flask import render_template

@bp.route('/')
def virtualMidi():
    return render_template('LiveVisualizationTool/liveVisualizationTool.html', title='Live Visualization Tool')

@bp.route('/test')
def testingMidi():
    return render_template('LiveVisualizationTool/testing.html', title='dimelo')