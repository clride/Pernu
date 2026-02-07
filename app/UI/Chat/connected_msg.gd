extends Label

var connection_success: bool = false

func _ready() -> void:
	text = "Connecting..."
	
	await get_tree().create_timer(10).timeout
	
	if not connection_success:
		add_theme_color_override("font_color", Config.ERROR_COLOR)
		text = "Could not connect. Please check your internet connection."

func _on_chat_client_connected() -> void:
	text = "Connected"
	connection_success = true
