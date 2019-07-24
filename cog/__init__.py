from flask import Flask, request, send_file
from rio_tiler import main
from rio_tiler.utils import array_to_image
from rio_tiler.profiles import img_profiles
import base64
import io

image_options = img_profiles["png"]

app = Flask(__name__)

@app.route('/cog/<b64url>/<z>/<x>/<y>/',  strict_slashes=False, methods=['GET'])
def tile(b64url, x, y, z):
    url = str(base64.b64decode(b64url).decode('utf-8'))
    app.logger.info(f"Getting tile z {z} x {x} y {y} at url {url}")

    tile, mask = main.tile(
        url,
        int(x),
        int(y),
        int(z),
        tilesize=256
    )

    _buffer = array_to_image(tile, mask=mask, img_format="png", **image_options)
    return send_file(
        io.BytesIO(_buffer),
        mimetype='image/png',
        as_attachment=False,
        attachment_filename='tile.jpg'
    )
