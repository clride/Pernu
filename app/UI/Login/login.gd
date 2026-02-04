extends VBoxContainer

@onready var username_field: LineEdit = $Username
@onready var password_field: LineEdit = $Password
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var info: Label = $Info

func _on_login_button_pressed() -> void:
	var headers = PackedStringArray([
		"Content-Type: application/json"
	])

	var username: String = username_field.text
	var password: String = password_field.text
	
	if username == "" or password == "": return
	
	Config.username = username
	Config.password = password

	var body = JSON.stringify({
		"username": username,
		"password": password
	})

	var error = http_request.request(
		Config.ENDPOINT_URL + "/login",
		headers,
		HTTPClient.METHOD_POST,
		body
	)

	if error != OK:
		push_error("An error occurred in the HTTP request.")
	
func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var json = JSON.new()
	json.parse(body.get_string_from_utf8())
	var response = json.get_data()
	print(response)
	info.text = response.status
	
	if response_code == 200:
		info.add_theme_color_override("font_color", Color(1.0, 1.0, 1.0, 1.0))
	else:
		info.add_theme_color_override("font_color", Color(1.0, 0.828, 0.799, 1.0))
