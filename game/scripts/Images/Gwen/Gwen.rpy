# ============================================================
# Gwen Standing — Blinking Eyes
# ============================================================

image gwen_standing_blink_normal:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Normal.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_sexy:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Sexy.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_looking_left:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_looking_right:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_looking_down:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Looking Down.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_looking_down_2:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Looking Down 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_squint:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Squint.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_squint_2:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Squint 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_squint_looking_right:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Squint Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_squint_looking_left:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Squint Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_surprised:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Surprised.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_surprised_2:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Surprised 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_scared:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Scared.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_blinking_left:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Blinking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image gwen_standing_blink_blinking_right:
    "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Gwen/Standing/Expressions/Eyes/Blinking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

# ============================================================
# Gwen Standing Layered Sprite
# ============================================================

layeredimage gwen standing:

    # --------------------------------------------------------
    # BASE BODY ORDER (DE BAIXO PRA CIMA)
    # torso -> arms -> body chest (sempre visíveis)
    # --------------------------------------------------------
    always:
        preg_art("gwen", "Standing/Gwen_Torso.png")

    group shoes:
        attribute shoes_none default:
            Null()
        attribute shoes_thigh_highs:
            "images/characters/Gwen/Standing/Clothes/Thigh Highs.png"

    # --------------------------------------------------------
    # PANTIES (FICAM ABAIXO DA SAIA)
    # --------------------------------------------------------
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_purple:
            preg_art("gwen", "Standing/Clothes/Panties/Purple Panties/Purple Panties.png")
        attribute panties_purple_side:
            preg_art("gwen", "Standing/Clothes/Panties/Purple Panties/Purple Panties Side.png")
        attribute panties_purple_down:
            "images/characters/Gwen/Standing/Clothes/Panties/Purple Panties/Purple Panties Down.png"
        attribute panties_bikini:
            preg_art("gwen", "Standing/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties.png")
        attribute panties_bikini_side:
            preg_art("gwen", "Standing/Clothes/Panties/Black Bikini Bottom/Black bikini panties Side.png")
        attribute panties_bikini_down:
            "images/characters/Gwen/Standing/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties Down.png"

    # --------------------------------------------------------
    # LEGS / SAIA (POR CIMA DAS PANTIES)
    # --------------------------------------------------------
    group legs:
        attribute legs_none default:
            Null()
        attribute legs_blue_skirt:
            preg_art("gwen", "Standing/Clothes/Legs/Blue Skirt/Blue Skirt.png")
        attribute legs_blue_skirt_up:
            preg_art("gwen", "Standing/Clothes/Legs/Blue Skirt/Blue Skirt Up.png")

    # Belly (pregnancy stage 2): above lower clothes, below arms and chest
    always:
        preg_art("gwen", "+Standing/belly")

    # --------------------------------------------------------
    # RIGHT ARM (below chest — all positions)
    # --------------------------------------------------------
    group right_arm:
        attribute arm_right_none:
            Null()
        attribute arm_right_1 default:
            "images/characters/Gwen/Standing/Gwen Arm Right 1.png"
        attribute arm_right_2:
            "images/characters/Gwen/Standing/Gwen Arm Right 2.png"
        attribute arm_right_3:
            "images/characters/Gwen/Standing/Gwen Arm Right 3.png"
        attribute arm_right_4:
            preg_art("gwen", "Standing/Gwen Arm Right 4.png")

    # --------------------------------------------------------
    # CHEST (BODY / PIERCING / CLOTHES)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("gwen", "Standing/Gwen_Chest.png")
        attribute chest_piercing:
            preg_art("gwen", "Standing/Gwen_Chest_Piercing.png")

    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("gwen", "Standing/Clothes/Chest/Corset/Cover.png")
        attribute chest_corset_down:
            preg_art("gwen", "Standing/Clothes/Chest/Corset/Base.png")
        attribute chest_bikini_top:
            preg_art("gwen", "Standing/Clothes/Chest/Black Bikini Top/Black Bikini Top.png")
        attribute chest_bikini_top_up:
            preg_art("gwen", "Standing/Clothes/Chest/Black Bikini Top/Black bikini top Up.png")

    # --------------------------------------------------------
    # LEFT ARM (above chest — all positions)
    # --------------------------------------------------------
    group left_arm:
        attribute left_arm_none default:
            Null()
        attribute left_arm_1:
            "images/characters/Gwen/Standing/Gwen Arm Left 1.png"
        attribute left_arm_2:
            "images/characters/Gwen/Standing/Gwen Arm Left 2.png"
        attribute left_arm_3:
            "images/characters/Gwen/Standing/Gwen Arm Left 3.png"
        attribute left_arm_4:
            "images/characters/Gwen/Standing/Gwen Arm Left 4.png"

    # --------------------------------------------------------
    # RIGHT ARM 1 FRONT (re-rendered above chest for arm_1)
    # --------------------------------------------------------
    group arms_front:
        attribute arms_front_none default:
            Null()
        attribute arms_front_1:
            "images/characters/Gwen/Standing/Gwen Arm Right 1.png"

    # --------------------------------------------------------
    # MID (placeholder — no mid items yet)
    # --------------------------------------------------------
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER — right arm sleeve only (left sleeve split to over_left, above corset)
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm 1 Long Shirt.png"
        attribute over_long_shirt_arm2:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm 2 Long Shirt.png"
        attribute over_long_shirt_arm3:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm 3 Long Shirt.png"
        attribute over_long_shirt_arm4:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm 4 Long Shirt.png"
        attribute over_towel:
            preg_art("gwen", "Standing/Clothes/Gwen Towel.png")

    # --------------------------------------------------------
    # CHEST RE-RENDER (unused — kept for attribute compatibility)
    # --------------------------------------------------------
    group chest_above_arms:
        attribute chest_above_none default:
            Null()
        attribute chest_above_corset:
            preg_art("gwen", "Standing/Clothes/Chest/Corset/Cover.png")
        attribute chest_above_corset_down:
            preg_art("gwen", "Standing/Clothes/Chest/Corset/Base.png")
        attribute chest_above_corset_up:
            Null()
        attribute chest_above_bikini:
            preg_art("gwen", "Standing/Clothes/Chest/Black Bikini Top/Black Bikini Top.png")
        attribute chest_above_bikini_up:
            preg_art("gwen", "Standing/Clothes/Chest/Black Bikini Top/Black bikini top Up.png")

    # --------------------------------------------------------
    # OVER LEFT — left arm sleeve above corset
    # --------------------------------------------------------
    group over_left:
        attribute over_left_none default:
            Null()
        attribute over_left_1:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm Left 1 Long Shirt.png"
        attribute over_left_2:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm Left 2 Long Shirt.png"
        attribute over_left_3:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm Left 3 Long Shirt.png"
        attribute over_left_4:
            "images/characters/Gwen/Standing/Clothes/Over/Long Shirt/Gwen Arm Left 4 Long Shirt.png"

    # --------------------------------------------------------
    # TOWEL ARM RE-RENDER (above over/towel)
    # --------------------------------------------------------
    group towel_right_arm:
        attribute towel_arm_right_none default:
            Null()
        attribute towel_arm_right_1:
            "images/characters/Gwen/Standing/Gwen Arm Right 1.png"
        attribute towel_arm_right_2:
            "images/characters/Gwen/Standing/Gwen Arm Right 2.png"
        attribute towel_arm_right_3:
            "images/characters/Gwen/Standing/Gwen Arm Right 3.png"
        attribute towel_arm_right_4:
            preg_art("gwen", "Standing/Gwen Arm Right 4.png")

    group towel_left_arm:
        attribute towel_arm_left_none default:
            Null()
        attribute towel_arm_left_1:
            "images/characters/Gwen/Standing/Gwen Arm Left 1.png"
        attribute towel_arm_left_2:
            "images/characters/Gwen/Standing/Gwen Arm Left 2.png"
        attribute towel_arm_left_3:
            "images/characters/Gwen/Standing/Gwen Arm Left 3.png"
        attribute towel_arm_left_4:
            "images/characters/Gwen/Standing/Gwen Arm Left 4.png"

    group towel_arms_front:
        attribute towel_arms_front_none default:
            Null()
        attribute towel_arms_front_1:
            "images/characters/Gwen/Standing/Gwen Arm Right 1.png"

    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Gwen/Standing/Clothes/Gwen Collar.png"

    # --------------------------------------------------------
    # CUM LAYERS (acima de tudo, abaixo apenas das roupas)
    # --------------------------------------------------------
    group cum_body:
        attribute cum_body_none default:
            Null()
        attribute cum_body_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Body Cum.png"

    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Boobs Cum.png"

    group cum_legs:
        attribute cum_legs_none default:
            Null()
        attribute cum_legs_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Legs Cum.png"

    group cum_dripping:
        attribute cum_dripping_none default:
            Null()
        attribute cum_dripping_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Dripping Cum.png"

    group cum_hand:
        attribute cum_hand_none default:
            Null()
        attribute cum_hand_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Hand Cum.png"

    # --------------------------------------------------------
    # HEAD (unica, sempre a mesma)
    # --------------------------------------------------------
    always:
        "images/characters/Gwen/Standing/Head/Gwen Head.png"

    # --------------------------------------------------------
    # BLUSH (acima da head)
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Gwen/Standing/Head/Gwen Standing Blush 1.png"
        attribute blush_2:
            "images/characters/Gwen/Standing/Head/Gwen Standing Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE (acima da head e blush)
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Face Cum.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            Null()
        attribute cum_mouth_on:
            "images/characters/Gwen/Standing/Cum/Gwen Standing Mouth Cum.png"

    # --------------------------------------------------------
    # EXPRESSIONS (BROWS / EYES / MOUTH)
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Gwen/Standing/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Gwen/Standing/Expressions/Brows/Confused.png"
        attribute brows_surprised:
            "images/characters/Gwen/Standing/Expressions/Brows/Surprised.png"
        attribute brows_sad:
            "images/characters/Gwen/Standing/Expressions/Brows/Sad.png"
        attribute brows_maniac:
            "images/characters/Gwen/Standing/Expressions/Brows/Maniac.png"

    group eyes:
        attribute eyes_normal default:
            "images/characters/Gwen/Standing/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Gwen/Standing/Expressions/Eyes/Sexy.png"
        attribute eyes_side:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_left:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_side_2:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_right:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_down:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Down.png"
        attribute eyes_looking_down_2:
            "images/characters/Gwen/Standing/Expressions/Eyes/Looking Down 2.png"
        attribute eyes_squint:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint 2.png"
        attribute eyes_squint_big:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_small:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_side_squint:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint Looking Right.png"
        attribute eyes_side_squint_2:
            "images/characters/Gwen/Standing/Expressions/Eyes/Squint Looking Left.png"
        attribute eyes_surprised:
            "images/characters/Gwen/Standing/Expressions/Eyes/Surprised.png"
        attribute eyes_surprised_2:
            "images/characters/Gwen/Standing/Expressions/Eyes/Surprised 2.png"
        attribute eyes_scared:
            "images/characters/Gwen/Standing/Expressions/Eyes/Scared.png"
        attribute eyes_blinking_left:
            "images/characters/Gwen/Standing/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blinking_right:
            "images/characters/Gwen/Standing/Expressions/Eyes/Blinking Right.png"
        attribute eyes_closed:
            "images/characters/Gwen/Standing/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Gwen/Standing/Expressions/Eyes/Closed Happy.png"

    group mouth:
        attribute mouth_normal default:
            "images/characters/Gwen/Standing/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Gwen/Standing/Expressions/Mouth/Big Smile.png"
        attribute mouth_laugh:
            "images/characters/Gwen/Standing/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Gwen/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Gwen/Standing/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Gwen/Standing/Expressions/Mouth/Tongue.png"
        attribute mouth_lipbite:
            "images/characters/Gwen/Standing/Expressions/Mouth/Lipbite.png"
        attribute mouth_kissing:
            "images/characters/Gwen/Standing/Expressions/Mouth/Kissing.png"
        attribute mouth_disgusted:
            "images/characters/Gwen/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_serious:
            "images/characters/Gwen/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_open_teeth:
            "images/characters/Gwen/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_talking:
            "images/characters/Gwen/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_sch:
            "images/characters/Gwen/Standing/Expressions/Mouth/Talk 2.png"

