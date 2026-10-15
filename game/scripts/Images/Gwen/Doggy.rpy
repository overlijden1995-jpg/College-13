# ============================================================
# Gwen Doggy Layered Sprite
# ============================================================
# Head 2 has the face baked in — no separate expression layers.

layeredimage gwen doggy:

    # --- Arm (bottommost layer) ---
    group arms:
        attribute arms_1 default:
            "images/characters/Gwen/Doggy/Gwen Doggy arm 1.png"
        attribute arms_none:
            Null()

    # --- Body ---
    group body:
        attribute body_base default:
            "images/characters/Gwen/Doggy/Gwen Doggy Body 1.png"

    # --- Body Safe removed from layeredimage — now standalone for penis masking ---

    # --- Calves & Legs removed from layeredimage — now standalone animated layers ---

    # --- Butt Gap (removed — standalone layers handle display during scenes) ---
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
            "images/characters/Gwen/Doggy/Ass/Clean Base Center.png"

    # --- Chest clothing (below over) ---
    group torso_chest:
        attribute torso_chest_none default:
            Null()
        attribute torso_chest_corset:
            "images/characters/Gwen/Doggy/Clothes/Chest/Corset/Gwen Doggy Corset.png"
        attribute torso_chest_bikini_top:
            "images/characters/Gwen/Doggy/Clothes/Chest/Black Bikini Top/Gwen Doggy Black Bikini Top.png"

    # --- Mid (placeholder) ---
    group mid:
        attribute mid_none default:
            Null()

    # --- Over clothing (above chest) ---
    group torso_over:
        attribute torso_over_none default:
            Null()
        attribute torso_over_long_shirt:
            "images/characters/Gwen/Doggy/Clothes/Over/Long Shirt/Gwen Doggy Long Shirt.png"

    # --- Collar (above body/clothes, below head) ---
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Gwen/Doggy/Clothes/Gwen Doggy Collar.png"

    # --- Head ---
    group head:
        attribute head_base default:
            "images/characters/Gwen/Doggy/Head/Gwen Doggy Head 2.png"

    # --- Mouth / Eyes / Brows / Blush hidden while Head 2 is active ---
    # (Head 2 has the face baked in — no separate expression layers)

# ============================================================
# Standalone Doggy images (animated layers shown by ApplySpeed)
# ============================================================
image gwen doggy_boobs = "images/characters/Gwen/Doggy/Gwen Doggy Boobs.png"
image gwen doggy_body_safe = "images/characters/Gwen/Doggy/Gwen Doggy Body 1 safe.png"

image gwen doggy_calves_left = "images/characters/Gwen/Doggy/Gwen Doggy Calves Left .png"
image gwen doggy_calves_right = "images/characters/Gwen/Doggy/Gwen Doggy Calves Right .png"
image gwen doggy_legs_left = "images/characters/Gwen/Doggy/Gwen Doggy Legs Left .png"
image gwen doggy_legs_right = "images/characters/Gwen/Doggy/Gwen Doggy Legs Right .png"

image gwen doggy_foot_left = "images/characters/Gwen/Doggy/Gwen Doggy Foot Left .png"
image gwen doggy_foot_right = "images/characters/Gwen/Doggy/Gwen Doggy Foot Right .png"
image gwen doggy_penis = _p("Doggy/Doggy Guy Penis.png")

# Base layers (Ass/ subfolder — shared between vaginal and anal)
image gwen doggy_ass_clean_center = "images/characters/Gwen/Doggy/Ass/Clean Base Center.png"
image gwen doggy_ass_clean_right = "images/characters/Gwen/Doggy/Ass/Clean Base Right.png"
image gwen doggy_ass_clean_left = "images/characters/Gwen/Doggy/Ass/Clean Base Left.png"
image gwen doggy_ass_before_pussy = "images/characters/Gwen/Doggy/Ass/Before Pussy.png"
image gwen doggy_ass_before_ass = "images/characters/Gwen/Doggy/Ass/Before Ass.png"
image gwen doggy_ass_after_pussy = "images/characters/Gwen/Doggy/Ass/After Pussy.png"
image gwen doggy_ass_after_ass = "images/characters/Gwen/Doggy/Ass/After Ass.png"
image gwen doggy_ass_during_pussy = "images/characters/Gwen/Doggy/Ass/During Pussy.png"
image gwen doggy_ass_during_pussy_below = "images/characters/Gwen/Doggy/Ass/During Pussy Below.png"
image gwen doggy_ass_during_anal = "images/characters/Gwen/Doggy/Ass/During Anal Fast.png"
image gwen doggy_ass_during_anal_below = "images/characters/Gwen/Doggy/Ass/During Anal Bellow.png"
image gwen doggy_ass_safe_layer = "images/characters/Gwen/Doggy/Ass/Ass Safe Layer.png"

