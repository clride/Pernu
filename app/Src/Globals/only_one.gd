## https://github.com/clride/Godot-OnlyOne/tree/main
## License: MIT

class_name OnlyOne
extends Node

## Change this number if your game closes even though there's only
## one instance running; you may have a port conflict with another application.
const PORT := 6453

const ADDRESS := "127.0.0.1"
const BUFFER_SIZE := 4096

var _lock_socket: PacketPeerUDP
var _server: TCPServer
var _listening := false
var _arguments: Array = []
var _observers := {}

## Returns true if the current instance running is the only one.
func only_one() -> bool:
	_lock_socket = PacketPeerUDP.new()
	var err := _lock_socket.bind(PORT, ADDRESS)

	if err != OK:
		_send_args_to_host()
		return false

	_start_server()
	return true

func _start_server() -> void:
	_server = TCPServer.new()
	var err := _server.listen(PORT + 1, ADDRESS)

	if err != OK:
		return

	_listening = true
	_server_loop()

func _server_loop() -> void:
	while _listening:
		if _server.is_connection_available():
			var peer := _server.take_connection()
			_handle_client(peer)

		await get_tree().process_frame

func _send_args_to_host() -> void:
	var peer := StreamPeerTCP.new()
	var err := peer.connect_to_host(ADDRESS, PORT + 1)

	if err != OK:
		return

	var buffer := PackedByteArray()

	for arg in OS.get_cmdline_args():
		buffer.append_array(arg.to_utf8_buffer())
		buffer.append(0)

	peer.put_data(buffer)
	peer.disconnect_from_host()

func _handle_client(peer: StreamPeerTCP) -> void:
	var result := peer.get_data(BUFFER_SIZE)
	peer.disconnect_from_host()

	if result[0] != OK:
		return

	var data: PackedByteArray = result[1]
	var args: Array[String] = []

	var start := 0
	for i in data.size():
		if data[i] == 0:
			if i > start:
				var slice := data.slice(start, i)
				args.append(slice.get_string_from_utf8())
			start = i + 1

	if args.is_empty():
		return

	_arguments.append(args)
	_notify_observers(args)

	
func trace(observer: Callable) -> void:
	_observers[observer] = true

func untrace(observer: Callable) -> void:
	_observers.erase(observer)

func _notify_observers(args: Array) -> void:
	for observer in _observers.keys():
		if observer.is_valid():
			observer.call(args)

func release() -> void:
	_listening = false
	_observers.clear()

	if _server:
		_server.stop()

	if _lock_socket:
		_lock_socket.close()

func _ready() -> void:
	var result: bool = only_one()
	
	if result == false and !OS.is_debug_build():
		OS.alert("Only one instance can run!")
		get_tree().quit()
