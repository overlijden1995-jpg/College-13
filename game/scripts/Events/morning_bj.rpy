# ============================================================
# Morning BJ Event
# Small chance of waking up to a BJ after a sleepover.
# Requires experience (3+ BJs or FavoriteAct), high Love/Obed,
# 7-day cooldown. Chance scales with stats, traits, relationship.
# A femdom veteran wakes him her way instead: she sits on his face
# (MORNING_WAKE_VARIANTS["face_sit"], label morning_face_sit_solo).
# ============================================================

init python:

    # ── Config ──────────────────────────────────────────
    MORNING_BJ_CONFIG = {
        "min_bj_count": 3,          # times she did the wake-up's act with him (the BJ, or oral for face_sit), unless it is her FavoriteAct
        "min_love": 500,
        "min_obed": 300,
        "cooldown_days": 7,
        "base_chance": 5,
        "love_per_pct": 100,
        "obed_per_pct": 150,
        "lust_per_pct": 10,
        "favorite_bonus": 5,
        "hardcore_bonus": 5,
        "dating_bonus": 5,
        "harem_bonus": 3,
        "hate_cum_blocks": True,    # a hate_cum girl never wakes him this way
        "femdom_scaled": False,     # chance x femdom_intensity(girl)
    }

    # ── Femdom wake-up (docs/plan_femdom.md section 7, "Acordar") ──
    # CHOICE: the face-sitting version is BUILT (not the BJ re-voiced as her decision). The scene already exists and is
    # launched here exactly like the sex menu's "Eat her out" (sex_touch_menu, interactions.rpy): the cowgirl
    # masturbation scene with store._oral_active (MASTURBATE_Launch / MASTURBATE_ControlMenu / COWGIRL_End,
    # Core_Cowgirl.rpy), her on top, him eating her out. No scene code changed.
    # Who: a femdom VETERAN (her discovery phase never forces, trait_is_veteran) whose on-top oral art exists
    # (mast_pose "cowgirl" + "<gid> cowgirl_pussy": Gwen, Rogue, NTW today; Tenny's oral is laying_down, on her back,
    # and Shion has no cowgirl masturbation art) and who had him go down on her min_bj_count times. Anyone else, and a
    # femdom girl who can't yet, keeps the morning BJ exactly as before. Eligibility asks would_accept_action(girl,
    # "oral") (ACT_CONTROL "oral" = her, so the femdom bonus works FOR it); same 7-day cooldown (_morning_bj_last_day),
    # same achievement. Solo mornings only: the two-girl morning (morning_bj_duo) keeps the BJ.
    # Each wake-up: "act" (approval, counters, history) + the MORNING_BJ_CONFIG keys it changes.
    MORNING_WAKE_VARIANTS = {
        "bj": {"act": "bj"},
        "face_sit": {
            "act": "oral",
            "min_obed": 0,              # her order, not a favor to him: her Obed does not gate it...
            "obed_per_pct": 0,          # ...nor raise the chance (0 = no Obed term)
            "hardcore_bonus": 0,        # hardcore is pace and slaps (D3), not taking charge
            "hate_cum_blocks": False,   # he does not cum in this one
            "femdom_scaled": True,      # FEMDOM_PROFILE intensity: NTW 1.5 ... Rogue 0.9
        },
    }

    # ── Centralized dialogue ────────────────────────────
    MORNING_BJ_LINES = {
        "narration": [
            _("You're sleeping soundly when a warm, wet sensation begins to pull you from your dreams."),
            _("Something feels... really good. Your mind swims between sleep and consciousness."),
            _("A wave of pleasure washes over you, slowly dragging you out of sleep."),
        ],

        "greeting": {
            "cum_lover": [
                _("Mmm... good morning~ I couldn't help myself."),
                _("I woke up and just... wanted a taste."),
            ],
            # taking charge of him is femdom (docs/plan_femdom.md D3): hardcore keeps the rough greetings
            "femdom": [
                _("Shh. Relax. I know what I'm doing."),
                _("Morning. Hands off. I'll tell you when you can move."),
                _("Don't move. This is my breakfast, and I say how it goes."),
            ],
            "hardcore": [
                _("Don't mind me. Just having my breakfast."),
                _("Mmm... morning. I want it all the way down my throat."),
            ],
            "cute": [
                _("Oh! You're awake... I, um... I wanted to surprise you."),
                _("I... I thought you might like waking up to this..."),
            ],
            "default": [
                _("Good morning~ Thought I'd give you a nice start to the day."),
                _("Rise and shine. I'm making sure you wake up in a good mood."),
            ],
        },

        "greeting_fav": [
            _("You know this is my favorite, right? Lucky you~"),
            _("I could do this all morning..."),
        ],

        "witness_reaction": [
            _("Wha... what are you doing?!"),
            _("Oh my god... already?! It's morning!"),
            _("I... I didn't expect to see THIS when I woke up."),
        ],

        "after_bj": [
            _("Mmm... now THAT'S a good morning."),
            _("Hope that was a nice wake-up call~"),
            _("You're welcome, by the way."),
        ],

        "after_wake": [
            _("Now let's get ready for the day, shall we?"),
            _("Come on, we should get moving."),
        ],

        "after_duo_wake": [
            _("Well... that was something to wake up to."),
            _("I think we're all awake now..."),
        ],

        # Femdom wake-up (MORNING_WAKE_VARIANTS["face_sit"]): a veteran's voice only. He stopping before she is
        # done plays her femdom_refused line (femdom_lines.rpy) instead of "after".
        "face_sit": {
            "narration": [
                _("You wake up to warmth and weight settling over your face, her thighs pinning your head to the pillow."),
                _("Something soft presses down on your mouth. You open your eyes to find her straddling your face, looking down at you."),
                _("A hand grips your hair and the world goes dark and warm. By the time you're awake, she's already sitting on your face."),
            ],
            "greeting": [
                _("Morning. Tongue out. You're not getting up until I'm done."),
                _("Don't bother saying good morning. Your mouth has a job to do."),
                _("Awake? Good. Get to work, and don't stop until I tell you to."),
            ],
            "after": [
                _("Good boy. Now you can say good morning."),
                _("That's how I like to start my day. Remember it."),
                _("Mmm. You may get up now."),
            ],
        },
    }

    # ── Helpers ─────────────────────────────────────────

    def _mbj_trait_key(girl):
        if girl.has_trait("cum_slut"):
            return "cum_lover"
        # an eager trait she is still discovering keeps its veteran voice silent (trait_line_keys): no "femdom" yet
        if girl.has_trait("femdom") and not trait_is_discovering(girl, "femdom"):
            return "femdom"
        if girl.has_trait("hardcore_sex"):
            return "hardcore"
        if girl.has_trait("cute_sex"):
            return "cute"
        return "default"

    def _mw_cfg(variant, key):
        """A MORNING_BJ_CONFIG value as this wake-up (MORNING_WAKE_VARIANTS) changes it."""
        return MORNING_WAKE_VARIANTS[variant].get(key, MORNING_BJ_CONFIG[key])

    def _morning_wake_history(girl, act):
        """(enough, count, favorite): she did the act with him min_bj_count times, or it is her FavoriteAct."""
        _count = girl.Sex_acts.get(act, 0)
        _fav = girl.FavoriteAct == act
        return (_count >= MORNING_BJ_CONFIG["min_bj_count"] or _fav, _count, _fav)

    def _morning_face_sit_scene_ok(girl):
        """Her on-top oral scene exists: the cowgirl masturbation scene (mast_pose "cowgirl") and her oral overlay."""
        return (getattr(girl, "mast_pose", "cowgirl") == "cowgirl"
                and renpy.has_image("%s cowgirl_pussy" % girl.gid, exact=True))

    def _morning_wake_variant(girl):
        """How she wakes him up (MORNING_WAKE_VARIANTS): "face_sit" for a femdom veteran who can, else "bj".
        Deterministic (no approval roll here), so the eligibility, the roll and the label all read the same one."""
        if not girl.has_trait("femdom"):
            return "bj"
        if not trait_is_veteran(girl, "femdom"):
            print("[FEMDOM] morning wake-up: %s is still discovering femdom, the morning BJ stays" % girl.gid)
            return "bj"
        if not _morning_face_sit_scene_ok(girl):
            print("[FEMDOM] morning wake-up: %s has no on-top oral scene (mast_pose=%s), the morning BJ stays" % (
                girl.gid, getattr(girl, "mast_pose", "cowgirl")))
            return "bj"
        _act = MORNING_WAKE_VARIANTS["face_sit"]["act"]
        _enough, _count, _fav = _morning_wake_history(girl, _act)
        if not _enough:
            print("[FEMDOM] morning wake-up: %s had %s only %d times (< %d), the morning BJ stays" % (
                girl.gid, _act, _count, MORNING_BJ_CONFIG["min_bj_count"]))
            return "bj"
        print("[FEMDOM] morning wake-up: %s would sit on his face (%s=%d, intensity %.1f)" % (
            girl.gid, _act, _count, femdom_intensity(girl)))
        return "face_sit"

    def _morning_bj_eligible(girl, variant="bj"):
        """Can she wake him up this morning with this wake-up (MORNING_WAKE_VARIANTS key)?"""
        C = MORNING_BJ_CONFIG
        _act = MORNING_WAKE_VARIANTS[variant]["act"]
        _enough, _count, _fav = _morning_wake_history(girl, _act)
        if not _enough:
            print("[MORNING_BJ] %s INELIGIBLE (%s): %s count=%d < %d and FavoriteAct=%s" % (girl.Name, variant, _act, _count, C["min_bj_count"], girl.FavoriteAct))
            return False
        if girl.Love < C["min_love"]:
            print("[MORNING_BJ] %s INELIGIBLE (%s): Love=%d < %d" % (girl.Name, variant, girl.Love, C["min_love"]))
            return False
        _min_obed = _mw_cfg(variant, "min_obed")
        if girl.Obed < _min_obed:
            print("[MORNING_BJ] %s INELIGIBLE (%s): Obed=%d < %d" % (girl.Name, variant, girl.Obed, _min_obed))
            return False
        if _mw_cfg(variant, "hate_cum_blocks") and girl.has_trait("hate_cum"):
            print("[MORNING_BJ] %s INELIGIBLE (%s): has hate_cum trait" % (girl.Name, variant))
            return False
        _last = getattr(girl, "_morning_bj_last_day", 0)
        if _last > 0 and Day - _last < C["cooldown_days"]:
            print("[MORNING_BJ] %s INELIGIBLE (%s): cooldown (last=%d, Day=%d, need %d days)" % (girl.Name, variant, _last, Day, C["cooldown_days"]))
            return False
        _check = would_accept_action(girl, _act)
        if not _check.get("accepted", False):
            print("[MORNING_BJ] %s INELIGIBLE (%s): would not accept %s (reason=%s score=%s)" % (girl.Name, variant, _act, _check.get("reason_primary"), _check.get("score")))
            return False
        print("[MORNING_BJ] %s ELIGIBLE (%s: %s=%d fav=%s L=%d O=%d)" % (girl.Name, variant, _act, _count, _fav, girl.Love, girl.Obed))
        return True

    def _morning_bj_chance(girl, variant="bj"):
        C = MORNING_BJ_CONFIG
        _act = MORNING_WAKE_VARIANTS[variant]["act"]
        chance = C["base_chance"]
        chance += max(0, girl.Love - C["min_love"]) // C["love_per_pct"]
        _obed_pct = _mw_cfg(variant, "obed_per_pct")
        if _obed_pct:
            chance += max(0, girl.Obed - _mw_cfg(variant, "min_obed")) // _obed_pct
        chance += getattr(girl, "_pre_sleep_lust", 0) // C["lust_per_pct"]
        if girl.FavoriteAct == _act:
            chance += C["favorite_bonus"]
        if girl.has_trait("hardcore_sex"):
            chance += _mw_cfg(variant, "hardcore_bonus")
        if getattr(girl, "Player_status", "none") == "dating":
            chance += C["dating_bonus"]
            if len(get_player_girlfriends(ALL_GIRLS)) >= 2:
                chance += C["harem_bonus"]
        if _mw_cfg(variant, "femdom_scaled"):
            _base = chance
            chance = int(round(chance * femdom_intensity(girl)))
            print("[FEMDOM] morning %s chance for %s: %d%% x intensity %.1f = %d%%" % (
                variant, girl.gid, _base, femdom_intensity(girl), chance))
        print("[MORNING_BJ] chance for %s (%s): %d%% (L=%d O=%d Lust=%d fav=%s hc=%s dating=%s)" % (
            girl.Name, variant, chance, girl.Love, girl.Obed,
            getattr(girl, "_pre_sleep_lust", 0),
            girl.FavoriteAct == _act,
            girl.has_trait("hardcore_sex"),
            getattr(girl, "Player_status", "none") == "dating"))
        return chance

    def _morning_bj_roll(girl, variant="bj"):
        return renpy.random.randint(1, 100) <= _morning_bj_chance(girl, variant)

    def _morning_bj_pick_duo(girl1, girl2):
        e1 = _morning_bj_eligible(girl1)
        e2 = _morning_bj_eligible(girl2)
        if not e1 and not e2:
            return (None, None)
        if e1 and not e2:
            return (girl1, girl2)
        if e2 and not e1:
            return (girl2, girl1)
        bj1 = girl1.Sex_acts.get("bj", 0)
        bj2 = girl2.Sex_acts.get("bj", 0)
        if bj1 > bj2:
            return (girl1, girl2)
        if bj2 > bj1:
            return (girl2, girl1)
        if renpy.random.random() < 0.5:
            return (girl1, girl2)
        return (girl2, girl1)


