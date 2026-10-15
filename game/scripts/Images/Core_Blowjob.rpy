# ============================================================
# CORE BLOWJOB SYSTEM (BODY MOVES / PENIS FIXED)
# ============================================================

default bj_speed = 1
default bj_action = "lick"
default bj_cheeks = False
default bj_eyes  = "normal"
default bj_brows = 1
default _bj_girl = None
default bj_torso_type = 1          # 1 = padrao | 2 = torso alternativo (arm + hand) | 3 = hiding face | 4 = arms behind back
default _bj_face_ordered_shown = False  # True after player orders her to show face (cannot hide again)
default _bj_cheeks_running = False  # guard para evitar multiplas threads de cheeks
default _bj_blink_running  = False  # guard para evitar multiplas threads de blink
default bj_idle_mouth = "mouth_tongue"  # mouth mostrada antes da acao comecar
default _bj_cum_done = False             # flag para retornar ao ControlMenu apos cum
default bj_forcing = False               # True = player forcing her head down
default _bj_pre_force_torso = 1          # torso_type before force started
default _bj_cum_entry_torso = 1          # torso_type captured at BJ_CumAnim entry
default _bj_cum_entry_forcing = False    # bj_forcing captured at BJ_CumAnim entry
default _recording_active = False
default _recording_girl = None
default _recording_face_locked = False
default _recording_watcher_gid = None

