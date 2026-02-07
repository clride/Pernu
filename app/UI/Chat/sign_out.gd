extends Button

func _on_pressed() -> void:
	Config.clear_key()
	get_tree().change_scene_to_file("uid://ctylr1aydvbrg")