# ============================================================
# Solo label
# ============================================================
label morning_bj_solo(girl):
    $ debug_log("[MORNING_BJ] solo event starting for %s" % girl.Name)

    $ Narration(_tl(renpy.random.choice(MORNING_BJ_LINES["narration"])))

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mbj_solo

    $ _scene_exit_flags_reset()
    call BJ_Launch(girl, start_speed=1) from _call_BJ_Launch_mbj_solo

    $ set_scene_expression(girl, "sly")
    $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["greeting"][_mbj_trait_key(girl)])))

    if girl.FavoriteAct == "bj":
        $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["greeting_fav"])))

    call BJ_ControlMenu(girl) from _call_BJ_ControlMenu_mbj_solo

    # Post-BJ cleanup: if cum happened, BJ is still active
    if store._bj_girl is not None:
        call BJ_End(girl, False) from _call_BJ_End_mbj_solo
    python:
        store._post_cum_pending = False
        mark_intimacy(girl, "bj")
        Change_Status(girl, "Love", 10)
        Change_Status(girl, "Inbt", 8)
        girl._morning_bj_last_day = Day

    $ unlock_achievement("great_good_morning")

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mbj_solo_post

    $ set_scene_expression(girl, "happy")
    $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["after_bj"])))

    menu:
        "Continue where we left off.":
            $ Change_Status(girl, "Lust", 20, max_val=100)
            call sex_menu(girl, CurrentLocation, TimeIndex) from _call_sex_menu_mbj_solo

        "Good morning to you too.":
            $ Change_Status(girl, "Love", 10)
            $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["after_wake"])))
            if getattr(girl, "_saved_outfit", None):
                $ girl.RestoreOutfit()

    return