init python:
    def bj_debug_layers():
        """Console: bj_debug_layers() — shows all images on master layer with z-order"""
        try:
            sl = renpy.game.context().scene_lists
            items = []
            for entry in sl.layers['master']:
                z = getattr(entry, 'zorder', '?')
                tag = getattr(entry, 'tag', '?')
                name = getattr(entry, 'name', None)
                name_str = " ".join(str(x) for x in name) if name else str(tag)
                items.append((z, tag, name_str))
            for z, tag, name_str in sorted(items, key=lambda x: x[0] if isinstance(x[0], (int, float)) else 0):
                print("%5s  %-35s  %s" % (z, tag, name_str))
        except Exception as e:
            print("Error: %s" % e)
            try:
                for tag in sorted(renpy.get_showing_tags()):
                    print("  showing: %s" % tag)
            except:
                print("Could not list tags either")

    def _bj_pause_forcing():
        saved = {
            "bj_forcing": store.bj_forcing,
            "_bj_use_half_penis": getattr(store, "_bj_use_half_penis", False),
        }
        if store.bj_forcing:
            store.bj_forcing = False
            store._bj_use_half_penis = False
        return saved

    def _bj_resume_forcing(saved):
        if saved.get("bj_forcing"):
            store.bj_forcing = True
            store._bj_use_half_penis = saved.get("_bj_use_half_penis", False)

    # BJ feature flags — configured in GIRL_SCENE_CONFIG (scene_config.rpy)
    def bj_has_sucking_mouth(girl):
        return _gsc(getattr(girl, "gid", ""), "has_sucking_mouth", False, "blowjob")

    def bj_has_looking_right(girl):
        return _gsc(getattr(girl, "gid", ""), "has_looking_right", False, "blowjob")

    def _bj_get_penis_tf(girl):
        gid = getattr(girl, "gid", "")
        _tf = renpy.store
        return getattr(_tf, "%s_bj_penis_corner" % gid, bj_penis_corner)()

    def _bj_get_penis_cum_tf(girl):
        gid = getattr(girl, "gid", "")
        _tf = renpy.store
        return getattr(_tf, "%s_bj_penis_cum_pulse" % gid, bj_penis_cum_pulse)()

    # -----------------------------
    # CHEEKS CYCLE — thread que ativa/desativa bj_cheeks autonomamente
    # Aparece 1 vez a cada 3-5 ciclos de animacao e some no ciclo seguinte
    # Ciclo = tempo de ida + volta do head bounce por velocidade
    # -----------------------------
    BJ_CYCLE_TIME = {1: 1.55, 2: 1.28, 3: 1.04}

    def _bj_cheeks_cycle():
        import time, random
        store._bj_cheeks_running = True
        try:
            while store._bj_girl is not None:
                spd    = store.bj_speed
                action = store.bj_action

                # So ativa durante suck com movimento
                if action != "suck" or spd == 0:
                    time.sleep(0.3)
                    continue

                cycle = BJ_CYCLE_TIME.get(spd, 1.55)

                # Espera 3-5 ciclos antes de mostrar
                end = time.time() + random.randint(3, 5) * cycle
                while time.time() < end:
                    if store._bj_girl is None:
                        return
                    time.sleep(0.05)

                if store._bj_girl is None:
                    break
                if store.bj_action != "suck" or store.bj_speed == 0:
                    continue

                # Liga cheeks por 1 ciclo
                store.bj_cheeks = True
                renpy.restart_interaction()

                cycle2 = BJ_CYCLE_TIME.get(store.bj_speed, 1.55)
                end2 = time.time() + cycle2
                while time.time() < end2:
                    if store._bj_girl is None:
                        store.bj_cheeks = False
                        renpy.restart_interaction()
                        return
                    time.sleep(0.05)

                # Desliga cheeks
                store.bj_cheeks = False
                renpy.restart_interaction()
        finally:
            store.bj_cheeks = False
            store._bj_cheeks_running = False

    def bj_has_torso2(girl):
        return _gsc(getattr(girl, "gid", ""), "has_torso_type2", False, "blowjob")

    def bj_has_back_arms(girl):
        return _gsc(getattr(girl, "gid", ""), "has_back_arms", False, "blowjob")

    # -----------------------------
    # INITIAL MOUTH — mapeia a boca do standing para a boca de idle da BJ
    # -----------------------------
    _BJ_MOUTH_FROM_STANDING = {
        "mouth_smile":     "mouth_smile",
        "mouth_happy":     "mouth_happy",
        "mouth_giggle":    "mouth_smile",
        "mouth_surprised": "mouth_surprised",
        "mouth_angry":     "mouth_lipbite",
        "mouth_pout":      "mouth_lipbite",
    }
    _BJ_NEUTRAL_MOUTHS = ["mouth_tongue", "mouth_lipbite"]

    def _bj_initial_mouth_for_girl(girl):
        state = sprite_state.get(girl.Id, {})
        standing_mouth = state.get("mouth", "mouth_normal")
        mapped = _BJ_MOUTH_FROM_STANDING.get(standing_mouth, None)
        if mapped:
            print("[BJ_MOUTH] %s standing_mouth=%s -> mapped=%s" % (girl.gid, standing_mouth, mapped))
            return mapped
        result = renpy.random.choice(_BJ_NEUTRAL_MOUTHS)
        print("[BJ_MOUTH] %s standing_mouth=%s -> no map, random=%s" % (girl.gid, standing_mouth, result))
        return result

    # -----------------------------
    # RESET — esconde todos os layers BJ e restaura variaveis de estado
    # Chamar antes de trocar acao, ao voltar ao ControlMenu e ao sair da cena.
    # -----------------------------
    def _bj_hide_all(girl):
        """Esconde todos os layers gerenciados pela cena BJ."""
        gid = girl.gid
        renpy.hide(gid)
        renpy.hide("%s_bj_jaw" % gid)
        renpy.hide("%s_bj_head" % gid)
        renpy.hide("%s_bj_sucking_mouth" % gid)
        renpy.hide("%s_bj_right_arm" % gid)
        renpy.hide("%s_bj_arm" % gid)
        renpy.hide("%s_bj_hand" % gid)
        renpy.hide("%s_bj_back_arm_left" % gid)
        renpy.hide("%s_bj_back_arm_right" % gid)
        renpy.hide("%s_bj_forcing_left" % gid)
        renpy.hide("%s_bj_forcing_right" % gid)
        renpy.hide("%s_bj_hide_left" % gid)
        renpy.hide("%s_bj_hide_right" % gid)
        renpy.hide("%s_bj_cum_face" % gid)
        renpy.hide("%s_bj_cum_face_under" % gid)
        renpy.hide("%s_bj_cum_mouth" % gid)
        renpy.hide("bj_penis")
        renpy.hide("bj_penis_guy")
        renpy.hide("bj_guy")

    def _bj_reset_state(girl):
        """Reseta todas as variaveis de estado da cena BJ para os defaults."""
        store.bj_action      = "suck"
        store.bj_speed       = 0
        store.bj_cheeks      = False
        store.bj_eyes        = "normal"
        store.bj_brows       = 1
        if not store.hiding_face:
            store.bj_torso_type = _gsc(girl.gid, 'default_torso_type', 1, pose='blowjob')
        store.bj_forcing     = False
        store._bj_use_half_penis = False
        store._bj_force_obed_given = False
        store.bj_idle_mouth  = _bj_initial_mouth_for_girl(girl)

    def _bj_arm_hand_transforms(speed):
        """Retorna (arm_t, right_arm_t, hand_t) sincronizados para a velocidade dada."""
        _map = {1: bj_arm_speed1, 2: bj_arm_speed2, 3: bj_arm_speed3}
        fn = _map.get(speed, bj_arm_speed1)
        return fn(), bj_right_arm_move(), fn()

    # -----------------------------
    # EXPRESSION POOLS — olhos e sobrancelhas por velocidade
    # -----------------------------
    BJ_EYES_BY_SPEED = {
        0: ["normal"],
        1: ["normal", "squint", "left_closed"],
        2: ["squint", "squint_2", "left_closed", "right_closed"],
        3: ["squint_2", "left_closed", "right_closed"],
    }
    BJ_BROWS_BY_SPEED = {
        0: [1],
        1: [1, 2, 3],
        2: [2, 3, 4],
        3: [3, 4, 5],
    }

    # -----------------------------
    # SLOT TRANSFORM
    # -----------------------------
    def bj_get_slot_transform(speed):
        # Lick: corpo quase nao se move — apenas rotacao suave de idle
        if bj_action == "lick":
            return bj_slot_lick
        if store.bj_forcing and speed >= 1:
            _gid = getattr(store._bj_girl, "gid", "") if store._bj_girl else ""
            for _s in (speed, 1):
                _tf = getattr(renpy.store, "%s_bj_slot_force_speed%d" % (_gid, _s), None)
                if _tf:
                    return _tf
            force_map = {1: bj_slot_force_speed1, 2: bj_slot_force_speed2, 3: bj_slot_force_speed3}
            return force_map.get(speed, force_map[1])
        slot_map = {0: bj_slot_speed0, 1: bj_slot_speed1, 2: bj_slot_speed2, 3: bj_slot_speed3}
        return slot_map.get(speed, slot_map[1])

    def bj_get_head_transform(speed):
        if bj_action == "lick" and speed >= 1:
            return bj_head_lick_speed1
        if store.bj_forcing and speed >= 1:
            _gid = getattr(store._bj_girl, "gid", "") if store._bj_girl else ""
            for _s in (speed, 1):
                _tf = getattr(renpy.store, "%s_bj_head_force_speed%d" % (_gid, _s), None)
                if _tf:
                    return _tf
            force_map = {1: bj_head_force_speed1, 2: bj_head_force_speed2, 3: bj_head_force_speed3}
            return force_map.get(speed, force_map[1])
        slot_map = {0: bj_head_speed0, 1: bj_head_speed1, 2: bj_head_speed2, 3: bj_head_speed3}
        return slot_map.get(speed, slot_map[1])

    def _bj_head_variant(gid, speed=None):
        """THE head attribute her blowjob head wears now (layeredimage names). A girl with has_head_normal
        (scene_config: Shion, Tenny) works on "head_base" = "Head Top", the mouth cut out so the penis shows
        through, and her JAW art is her open mouth under it; she rests (speed 0) and speaks (_bj_head_normal)
        on the full "head_normal". A face mouth (surprised, smile...) drawn on her working head makes TWO mouths
        (player report 2026-10-11: her husband's call during a BJ). Every other girl: "head_base" always, her
        jaw art is a bare chin."""
        if not _gsc(gid, 'has_head_normal', False, pose='blowjob'):
            return "head_base"
        if speed is None:
            speed = getattr(store, 'bj_speed', 0)
        if speed == 0 or getattr(store, '_bj_head_normal', False):
            return "head_normal"
        return "head_base"

    def _bj_swap_speaking_head(girl):
        _bj = getattr(store, '_bj_girl', None)
        if _bj is not girl:
            print("[BJ_HEAD] swap BLOCKED: _bj_girl mismatch (_bj=%s, girl=%s)" % (_bj, girl))
            return False
        if getattr(store, '_bj_head_normal', False):
            print("[BJ_HEAD] swap BLOCKED: _bj_head_normal already True")
            return False
        if getattr(store, 'bj_forcing', False):
            print("[BJ_HEAD] swap BLOCKED: bj_forcing is True")
            return False
        _gid = getattr(girl, 'gid', '')
        if not _gsc(_gid, 'has_head_normal', False, pose='blowjob'):
            return False

        _prev_speed = getattr(store, 'bj_speed', 0)
        store._bj_speaking_saved_speed = _prev_speed

        if _prev_speed > 0:
            store.bj_speed = 0
            _slot0 = bj_get_slot_transform(0)
            _head0 = bj_get_head_transform(0)
            _attrs = _build_attributes_for_girl(girl, pose="blowjob")
            _img = "%s blowjob" % _gid
            if _attrs:
                _img += " " + " ".join(_attrs)
            renpy.show(_img, tag=_gid, at_list=[_slot0], zorder=9980)
            _jaw_z = 9979 if (getattr(store, 'bj_forcing', False) and _gid == "tenny") else 9984
            renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head0], zorder=_jaw_z)
            renpy.hide("%s_bj_sucking_mouth" % _gid)
            _cum_under = "%s bj_cum_face_under" % _gid
            if renpy.has_image(_cum_under):
                renpy.show(_cum_under, tag="%s_bj_cum_face_under" % _gid, at_list=[_head0], zorder=9986)
            print("[BJ_HEAD] paused animation: speed %d -> 0" % _prev_speed)

        store._bj_head_normal = True
        _pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        _z = 10058 if _pov else 10015
        _at = [bj_get_head_transform(0)]
        _mouth = getattr(store, 'bj_idle_mouth', 'mouth_sucking')
        if _mouth in ('mouth_sucking', 'mouth_none', ''):
            _mouth = 'mouth_normal'
        renpy.show(
            "%s blowjob_head head_normal %s" % (_gid, _mouth),
            tag="%s_bj_head" % _gid,
            at_list=_at,
            zorder=_z
        )
        print("[BJ_HEAD] swap to head_normal for %s (mouth=%s, was_speed=%d)" % (_gid, _mouth, _prev_speed))
        return True

    def _bj_restore_speaking_head(girl):
        store._bj_head_normal = False
        _gid = getattr(girl, 'gid', '')
        _pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        _z = 10058 if _pov else 10015
        _prev_speed = getattr(store, '_bj_speaking_saved_speed', 0)

        if _prev_speed > 0 and getattr(store, 'bj_speed', 0) == 0:
            store.bj_speed = _prev_speed
            _slot_tf = bj_get_slot_transform(_prev_speed)
            _head_tf = bj_get_head_transform(_prev_speed)
            _attrs = _build_attributes_for_girl(girl, pose="blowjob")
            _img = "%s blowjob" % _gid
            if _attrs:
                _img += " " + " ".join(_attrs)
            renpy.show(_img, tag=_gid, at_list=[_slot_tf], zorder=9980)
            _action = getattr(store, 'bj_action', 'idle')
            if _action == "suck" and _prev_speed >= 1:
                _jaw_attr = "jaw_2"
            else:
                _jaw_attr = "jaw_1"
            _jaw_z = 9979 if (getattr(store, 'bj_forcing', False) and _gid == "tenny") else 9984
            renpy.show("%s blowjob_jaw %s" % (_gid, _jaw_attr), tag="%s_bj_jaw" % _gid, at_list=[_head_tf], zorder=_jaw_z)
            _cum_under = "%s bj_cum_face_under" % _gid
            if renpy.has_image(_cum_under):
                renpy.show(_cum_under, tag="%s_bj_cum_face_under" % _gid, at_list=[_head_tf], zorder=9986)
            if bj_has_sucking_mouth(girl) and _action == "suck" and not (getattr(store, 'bj_forcing', False) and _gid == "tenny"):
                renpy.show(
                    "%s bj_sucking_mouth" % _gid,
                    tag="%s_bj_sucking_mouth" % _gid,
                    at_list=[_head_tf],
                    zorder=10061 if _pov else 10030
                )
            print("[BJ_HEAD] resumed animation: speed 0 -> %d" % _prev_speed)

        _at = [bj_get_head_transform(getattr(store, 'bj_speed', 0))]
        _action = getattr(store, 'bj_action', 'idle')
        _cur_speed = getattr(store, 'bj_speed', 0)
        # at rest a cut-out head (has_head_normal) stays on the full head: a face mouth on "Head Top" = two mouths
        _head = "%s blowjob_head %s" % (_gid, _bj_head_variant(_gid, _cur_speed))
        if _cur_speed == 0:
            _mouth = getattr(store, 'bj_idle_mouth', 'mouth_sucking')
            _head += " " + _mouth
        elif _action == "lick":
            _head += " mouth_tongue"
        elif _action == "suck":
            _head += " mouth_sucking"
        else:
            _head += " mouth_tongue"
        renpy.show(_head, tag="%s_bj_head" % _gid, at_list=_at, zorder=_z)
        print("[BJ_HEAD] restored head_base for %s" % _gid)

    def _bj_pause_for_narration(girl):
        """Pause BJ to speed 0 + head_normal/head_base for narration. Works even during forcing."""
        _gid = getattr(girl, 'gid', '')
        _was_forcing = getattr(store, 'bj_forcing', False)
        _prev_speed = getattr(store, 'bj_speed', 0)
        store._bj_narration_saved_speed = _prev_speed
        store._bj_narration_saved_forcing = _was_forcing

        if _was_forcing:
            store.bj_forcing = False
            renpy.hide("%s_bj_forcing_left" % _gid)
            renpy.hide("%s_bj_forcing_right" % _gid)

        store.bj_speed = 0
        _slot0 = bj_get_slot_transform(0)
        _head0 = bj_get_head_transform(0)
        _attrs = _build_attributes_for_girl(girl, pose="blowjob")
        _img = "%s blowjob" % _gid
        if _attrs:
            _img += " " + " ".join(_attrs)
        renpy.show(_img, tag=_gid, at_list=[_slot0], zorder=9980)
        renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head0], zorder=9984)
        renpy.hide("%s_bj_sucking_mouth" % _gid)

        _pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        _z = 10058 if _pov else 10015
        _has_normal = _gsc(_gid, 'has_head_normal', False, pose='blowjob')
        _head_attr = "head_normal" if _has_normal else "head_base"
        renpy.show(
            "%s blowjob_head %s mouth_normal" % (_gid, _head_attr),
            tag="%s_bj_head" % _gid, at_list=[_head0], zorder=_z
        )
        print("[BJ_NARR] paused for narration: gid=%s speed=%d forcing=%s" % (_gid, _prev_speed, _was_forcing))
        return True

    def _bj_resume_from_narration(girl):
        """Resume BJ state after narration pause."""
        _gid = getattr(girl, 'gid', '')
        _prev_speed = getattr(store, '_bj_narration_saved_speed', 0)
        _was_forcing = getattr(store, '_bj_narration_saved_forcing', False)

        if _was_forcing:
            store.bj_forcing = True

        store.bj_speed = _prev_speed
        print("[BJ_NARR] resuming: gid=%s speed=%d forcing=%s" % (_gid, _prev_speed, _was_forcing))

# -----------------------------
# BLOWJOB SLOT (CHARACTER MOVES)
# Assimetrico: descida mais rapida (stroke), subida mais lenta (retorno)
# matrixanchor (960, 800) = pivot na cintura, rotacao independente do bounce
# -----------------------------
transform bj_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform bj_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 110
    block:
        ease 0.60 yoffset 125
        ease 0.95 yoffset 110
        repeat

transform bj_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 110
    block:
        ease 0.48 yoffset 130
        ease 0.80 yoffset 110
        repeat

transform bj_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 110
    block:
        ease 0.36 yoffset 140
        ease 0.68 yoffset 110
        repeat

# Force: corpo acompanha a cabeca (posicao mais baixa, range menor)
transform bj_slot_force_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 190
    block:
        ease 0.65 yoffset 207
        ease 0.95 yoffset 190
        repeat

transform bj_slot_force_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 210
    block:
        ease 0.48 yoffset 230
        ease 0.75 yoffset 210
        repeat

