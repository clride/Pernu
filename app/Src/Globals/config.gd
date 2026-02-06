extends Node

const ENDPOINT_URL: String = "http://127.0.0.1:5000"
const SOCKET_URL: String = "ws://127.0.0.1:5001/ws"

const PACKAGE_NAME: String = "ChatApp"

func get_header(username, password) -> Dictionary:
	return {
		"type": "auth",
		"username": username,
		"password": password
	}

func set_key(username, password):
	Keyring.set_password(PACKAGE_NAME, "auth", "login", JSON.stringify(
		get_header(username, password)
	)
	)
	
func get_key() -> Variant:
	return JSON.parse_string(Keyring.get_password(PACKAGE_NAME, "auth", "login"))

var ERROR_COLOR = Color(1.0, 0.828, 0.799, 1.0)
var SUCCESS_COLOR = Color("ffff")
