class_name APIClient
extends Node

## A custom class that deals with API specific things
## and streamlines the HTTP request workflow

var http_send = HTTPRequest.new()

var _res
var _code
signal result_ready

var mutex = Mutex.new()

# Async function which handles everything
# related to http(s)
func send_message(path: String, request_content: String, is_post:bool =true, type:String ="json") -> Variant:
	mutex.lock()
	
	var headers = PackedStringArray([
		"Content-Type: application/"+type
	])
	
	var method = HTTPClient.METHOD_GET
	if is_post:
		method = HTTPClient.METHOD_POST
	
	var error: Error = http_send.request(Config.ENDPOINT_URL+path, headers, method, request_content)
	
	if error != Error.OK:
		mutex.unlock()
		return null
	
	await result_ready
	
	mutex.unlock()
	
	return [_code, _res]

func _enter_tree() -> void:
	add_child(http_send)
	http_send.request_completed.connect(_on_http_request_request_completed)
	
func _on_http_request_request_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray):
	var json = JSON.new()
	json.parse(body.get_string_from_utf8())
	var response = json.get_data()
	_code = response_code
	_res = response
	result_ready.emit()
	