transform bj_slot_force_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 225
    block:
        ease 0.36 yoffset 245
        ease 0.60 yoffset 225
        repeat

# Lick: corpo estatico
transform bj_slot_lick:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

# Hide-face: corpo mais baixo, bounce maior que suck normal
transform bj_slot_hide_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 55

transform bj_slot_hide_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 135
    block:
        ease 0.60 yoffset 155
        ease 0.95 yoffset 135
        repeat

transform bj_slot_hide_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 135
    block:
        ease 0.48 yoffset 161
        ease 0.80 yoffset 135
        repeat

transform bj_slot_hide_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 135
    block:
        ease 0.36 yoffset 174
        ease 0.68 yoffset 135
        repeat

# -----------------------------
# HEAD SLOT
# Repouso em yoffset 145 — cabeca fica mais baixa, animacao desce e retorna
# ao mesmo ponto (nao sobe alem do repouso).
# -----------------------------
transform bj_head_speed0:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform bj_head_speed1:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    block:
        ease 0.60 yoffset 220   # descida
        ease 0.95 yoffset 145   # retorno ao repouso
        repeat

transform bj_head_speed1_bob:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    block:
        ease 0.70 yoffset 210   # descida
        ease 1.05 yoffset 145   # retorno lento (bob = devagar)
        repeat

transform bj_head_speed1_deep:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    block:
        ease 0.65 yoffset 245   # descida profunda
        ease 1.00 yoffset 145   # retorno
        repeat

transform bj_head_lick_speed1:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 60
    block:
        ease 1.20 yoffset 110
        ease 1.50 yoffset 60
        repeat

transform bj_head_speed2:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    block:
        ease 0.48 yoffset 265   # descida
        ease 0.80 yoffset 145   # retorno
        repeat

transform bj_head_speed3:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    block:
        ease 0.36 yoffset 285   # descida rapida
        ease 0.68 yoffset 145   # retorno
        repeat

# -----------------------------
# HEAD — Force her head (deep, minimal upward travel)
# Resting position is already very deep; head barely rises.
# -----------------------------
transform bj_head_force_speed1:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 300
    block:
        ease 0.65 yoffset 340
        ease 0.95 yoffset 300
        repeat

transform bj_head_force_speed2:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 320
    block:
        ease 0.48 yoffset 355
        ease 0.75 yoffset 320
        repeat

transform bj_head_force_speed3:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 335
    block:
        ease 0.36 yoffset 370
        ease 0.60 yoffset 335
        repeat

# -----------------------------
# Descent from normal to force depth (hands push head down)
# Head: 145 -> 300, Slot: 110 -> 190
# -----------------------------
transform bj_head_force_descent:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 145
    ease 0.7 yoffset 300

transform bj_slot_force_descent:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 110
    ease 0.7 yoffset 190

# -----------------------------
# Rise from force depth to idle (after forced swallow)
# Head: 335 -> 30, Slot: 225 -> 30, Jaw follows head
# -----------------------------
transform bj_head_force_rise:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 335
    ease 0.8 yoffset 30

transform bj_slot_force_rise:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 225
    ease 0.8 yoffset 30

# -----------------------------
# HEAD — cum in mouth (deepthroat push + slow bobs)
# Desce alem do maximo, volta ao limite, repete devagar
# -----------------------------
transform bj_head_cum_mouth:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 315
    # Push 1: desce fundo
    ease 0.30 yoffset 370
    ease 0.50 yoffset 315
    # Push 2: desce fundo de novo
    ease 0.30 yoffset 370
    ease 0.50 yoffset 315
    # Bobs lentos segurando
    block:
        ease 0.80 yoffset 340
        ease 1.20 yoffset 315
        repeat

# SLOT (body) — cum in mouth, acompanha a head
transform bj_slot_cum_mouth:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 165
    ease 0.30 yoffset 200
    ease 0.50 yoffset 165
    ease 0.30 yoffset 200
    ease 0.50 yoffset 165
    block:
        ease 0.80 yoffset 180
        ease 1.20 yoffset 165
        repeat

# JAW — cum in mouth, mesmo timing que head
transform bj_jaw_cum_mouth:
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset 315
    ease 0.30 yoffset 370
    ease 0.50 yoffset 315
    ease 0.30 yoffset 370
    ease 0.50 yoffset 315
    block:
        ease 0.80 yoffset 340
        ease 1.20 yoffset 315
        repeat

# -----------------------------
# GUY POSITION (FIXED, BEHIND EVERYTHING)
# -----------------------------
transform bj_guy_static:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

# -----------------------------
# PENIS POSITION (FIXED)
# -----------------------------
transform bj_penis_corner():
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    ypos 1.0
    xoffset 0
    yoffset 60

# Penis pulse during cum — yzoom throb synced with punches (Y axis only)
transform bj_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    ypos 1.0
    xoffset 0
    yoffset 60
    yzoom 1.0
    # Pulse 1 (synced with punch 1 at 0.50s)
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    # Pulse 2 (synced with punch 2 at 0.50s later)
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

# -----------------------------
# ARM / HAND — pivot em (845, 889), angulo e timing por velocidade
# -----------------------------
transform bj_arm_speed1():
    subpixel True
    matrixanchor (845, 889)
    block:
        ease 0.80 matrixtransform RotateMatrix(0, 0, -3)
        ease 1.10 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform bj_arm_speed2():
    subpixel True
    matrixanchor (845, 889)
    block:
        ease 0.55 matrixtransform RotateMatrix(0, 0, -5)
        ease 0.75 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform bj_arm_speed3():
    subpixel True
    matrixanchor (845, 889)
    block:
        ease 0.25 matrixtransform RotateMatrix(0, 0, -10)
        ease 0.35 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform bj_arm_cum():
    subpixel True
    matrixanchor (845, 889)
    block:
        ease 0.12 matrixtransform RotateMatrix(0, 0, -14)
        ease 0.16 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform bj_right_arm_move():
    subpixel True

# POV tunable values — shared with F12 Transform Tuner
init python:
    store._bj_pov_ar_ax = 1485
    store._bj_pov_ar_ay = 700
    store._bj_pov_ar_start = 22.0
    store._bj_pov_ar_end = 18.0
    store._bj_pov_al_ax = 1080
    store._bj_pov_al_ay = 785
    store._bj_pov_al_start = 0.0
    store._bj_pov_al_end = 8.0
    store._bj_pov_al_lick_start = 0.0
    store._bj_pov_al_lick_end = 3.0
    store._bj_pov_ar_lick_start = 22.0
    store._bj_pov_ar_lick_end = 20.0
    store._bj_pov_hand_static_y = -30
    store._bj_pov_hand_start = 90
    store._bj_pov_hand_end = 70

# POV arm transforms — read from store variables for live tuning
transform bj_pov_arm_left_speed1():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
    block:
        ease 0.60 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_end)
        ease 0.95 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
        repeat

transform bj_pov_arm_left_speed2():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
    block:
        ease 0.48 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_end)
        ease 0.80 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
        repeat

transform bj_pov_arm_left_speed3():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
    block:
        ease 0.36 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_end)
        ease 0.68 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_start)
        repeat

# Cum-in-mouth right arm: 10px toward center (1490), more rotation (19->0)
transform bj_cum_arm_right():
    subpixel True
    matrixanchor (1490, 710)
    matrixtransform RotateMatrix(0, 0, 19.0)
    block:
        ease 0.22 matrixtransform RotateMatrix(0, 0, 0.0)
        ease 0.18 matrixtransform RotateMatrix(0, 0, 19.0)
        repeat

# Cum-in-mouth left arm: HJ anchor + raised rotation (0->9) at HJ speed 2 timing
transform bj_cum_arm_left():
    subpixel True
    matrixanchor (store._hj_pov_al_ax, store._hj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, 0.0)
    block:
        ease 0.22 matrixtransform RotateMatrix(0, 0, 9.0)
        ease 0.18 matrixtransform RotateMatrix(0, 0, 0.0)
        repeat

# Cum-in-mouth hand: Y position (5 to 55) at HJ speed 2 timing — 50px range
transform bj_cum_hand:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 5
    block:
        ease 0.22 yoffset 55
        ease 0.18 yoffset 5
        repeat

# Cum-in-mouth hand static (menu visible)
transform bj_cum_hand_static:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform bj_pov_arm_right_speed1():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
    block:
        ease 0.60 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_end)
        ease 0.95 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
        repeat

transform bj_pov_arm_right_speed2():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
    block:
        ease 0.48 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_end)
        ease 0.80 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
        repeat

transform bj_pov_arm_right_speed3():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
    block:
        ease 0.36 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_end)
        ease 0.68 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_start)
        repeat

# POV arm transforms — lick variants (reduced rotation, body is 80px higher)
transform bj_pov_arm_left_lick_speed1():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
    block:
        ease 0.60 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_end)
        ease 0.95 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
        repeat

transform bj_pov_arm_left_lick_speed2():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
    block:
        ease 0.48 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_end)
        ease 0.80 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
        repeat

transform bj_pov_arm_left_lick_speed3():
    subpixel True
    matrixanchor (store._bj_pov_al_ax, store._bj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
    block:
        ease 0.36 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_end)
        ease 0.68 matrixtransform RotateMatrix(0, 0, store._bj_pov_al_lick_start)
        repeat

transform bj_pov_arm_right_lick_speed1():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
    block:
        ease 0.60 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_end)
        ease 0.95 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
        repeat

transform bj_pov_arm_right_lick_speed2():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
    block:
        ease 0.48 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_end)
        ease 0.80 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
        repeat

transform bj_pov_arm_right_lick_speed3():
    subpixel True
    matrixanchor (store._bj_pov_ar_ax, store._bj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
    block:
        ease 0.36 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_end)
        ease 0.68 matrixtransform RotateMatrix(0, 0, store._bj_pov_ar_lick_start)
        repeat

# POV hand transforms — lick variants animate around static position (30→50)
transform bj_pov_hand_lick_speed1:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_static_y
    block:
        ease 0.60 yoffset (store._bj_pov_hand_static_y + 20)
        ease 0.95 yoffset store._bj_pov_hand_static_y
        repeat

transform bj_pov_hand_lick_speed2:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_static_y
    block:
        ease 0.48 yoffset (store._bj_pov_hand_static_y + 20)
        ease 0.80 yoffset store._bj_pov_hand_static_y
        repeat

