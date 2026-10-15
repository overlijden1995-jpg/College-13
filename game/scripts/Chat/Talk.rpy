default _sex_bubble_who = None
default _sex_bubble_text = ""
default _sex_bubble_color = "#ffffff"
default _sex_bubble_saved_face = None
default _pending_tease_restore = None
default _sex_bubble_pending = False

init python:

    def _in_sex_nonbj():
        if getattr(store, "_bj_girl", None) is not None:
            return False
        return (getattr(store, "_hj_girl", None) is not None
                or getattr(store, "_titjob_girl", None) is not None
                or getattr(store, "_cowgirl_girl", None) is not None
                or getattr(store, "_rcg_girl", None) is not None
                or getattr(store, "_doggy_girl", None) is not None
                or getattr(store, "_fn_girl", None) is not None
                or getattr(store, "_laying_girl", None) is not None
                or getattr(store, "_ft_girl", None) is not None
                or getattr(store, "_rj_girl", None) is not None)

    # The bubble flows free ONLY when an interaction (a menu, a say, a pause) happened since the last one
    # (author, 2026-10-09, player report: "scenes don't wait for you to advance"). A lone action line keeps
    # its flow: the control menu right after it is the interaction that lets him read it. A SECOND bubble with
    # no interaction between is a conversation: it waits for his click (renpy.pause: the animation keeps
    # running under it), one click per line, as any dialogue.
    # Only an interaction the PLAYER ends counts (tester 2026-10-11, the marital bed: "She pushes you onto
    # the bed..." vanished in under a second, swallowed by RCG_Launch's `with fade`). A transition (mode
    # "with") and a TIMED renpy.pause(x) end on their own: the line before them still waits for a click.
    # The timed pause is interact()'s own `pause` argument, read from its frame (the caller of this
    # callback, Ren'Py 8.4 core.py); anything unreadable counts, exactly as before.
    import sys as _sb_sys

    def _sex_bubble_interacted():
        if renpy.get_mode() == "with":
            return
        try:
            if _sb_sys._getframe(1).f_locals.get("pause") is not None:
                return
        except Exception:
            pass
        store._sex_bubble_pending = False

    config.start_interact_callbacks.append(_sex_bubble_interacted)

    # Ren'Py drives rollback, load, quit, jump and call with EXCEPTIONS (renpy/game.py: every one of them
    # a plain Exception subclass). A `try / except Exception` around an interaction swallows them: the store
    # is already rolled back (or replaced by the loaded save) and the code goes on as if nothing happened
    # (player crash 2026-10-11: the bubble wait in scene_full_cleanup ate a rollback, and the line after it
    # read a variable the rollback had deleted: NameError '_save_exhausted'). Never catch these: re-raise first.
    RENPY_FLOW_EXCEPTIONS = (
        renpy.game.RestartContext, renpy.game.RestartTopContext, renpy.game.FullRestartException,
        renpy.game.UtterRestartException, renpy.game.QuitException, renpy.game.JumpException,
        renpy.game.JumpOutException, renpy.game.CallException, renpy.game.EndReplay)

    def _sex_bubble_wait_click():
        """A bubble nobody clicked yet waits for his click before anything replaces or wipes it (a new
        bubble, the scene teardown). Only with the bubble REALLY on screen: the flag alone can come stale
        out of a save, and must never pause into nothing. The animation keeps running under the pause."""
        if not (getattr(store, "_sex_bubble_pending", False) and renpy.get_screen("sex_bubble")):
            return
        try:
            renpy.pause()
        except RENPY_FLOW_EXCEPTIONS as e:
            print("[SEX_BUBBLE] %s during the bubble wait: propagating (rollback / load / quit restart the context)" % type(e).__name__)
            raise
        except Exception as e:
            print("[SEX_BUBBLE] wait for click skipped (no interaction possible here): %r" % (e,))

    def _sex_bubble_show(who_name, text, who_color=None):
        _sex_bubble_wait_click()
        renpy.hide_screen("sex_bubble")
        store._sex_bubble_who = who_name
        store._sex_bubble_text = text
        store._sex_bubble_color = who_color or "#ffffff"
        if who_name and who_name != getattr(store.Player, "Name", ""):
            _sex_bubble_set_face(who_name)
        renpy.show_screen("sex_bubble")
        store._sex_bubble_pending = True

    def _sex_bubble_dismiss():
        _sex_bubble_restore_face()
        store._sex_bubble_who = None
        store._sex_bubble_text = ""
        store._sex_bubble_color = "#ffffff"
        store._sex_bubble_pending = False

    def _force_dismiss_sex_bubble():
        if store._sex_bubble_who is not None or renpy.get_screen("sex_bubble"):
            _sex_bubble_dismiss()
            if renpy.get_screen("sex_bubble"):
                renpy.hide_screen("sex_bubble")

    def _sex_bubble_set_face(who_name):
        for g in store.ALL_GIRLS:
            if g.Name == who_name:
                gid = g.gid
                if store._sex_bubble_saved_face and store._sex_bubble_saved_face.get("gid") == gid:
                    set_scene_expression(g, "moaning")
                    return
                ss = sprite_state.get(gid, {})
                prev = {k: ss.get(k) for k in ("eyes", "brows", "mouth")}
                set_scene_expression(g, "moaning")
                now = {k: sprite_state.get(gid, {}).get(k) for k in ("eyes", "brows", "mouth")}
                store._sex_bubble_saved_face = {"gid": gid, "prev": prev, "set": now}
                return

    def _sex_bubble_restore_face():
        saved = store._sex_bubble_saved_face
        if not saved:
            return
        store._sex_bubble_saved_face = None
        gid = saved["gid"]
        ss = sprite_state.get(gid, {})
        expected = saved["set"]
        if all(ss.get(k) == expected.get(k) for k in ("eyes", "brows", "mouth")):
            for k in ("eyes", "brows", "mouth"):
                if saved["prev"].get(k) is not None:
                    ss[k] = saved["prev"][k]

    def find_girl_for_who(who):
        """
        Tenta mapear o 'who' para uma das garotas em ALL_GIRLS.
        Compara gid, name, Name em lowercase.
        """
        if not who:
            return None

        wlow = who.lower()
        try:
            girls_here = girls_on_scene()
        except Exception:
            # fallback: tenta ALL_GIRLS se não tiver cena
            girls_here = ALL_GIRLS if 'ALL_GIRLS' in globals() else []

        debug_log(who)

        for g in girls_here:
            gid   = getattr(g, "gid", "").lower()
            name1 = getattr(g, "Name", "").lower()
            if wlow in (gid, name1):
                debug_log(g)
                return g

        return None

    def ru_keys_safety(text, girl=None):
        """A line still carrying a Russian case key ("%(r_...)s") or her partner's name ("%(pn)s", a translation that
        names him where the English does not): its pool's formatter has none, so it gets the partner keys of the girl it
        is about (the speaker, else the girl of the scene), never a crash. Logged: such a pool should go through
        partner_fmt / _format_partner_line."""
        if not text or ("%(r_" not in text and "%(pn)s" not in text and "%(Pn)s" not in text):
            return text
        _g = girl if hasattr(girl, "get_flag") else getattr(store, "CurrentGirl", None)
        print("[I18N] unformatted partner keys (girl %s): %r" % (getattr(_g, "gid", None), text[:80]))
        if _g is None or not hasattr(_g, "get_flag"):
            _d = dict(gender_fmt(False), **partner_label_fmt(False))
            _d.setdefault("pn", _d.get("pl", ""))
            _d.setdefault("Pn", _d["pn"][:1].upper() + _d["pn"][1:])
            return fmt_safe(text, _d)
        return fmt_safe(text, partner_fmt(_g))

    def Say_Line(who, text):
        """
        who: Girl instance that will speak.
        text: dialogue line string to display.
        Petname substitution: if the girl has a petname for the player,
        [Player.Name] in text is replaced with the petname.
        """
        text = ru_keys_safety(_tl(text), who)
        if hasattr(who, "has_npc_partner") and who.has_npc_partner():
            if who.get_flag("partner_is_female"):
                text = text.replace("my boyfriend", "my girlfriend").replace("My boyfriend", "My girlfriend")
            else:
                text = text.replace("my girlfriend", "my boyfriend").replace("My girlfriend", "My boyfriend")
        _pn = getattr(who, "petname_for_player", None)
        if "[Player.Name]" in text:
            text = text.replace("[Player.Name]", _tr(_pn) if _pn else store.Player.Name)
        if getattr(store, "_phone_mode", False):
            g = getattr(store, "_phone_mode_girl", None)
            if g is not None:
                gid = getattr(g, "gid", "")
                sender = getattr(who, "gid", gid)
                if not hasattr(store, "_phone_msg_queue"):
                    store._phone_msg_queue = []
                store._phone_msg_queue.append({"gid": gid, "sender": sender, "text": text})
            return
        if _in_sex_nonbj():
            _sex_bubble_show(who.Name, text, who_color=getattr(who, "color", "#ffffff"))
            return
        _force_dismiss_sex_bubble()
        _bj_swapped = _bj_swap_speaking_head(who)
        char = _make_char_from_girl(who)
        renpy.say(char, text)
        if _bj_swapped:
            _bj_restore_speaking_head(who)

    def Say_Player(text):
        """
        text: dialogue line string spoken by the Player character.
        Wrapper to keep player speech consistent with Say_Line().

        Example:
            $ Say_Player(_("Yeah, let's go."))
        """
        text = ru_keys_safety(_tl(text))
        if getattr(store, "_phone_mode", False):
            g = getattr(store, "_phone_mode_girl", None)
            if g is not None:
                gid = getattr(g, "gid", "")
                if not hasattr(store, "_phone_msg_queue"):
                    store._phone_msg_queue = []
                store._phone_msg_queue.append({"gid": gid, "sender": "player", "text": text})
            return
        if _in_sex_nonbj():
            _sex_bubble_show(store.Player.Name, text, who_color="#77aaff")
            return
        _force_dismiss_sex_bubble()
        renpy.say(PlayerChar, text)

    def Narration(text):
        """
        text: narration line with no speaker name.

        Example:
            $ Narration(_("The room suddenly feels colder."))
        """
        text = ru_keys_safety(_tl(text))
        if getattr(store, "_phone_mode", False):
            return
        if _in_sex_nonbj():
            _sex_bubble_show(None, text)
            return
        _force_dismiss_sex_bubble()
        renpy.say(None, text)

    def Thinking(who, text):
        """
        who: Girl instance that is thinking.
        text: thought content, will be shown in parentheses.

        Example:
            $ Thinking(Gwen, "I wonder what he's planning...")
        """
        if getattr(store, "_phone_mode", False):
            return
        if _in_sex_nonbj():
            _sex_bubble_show(who.Name, "(" + text + ")", who_color=getattr(who, "color", "#ffffff"))
            return
        _force_dismiss_sex_bubble()
        char = _make_char_from_girl(who)
        renpy.say(char, "(" + text + ")")

    def _make_char_from_girl(girl):
        """
        girl: Girl instance used as speaker.
        Creates a Ren'Py Character using girl.Name and girl.color.
        """
        from renpy.character import Character
        return Character(girl.Name, who_color=girl.color)