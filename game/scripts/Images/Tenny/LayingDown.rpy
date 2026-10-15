# LayingDown.rpy — Tenny laying down pose (EXCLUSIVE)
# Layeredimage (head + expressions) + standalone images for all other layers

init python:

    _LD_FALLBACK = {
        "brows_up": "brows_surprised",
        "brows_challenging": "brows_horny",
        "eyes_squint_big": "eyes_squint",
        "eyes_side_squint": "eyes_squint",
        "eyes_blink_left": "eyes_left_closed",
        "eyes_blink_right": "eyes_right_closed",
        "mouth_disgusted": "mouth_sad",
        "mouth_open_teeth": "mouth_moaning",
        "mouth_sch": "mouth_normal",
        "mouth_serious": "mouth_normal",
    }

    def _laying_safe(attr):
        return _LD_FALLBACK.get(attr, attr)

    def _ld_face(path):
        return ConditionSwitch("store.hiding_face", Null(), "True", path)

layeredimage tenny laying:

    group head:
        attribute head_base default:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Tenny/Laying Down/Head/Head looking back.png",
                "True",
                "images/characters/Tenny/Laying Down/Head/Head.png",
            )
        attribute head_looking_back:
            "images/characters/Tenny/Laying Down/Head/Head looking back.png"

    group brows:
        attribute brows_normal default:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Normal.png")
        attribute brows_angry:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Angry.png")
        attribute brows_confused:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Confused.png")
        attribute brows_confused_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Confused 2.png")
        attribute brows_horny:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Horny.png")
        attribute brows_maniac:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Maniac.png")
        attribute brows_sad:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Sad.png")
        attribute brows_scared:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Scared.png")
        attribute brows_surprised:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Brows/Surprised.png")

    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            _ld_face("images/characters/Tenny/Laying Down/Head/blush 1.png")
        attribute blush_2:
            _ld_face("images/characters/Tenny/Laying Down/Head/blush 2.png")

    group eyes:
        attribute eyes_normal default:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Normal.png")
        attribute eyes_ahegao:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Ahegao.png")
        attribute eyes_ahegao_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Ahegao 2.png")
        attribute eyes_bliss:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Bliss.png")
        attribute eyes_closed:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Closed.png")
        attribute eyes_closed_happy:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Closed Happy.png")
        attribute eyes_left_closed:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Closed Left.png")
        attribute eyes_right_closed:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Closed Right.png")
        attribute eyes_looking_left:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Looking Left.png")
        attribute eyes_looking_right:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Looking Right.png")
        attribute eyes_looking_to_player:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Looking To Player.png")
        attribute eyes_looking_up:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Looking Up.png")
        attribute eyes_sexy:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Sexy.png")
        attribute eyes_side:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Side.png")
        attribute eyes_side_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Side 2.png")
        attribute eyes_squint:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Squint.png")
        attribute eyes_squint_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Squint 2.png")
        attribute eyes_surprised:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Surprised.png")
        attribute eyes_surprised_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Surprised 2.png")
        attribute eyes_up:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Up.png")
        attribute eyes_up_closed_left:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Up Closed Left.png")
        attribute eyes_up_closed_right:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Eyes/Up Closed Right.png")

    group mouth:
        attribute mouth_normal default:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Normal.png")
        attribute mouth_ahegao:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Ahegao.png")
        attribute mouth_angry:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Angry.png")
        attribute mouth_happy:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Happy.png")
        attribute mouth_kiss:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Kiss.png")
        attribute mouth_laugh:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Laugh.png")
        attribute mouth_lipbite:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Lipbite.png")
        attribute mouth_moaning:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Moaning.png")
        attribute mouth_moaning_2:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Moaning 2.png")
        attribute mouth_moaning_3:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Moaning 3.png")
        attribute mouth_sad:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Sad.png")
        attribute mouth_scared:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Scared.png")
        attribute mouth_screaming:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Screaming.png")
        attribute mouth_smile:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Smile.png")
        attribute mouth_surprised:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Surprised.png")
        attribute mouth_tongue:
            _ld_face("images/characters/Tenny/Laying Down/Expressions/Mouth/Tongue.png")


# ═══════════════════════════════════════════════════════════
# STANDALONE — Body
# ═══════════════════════════════════════════════════════════

image tenny laying_torso_1 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Torso 1.png"
image tenny laying_torso_2 = "images/characters/Tenny/Laying Down/Torso/Torso 2/Torso 2.png"

# Torso 1 arms (6 variants: left/right x 3 poses)
image tenny laying_green_pillow = "images/characters/Tenny/Laying Down/Clothes/Green Pillow.png"