transform bj_pov_hand_lick_speed3:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_static_y
    block:
        ease 0.36 yoffset (store._bj_pov_hand_static_y + 20)
        ease 0.68 yoffset store._bj_pov_hand_static_y
        repeat

# POV hand transforms — suck variants (70→90)
transform bj_pov_hand_static:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_static_y

transform bj_pov_hand_speed1:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_end
    block:
        ease 0.60 yoffset store._bj_pov_hand_start
        ease 0.95 yoffset store._bj_pov_hand_end
        repeat

transform bj_pov_hand_speed2:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_end
    block:
        ease 0.48 yoffset store._bj_pov_hand_start
        ease 0.80 yoffset store._bj_pov_hand_end
        repeat

transform bj_pov_hand_speed3:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._bj_pov_hand_end
    block:
        ease 0.36 yoffset store._bj_pov_hand_start
        ease 0.68 yoffset store._bj_pov_hand_end
        repeat

# ============================================================
# SLAP — hand flies in from offscreen, impacts at face Y level
# ============================================================
# HJ slap transforms (HJ images are full-frame 1920x1080)
transform hj_slap_right_in:
    subpixel True
    pos (0, 0)
    xoffset 1920
    yoffset -124
    alpha 1.0
    easein 0.08 xoffset -180
    pause 0.15
    easeout 0.25 xoffset -1920 alpha 0.0

transform hj_slap_left_in:
    subpixel True
    pos (0, 0)
    xoffset -1920
    yoffset -84
    alpha 1.0
    easein 0.08 xoffset -180
    pause 0.15
    easeout 0.25 xoffset 1920 alpha 0.0

# BJ slap transforms (BJ images need to reach specific pixel positions)
transform bj_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.52
    alpha 1.0
    easein 0.08 xpos 0.40
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform bj_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.52
    alpha 1.0
    easein 0.08 xpos 0.60
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0

transform bj_slap_shake:
    xoffset 0
    easein 0.03 xoffset 12
    easeout 0.03 xoffset -10
    easein 0.03 xoffset 8
    easeout 0.03 xoffset -5
    easein 0.02 xoffset 3
    easeout 0.02 xoffset 0

