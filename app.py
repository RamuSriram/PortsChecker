from flask import Flask, render_template, request
import socket
import threading

app = Flask(__name__)

def scan_port(ip, port, result):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((ip, port))
        result[port] = 'Open'
    except (socket.timeout, socket.error):
        result[port] = 'Closed'
    finally:
        sock.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        open_ports = {}

        # Perform port scan (0 to 65535)
        threads = []
        for port in range(65536):
            thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Filter open ports
        open_ports = {port: status for port, status in open_ports.items() if status == 'Open'}
        return render_template('result.html', ip=ip, open_ports=open_ports)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
