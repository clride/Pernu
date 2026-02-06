class_name ChatClient
extends SocketClient

@export var chat_controller: ChatController

func _on_string_packet(data: String):
	var json = JSON.parse_string(data)
	
	if json == null:
		return
		
	var message = json.text
	var type = json.type
	var user = json.user
	chat_controller.append_message(user, message, user == Config.username)

func send_message(data: String):
	send_json({
		"type": "message",
		"user": Config.username,
		"text": data
		})
