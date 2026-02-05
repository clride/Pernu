extends VBoxContainer

@onready var username_field: LineEdit = $Username
@onready var password_field: LineEdit = $Password
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var info: Label = $Info

func show_info(text: String, is_error: bool):
	var color: Color = Color("ffff")
	
	if is_error:
		color = Color(1.0, 0.828, 0.799, 1.0)
	
	info.add_theme_color_override("font_color", color)
	info.text = text

func _on_login_button_pressed() -> void:
	var username: String = username_field.text
	var password: String = password_field.text
	
	if username == "" or password == "": return
	
	Config.username = username
	Config.password = password

	var body = JSON.stringify({
		"username": username,
		"password": password
	})
	
	var req = APIClient.new()
	add_child(req)
	var result = await req.send_message("/login", body)

	if not result or result[0] == 0:
		print("[LOGIN] An error occurred in the HTTP request.")
		show_info("Network Error.", true)
		return

	var status_code = result[0]
	var response_body = result[1]
	
	var result_text = response_body.status
	
	if status_code == 200:
		show_info(result_text, false)
	else:
		show_info(result_text, true)
	
