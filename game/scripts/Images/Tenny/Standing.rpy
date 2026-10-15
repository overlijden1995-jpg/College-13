# ============================================================
# Tenny Standing — Blinking Eyes
# ============================================================

image tenny_standing_blink_normal:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Normal.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_sexy:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Sexy.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_looking_left:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_looking_right:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_looking_down:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Looking Down.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_looking_down_2:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Looking Down 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_squint:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Squint.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_squint_2:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Squint 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_squint_looking_right:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Squint Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_squint_looking_left:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Squint Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_surprised:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Surprised.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_surprised_2:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Surprised 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_scared:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Scared.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_blinking_left:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Blinking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image tenny_standing_blink_blinking_right:
    "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Tenny/Standing/Expressions/Eyes/Blinking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

# ============================================================
# Tenny Standing Layered Sprite
# ============================================================

layeredimage tenny standing:

    # --------------------------------------------------------
    # BASE BODY
    # --------------------------------------------------------
    always:
        preg_art("tenny", "Standing/Tenny_Torso.png")

    # Full belly (visual pregnancy stage 2): right above the torso, BELOW panties / legs / arms
    # (its soft lower edge would tint them if it sat on top).
    always:
        preg_art("tenny", "+Standing/belly")

    group shoes:
        attribute shoes_none default:
            Null()
        attribute shoes_thigh_highs:
            "images/characters/Tenny/Standing/Clothes/Tenny Shoes.png"

    # --------------------------------------------------------
    # PANTIES
    # --------------------------------------------------------
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_striped:
            preg_art("tenny", "Standing/Clothes/Panties/Striped Panties/Striped Panties.png")
        attribute panties_striped_side:
            preg_art("tenny", "Standing/Clothes/Panties/Striped Panties/Striped Panties Side.png")
        attribute panties_striped_down:
            "images/characters/Tenny/Standing/Clothes/Panties/Striped Panties/Striped Panties Down.png"
        attribute panties_blue_bikini:
            preg_art("tenny", "Standing/Clothes/Panties/Blue Bikini/Blue Bikini.png")
        attribute panties_blue_bikini_side:
            preg_art("tenny", "Standing/Clothes/Panties/Blue Bikini/Blue Bikini Side.png")
        attribute panties_blue_bikini_down:
            "images/characters/Tenny/Standing/Clothes/Panties/Blue Bikini/Blue Bikini Down.png"

    # --------------------------------------------------------
    # LEGS
    # --------------------------------------------------------
    group legs:
        attribute legs_none default:
            Null()
        attribute legs_white_legs:
            preg_art("tenny", "Standing/Clothes/Legs/White Legs/Tenny White Legs.png")
        attribute legs_white_legs_wet:
            preg_art("tenny", "Standing/Clothes/Legs/White Legs/Tenny White Legs Wet.png")
        attribute legs_white_legs_down:
            "images/characters/Tenny/Standing/Clothes/Legs/White Legs/Tenny White Legs Down.png"

    # --------------------------------------------------------
    # RIGHT ARM (below chest so bikini/bra renders on top)
    # --------------------------------------------------------
    group right_arm:
        attribute arm_right_none:
            Null()
        attribute arm_right_1 default:
            "images/characters/Tenny/Standing/Tenny Arm Right 1.png"
        attribute arm_right_2:
            "images/characters/Tenny/Standing/Tenny Arm Right 2.png"
        attribute arm_right_3:
            "images/characters/Tenny/Standing/Tenny Arm Right 3.png"
        attribute arm_right_4:
            preg_art("tenny", "Standing/Tenny Arm Right 4.png")

    # --------------------------------------------------------
    # CHEST (BODY / PIERCING / CLOTHES LAYER)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("tenny", "Standing/Tenny_Chest.png")
        attribute chest_piercing:
            preg_art("tenny", "Standing/Tenny_Chest_Piercing.png")
        attribute chest_clothes:
            "images/characters/Tenny/Standing/Tenny_Chest_Clothes.png"

    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_white_bra:
            preg_art("tenny", "Standing/Clothes/Chest/White Bra/White Bra.png")
        attribute chest_white_bra_up:
            preg_art("tenny", "Standing/Clothes/Chest/White Bra/White Bra Up.png")
        attribute chest_blue_bikini_top:
            preg_art("tenny", "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top.png")
        attribute chest_blue_bikini_top_up:
            preg_art("tenny", "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top Up.png")

    # --------------------------------------------------------
    # CLOTHING BODY: BLUE SHIRT (below arms)
    # --------------------------------------------------------
    group mid_body:
        attribute mid_body_none default:
            Null()
        attribute mid_body_blue_shirt:
            preg_art("tenny", "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt.png")

    # --------------------------------------------------------
    # CLOTHING BODY: BLUE JACKET (above shirt body, below arms)
    # Arm 1: jacket body here, shirt sleeves peek above it.
    # Arms 2/3/4: over_body_none, body merged into over composite.
    # --------------------------------------------------------
    group over_body:
        attribute over_body_none default:
            Null()
        attribute over_body_blue_jacket:
            preg_art("tenny", "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket.png")

    # --------------------------------------------------------
    # CUM BODY (above torso/clothes, below arms)
    # --------------------------------------------------------
    group cum_body:
        attribute cum_body_none default:
            Null()
        attribute cum_body_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Body Cum.png"

    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Boobs Cum.png"

    # --------------------------------------------------------
    # RIGHT ARM 1 FRONT (above jacket body)
    # --------------------------------------------------------
    group arms_front:
        attribute arms_front_none default:
            Null()
        attribute arms_front_1:
            "images/characters/Tenny/Standing/Tenny Arm Right 1.png"

    # --------------------------------------------------------
    # LEFT ARM (above right arm front)
    # --------------------------------------------------------
    group left_arm:
        attribute left_arm_none default:
            Null()
        attribute left_arm_1:
            "images/characters/Tenny/Standing/Tenny Arm Left 1.png"
        attribute left_arm_2:
            "images/characters/Tenny/Standing/Tenny Arm Left 2.png"
        attribute left_arm_3:
            "images/characters/Tenny/Standing/Tenny Arm Left 3.png"
        attribute left_arm_4:
            "images/characters/Tenny/Standing/Tenny Arm Left 4.png"

    # --------------------------------------------------------
    # MID (shirt sleeves — above bare arms)
    # --------------------------------------------------------
    group mid:
        attribute mid_none default:
            Null()
        attribute mid_blue_shirt:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 1 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 1 Blue Shirt.png",
            )
        attribute mid_blue_shirt_up:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt Up.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 1 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 1 Blue Shirt.png",
            )
        attribute mid_blue_shirt_up_arm2:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt Up.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 2 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 2 Blue Shirt.png",
            )
        attribute mid_blue_shirt_up_arm3:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt Up.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 3 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 3 Blue Shirt.png",
            )
        attribute mid_blue_shirt_up_arm4:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Mid/Blue Shirt/Tenny Blue Shirt Up.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 4 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 4 Blue Shirt.png",
            )
        attribute mid_blue_shirt_arm2:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 2 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 2 Blue Shirt.png",
            )
        attribute mid_blue_shirt_arm3:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 3 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 3 Blue Shirt.png",
            )
        attribute mid_blue_shirt_arm4:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm 4 Blue Shirt.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Mid/Blue Shirt/Tenny Arm Left 4 Blue Shirt.png",
            )

    # --------------------------------------------------------
    # OVER (jacket collar + arms — outermost)
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_blue_jacket:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Collar.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm 1 Blue Jacket.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm Left 1 Blue Jacket.png",
            )
        attribute over_blue_jacket_up:
            preg_art("tenny", "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Up.png")
        attribute over_blue_jacket_arm2:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Collar.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm 2 Blue Jacket.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm Left 2 Blue Jacket.png",
            )
        attribute over_blue_jacket_arm3:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Collar.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm 3 Blue Jacket.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm Left 3 Blue Jacket.png",
            )
        attribute over_blue_jacket_arm4:
            Composite(
                (480, 960),
                (0, 0), preg_art("tenny", "Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket.png"),
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Blue Jacket Collar.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm 4 Blue Jacket.png",
                (0, 0), "images/characters/Tenny/Standing/Clothes/Over/Blue Jacket/Tenny Arm Left 4 Blue Jacket.png",
            )
        attribute over_towel:
            preg_art("tenny", "Standing/Clothes/Tenny Towel 1.png")
        attribute over_towel_arm23:
            preg_art("tenny", "Standing/Clothes/Tenny Towel 23.png")
        attribute over_towel_arm4:
            preg_art("tenny", "Standing/Clothes/Tenny Towel 4.png")

    # --------------------------------------------------------
    # CHEST RE-RENDER (above over — chest clothing on top of all arms and sleeves)
    # --------------------------------------------------------
    group chest_above_arms:
        attribute chest_above_none default:
            Null()
        attribute chest_above_corset:
            preg_art("tenny", "Standing/Clothes/Chest/White Bra/White Bra.png")
        attribute chest_above_corset_down:
            Null()
        attribute chest_above_corset_up:
            preg_art("tenny", "Standing/Clothes/Chest/White Bra/White Bra Up.png")
        attribute chest_above_bikini:
            preg_art("tenny", "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top.png")
        attribute chest_above_bikini_up:
            preg_art("tenny", "Standing/Clothes/Chest/Blue Bikini Top/Blue Bikini Top Up.png")

    # --------------------------------------------------------
    # TOWEL LEFT ARM RE-RENDER (above over/towel)
    # --------------------------------------------------------
    group towel_left_arm:
        attribute towel_arm_left_none default:
            Null()
        attribute towel_arm_left_1:
            "images/characters/Tenny/Standing/Tenny Arm Left 1.png"
        attribute towel_arm_left_2:
            "images/characters/Tenny/Standing/Tenny Arm Left 2.png"
        attribute towel_arm_left_3:
            "images/characters/Tenny/Standing/Tenny Arm Left 3.png"
        attribute towel_arm_left_4:
            "images/characters/Tenny/Standing/Tenny Arm Left 4.png"

    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Tenny/Standing/Clothes/Tenny Collar.png"

    # --------------------------------------------------------
    # CUM LAYERS (cum_body and cum_boobs moved above arms)
    # --------------------------------------------------------
    group cum_legs:
        attribute cum_legs_none default:
            Null()
        attribute cum_legs_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Legs Cum.png"

    group cum_dripping:
        attribute cum_dripping_none default:
            Null()
        attribute cum_dripping_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Dripping Cum.png"

    group cum_hand:
        attribute cum_hand_none default:
            Null()
        attribute cum_hand_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Hand Cum.png"

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------
    always:
        "images/characters/Tenny/Standing/Head/Tenny Head.png"

    # --------------------------------------------------------
    # BLUSH
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Tenny/Standing/Head/Tenny Standing Blush 1.png"
        attribute blush_2:
            "images/characters/Tenny/Standing/Head/Tenny Standing Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Face Cum.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            Null()
        attribute cum_mouth_on:
            "images/characters/Tenny/Standing/Cum/Tenny Standing Mouth Cum.png"

    # --------------------------------------------------------
    # EXPRESSIONS (BROWS / EYES / MOUTH)
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Tenny/Standing/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Tenny/Standing/Expressions/Brows/Confused.png"
        attribute brows_surprised:
            "images/characters/Tenny/Standing/Expressions/Brows/Surprised.png"
        attribute brows_sad:
            "images/characters/Tenny/Standing/Expressions/Brows/Sad.png"
        attribute brows_maniac:
            "images/characters/Tenny/Standing/Expressions/Brows/Maniac.png"

    group eyes:
        attribute eyes_normal default:
            "images/characters/Tenny/Standing/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Tenny/Standing/Expressions/Eyes/Sexy.png"
        attribute eyes_side:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_left:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_side_2:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_right:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_down:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Down.png"
        attribute eyes_looking_down_2:
            "images/characters/Tenny/Standing/Expressions/Eyes/Looking Down 2.png"
        attribute eyes_squint:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint 2.png"
        attribute eyes_squint_big:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_small:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_side_squint:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint Looking Right.png"
        attribute eyes_side_squint_2:
            "images/characters/Tenny/Standing/Expressions/Eyes/Squint Looking Left.png"
        attribute eyes_surprised:
            "images/characters/Tenny/Standing/Expressions/Eyes/Surprised.png"
        attribute eyes_surprised_2:
            "images/characters/Tenny/Standing/Expressions/Eyes/Surprised 2.png"
        attribute eyes_scared:
            "images/characters/Tenny/Standing/Expressions/Eyes/Scared.png"
        attribute eyes_blinking_left:
            "images/characters/Tenny/Standing/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blinking_right:
            "images/characters/Tenny/Standing/Expressions/Eyes/Blinking Right.png"
        attribute eyes_closed:
            "images/characters/Tenny/Standing/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Tenny/Standing/Expressions/Eyes/Closed Happy.png"

    group mouth:
        attribute mouth_normal default:
            "images/characters/Tenny/Standing/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Tenny/Standing/Expressions/Mouth/Big Smile.png"
        attribute mouth_laugh:
            "images/characters/Tenny/Standing/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Tenny/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Tenny/Standing/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Tenny/Standing/Expressions/Mouth/Tongue.png"
        attribute mouth_lipbite:
            "images/characters/Tenny/Standing/Expressions/Mouth/Lipbite.png"
        attribute mouth_kissing:
            "images/characters/Tenny/Standing/Expressions/Mouth/Kissing.png"
        attribute mouth_disgusted:
            "images/characters/Tenny/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_serious:
            "images/characters/Tenny/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_open_teeth:
            "images/characters/Tenny/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_talking:
            "images/characters/Tenny/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_sch:
            "images/characters/Tenny/Standing/Expressions/Mouth/Talk 2.png"
