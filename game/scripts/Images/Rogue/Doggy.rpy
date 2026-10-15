# ============================================================
# Rogue Doggy Layered Sprite
# ============================================================
# Head 2 has the face baked in — no separate expression layers.
# Same structure as Gwen. Crop Top replaces Corset.
# Mesh Top as over. Green Panties/Bikini replaces Purple/Black.

layeredimage rogue doggy:

    # --- Arm (bottommost layer) ---
    group arms:
        attribute arms_1 default:
            "images/characters/Rogue/Doggy/Rogue Doggy arm 1.png"
        attribute arms_none:
            Null()

    # --- Body ---
    group body:
        attribute body_base default:
            "images/characters/Rogue/Doggy/Rogue Doggy Body 1.png"

    # --- Body Safe removed from layeredimage — now standalone for penis masking ---

    # --- Calves & Legs removed from layeredimage — now standalone animated layers ---

    # --- Butt Gap (standalone layers handle display during scenes) ---
    group butt_gap:
        attribute butt_gap_base default:
            Null()
        attribute butt_gap_none:
            Null()

    # --- Butt Base (static preview; hidden during scene — standalone animates) ---
    group butt_top:
        attribute butt_top_none default:
            Null()
        attribute butt_top_base:
            "images/characters/Rogue/Doggy/Ass/Clean Base Center.png"

    # --- Chest clothing ---
    group torso_chest:
        attribute torso_chest_none default:
            Null()
        attribute torso_chest_corset:
            "images/characters/Rogue/Doggy/Clothes/Chest/Crop Top/Rogue Doggy Crop Top.png"
        attribute torso_chest_bikini_top:
            "images/characters/Rogue/Doggy/Clothes/Chest/Black Bikini Top/Rogue Doggy Black Bikini Top.png"

    # --- Mid (placeholder) ---
    group mid:
        attribute mid_none default:
            Null()

    # --- Over clothing (Mesh Top) — above chest ---
    group torso_over:
        attribute torso_over_none default:
            Null()
        attribute torso_over_mesh_top:
            "images/characters/Rogue/Doggy/Clothes/Over/Mesh Top/Rogue Doggy Mesh Top.png"

    # --- Collar (above body/clothes, below head) ---
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Green Collar.png"

    # --- Head ---
    group head:
        attribute head_base default:
            "images/characters/Rogue/Doggy/Head/Rogue Doggy Head 2.png"

# ============================================================
# Rogue-specific leg rotation — LEFT (anchor 845, 590)
# ============================================================
transform dg_rogue_leg_left_speed0():
    subpixel True
    matrixanchor (845, 590)

transform dg_rogue_leg_left_speed1():
    subpixel True
    matrixanchor (845, 590)
    block:
        pause 0.35
        ease 0.20 matrixtransform RotateMatrix(0, 0, -8)
        pause 0.25
        ease 1.20 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_rogue_leg_left_speed2():
    subpixel True
    matrixanchor (845, 590)
    block:
        pause 0.12
        ease 0.12 matrixtransform RotateMatrix(0, 0, -12)
        pause 0.10
        easein 0.45 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_rogue_leg_left_speed3():
    subpixel True
    matrixanchor (845, 590)
    block:
        ease 0.18 matrixtransform RotateMatrix(0, 0, -14)
        easein 0.18 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# ============================================================
# Rogue-specific leg rotation — RIGHT (anchor 1465, 590)
# ============================================================
transform dg_rogue_leg_right_speed0():
    subpixel True
    matrixanchor (1465, 590)

transform dg_rogue_leg_right_speed1():
    subpixel True
    matrixanchor (1465, 590)
    block:
        pause 0.35
        ease 0.20 matrixtransform RotateMatrix(0, 0, 8)
        pause 0.25
        ease 1.20 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_rogue_leg_right_speed2():
    subpixel True
    matrixanchor (1465, 590)
    block:
        pause 0.12
        ease 0.12 matrixtransform RotateMatrix(0, 0, 12)
        pause 0.10
        easein 0.45 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_rogue_leg_right_speed3():
    subpixel True
    matrixanchor (1465, 590)
    block:
        ease 0.18 matrixtransform RotateMatrix(0, 0, 14)
        easein 0.18 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# ============================================================