# ============================================================
# Duo label
# ============================================================
label morning_bj_duo(bj_girl, witness_girl):
    $ debug_log("[MORNING_BJ] duo event: %s does BJ, %s watches" % (bj_girl.Name, witness_girl.Name))

    $ Narration(_tl(renpy.random.choice(MORNING_BJ_LINES["narration"])))

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mbj_duo

    python:
        _wit_check = would_accept_action(witness_girl, "bj")
        _wit_can_join = _wit_check.get("accepted", False)
        print("[MORNING_BJ] witness %s would_accept_bj: %s (reason=%s)" % (witness_girl.Name, _wit_can_join, _wit_check.get("reason_primary")))
        store._witness_girl = witness_girl
        store._witness_watching = True
        store._witness_was_near = True
        store._witness_entered = True
        store._witness_join_available = _wit_can_join
        store._witness_check_done = True
        set_scene_expression(witness_girl, "surprised")
        set_girl_sprite(witness_girl, pose="standing", at_list=[slot_right])

    $ _scene_exit_flags_reset()
    call BJ_Launch(bj_girl, start_speed=1) from _call_BJ_Launch_mbj_duo

    $ set_scene_expression(bj_girl, "sly")
    $ Say_Line(bj_girl, _tl(renpy.random.choice(MORNING_BJ_LINES["greeting"][_mbj_trait_key(bj_girl)])))

    if bj_girl.FavoriteAct == "bj":
        $ Say_Line(bj_girl, _tl(renpy.random.choice(MORNING_BJ_LINES["greeting_fav"])))

    $ set_scene_expression(witness_girl, "surprised")
    $ Say_Line(witness_girl, _tl(renpy.random.choice(MORNING_BJ_LINES["witness_reaction"])))

    call BJ_ControlMenu(bj_girl) from _call_BJ_ControlMenu_mbj_duo

    if store._bj_girl is not None:
        call BJ_End(bj_girl, False) from _call_BJ_End_mbj_duo
    python:
        store._post_cum_pending = False
        mark_intimacy(bj_girl, "bj")
        Change_Status(bj_girl, "Love", 10)
        Change_Status(bj_girl, "Inbt", 8)
        bj_girl._morning_bj_last_day = Day

    $ unlock_achievement("great_good_morning")

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mbj_duo_post
    $ set_girl_sprite(bj_girl, pose="standing", at_list=[slot_left])
    $ set_girl_sprite(witness_girl, pose="standing", at_list=[slot_right])

    $ set_scene_expression(bj_girl, "happy")

    if _wit_can_join:
        $ set_scene_expression(witness_girl, "sly")
    else:
        $ set_scene_expression(witness_girl, "uncomfortable")

    $ Say_Line(bj_girl, _tl(renpy.random.choice(MORNING_BJ_LINES["after_bj"])))

    menu:
        "Continue where we left off." if _wit_can_join:
            $ Change_Status(bj_girl, "Lust", 20, max_val=100)
            python:
                store._witness_girl = witness_girl
                store._witness_watching = True
                store._witness_join_available = True
                store._witness_was_near = True
                store._witness_entered = True
                store._witness_check_done = True
                store._threesome_mode = True
                store._threesome_participants = {bj_girl.gid}
            call sex_menu(bj_girl, CurrentLocation, TimeIndex) from _call_sex_menu_mbj_duo

        "Continue where we left off." if not _wit_can_join:
            $ Change_Status(bj_girl, "Lust", 20, max_val=100)
            python:
                store._witness_girl = witness_girl
                store._witness_watching = True
                store._witness_join_available = False
                store._witness_was_near = True
                store._witness_entered = True
                store._witness_check_done = True
                store._threesome_mode = False
            call sex_menu(bj_girl, CurrentLocation, TimeIndex) from _call_sex_menu_mbj_duo_obs

        "Good morning, you two.":
            $ Change_Status(bj_girl, "Love", 10)
            $ Change_Status(witness_girl, "Love", 5)
            $ Say_Line(witness_girl, _tl(renpy.random.choice(MORNING_BJ_LINES["after_duo_wake"])))
            python:
                store._witness_girl = None
                store._witness_watching = False
                store._witness_join_available = False
                store._threesome_mode = False
                store._threesome_participants = set()
                if getattr(bj_girl, "_saved_outfit", None):
                    bj_girl.RestoreOutfit()
                if getattr(witness_girl, "_saved_outfit", None):
                    witness_girl.RestoreOutfit()

    return


