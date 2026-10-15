# ============================================================
# Rogue Standing — Blinking Eyes
# ============================================================

image rogue_standing_blink_normal:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Normal.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_sexy:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Sexy.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_looking_left:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_looking_right:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_looking_down:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Looking Down.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_looking_down_2:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Looking Down 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_squint:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Squint.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_squint_2:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Squint 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_squint_looking_right:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Squint Looking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_squint_looking_left:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Squint Looking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_surprised:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Surprised.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_surprised_2:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Surprised 2.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_scared:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Scared.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_blinking_left:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Blinking Left.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

image rogue_standing_blink_blinking_right:
    "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
    pause 0.08
    block:
        "images/characters/Rogue/Standing/Expressions/Eyes/Blinking Right.png"
        pause renpy.random.uniform(3.0, 7.0)
        "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        pause 0.12
        repeat

# ============================================================
# Rogue Standing Layered Sprite
# ============================================================
# Layer order follows artist guide (bottom to top):
#   Torso > Shoes > Panties > Skirt > Left Arm > Crop Top >
#   Right Arm > Gloves > Boobs > Over > Cum > Head > Collar >
#   Blush > Cum Face > Brows > Eyes > Mouth

layeredimage rogue standing:

    # --------------------------------------------------------
    # BASE BODY (torso includes legs)
    # --------------------------------------------------------
    always:
        preg_art("rogue", "Standing/Rogue_Torso.png")

    # Full belly (pregnancy stage 2): right above torso, behind panties/skirt/arms/chest
    always:
        preg_art("rogue", "+Standing/belly")

    # --------------------------------------------------------
    # SHOES
    # --------------------------------------------------------
    group shoes:
        attribute shoes_none default:
            Null()
        attribute shoes_thigh_highs:
            "images/characters/Rogue/Standing/Clothes/High Thighs.png"

    # --------------------------------------------------------
    # PANTIES
    # --------------------------------------------------------
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_purple:
            "images/characters/Rogue/Standing/Clothes/Panties/Green Panties/Green Panties.png"
        attribute panties_purple_side:
            "images/characters/Rogue/Standing/Clothes/Panties/Green Panties/Green Panties Side.png"
        attribute panties_purple_down:
            "images/characters/Rogue/Standing/Clothes/Panties/Green Panties/Green Panties Down.png"
        attribute panties_bikini:
            preg_art("rogue", "Standing/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Up.png")
        attribute panties_bikini_side:
            preg_art("rogue", "Standing/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Side.png")
        attribute panties_bikini_down:
            "images/characters/Rogue/Standing/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Down.png"

    # --------------------------------------------------------
    # SKIRT
    # --------------------------------------------------------
    group legs:
        attribute legs_none default:
            Null()
        attribute legs_blue_skirt:
            preg_art("rogue", "Standing/Clothes/Legs/Black Skirt/Black Skirt.png")
        attribute legs_blue_skirt_up:
            preg_art("rogue", "Standing/Clothes/Legs/Black Skirt/Black Skirt Up.png")

    # --------------------------------------------------------
    # --------------------------------------------------------
    # RIGHT ARM (below chest — all positions)
    # --------------------------------------------------------
    group right_arm:
        attribute arm_right_none:
            Null()
        attribute arm_right_1 default:
            "images/characters/Rogue/Standing/Rogue Arm Right 1.png"
        attribute arm_right_2:
            "images/characters/Rogue/Standing/Rogue Arm Right 2.png"
        attribute arm_right_3:
            "images/characters/Rogue/Standing/Rogue Arm Right 3.png"
        attribute arm_right_4:
            preg_art("rogue", "Standing/Rogue Arm Right 4.png")

    # --------------------------------------------------------
    # GLOVES (above right arm, below chest)
    # --------------------------------------------------------
    group gloves:
        attribute gloves_none default:
            Null()
        attribute gloves_on:
            "images/characters/Rogue/Standing/Clothes/Rogue Gloves.png"

    # --------------------------------------------------------
    # CROP TOP BASE (below boobs, stays when ChestUp)
    # --------------------------------------------------------
    group chest_base:
        attribute chest_base_none default:
            Null()
        attribute chest_base_on:
            preg_art("rogue", "Standing/Clothes/Chest/Crop Top/Base.png")

    # --------------------------------------------------------
    # CHEST BODY (nude — always visible, between Base and Cover)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("rogue", "Standing/Rogue_Chest.png")
        attribute chest_piercing:
            preg_art("rogue", "Standing/Boobs Piercing.png")

    # --------------------------------------------------------
    # CROP TOP COVER (above boobs, hidden when ChestUp)
    # --------------------------------------------------------
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("rogue", "Standing/Clothes/Chest/Crop Top/Cover.png")
        attribute chest_corset_down:
            Null()
        attribute chest_bikini_top:
            preg_art("rogue", "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top.png")
        attribute chest_bikini_top_up:
            preg_art("rogue", "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top Up.png")

    # --------------------------------------------------------
    # LEFT ARM (above chest — all positions)
    # --------------------------------------------------------
    group left_arm:
        attribute left_arm_none default:
            Null()
        attribute left_arm_1:
            "images/characters/Rogue/Standing/Rogue Arm Left 1.png"
        attribute left_arm_2:
            "images/characters/Rogue/Standing/Rogue Arm Left 2.png"
        attribute left_arm_3:
            "images/characters/Rogue/Standing/Rogue Arm Left 3.png"
        attribute left_arm_4:
            "images/characters/Rogue/Standing/Rogue Arm Left 4.png"

    # --------------------------------------------------------
    # RIGHT ARM 1 FRONT (re-rendered above chest for arm_1)
    # --------------------------------------------------------
    group arms_front:
        attribute arms_front_none default:
            Null()
        attribute arms_front_1:
            "images/characters/Rogue/Standing/Rogue Arm Right 1.png"

    # --------------------------------------------------------
    # MID (placeholder — no mid items yet)
    # --------------------------------------------------------
    group mid:
        attribute mid_none default:
            Null()

    # --------------------------------------------------------
    # OVER — arm_1 sleeves only (body split to over_body above crop top)
    # arm_2/3/4 full meshes also in over_body (over_none here)
    # --------------------------------------------------------
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            Composite(
                (480, 960),
                (0, 0), "images/characters/Rogue/Standing/Clothes/Over/Green Mesh/Rogue Arm Left 1 Mesh Top.png",
                (0, 0), "images/characters/Rogue/Standing/Clothes/Over/Green Mesh/Rogue Arm Right 1 Mesh Top.png",
            )
        attribute over_towel:
            preg_art("rogue", "Standing/Clothes/Rogue Towel.png")

    # --------------------------------------------------------
    # CHEST RE-RENDER (above over sleeves)
    # --------------------------------------------------------
    group chest_above_arms:
        attribute chest_above_none default:
            Null()
        attribute chest_above_corset:
            preg_art("rogue", "Standing/Clothes/Chest/Crop Top/Cover.png")
        attribute chest_above_corset_down:
            Null()
        attribute chest_above_corset_up:
            Null()
        attribute chest_above_bikini:
            preg_art("rogue", "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top.png")
        attribute chest_above_bikini_up:
            preg_art("rogue", "Standing/Clothes/Chest/Green Bikini Top/Green Bikini Top Up.png")

    # --------------------------------------------------------
    # OVER BODY — mesh body (arm_1) or full mesh (arm_2/3/4), above crop top
    # --------------------------------------------------------
    group over_body:
        attribute over_body_none default:
            Null()
        attribute over_body_mesh:
            preg_art("rogue", "Standing/Clothes/Over/Green Mesh/Rogue Arm 1 Mesh Top.png")
        attribute over_body_mesh_arm2:
            preg_art("rogue", "Standing/Clothes/Over/Green Mesh/Mesh Top 2.png")
        attribute over_body_mesh_arm3:
            preg_art("rogue", "Standing/Clothes/Over/Green Mesh/Mesh Top 3.png")
        attribute over_body_mesh_arm4:
            preg_art("rogue", "Standing/Clothes/Over/Green Mesh/Mesh Top 4.png")

    # Arms re-rendered on top of towel
    group towel_right_arm:
        attribute towel_arm_right_none default:
            Null()
        attribute towel_arm_right_1:
            "images/characters/Rogue/Standing/Rogue Arm Right 1.png"
        attribute towel_arm_right_2:
            "images/characters/Rogue/Standing/Rogue Arm Right 2.png"
        attribute towel_arm_right_3:
            "images/characters/Rogue/Standing/Rogue Arm Right 3.png"
        attribute towel_arm_right_4:
            preg_art("rogue", "Standing/Rogue Arm Right 4.png")

    group towel_left_arm:
        attribute towel_arm_left_none default:
            Null()
        attribute towel_arm_left_1:
            "images/characters/Rogue/Standing/Rogue Arm Left 1.png"
        attribute towel_arm_left_2:
            "images/characters/Rogue/Standing/Rogue Arm Left 2.png"
        attribute towel_arm_left_3:
            "images/characters/Rogue/Standing/Rogue Arm Left 3.png"
        attribute towel_arm_left_4:
            "images/characters/Rogue/Standing/Rogue Arm Left 4.png"

    group towel_arms_front:
        attribute towel_arms_front_none default:
            Null()
        attribute towel_arms_front_1:
            "images/characters/Rogue/Standing/Rogue Arm Right 1.png"

    # --------------------------------------------------------
    # CUM LAYERS
    # --------------------------------------------------------
    group cum_body:
        attribute cum_body_none default:
            Null()
        attribute cum_body_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Body Cum.png"

    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Boobs Cum.png"

    group cum_legs:
        attribute cum_legs_none default:
            Null()
        attribute cum_legs_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Legs Cum.png"

    group cum_dripping:
        attribute cum_dripping_none default:
            Null()
        attribute cum_dripping_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Dripping Cum.png"

    group cum_hand:
        attribute cum_hand_none default:
            Null()
        attribute cum_hand_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Hand Cum.png"

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------
    always:
        "images/characters/Rogue/Standing/Head/Rogue Head.png"

    # --------------------------------------------------------
    # COLLAR (above head per artist guide)
    # --------------------------------------------------------
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/Standing/Clothes/Rogue Collar.png"

    # Towel left arm (above head/collar — holding the towel)
    group towel_larm_layer:
        attribute towel_left_arm_none default:
            Null()
        attribute towel_left_arm:
            "images/characters/Rogue/Standing/Clothes/Rogue Towel Arm.png"

    # --------------------------------------------------------
    # BLUSH
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Rogue/Standing/Head/Rogue Standing Blush 1.png"
        attribute blush_2:
            "images/characters/Rogue/Standing/Head/Rogue Standing Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Face Cum.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            Null()
        attribute cum_mouth_on:
            "images/characters/Rogue/Standing/Cum/Rogue Standing Mouth Cum.png"

    # --------------------------------------------------------
    # EXPRESSIONS
    # --------------------------------------------------------
    group brows:
        attribute brows_normal default:
            "images/characters/Rogue/Standing/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Rogue/Standing/Expressions/Brows/Confused.png"
        attribute brows_surprised:
            "images/characters/Rogue/Standing/Expressions/Brows/Surprised.png"
        attribute brows_sad:
            "images/characters/Rogue/Standing/Expressions/Brows/Sad.png"
        attribute brows_maniac:
            "images/characters/Rogue/Standing/Expressions/Brows/Maniac.png"

    group eyes:
        attribute eyes_normal default:
            "images/characters/Rogue/Standing/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Rogue/Standing/Expressions/Eyes/Sexy.png"
        attribute eyes_side:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_left:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Left.png"
        attribute eyes_side_2:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_right:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_down:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Down.png"
        attribute eyes_looking_down_2:
            "images/characters/Rogue/Standing/Expressions/Eyes/Looking Down 2.png"
        attribute eyes_squint:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint 2.png"
        attribute eyes_squint_big:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_small:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint.png"
        attribute eyes_side_squint:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint Looking Right.png"
        attribute eyes_side_squint_2:
            "images/characters/Rogue/Standing/Expressions/Eyes/Squint Looking Left.png"
        attribute eyes_surprised:
            "images/characters/Rogue/Standing/Expressions/Eyes/Surprised.png"
        attribute eyes_surprised_2:
            "images/characters/Rogue/Standing/Expressions/Eyes/Surprised 2.png"
        attribute eyes_scared:
            "images/characters/Rogue/Standing/Expressions/Eyes/Scared.png"
        attribute eyes_blinking_left:
            "images/characters/Rogue/Standing/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blinking_right:
            "images/characters/Rogue/Standing/Expressions/Eyes/Blinking Right.png"
        attribute eyes_closed:
            "images/characters/Rogue/Standing/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Rogue/Standing/Expressions/Eyes/Closed Happy.png"

    group mouth:
        attribute mouth_normal default:
            "images/characters/Rogue/Standing/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Rogue/Standing/Expressions/Mouth/Big Smile.png"
        attribute mouth_laugh:
            "images/characters/Rogue/Standing/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Rogue/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Rogue/Standing/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Rogue/Standing/Expressions/Mouth/Tongue.png"
        attribute mouth_lipbite:
            "images/characters/Rogue/Standing/Expressions/Mouth/Lipbite.png"
        attribute mouth_kissing:
            "images/characters/Rogue/Standing/Expressions/Mouth/Kissing.png"
        attribute mouth_disgusted:
            "images/characters/Rogue/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_serious:
            "images/characters/Rogue/Standing/Expressions/Mouth/Sad.png"
        attribute mouth_open_teeth:
            "images/characters/Rogue/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_talking:
            "images/characters/Rogue/Standing/Expressions/Mouth/Talk.png"
        attribute mouth_sch:
            "images/characters/Rogue/Standing/Expressions/Mouth/Talk 2.png"
