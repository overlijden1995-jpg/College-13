layeredimage tenny blowjob:

    # --------------------------------------------------------
    # Layer order (bottom -> top):
    # Legs L/R -> Legs clothes -> Panties -> Pelvis -> Arms L/R
    # -> Torso -> Chest -> Chest clothes -> Over -> Mid -> Cum
    # --------------------------------------------------------

    # LEGS
    always:
        "images/characters/Tenny/BJ_HJ/Legs Left.png"
    always:
        "images/characters/Tenny/BJ_HJ/Legs Right.png"

    group legs_clothes:
        attribute legs_none default:
            Null()
        attribute legs_white_pants:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/Legs Left White Pants.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/Legs Right White Pants.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Legs/White Pants Pelvis.png",
            )

    group shoes:
        attribute shoes_none default:
            Null()

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_bikini:
            "images/characters/Tenny/BJ_HJ/Clothes/Panties/Bikini Bottom/Blue Bikini Bottom.png"
        attribute panties_striped:
            "images/characters/Tenny/BJ_HJ/Clothes/Panties/Striped Panties/Tenny Striped Panties.png"

    # PELVIS
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Pelvis.png"

    # BODY ARMS (below torso) — hidden in torso_type 4 (arms behind back)
    group body_arm_left:
        attribute arm_left_show default:
            ConditionSwitch(
                "bj_torso_type == 4", Null(),
                "True", "images/characters/Tenny/BJ_HJ/Tenny Left.png"
            )
    group body_arm_right:
        attribute arm_right_show default:
            ConditionSwitch(
                "bj_torso_type == 4", Null(),
                "True", "images/characters/Tenny/BJ_HJ/Tenny Right.png"
            )

    # TORSO (above arms, below chest)
    always:
        "images/characters/Tenny/BJ_HJ/Tenny Torso.png"

    # BELLY (visual pregnancy stage 1 on, one size in this pose): right above the torso, below the chest
    always:
        preg_art("tenny", "+BJ_HJ/belly")

    # --------------------------------------------------------
    # CHEST (nude / piercing / clothed base)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("tenny", "BJ_HJ/Tenny Chest.png")
        attribute chest_piercing:
            preg_art("tenny", "BJ_HJ/Tenny Chest Piercing.png")
        attribute chest_hidden:
            "images/characters/Tenny/BJ_HJ/Tenny Chest Clothed.png"

    # CHEST CLOTHING
    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_bikini_top:
            preg_art("tenny", "BJ_HJ/Clothes/Chest/Bikini Top/Blue Bikini Top.png")
        attribute boobs_bikini_top_up:
            "images/characters/Tenny/BJ_HJ/Clothes/Chest/Bikini Top/Blue Bikini Top Up.png"
        attribute boobs_white_top:
            preg_art("tenny", "BJ_HJ/Clothes/Chest/Top/White Top.png")
        attribute boobs_white_top_up:
            "images/characters/Tenny/BJ_HJ/Clothes/Chest/Top/White Top Up.png"

    # MID CLOTHING (below over)
    group mid_clothing:
        attribute mid_none default:
            Null()
        attribute over_blue_shirt:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt Arm Left.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt Arm Right.png",
                (0, 0), preg_art("tenny", "BJ_HJ/Clothes/Mid/Blue Shirt/Blue Shirt.png"),
            )

    # OVER CLOTHING (above mid)
    group over:
        attribute over_none default:
            Null()
        attribute over_blue_jacket:
            Composite(
                (1920, 1080),
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket Arm Left.png",
                (0, 0), "images/characters/Tenny/BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket Arm Right.png",
                (0, 0), preg_art("tenny", "BJ_HJ/Clothes/Over/Blue Jacket/Blue Jacket.png"),
            )

    # --------------------------------------------------------
    # CUM BODY
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_auto default:
            ConditionSwitch(
                "store._bj_girl and 'boobs' in getattr(store._bj_girl, 'Cum', [])",
                "images/characters/Tenny/BJ_HJ/Cum/Cum Tits.png",
                "True", Null()
            )

    group cum_extra:
        attribute cum_extra_auto default:
            ConditionSwitch(
                "store._bj_girl and len(getattr(store._bj_girl, 'Cum', [])) > 0",
                "images/characters/Tenny/BJ_HJ/Cum/Cum Extra.png",
                "True", Null()
            )

    group penis_mid:
        attribute penis_mid default:
            Null()

