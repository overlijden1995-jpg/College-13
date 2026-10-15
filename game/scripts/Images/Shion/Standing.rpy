# ============================================================
# Shion Standing — Blinking Eyes
# ============================================================

image shion_standing_blink_normal:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Normal.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_sexy:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Sexy.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_looking_left:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_looking_right:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_looking_down:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Looking Down.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_looking_down_2:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Looking Down 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_squint:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Squint.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_squint_2:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Squint 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_squint_looking_right:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Squint Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_squint_looking_left:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Squint Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_surprised:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Surprised.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_surprised_2:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Surprised 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_scared:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Scared.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_blinking_left:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Blinking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

image shion_standing_blink_blinking_right:
    "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Shion/Standing/Expression/Eyes/Blinking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        pause 0.12
        repeat

# ============================================================
# Shion Standing Layered Sprite
# ============================================================

layeredimage shion standing:

    # --------------------------------------------------------
    # BASE BODY (legs behind torso)
    # --------------------------------------------------------
    always:
        "images/characters/Shion/Standing/Left Leg.png"
    always:
        "images/characters/Shion/Standing/Right Leg.png"

    always:
        "images/characters/Shion/Standing/Torso.png"

    # SHOES (placeholder)
    group shoes:
        attribute shoes_none default:
            Null()

    # --------------------------------------------------------
    # LOWER BODY CLOTHING (below belly)
    # --------------------------------------------------------
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_on:
            preg_art("shion", "Standing/Clothes/Red Panties/Red Panties.png")
        attribute panties_semi:
            "images/characters/Shion/Standing/Clothes/Red Panties/Red Panties Down.png"
        attribute panties_bikini:
            preg_art("shion", "Standing/Clothes/Bikini/Bikini Bottom.png")

    group pants:
        attribute pants_none default:
            Null()
        attribute pants_on:
            preg_art("shion", "Standing/Clothes/Pants Legs/White Pants.png")
        attribute pants_semi:
            "images/characters/Shion/Standing/Clothes/Pants Legs/White Pants Down.png"

    # LEGS (skirt clothing slot — placeholder)
    group legs:
        attribute legs_none default:
            Null()

    # --------------------------------------------------------
    # ARMS (below chest and all clothes). The right arm hangs BEHIND the belly (author).
    # --------------------------------------------------------
    group right_arm:
        attribute arm_right_none:
            Null()
        attribute arm_right_1 default:
            "images/characters/Shion/Standing/Arms/Arm Right 1.png"
        attribute arm_right_2:
            "images/characters/Shion/Standing/Arms/Arm Right 2.png"
        attribute arm_right_3:
            "images/characters/Shion/Standing/Arms/Arm Righ 3.png"
        attribute arm_right_4:
            Null()

    # Belly (pregnancy stage 2: on top of panties / pants and of the right arm, under the left arm and the chest)
    always:
        preg_art("shion", "+Standing/belly")

    group left_arm:
        attribute left_arm_none:
            Null()
        attribute left_arm_1 default:
            "images/characters/Shion/Standing/Arms/Arm Left 1.png"
        attribute left_arm_2:
            "images/characters/Shion/Standing/Arms/Arm Left 2.png"
        attribute left_arm_3:
            "images/characters/Shion/Standing/Arms/Arm Left 3.png"
        attribute left_arm_4:
            "images/characters/Shion/Standing/Arms/Arms Crossed.png"

    # ARMS FRONT (placeholder)
    group arms_front:
        attribute arms_front_none default:
            Null()
        attribute arms_front_1:
            Null()

    # --------------------------------------------------------
    # CHEST (above arms)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("shion", "Standing/Chest/Chest.png")
        attribute chest_piercing:
            preg_art("shion", "Standing/Chest/Chest Piercing.png")
        # under a bra / bikini top (has_chest_clothes_body, scene_config): at stage 1+ the XL chest
        # replaces it (the XL cups cover the nipples)
        attribute chest_clothes:
            preg_art("shion", "Standing/Chest/Boobs No Nip.png")

    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_bra:
            preg_art("shion", "Standing/Clothes/Chest Bra/Red Bra.png")
        attribute chest_bra_semi:
            preg_art("shion", "Standing/Clothes/Chest Bra/Red Bra Down.png")
        attribute chest_bikini_top:
            preg_art("shion", "Standing/Clothes/Bikini/Bikini Top.png")

    # --------------------------------------------------------
    # MID BODY (vest — per-arm composites)
    # --------------------------------------------------------
    group mid_body:
        attribute mid_body_none default:
            Null()
        attribute mid_body_vest:
            preg_art("shion", "Standing/Clothes/Vest Mid/Vest Arms 1.png")
        attribute mid_body_vest_arm2:
            preg_art("shion", "Standing/Clothes/Vest Mid/Vest Arms 2.png")
        attribute mid_body_vest_arm3:
            preg_art("shion", "Standing/Clothes/Vest Mid/Vest Arms 3.png")
        attribute mid_body_vest_arm4:
            preg_art("shion", "Standing/Clothes/Vest Mid/Vest Arms 4.png")

    # MID (clothing system slot — placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER BODY (jacket — per-arm composites)
    # --------------------------------------------------------
    group over_body:
        attribute over_body_none default:
            Null()
        attribute over_body_jacket:
            preg_art("shion", "Standing/Clothes/Jacket Over/Jacket Arms 1.png")
        attribute over_body_jacket_arm2:
            preg_art("shion", "Standing/Clothes/Jacket Over/Jacket Arms 2.png")
        attribute over_body_jacket_arm3:
            preg_art("shion", "Standing/Clothes/Jacket Over/Jacket Arms 3.png")
        attribute over_body_jacket_arm4:
            preg_art("shion", "Standing/Clothes/Jacket Over/Jacket Arms 4.png")

    # --------------------------------------------------------
    # CUM
    # --------------------------------------------------------
    group cum_body:
        attribute cum_body_none default:
            Null()
        attribute cum_body_on:
            "images/characters/Shion/Standing/Cum/Cum Body.png"

    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Shion/Standing/Cum/Cum Boobs.png"

    # --------------------------------------------------------
    # TOWEL
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_towel:
            preg_art("shion", "Standing/Towel/Towell.png")

    # --------------------------------------------------------
    # TOWEL ARMS (placeholders — reuse regular arm art)
    # --------------------------------------------------------
    group towel_arm_right:
        attribute towel_arm_right_none default:
            Null()
        attribute towel_arm_right_1:
            "images/characters/Shion/Standing/Arms/Arm Right 1.png"

    group towel_arm_left:
        attribute towel_arm_left_none default:
            Null()
        attribute towel_arm_left_1:
            "images/characters/Shion/Standing/Arms/Arm Left 1.png"
        attribute towel_arm_left_2:
            "images/characters/Shion/Standing/Arms/Arm Left 2.png"
        attribute towel_arm_left_3:
            "images/characters/Shion/Standing/Arms/Arm Left 3.png"
        attribute towel_arm_left_4:
            "images/characters/Shion/Standing/Arms/Arms Crossed.png"

    group towel_arms_front:
        attribute towel_arms_front_none default:
            Null()
        attribute towel_arms_front_1:
            Null()

    # --------------------------------------------------------
    # CUM LEGS / DRIPPING
    # --------------------------------------------------------
    group cum_legs:
        attribute cum_legs_none default:
            Null()
        attribute cum_legs_on:
            "images/characters/Shion/Standing/Cum/Cum Legs.png"

    group cum_dripping:
        attribute cum_dripping_none default:
            Null()
        attribute cum_dripping_on:
            "images/characters/Shion/Standing/Cum/Cum Dripping.png"

    # CUM HAND (placeholder)
    group cum_hand:
        attribute cum_hand_none default:
            Null()
        attribute cum_hand_on:
            Null()

    # COLLAR (placeholder)
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------
    always:
        "images/characters/Shion/Standing/Head.png"

    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Shion/Standing/Head/Blush 1.png"
        attribute blush_2:
            "images/characters/Shion/Standing/Head/Blush 2.png"

    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Shion/Standing/Cum/Cum Face.png"

    # CUM MOUTH (placeholder)
    group cum_mouth:
        attribute cum_mouth_none default:
            Null()
        attribute cum_mouth_on:
            Null()

    # --------------------------------------------------------
    # TOWEL HEAD
    # --------------------------------------------------------
    group towel_head:
        attribute towel_head_none default:
            Null()
        attribute towel_head_on:
            "images/characters/Shion/Standing/Towel/Head Towel.png"

    # --------------------------------------------------------
    # EXPRESSIONS
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Shion/Standing/Expression/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Shion/Standing/Expression/Brows/Confused.png"
        attribute brows_surprised:
            "images/characters/Shion/Standing/Expression/Brows/Surprised.png"
        attribute brows_sad:
            "images/characters/Shion/Standing/Expression/Brows/Sad.png"
        attribute brows_maniac:
            "images/characters/Shion/Standing/Expression/Brows/Maniac.png"
        attribute brows_angry:
            "images/characters/Shion/Standing/Expression/Brows/Angry.png"
        attribute brows_confused_2:
            "images/characters/Shion/Standing/Expression/Brows/Confused 2.png"

    group eyes:
        attribute eyes_normal default:
            "images/characters/Shion/Standing/Expression/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Shion/Standing/Expression/Eyes/Sexy.png"
        attribute eyes_side:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Left.png"
        attribute eyes_looking_left:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Left.png"
        attribute eyes_side_2:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Right.png"
        attribute eyes_looking_right:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Right.png"
        attribute eyes_looking_down:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Down.png"
        attribute eyes_looking_down_2:
            "images/characters/Shion/Standing/Expression/Eyes/Looking Down 2.png"
        attribute eyes_squint:
            "images/characters/Shion/Standing/Expression/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Shion/Standing/Expression/Eyes/Squint 2.png"
        attribute eyes_squint_big:
            "images/characters/Shion/Standing/Expression/Eyes/Squint.png"
        attribute eyes_small:
            "images/characters/Shion/Standing/Expression/Eyes/Squint.png"
        attribute eyes_side_squint:
            "images/characters/Shion/Standing/Expression/Eyes/Squint Looking Right.png"
        attribute eyes_side_squint_2:
            "images/characters/Shion/Standing/Expression/Eyes/Squint Looking Left.png"
        attribute eyes_surprised:
            "images/characters/Shion/Standing/Expression/Eyes/Surprised.png"
        attribute eyes_surprised_2:
            "images/characters/Shion/Standing/Expression/Eyes/Surprised 2.png"
        attribute eyes_scared:
            "images/characters/Shion/Standing/Expression/Eyes/Scared.png"
        attribute eyes_blinking_left:
            "images/characters/Shion/Standing/Expression/Eyes/Blinking Left.png"
        attribute eyes_blinking_right:
            "images/characters/Shion/Standing/Expression/Eyes/Blinking Right.png"
        attribute eyes_closed:
            "images/characters/Shion/Standing/Expression/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Shion/Standing/Expression/Eyes/Closed Happy.png"

    group mouth:
        attribute mouth_normal default:
            "images/characters/Shion/Standing/Expression/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Shion/Standing/Expression/Mouth/Big Smile.png"
        attribute mouth_laugh:
            "images/characters/Shion/Standing/Expression/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Shion/Standing/Expression/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Shion/Standing/Expression/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Shion/Standing/Expression/Mouth/Tongue.png"
        attribute mouth_lipbite:
            "images/characters/Shion/Standing/Expression/Mouth/Lipbite.png"
        attribute mouth_kissing:
            "images/characters/Shion/Standing/Expression/Mouth/Kissing.png"
        attribute mouth_disgusted:
            "images/characters/Shion/Standing/Expression/Mouth/Sad.png"
        attribute mouth_serious:
            "images/characters/Shion/Standing/Expression/Mouth/Sad.png"
        attribute mouth_open_teeth:
            "images/characters/Shion/Standing/Expression/Mouth/Talk.png"
        attribute mouth_talking:
            "images/characters/Shion/Standing/Expression/Mouth/Talk.png"
        attribute mouth_sch:
            "images/characters/Shion/Standing/Expression/Mouth/Talk 2.png"