# ============================================================
# Apply speed
# ============================================================
label BJ_ApplySpeed(girl, speed=1):

    $ store.bj_speed = speed
    $ store._bj_head_normal = False
    $ penis_img = "%s bj_penis" % girl.gid

    python:
        # Enforce invariant: torso 3 ↔ hiding face must stay in sync
        if store.hiding_face and store.bj_torso_type != 3:
            print("[BJ_APPLY_SPEED] hiding_face OVERRIDE: torso_type %d -> 3 (saving pre_hide=%d)" % (store.bj_torso_type, store.bj_torso_type))
            store._bj_pre_hide_torso = store.bj_torso_type
            store.bj_torso_type = 3
        elif not store.hiding_face and store.bj_torso_type == 3:
            _restore = getattr(store, '_bj_pre_hide_torso', _gsc(girl.gid, 'default_torso_type', 1, pose='blowjob'))
            print("[BJ_APPLY_SPEED] hiding_face RESTORE: torso_type 3 -> %d" % _restore)
            store.bj_torso_type = _restore

        slot_transform = bj_get_slot_transform(speed)
        head_transform = bj_get_head_transform(speed)

        if store.hiding_face:
            _hide_slot = {0: bj_slot_hide_speed0, 1: bj_slot_hide_speed1, 2: bj_slot_hide_speed2, 3: bj_slot_hide_speed3}
            slot_transform = _hide_slot.get(speed, _hide_slot[1])

        # Expressao: reseta no idle, muda com 70% de chance ao trocar velocidade
        # Witness lock: manter expressao definida pelo witness event
        if not getattr(store, "_witness_expression_lock", False):
            if speed == 0:
                store.bj_eyes  = "normal"
                store.bj_brows = 1
            elif renpy.random.random() < 0.70:
                store.bj_eyes  = renpy.random.choice(BJ_EYES_BY_SPEED.get(speed, ["normal"]))
                store.bj_brows = renpy.random.choice(BJ_BROWS_BY_SPEED.get(speed, [1]))
        # Tenny forcing: Jaw 1 (open). Suck speed>=1: Jaw 2 (sucking). Otherwise: Jaw 1.
        if store.bj_forcing and girl.gid == "tenny":
            jaw_attr = "jaw_1"
        elif bj_action == "suck" and speed >= 1:
            jaw_attr = "jaw_2"
        else:
            jaw_attr = "jaw_1"
        jaw_img = "%s blowjob_jaw %s" % (girl.gid, jaw_attr)

        attrs = _build_attributes_for_girl(girl, pose="blowjob")
        img_name = "%s blowjob" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)

        print("[BJ_ApplySpeed] gid=%s speed=%d action=%s jaw=%s head_mouth=%s sucking=%s cheeks=%s blush=%s torso=%d hiding=%s" % (
            girl.gid, speed, bj_action, jaw_attr,
            (bj_idle_mouth if speed == 0 else ("mouth_tongue" if bj_action == "lick" else "mouth_sucking")),
            ("ON" if bj_has_sucking_mouth(girl) and bj_action == "suck" and speed > 0 else "OFF"),
            bj_cheeks, _ssg(girl.gid, 'blush', 0), bj_torso_type, hiding_face
        ))

        _pov_bj = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
        # Standard:  corpo(9980) < jaw(9984) < penis(9990/10020) < head(10015) < hand(10040) < forcing(10045) < guy(10050) < slap(10070)
        # POV:       corpo(9980) < jaw(9984) < guy(10050) < right_arm(10051) < arm(10052) < penis(10055) < hand(10057) < head(10058)

        # Guy (fixo, ACIMA de tudo)
        _guy_img = "%s bj_guy" % girl.gid
        if renpy.has_image(_guy_img):
            renpy.show(_guy_img, tag="bj_guy", at_list=[bj_guy_static], zorder=10050)
        else:
            renpy.hide("bj_guy")

        # Corpo da girl (layeredimage)
        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=[slot_transform],
            zorder=9980
        )

        # Jaw — Tenny forcing: 9979 (below girl+player body). Normal: 9984.
        _jaw_z = 9979 if (store.bj_forcing and girl.gid == "tenny") else 9984
        renpy.show(
            jaw_img,
            tag="%s_bj_jaw" % girl.gid,
            at_list=[head_transform],
            zorder=_jaw_z
        )

        # Face cum under (9986) — parte do cum abaixo do penis, acima do jaw
        _cum_under_img = "%s bj_cum_face_under" % girl.gid
        if renpy.has_image(_cum_under_img):
            renpy.show(
                _cum_under_img,
                tag="%s_bj_cum_face_under" % girl.gid,
                at_list=[head_transform],
                zorder=9986
            )

        # Head (10015) — mouth sempre explicito para evitar attribute-retention do Ren'Py
        # speed=0 (idle)  -> bj_idle_mouth (boca baseada no estado anterior do personagem)
        # lick speed>=1   -> mouth_tongue (Jaw 1 + boca visivel, penis na frente via zorder)
        # suck speed>=1   -> mouth_sucking (Null no layeredimage; sucking layer separado zorder 10030)
        head_img = "%s blowjob_head" % girl.gid

        if store.bj_forcing and girl.gid == "tenny":
            head_img += " head_deepthroat_full_bottom"
            head_img += " mouth_none"
        else:
            # the variant is explicit (the tag keeps head_normal from speed 0: attribute retention)
            head_img += " " + _bj_head_variant(girl.gid, speed)
            if speed == 0:
                head_img += " " + bj_idle_mouth
            elif bj_action == "lick":
                head_img += " mouth_tongue"
            elif bj_action == "suck":
                head_img += " mouth_sucking"
            else:
                head_img += " mouth_tongue"
        # cheeks_sucking e controlado dinamicamente via ConditionSwitch no layeredimage
        # (thread _bj_cheeks_cycle alterna bj_cheeks; ConditionSwitch re-avalia por frame)
        print("[BJ_HEAD_SHOW] head_img='%s' tag='%s_bj_head' z=%d eyes=%s brows=%s" % (
            head_img, girl.gid, (10058 if _pov_bj else 10015), store.bj_eyes, store.bj_brows))
        renpy.show(
            head_img,
            tag="%s_bj_head" % girl.gid,
            at_list=[head_transform],
            zorder=10058 if _pov_bj else 10015
        )

        # Sucking mouth — layer independente, zorder maximo (10030).
        # Hide SEMPRE (incondicional) para limpar qualquer residuo.
        renpy.hide("%s_bj_sucking_mouth" % girl.gid)
        if bj_has_sucking_mouth(girl):
            if bj_action == "suck" and speed > 0 and not (store.bj_forcing and girl.gid == "tenny"):
                renpy.show(
                    "%s bj_sucking_mouth" % girl.gid,
                    tag="%s_bj_sucking_mouth" % girl.gid,
                    at_list=[head_transform],
                    zorder=10061 if _pov_bj else 10030
                )

        # Arm e Hand do torso 2
        # Standard: right_arm(9973) < body(9980) < arm(9982) < jaw(9984) < penis(9990/10020) < hand(10040)
        # POV:      body(9980) < guy(10050) < right_arm(10051) < arm(10052) < head(10058) < penis(10059) < hand(10060) < suck_mouth(10061) < forcing(10063) < slap(10070)
        print("[BJ_APPLY_ARMS] gid=%s has_torso2=%s torso_type=%d forcing=%s" % (girl.gid, bj_has_torso2(girl), bj_torso_type, store.bj_forcing))
        if bj_has_torso2(girl):
            if bj_torso_type == 2:
                renpy.hide("%s_bj_back_arm_left" % girl.gid)
                renpy.hide("%s_bj_back_arm_right" % girl.gid)
                if _pov_bj:
                    # POV: arms follow body + rotate, hands animate up/down
                    if bj_action == "lick":
                        _arm_right_map = {1: bj_pov_arm_right_lick_speed1, 2: bj_pov_arm_right_lick_speed2, 3: bj_pov_arm_right_lick_speed3}
                        _arm_left_map = {1: bj_pov_arm_left_lick_speed1, 2: bj_pov_arm_left_lick_speed2, 3: bj_pov_arm_left_lick_speed3}
                    else:
                        _arm_right_map = {1: bj_pov_arm_right_speed1, 2: bj_pov_arm_right_speed2, 3: bj_pov_arm_right_speed3}
                        _arm_left_map = {1: bj_pov_arm_left_speed1, 2: bj_pov_arm_left_speed2, 3: bj_pov_arm_left_speed3}

                    if renpy.has_image("%s bj_right_arm" % girl.gid):
                        _at_r = [slot_transform]
                        if speed in _arm_right_map:
                            _at_r.append(_arm_right_map[speed]())
                        renpy.show(
                            "%s bj_right_arm" % girl.gid,
                            tag="%s_bj_right_arm" % girl.gid,
                            at_list=_at_r,
                            zorder=10051
                        )
                    if renpy.has_image("%s bj_arm" % girl.gid):
                        _at_l = [slot_transform]
                        if speed in _arm_left_map:
                            _at_l.append(_arm_left_map[speed]())
                        renpy.show(
                            "%s bj_arm" % girl.gid,
                            tag="%s_bj_arm" % girl.gid,
                            at_list=_at_l,
                            zorder=10052
                        )
                    if bj_action == "lick":
                        _pov_h = {0: bj_pov_hand_static, 1: bj_pov_hand_lick_speed1, 2: bj_pov_hand_lick_speed2, 3: bj_pov_hand_lick_speed3}.get(speed, bj_pov_hand_lick_speed1)
                    else:
                        _pov_h = {0: bj_pov_hand_static, 1: bj_pov_hand_speed1, 2: bj_pov_hand_speed2, 3: bj_pov_hand_speed3}.get(speed, bj_pov_hand_speed1)
                    renpy.show(
                        "%s bj_hand" % girl.gid,
                        tag="%s_bj_hand" % girl.gid,
                        at_list=[_pov_h],
                        zorder=10060
                    )
                else:
                    # Standard: arms/hands rotate
                    _arm_t_fn = {1: bj_arm_speed1, 2: bj_arm_speed2, 3: bj_arm_speed3}.get(speed, bj_arm_speed1)
                    _hand_t = _arm_t_fn()
                    if renpy.has_image("%s bj_right_arm" % girl.gid):
                        renpy.show(
                            "%s bj_right_arm" % girl.gid,
                            tag="%s_bj_right_arm" % girl.gid,
                            at_list=[slot_transform],
                            zorder=9973
                        )
                    if renpy.has_image("%s bj_arm" % girl.gid):
                        renpy.show(
                            "%s bj_arm" % girl.gid,
                            tag="%s_bj_arm" % girl.gid,
                            at_list=[slot_transform, _arm_t_fn()],
                            zorder=9982
                        )
                    renpy.show(
                        "%s bj_hand" % girl.gid,
                        tag="%s_bj_hand" % girl.gid,
                        at_list=[slot_transform, _hand_t],
                        zorder=10040
                    )
            elif bj_torso_type == 4:
                print("[BJ_APPLY_ARMS] torso_type==4: hiding front arms, showing back arms for %s" % girl.gid)
                renpy.hide("%s_bj_right_arm" % girl.gid)
                renpy.hide("%s_bj_arm" % girl.gid)
                renpy.hide("%s_bj_hand" % girl.gid)
                _gid_ba = girl.gid
                _ba_l_img = "%s bj_back_arm_left" % _gid_ba
                _ba_r_img = "%s bj_back_arm_right" % _gid_ba
                _ba_l_has = renpy.has_image(_ba_l_img)
                _ba_r_has = renpy.has_image(_ba_r_img)
                print("[BJ_APPLY_ARMS] back_arm_left='%s' has=%s | back_arm_right='%s' has=%s | slot_transform=%s" % (_ba_l_img, _ba_l_has, _ba_r_img, _ba_r_has, slot_transform))
                if _ba_l_has:
                    renpy.show(
                        _ba_l_img,
                        tag="%s_bj_back_arm_left" % _gid_ba,
                        at_list=[slot_transform],
                        zorder=9970
                    )
                    print("[BJ_APPLY_ARMS] showed back_arm_left z=9970")
                if _ba_r_has:
                    renpy.show(
                        _ba_r_img,
                        tag="%s_bj_back_arm_right" % _gid_ba,
                        at_list=[slot_transform],
                        zorder=9970
                    )
                    print("[BJ_APPLY_ARMS] showed back_arm_right z=9970")
            else:
                renpy.hide("%s_bj_right_arm" % girl.gid)
                renpy.hide("%s_bj_arm" % girl.gid)
                renpy.hide("%s_bj_hand" % girl.gid)
                renpy.hide("%s_bj_back_arm_left" % girl.gid)
                renpy.hide("%s_bj_back_arm_right" % girl.gid)

        # Forcing hands — shown when bj_forcing is active and speed >= 1
        _gid = girl.gid
        _forcing_z = 10100 if _pov_bj else 10080
        if store.bj_forcing and speed >= 1:
            _hand_disabled = getattr(store, "_player_hand_disabled", None)
            _slap_hide = getattr(store, "_slap_hide_hand", None)
            _f_left = "%s bj_forcing_hands_left" % _gid
            if renpy.has_image(_f_left):
                for _side in ("left", "right"):
                    _f_img = "%s bj_forcing_hands_%s" % (_gid, _side)
                    _f_tag = "%s_bj_forcing_%s" % (_gid, _side)
                    if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_f_img):
                        renpy.show(_f_img, tag=_f_tag, at_list=[head_transform], zorder=_forcing_z)
                    else:
                        renpy.hide(_f_tag)
            else:
                _f_img = "%s bj_forcing_hands" % _gid
                if renpy.has_image(_f_img):
                    renpy.show(_f_img, tag="%s_bj_forcing_left" % _gid, at_list=[head_transform], zorder=_forcing_z)
                renpy.hide("%s_bj_forcing_right" % _gid)
        else:
            renpy.hide("%s_bj_forcing_left" % _gid)
            renpy.hide("%s_bj_forcing_right" % _gid)

        # Hide-face hands — shown when hiding_face is active (above head)
        if store.hiding_face:
            _hf_z = 10061 if _pov_bj else 10035
            for _side in ("left", "right"):
                _hf_img = "%s bj_hide_hand_%s" % (_gid, _side)
                _hf_tag = "%s_bj_hide_%s" % (_gid, _side)
                if renpy.has_image(_hf_img):
                    renpy.show(_hf_img, tag=_hf_tag, at_list=[slot_transform], zorder=_hf_z)
                else:
                    renpy.hide(_hf_tag)
        else:
            renpy.hide("%s_bj_hide_left" % _gid)
            renpy.hide("%s_bj_hide_right" % _gid)

        # Penis guy layer — above body (9980), below arm_torso2 (9982)
        _penis_guy_img = "%s bj_penis_guy" % girl.gid
        if renpy.has_image(_penis_guy_img):
            renpy.show(_penis_guy_img, tag="bj_penis_guy", at_list=[_bj_get_penis_tf(girl)], zorder=9981)
        else:
            renpy.hide("bj_penis_guy")

        # Penis z-order
        if _pov_bj:
            penis_z = 10059 if bj_action == "lick" else 10055
        elif store.bj_forcing:
            penis_z = 9990
        else:
            penis_z = 9990 if (bj_action == "suck" and speed >= 1) else 10020
        print("[BJ_APPLY_SPEED] penis z=%d (pov=%s, action=%s, speed=%d, forcing=%s)" % (penis_z, _pov_bj, bj_action, speed, store.bj_forcing))
        renpy.show(
            penis_img,
            tag="bj_penis",
            at_list=[_bj_get_penis_tf(girl)],
            zorder=penis_z
        )

        # Face cum overlay — zorder 10025 para ficar ACIMA do penis (10020).
        # ConditionSwitch dentro da image avalia girl.Cum por frame.
        _cum_face_img = "%s bj_cum_face" % girl.gid
        if renpy.has_image(_cum_face_img):
            renpy.show(
                _cum_face_img,
                tag="%s_bj_cum_face" % girl.gid,
                at_list=[head_transform],
                zorder=10059 if _pov_bj else 10025
            )

        # Mouth cum — zorder 9988: abaixo do penis suck (9990), abaixo da head (10015).
        _cum_mouth_img = "%s bj_cum_mouth" % girl.gid
        if renpy.has_image(_cum_mouth_img):
            renpy.show(
                _cum_mouth_img,
                tag="%s_bj_cum_mouth" % girl.gid,
                at_list=[head_transform],
                zorder=9988
            )

    return

# ============================================================
# BJ_ForceRise — centralized rise from force position
# Called by: Release her head, BJ_CumAnim (cum outside while forcing)
# ============================================================
label BJ_ForceRise(girl):
    python:
        _gid = girl.gid
        _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        print("[BJ_RISE] === START === gid=%s pov=%s" % (_gid, _is_pov))

        store._bj_use_half_penis = False

        renpy.hide("%s_bj_sucking_mouth" % _gid)
        renpy.hide("%s_bj_right_arm" % _gid)
        renpy.hide("%s_bj_arm" % _gid)
        renpy.hide("%s_bj_hand" % _gid)

        if _gid != "tenny":
            renpy.hide("%s_bj_forcing_left" % _gid)
            renpy.hide("%s_bj_forcing_right" % _gid)

        _head_rise = getattr(renpy.store, "%s_bj_head_force_rise" % _gid, None)
        _slot_rise = getattr(renpy.store, "%s_bj_slot_force_rise" % _gid, None)

    if _head_rise and _slot_rise:
        python:
            _attrs = _build_attributes_for_girl(girl, pose="blowjob")
            _body_img = "%s blowjob" % _gid
            if _attrs:
                _body_img += " " + " ".join(_attrs)
            renpy.show(_body_img, tag=_gid, at_list=[_slot_rise], zorder=9980)

            if _gid == "tenny":
                _rise_head = "%s blowjob_head head_base" % _gid
            else:
                _rise_head = "%s blowjob_head mouth_sad" % _gid
            renpy.show(_rise_head, tag="%s_bj_head" % _gid, at_list=[_head_rise], zorder=10058 if _is_pov else 10015)

            renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head_rise], zorder=9984)

            # Cum layers follow head
            _cum_face_z = 10059 if _is_pov else 10025
            for _suffix, _z in [("bj_cum_face", _cum_face_z), ("bj_cum_face_under", 9986), ("bj_cum_mouth", 9988)]:
                _img = "%s %s" % (_gid, _suffix)
                if renpy.has_image(_img):
                    renpy.show(_img, tag="%s_%s" % (_gid, _suffix), at_list=[_head_rise], zorder=_z)

            if _gid == "tenny":
                _fd_z = 10100 if _is_pov else 10080
                for _side in ("left", "right"):
                    _f_img = "%s bj_forcing_hands_%s" % (_gid, _side)
                    _f_tag = "%s_bj_forcing_%s" % (_gid, _side)
                    if renpy.has_image(_f_img):
                        renpy.show(_f_img, tag=_f_tag, at_list=[_head_rise], zorder=_fd_z)

            for _side_name in ("left", "right"):
                _ba = "%s bj_back_arm_%s" % (_gid, _side_name)
                if renpy.has_image(_ba):
                    renpy.show(_ba, tag="%s_bj_back_arm_%s" % (_gid, _side_name), at_list=[_slot_rise], zorder=9970)

        $ renpy.pause(0.8, hard=True)

        python:
            renpy.hide("%s_bj_forcing_left" % _gid)
            renpy.hide("%s_bj_forcing_right" % _gid)
            print("[BJ_RISE] rise animation done")
    else:
        python:
            renpy.hide("%s_bj_forcing_left" % _gid)
            renpy.hide("%s_bj_forcing_right" % _gid)
            print("[BJ_RISE] no rise transforms found")

    python:
        store.bj_forcing = False
        store._bj_use_half_penis = False
        if _gid == "tenny":
            store.bj_torso_type = 4
            store.bj_idle_mouth = "mouth_none"
        else:
            store.bj_torso_type = getattr(store, '_bj_pre_force_torso', _gsc(_gid, 'default_torso_type', 1, pose='blowjob'))
        print("[BJ_RISE] post: forcing=%s torso=%d" % (store.bj_forcing, store.bj_torso_type))
    return