# Standalone Doggy images (animated layers shown by DG_ApplySpeed)
# ============================================================
image rogue doggy_boobs = "images/characters/Rogue/Doggy/Rogue Doggy Boobs 1.png"
image rogue doggy_body_safe = "images/characters/Rogue/Doggy/Rogue Doggy Body 1 safe.png"
image rogue doggy_head = "images/characters/Rogue/Doggy/Head/Rogue Doggy Head 2.png"
image rogue doggy_calves_left = "images/characters/Rogue/Doggy/Rogue Doggy Calves Left.png"
image rogue doggy_calves_right = "images/characters/Rogue/Doggy/Rogue Doggy Calves right.png"
image rogue doggy_legs_left = "images/characters/Rogue/Doggy/Rogue Doggy Legs Left.png"
image rogue doggy_legs_right = "images/characters/Rogue/Doggy/Rogue Doggy Legs right.png"
image rogue doggy_foot_left = "images/characters/Rogue/Doggy/Rogue Doggy Foot Left.png"
image rogue doggy_foot_right = "images/characters/Rogue/Doggy/Rogue Doggy Foot right.png"
image rogue doggy_penis = _p("Doggy/Doggy Guy Penis.png")

# Base layers (Ass/ subfolder — shared between vaginal and anal)
image rogue doggy_ass_clean_center = "images/characters/Rogue/Doggy/Ass/Clean Base Center.png"
image rogue doggy_ass_clean_right = "images/characters/Rogue/Doggy/Ass/Clean Base Right.png"
image rogue doggy_ass_clean_left = "images/characters/Rogue/Doggy/Ass/Clean Base Left.png"
image rogue doggy_ass_before_pussy = "images/characters/Rogue/Doggy/Ass/Before Pussy.png"
image rogue doggy_ass_before_ass = "images/characters/Rogue/Doggy/Ass/Before Ass.png"
image rogue doggy_ass_after_pussy = "images/characters/Rogue/Doggy/Ass/After Pussy.png"
image rogue doggy_ass_after_ass = "images/characters/Rogue/Doggy/Ass/After Ass.png"
image rogue doggy_ass_during_pussy = "images/characters/Rogue/Doggy/Ass/During Pussy.png"
image rogue doggy_ass_during_pussy_below = "images/characters/Rogue/Doggy/Ass/During Pussy Below.png"
image rogue doggy_ass_during_anal = "images/characters/Rogue/Doggy/Ass/During Anal Fast.png"
image rogue doggy_ass_during_anal_below = "images/characters/Rogue/Doggy/Ass/During Anal Bellow.png"
image rogue doggy_ass_safe_layer = "images/characters/Rogue/Doggy/Ass/Ass Safe Layer.png"

# ============================================================
# Cum layers (ConditionSwitch — auto-update when girl.Cum changes)
# ============================================================
image rogue doggy_butt_cum = ConditionSwitch(
    "store._doggy_girl and 'ass' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Ass.png",
    "True", Null()
)
image rogue doggy_back_cum = ConditionSwitch(
    "store._doggy_girl and 'back' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Back.png",
    "True", Null()
)
image rogue doggy_dripping_cum = ConditionSwitch(
    "store._doggy_girl and 'dripping' in getattr(store._doggy_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Dripping 2.png",
    "store._doggy_girl and 'dripping' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Dripping 1.png",
    "True", Null()
)
image rogue doggy_dripping_ass_cum = ConditionSwitch(
    "store._doggy_girl and 'dripping_ass' in getattr(store._doggy_girl, 'Cum', []) and store._session_cum.get('anal_inside', 0) >= 2",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Dripping Ass 2.png",
    "store._doggy_girl and 'dripping_ass' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Rogue/Doggy/Cum/Rogue Doggy Cum Dripping Ass 1.png",
    "True", Null()
)

