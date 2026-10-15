layeredimage tenny handjob:

    # --------------------------------------------------------
    # Layer order (bottom -> top):
    # Legs L/R -> Pelvis -> Arms L/R -> Torso -> Chest body
    # -> Chest clothes -> Boobs clothes -> Collar -> Mid -> Over
    # -> Jaw -> Head -> Blush -> Cum -> Expressions
    # --------------------------------------------------------

    # LEGS
    always:
        "images/characters/Tenny/BJ_HJ/Legs Left.png"
    always:
        "images/characters/Tenny/BJ_HJ/Legs Right.png"

    group legs_clothes:
        attribute legs_none default:
            Null()
        attribute legs_white_pants:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/Legs Left White Pants.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/Legs Right White Pants.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/White Pants Pelvis.png",
            )

    group shoes:
        attribute shoes_none default:
            Null()

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_bikini:
            "images/characters/Tenny/BJ_HJ/Clothes/Panties/Bikini Bottom/Blue Bikini Bottom.png"
        attribute panties_striped:
            "images/characters/Tenny/BJ_HJ/Clothes/Panties/Striped Panties/Tenny Striped Panties.png"

    # PELVIS
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Pelvis.png"

    # BODY ARMS (below torso and chest)
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Left.png"
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Right.png"

    # TORSO (above arms, below chest)
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Torso.png"

    # BELLY (visual pregnancy stage 1 on, one size in this pose): right above the torso, below the chest
    always:
        preg_art("tenny", "+BJ_HJ/belly")

    # --------------------------------------------------------
    # CHEST (nude / piercing / clothed base)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("tenny", "BJ_HJ/Tenny Chest.png")
        attribute chest_piercing:
            preg_art("tenny", "BJ_HJ/Tenny Chest Piercing.png")
        attribute chest_hidden:
            "images/characters/Tenny/BJ_HJ/Tenny Chest Clothed.png"
        attribute chest_clothes:
            "images/characters/Tenny/BJ_HJ/Tenny Chest Clothed.png"

    # --------------------------------------------------------
    # CLOTHING (all below head/jaw so clothes don't hide face)
    # --------------------------------------------------------

    # CHEST CLOTHING
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()

    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_bikini_top:
            preg_art("tenny", "BJ_HJ/Clothes/Chest/Bikini Top/Blue Bikini Top.png")
        attribute boobs_bikini_top_up:
            "images/characters/Tenny/BJ_HJ/Clothes/Chest/Bikini Top/Blue Bikini Top Up.png"
        attribute boobs_white_top:
            preg_art("tenny", "BJ_HJ/Clothes/Chest/Top/White Top.png")
        attribute boobs_white_top_up:
            "images/characters/Tenny/BJ_HJ/Clothes/Chest/Top/White Top Up.png"

    # COLLAR
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # MID CLOTHING (below over)
    group mid_clothing:
        attribute mid_none default:
            Null()
        attribute over_blue_shirt:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt Arm Left.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt Arm Right.png",
                (0, 0), preg_art("tenny", "BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt.png"),
            )

    # OVER CLOTHING (above mid)
    group over:
        attribute over_none default:
            Null()
        attribute over_blue_jacket:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket Arm Left.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket Arm Right.png",
                (0, 0), preg_art("tenny", "BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket.png"),
            )

    # CUM BODY (above clothes, below jaw — ConditionSwitch like BJ)
    group cum_boobs:
        attribute cum_boobs_none default:
            ConditionSwitch(
                "store._hj_girl and 'boobs' in getattr(store._hj_girl, 'Cum', [])",
                "images/characters/Tenny/BJ_HJ/Cum/Cum Tits.png",
                "True", Null()
            )
        attribute cum_boobs_on:
            "images/characters/Tenny/BJ_HJ/Cum/Cum Tits.png"

    # --------------------------------------------------------
    # JAW & HEAD (above clothes so face is never hidden)
    # --------------------------------------------------------

    # JAW (below head, hidden when hiding_face)
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "True", "images/characters/Tenny/BJ_HJ/Jaw.png"
        )

    # HEAD (hidden when hiding_face)
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "True", "images/characters/Tenny/BJ_HJ/Head/Tenny Head.png"
        )

    # --------------------------------------------------------
    # BLUSH
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Tenny/BJ_HJ/Head/BJ Head Blush.png"
        attribute blush_2:
            "images/characters/Tenny/BJ_HJ/Head/BJ Head Blush 2.png"

    # CUM FACE (above head/blush, below expressions — ConditionSwitch like BJ)
    group cum_face:
        attribute cum_face_none default:
            ConditionSwitch(
                "store._hj_girl and 'face' in getattr(store._hj_girl, 'Cum', [])",
                "images/characters/Tenny/BJ_HJ/Cum/Cum Face.png",
                "True", Null()
            )
        attribute cum_face_on:
            "images/characters/Tenny/BJ_HJ/Cum/Cum Face.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            ConditionSwitch(
                "store._hj_girl and 'mouth' in getattr(store._hj_girl, 'Cum', [])",
                "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth.png",
                "True", Null()
            )
        attribute cum_mouth_on:
            "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth.png"

    # BROWS
    group brows:
        attribute brows_normal default:
            "images/characters/Tenny/BJ_HJ/Expression/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Tenny/BJ_HJ/Expression/Brows/Perplexed.png"
        attribute brows_surprised:
            "images/characters/Tenny/BJ_HJ/Expression/Brows/Angry.png"
        attribute brows_sad:
            "images/characters/Tenny/BJ_HJ/Expression/Brows/Sad.png"

    # EYES (ConditionSwitch per attribute: hj_blink -> Closed.png)
    group eyes:
        attribute eyes_normal default:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Normal.png",
            )
        attribute eyes_side:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Left.png",
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Right.png",
            )
        attribute eyes_looking_right:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Right.png",
            )
        attribute eyes_squint:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Squint.png",
            )
        attribute eyes_squint_big:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Squint 2.png",
            )
        attribute eyes_surprised:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Surprised.png",
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Surprised.png",
            )
        attribute eyes_closed:
            "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png"
        attribute eyes_left_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Left Closed.png",
            )
        attribute eyes_right_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Right Closed.png",
            )
        attribute eyes_squint_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "True", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Squint 2.png",
            )
        attribute eyes_closed_happy:
            "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed Happy.png"

    # MOUTH
    group mouth:
        attribute mouth_normal default:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Smile.png"
        attribute mouth_laugh:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Happy.png"
        attribute mouth_surprised:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Tongue.png"
        attribute mouth_open_teeth:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Surprised.png"
        attribute mouth_disgusted:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Angry.png"
        attribute mouth_serious:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Normal.png"
        attribute mouth_sad:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Sad.png"
        attribute mouth_sch:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Surprised.png"
        attribute mouth_lipbite:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Lipbite.png"

