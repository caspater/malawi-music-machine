import os
import os.path
from flask import Flask, g, request, jsonify, send_from_directory
from collect.bundle import Bundle

base_name = os.path.dirname(os.path.abspath(__file__))
WEBAPP_PUBLIC_DIRECTORY = os.path.abspath(os.path.join(base_name, "..", "webapp", "public"))
BUNDLES_DIRECTORY =  os.path.join(WEBAPP_PUBLIC_DIRECTORY, 'bundles')
# Set the static directory as the download directory
os.environ['MMM_DOWNLOAD_DIR'] = BUNDLES_DIRECTORY

app = Flask(__name__, 
    static_url_path='/public',
    static_folder=WEBAPP_PUBLIC_DIRECTORY)

app.debug = True
MAX_BUNDLE_SIZE = app.config['MAX_BUNDLE_SIZE'] if 'MAX_BUNDLE_SIZE' in app.config else 10

@app.route("/artists", methods = [ "GET" ])
def get_artists():
    pass

@app.route("/artists/:name", methods = [ "GET" ])
def get_artist():
    pass

@app.route("/artists/:name/songs", methods = [ "GET" ])
def get_artist_songs():
    pass  

@app.route("/artists/:name/albums", methods = [ "GET" ])
def get_artist_albums():
    pass

@app.route("/songs", methods = [ "GET" ])
def get_songs():
    pass

@app.route("/songs/:id/:name", methods = [ "GET" ])
def get_song():
    pass

@app.route("/albums", methods = [ "GET" ])
def get_albums():
    pass
    
@app.route("/albums/:id/:name", methods = [ "GET" ])
def get_album():
    pass

@app.route("/bundles/<string:bundle_name>.tar.gz", methods = [ "GET" ])
def create_bundle_request(bundle_name):
    ids_query = request.args.get('ids', '')
    ids = ids_query.split(',')

    if len(ids) < 0:
        return jsonify({ 'message': 'No song ids given. Bundle will not be created', 'error' : True }), 400
    
    if  len(ids) > MAX_BUNDLE_SIZE:
        return jsonify({ 'message': 'Too many song ids', 'error' : True }), 400
    
    bundle_request = Bundle(bundle_name, ids, 'tar')
    # this might take some time :/
    bundle_request.create_bundle()
    # logger.info("Sending bundle:", bundle_request.archive_name)
    return send_from_directory(BUNDLES_DIRECTORY,
                               bundle_request.archive_name)