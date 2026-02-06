## WIP
## https://docs.godotengine.org/en/stable/tutorials/networking/websocket.html
## Custom base class for WebSocket connections

class_name SocketClient
extends Node

signal connected
signal disconnected

signal message_received(data: Variant)

@export var endpoint: String = Config.SOCKET_URL
var is_connected: bool = false

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()
var last_state = WebSocketPeer.STATE_CLOSED

func send_json(data: Variant):
	socket.send_text(JSON.stringify(data))

func initialize():
	print("[SocketClient] Running Ready!")
	# Initiate connection to the given URL.
	var err = socket.connect_to_url(endpoint)
	if err == OK:
		print("[SocketClient] Connecting to %s..." % endpoint)
	else:
		push_error("[SocketClient] Unable to connect.")
		set_process(false)

func _on_string_packet(data: String):
	pass

func _on_binary_packet(data: PackedByteArray):
	pass

func _process(_delta):
	# Call this in `_process()` or `_physics_process()`.
	# Data transfer and state updates will only happen when calling this function.
	socket.poll()

	# get_ready_state() tells you what state the socket is in.
	var state = socket.get_ready_state()

	# `WebSocketPeer.STATE_OPEN` means the socket is connected and ready
	# to send and receive data.
	if state == WebSocketPeer.STATE_OPEN:
		is_connected = true
		if last_state == WebSocketPeer.STATE_CLOSED:
			connected.emit()
		
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			if socket.was_string_packet():
				var packet_text = packet.get_string_from_utf8()
				print("[SocketClient] Got text data from server: %s" % packet_text)
				message_received.emit(packet_text)
				_on_string_packet(packet_text)
			else:
				print("[SocketClient] Got binary data from server: %d bytes" % packet.size())
				message_received.emit(packet)
	# `WebSocketPeer.STATE_CLOSING` means the socket is closing.
	# It is important to keep polling for a clean close.
	elif state == WebSocketPeer.STATE_CLOSING:
		pass

	# `WebSocketPeer.STATE_CLOSED` means the connection has fully closed.
	# It is now safe to stop polling.
	elif state == WebSocketPeer.STATE_CLOSED:
		# The code will be `-1` if the disconnection was not properly notified by the remote peer.
		is_connected = false
		disconnected.emit()
		var code = socket.get_close_code()
		print("[SocketClient] WebSocket closed with code: %d. Clean: %s" % [code, code != -1])
		set_process(false) # Stop processing.

func _ready() -> void:
	initialize()
