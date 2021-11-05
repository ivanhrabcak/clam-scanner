import clamd
from flask import Flask, request, jsonify

app = Flask(__name__)

def response(message):
    return jsonify({'response': message})

@app.route('/scan', methods=['POST'])
def scan_file():
    file = request.files.get('file')

    if file == None:
        return response('No file in request!'), 400
    
    try:
        clam = clamd.ClamdNetworkSocket()
        scan_result = clam.instream(file.stream).get("stream")
        clam._close_socket()
    except ConnectionResetError:
        return response('File too large.'), 400
    except (clamd.ConnectionError, ConnectionError) as e:
        return response(f'{e}'), 500

    if len(scan_result) != 2:
        return response("Unexpected response from CLAM's socket."), 500
    
    return jsonify({"response": {"result": scan_result[0], "virus": scan_result[1]}})

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, threaded=True)