# ============================================================
# Cum layers (ConditionSwitch — auto-update when girl.Cum changes)
# ============================================================
image gwen doggy_butt_cum = ConditionSwitch(
    "store._doggy_girl and 'ass' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Ass.png",
    "True", Null()
)
image gwen doggy_back_cum = ConditionSwitch(
    "store._doggy_girl and 'back' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Back.png",
    "True", Null()
)
image gwen doggy_dripping_cum = ConditionSwitch(
    "store._doggy_girl and 'dripping' in getattr(store._doggy_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Dripping 2.png",
    "store._doggy_girl and 'dripping' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Dripping 1.png",
    "True", Null()
)
image gwen doggy_dripping_ass_cum = ConditionSwitch(
    "store._doggy_girl and 'dripping_ass' in getattr(store._doggy_girl, 'Cum', []) and store._session_cum.get('anal_inside', 0) >= 2",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Dripping Ass 2.png",
    "store._doggy_girl and 'dripping_ass' in getattr(store._doggy_girl, 'Cum', [])",
    "images/characters/Gwen/Doggy/Cum/Gwen Doggy Cum Dripping Ass 1.png",
    "True", Null()
)

# (old transition bases removed — now using split Ass/ layers)

# ============================================================
# Standalone clothing layers (shown by DG_ApplySpeed)
# ============================================================
# Thigh highs (two parts: calves + legs)
image gwen doggy_thigh_highs_calves = "images/characters/Gwen/Doggy/Clothes/Gwen Doggy Thigh Highs Calves.png"
image gwen doggy_thigh_highs_legs_left = "images/characters/Gwen/Doggy/Clothes/Gwen Doggy Thigh Highs Legs Left.png"
image gwen doggy_thigh_highs_legs_right = "images/characters/Gwen/Doggy/Clothes/Gwen Doggy Thigh Highs Legs Right.png"
image gwen doggy_thigh_highs_foot = "images/characters/Gwen/Doggy/Clothes/Gwen Doggy Thigh Highs Foot.png"

# Long shirt (body + arms as separate standalones)
image gwen doggy_shirt_body = "images/characters/Gwen/Doggy/Clothes/Over/Long Shirt/Gwen Doggy Long Shirt.png"
image gwen doggy_shirt_arms = "images/characters/Gwen/Doggy/Clothes/Over/Long Shirt/Gwen Doggy Long Shirt Arm.png"

# Corset / Bikini top (standalone for above body_safe)
image gwen doggy_corset = "images/characters/Gwen/Doggy/Clothes/Chest/Corset/Gwen Doggy Corset.png"
image gwen doggy_bikini_top = "images/characters/Gwen/Doggy/Clothes/Chest/Black Bikini Top/Gwen Doggy Black Bikini Top.png"

# Skirt
image gwen doggy_skirt = "images/characters/Gwen/Doggy/Clothes/Legs/Blue Skirt/Gwen Doggy Blue Skirt.png"
image gwen doggy_skirt_up = "images/characters/Gwen/Doggy/Clothes/Legs/Blue Skirt/Gwen Doggy Blue Skirt Up.png"
image gwen doggy_skirt_up_safe = "images/characters/Gwen/Doggy/Clothes/Legs/Blue Skirt/Gwen Doggy Blue Skirt Up Safe.png"

# Panties — purple
image gwen doggy_panties_purple_full = "images/characters/Gwen/Doggy/Clothes/Panties/Purple Panties/Gwen Doggy Purple Panties Up.png"
image gwen doggy_panties_purple_down = "images/characters/Gwen/Doggy/Clothes/Panties/Purple Panties/Gwen Doggy Purple Panties Down.png"
image gwen doggy_panties_purple_side_right = "images/characters/Gwen/Doggy/Clothes/Panties/Purple Panties/Gwen Doggy Purple Panties Side Right.png"
image gwen doggy_panties_purple_side_left = "images/characters/Gwen/Doggy/Clothes/Panties/Purple Panties/Gwen Doggy Purple Panties Side Left.png"

# ============================================================
# Player action layers (grab / slap)
# ============================================================
image gwen doggy_grab_butt_left = _p("Doggy/Doggy Guy Hand Squeeze Left.png")
image gwen doggy_grab_butt_right = _p("Doggy/Doggy Guy Hand Squeeze Right.png")
image gwen doggy_slap_left = _p("Doggy/Doggy Guy Hand Smack Left.png")
image gwen doggy_slap_right = _p("Doggy/Doggy Guy Hand Smack Right.png")

# Panties — bikini
image gwen doggy_panties_bikini_panties_full = "images/characters/Gwen/Doggy/Clothes/Panties/Black Bikini Bottom/Gwen Doggy Black Bikini Bottom Up.png"
image gwen doggy_panties_bikini_panties_down = "images/characters/Gwen/Doggy/Clothes/Panties/Black Bikini Bottom/Gwen Doggy Black Bikini Bottom Down.png"
image gwen doggy_panties_bikini_panties_side_right = "images/characters/Gwen/Doggy/Clothes/Panties/Black Bikini Bottom/Gwen Doggy Black Bikini Bottom Side Right.png"
image gwen doggy_panties_bikini_panties_side_left = "images/characters/Gwen/Doggy/Clothes/Panties/Black Bikini Bottom/Gwen Doggy Black Bikini Bottom Side Left.png"
