# ============================================================
# Rogue Blowjob Layered Sprite
# ============================================================
# Follows Gwen's BJ structure. Crop Top uses 3 layers:
#   Bottom > Braces > Rogue Chest (nude) > Crop Top (cover)
# ChestUp removes only the Crop Top cover.

layeredimage rogue blowjob:

    # LEGS
    group legs:
        attribute legs_base default:
            preg_art("rogue", "Blowjob/Legs.png")

    group legs_clothes:
        attribute legs_clothes_none default:
            Null()
        attribute legs_blue_skirt:
            preg_art("rogue", "Blowjob/Clothes/Legs/Rogue BJ Skirt.png")

    group legs_thighs:
        attribute legs_thighs_none default:
            Null()
        attribute legs_thigh_highs:
            "images/characters/Rogue/Blowjob/Clothes/Thigh Highs.png"

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_purple:
            "images/characters/Rogue/Blowjob/Clothes/Panties/Green Panties/Green Panties BJ.png"
        attribute panties_bikini:
            "images/characters/Rogue/Blowjob/Clothes/Panties/Green Bikini Bottom/Rogue BJ Green Bikini Bottom Up.png"

    # --------------------------------------------------------
    # TORSO (Arms 1 = BJ Torso, Arms 2 = BJ Torso 2)
    # --------------------------------------------------------
    group torso:
        attribute torso_auto default:
            ConditionSwitch(
                "bj_torso_type == 3",
                "images/characters/Rogue/Blowjob/BJ Torso 3.png",
                "bj_torso_type == 2",
                "images/characters/Rogue/Blowjob/BJ Torso 2.png",
                True,
                "images/characters/Rogue/Blowjob/BJ Torso.png"
            )

    # --------------------------------------------------------
    # CROP TOP: Bottom > Braces > Rogue Chest > Cover
    # Full: all 3 pieces shown. Up: Crop Top cover removed.
    # --------------------------------------------------------
    group chest_bottom:
        attribute chest_bottom_none default:
            Null()
        attribute crop_top_bottom:
            "images/characters/Rogue/Blowjob/Clothes/Chest/Crop Top/Crop Top Bottom.png"

    group chest_braces:
        attribute chest_braces_none default:
            Null()
        attribute crop_top_braces:
            "images/characters/Rogue/Blowjob/Clothes/Chest/Crop Top/Crop Top Braces.png"

    # CHEST BODY — always visible
    group chest_body:
        attribute chest_none default:
            preg_art("rogue", "Blowjob/Rogue Chest.png")
        attribute chest_piercing:
            preg_art("rogue", "Blowjob/Rogue Chest Piercing.png")

    group chest_top:
        attribute chest_top_none default:
            Null()
        attribute crop_top_top:
            preg_art("rogue", "Blowjob/Clothes/Chest/Crop Top/Crop Top.png")

    # --------------------------------------------------------
    # BIKINI TOP (above nude body, separate from crop_top groups)
    # --------------------------------------------------------
    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_bikini_top:
            preg_art("rogue", "Blowjob/Clothes/Chest/Green Bikini Top/Rogue BJ Green Bikini Top.png")
        attribute boobs_bikini_top_up:
            preg_art("rogue", "Blowjob/Clothes/Chest/Green Bikini Top/Rogue BJ Green Bikini Top Up.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER / MESH TOP (topmost layer — above chest, crop top)
    # Arms 1: BJ Body (full mesh). Arms 2: BJ Torso (mesh torso only, arm separate).
    # --------------------------------------------------------
    group torso_arms:
        attribute torso_arms_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "bj_torso_type == 3",
                preg_art("rogue", "Blowjob/Clothes/Over/Mesh Top/BJ Torso 3 Mesh Top.png"),
                "bj_torso_type == 2",
                preg_art("rogue", "Blowjob/Clothes/Over/Mesh Top/BJ Torso.png"),
                True,
                preg_art("rogue", "Blowjob/Clothes/Over/Mesh Top/BJ Body.png")
            )

    # COLLAR
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/Blowjob/Clothes/Rogue BJ Collar.png"

    # --------------------------------------------------------
    # CUM BOOBS (above body/clothes)
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_auto default:
            ConditionSwitch(
                "store._bj_girl and 'boobs' in getattr(store._bj_girl, 'Cum', [])",
                "images/characters/Rogue/Blowjob/Cum/Rogue BJ Boobs Cum.png",
                "True", Null()
            )

    group penis_mid:
        attribute penis_mid default:
            Null()

