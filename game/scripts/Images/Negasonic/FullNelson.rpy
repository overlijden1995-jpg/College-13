# ============================================================
# Negasonic (NTW) Full Nelson Layered Sprite
# ============================================================
# Exclusive position for NTW. Front-facing, held up by the player.
# Layer order follows "Ordem dos Layers.txt" reference.
#
# Layeredimage contains: Torso, Chest, Nipples, Clothes, Head, Expressions
# Standalones: Girl arms, Ass, Legs, Guy arms, Pelvis/Anal layers, Penis

layeredimage ntw fn:

    # --- Torso (base body) ---
    group torso:
        attribute torso_base default:
            preg_art("ntw", "Full Nelson/Torso.png")

    # --- Chest + Nipples: rendered as standalone with bounce transforms ---
    # See fn_chest_over / fn_nipples_over (shown by FN_ApplySpeed)

    # --- Clothes: Yellow Bottom (below belly) ---
    group yellow_bottom:
        attribute yellow_bottom_none default:
            Null()
        attribute yellow_bottom_on:
            "images/characters/Negasonic/Full Nelson/Clothes/Yellow Bottom.png"

    # --- Clothes: Bikini Bottom (below belly) ---
    group bikini_bottom:
        attribute bikini_bottom_none default:
            Null()
        attribute bikini_bottom_on:
            "images/characters/Negasonic/Full Nelson/Clothes/Bikini/Bikini Bottom.png"

    # --- Full belly (visual pregnancy stage 2): above bottoms, below tops ---
    # fn_during_pussy_fast carries it too (see that image).
    always:
        preg_belly("ntw", "+Full Nelson/belly")

    # --- Clothes: Yellow Top (above belly) ---
    group yellow_top:
        attribute yellow_top_none default:
            Null()
        attribute yellow_top_up:
            preg_art("ntw", "Full Nelson/Clothes/Yellow Top Up.png")
        attribute yellow_top_down:
            preg_art("ntw", "Full Nelson/Clothes/Yellow Top Down.png")

    # --- Clothes: Bikini Top (above belly) ---
    group bikini_top:
        attribute bikini_top_none default:
            Null()
        attribute bikini_top_up:
            preg_art("ntw", "Full Nelson/Clothes/Bikini/Bikini Top Up.png")
        attribute bikini_top_down:
            preg_art("ntw", "Full Nelson/Clothes/Bikini/Bikini Top Down.png")

    # --- Head + Expressions: rendered as standalone with rotation transform ---
    # See fn_head_over layeredimage (shown by FN_ApplySpeed)


# ============================================================
# Head + Expressions (standalone layeredimage with rotation)
# ============================================================
layeredimage ntw fn_head_over:

    # --- Head ---
    always:
        "images/characters/Negasonic/Full Nelson/Head/Head.png"

    # --- Blush ---
    always:
        ConditionSwitch(
            "_gs('fn', 'blush', 0) >= 2",
            "images/characters/Negasonic/Full Nelson/Head/Blush 2.png",
            "_gs('fn', 'blush', 0) >= 1",
            "images/characters/Negasonic/Full Nelson/Head/Blush 1.png",
            "True", Null()
        )

    # --- Mouth ---
    always:
        ConditionSwitch(
            "_gs('fn', 'mouth') == 'mouth_tongue'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Tongue.png",
            "_gs('fn', 'mouth') == 'mouth_lipbite'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Lipbite.png",
            "_gs('fn', 'mouth') == 'mouth_kiss'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Kiss.png",
            "_gs('fn', 'mouth') == 'mouth_scared'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Scared.png",
            "_gs('fn', 'mouth') == 'mouth_angry'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Angry.png",
            "_gs('fn', 'mouth') == 'mouth_sad'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Sad.png",
            "_gs('fn', 'mouth') == 'mouth_laugh'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Laugh.png",
            "_gs('fn', 'mouth') == 'mouth_screaming'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Screaming.png",
            "_gs('fn', 'mouth') in ('mouth_moaning_2', 'mouth_surprised', 'mouth_open_teeth', 'mouth_sch')",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Moaning 2.png",
            "_gs('fn', 'mouth') == 'mouth_moaning_3'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Moaning 3.png",
            "_gs('fn', 'mouth') == 'mouth_smile'",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Smile.png",
            "_gs('fn', 'mouth') in ('mouth_moaning', 'mouth_serious')",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Moaning.png",
            "True",
            "images/characters/Negasonic/Full Nelson/Expression/Mouth/Normal.png",
        )

    # --- Eyes ---
    always:
        ConditionSwitch(
            "getattr(store, 'fn_blink', False)",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Closed.png",
            "_gs('fn', 'eyes') == 'eyes_ahegao'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Ahegao.png",
            "_gs('fn', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Ahegao 2.png",
            "_gs('fn', 'eyes') == 'eyes_bliss'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Bliss.png",
            "_gs('fn', 'eyes') == 'eyes_sexy'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Sexy.png",
            "_gs('fn', 'eyes') == 'eyes_squint'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Squint.png",
            "_gs('fn', 'eyes') == 'eyes_surprised'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Surprised.png",
            "_gs('fn', 'eyes') == 'eyes_up'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Up.png",
            "_gs('fn', 'eyes') == 'eyes_away'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Away.png",
            "_gs('fn', 'eyes') == 'eyes_side'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Looking Left.png",
            "_gs('fn', 'eyes') == 'eyes_side_2'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Looking Right.png",
            "_gs('fn', 'eyes') == 'eyes_closed_happy'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Closed Happy.png",
            "_gs('fn', 'eyes') == 'eyes_closed_left'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Closed Left.png",
            "_gs('fn', 'eyes') == 'eyes_closed_right'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Closed Right.png",
            "_gs('fn', 'eyes') == 'eyes_up_closed_left'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Up Closed Left.png",
            "_gs('fn', 'eyes') == 'eyes_up_closed_right'",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Up Closed Right.png",
            "_gs('fn', 'eyes') in ('eyes_closed', 'eyes_squint_big', 'eyes_left_closed', 'eyes_right_closed')",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Closed.png",
            "True",
            "images/characters/Negasonic/Full Nelson/Expression/Eyes/Normal.png",
        )

    # --- Brows ---
    always:
        ConditionSwitch(
            "_gs('fn', 'brows') == 'brows_angry'",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Angry.png",
            "_gs('fn', 'brows') == 'brows_sad'",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Sad.png",
            "_gs('fn', 'brows') == 'brows_scared'",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Scared.png",
            "_gs('fn', 'brows') in ('brows_surprised', 'brows_confused')",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Perplexed.png",
            "_gs('fn', 'brows') == 'brows_perplexed_2'",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Perplexed 2.png",
            "_gs('fn', 'brows') == 'brows_horny'",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Perplexed 2.png",
            "True",
            "images/characters/Negasonic/Full Nelson/Expression/Brows/Normal.png",
        )


