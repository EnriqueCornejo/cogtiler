from flask import Flask, request, send_file, abort, jsonify
from rio_tiler import main
from rio_tiler.utils import array_to_image
from rio_tiler.profiles import img_profiles
from rio_tiler.errors import TileOutsideBounds
import base64
import io

image_options = img_profiles["png"]

app = Flask(__name__)

@app.route('/cog/<b64url>/<z>/<x>/<y>/',  strict_slashes=False, methods=['GET'])
def tile(b64url, x, y, z):
    url = str(base64.b64decode(b64url).decode('utf-8'))
    app.logger.debug(f"Getting tile z {z} x {x} y {y} at url {url}")
    try:
        tile, mask = main.tile(
            url,
            int(x),
            int(y),
            int(z),
            tilesize=256
        )
    except TileOutsideBounds as e:
        app.logger.debug("Tile out of bounds")
        return abort(404)
    
    _buffer = array_to_image(tile, mask=mask, img_format="png", **image_options)
    del tile, mask
    return send_file(
        io.BytesIO(_buffer),
        mimetype='image/png',
        as_attachment=False,
        attachment_filename='tile.jpg'
    )

@app.route('/cog/<b64url>/',  strict_slashes=False, methods=['GET'])
def metadata(b64url):
    url = str(base64.b64decode(b64url).decode('utf-8'))
    app.logger.debug(f"Getting metadata at url {url}")
    try:
        metadata = main.metadata(url)
        app.logger.debug(metadata)
    except Exception as e:
        app.logger.debug(e)
        return abort(500)
    return jsonify(metadata)