# ============================================================
# HEAD (separate layeredimage - moves independently for bobbing)
# ============================================================
layeredimage tenny blowjob_head:

    # HEAD
    group head:
        attribute head_base default:
            "images/characters/Tenny/BJ_HJ/Head/Tenny Blow Job Head.png"
        attribute head_2:
            "images/characters/Tenny/BJ_HJ/Head/Tenny Blow Job Head 2.png"
        attribute head_deepthroat:
            "images/characters/Tenny/BJ_HJ/Head/Head Deepthroat.png"
        attribute head_deepthroat_full_bottom:
            "images/characters/Tenny/BJ_HJ/Head/Head Deepthroat Full Bottom.png"
        attribute head_normal:
            "images/characters/Tenny/BJ_HJ/Head/Tenny Head.png"

    # --------------------------------------------------------
    # BLUSH
    # --------------------------------------------------------
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('bj', 'blush', 0) == 2",
                "images/characters/Tenny/BJ_HJ/Head/BJ Head Blush 2.png",
                "_gs('bj', 'blush', 0) == 1",
                "images/characters/Tenny/BJ_HJ/Head/BJ Head Blush.png",
                "True", Null()
            )

    # MOUTH
    group mouth:
        attribute mouth_none:
            Null()
        attribute mouth_tongue:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Tongue.png"
        attribute mouth_sucking default:
            Null()
        attribute mouth_smile:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Smile.png"
        attribute mouth_happy:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Happy.png"
        attribute mouth_lipbite:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Lipbite.png"
        attribute mouth_sad:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Surprised.png"
        attribute mouth_angry:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Angry.png"
        attribute mouth_screaming:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Screaming.png"
        attribute mouth_scared:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Scared.png"
        attribute mouth_kiss:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Kiss.png"
        attribute mouth_normal:
            "images/characters/Tenny/BJ_HJ/Expression/Mouth/Normal.png"

    # EYES
    group eyes:
        attribute eyes_auto default:
            ConditionSwitch(
                "store.hiding_face or bj_blink", "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed.png",
                "bj_eyes == 'squint_2'",         "images/characters/Tenny/BJ_HJ/Expression/Eyes/Squint 2.png",
                "bj_eyes == 'squint'",           "images/characters/Tenny/BJ_HJ/Expression/Eyes/Squint.png",
                "bj_eyes == 'left_closed'",      "images/characters/Tenny/BJ_HJ/Expression/Eyes/Left Closed.png",
                "bj_eyes == 'right_closed'",     "images/characters/Tenny/BJ_HJ/Expression/Eyes/Right Closed.png",
                "bj_eyes == 'looking_left'",     "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Left.png",
                "bj_eyes == 'looking_right'",    "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Right.png",
                "bj_eyes == 'looking_down'",     "images/characters/Tenny/BJ_HJ/Expression/Eyes/Looking Down.png",
                "bj_eyes == 'ahegao'",           "images/characters/Tenny/BJ_HJ/Expression/Eyes/Ahegao.png",
                "bj_eyes == 'ahegao_2'",         "images/characters/Tenny/BJ_HJ/Expression/Eyes/Ahegao 2.png",
                "bj_eyes == 'closed_happy'",     "images/characters/Tenny/BJ_HJ/Expression/Eyes/Closed Happy.png",
                "bj_eyes == 'up_left_closed'",   "images/characters/Tenny/BJ_HJ/Expression/Eyes/Up Left Closed.png",
                "bj_eyes == 'up_right_closed'",  "images/characters/Tenny/BJ_HJ/Expression/Eyes/Up Right Closed.png",
                "bj_eyes == 'surprised'",        "images/characters/Tenny/BJ_HJ/Expression/Eyes/Surprised.png",
                "True",                          "images/characters/Tenny/BJ_HJ/Expression/Eyes/Normal.png"
            )

    # BROWS
    group brows:
        attribute brows_auto default:
            ConditionSwitch(
                "bj_brows == 2", "images/characters/Tenny/BJ_HJ/Expression/Brows/Sad.png",
                "bj_brows == 3", "images/characters/Tenny/BJ_HJ/Expression/Brows/Perplexed.png",
                "bj_brows == 4", "images/characters/Tenny/BJ_HJ/Expression/Brows/Perplexed 2.png",
                "bj_brows == 5", "images/characters/Tenny/BJ_HJ/Expression/Brows/Angry.png",
                "bj_brows == 6", "images/characters/Tenny/BJ_HJ/Expression/Brows/Worried.png",
                "bj_brows == 7", "images/characters/Tenny/BJ_HJ/Expression/Brows/Determined.png",
                "True",          "images/characters/Tenny/BJ_HJ/Expression/Brows/Normal.png"
            )