# ============================================================
# BJ Cum Animation — shared for ALL cum types during BJ
# forced=True shows forcing hands (Cum in her mouth)
# ============================================================
label BJ_CumAnim(girl, forced=False):
    $ debug_log("[DEBUG] BJ_CumAnim: entered, forced=%s forcing=%s" % (forced, store.bj_forcing))
    # Save state for resume
    $ store._bj_prev_speed = store.bj_speed
    $ store._bj_prev_action = store.bj_action
    # Capture arm/force state at entry so the forced-cum tail can restore the
    # player's real torso (e.g. "use her arms" = 2) instead of a stale pre-force value.
    $ store._bj_cum_entry_torso = store.bj_torso_type
    $ store._bj_cum_entry_forcing = store.bj_forcing

    # Rise from force position first (smooth transition, not snap)
    if store.bj_forcing and not forced:
        call BJ_ForceRise(girl) from _call_BJ_ForceRise_cum

    # Stop everything first (speed 0, tongue out)
    $ store.bj_speed = 0
    $ store.bj_action = "lick"
    $ store.bj_idle_mouth = "mouth_tongue"
    if store.hiding_face:
        $ store.hiding_face = False
        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_unhide
        if getattr(store, "_recording_active", False):
            $ Say_Line(girl, _("Wait, stop recording!"))
            $ finalize_recording()
    call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_cum_stop

    # Expression: eyes + brows change based on trait (forced = surprised)
    python:
        _bj_forced_surprise = forced or getattr(store, '_cum_forced_surprise', False)
        if _bj_forced_surprise and not (girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex")):
            _cum_eyes = "surprised"
            store.bj_brows = "brows_surprised"
            store._cum_forced_surprise = False
        elif girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex"):
            _cum_eyes = renpy.random.choice([_("up_right_closed"), "right_closed", "ahegao_2"])
        elif girl.has_trait("hate_cum"):
            _cum_eyes = renpy.random.choice(["squint", "squint_2", _("closed_happy")])
        else:
            _cum_eyes = renpy.random.choice([_("surprised"), "left_closed", "right_closed", "squint"])
        store.bj_eyes = _cum_eyes
        renpy.restart_interaction()

    # POV cum-in-mouth: head_normal at lower z, custom arm/hand cum transforms
    python:
        _pov_cum = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
        if _pov_cum and not forced:
            _gid = girl.gid
            store.bj_torso_type = 2
            store._bj_head_normal = True
            _head_tf = bj_get_head_transform(0)
            _slot_tf = bj_get_slot_transform(0)
            renpy.show(
                "%s blowjob_head head_normal mouth_tongue" % _gid,
                tag="%s_bj_head" % _gid,
                at_list=[_head_tf],
                zorder=10035
            )
            if renpy.has_image("%s bj_right_arm" % _gid):
                renpy.show(
                    "%s bj_right_arm" % _gid,
                    tag="%s_bj_right_arm" % _gid,
                    at_list=[_slot_tf, bj_cum_arm_right()],
                    zorder=10051
                )
            if renpy.has_image("%s bj_arm" % _gid):
                renpy.show(
                    "%s bj_arm" % _gid,
                    tag="%s_bj_arm" % _gid,
                    at_list=[_slot_tf, bj_cum_arm_left()],
                    zorder=10052
                )
            renpy.show(
                "%s bj_hand" % _gid,
                tag="%s_bj_hand" % _gid,
                at_list=[bj_cum_hand],
                zorder=10060
            )
            print("[BJ_CUM_ANIM] POV: head_normal z=10035, arms cum transforms, hand cum")

    # Penis pulse animation
    python:
        _penis_cum_z = 10055 if (_pov_cum and not forced) else 10031
        print("[BJ_CUM_ANIM] penis cum_pulse z=%d, pov=%s, forced=%s" % (_penis_cum_z, _pov_cum, forced))
        renpy.show("%s bj_penis" % girl.gid, tag="bj_penis", at_list=[_bj_get_penis_cum_tf(girl)], zorder=_penis_cum_z)

    # Cum in mouth (forced): she keeps sucking at speed 3 + forcing hands
    if forced:
        $ store.bj_speed = 3
        $ store.bj_action = "suck"
        call BJ_ApplySpeed(girl, 3) from _call_BJ_ApplySpeed_cum_forced
        python:
            store.bj_eyes = _cum_eyes
            renpy.restart_interaction()
        python:
            _hand_disabled = getattr(store, "_player_hand_disabled", None)
            _gid = girl.gid
            _force_tf = bj_get_head_transform(3)
            _cf_z = 10100 if _gsc(_gid, 'pov_overlay', False, pose='blowjob') else 10080
            _f_left = "%s bj_forcing_hands_left" % _gid
            if renpy.has_image(_f_left):
                for _side in ("left", "right"):
                    _f_img = "%s bj_forcing_hands_%s" % (_gid, _side)
                    _f_tag = "%s_bj_forcing_%s" % (_gid, _side)
                    if _hand_disabled != _side and renpy.has_image(_f_img):
                        renpy.show(_f_img, tag=_f_tag, at_list=[_force_tf], zorder=_cf_z)
                    else:
                        renpy.hide(_f_tag)
            else:
                _f_img = "%s bj_forcing_hands" % _gid
                if renpy.has_image(_f_img):
                    renpy.show(_f_img, tag="%s_bj_forcing_left" % _gid, at_list=[_force_tf], zorder=_cf_z)
                renpy.hide("%s_bj_forcing_right" % _gid)

    python:
        _wg_check = getattr(store, "_witness_girl", None)
        _wg_gid_check = getattr(_wg_check, "gid", None) if _wg_check else None
        print("[BJ_CUM_ANIM] PRE-SHAKE witness=%s showing=%s rec_watcher=%s" % (
            _wg_gid_check,
            renpy.showing(_wg_gid_check) if _wg_gid_check else "N/A",
            getattr(store, "_recording_watcher_gid", None)))

    call _cum_punch_pair("oral") from _call_cum_punch_bj_cum

    python:
        if _wg_gid_check:
            print("[BJ_CUM_ANIM] POST-SHAKE witness=%s showing=%s" % (
                _wg_gid_check, renpy.showing(_wg_gid_check)))

    # Restore penis to static transform (above mouth since not sucking)
    $ store._bj_use_half_penis = False
    python:
        _penis_restore_z = 10055 if (_pov_cum and not forced) else 10020
        print("[BJ_CUM_ANIM] penis restore z=%d" % _penis_restore_z)
        renpy.show("%s bj_penis" % girl.gid, tag="bj_penis", at_list=[_bj_get_penis_tf(girl)], zorder=_penis_restore_z)

    # Hide forcing hands + stop to idle
    $ renpy.hide("%s_bj_forcing_left" % girl.gid)
    $ renpy.hide("%s_bj_forcing_right" % girl.gid)
    if forced:
        # Finalize ALL state (speed/action/forcing/torso) BEFORE ApplySpeed so the
        # arm layers are reconciled in a single pass. Previously torso_type was set
        # AFTER ApplySpeed, leaving the standalone arm/hand (torso 2) shown on top of
        # a torso-1 body -> duplicated arm during the swallow menu.
        python:
            store.bj_speed = 0
            store.bj_action = "lick"
            store.bj_forcing = False
            if girl.gid == "tenny":
                store.bj_torso_type = 4
            elif getattr(store, "_bj_cum_entry_forcing", False):
                # Head was being forced -> restore the torso saved before the force
                store.bj_torso_type = getattr(store, '_bj_pre_force_torso', _gsc(girl.gid, 'default_torso_type', 1, pose='blowjob'))
            else:
                # No head-force: keep the player's arm choice (e.g. "use her arms" = 2)
                store.bj_torso_type = getattr(store, '_bj_cum_entry_torso', store.bj_torso_type)
            print("[BJ_CUM_ANIM] forced tail: torso_type=%d entry_torso=%s entry_forcing=%s" % (store.bj_torso_type, getattr(store, '_bj_cum_entry_torso', '?'), getattr(store, '_bj_cum_entry_forcing', '?')))
        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_cum_forced_stop

    # Signal BJ_ActionMenu to return to BJ_ControlMenu
    $ store._bj_cum_done = True

    return

# ============================================================
# Launch
# ============================================================
label BJ_Launch(girl, start_speed=0):
    $ sub_event_reset(girl)
    $ debug_log("[DEBUG] BJ_Launch: entered")
    $ _kill_scene_threads()
    $ stop_standing_blink(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _hide_all_scene_layers(girl)
        store._bj_girl     = girl
        store.bj_action    = "suck"
        store.bj_speed     = start_speed
        store.bj_cheeks    = False
        store.bj_blink     = False
        store.bj_eyes      = "normal"
        store.bj_brows     = 1
        store.bj_torso_type = _gsc(girl.gid, 'default_torso_type', 1, pose='blowjob')
        store.hiding_face = False
        store._bj_face_ordered_shown = False
        store.bj_idle_mouth = _bj_initial_mouth_for_girl(girl)
        store._slap_count = 0
        store.bj_forcing   = False
        store._bj_use_half_penis = False
        store._bj_force_obed_given = False
        if not store._bj_cheeks_running:
            renpy.invoke_in_thread(_bj_cheeks_cycle)
        if not store._bj_blink_running:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_bj_girl", "bj_blink", blink_timing=(0.10, 0.20), running_var="_bj_blink_running")

    call BJ_ApplySpeed(girl, start_speed) from _call_BJ_ApplySpeed
    with fade
    return

# ============================================================
# Control Menu
# ============================================================
label BJ_ControlMenu(girl):
    $ debug_log("[DEBUG] BJ_ControlMenu: entered")
    $ store._player_exhausted = False
    if "bj_action" not in globals():
        $ bj_action = "lick"
    if "bj_speed" not in globals():
        $ bj_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            call _moan_say(girl, _scene_time_up_line()) from _call_ms_bj_timeout_ctrl
            call BJ_End(girl, dress_up=False) from _call_BJ_End_timeout_ctrl
            return

        menu:
            "Lick it":
                python:
                    _bj_hide_all(girl)
                    _bj_reset_state(girl)
                $ bj_action = "lick"
                $ bj_speed  = 1
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_1
                "She starts licking."
                if getattr(store, "_atm_cum_in_mouth", False) and not getattr(store, "_atm_tease_played", False):
                    python:
                        _atm_src = getattr(store, "_atm_source_gid", None)
                        _atm_is_cross = _atm_src is not None and _atm_src != girl.gid
                    if _atm_is_cross:
                        python:
                            _atm_sn = GIRL_BY_ID.get(_atm_src)
                            _atm_sn = _atm_sn.Name if _atm_sn else "her"
                            _atm_react = renpy.random.choice([
                                _tl(_("Wait... you're putting it in my mouth after it was in %s's...?")) % _atm_sn,
                                _tl(_("Oh god... I can taste... this was just in %s...")) % _atm_sn,
                            ])
                            _atm_react = atm_cross_override(girl, "react", _atm_react)   # her own voice / traits (Dialogs/atm_cross.rpy)
                        call _moan_say(girl, _atm_react) from _call_ms_bj_atm_cross
                    else:
                        $ _atm_react = scene_pick_line("atm_react", scene="bj", girl=girl)
                        if _atm_react:
                            call _moan_say(girl, _atm_react) from _call_ms_bj_atm
                    $ store._atm_tease_played = True
                call BJ_ActionMenu(girl) from _call_BJ_ActionMenu
                if _scene_should_exit() or store._bj_girl is None:
                    return

            "Suck it":
                python:
                    _bj_hide_all(girl)
                    _bj_reset_state(girl)
                $ bj_action = "suck"
                $ bj_speed  = 1
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_2
                "She starts sucking."
                if getattr(store, "_atm_cum_in_mouth", False) and not getattr(store, "_atm_tease_played", False):
                    python:
                        _atm_src = getattr(store, "_atm_source_gid", None)
                        _atm_is_cross = _atm_src is not None and _atm_src != girl.gid
                    if _atm_is_cross:
                        python:
                            _atm_sn = GIRL_BY_ID.get(_atm_src)
                            _atm_sn = _atm_sn.Name if _atm_sn else "her"
                            _atm_react = renpy.random.choice([
                                _tl(_("Wait... you're putting it in my mouth after it was in %s's...?")) % _atm_sn,
                                _tl(_("Oh god... I can taste... this was just in %s...")) % _atm_sn,
                            ])
                            _atm_react = atm_cross_override(girl, "react", _atm_react)   # her own voice / traits (Dialogs/atm_cross.rpy)
                        call _moan_say(girl, _atm_react) from _call_ms_bj_atm_cross2
                    else:
                        $ _atm_react = scene_pick_line("atm_react", scene="bj", girl=girl)
                        if _atm_react:
                            call _moan_say(girl, _atm_react) from _call_ms_bj_atm2
                    $ store._atm_tease_played = True
                call BJ_ActionMenu(girl) from _call_BJ_ActionMenu_1
                if _scene_should_exit() or store._bj_girl is None:
                    return

            "Tease her..." if bj_speed > 0 and not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call _tease_menu(girl, "bj") from _call_tease_menu_bj

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call BJ_StripMenu(girl) from _call_BJ_StripMenu

            "Record Options..." if (bj_action != "lick" and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False)) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _sex_phone_menu(girl, "bj") from _call__sex_phone_menu
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "bj") from _call_watcher_rec_start_bj_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "bj") from _call_watcher_rec_start_bj_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ _rec_stop_name = _get_recording_stopper_name()
                        $ finalize_recording()
                        if store.hiding_face:
                            $ store.hiding_face = False
                        if _rec_stop_name:
                            $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                            "[_rec_stop_text]"
                        else:
                            "You stop recording."
                    "Order her to show her face" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        $ store._bj_face_ordered_shown = True
                        "You tell her to show her face."
                    "Back":
                        pass
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_rec_opts

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "bj") from _call__player_stops_forced_bj
                else:
                    # on the edge she pleads (or orders him back): "Let her have it" keeps the menu going
                    call _scene_stop_reaction(girl) from _call_scene_stop_reaction_bj
                    if store._stop_accepted:
                        call BJ_End(girl, dress_up=False) from _call_BJ_End
                        return