image tenny laying_arm_left_1 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Left 1.png"
image tenny laying_arm_left_2 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Left 2.png"
image tenny laying_arm_left_3 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Left 3.png"
image tenny laying_arm_right_1 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Right 1.png"
image tenny laying_arm_right_2 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Right 2.png"
image tenny laying_arm_right_3 = "images/characters/Tenny/Laying Down/Torso/Torso 1/Arm Right 3.png"

# Torso 2 arms (3 variants: left 1/2 + masturbation)
image tenny laying_t2_arm_left_1 = "images/characters/Tenny/Laying Down/Torso/Torso 2/Arm Left 1.png"
image tenny laying_t2_arm_left_2 = "images/characters/Tenny/Laying Down/Torso/Torso 2/Arm Left 2.png"
image tenny laying_t2_arm_mast = "images/characters/Tenny/Laying Down/Torso/Torso 2/Arm Masturbation.png"

# Legs (closed)
image tenny laying_legs_left = "images/characters/Tenny/Laying Down/Legs Left.png"
image tenny laying_legs_right = "images/characters/Tenny/Laying Down/Legs Right.png"

# Legs (open — future)
image tenny laying_legs_open_left = "images/characters/Tenny/Laying Down/Legs Open Left.png"
image tenny laying_legs_open_left_2 = "images/characters/Tenny/Laying Down/Legs Open Left 2.png"
image tenny laying_legs_open_right = "images/characters/Tenny/Laying Down/Legs Open Right.png"
image tenny laying_legs_open_right_2 = "images/characters/Tenny/Laying Down/Legs Open Right 2.png"

# Masturbation animated (composited GIF frames: pre-insert, insert, oral after)
image tenny laying_mast_pre_insert = DynamicDisplayable(_ld_mast_frame_anim, "Pussy Mast Pre-Insert", 0.042)
image tenny laying_mast_insert = DynamicDisplayable(_ld_mast_frame_anim, "Pussy Mast Insert")
image tenny laying_mast_after_anim = DynamicDisplayable(_ld_mast_frame_anim, "After Pussy Animated", 0.083)


# ═══════════════════════════════════════════════════════════
# STANDALONE — Ass / Pelvis
# ═══════════════════════════════════════════════════════════

image tenny laying_wave_test = "images/characters/Tenny/Laying Down/Wave Test.png"
image tenny laying_wave_left = "images/characters/Tenny/Laying Down/Wave Test Left.png"
image tenny laying_wave_right = "images/characters/Tenny/Laying Down/Wave Test Right.png"
image tenny laying_slap_wave_left = "images/characters/Tenny/Laying Down/Slap Wave Left.png"
image tenny laying_slap_wave_right = "images/characters/Tenny/Laying Down/Slap Wave Right.png"

image tenny laying_pelvis = "images/characters/Tenny/Laying Down/Ass/Pelvis Base.png"
image tenny laying_before_pussy = "images/characters/Tenny/Laying Down/Ass/Before Pussy.png"
image tenny laying_before_ass = "images/characters/Tenny/Laying Down/Ass/Before Ass.png"
image tenny laying_before_ass_2 = "images/characters/Tenny/Laying Down/Ass/Before Ass 2.png"
image tenny laying_after_ass = "images/characters/Tenny/Laying Down/Ass/After Ass.png"

image tenny laying_ass_base_left = "images/characters/Tenny/Laying Down/Ass/Base Ass/Base Ass Left.png"
image tenny laying_ass_base_right = "images/characters/Tenny/Laying Down/Ass/Base Ass/Base Ass Right.png"
image tenny laying_ass_vaginal_left = "images/characters/Tenny/Laying Down/Ass/Vaginal Ass/Ass Vaginal Left.png"
image tenny laying_ass_vaginal_right = "images/characters/Tenny/Laying Down/Ass/Vaginal Ass/Ass Vaginal Right.png"
image tenny laying_ass_anal_left = "images/characters/Tenny/Laying Down/Ass/Anal Ass/Anal Ass Left.png"
image tenny laying_ass_anal_right = "images/characters/Tenny/Laying Down/Ass/Anal Ass/Anal Ass Right.png"

image tenny laying_during_pussy_safe = "images/characters/Tenny/Laying Down/During Pussy Safe.png"
image tenny laying_during_pussy = "images/characters/Tenny/Laying Down/Ass/During Pussy.png"
image tenny laying_during_pussy_below = "images/characters/Tenny/Laying Down/Ass/During Pussy Below.png"
image tenny laying_after_pussy = "images/characters/Tenny/Laying Down/Ass/After Pussy.png"
image tenny laying_during_anal = "images/characters/Tenny/Laying Down/Ass/During Anal Fast.png"
image tenny laying_during_anal_below = "images/characters/Tenny/Laying Down/Ass/During Anal Below.png"
image tenny laying_during_anal_fast = "images/characters/Tenny/Laying Down/Ass/During Anal Fast 2.png"
image tenny laying_during_anal_safe = "images/characters/Tenny/Laying Down/Ass/During Anal Safe.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Guy / Player
# ═══════════════════════════════════════════════════════════

