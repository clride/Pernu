class_name Message
extends HBoxContainer

@export var is_from_self: bool = false
@export var username: String = "Loading..."
@export var message_to_display: String = "Loading..."
@export var profile_picture: Texture2D = Texture2D.new()

func update_vis():
	$UsernameAndMsg/Message.text = message_to_display
	$ProfilePicture.texture = profile_picture
	
	if is_from_self:
		alignment = BoxContainer.ALIGNMENT_END
		move_child($ProfilePicture, 1)
		move_child($UsernameAndMsg, 0)
		$UsernameAndMsg/Username.horizontal_alignment = ALIGNMENT_END
		$UsernameAndMsg/Username.text = "You"
	else:
		alignment = BoxContainer.ALIGNMENT_BEGIN
		move_child($ProfilePicture, 0)
		move_child($UsernameAndMsg, 1)
		$UsernameAndMsg/Username.horizontal_alignment = ALIGNMENT_BEGIN
		$UsernameAndMsg/Username.text = username
		
func _ready() -> void:
	update_vis()

func _enter_tree() -> void:
	update_vis()
