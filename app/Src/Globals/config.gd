extends Node

const ENDPOINT_URL: String = "http://127.0.0.1:5000"
const SOCKET_URL: String = "ws://127.0.0.1:5001/ws"

const PACKAGE_NAME: String = "ChatApp"

var username: String = ""
var id: int = -1

func get_header(token: String) -> Dictionary:
	return {
		"type": "auth",
		"token": token
	}

func set_key(token: String):
	Keyring.set_password(PACKAGE_NAME, "auth", "login", JSON.stringify(
		get_header(token)
	)
	)
	
func get_key() -> Variant:
	var data = JSON.parse_string(Keyring.get_password(PACKAGE_NAME, "auth", "login"))
	
	return data

func clear_key():
	print("[Config] Clearing Key Cache")
	Keyring.set_password(PACKAGE_NAME, "auth", "login", "")

var ERROR_COLOR = Color(1.0, 0.828, 0.799, 1.0)
var SUCCESS_COLOR = Color("ffff")