# ============================================================
# Standalone Full Nelson images
# ============================================================

# --- Chest Bounce (standalone above layeredimage) ---
image ntw fn_chest_over = preg_art("ntw", "Full Nelson/Chest.png")

# --- Nipples Bounce (standalone above chest) ---
image ntw fn_nipples_over = ConditionSwitch(
    "store._fn_girl and getattr(store._fn_girl, 'Piercing', False)",
    preg_art("ntw", "Full Nelson/Nipples Piercing.png"),
    "True",
    preg_art("ntw", "Full Nelson/Nipples.png"),
)

# --- Girl Arms (Layer 12 — bottom) ---
image ntw fn_arm_left = "images/characters/Negasonic/Full Nelson/Arm Left 1.png"
image ntw fn_arm_right = "images/characters/Negasonic/Full Nelson/Arm Right 1.png"

# --- Ass Base Safe (Layer 11) ---
image ntw fn_ass_safe = "images/characters/Negasonic/Full Nelson/Ass Base Safe.png"

# --- Legs (Layer 10) ---
image ntw fn_shin_left = "images/characters/Negasonic/Full Nelson/Shin Left.png"
image ntw fn_shin_right = "images/characters/Negasonic/Full Nelson/Shin Right.png"
image ntw fn_thigh_left = "images/characters/Negasonic/Full Nelson/Thigh Left.png"
image ntw fn_thigh_right = "images/characters/Negasonic/Full Nelson/Thigh Right.png"

# --- Guy Arms (Layer 10 — above legs) ---
image ntw fn_guy_arm_left = _p("Full Nelson/FN Guy Arm Left.png")
image ntw fn_guy_arm_right = _p("Full Nelson/FN Guy Arm Right.png")

# --- Pelvis Base Safe (Layer 8) ---
image ntw fn_pelvis_safe = "images/characters/Negasonic/Full Nelson/Pelvis Base Safe.png"

# --- Before Pussy (Layer 8 — clean state, no penetration) ---
image ntw fn_before_pussy = "images/characters/Negasonic/Full Nelson/Before Pussy.png"

# --- During Pussy Below (Layer 8 — below penis during sex) ---
image ntw fn_during_pussy_below = "images/characters/Negasonic/Full Nelson/During Pussy Below.png"

# --- During Pussy Fast (Layer 8 — above penis at fast speed) ---
# This layer redraws the lower torso ABOVE the layeredimage, so at fast speed it would cover the full
# belly: the part of the belly it hides rides on it (cropped at its top edge, so the tops that hang over
# the belly inside the layeredimage stay in front).
image ntw fn_during_pussy_fast = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Negasonic/Full Nelson/During Pussy Fast.png",
    (0, 527), preg_belly("ntw", "+Full Nelson/belly", window_top=527),
)

# --- Pussy Penis (Player) ---
image ntw fn_pussy_penis = _p("Full Nelson/FN Pussy Penis.png")

# --- Scrotum (Player — subtle zoom animation) ---
image ntw fn_scrotum = _p("Full Nelson/FN Scrotum.png")

# --- Before Ass (Layer 9 — clean state, no anal penetration) ---
image ntw fn_before_ass = "images/characters/Negasonic/Full Nelson/Before Ass.png"

# --- During Anal Below (Layer 9 — below penis during anal) ---
image ntw fn_during_anal_below = "images/characters/Negasonic/Full Nelson/During Anal Below.png"

# --- During Anal Fast (Layer 9 — above penis at fast anal speed) ---
image ntw fn_during_anal_fast = "images/characters/Negasonic/Full Nelson/During Anal Fast.png"

# --- FN Legs (Player — below all other layers, moves with penis) ---
image ntw fn_legs = _p("Full Nelson/FN Legs.png")

# --- Cum Layers ---
image ntw fn_cum_penis = "images/characters/Negasonic/Full Nelson/Cum/Cum Penis.png"
image ntw fn_cum_inside_pussy_2 = "images/characters/Negasonic/Full Nelson/Cum/Cum Inside Pussy 2.png"
image ntw fn_cum_ass_inside = "images/characters/Negasonic/Full Nelson/Cum/Cum Ass Inside.png"
image ntw fn_cum_boobs = preg_art("ntw", "Full Nelson/Cum/Cum Boobs.png")
image ntw fn_cum_ass = "images/characters/Negasonic/Full Nelson/Cum/Cum Ass.png"
image ntw fn_cum_face = "images/characters/Negasonic/Full Nelson/Cum/Negasonic Cum Face FN.png"
