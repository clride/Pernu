extends LineEdit

@onready var api_client: APIClient = $SendMessage
@onready var send_button: Button = $SendButton

func send_triggered():
	var msg: String = text
	
	if msg == "":
		return
	
	api_client.send_message("/messages", JSON.stringify({"message": msg}), true)
	text = ""	
	%ChatHistory.append_message("You", msg, true)

func _on_send_button_button_up() -> void:
	send_triggered()

func _on_text_submitted(_new_text: String) -> void:
	send_triggered()