# ============================================================
# Slap
# ============================================================
label BJ_Slap(girl):
    call SexScene_Slap(girl, "bj") from _call_SexScene_Slap_bj
    return

label BJ_ActionMenu(girl):

    while True:

        # After cum, resume in the action menu instead of bouncing to ControlMenu.
        # Paths that restore bj_speed (cum_slut, mouth_cum_reaction "Keep going")
        # already called BJ_ApplySpeed — just clear the flag and stay here.
        # Paths that left speed at 0 (forced swallow, bite aftermath) drop to slow.
        if getattr(store, "_bj_cum_done", False):
            $ store._bj_cum_done = False
            if bj_speed < 1:
                $ bj_speed = 1
                $ bj_action = getattr(store, "_bj_prev_action", "suck") or "suck"
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_cum_resume

        if Round >= 100:
            call _moan_say(girl, _scene_time_up_line()) from _call_ms_bj_timeout_act
            call BJ_End(girl, dress_up=False) from _call_BJ_End_timeout_act
            return

        menu:
            "Keep going" if bj_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                if bj_action == "lick":
                    $ add_player_focus(get_player_lust_gain("bj_lick", bj_speed))
                    $ _girl_lust_gain(girl, 1, bj_speed)
                else:
                    $ add_player_focus(get_player_lust_gain("bj_suck", bj_speed))
                    $ _girl_lust_gain(girl, (2 if bj_speed == 1 else 3 if bj_speed == 2 else 5), bj_speed)
                $ _moan = scene_moan_tick(girl, "bj", bj_speed)
                if _moan:
                    call _moan_say(girl, _moan, muffled=True) from _call_ms_bj_kg

                # Public attention
                $ _pa_caught = public_attention_tick(girl, "keep_going", bj_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call BJ_End(girl, dress_up=False) from _call_BJ_End_pa
                    call caught_in_public(girl, "bj") from _call_caught_public_bj_kg
                    return

                # Random interruption check
                call _sex_interruption_check(girl, "bj") from _call__sex_interruption_check
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call BJ_End(girl, dress_up=False) from _call_BJ_End_1
                    return

                call _npc_partner_detection_tick(girl, "bj") from _call_npc_detect_bj
                if store._npc_witness_scene_aborted:
                    call BJ_End(girl, dress_up=False) from _call_BJ_End_npc
                    return

                call _sub_event_tick_nonpen(girl, "bj") from _call_se_np_bj
                if store._sst_result == "abort":
                    call BJ_End(girl, dress_up=False) from _call_BJ_End_se
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "bj", "blowjob") from _call_GirlCumming_2
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "bj") from _call_ForcedCumOverdue_bj_kg
                        if getattr(store, "_bj_mouth_cum_continued", False):
                            $ store._bj_mouth_cum_continued = False
                            $ debug_log("[DEBUG] BJ_ActionMenu: forced overdue mouth cum continue (kg)")
                        else:
                            $ _pce = _handle_post_cum_exit("bj", "sex")
                            if _pce == "hate_abort":
                                call BJ_End(girl, dress_up=False) from _call_BJ_End_hate_cum
                            return

            "Speed up" if bj_speed < 3 and bj_action == "suck":
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ bj_speed += 1
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_3
                $ add_player_focus(get_player_lust_gain("bj_suck", bj_speed))
                $ _girl_lust_gain(girl, (2 if bj_speed == 1 else 3 if bj_speed == 2 else 5), bj_speed)
                $ _moan = scene_moan_tick(girl, "bj", bj_speed)
                if _moan:
                    call _moan_say(girl, _moan, muffled=True) from _call_ms_bj_su
                # Public attention
                $ _pa_caught = public_attention_tick(girl, "speed_up", bj_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call BJ_End(girl, dress_up=False) from _call_BJ_End_pa2
                    call caught_in_public(girl, "bj") from _call_caught_public_bj_su
                    return
                if girl.Lust >= 100:
                    call GirlCumming(girl, "bj", "blowjob") from _call_GirlCumming_3
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "bj") from _call_ForcedCumOverdue_bj_su
                        if getattr(store, "_bj_mouth_cum_continued", False):
                            $ store._bj_mouth_cum_continued = False
                            $ debug_log("[DEBUG] BJ_ActionMenu: forced overdue mouth cum continue (su)")
                        else:
                            $ _pce = _handle_post_cum_exit("bj", "sex")
                            if _pce == "hate_abort":
                                call BJ_End(girl, dress_up=False) from _call_BJ_End_hate_cum_2
                            return
                "She speeds up her mouth."

            "Speed down" if bj_speed > 1 and bj_action == "suck":
                $ advance_round(1)
                $ bj_speed -= 1
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_4
                $ add_player_focus(10 if bj_speed == 1 else 20 if bj_speed >= 2 else 0)
                "She slows her movements."

            "Force her head" if not bj_forcing and not hiding_face and bj_action == "suck" and bj_speed >= 1 and not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                python:
                    if girl.has_trait("cute_sex"):
                        _can_force = (girl.Obed >= 600)
                    else:
                        _can_force = (girl.Obed >= 300 or girl.Inbt >= 300 or girl.Lust >= 300 or girl.has_trait("hardcore_sex"))
                if _can_force:
                    "You grab her head and push it down."
                    # Hide standalone arms/hands and show back arms BEFORE descent
                    python:
                        _gid = girl.gid
                        renpy.hide("%s_bj_right_arm" % _gid)
                        renpy.hide("%s_bj_arm" % _gid)
                        renpy.hide("%s_bj_hand" % _gid)
                        store._bj_pre_force_torso = store.bj_torso_type
                        _ba_slot_descent = getattr(renpy.store, "%s_bj_slot_force_descent" % _gid, bj_slot_force_descent)
                        if not store.hiding_face:
                            if bj_has_back_arms(girl):
                                store.bj_torso_type = 4
                                if renpy.has_image("%s bj_back_arm_left" % _gid):
                                    renpy.show(
                                        "%s bj_back_arm_left" % _gid,
                                        tag="%s_bj_back_arm_left" % _gid,
                                        at_list=[_ba_slot_descent],
                                        zorder=9970
                                    )
                                if renpy.has_image("%s bj_back_arm_right" % _gid):
                                    renpy.show(
                                        "%s bj_back_arm_right" % _gid,
                                        tag="%s_bj_back_arm_right" % _gid,
                                        at_list=[_ba_slot_descent],
                                        zorder=9970
                                    )
                            else:
                                store.bj_torso_type = 1
                    # Descend all head-attached layers into force depth
                    python:
                        _gid = girl.gid
                        _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
                        _attrs = _build_attributes_for_girl(girl, pose="blowjob")
                        _body_img = "%s blowjob" % _gid
                        if _attrs:
                            _body_img += " " + " ".join(_attrs)
                        _slot_descent = getattr(renpy.store, "%s_bj_slot_force_descent" % _gid, bj_slot_force_descent)
                        _head_descent = getattr(renpy.store, "%s_bj_head_force_descent" % _gid, bj_head_force_descent)
                        # Body
                        renpy.show(
                            _body_img,
                            tag=_gid,
                            at_list=[_slot_descent],
                            zorder=9980
                        )
                        # Head — Tenny keeps head_base during descent (full_bottom only at final position via BJ_ApplySpeed)
                        _descent_head = "%s blowjob_head" % _gid
                        if _gid == "tenny":
                            _descent_head += " head_base"
                        renpy.show(
                            _descent_head,
                            tag="%s_bj_head" % _gid,
                            at_list=[_head_descent],
                            zorder=10058 if _is_pov else 10015
                        )
                        renpy.show(
                            "%s blowjob_jaw jaw_1" % _gid,
                            tag="%s_bj_jaw" % _gid,
                            at_list=[_head_descent],
                            zorder=9984
                        )
                        # Sucking mouth
                        if bj_has_sucking_mouth(girl):
                            renpy.show(
                                "%s bj_sucking_mouth" % _gid,
                                tag="%s_bj_sucking_mouth" % _gid,
                                at_list=[_head_descent],
                                zorder=10061 if _is_pov else 10030
                            )
                        # Forcing hands (use same descent transform as head)
                        _fd_forcing_z = 10100 if _is_pov else 10080
                        _f_left = "%s bj_forcing_hands_left" % _gid
                        if renpy.has_image(_f_left):
                            for _side in ("left", "right"):
                                _f_img = "%s bj_forcing_hands_%s" % (_gid, _side)
                                _f_tag = "%s_bj_forcing_%s" % (_gid, _side)
                                if renpy.has_image(_f_img):
                                    renpy.show(_f_img, tag=_f_tag, at_list=[_head_descent], zorder=_fd_forcing_z)
                        else:
                            _f_img = "%s bj_forcing_hands" % _gid
                            if renpy.has_image(_f_img):
                                renpy.show(_f_img, tag="%s_bj_forcing_left" % _gid, at_list=[_head_descent], zorder=_fd_forcing_z)
                    $ renpy.pause(0.7, hard=True)
                    $ store.bj_forcing = True
                    $ store._bj_use_half_penis = (girl.gid == "tenny")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_force
                    $ add_player_focus(get_player_lust_gain("bj_suck", bj_speed))
                    $ _girl_lust_gain(girl, 5, bj_speed)
                    if not getattr(store, "_bj_force_obed_given", False):
                        $ Change_Status(girl, "Obed", 10)
                        $ store._bj_force_obed_given = True
                else:
                    python:
                        _force_deny_lines = [
                            _("Don't push my head like that!"),

                            _("Hey! I decide how deep I go, not you."),

                            _("Stop! You're not shoving my head down."),

                            _("I'll suck it MY way, don't force me."),

                            _("No! You don't get to do that."),

                        ]
                    python:
                        _saved_bj_force_speed = store.bj_speed
                        _saved_bj_force_mouth = store.bj_idle_mouth
                        store.bj_idle_mouth = "mouth_lipbite"
                    call BJ_ApplySpeed(girl, 0) from _call_BJ_AS_force_deny
                    python:
                        store.bj_eyes = "squint_2"
                        store.bj_brows = 4
                    $ Say_Line(girl, _tl(renpy.random.choice(_force_deny_lines)))
                    $ store.bj_idle_mouth = _saved_bj_force_mouth
                    call BJ_ApplySpeed(girl, _saved_bj_force_speed) from _call_BJ_AS_force_deny_restore
                    $ Change_Status(girl, "Obed", -5)
                    $ _girl_lust_gain(girl, -3, 0)

            "Release her head" if bj_forcing:
                $ advance_round(1)
                call BJ_ForceRise(girl) from _call_BJ_ForceRise_release
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_release
                $ _tenny_bj_post_apply_correct(girl, bj_speed, mouth="mouth_none") if girl.gid == "tenny" else None
                "You let go of her head."

            "Change Her Hands" if bj_has_torso2(girl) and bj_torso_type == 1 and not bj_forcing and not hiding_face:
                $ bj_torso_type = 2
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_5

            "Let go" if bj_has_torso2(girl) and not bj_has_back_arms(girl) and bj_torso_type == 2 and not bj_forcing and not hiding_face:
                $ advance_round(1)
                $ bj_torso_type = 1
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_6

            "Arms Behind Back" if bj_has_back_arms(girl) and bj_torso_type == 2 and not bj_forcing and not hiding_face:
                $ bj_torso_type = 4
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_back_arms

            "Use Her Hands" if bj_has_back_arms(girl) and bj_torso_type == 4 and not bj_forcing and not hiding_face:
                $ bj_torso_type = 2
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_front_arms

            "Slap her" if bj_speed >= 1 and not hiding_face and not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call BJ_Slap(girl) from _call_BJ_Slap

            "Tease her..." if bj_speed > 0 and not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call _tease_menu(girl, "bj") from _call_tease_menu_bj2

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call BJ_StripMenu(girl) from _call_BJ_StripMenu_1

            "Record Options..." if (bj_action != "lick" and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False)) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _sex_phone_menu(girl, "bj") from _call__sex_phone_menu_1
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "bj") from _call_watcher_rec_start_bj2_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "bj") from _call_watcher_rec_start_bj2_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ _rec_stop_name = _get_recording_stopper_name()
                        $ finalize_recording()
                        if store.hiding_face:
                            $ store.hiding_face = False
                        if _rec_stop_name:
                            $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                            "[_rec_stop_text]"
                        else:
                            "You stop recording."
                    "Order her to show her face" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        $ store._bj_face_ordered_shown = True
                        "You tell her to show her face."
                    "Back":
                        pass
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_rec_opts2

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "bj") from _call_PlayerCumMenu_voluntary_bj
                if getattr(store, "_bj_mouth_cum_continued", False):
                    $ store._bj_mouth_cum_continued = False
                    $ debug_log("[DEBUG] BJ_ActionMenu: mouth cum continue, staying in BJ")
                else:
                    $ _pce = _handle_post_cum_exit("bj", "sex")
                    if _pce == "hate_abort":
                        call BJ_End(girl, dress_up=False) from _call_BJ_End_hate_cum_vol
                    return

            "Go back":
                python:
                    _bj_hide_all(girl)
                    _bj_reset_state(girl)
                call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_7
                return