# ============================================================
# Rogue BJ Head (moves with bj_head transforms)
# ============================================================

layeredimage rogue blowjob_head:

    group head:
        attribute head_base default:
            "images/characters/Rogue/Blowjob/Head/BJ Head.png"

    group cheeks:
        attribute cheeks_auto default:
            ConditionSwitch(
                "bj_cheeks", "images/characters/Rogue/Blowjob/Cheeks Sucking.png",
                "True",      Null()
            )

    # BLUSH
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('bj', 'blush', 0) == 2",
                "images/characters/Rogue/Blowjob/Head/Rogue BJ Face Blush 2.png",
                "_gs('bj', 'blush', 0) == 1",
                "images/characters/Rogue/Blowjob/Head/Rogue BJ Face Blush 1.png",
                "True", Null()
            )

    # MOUTH
    group mouth:
        attribute mouth_none:
            Null()
        attribute mouth_tongue:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Tongue.png"
        attribute mouth_sucking default:
            Null()
        attribute mouth_normal:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Smile.png"
        attribute mouth_smile:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Smile.png"
        attribute mouth_happy:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Happy.png"
        attribute mouth_lipbite:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_sad:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Surprised.png"
        attribute mouth_angry:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Angry.png"
        attribute mouth_scared:
            "images/characters/Rogue/Blowjob/Expressions/Mouth/Scared.png"

    # EYES
    group eyes:
        attribute eyes_auto default:
            ConditionSwitch(
                "store.hiding_face or bj_blink", "images/characters/Rogue/Blowjob/Expressions/Eyes/Closed.png",
                "bj_eyes == 'squint_2'",       "images/characters/Rogue/Blowjob/Expressions/Eyes/Squint 2.png",
                "bj_eyes == 'squint'",         "images/characters/Rogue/Blowjob/Expressions/Eyes/Squint.png",
                "bj_eyes == 'left_closed'",    "images/characters/Rogue/Blowjob/Expressions/Eyes/Left Closed.png",
                "bj_eyes == 'right_closed'",   "images/characters/Rogue/Blowjob/Expressions/Eyes/Right Closed.png",
                "True",                        "images/characters/Rogue/Blowjob/Expressions/Eyes/Normal.png"
            )

    # BROWS
    group brows:
        attribute brows_auto default:
            ConditionSwitch(
                "bj_brows == 2", "images/characters/Rogue/Blowjob/Expressions/Brows/Sad.png",
                "bj_brows == 3", "images/characters/Rogue/Blowjob/Expressions/Brows/Perplexed.png",
                "bj_brows == 4", "images/characters/Rogue/Blowjob/Expressions/Brows/Perplexed 2.png",
                "bj_brows == 5", "images/characters/Rogue/Blowjob/Expressions/Brows/Angry.png",
                "True",          "images/characters/Rogue/Blowjob/Expressions/Brows/Normal.png"
            )

# ============================================================
# Rogue BJ Jaw
# ============================================================

layeredimage rogue blowjob_jaw:

    group jaw:
        attribute jaw_auto default:
            "images/characters/Rogue/Blowjob/Jaw 1.png"
        attribute jaw_1:
            "images/characters/Rogue/Blowjob/Jaw 1.png"
        attribute jaw_2:
            "images/characters/Rogue/Blowjob/Jaw 2.png"

    group teeth:
        attribute teeth_none default:
            Null()
        attribute teeth_visible:
            "images/characters/Rogue/Blowjob/BJ Teeth.png"

