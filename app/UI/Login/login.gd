extends VBoxContainer

@onready var username_field: LineEdit = $Username
@onready var password_field: LineEdit = $Password
@onready var info: Label = $Info
@onready var api_client: APIClient = $LoginMessagePost

func show_info(text: String, is_error: bool):
	var color: Color = Config.SUCCESS_COLOR
	
	if is_error:
		color = Config.ERROR_COLOR
	
	info.add_theme_color_override("font_color", color)
	info.text = text

func goto_chat_page():
	get_tree().change_scene_to_file("uid://cpuuiy4wqpu4u")

func login(username: String, password: String) -> bool:
	if username == "" or password == "": 
		show_info("Please fill every field.", true)
		return false

	var body = JSON.stringify(
		{"type": "auth",
		"username": username,
		"password": password
		}
	)
	
	var result = await api_client.send_message("/login", body)

	if not result or result[0] == 0:
		print("[LOGIN] An error occurred in the HTTP request.")
		show_info("Auth Server unreachable.", true)
		return false

	var status_code = result[0]
	var response_body = result[1]
	
	var result_text = response_body.status
	
	if status_code == 200:
		var token: String = response_body.token
		
		show_info(result_text, false)
		
		Config.set_key(token)
		return true
	else:
		show_info(result_text, true)
		return false

func attempt_login():
	var username: String = username_field.text
	var password: String = password_field.text
	
	var result: bool = await login(username, password)
	
	if result:
		call_deferred("goto_chat_page")

func _on_login_button_pressed() -> void:
	attempt_login()

func _on_username_text_submitted(_new_text: String) -> void:
	attempt_login()

func _on_password_text_submitted(_new_text: String) -> void:
	attempt_login()

func _ready() -> void:
	var result = Config.get_key()
	
	var logged_in = false
	
	get_parent().hide()
	
	if result != null:
		logged_in = true
	
	if not logged_in:
		get_parent().show()
	else:
		await get_tree().create_timer(0.4).timeout
		call_deferred("goto_chat_page")
