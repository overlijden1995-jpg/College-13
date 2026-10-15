# ============================================================
# Rogue Handjob Layered Sprite
# ============================================================

layeredimage rogue handjob:

    # BASE (never moves)
    always:
        ConditionSwitch(
            "store.hiding_face",
            preg_art("rogue", "Handjob/Torso 2.png"),
            "True",
            preg_art("rogue", "Handjob/Torso Head.png")
        )

    # --------------------------------------------------------
    # CHEST BODY (nude base, always visible)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("rogue", "Handjob/Rogue Chest.png")
        attribute chest_piercing:
            preg_art("rogue", "Handjob/Boobs Piercing.png")

    # --------------------------------------------------------
    # CHEST CLOTHING (Top Crop above boobs, Top Crop Up when ChestUp)
    # --------------------------------------------------------
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("rogue", "Handjob/Clothes/Chest/Top Crop.png")
        attribute chest_corset_down:
            preg_art("rogue", "Handjob/Clothes/Chest/Top Crop Up.png")
        attribute chest_bikini_top:
            preg_art("rogue", "Handjob/Clothes/Chest/Green Bikini/Green Bikini Top Down.png")
        attribute chest_bikini_top_up:
            preg_art("rogue", "Handjob/Clothes/Chest/Green Bikini/Green Bikini Top Up.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER (mesh — above chest and boobs)
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Rogue/Handjob/Clothes/Over/HJ Torso 2 Mesh Top.png",
                "True",
                "images/characters/Rogue/Handjob/Clothes/Over/Mesh Over.png"
            )

    # --------------------------------------------------------
    # COLLAR
    # --------------------------------------------------------
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/Handjob/Clothes/Rogue HJ Collar.png"

    # --------------------------------------------------------
    # CUM BOOBS
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Rogue/Handjob/Cum/Rogue HJ Boobs Cum.png"

    # --------------------------------------------------------
    # BLUSH (no assets yet, defined for system compatibility)
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Rogue/Handjob/Head/Rogue HJ Blush 1.png"
        attribute blush_2:
            "images/characters/Rogue/Handjob/Head/Rogue HJ Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Rogue/Handjob/Cum/Rogue HJ Face Cum.png"

    # --------------------------------------------------------
    # BROWS
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Rogue/Handjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Rogue/Handjob/Expressions/Brows/Perplexed.png"
        attribute brows_surprised:
            "images/characters/Rogue/Handjob/Expressions/Brows/Angry.png"
        attribute brows_sad:
            "images/characters/Rogue/Handjob/Expressions/Brows/Sad.png"

    # --------------------------------------------------------
    # EYES (ConditionSwitch: hj_blink -> Closed)
    # --------------------------------------------------------
    group eyes:
        attribute eyes_normal default:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Normal.png",
            )
        attribute eyes_side:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Looking Left.png",
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_looking_right:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_squint:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Squint.png",
            )
        attribute eyes_squint_big:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Squint Normal.png",
            )
        attribute eyes_surprised:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_closed:
            "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png"
        attribute eyes_left_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Blink Left.png",
            )
        attribute eyes_right_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Blink Right.png",
            )
        attribute eyes_squint_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Rogue/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Rogue/Handjob/Expressions/Eyes/Squint Normal.png",
            )

    # --------------------------------------------------------
    # MOUTH
    # --------------------------------------------------------
    group mouth:
        attribute mouth_normal default:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_laugh:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Laugh.png"
        attribute mouth_surprised:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Tongue.png"
        attribute mouth_open_teeth:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_disgusted:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_serious:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_sad:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Sad.png"
        attribute mouth_sch:
            "images/characters/Rogue/Handjob/Expressions/Mouth/Surprised.png"

# ============================================================
# Standalone HJ images (used by Core_Handjob.rpy)
# ============================================================
image rogue hj_hand = "images/characters/Rogue/Handjob/Rogue Hand.png"
image rogue hj_palm = "images/characters/Rogue/Handjob/Rogue HJ Palm.png"
image rogue hj_thumb = "images/characters/Rogue/Handjob/Rogue HJ Thumb.png"
image rogue hj_squeeze_left  = _p("HJ/Guy Hands Squeeze Left.png")
image rogue hj_squeeze_right = _p("HJ/Guy Hands Squeeze Right.png")
image rogue hj_slap_right = _p("HJ/Guy Hand Smack Right.png")
image rogue hj_slap_left = _p("HJ/Guy Hand Smack Left.png")

image rogue hj_hide_hand = ConditionSwitch(
    "store._hj_girl and store._hj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/Handjob/Hide Hand.png",
        (0, 0), "images/characters/Rogue/Handjob/Clothes/Over/Mesh Top Hide Hand.png",
    ),
    True,
    "images/characters/Rogue/Handjob/Hide Hand.png"
)

image rogue hj_penis = ConditionSwitch(
    "store._hj_girl and 'penis' in getattr(store._hj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("HJ/HJ Penis.png"),
        (0, 15), "images/characters/Rogue/Handjob/Cum/Rogue HJ Penis Cum.png",
    ),
    "True",
    _p("HJ/HJ Penis.png"),
)
