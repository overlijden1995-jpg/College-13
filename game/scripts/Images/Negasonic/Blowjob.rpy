# ============================================================
# Negasonic (NTW) Blowjob Layered Sprite
# ============================================================
# Follows Gwen/Rogue BJ structure.
# Clothes: Default Uniform (over), Yellow Bra (chest).
# No cheeks asset. No cum face/head/mouth assets yet.

layeredimage ntw blowjob:

    # LEGS
    group legs:
        attribute legs_base default:
            preg_art("ntw", "Blowjob/Legs.png")

    group legs_clothes:
        attribute legs_clothes_none default:
            Null()
        attribute legs_none:
            Null()

    group legs_over:
        attribute legs_over_none default:
            Null()
        attribute legs_over_clothed:
            preg_art("ntw", "Blowjob/Clothes/Over/Default Uniform/BJ Legs Clothed.png")

    group legs_thighs:
        attribute legs_thighs_none default:
            Null()

    group shoes:
        attribute shoes_none default:
            Null()

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_yellow:
            "images/characters/Negasonic/Blowjob/Clothes/Panties/Yellow Panties/BJ Panties.png"
        attribute panties_bikini:
            "images/characters/Negasonic/Blowjob/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Bottom.png"

    # --------------------------------------------------------
    # TORSO (BJ Torso = default, BJ Torso 2 = arms down)
    # --------------------------------------------------------
    group torso:
        attribute torso_auto default:
            ConditionSwitch(
                "bj_torso_type == 3",
                "images/characters/Negasonic/Blowjob/BJ Torso 3.png",
                "bj_torso_type == 2",
                "images/characters/Negasonic/Blowjob/BJ Torso 2.png",
                True,
                "images/characters/Negasonic/Blowjob/BJ Torso.png"
            )

    # CHEST BODY — hidden when over covers chest
    group chest_body:
        attribute chest_none default:
            preg_art("ntw", "Blowjob/Negasonic Chest.png")
        attribute chest_piercing:
            preg_art("ntw", "Blowjob/Negasonic Chest Piercing.png")
        attribute chest_hidden:
            Null()

    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_clothes_1:
            preg_art("ntw", "Blowjob/Clothes/Chest/Yellow Bra/BJ Boobs Bra.png")
        attribute boobs_clothes_2:
            preg_art("ntw", "Blowjob/Clothes/Chest/Yellow Bra/BJ Boobs Bra.png")
        attribute boobs_clothes_1_up:
            preg_art("ntw", "Blowjob/Clothes/Chest/Yellow Bra/Yellow Bra Up.png")
        attribute boobs_bikini_top:
            preg_art("ntw", "Blowjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png")
        attribute boobs_bikini_top_up:
            preg_art("ntw", "Blowjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # OVER (Default Uniform — torso/arms)
    group torso_arms:
        attribute torso_arms_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "bj_torso_type == 3", Null(),
                "bj_torso_type == 2",
                "images/characters/Negasonic/Blowjob/Clothes/Over/Default Uniform/BJ Torso 2 Clothed.png",
                True,
                "images/characters/Negasonic/Blowjob/Clothes/Over/Default Uniform/BJ Torso Clothed.png"
            )

    # BOOBS OVER (Default Uniform covers chest — above torso_arms)
    group boobs_over:
        attribute boobs_over_none default:
            Null()
        attribute boobs_over_clothed:
            preg_art("ntw", "Blowjob/Clothes/Over/Default Uniform/BJ Boobs Clothed.png")

    # COLLAR (NTW has none)
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # CUM BOOBS (above body/clothes)
    group cum_boobs:
        attribute cum_boobs_auto default:
            ConditionSwitch(
                "store._bj_girl and 'boobs' in getattr(store._bj_girl, 'Cum', [])",
                "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Boobs Cum.png",
                "True", Null()
            )

    group penis_mid:
        attribute penis_mid default:
            Null()

# ============================================================
# NTW BJ Head (moves with bj_head transforms)
# ============================================================