# ============================================================
# Standalone clothing layers (shown by DG_ApplySpeed)
# ============================================================
# Thigh highs (all split left/right for Rogue)
image rogue doggy_thigh_highs_calves_left = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Calves Left.png"
image rogue doggy_thigh_highs_calves_right = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Calves Right.png"
image rogue doggy_thigh_highs_legs_left = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Legs Left.png"
image rogue doggy_thigh_highs_legs_right = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Legs Right.png"
image rogue doggy_thigh_highs_foot_left = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Foot Left.png"
image rogue doggy_thigh_highs_foot_right = "images/characters/Rogue/Doggy/Clothes/Rogue Doggy Thigh Highs Foot Right.png"

# Crop Top / Bikini top / Mesh Top (standalone for above body_safe)
image rogue doggy_corset = "images/characters/Rogue/Doggy/Clothes/Chest/Crop Top/Rogue Doggy Crop Top.png"
image rogue doggy_bikini_top = "images/characters/Rogue/Doggy/Clothes/Chest/Black Bikini Top/Rogue Doggy Black Bikini Top.png"
image rogue doggy_mesh_top = "images/characters/Rogue/Doggy/Clothes/Over/Mesh Top/Rogue Doggy Mesh Top.png"

# Skirt
image rogue doggy_skirt = "images/characters/Rogue/Doggy/Clothes/Legs/Black Skirt/Rogue Doggy Black Skirt.png"
image rogue doggy_skirt_up = "images/characters/Rogue/Doggy/Clothes/Legs/Black Skirt/Rogue Doggy Black Skirt Up.png"
image rogue doggy_skirt_up_safe = "images/characters/Rogue/Doggy/Clothes/Legs/Black Skirt/Rogue Doggy Black Skirt Up Safe.png"

# Panties — green (code key: purple)
image rogue doggy_panties_purple_full = "images/characters/Rogue/Doggy/Clothes/Panties/Green Panties/Rogue Doggy Green Panties Up.png"
image rogue doggy_panties_purple_down = "images/characters/Rogue/Doggy/Clothes/Panties/Green Panties/Rogue Doggy Green Panties Down.png"
image rogue doggy_panties_purple_side_right = "images/characters/Rogue/Doggy/Clothes/Panties/Green Panties/Rogue Doggy Green Panties Side Right.png"
image rogue doggy_panties_purple_side_left = "images/characters/Rogue/Doggy/Clothes/Panties/Green Panties/Rogue Doggy Green Panties Side Left.png"

# Panties — bikini (code key: bikini_panties)
image rogue doggy_panties_bikini_panties_full = "images/characters/Rogue/Doggy/Clothes/Panties/Green Bikini Bottom/Rogue Doggy Green Bikini Bottom Up.png"
image rogue doggy_panties_bikini_panties_down = "images/characters/Rogue/Doggy/Clothes/Panties/Green Bikini Bottom/Rogue Doggy Green Bikini Bottom Down.png"
image rogue doggy_panties_bikini_panties_side_right = "images/characters/Rogue/Doggy/Clothes/Panties/Green Bikini Bottom/Rogue Doggy Green Bikini Bottom Side Right.png"
image rogue doggy_panties_bikini_panties_side_left = "images/characters/Rogue/Doggy/Clothes/Panties/Green Bikini Bottom/Rogue Doggy Green Bikini Bottom Side Left.png"

# ============================================================
# Player action layers (grab / slap)
# ============================================================
image rogue doggy_grab_butt_left = _p("Doggy/Doggy Guy Hand Squeeze Left.png")
image rogue doggy_grab_butt_right = _p("Doggy/Doggy Guy Hand Squeeze Right.png")
image rogue doggy_slap_left = Transform(_p("Doggy/Doggy Guy Hand Smack Left.png"), xoffset=40)
image rogue doggy_slap_right = Transform(_p("Doggy/Doggy Guy Hand Smack Right.png"), xoffset=-40)
