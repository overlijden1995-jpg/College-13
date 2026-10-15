image bg pool_day = im.Scale("images/bg/Pool.png", config.screen_width, config.screen_height)
image bg pool_evening = im.Scale("images/bg/Pool Evening.png", config.screen_width, config.screen_height)
image bg pool_night = im.Scale("images/bg/Pool Night.png", config.screen_width, config.screen_height)
image bg showers   = im.Scale("images/bg/Shower.png",     config.screen_width, config.screen_height)
image bg room_day = im.Scale("images/bg/Playerroom.png", config.screen_width, config.screen_height)
image bg room_night = im.Scale("images/bg/Playerroom Night.png", config.screen_width, config.screen_height)
image bg campus = im.Scale("images/bg/Campus.jpg", config.screen_width, config.screen_height)
image bg campus_evening = im.Scale("images/bg/Campus Evening.png", config.screen_width, config.screen_height)
image bg campus_night = im.Scale("images/bg/Campus Night.png", config.screen_width, config.screen_height)
image bg GwenRoom = im.Scale("images/bg/GwenRoom.png", config.screen_width, config.screen_height)
image bg GwenRoom_night = im.Scale("images/bg/GwenRoom Night.png", config.screen_width, config.screen_height)
image bg RogueRoom = im.Scale("images/bg/RogueRoom.jpg", config.screen_width, config.screen_height)
image bg RogueRoom_night = im.Scale("images/bg/RogueRoom Night.png", config.screen_width, config.screen_height)
image bg TennyRoom = im.Scale("images/bg/TennyRoom.jpg", config.screen_width, config.screen_height)
image bg TennyRoom_night = im.Scale("images/bg/TennyRoom Night.png", config.screen_width, config.screen_height)
image bg ClassRoom = im.Scale("images/bg/Classroom.png", config.screen_width, config.screen_height)
image bg Door = im.Scale("images/bg/Door.jpg", config.screen_width, config.screen_height)
image door_open = im.Scale("images/bg/Door_Open.png", config.screen_width, config.screen_height)
image bg gym = im.Scale("images/bg/gym.jpg", config.screen_width, config.screen_height)
image bg mall = im.Scale("images/bg/Mall.jpg", config.screen_width, config.screen_height)
image bg apartment = im.Scale("images/bg/Apartment.jpg", config.screen_width, config.screen_height)
image bg apartment_night = im.Scale("images/bg/Apartment Night.jpg", config.screen_width, config.screen_height)
image bg apartment_room = im.Scale("images/bg/ApartmentRoom.jpg", config.screen_width, config.screen_height)
image bg apartmentroom_night = im.Scale("images/bg/ApartmentRoom Night.jpg", config.screen_width, config.screen_height)
image bg apartment_shower = im.Scale("images/bg/ApartmentShower.jpg", config.screen_width, config.screen_height)
image bg apartmentshower_night = im.Scale("images/bg/ApartmentShower Night.jpg", config.screen_width, config.screen_height)
image bg downtown = im.Scale("images/bg/Downtown.jpg", config.screen_width, config.screen_height)
image bg downtown_night = im.Scale("images/bg/Downtown Night.jpg", config.screen_width, config.screen_height)
image bg jptown = im.Scale("images/bg/Jptown.png", config.screen_width, config.screen_height)
image bg pharmacy = im.Scale("images/bg/Pharmacy.jpg", config.screen_width, config.screen_height)
image bg bikini_shop = im.Scale("images/bg/Bikini Shop.jpg", config.screen_width, config.screen_height)
image bg dressing_room = im.Scale("images/bg/Dressing Room.png", config.screen_width, config.screen_height)
image bg dressing_room_outside = im.Scale("images/bg/Dressing Room Outside.png", config.screen_width, config.screen_height)
image bg electronics_store = im.Scale("images/bg/GeekStore.png", config.screen_width, config.screen_height)
image bg restaurant = im.Scale("images/bg/Restaurant.png", config.screen_width, config.screen_height)
image bg restaurant_restroom = im.Scale("images/bg/Restaurant Restroom.png", config.screen_width, config.screen_height)
image bg restaurant_under_table = im.Scale("images/bg/Under Table.png", config.screen_width, config.screen_height)
image restaurant_table = im.Scale("images/bg/Restaurant Table.png", config.screen_width, config.screen_height)

image jurassic_dog_van = "images/bg/Jurassic Dog.png"

# ── Jurassic Dog food truck overlay (campus, Mon/Wed/Fri, Morning/Midday) ──

init python:
    _JD_PATH = "images/bg/Jurassic Dog.png"
    _JD_GOLD = im.matrix(
        0, 0, 0, 0, 1.0,
        0, 0, 0, 0, 0.84,
        0, 0, 0, 0, 0.0,
        0, 0, 0, 1, 0
    )
    _JD_OUTLINE_IMG = im.MatrixColor(_JD_PATH, _JD_GOLD)
    _JD_B = 3

    renpy.image("_jd_hover", im.Composite(
        (1920, 1080),
        (-_JD_B, 0), _JD_OUTLINE_IMG,
        (_JD_B, 0), _JD_OUTLINE_IMG,
        (0, -_JD_B), _JD_OUTLINE_IMG,
        (0, _JD_B), _JD_OUTLINE_IMG,
        (-_JD_B, -_JD_B), _JD_OUTLINE_IMG,
        (_JD_B, -_JD_B), _JD_OUTLINE_IMG,
        (-_JD_B, _JD_B), _JD_OUTLINE_IMG,
        (_JD_B, _JD_B), _JD_OUTLINE_IMG,
        (0, 0), _JD_PATH,
    ))

    if "jurassic_dog_overlay" not in config.overlay_screens:
        config.overlay_screens.append("jurassic_dog_overlay")

transform _jd_pulse:
    alpha 0.0
    ease 1.2 alpha 0.35
    ease 1.2 alpha 0.0
    repeat

screen jurassic_dog_overlay():
    zorder 1

    $ _jd_weekday = (Day - 1) % 7
    $ _jd_in_sex = player_in_sex_scene()

    if CurrentLocation == "campus" and _jd_weekday in (1, 3, 5) and TimeIndex in (0, 1) and not _jd_in_sex and not _in_intro and not _in_event and not getattr(store, '_player_is_navigating', False):
        if _met_cjohnson and not store._cj_shady_intro:
            add _JD_OUTLINE_IMG at _jd_pulse
        imagebutton:
            idle Transform(_JD_PATH, alpha=0.0)
            hover Transform(_JD_PATH, alpha=0.0)
            focus_mask _JD_PATH
            hovered Function(renpy.show, "_jd_hover", tag="jurassic_dog_van")
            unhovered Function(renpy.show, "jurassic_dog_van")
            # from_current: back to the interrupted statement when his menu ends (the location menu shows again).
            # Without it Ren'Py resumes at the node after it, and a menu sets that node to its LAST choice's block
            # (ast.Menu.execute): his menu ended inside "Back to Campus" at campus (KeyError: 'campus', 2026-10-07)
            action Call("jurassic_dog_menu", from_current=True)