label BJ_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_4
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_8
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_4
                    return

            "Remove shirt" if girl.Mid:
                call _strip_approval(girl, ["mid"]) from _call__strip_approval_bj_mid
                if store._strip_approved:
                    $ girl.Outfit_Change(mid="none", pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_mid
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_bj_mid
                    return

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_5
                if store._strip_approved:
                    $ girl.Outfit_Change(chest_up=True, pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_9
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_5
                    return

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_5b
                if store._strip_approved:
                    $ girl.Outfit_Change(chest="none", pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_9b
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_5b
                    return

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_6
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_10
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_6
                    return

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_7
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="blowjob")
                    call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_11
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_7
                    return

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="blowjob")
                call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_12
                return

            "Back":
                return

# ============================================================
# End
# ============================================================
label BJ_End(girl, dress_up=True):
    $ debug_log("[DEBUG] BJ_End: entered, dress_up=%s" % str(dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _bj_hide_all(girl)
        _reset_expression_state(girl)
        store.hiding_face = False
        # The ATM context only lives inside a BJ scene. It used to be closed at the mouth cum only, so an ATM BJ that
        # ended any other way (facial, "Stop now", head grab rejection, forced swallow branches) leaked it into the
        # next scenes: ATM entry lines, the 850 ATM swallow check and now Firsts["cum_mouth"]="from_anal" on a plain BJ.
        if getattr(store, "_atm_cum_in_mouth", False):
            print("[ATM] BJ_End: closing a leftover ATM context (no mouth cum reaction) for %s" % girl.gid)
        store._atm_cum_in_mouth = False
        store._atm_tease_played = False

        store._bj_girl  = None
        store._bj_blink_running = False
        store._bj_cheeks_running = False
        store._bj_head_normal = False
        store.bj_blink  = False
        store.bj_eyes   = "normal"
        store.bj_brows  = 1
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_2
    $ debug_log("[DEBUG] BJ_End: returning")
    return
