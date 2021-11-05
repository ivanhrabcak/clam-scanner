import clamd
from flask import Flask, request, jsonify

app = Flask(__name__)

def response(message):
    return jsonify({'response': message})

@app.route('/scan', methods=['POST'])
async def scan_file():
    file = request.files.get('file')

    if file == None:
        return response('No file in request!'), 400
    
    try:
        clam = clamd.ClamdNetworkSocket()
        scan_result = clam.instream(file.stream)
        clam._close_socket()
    except ConnectionResetError:
        return response('File too large.'), 400
    except (clamd.ConnectionError, ConnectionError) as e:
        return response(f'There was an error while communicating with the CLAM socket'), 500

    return response(scan_result.get('stream')), 200

app.run('0.0.0.0', 8080, threaded=True)