# ============================================================
# Standalone BJ images (used by Core_Blowjob.rpy)
# ============================================================

image rogue bj_penis = ConditionSwitch(
    "store._bj_girl and 'penis' in getattr(store._bj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("BJ/BJ Penis.png"),
        (0, 0), "images/characters/Rogue/Blowjob/Cum/Rogue BJ Penis Cum.png",
    ),
    "True",
    _p("BJ/BJ Penis.png"),
)

image rogue bj_penis_guy = _p("BJ/BJ Penis Guy.png")

# bj_right_arm: Rogue has no separate right arm asset — bj_arm covers both sides.
image rogue bj_forcing_hands_left  = _p("BJ/BJ Forcing Hands Left.png")
image rogue bj_forcing_hands_right = _p("BJ/BJ Forcing Hands Right.png")

# bj_arm (zorder 9981, ABOVE body, animated with bj_arm_speed transforms)
# Arm Torso 2 always shows; Mesh Top arm stacked on top when Over is on.
image rogue bj_arm = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/Blowjob/Arm Torso 2.png",
        (0, 0), "images/characters/Rogue/Blowjob/Clothes/Over/Mesh Top/BJ Arm.png",
    ),
    True,
    "images/characters/Rogue/Blowjob/Arm Torso 2.png"
)
image rogue bj_hand      = "images/characters/Rogue/Blowjob/BJ Hand.png"
image rogue bj_slap_right = _p("BJ/BJ Guy Hand Smack Right.png")
image rogue bj_slap_left  = _p("BJ/BJ Guy Hand Smack Left.png")

image rogue bj_hide_hand_left = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/Blowjob/Hide Hand left.png",
        (0, 0), "images/characters/Rogue/Blowjob/Clothes/Over/Mesh Top/Hide Hand Left Mesh Top.png",
    ),
    True,
    "images/characters/Rogue/Blowjob/Hide Hand left.png"
)
image rogue bj_hide_hand_right = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/Blowjob/Hide Hand Right.png",
        (0, 0), "images/characters/Rogue/Blowjob/Clothes/Over/Mesh Top/Hide Hand Right Mesh Top.png",
    ),
    True,
    "images/characters/Rogue/Blowjob/Hide Hand Right.png"
)

# Face cum — ABOVE penis (zorder 10025)
image rogue bj_cum_face = Composite(
    (1920, 1080),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Rogue/Blowjob/Cum/Rogue BJ Face Cum.png",
        "True", Null()
    ),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'head' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Rogue/Blowjob/Cum/Rogue BJ Head Cum.png",
        "True", Null()
    ),
)

# Mouth cum — BELOW penis (zorder 9988)
image rogue bj_cum_mouth = ConditionSwitch(
    "store._bj_girl and 'mouth' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Rogue/Blowjob/Cum/Rogue BJ Mouth Cum.png",
    "True", Null()
)

# Face cum under — BELOW penis, ABOVE jaw (zorder 9986)
image rogue bj_cum_face_under = ConditionSwitch(
    "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Rogue/Blowjob/Cum/Rogue BJ Face Cum 2.png",
    "True", Null()
)

# Sucking mouth — separate layer (zorder 10030)
image rogue bj_sucking_mouth = ConditionSwitch(
    "bj_speed <= 1", "images/characters/Rogue/Blowjob/Expressions/Mouth/Sucking 1.png",
    "bj_speed == 2", "images/characters/Rogue/Blowjob/Expressions/Mouth/Sucking 2.png",
    "bj_speed >= 3", "images/characters/Rogue/Blowjob/Expressions/Mouth/Sucking 3.png"
)

# Sucking below — lower lip/chin visible below penis during rise
image rogue bj_sucking_below = "images/characters/Rogue/Blowjob/Expressions/Mouth/Sucking Below.png"
