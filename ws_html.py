import usocket as socket
import uos
import network
import websocket
import websocket_helper

CONTENT = b"""\
<!DOCTYPE HTML>
<html>
  <head> 
    <title>ESPGeiger CPM</title>
  </head>
  <body>
    <label id="CPM"></label>
    <script type="text/javascript">
      if ("WebSocket" in window)
      {
        var ws = new WebSocket("ws://%s:5000/");
        
        ws.onmessage = function (evt) 
        {
          var CPM_label = document.getElementById("CPM");
            CPM_label.innerHTML = evt.data;
        };
      }
      else
      {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
      }
    </script>
  </body>
</html>
"""

def send_CPM():


listen_s = None
client_s = None

def setup_conn(port, accept_handler):
    global listen_s
    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][4]

    listen_s.bind(addr)
    listen_s.listen(1)
    if accept_handler:
        listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
    for i in (network.AP_IF, network.STA_IF):
        iface = network.WLAN(i)
        if iface.active():
            print("WebREPL daemon started on ws://%s:%d" % (iface.ifconfig()[0], port))
    return listen_s


def accept_conn(listen_sock):
    global client_s
    cl, remote_addr = listen_sock.accept()
    print("\nWebREPL connection from:", remote_addr)
    client_s = cl
    websocket_helper.server_handshake(cl)
    ws = websocket.websocket(cl, True)
    ws = _webrepl._webrepl(ws)
    cl.setblocking(False)
    # notify REPL on socket incoming data
    cl.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
    uos.dupterm(ws)

def stop():

def start():
    # First start WebSockets server

    # Now start webserver