image tenny laying_guy_legs_base = _p("Laying Down/Guy Legs Base.png")
image tenny laying_guy_legs_1 = _p("Laying Down/Guy Legs 1.png")
image tenny laying_guy_legs_2 = _p("Laying Down/Guy Legs 2.png")
image tenny laying_guy_calf_1 = _p("Laying Down/Guy Legs calf 1.png")
image tenny laying_guy_calf_2 = _p("Laying Down/Guy Legs calf 2.png")

image tenny laying_guy_pelvis = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Guy pelvis 1.png",
    "True", "images/characters/Player/White/Laying Down/Guy pelvis 1.png"
)

image tenny laying_guy_pelvis_safe = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Guy Pelvis Safe.png",
    "True", "images/characters/Player/White/Laying Down/Guy Pelvis Safe.png"
)

image tenny laying_penis = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Guy Penis 1.png",
    "True", "images/characters/Player/White/Laying Down/Guy Penis 1.png"
)

image tenny laying_grab_left = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Grab Ass Left LD.png",
    "True", "images/characters/Player/White/Laying Down/Grab Ass Left LD.png"
)

image tenny laying_grab_right = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Grab Ass Right LD.png",
    "True", "images/characters/Player/White/Laying Down/Grab Ass Right LD.png"
)

image tenny laying_slap_left = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Smack LD Left.png",
    "True", "images/characters/Player/White/Laying Down/Smack LD Left.png"
)

image tenny laying_slap_right = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/Laying Down/Smack LD Right.png",
    "True", "images/characters/Player/White/Laying Down/Smack LD Right.png"
)

image tenny laying_butt_blush = ConditionSwitch(
    "_gs('laying', 'butt_blush', 0) >= 2",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Tenny/Laying Down/Effects/Butt Blush Left 2.png",
        (0, 0), "images/characters/Tenny/Laying Down/Effects/Butt Blush Right 2.png",
    ),
    "_gs('laying', 'butt_blush', 0) >= 1",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Tenny/Laying Down/Effects/Butt Blush Left 1.png",
        (0, 0), "images/characters/Tenny/Laying Down/Effects/Butt Blush Right 1.png",
    ),
    "True", Null()
)

# Virginity blood animation (57 frames, 0.04s each → Static Blood)
image tenny laying_blood_anim:
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 1.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 2.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 3.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 4.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 5.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 6.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 7.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 8.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 9.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 10.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 11.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 12.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 13.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 14.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 15.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 16.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 17.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 18.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 19.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 20.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 21.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 22.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 23.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 24.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 25.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 26.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 27.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 28.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 29.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 30.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 31.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 32.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 33.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 34.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 35.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 36.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 37.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 38.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 39.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 40.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 41.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 42.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 43.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 44.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 45.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 46.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 47.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 48.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 49.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 50.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 51.png"
    0.05
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 52.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 53.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 54.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 55.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 56.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Blood 57.png"
    0.04
    "images/characters/Tenny/Laying Down/Effects/Animation/Static Blood.png"

image tenny laying_blood_static = "images/characters/Tenny/Laying Down/Effects/Animation/Static Blood.png"

image tenny laying_blood_penis = "images/characters/Tenny/Laying Down/Effects/Blood Penis.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Clothing: Panties
# ═══════════════════════════════════════════════════════════

# Blue Bikini Bottom
image tenny laying_panties_blue_bikini_bottom_full = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom.png"
image tenny laying_panties_blue_bikini_bottom_down = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Down.png"
image tenny laying_panties_blue_bikini_bottom_down_1 = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Down 1.png"
image tenny laying_panties_blue_bikini_bottom_down_2 = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Down 2.png"
image tenny laying_panties_blue_bikini_bottom_side = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Side.png"
image tenny laying_panties_blue_bikini_bottom_side_1 = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Side 1.png"
image tenny laying_panties_blue_bikini_bottom_side_2 = "images/characters/Tenny/Laying Down/Clothes/Panties/Blue Bikini Bottom/Blue Bikini Bottom Side 2.png"

