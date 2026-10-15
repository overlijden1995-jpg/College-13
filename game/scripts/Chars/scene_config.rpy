# scene_config.rpy — Centralized per-girl scene overrides
#
# Instead of hardcoding `if girl.gid == "rogue"` in every Core file,
# add overrides here. Core files call _gsc() to look them up at runtime.

init -996 python:

    GIRL_SCENE_CONFIG = {

        # ── Gwen ──────────────────────────────────────────────
        "gwen": {
            "blowjob": {
                "has_torso_type2": True,
                "has_sucking_mouth": True,
                "has_looking_right": True,
            },
            "cowgirl": {
                "mast_corset_z": 9995,
                "mast_boobs_clothed_z": 9989,
                "mast_nipples_clothed_z": 9990,
                "mast_boobs_z": 9989,
                "mast_nipples_z": 9990,
                "mast_chest_z": 9991,
                "mast_arm_separate": True,
                "has_shoulders": True,
            },
            "doggy": {
                "uses_conditionswitch": True,
            },
            "rcg": {
                "uses_conditionswitch": True,
            },
            "standing": {
                "has_arms_front": True,
            },
        },

        # ── Rogue ─────────────────────────────────────────────
        "rogue": {
            "strip_chest_includes_over": True,

            "standing": {
                "has_arms_front": True,
            },

            "blowjob": {
                "has_torso_type2": True,
                "has_sucking_mouth": True,
            },
            "titjob": {
                "boobs_transforms": {
                    1: "titjob_boobs_rogue1",
                    2: "titjob_boobs_rogue2",
                    3: "titjob_boobs_rogue3",
                },
                "nipples_transforms": {
                    1: "titjob_nipples_rogue1",
                    2: "titjob_nipples_rogue2",
                    3: "titjob_nipples_rogue3",
                },
            },
            "cowgirl": {
                "guy_z": 10050,
                "guy_synced": True,
                "chest_up_removes_over": True,
                "has_shoulders": True,
                "chest_always_hidden": True,
                "mast_corset_z": 9995,
                "mast_boobs_clothed_z": 9989,
                "mast_nipples_clothed_z": 9990,
                "mast_boobs_z": 9989,
                "mast_nipples_z": 9990,
                "mast_chest_z": 9991,
            },
            "doggy": {
                "leg_left_transforms": {
                    0: "dg_rogue_leg_left_speed0",
                    1: "dg_rogue_leg_left_speed1",
                    2: "dg_rogue_leg_left_speed2",
                    3: "dg_rogue_leg_left_speed3",
                },
                "leg_right_transforms": {
                    0: "dg_rogue_leg_right_speed0",
                    1: "dg_rogue_leg_right_speed1",
                    2: "dg_rogue_leg_right_speed2",
                    3: "dg_rogue_leg_right_speed3",
                },
            },
            "rcg": {
                "slot_offset": "rcg_slot_rogue_offset",
                "uses_conditionswitch": True,
                "arms_2_in_li": True,
            },
        },

        # ── Negasonic ─────────────────────────────────────────
        "ntw": {
            "standing": {
                "has_arms_front": True,
            },
            "blowjob": {
                "has_torso_type2": True,
                "has_sucking_mouth": True,
            },
            "titjob": {
                "tj_arms_list": [2, 3],
            },
            "cowgirl": {
                "has_shoulders": True,
            },
            "rcg": {
                "uses_conditionswitch": True,
                "over_blocks_penetration": True,
            },
        },

        # ── Tenny ─────────────────────────────────────────────
        "tenny": {
            "standing": {
                "has_arms_front": True,
                "has_chest_clothes_body": True,
            },
            "blowjob": {
                "has_torso_type2": True,
                "has_back_arms": True,
                "has_sucking_mouth": False,
                "has_looking_right": True,
                "default_torso_type": 2,
                "pov_overlay": True,
                "has_head_normal": True,
            },
            "handjob": {
                "pov_overlay": True,
                "has_hide_face": False,
            },
        },

        # ── Shion ─────────────────────────────────────────────
        "shion": {
            "standing": {
                "has_arms_front": True,
                "has_chest_clothes_body": True,     # "Boobs No Nip" under a bra / bikini top
                "preg_crossed_arms": True,          # she crosses her arms pregnant too (arm pose 4, "Jacket Preg Crossed")
            },
            "blowjob": {
                "has_torso_type2": True,
                "has_sucking_mouth": True,
                "has_head_normal": True,            # "Head Top" (mouth cut out) while she works, "Head" at rest
            },
            "cowgirl": {
                "uses_conditionswitch": True,
            },
            "rcg": {
                "uses_conditionswitch": True,
                "sex_nude": True,                   # no dressed penetration art: everything off before he goes in (tip too)
                "anal": True,                       # her art draws him in her ass (Butt Top 2 = the mask): Core_RCG rcg_has_anal
                "has_rub": False,                   # no rub mode: tip is the entry point
                "has_arms_change": False,           # one arm pose, no "Change her arms"
                "has_hide_face": False,             # no "Tell her to look forward/back"
                "has_hold": False,                  # no "Hold her down" (art exists but disabled by design)
                "cum_outside_targets": ("ass",),    # only "On her ass" in the outside cum menu
            },
            "doggy": {
                "uses_conditionswitch": True,
                "self_touch_anal": True,            # her hand on herself while he is in her ass (Doggy/Hand.png); never vaginal
                "has_hide_face": True,              # Head 2 shows her face; hidden = Head 1 (from behind): the look away /
                                                    # look back orders and the recording's "hide her face" (dg_has_hide_face)
                "has_grab": False,                  # no "Grab her ass": no hands-on-her-ass art in this pose (dg_has_grab)
            },
        },
    }

    GIRL_DISABLED_POSES = {
        "ntw": {"doggy", "laying_down"},
        "gwen": {"full_nelson", "laying_down"},
        "rogue": {"full_nelson", "laying_down"},
        "tenny": {"titjob", "cowgirl", "reverse_cowgirl", "doggy"},
        # cowgirl: her riding art is in (Images/Shion/Cowgirl.rpy, F9) but off in play for now (author, 2026-10-05);
        # her masturbation lives in the doggy pose (mast_pose)
        "shion": {"full_nelson", "laying_down", "cowgirl"},
    }

    # Poses only some girls have the art for (opt-in: a girl not listed never gets them, a new girl included).
    # The act of the pose is _ACT_TO_POSE (characters_stats.rpy): "fj" -> footjob, "rj" -> rimjob.
    POSE_ONLY_FOR = {
        "footjob": ("tenny",),
        "rimjob": ("shion",),
    }

    def girl_has_pose(girl, pose):
        if pose in POSE_ONLY_FOR and girl.gid not in POSE_ONLY_FOR[pose]:
            return False
        return pose not in GIRL_DISABLED_POSES.get(girl.gid, set())

    def _rear_pose_for(girl):
        """The pose of a face-down moment (massage, sunscreen, touch massage): her SOLO rear pose.
        "doggy" for a girl whose solo scene lives there (mast_pose "doggy", Shion: her RCG rides ON
        the player, no pose for a massage, and nothing of his may be drawn, author 2026-10-11);
        "laying_down" without an RCG (Tenny); else "reverse_cowgirl"."""
        if getattr(girl, "mast_pose", "") == "doggy":
            return "doggy"
        return "reverse_cowgirl" if girl_has_pose(girl, "reverse_cowgirl") else "laying_down"

    def _setup_rear_pose_vars(girl):
        _kind = _rear_pose_for(girl)
        if _kind == "doggy":
            # her solo-doggy display (the python of _dg_masturbate_setup, Core_Doggy): her layers
            # only, nothing of his drawn (_sdg_mode "mast") and no hand of hers either (_dg_massage,
            # read by _sdg_hand_on). The caller shows it with DG_ApplySpeed(girl, 0).
            _clear_scene_refs("doggy")
            _hide_non_scene_girls(girl)
            store._doggy_girl = girl
            store.doggy_started = False
            store.doggy_rub_mode = False
            store.doggy_tip_mode = False
            store.doggy_anal = False
            store.doggy_grab = False
            store.doggy_speed = 0
            store._dg_butt_state = "base"
            store._dg_had_pussy = False
            store._dg_had_anal = False
            store._dg_masturbating = True
            store._dg_massage = True
            store._oral_active = False
            store.hiding_face = False
            sprite_state.setdefault(girl.Id, {})["pose"] = "doggy"
            if girl.gid == "shion":
                store._sdg_girl = girl
                store._sdg_head_pos = 2
                store._sdg_butt_state = "closed"
                store._sdg_guy_on = False
            hide_girl_sprite(girl)
            return _kind
        if _kind == "laying_down":
            store._laying_girl = girl
            store.laying_started = False
            store.laying_rub_mode = False
            store.laying_tip_mode = False
            store.laying_anal = False
            store.laying_grab = False
            store.laying_speed = 0
            store._ld_torso_variant = 1
            store._ld_arm_variant = 2
            sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
            return _kind
        else:
            store._rcg_girl = girl
            store.rcg_started = False
            store.rcg_rub_mode = False
            store.rcg_tip_mode = False
            store.rcg_grab = False
            store.rcg_hold = False
            store.rcg_anal = False
            store.rcg_arms_pose = 1
            store.rcg_butt_state = "butt_top_1"
            return _kind

    def _start_rear_blink(girl):
        _kind = _rear_pose_for(girl)
        if _kind == "doggy":
            # the solo-doggy threads (the tail of _dg_masturbate_setup, Core_Doggy)
            if girl.gid == "shion":
                renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_doggy_girl", blink_timing=(0.12, 0.22))
            else:
                renpy.invoke_in_thread(_scene_blink_loop, girl, "_doggy_girl", "doggy_blink", cs_girls=_dg_cs_girls(), blink_timing=(0.12, 0.22))
            renpy.invoke_in_thread(_doggy_expression_cycle, girl)
        elif _kind == "laying_down":
            renpy.invoke_in_thread(_ld_blink_loop, girl)
            renpy.invoke_in_thread(_laying_expression_cycle, girl)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_rcg_girl", "rcg_blink", is_active_fn=_rcg_is_active, cs_girls=_RCG_CS_GIRLS)
            renpy.invoke_in_thread(_rcg_expression_cycle, girl)

    def _rear_grab_img(girl, side=None):
        _kind = _rear_pose_for(girl)
        if _kind == "doggy":
            # the doggy pose's open hand (Shion: one full-screen art, no sides; grab art is on the
            # artist's list). Shown with _rear_grab_at: anchored (0,0), never at the girl slot.
            return "%s sdg_slap" % girl.gid
        if _kind == "laying_down":
            return "tenny laying_grab_%s" % (side or "left")
        _img = "%s rcg_grab_butt" % girl.gid
        if not renpy.has_image(_img, exact=True):
            # a girl without grab art yet (Shion 2026-10-10): the slap's open hand stands in, never an
            # "image not found" box on screen; her real grab art is on the artist's list
            return "%s rcg_slap_%s" % (girl.gid, side or "left")
        return _img

    def _rear_grab_at(girl):
        """The at_list of the massage / sunscreen ass rub: the LD / RCG grab arts circle at the girl
        slot (massage_ass_motion); the doggy's hand art is FULL SCREEN with the hand baked where it
        lands (sdg_slap), so its circles anchor at (0,0) (massage_ass_motion_dg, Flirty.rpy)."""
        if _rear_pose_for(girl) == "doggy":
            return [massage_ass_motion_dg]
        return [massage_ass_motion]

    def _rear_pose_hide(girl):
        """The touch massage's quick exit (no *_End label): hide that rear pose's layers; the doggy
        solo also drops its flags and refs (nothing else clears them on this path)."""
        _kind = _rear_pose_for(girl)
        if _kind == "doggy":
            _hide_scene_layers("doggy")
            store._dg_masturbating = False
            store._dg_massage = False
            store._doggy_girl = None
            store._sdg_girl = None
        else:
            _hide_scene_layers(_kind)

    def _rear_slap_img(girl, side):
        if _rear_pose_for(girl) == "doggy":
            return "%s sdg_slap" % girl.gid
        if not girl_has_pose(girl, "reverse_cowgirl"):
            return "tenny laying_slap_%s" % side
        return "%s rcg_slap_%s" % (girl.gid, side)

    def _rear_slap_tf(girl, side):
        if _rear_pose_for(girl) == "doggy":
            return sdg_slap_in
        if not girl_has_pose(girl, "reverse_cowgirl"):
            return ld_slap_right_in if side == "right" else ld_slap_left_in
        return rcg_slap_right_in if side == "right" else rcg_slap_left_in

    _DG_CS_GIRLS = {gid for gid, cfg in GIRL_SCENE_CONFIG.items() if cfg.get("doggy", {}).get("uses_conditionswitch")}
    _RCG_CS_GIRLS = {gid for gid, cfg in GIRL_SCENE_CONFIG.items() if cfg.get("rcg", {}).get("uses_conditionswitch")}

    def scene_has_hide_face(gid, pose):
        """ONE source of truth for "has_hide_face" (review 2026-10-10: the menu read it with default True and
        the doggy with default False). A pose shows her face unless her config says otherwise, EXCEPT the
        doggy, drawn from behind by default: only an art with a face entry (Shion's Head 2) turns it on."""
        return bool(_gsc(gid, "has_hide_face", pose != "doggy", pose))

    def _gsc(gid, key, default=None, pose=None):
        """Lookup GIRL_SCENE_CONFIG: girl+pose -> girl-level -> default value."""
        cfg = GIRL_SCENE_CONFIG.get(gid, {})
        if pose:
            pose_cfg = cfg.get(pose, {})
            if key in pose_cfg:
                return pose_cfg[key]
        if key in cfg:
            return cfg[key]
        return default

    renpy._orig_gsc = _gsc
    renpy.pure("_gsc")

    # ── Generic strip helpers ─────────────────────────────────

    def _get_strip_slots(girl, slot):
        """Get actual slots to strip, handling linked slots.
        e.g. Rogue: stripping 'chest' also strips 'over' (crop_top covers both)."""
        if _gsc(girl.gid, "strip_chest_includes_over") and slot in ("chest", "over"):
            return ["over", "chest"]
        return [slot]

    def _do_strip_change(girl, slot, pose):
        """Execute Outfit_Change for strip with linked slot handling."""
        slots = _get_strip_slots(girl, slot)
        kwargs = {s: "none" for s in slots}
        kwargs["pose"] = pose
        girl.Outfit_Change(**kwargs)

    # ── Centralized cum expressions ──────────────────────────

    CUM_EXPRESSIONS = {
        "cowgirl": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_surprised_2", "eyes_squint_big"], "mouth": ["mouth_tongue"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint_big", "eyes_closed"], "mouth": ["mouth_disgusted"], "brows": ["brows_surprised"]},
                "default": {"eyes": ["eyes_surprised", "eyes_surprised_2", "eyes_squint_big"], "mouth": ["mouth_tongue", "mouth_surprised"], "brows": ["brows_horny", "brows_surprised"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_surprised_2", "eyes_squint_big"], "mouth": ["mouth_tongue", "mouth_laugh"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_closed"], "mouth": ["mouth_disgusted", "mouth_open_teeth"], "brows": ["brows_surprised"]},
                "default": {"eyes": ["eyes_surprised", "eyes_squint_big", "eyes_side"], "mouth": ["mouth_surprised", "mouth_smile", "mouth_tongue"], "brows": ["brows_surprised", "brows_normal"]},
            },
        },
        "rcg": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_looking_up", "eyes_surprised_2"], "mouth": ["mouth_tongue"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint_big", "eyes_closed"], "mouth": ["mouth_scared"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_surprised", "eyes_looking_up", "eyes_squint_big"], "mouth": ["mouth_tongue", "mouth_surprised"], "brows": ["brows_horny", "brows_surprised"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_looking_to_player", "eyes_surprised"], "mouth": ["mouth_tongue", "mouth_smile"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_looking_to_player"], "mouth": ["mouth_scared", "mouth_disgusted"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_looking_to_player", "eyes_surprised", "eyes_side"], "mouth": ["mouth_surprised", "mouth_smile", "mouth_tongue"], "brows": ["brows_surprised", "brows_normal"]},
            },
        },
        "doggy": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_looking_up", "eyes_surprised_2"], "mouth": ["mouth_tongue"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint_big", "eyes_closed"], "mouth": ["mouth_scared"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_surprised", "eyes_looking_up", "eyes_squint_big"], "mouth": ["mouth_tongue", "mouth_surprised"], "brows": ["brows_horny", "brows_surprised"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_looking_to_player", "eyes_surprised"], "mouth": ["mouth_tongue", "mouth_smile"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_looking_to_player"], "mouth": ["mouth_scared", "mouth_disgusted"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_looking_to_player", "eyes_surprised", "eyes_side"], "mouth": ["mouth_surprised", "mouth_smile", "mouth_tongue"], "brows": ["brows_surprised", "brows_normal"]},
            },
        },
        "handjob": {
            # his load always lands ON her in a handjob: the key is "outside" (it was "inside", which also
            # read as a creampie face on the mouth-ask denial; tester 2026-10-10)
            "outside": {
                "cum_slut": {"eyes": ["eyes_surprised", "eyes_squint_big"], "mouth": ["mouth_tongue"], "brows": ["brows_surprised"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_closed"], "mouth": ["mouth_disgusted", "mouth_surprised"], "brows": ["brows_surprised"]},
                "default": {"eyes": ["eyes_surprised", "eyes_surprised_2", "eyes_squint_big"], "mouth": ["mouth_surprised", "mouth_tongue", "mouth_laugh"], "brows": ["brows_surprised", "brows_normal"]},
            },
        },
        "footjob": {
            # his cum lands on her feet: always "outside" (names from the ft_head ConditionSwitch)
            "outside": {
                "cum_slut": {"eyes": ["eyes_ahegao", "eyes_ahegao_2"], "mouth": ["mouth_tongue"], "brows": ["brows_surprised"]},
                "hate_cum": {"eyes": ["eyes_closed", "eyes_squint_big"], "mouth": ["mouth_scared", "mouth_sad"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_up_closed_surprised", "eyes_bliss"], "mouth": ["mouth_moaning_2", "mouth_laugh"], "brows": ["brows_surprised"]},
            },
        },
        "titjob": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_squint", "eyes_sexy"], "mouth": ["mouth_ahegao"], "brows": ["brows_challenging"]},
                "hate_cum": {"eyes": ["eyes_closed", "eyes_squint"], "mouth": ["mouth_sad", "mouth_surprised"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_squint", "eyes_sexy", "eyes_closed"], "mouth": ["mouth_ahegao", "mouth_surprised"], "brows": ["brows_confused", "brows_challenging"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_looking_left", "eyes_looking_right"], "mouth": ["mouth_ahegao", "mouth_kiss"], "brows": ["brows_challenging"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_closed"], "mouth": ["mouth_sad", "mouth_surprised"], "brows": ["brows_confused"]},
                "default": {"eyes": ["eyes_looking_left", "eyes_squint", "eyes_normal"], "mouth": ["mouth_surprised", "mouth_ahegao", "mouth_lipbite"], "brows": ["brows_confused", "brows_normal"]},
            },
        },
        "full_nelson": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_ahegao", "eyes_bliss"], "mouth": ["mouth_moaning_3", "mouth_screaming"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_surprised", "eyes_closed"], "mouth": ["mouth_scared", "mouth_screaming"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_surprised", "eyes_up", "eyes_squint"], "mouth": ["mouth_screaming", "mouth_moaning_2"], "brows": ["brows_scared", "brows_surprised"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_bliss", "eyes_ahegao"], "mouth": ["mouth_moaning_2", "mouth_moaning_3"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_side"], "mouth": ["mouth_scared", "mouth_angry"], "brows": ["brows_sad", "brows_scared"]},
                "default": {"eyes": ["eyes_surprised", "eyes_squint", "eyes_side"], "mouth": ["mouth_moaning_2", "mouth_surprised"], "brows": ["brows_surprised", "brows_scared"]},
            },
        },
        "full_nelson_anal": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_ahegao", "eyes_ahegao_2", "eyes_up"], "mouth": ["mouth_moaning_3", "mouth_screaming"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_surprised", "eyes_closed"], "mouth": ["mouth_scared", "mouth_screaming"], "brows": ["brows_sad", "brows_scared"]},
                "default": {"eyes": ["eyes_surprised", "eyes_up", "eyes_closed"], "mouth": ["mouth_screaming", "mouth_moaning_3"], "brows": ["brows_scared", "brows_sad"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_bliss", "eyes_up"], "mouth": ["mouth_moaning_2", "mouth_moaning_3"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_closed"], "mouth": ["mouth_scared", "mouth_angry"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_squint", "eyes_surprised", "eyes_side"], "mouth": ["mouth_moaning_2", "mouth_scared"], "brows": ["brows_scared", "brows_surprised"]},
            },
        },
        "laying_down": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_ahegao", "eyes_bliss"], "mouth": ["mouth_moaning_3", "mouth_screaming"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_surprised", "eyes_closed"], "mouth": ["mouth_scared", "mouth_screaming"], "brows": ["brows_sad", "brows_scared"]},
                "default": {"eyes": ["eyes_surprised", "eyes_up", "eyes_squint"], "mouth": ["mouth_screaming", "mouth_moaning_2"], "brows": ["brows_surprised", "brows_scared"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_bliss", "eyes_ahegao"], "mouth": ["mouth_moaning_2", "mouth_moaning_3"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_side"], "mouth": ["mouth_scared", "mouth_angry"], "brows": ["brows_sad", "brows_scared"]},
                "default": {"eyes": ["eyes_surprised", "eyes_squint", "eyes_side"], "mouth": ["mouth_moaning_2", "mouth_surprised"], "brows": ["brows_surprised", "brows_scared"]},
            },
        },
        "laying_anal": {
            "inside": {
                "cum_slut": {"eyes": ["eyes_ahegao", "eyes_ahegao_2", "eyes_up"], "mouth": ["mouth_moaning_3", "mouth_screaming"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_surprised", "eyes_closed"], "mouth": ["mouth_scared", "mouth_screaming"], "brows": ["brows_sad", "brows_scared"]},
                "default": {"eyes": ["eyes_surprised", "eyes_up", "eyes_closed"], "mouth": ["mouth_screaming", "mouth_moaning_3"], "brows": ["brows_scared", "brows_sad"]},
            },
            "outside": {
                "cum_slut": {"eyes": ["eyes_bliss", "eyes_up"], "mouth": ["mouth_moaning_2", "mouth_moaning_3"], "brows": ["brows_horny"]},
                "hate_cum": {"eyes": ["eyes_squint", "eyes_closed"], "mouth": ["mouth_scared", "mouth_angry"], "brows": ["brows_sad"]},
                "default": {"eyes": ["eyes_squint", "eyes_surprised", "eyes_side"], "mouth": ["mouth_moaning_2", "mouth_scared"], "brows": ["brows_scared", "brows_surprised"]},
            },
        },
    }

    def _apply_cum_expression(girl, pose, cum_type="inside"):
        """Set cum reaction expression on girl's sprite_state."""
        state = sprite_state.setdefault(girl.Id, {})
        cfg = CUM_EXPRESSIONS.get(pose, {}).get(cum_type, {})
        if not cfg:
            return
        _is_anal_pose = "anal" in pose
        if cum_type == "inside":
            is_eager = girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex") or (_is_anal_pose and girl.has_trait("anal_lover"))
        else:
            is_eager = girl.has_trait("cum_slut") or (_is_anal_pose and girl.has_trait("anal_lover"))
        is_hate = girl.has_trait("hate_cum") or (_is_anal_pose and girl.has_trait("anal_hater"))
        if getattr(store, '_cum_forced_surprise', False) and not is_eager:
            pool = {"eyes": ["eyes_surprised"], "mouth": ["mouth_surprised"], "brows": ["brows_surprised"]}
            store._cum_forced_surprise = False
        elif is_eager:
            pool = cfg.get("cum_slut", {})
        elif is_hate:
            pool = cfg.get("hate_cum", {})
        else:
            pool = cfg.get("default", {})
        for key in ("eyes", "mouth", "brows"):
            choices = pool.get(key)
            if choices:
                state[key] = renpy.random.choice(choices) if len(choices) > 1 else choices[0]