layeredimage ntw blowjob_head:

    group head:
        attribute head_base default:
            "images/characters/Negasonic/Blowjob/Head/BJ Head.png"

    group cheeks:
        attribute cheeks_auto default:
            ConditionSwitch(
                "bj_cheeks", "images/characters/Negasonic/Blowjob/Cheeks Sucking.png",
                "True",      Null()
            )

    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('bj', 'blush', 0) == 2",
                "images/characters/Negasonic/Blowjob/Head/NTW BJ Face Blush 2.png",
                "_gs('bj', 'blush', 0) == 1",
                "images/characters/Negasonic/Blowjob/Head/NTW BJ Face Blush 1.png",
                "True", Null()
            )

    # MOUTH
    group mouth:
        attribute mouth_none:
            Null()
        attribute mouth_tongue:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Tongue.png"
        attribute mouth_sucking default:
            Null()
        attribute mouth_normal:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Smile.png"
        attribute mouth_happy:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Happy.png"
        attribute mouth_lipbite:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_sad:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Surprised.png"
        attribute mouth_angry:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Angry.png"
        attribute mouth_scared:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Scared.png"
        attribute mouth_screaming:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Screamming.png"
        attribute mouth_kiss:
            "images/characters/Negasonic/Blowjob/Expressions/Mouth/Kiss.png"

    # EYES
    group eyes:
        attribute eyes_auto default:
            ConditionSwitch(
                "store.hiding_face or bj_blink", "images/characters/Negasonic/Blowjob/Expressions/Eyes/Closed.png",
                "bj_eyes == 'left_closed'",     "images/characters/Negasonic/Blowjob/Expressions/Eyes/Left Closed.png",
                "bj_eyes == 'right_closed'",    "images/characters/Negasonic/Blowjob/Expressions/Eyes/Right Closed.png",
                "bj_eyes == 'looking_left'",    "images/characters/Negasonic/Blowjob/Expressions/Eyes/Looking Left.png",
                "bj_eyes == 'looking_right'",   "images/characters/Negasonic/Blowjob/Expressions/Eyes/Looking Right.png",
                "bj_eyes == 'looking_down'",    "images/characters/Negasonic/Blowjob/Expressions/Eyes/Looking Down.png",
                "bj_eyes == 'looking_down_surprised'", "images/characters/Negasonic/Blowjob/Expressions/Eyes/Looking Down Surprised.png",
                "bj_eyes == 'surprised'",       "images/characters/Negasonic/Blowjob/Expressions/Eyes/Surprised.png",
                "bj_eyes == 'ahegao'",          "images/characters/Negasonic/Blowjob/Expressions/Eyes/Ahegao.png",
                "bj_eyes == 'ahegao_2'",        "images/characters/Negasonic/Blowjob/Expressions/Eyes/Ahegao 2.png",
                "bj_eyes == 'closed_happy'",    "images/characters/Negasonic/Blowjob/Expressions/Eyes/Closed Happy.png",
                "True",                         "images/characters/Negasonic/Blowjob/Expressions/Eyes/Normal.png"
            )

    # BROWS
    group brows:
        attribute brows_auto default:
            ConditionSwitch(
                "bj_brows == 2", "images/characters/Negasonic/Blowjob/Expressions/Brows/Perplexed.png",
                "bj_brows == 3", "images/characters/Negasonic/Blowjob/Expressions/Brows/Perplexed 2.png",
                "bj_brows == 4", "images/characters/Negasonic/Blowjob/Expressions/Brows/Sad.png",
                "bj_brows == 5", "images/characters/Negasonic/Blowjob/Expressions/Brows/Angry.png",
                "True",          "images/characters/Negasonic/Blowjob/Expressions/Brows/Normal.png"
            )

# ============================================================
# NTW BJ Jaw
# ============================================================

layeredimage ntw blowjob_jaw:

    group jaw:
        attribute jaw_auto default:
            "images/characters/Negasonic/Blowjob/Jaw 1.png"
        attribute jaw_1:
            "images/characters/Negasonic/Blowjob/Jaw 1.png"
        attribute jaw_2:
            "images/characters/Negasonic/Blowjob/Jaw 2.png"

    group teeth:
        attribute teeth_none default:
            Null()

# ============================================================
# Standalone BJ images (used by Core_Blowjob.rpy)
# ============================================================

image ntw bj_penis = ConditionSwitch(
    "store._bj_girl and 'penis' in getattr(store._bj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("BJ/BJ Penis.png"),
        (0, 0), "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Penis Cum.png",
    ),
    "True",
    _p("BJ/BJ Penis.png"),
)

image ntw bj_penis_guy = _p("BJ/BJ Penis Guy.png")

image ntw bj_forcing_hands_left  = _p("BJ/BJ Forcing Hands Left.png")
image ntw bj_forcing_hands_right = _p("BJ/BJ Forcing Hands Right.png")

# bj_arm — shows with/without clothes
image ntw bj_arm = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'yellow_jacket'",
    "images/characters/Negasonic/Blowjob/Clothes/Over/Default Uniform/BJ Arm Clothed.png",
    True,
    "images/characters/Negasonic/Blowjob/Arm Torso 2.png"
)

image ntw bj_hand = "images/characters/Negasonic/Blowjob/BJ Hand.png"

image ntw bj_slap_right = _p("BJ/BJ Guy Hand Smack Right.png")
image ntw bj_slap_left  = _p("BJ/BJ Guy Hand Smack Left.png")

image ntw bj_hide_hand_left  = "images/characters/Negasonic/Blowjob/Hide Hand Left.png"
image ntw bj_hide_hand_right = "images/characters/Negasonic/Blowjob/Hide Hand Right.png"

# Face cum — ABOVE penis (zorder 10025)
image ntw bj_cum_face = Composite(
    (1920, 1080),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Face Cum.png",
        "True", Null()
    ),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'head' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Head Cum.png",
        "True", Null()
    ),
)

# Mouth cum — BELOW penis (zorder 9988)
image ntw bj_cum_mouth = ConditionSwitch(
    "store._bj_girl and 'mouth' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Mouth Cum.png",
    "True", Null()
)

# Face cum under — BELOW penis, ABOVE jaw (zorder 9986)
image ntw bj_cum_face_under = ConditionSwitch(
    "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Negasonic/Blowjob/Cum/Negasonic BJ Face Cum 2.png",
    "True", Null()
)

# Sucking mouth — speed-based layer (zorder 10030)
image ntw bj_sucking_mouth = ConditionSwitch(
    "bj_speed <= 1", "images/characters/Negasonic/Blowjob/Expressions/Mouth/Sucking 1.png",
    "bj_speed == 2", "images/characters/Negasonic/Blowjob/Expressions/Mouth/Sucking 2.png",
    "bj_speed >= 3", "images/characters/Negasonic/Blowjob/Expressions/Mouth/Sucking 3.png"
)

# Sucking below — lower lip visible below penis
image ntw bj_sucking_below = "images/characters/Negasonic/Blowjob/Expressions/Mouth/Sucking Below.png"
