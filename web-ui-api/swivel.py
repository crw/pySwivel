from flask import Flask, url_for, render_template, Response
app = Flask(__name__)

from PanTiltSwivel import PanTiltSwivel

##
# WEBSITE
##
@app.route('/')
def index():
    data = {
        'jquery_js': url_for('static', filename='jquery-1.8.1.js'),
        'bootstrap_css': url_for('static', filename='bootstrap/css/bootstrap.css'),
        'bootstrap_js': url_for('static', filename='bootstrap/js/bootstrap.js'),
        'pantilt_js': url_for('static', filename='pantilt.js')
    }
    return render_template('index.html', data=data)


##
# API
##
@app.route('/pan/')
@app.route('/pan/<int:degree>', methods=['POST', 'PUT'])
def pan(degree):
    app.logger.info('pan to ' + str(degree))
    pantilt = PanTiltSwivel()
    pantilt.pan(degree)
    resp = Response('', status=200, mimetype='application/json')
    return resp


@app.route('/tilt/')
@app.route('/tilt/<int:degree>', methods=['POST', 'PUT'])
def tilt(degree):
    app.logger.info('tilt to ' + str(degree))
    pantilt = PanTiltSwivel()
    pantilt.tilt(degree)
    resp = Response('', status=200, mimetype='application/json')
    return resp


@app.route('/location/<int:loc_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def location(loc_id):
    # POST saves a location
    # PUT modifies a saved location
    # DELETE removes a saved location
    # GET moves the pan/tilt to a saved location
    pass;


@app.route('/locations/')
def locations():
    # GET gets a list of all saved locations
    pass;


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)