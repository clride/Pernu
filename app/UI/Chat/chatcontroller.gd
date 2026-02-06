class_name ChatController
extends ScrollContainer

@onready var vbox = $ChatContainer

@export var scroll_threshold = 1000

func snap_to_bottom_if_close():
	var max_scroll = get_v_scroll_bar().max_value
	var current_scroll = get_v_scroll_bar().value
	
	if max_scroll - current_scroll <= scroll_threshold:
		get_v_scroll_bar().value = get_v_scroll_bar().max_value

func append_message(username: String, content: String, from_self:bool, pfp: Texture2D = load("res://icon.svg")):	
	var scene: PackedScene = load("uid://b12bjhi2dlfg6")
	var newmsg: Message = scene.instantiate()
	vbox.add_child(newmsg)
	newmsg.username = username
	newmsg.message_to_display = content
	newmsg.profile_picture = pfp
	newmsg.is_from_self = from_self
	newmsg.update_vis()

# TODO better way ??
func _on_v_box_container_resized() -> void:
	# This is absolutely awful
	# but there doesn't seem to be
	# a reliable way to tell when the max_value
	# of a scroll container updates
	# so we just wait a couple frames
	# before snapping the scroll bar down
	#await get_tree().process_frame
	#await get_tree().process_frame
	#await get_tree().process_frame
	#await get_tree().process_frame
	await get_tree().process_frame
	await get_tree().process_frame
	snap_to_bottom_if_close()