# Striped Panties
image tenny laying_panties_striped_panties_full = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties.png"
image tenny laying_panties_striped_panties_down = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Down.png"
image tenny laying_panties_striped_panties_down_1 = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Down 1.png"
image tenny laying_panties_striped_panties_down_2 = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Down 2.png"
image tenny laying_panties_striped_panties_side = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Side.png"
image tenny laying_panties_striped_panties_side_1 = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Side 1.png"
image tenny laying_panties_striped_panties_side_2 = "images/characters/Tenny/Laying Down/Clothes/Panties/Striped panties/Striped Panties Side 2.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Clothing: Chest (bikini top, white top)
# Image name format: tenny laying_chest_{item}_{t1/t2}
# ═══════════════════════════════════════════════════════════

# white_bra (White Top)
image tenny laying_chest_white_bra_t1 = "images/characters/Tenny/Laying Down/Clothes/Chest/Torso 1/White Top/White Top.png"
image tenny laying_chest_white_bra_t2 = "images/characters/Tenny/Laying Down/Clothes/Chest/Torso 2/White Top/White Top.png"

# blue_bikini_top (Blue Bikini)
image tenny laying_chest_blue_bikini_top_t1 = "images/characters/Tenny/Laying Down/Clothes/Chest/Torso 1/Blue Bikini/Blue Bikini Top.png"
image tenny laying_chest_blue_bikini_top_t2 = "images/characters/Tenny/Laying Down/Clothes/Chest/Torso 2/Blue Bikini/Blue Bikini Top.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Clothing: Mid (blue shirt body + sleeves)
# Body: tenny laying_mid_{item}_{t1/t2}
# T1 sleeves: tenny laying_mid_{item}_t1_sl_{l/r}{12/3}
# T2 arms: tenny laying_mid_{item}_t2_arm{1/2}
# ═══════════════════════════════════════════════════════════

# blue_shirt — T1
image tenny laying_mid_blue_shirt_t1 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 1/Blue Shirt/Blue Shirt.png"
image tenny laying_mid_blue_shirt_t1_sl_l12 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 1/Blue Shirt/Blue Shirt Sleeve Left 1 2.png"
image tenny laying_mid_blue_shirt_t1_sl_r12 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 1/Blue Shirt/Blue Shirt Sleeve Right 1 2.png"
image tenny laying_mid_blue_shirt_t1_sl_l3 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 1/Blue Shirt/Blue Shirt Sleeve Left 3.png"
image tenny laying_mid_blue_shirt_t1_sl_r3 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 1/Blue Shirt/Blue Shirt Sleeve Right 3.png"

# blue_shirt — T2
image tenny laying_mid_blue_shirt_t2 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 2/Blue Shirt/Blue Shirt.png"
image tenny laying_mid_blue_shirt_t2_arm1 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 2/Blue Shirt/Blue Shirt Arm 1.png"
image tenny laying_mid_blue_shirt_t2_arm2 = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 2/Blue Shirt/Blue Shirt Arm 2.png"
image tenny laying_mid_blue_shirt_t2_arm_mast = "images/characters/Tenny/Laying Down/Clothes/Mid/Torso 2/Blue Shirt/Blue Shirt Arm Right Masturbate.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Clothing: Over (blue jacket body + sleeves)
# Body: tenny laying_over_{item}_{t1/t2}
# T1 sleeves: tenny laying_over_{item}_t1_sl_{l/r}{12/3}
# T2 arms: tenny laying_over_{item}_t2_arm{1/2}
# ═══════════════════════════════════════════════════════════

# blue_jacket — T1
image tenny laying_over_blue_jacket_t1 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 1/Blue Jacket/Blue Jacket.png"
image tenny laying_over_blue_jacket_t1_sl_l12 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 1/Blue Jacket/Blue Jacket Sleeve Left 1 2.png"
image tenny laying_over_blue_jacket_t1_sl_r12 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 1/Blue Jacket/Blue Jacket Sleeve Right 1 2.png"
image tenny laying_over_blue_jacket_t1_sl_l3 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 1/Blue Jacket/Blue Jacket Sleeve Left 3.png"
image tenny laying_over_blue_jacket_t1_sl_r3 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 1/Blue Jacket/Blue Jacket Sleeve Right 3.png"

# blue_jacket — T2
image tenny laying_over_blue_jacket_t2 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 2/Blue Jacket/Blue Jacket.png"
image tenny laying_over_blue_jacket_t2_arm1 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 2/Blue Jacket/Blue Jacket Arm 1.png"
image tenny laying_over_blue_jacket_t2_arm2 = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 2/Blue Jacket/Blue Jacket Arm 2.png"
image tenny laying_over_blue_jacket_t2_arm_mast = "images/characters/Tenny/Laying Down/Clothes/Over/Torso 2/Blue Jacket/Blue Jacket Arm Right Mastubate.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Clothing: Legs (White Pants)
# ═══════════════════════════════════════════════════════════

