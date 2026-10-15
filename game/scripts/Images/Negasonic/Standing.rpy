# ============================================================
# Negasonic (NTW) Standing — Blinking Eyes
# ============================================================

image ntw_standing_blink_normal:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Normal.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_sexy:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Sexy.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_looking_left:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_looking_right:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_looking_down:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Down.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_looking_down_2:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Down 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_squint:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Squint.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_squint_2:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Squint 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_squint_looking_right:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Squint Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_squint_looking_left:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Squint Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_surprised:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Surprised.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_surprised_2:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Surprised 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_scared:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Scared.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_blinking_left:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Blinking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image ntw_standing_blink_blinking_right:
    "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Negasonic/Standing/Expressions/Eyes/Blinking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

# ============================================================
# Room backgrounds
# ============================================================
image bg NTWRoom = "bg/NtwRoom.jpg"
image bg NTWRoom_night = "bg/NtwRoomNight.jpg"

# ============================================================
# Negasonic Standing Layered Sprite
# ============================================================

layeredimage ntw standing:

    # --------------------------------------------------------
    # BASE BODY (torso includes legs)
    # --------------------------------------------------------
    always:
        preg_art("ntw", "Standing/Negasonic Torso.png")

    # Full belly (visual pregnancy stage 2): right above the torso, BELOW panties / legs / arms
    # (its soft lower edge would tint them if it sat on top).
    always:
        preg_art("ntw", "+Standing/belly")

    # --------------------------------------------------------
    # SHOES (NTW has none — placeholder group for compatibility)
    # --------------------------------------------------------
    group shoes:
        attribute shoes_none default:
            Null()

    # --------------------------------------------------------
    # PANTIES
    # --------------------------------------------------------
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_yellow:
            preg_art("ntw", "Standing/Clothes/Panties/Yellow Panties/Yellow Panties.png")
        attribute panties_yellow_side:
            preg_art("ntw", "Standing/Clothes/Panties/Yellow Panties/Yellow Panties Side.png")
        attribute panties_yellow_down:
            "images/characters/Negasonic/Standing/Clothes/Panties/Yellow Panties/Yellow Panties Down.png"
        attribute panties_bikini:
            preg_art("ntw", "Standing/Clothes/Panties/Pink Bikini Panties/Pink Bikini Bottom Up.png")
        attribute panties_bikini_side:
            preg_art("ntw", "Standing/Clothes/Panties/Pink Bikini Panties/Pink Bikini Bottom Side.png")
        attribute panties_bikini_down:
            "images/characters/Negasonic/Standing/Clothes/Panties/Pink Bikini Panties/Pink Bikini Bottom Down.png"

    # --------------------------------------------------------
    # LEGS / SKIRT (NTW has none — placeholder group)
    # --------------------------------------------------------
    group legs:
        attribute legs_none default:
            Null()

    # --------------------------------------------------------
    # RIGHT ARM (below chest — all positions)
    # --------------------------------------------------------
    group right_arm:
        attribute arm_right_none:
            Null()
        attribute arm_right_1 default:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 1.png"
        attribute arm_right_2:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 2.png"
        attribute arm_right_3:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 3.png"
        attribute arm_right_4:
            preg_art("ntw", "Standing/Negasonic Arm Right 4.png")

    # --------------------------------------------------------
    # CHEST BODY (nude base — always visible under clothing)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("ntw", "Standing/Negasonic Standing Boobs Naked.png")
        attribute chest_piercing:
            preg_art("ntw", "Standing/Negasonic Standing Boobs Naked Piercings.png")

    # --------------------------------------------------------
    # CHEST CLOTHING (Yellow Bra)
    # --------------------------------------------------------
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("ntw", "Standing/Clothes/Chest/Yellow Bra/Yellow Bra.png")
        attribute chest_corset_up:
            preg_art("ntw", "Standing/Clothes/Chest/Yellow Bra/Yellow Bra Up.png")
        attribute chest_corset_down:
            Null()
        attribute chest_bikini_top:
            preg_art("ntw", "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Down.png")
        attribute chest_bikini_top_up:
            preg_art("ntw", "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png")

    # --------------------------------------------------------
    # LEFT ARM (above chest — all positions)
    # --------------------------------------------------------
    group left_arm:
        attribute left_arm_none default:
            Null()
        attribute left_arm_1:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 1.png"
        attribute left_arm_2:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 2.png"
        attribute left_arm_3:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 3.png"
        attribute left_arm_4:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 4.png"

    # --------------------------------------------------------
    # RIGHT ARM 1 FRONT (re-rendered above chest for arm_1)
    # --------------------------------------------------------
    group arms_front:
        attribute arms_front_none default:
            Null()
        attribute arms_front_1:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 1.png"

    # --------------------------------------------------------
    # MID (placeholder — no mid items yet)
    # --------------------------------------------------------
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER — body + right arm sleeve (left sleeve split to over_left, above bra)
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            Composite(
                (480, 960),
                (0, 0), preg_art("ntw", "Standing/Clothes/Over/Default Uniform/Negasonic Torso Clothed.png"),
                (0, 0), "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Right 1 Default Uniform.png",
            )
        attribute over_long_shirt_arm2:
            Composite(
                (480, 960),
                (0, 0), preg_art("ntw", "Standing/Clothes/Over/Default Uniform/Negasonic Torso Clothed.png"),
                (0, 0), "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Right 2 Default Uniform.png",
            )
        attribute over_long_shirt_arm3:
            Composite(
                (480, 960),
                (0, 0), preg_art("ntw", "Standing/Clothes/Over/Default Uniform/Negasonic Torso Clothed.png"),
                (0, 0), "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Right 3 Default Uniform.png",
            )
        attribute over_long_shirt_arm4:
            Composite(
                (480, 960),
                (0, 0), preg_art("ntw", "Standing/Clothes/Over/Default Uniform/Negasonic Torso Clothed.png"),
                (0, 0), preg_art("ntw", "Standing/Clothes/Over/Default Uniform/Negasonic Arm Right 4 Default Uniform.png"),
            )
        attribute over_towel:
            preg_art("ntw", "Standing/Clothes/Negasonic Standing Towel Body.png")

    # --------------------------------------------------------
    # CHEST RE-RENDER (above over body + right sleeve)
    # --------------------------------------------------------
    group chest_above_arms:
        attribute chest_above_none default:
            Null()
        attribute chest_above_corset:
            preg_art("ntw", "Standing/Clothes/Chest/Yellow Bra/Yellow Bra.png")
        attribute chest_above_corset_down:
            Null()
        attribute chest_above_corset_up:
            preg_art("ntw", "Standing/Clothes/Chest/Yellow Bra/Yellow Bra Up.png")
        attribute chest_above_bikini:
            preg_art("ntw", "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Down.png")
        attribute chest_above_bikini_up:
            preg_art("ntw", "Standing/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png")

    # --------------------------------------------------------
    # OVER LEFT — left arm sleeve above bra
    # --------------------------------------------------------
    group over_left:
        attribute over_left_none default:
            Null()
        attribute over_left_1:
            "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Left 1 Default Uniform.png"
        attribute over_left_2:
            "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Left 2 Default Uniform.png"
        attribute over_left_3:
            "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Left 3 Default Uniform.png"
        attribute over_left_4:
            "images/characters/Negasonic/Standing/Clothes/Over/Default Uniform/Negasonic Arm Left 4 Default Uniform.png"

    # --------------------------------------------------------
    # TOWEL ARM RE-RENDER (above over/towel)
    # --------------------------------------------------------
    group towel_right_arm:
        attribute towel_arm_right_none default:
            Null()
        attribute towel_arm_right_1:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 1.png"
        attribute towel_arm_right_2:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 2.png"
        attribute towel_arm_right_3:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 3.png"
        attribute towel_arm_right_4:
            preg_art("ntw", "Standing/Negasonic Arm Right 4.png")

    group towel_left_arm:
        attribute towel_arm_left_none default:
            Null()
        attribute towel_arm_left_1:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 1.png"
        attribute towel_arm_left_2:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 2.png"
        attribute towel_arm_left_3:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 3.png"
        attribute towel_arm_left_4:
            "images/characters/Negasonic/Standing/Negasonic Arm Left 4.png"

    group towel_arms_front:
        attribute towel_arms_front_none default:
            Null()
        attribute towel_arms_front_1:
            "images/characters/Negasonic/Standing/Negasonic Arm Right 1.png"

    # --------------------------------------------------------
    # COLLAR (NTW has none — placeholder group)
    # --------------------------------------------------------
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # --------------------------------------------------------
    # CUM LAYERS
    # --------------------------------------------------------
    group cum_body:
        attribute cum_body_none default:
            Null()
        attribute cum_body_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Body.png"

    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Boobs.png"

    group cum_legs:
        attribute cum_legs_none default:
            Null()
        attribute cum_legs_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Legs.png"

    group cum_dripping:
        attribute cum_dripping_none default:
            Null()
        attribute cum_dripping_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Dripping.png"

    group cum_hand:
        attribute cum_hand_none default:
            Null()
        attribute cum_hand_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Hand.png"

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------
    always:
        "images/characters/Negasonic/Standing/Head/Negasonic Head.png"

    # --------------------------------------------------------
    # BLUSH
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Negasonic/Standing/Head/Negasonic Standing Blush 1.png"
        attribute blush_2:
            "images/characters/Negasonic/Standing/Head/Negasonic Standing Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Cum Face.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            Null()
        attribute cum_mouth_on:
            "images/characters/Negasonic/Standing/Cum/Negasonic Standing Mouth Cum.png"

    # --------------------------------------------------------
    # EXPRESSIONS (BROWS / EYES / MOUTH)
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Negasonic/Standing/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Negasonic/Standing/Expressions/Brows/Confused.png"
        attribute brows_surprised:
            "images/characters/Negasonic/Standing/Expressions/Brows/Surprised.png"
        attribute brows_sad:
            "images/characters/Negasonic/Standing/Expressions/Brows/Sad.png"
        attribute brows_maniac:
            "images/characters/Negasonic/Standing/Expressions/Brows/Maniac.png"

    group eyes:
        attribute eyes_normal default:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Sexy.png"
        attribute eyes_side:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_left:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_side_2:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_right:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_down:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Down.png"
        attribute eyes_looking_down_2:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Looking Down 2.png"
        attribute eyes_squint:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint 2.png"
        attribute eyes_squint_big:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_small:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_side_squint:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint Looking Right.png"
        attribute eyes_side_squint_2:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Squint Looking Left.png"
        attribute eyes_surprised:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Surprised.png"
        attribute eyes_surprised_2:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Surprised 2.png"
        attribute eyes_scared:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Scared.png"
        attribute eyes_blinking_left:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blinking_right:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Blinking Right.png"
        attribute eyes_closed:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Negasonic/Standing/Expressions/Eyes/Closed Happy.png"

    group mouth:
        attribute mouth_normal default:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Big Smile.png"
        attribute mouth_laugh:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Tongue.png"
        attribute mouth_lipbite:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Lipbite.png"
        attribute mouth_kissing:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Kissing.png"
        attribute mouth_disgusted:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_serious:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_open_teeth:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_talking:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_sch:
            "images/characters/Negasonic/Standing/Expressions/Mouth/Talk 2.png"