# ============================================================
# STANDALONE IMAGES
# ============================================================

image tenny hj_hide_hand = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Tenny/BJ_HJ/Hide Hand Left.png",
    (0, 0), "images/characters/Tenny/BJ_HJ/Hide Hand Right.png",
)

image tenny hj_hand = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Tenny/BJ_HJ/Hand Job Hand Left.png",
    (0, 0), "images/characters/Tenny/BJ_HJ/Hand Job Hand Right.png",
)

image tenny hj_penis = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/BJ Penis Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Penis.png",
)

image tenny hj_slap_right = _p("HJ/Guy Hand Smack Right.png")
image tenny hj_slap_left  = _p("HJ/Guy Hand Smack Left.png")
image tenny hj_squeeze_left  = _p("HJ/Guy Hands Squeeze Left.png")
image tenny hj_squeeze_right = _p("HJ/Guy Hands Squeeze Right.png")

# Guy body (POV overlay — skin-aware)
image tenny hj_guy = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/Guy Body Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Guy Body.png",
)

# Arm overlay (Blow Job Arms — composite fallback)
image tenny hj_arm_overlay = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Tenny/BJ_HJ/Blow Job Arm Left.png",
    (0, 0), "images/characters/Tenny/BJ_HJ/Blow Job Arm Right.png",
)

# Split arms for independent rotation
image tenny hj_arm_left  = "images/characters/Tenny/BJ_HJ/Blow Job Arm Left.png"
image tenny hj_arm_right = "images/characters/Tenny/BJ_HJ/Blow Job Arm Right.png"

# Her face and mouth cum live INSIDE the layeredimage (groups cum_face / cum_mouth above: they move with
# her body). The standalone copies the core also shows (slot transform, their own bounce phase, above his
# body in POV) painted a SECOND facial floating in the air (tester 2026-10-11, "cum all over her"; Shion had
# the same fix 2026-10-10). Null keeps the core's show/hide calls harmless, the layeredimage does the work.
image tenny hj_cum_face = Null()
image tenny hj_cum_mouth = Null()
image tenny hj_cum_face_UNUSED = ConditionSwitch(
    "store._hj_girl and 'face' in getattr(store._hj_girl, 'Cum', [])",
    "images/characters/Tenny/BJ_HJ/Cum/Cum Face.png",
    "True", Null()
)
image tenny hj_cum_mouth_UNUSED = ConditionSwitch(
    "store._hj_girl and 'mouth' in getattr(store._hj_girl, 'Cum', [])",
    "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth.png",
    "True", Null()
)
