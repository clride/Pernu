extends Label

func _ready() -> void:
	text = "Connecting..."

func _on_chat_client_connected() -> void:
	text = "Connected"
