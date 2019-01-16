Run the server (srv.py). It will accept UDP messages on port 50000.
The server will report counter statistics every 5 seconds (or when a message comes in).

You can emulate a device by using netcat (like 'nc -u localhost 50000').
Format of the message: "DEVICE_ID Some message here".
