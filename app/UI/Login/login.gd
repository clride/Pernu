extends VBoxContainer

@onready var username_field: LineEdit = $Username
@onready var password_field: LineEdit = $Password
@onready var info: Label = $Info
@onready var api_client: APIClient = $LoginMessagePost

func show_info(text: String, is_error: bool):
	var color: Color = Color("ffff")
	
	if is_error:
		color = Color(1.0, 0.828, 0.799, 1.0)
	
	info.add_theme_color_override("font_color", color)
	info.text = text

func attempt_login():
	var username: String = username_field.text
	var password: String = password_field.text
	
	if username == "" or password == "": 
		show_info("Please fill every field.", true)
		return
	
	Config.username = username
	Config.password = password

	var body = JSON.stringify({
		"username": username,
		"password": password
	})
	
	var result = await api_client.send_message("/login", body)

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

func _on_login_button_pressed() -> void:
	attempt_login()

func _on_username_text_submitted(_new_text: String) -> void:
	attempt_login()

func _on_password_text_submitted(_new_text: String) -> void:
	attempt_login()