# ============================================================
# Femdom solo label: she wakes him by sitting on his face (docs/plan_femdom.md section 7, "Acordar")
# CHOICE (see MORNING_WAKE_VARIANTS): the face-sitting version is built from the existing oral scene, launched like
# the sex menu's "Eat her out" (sex_touch_menu): _oral_active + MASTURBATE_Launch + MASTURBATE_ControlMenu.
# Picked in sleepover.rpy (.wake_up_together) by _morning_wake_variant; same roll, cooldown and achievement as the BJ.
# Her order ("you're not getting up until I'm done") is judged like her other orders (femdom.rpy): he stops before
# she comes = he refused it (_femdom_refused_react: angry line, Obed -5 to -10, control corruption), no second round.
# ============================================================
label morning_face_sit_solo(girl):
    $ print("[FEMDOM] morning wake-up: %s sits on his face (intensity %.1f)" % (girl.gid, femdom_intensity(girl)))

    $ Narration(_tl(renpy.random.choice(MORNING_BJ_LINES["face_sit"]["narration"])))

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mfs_solo

    $ _scene_exit_flags_reset()
    python:
        # She got her bottoms off before climbing on him: saved first (the "Good morning" choice restores it), and
        # the launch's "better view" line and panties menu stay out of a wake-up.
        if not getattr(girl, "_saved_outfit", None):
            girl.SaveOutfit()
        girl.Outfit_Change(legs="none", panties="none", refresh=False)
        store.cowgirl_speed = 0
        store._oral_active = True
        _mfs_orgasms_before = sum((getattr(girl, "Orgasms", None) or {}).values())
    call MASTURBATE_Launch(girl) from _call_MASTURBATE_Launch_mfs_solo
    python:
        store._scene_phase = "oral"
        mark_intimacy(girl, "oral")     # counted when the scene starts, like the sex menu's oral

    $ set_scene_expression(girl, "sexy")
    $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["face_sit"]["greeting"])))
    $ girl.discover("discovered_trait_femdom")

    call MASTURBATE_ControlMenu(girl) from _call_MASTURBATE_ControlMenu_mfs_solo

    # The control menu ends the scene on every exit; this only guards a path that left it up
    if store._cowgirl_girl is not None:
        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_mfs_solo
    python:
        _mfs_done = sum((getattr(girl, "Orgasms", None) or {}).values()) > _mfs_orgasms_before
        print("[FEMDOM] morning face-sit: %s %s" % (
            girl.gid, "came, he obeyed (Love +10)" if _mfs_done else "did not come, he stopped first: he refused her order"))
        store._post_cum_pending = False
        if _mfs_done:
            Change_Status(girl, "Love", 10)
        Change_Status(girl, "Inbt", 8)
        girl._morning_bj_last_day = Day

    $ unlock_achievement("great_good_morning")

    call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_mfs_solo_post

    if not _mfs_done:
        call _femdom_refused_react(girl, "wake_up", "oral") from _call_fdr_mfs_solo
        if getattr(girl, "_saved_outfit", None):
            $ girl.RestoreOutfit()
        return

    $ set_scene_expression(girl, "sly")
    $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["face_sit"]["after"])))

    menu:
        "Continue where we left off.":
            $ Change_Status(girl, "Lust", 20, max_val=100)
            call sex_menu(girl, CurrentLocation, TimeIndex) from _call_sex_menu_mfs_solo

        "Good morning to you too.":
            $ Change_Status(girl, "Love", 10)
            $ Say_Line(girl, _tl(renpy.random.choice(MORNING_BJ_LINES["after_wake"])))
            if getattr(girl, "_saved_outfit", None):
                $ girl.RestoreOutfit()

    return
