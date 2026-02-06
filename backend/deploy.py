import threading

import ws_app as app
import ws_auth as auth
import ws_socket as socket

if __name__ == "__main__":
    threading.Thread(None, app.main, "WebApp-Server").start()
    threading.Thread(None, auth.main, "Authentication-Server").start()
    threading.Thread(None, socket.main, "RealTime-Server").start()