# ============================================================
# JAW (separate - follows head_transform)
# ============================================================
layeredimage tenny blowjob_jaw:

    group jaw:
        attribute jaw_auto default:
            "images/characters/Tenny/BJ_HJ/Jaw.png"
        attribute jaw_1:
            "images/characters/Tenny/BJ_HJ/Jaw.png"
        attribute jaw_2:
            "images/characters/Tenny/BJ_HJ/Jaw Sucking.png"

# ============================================================
# TRANSFORMS (Tenny-specific overrides)
# ============================================================

# --- Force descent (deeper than default 300/190) ---
transform tenny_bj_head_force_descent:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    ease 0.7 yoffset 480

transform tenny_bj_slot_force_descent:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 110
    ease 0.7 yoffset 280

# --- Force speed (minimal bob at descent depth) ---
transform tenny_bj_head_force_speed1:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 480
    block:
        ease 0.65 yoffset 490
        ease 0.95 yoffset 480
        repeat

transform tenny_bj_head_force_speed2:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 483
    block:
        ease 0.48 yoffset 493
        ease 0.75 yoffset 483
        repeat

transform tenny_bj_head_force_speed3:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 485
    block:
        ease 0.36 yoffset 495
        ease 0.60 yoffset 485
        repeat

transform tenny_bj_slot_force_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 280
    block:
        ease 0.65 yoffset 286
        ease 0.95 yoffset 280
        repeat

transform tenny_bj_slot_force_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 282
    block:
        ease 0.48 yoffset 288
        ease 0.75 yoffset 282
        repeat

transform tenny_bj_slot_force_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 284
    block:
        ease 0.36 yoffset 290
        ease 0.60 yoffset 284
        repeat

# --- Force rise (release head — back to normal position) ---
transform tenny_bj_head_force_rise:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 480
    ease 0.8 yoffset 135

transform tenny_bj_slot_force_rise:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 280
    ease 0.8 yoffset 110

# --- Penis position ---
transform tenny_bj_penis_corner():
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform tenny_bj_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    zoom 1.0
    pause 0.45
    ease 0.08 zoom 1.008
    ease 0.15 zoom 1.0
    pause 0.27
    ease 0.08 zoom 1.008
    ease 0.15 zoom 1.0

# ============================================================
# STANDALONE IMAGES
# ============================================================

# Penis (HJ BJ art, skin-aware)
image tenny bj_penis = ConditionSwitch(
    "getattr(store, '_bj_use_half_penis', False) and getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/Half Penis.png",
    "getattr(store, '_bj_use_half_penis', False)",
    "images/characters/Player/White/HJ BJ/Half Penis.png",
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/BJ Penis Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Penis.png",
)

# Girl's arms (torso_type 2 - below penis)
image tenny bj_arm       = "images/characters/Tenny/BJ_HJ/Blow Job Arm Left.png"
image tenny bj_right_arm = "images/characters/Tenny/BJ_HJ/Blow Job Arm Right.png"

# Girl's arms behind back (torso_type 3)
image tenny bj_back_arm_left  = "images/characters/Tenny/BJ_HJ/Back Arm Left.png"
image tenny bj_back_arm_right = "images/characters/Tenny/BJ_HJ/Back Arm Right.png"

# Girl's hands (above penis - shared HJ hand art)
image tenny bj_hand = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Tenny/BJ_HJ/Hand Job Hand Left.png",
    (0, 0), "images/characters/Tenny/BJ_HJ/Hand Job Hand Right.png",
)

# Forcing hands (player pushes her head)
image tenny bj_forcing_hands_left = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/Guy Hand Left Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Guy Hand Left.png",
)
image tenny bj_forcing_hands_right = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/Guy Hand Right Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Guy Hand Right.png",
)

# Slap (standard player BJ slap, skin-aware)
image tenny bj_slap_right = _p("BJ/BJ Guy Hand Smack Right.png")
image tenny bj_slap_left  = _p("BJ/BJ Guy Hand Smack Left.png")

# Hide face hands
image tenny bj_hide_hand_left  = "images/characters/Tenny/BJ_HJ/Hide Hand Left.png"
image tenny bj_hide_hand_right = "images/characters/Tenny/BJ_HJ/Hide Hand Right.png"