image tenny laying_pants_ass_left = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Ass Left.png"
image tenny laying_pants_ass_right = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Ass Right.png"
image tenny laying_pants_down_left = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Down Left.png"
image tenny laying_pants_down_right = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Down Right.png"
image tenny laying_pants_left = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Left.png"
image tenny laying_pants_right = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Right.png"
image tenny laying_pants_open_left = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Open Left.png"
image tenny laying_pants_open_left_2 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Open Left 2.png"
image tenny laying_pants_open_right = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Open Right.png"
image tenny laying_pants_open_right_2 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Open Right 2.png"
image tenny laying_pants_pelvis = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Pelvis Base.png"
image tenny laying_pants_torso_1 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Torso 1.png"
image tenny laying_pants_torso_2 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Torso 2.png"
image tenny laying_pants_squirt_1 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Squirting 1.png"
image tenny laying_pants_squirt_2 = "images/characters/Tenny/Laying Down/Clothes/Legs/White Pants/White Pants Squirting 2.png"


# ═══════════════════════════════════════════════════════════
# STANDALONE — Cum (ConditionSwitch)
# ═══════════════════════════════════════════════════════════

image tenny laying_cum_vaginal = ConditionSwitch(
    "store._laying_girl and 'dripping' in getattr(store._laying_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2", "images/characters/Tenny/Laying Down/Cum/Vaginal Cum 2.png",
    "store._laying_girl and 'dripping' in getattr(store._laying_girl, 'Cum', [])", "images/characters/Tenny/Laying Down/Cum/Vaginal Cum.png",
    "True", Null(),
)
image tenny laying_cum_anal = ConditionSwitch(
    "store._laying_girl and 'anal' in getattr(store._laying_girl, 'Cum', [])", "images/characters/Tenny/Laying Down/Cum/Anal Cum.png",
    "True", Null(),
)
image tenny laying_cum_ass = ConditionSwitch(
    "store._laying_girl and 'ass' in getattr(store._laying_girl, 'Cum', [])", "images/characters/Tenny/Laying Down/Cum/Ass Cum.png",
    "True", Null(),
)
image tenny laying_cum_body = ConditionSwitch(
    "store._laying_girl and ('body' in getattr(store._laying_girl, 'Cum', []) or 'back' in getattr(store._laying_girl, 'Cum', []))", "images/characters/Tenny/Laying Down/Cum/Body Cum.png",
    "True", Null(),
)
image tenny laying_cum_face = ConditionSwitch(
    "store._laying_girl and 'face' in getattr(store._laying_girl, 'Cum', []) and not store.hiding_face", "images/characters/Tenny/Laying Down/Cum/Face Cum.png",
    "True", Null(),
)
image tenny laying_cum_mouth = ConditionSwitch(
    "store._laying_girl and 'mouth' in getattr(store._laying_girl, 'Cum', [])", "images/characters/Tenny/Laying Down/Cum/Mouth Cum.png",
    "True", Null(),
)

image tenny laying_cum_girl_anim = DynamicDisplayable(_ld_cum_frame_anim, "Cum Girl", 55)
image tenny laying_cum_girl = "images/characters/Tenny/Laying Down/Cum/Cum Girl.png"

image tenny laying_cum_dick_1_anim = Transform(DynamicDisplayable(_ld_cum_frame_anim, "Cum Dick  Creampie 1", 31), alpha=0.7)
image tenny laying_cum_dick_1 = Transform("images/characters/Tenny/Laying Down/Cum/Cum Dick  Creampie 1/Cum Dick Creampie 1 Static.png", alpha=0.7)

image tenny laying_cum_dick_2_anim = Transform(DynamicDisplayable(_ld_cum_frame_anim, "Cum Dick Creampie 2", 55), alpha=0.7)
image tenny laying_cum_dick_2 = Transform("images/characters/Tenny/Laying Down/Cum/After Creampie Static.png", alpha=0.7)

image tenny laying_cum_creampie_2 = Transform("images/characters/Tenny/Laying Down/Cum/Cum Creampie 2.png", alpha=0.8)
image tenny laying_cum_creampie_3 = Transform("images/characters/Tenny/Laying Down/Cum/Cum Creampie 3.png", alpha=0.8)

image tenny laying_after_creampie_anim = DynamicDisplayable(_ld_cum_frame_anim, "After Creampie", 57)
image tenny laying_after_creampie = "images/characters/Tenny/Laying Down/Cum/After Creampie Static.png"
