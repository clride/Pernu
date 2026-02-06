class_name ChatClient
extends SocketClient

@export var chat_controller: ChatController

func _on_string_packet(data: String):
	var json = JSON.parse_string(data)
	
	if json == null:
		return
	
	var type = json.type
	
	if type == "message":
		var message = json.text
		var user = json.user
		chat_controller.append_message(user, message, user == Config.username)
	if type == "auth":
		var status = json.status
		if status == "failure":
			get_tree().change_scene_to_file("res://UI/login.tscn")

func send_message(data: String):
	send_json({
		"type": "message",
		#"user": Config.username,
		"text": data
		})
		
func on_connect_send_auth():
	send_json({"type": "auth", "username": Config.username, "password": Config.password})

func _ready():
	initialize()
	connected.connect(on_connect_send_auth)
	