# Cum face (above penis, zorder 10025)
image tenny bj_cum_face = ConditionSwitch(
    "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Tenny/BJ_HJ/Cum/Cum Face.png",
    "True", Null()
)

# Cum mouth (below penis, zorder 9988) — random variant per session
image tenny bj_cum_mouth = ConditionSwitch(
    "store._bj_girl and 'mouth' in getattr(store._bj_girl, 'Cum', [])",
    renpy.random.choice([
        "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth.png",
        "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth 2.png",
        "images/characters/Tenny/BJ_HJ/Cum/Cum Mouth 3.png",
    ]),
    "True", Null()
)

# Cum deepthroat
image tenny bj_cum_deepthroat = "images/characters/Tenny/BJ_HJ/Cum/Cum Deepthroat.png"

# Guy body (POV, behind everything — skin-aware)
image tenny bj_guy = ConditionSwitch(
    "getattr(Player, 'skin', 'White') == 'Black'",
    "images/characters/Player/Black/HJ BJ/Guy Body Black.png",
    "True",
    "images/characters/Player/White/HJ BJ/Guy Body.png",
)

# ============================================================
# TENNY BJ HELPER FUNCTIONS
# ============================================================
init python:

    def _tenny_bj_force_rise_anim(girl, show_cum=True):
        _gid = girl.gid
        _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        store._bj_use_half_penis = False
        store.bj_idle_mouth = "mouth_tongue"
        store.bj_action = "lick"
        store.bj_speed = 0
        _head_rise = getattr(renpy.store, "%s_bj_head_force_rise" % _gid, bj_head_force_rise)
        _slot_rise = getattr(renpy.store, "%s_bj_slot_force_rise" % _gid, bj_slot_force_rise)
        _rise_penis_z = 10055 if _is_pov else 9990
        renpy.show("%s bj_penis" % _gid, tag="bj_penis", at_list=[_bj_get_penis_tf(girl)], zorder=_rise_penis_z)
        renpy.show("%s blowjob_head head_base" % _gid, tag="%s_bj_head" % _gid, at_list=[_head_rise], zorder=10058 if _is_pov else 10015)
        renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head_rise], zorder=9984)
        _attrs = _build_attributes_for_girl(girl, pose="blowjob")
        _body_img = "%s blowjob" % _gid
        if _attrs:
            _body_img += " " + " ".join(_attrs)
        renpy.show(_body_img, tag=_gid, at_list=[_slot_rise], zorder=9980)
        renpy.hide("%s_bj_right_arm" % _gid)
        renpy.hide("%s_bj_arm" % _gid)
        renpy.hide("%s_bj_hand" % _gid)
        for _side in ("left", "right"):
            _ba = "%s bj_back_arm_%s" % (_gid, _side)
            if renpy.has_image(_ba):
                renpy.show(_ba, tag="%s_bj_back_arm_%s" % (_gid, _side), at_list=[_slot_rise], zorder=9970)
        if show_cum:
            _cum_face_z = 10059 if _is_pov else 10025
            for _suffix, _z in [("bj_cum_face", _cum_face_z), ("bj_cum_face_under", 9986), ("bj_cum_mouth", 9988)]:
                _img = "%s %s" % (_gid, _suffix)
                if renpy.has_image(_img):
                    renpy.show(_img, tag="%s_%s" % (_gid, _suffix), at_list=[_head_rise], zorder=_z)
        print("[TENNY_RISE] pov=%s cum=%s" % (_is_pov, show_cum))

    def _tenny_bj_post_apply_correct(girl, speed=0, mouth="mouth_sad"):
        _gid = girl.gid
        _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        _ht = bj_get_head_transform(speed)
        _st = bj_get_slot_transform(speed)
        _head = "%s blowjob_head head_base" % _gid
        if mouth:
            _head += " " + mouth
        renpy.show(_head, tag="%s_bj_head" % _gid, at_list=[_ht], zorder=10058 if _is_pov else 10015)
        renpy.hide("%s_bj_right_arm" % _gid)
        renpy.hide("%s_bj_arm" % _gid)
        renpy.hide("%s_bj_hand" % _gid)
        for _side in ("left", "right"):
            _ba = "%s bj_back_arm_%s" % (_gid, _side)
            if renpy.has_image(_ba):
                renpy.show(_ba, tag="%s_bj_back_arm_%s" % (_gid, _side), at_list=[_st], zorder=9970)
        print("[TENNY_POST_RISE] %s speed=%d" % (_head, speed))
