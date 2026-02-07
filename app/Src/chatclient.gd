class_name ChatClient
extends SocketClient

@export var chat_controller: ChatController

func goto_login_page():
	get_tree().change_scene_to_file("uid://ctylr1aydvbrg")

func _on_string_packet(data: String):
	var json = JSON.parse_string(data)
	
	if json == null:
		return
	
	var type = json.type
	
	if type == "message":
		var message = json.text
		var user = json.user
		
		var key = Config.get_key()
		
		if key == null:
			return
		
		chat_controller.append_message(user, message, user == key.username)
	if type == "auth":
		var status = json.status
		if status == "failure":
			print("[ChatClient] Login Information Invalid!")
			call_deferred("goto_login_page")

func _on_binary_packet(_data: PackedByteArray):
	pass

func send_message(data: String):
	send_json({
		"type": "message",
		#"user": Config.username,
		"text": data
		})
		
func on_connect_send_auth():
	send_json(Config.get_key())

func _ready():
	initialize()
	connected.connect(on_connect_send_auth)
	
