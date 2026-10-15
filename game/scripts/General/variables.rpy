init -2 python:
    DEBUG = True
    def debug_log(msg):
        if DEBUG:
            print(msg)

    def _p(subpath):
        return ConditionSwitch(
            "getattr(Player, 'skin', 'White') == 'Black'", "images/characters/Player/Black/" + subpath,
            "True", "images/characters/Player/White/" + subpath
        )

    # His body drawn in HER folder, delivered in one skin only (Shion's Cowgirl / Reverse Cowgirl "Guy"): the
    # Black skin is the artist's own recipe, MEASURED on Player/Black/Doggy Shion against White (Guy.png and
    # Penis.png, 2026-10-12): every channel x0.30, pixel for pixel. A new Player/<skin>/ pair from the artist
    # replaces this with _p(). (Player report 2026-10-11: "asked Shion for a ride, now I'm white".)
    _BLACK_SKIN_TINT = TintMatrix("#4e4d4d")

    def _p_one_skin(path):
        return ConditionSwitch(
            "getattr(Player, 'skin', 'White') == 'Black'", Transform(path, matrixcolor=_BLACK_SKIN_TINT),
            "True", path
        )

    PUBLIC_LOCATIONS = frozenset({
        "campus", "pool", "hall", "street", "mall", "party",
        "gym", "classroom", "showers", "shower", "restaurant_restroom",
    })

    def _is_public_location(loc=None):
        if loc is None:
            loc = getattr(store, "CurrentLocation", "room")
        return loc in PUBLIC_LOCATIONS

init -1:
# Core loop state
    define PlayerChar = Character("[Player.Name]", color="#77aaff")
    define ProfessorChar = Character("Professor", color="#000000")
    define CJohnsonChar = Character("C. Johnson", color="#ff8c00")
    define BigFansChar = Character("BigFans", color="#ff5c93")
    default Player = PlayerData()
    default CurrentGirl = None          # Currently focused girl (Girl() instance) for interactions
    default CurrentLocation = "campus"  # Current player location: "campus", "room", "pool", or "shower"
    default Day = 1                     # Current in-game day counter (1 = first day)
    default TimeIndex = 0               # Index for TIME_NAMES (0 = Morning, 1 = Noon, etc.)
    default Round = 0                   # 0–100 progress inside the current time period; actions consume this
    default _girl_save = {}              # Snapshot of girl __dict__s, persisted across saves/loads
    default _npc_partner_cleared = set() # gids whose partner was intentionally cleared (rollback marker)
    default _scene_marked_acts = set()   # {(gid, act_or_position)} already counted in the current sex scene (mark_intimacy)
    default _switch_gate_ok = True        # _switch_to_vaginal_gate: the anal -> riding / reverse cowgirl switch may go ahead
    default _switch_gate_scene_ended = False   # ... the gate ended the scene (cheat path condom breakdown)
    default _save_version = None         # Version string stamped on save; None = pre-migration save
    default _migration_needs_redirect = False
    default Party = []
    define StageFarLeft    = 0.15
    define StageLeft       = 0.40
    define StageCenterLeft = 0.60
    define StageCenter     = 0.75
    define StageCenterRight = 0.80
    define StageRight      = 1.05
    define StageFarRight   = 0.95
    define StageNPCRight = 0.90
    default HolderCount = 0
    default consecutive_room_sleeps = 0   # resets when player leaves the room

    # ── Global state flags ─────────────────────────────────────
    # Track what the game is currently doing so systems (phone,
    # notifications, etc.) can gate behaviour accordingly.
    default _in_event   = False   # True while a scripted event is running (exam, hangout, night_swim)
    default _in_intro   = False   # True during the intro sequence (label intro)
    default _in_sandbox = True    # True while the player is in the main loop / free-roam
    default _met_cjohnson = False
    default virginity_blood = False
    default _virgin_blood_postscene = False
    default _cj_last_talk_day = -1

init python:
    def _migration_full_reset():
        store._in_event = False
        store._npc_passed_out = False
        store._tod_ended_sick = None
        store._scene_restricted = False
        store._scene_cum_continues = False
        store._interruption_happened = False
        store._witness_check_done = False
        store._hangout_scheduled_day = -1
        store._hangout_group_id = None
        store._hangout_members = []
        store._hangout_girl_a = None
        store._hangout_girl_b = None
        store._hangout_girl_c = None
        store._hangout_partner_npc = None
        store._hangout_partner_npc_id = None
        store._h_npc = None
        store._hangout_player_alcohol = 0
        store._cowgirl_girl = None
        store._rcg_girl = None
        store._hj_girl = None
        store._bj_girl = None
        store._titjob_girl = None
        store._fn_girl = None
        store._doggy_girl = None
        store._ft_girl = None
        store._rj_girl = None
        store.bk_in_store = False
        store.bk_auto_witness = None
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store.rcg_started = False
        store.rcg_rub_mode = False
        store.rcg_tip_mode = False
        store.rcg_grab = False
        store.rcg_arms_pose = 1
        store.doggy_started = False
        store.doggy_anal = False
        store.doggy_tip_mode = False
        store.titjob_started = False
        store.condom_active = False
        store.condom_denied = False
        store._condom_removed_midscene = False
        store._condom_broken = False
        store._condom_broken_hidden = False
        store._condom_break_will_happen = False
        store._stealth_condom_removed = False
        store._sex_menu_active = False
        store._threesome_mode = False
        store._threesome_participants = set()
        store._witness_girl = None
        store._witness_watching = False
        store._witness_join_available = False
        store._gf_permission_accepted = False
        store._gf_permission_mode = None
        store._gf_permission_gf = None
        store._ntr_partner_watching = False
        store._ntr_watching_npc = None
        # 0.11.x saves: the NTR bet flags leaked and broke the partner's reactions. A save made in the middle of
        # the event (or right after the heavy-spank abort) also keeps time locked and the day scheduled.
        if getattr(store, "_bet_event_active", False) and callable(globals().get("_bet_reset_flags", None)):
            _bet_reset_flags("migration", mark_done=False)
        store._bet_event_active = False
        store._bet_npc_looked = False
        store._recording_active = False
        store._recording_girl = None
        store._player_exhausted = False
        store._last_scene_was_anal = False
        store._atm_cum_in_mouth = False
        store._atm_source_gid = None
        store._creampie_consent = "denied"
        store._scene_condom_break = False
        store._scene_condom_break_believed = False
        store._sub_event_position_switched = False
        store.hiding_face = False
        for _mg in getattr(store, "ALL_GIRLS", []):
            if hasattr(store, "scene_full_cleanup"):
                try:
                    scene_full_cleanup(_mg)
                except RENPY_FLOW_EXCEPTIONS:
                    raise   # rollback / load / quit are exceptions in Ren'Py: never swallow them
                except Exception:
                    pass
        if hasattr(store, "session_cum_reset"):
            session_cum_reset()
        if hasattr(store, "condom_break_reset") and callable(condom_break_reset):
            condom_break_reset()
        if hasattr(store, "stealth_condom_reset") and callable(stealth_condom_reset):
            stealth_condom_reset()
        if renpy.get_screen("recording_overlay"):
            renpy.hide_screen("recording_overlay")
        if renpy.get_screen("tod_drunk_bars"):
            renpy.hide_screen("tod_drunk_bars")
        debug_log("[MIGRATE] Full sex scene state reset applied")
        store._restaurant_bg = None
        for _mg_girl in ALL_GIRLS:
            if hasattr(_mg_girl, "_hangout_alcohol"):
                _mg_girl._hangout_alcohol = 0
            _mg_girl.loc = _mg_girl.get_scheduled_location(store.Day, store.TimeIndex)
        for _mg_npc_id, _mg_npc in NPC_PARTNERS.items():
            if hasattr(_mg_npc, "_hangout_alcohol"):
                _mg_npc._hangout_alcohol = 0
            if hasattr(_mg_npc, "hide_sprite"):
                _mg_npc.hide_sprite()
        _mg_legacy = store.Player.get_item_count("drinks") if hasattr(store.Player, "get_item_count") else 0
        if _mg_legacy > 0:
            store.Player.remove_item("drinks", _mg_legacy)
            store.Player.add_item("drink_med", _mg_legacy)
            debug_log("[MIGRATE] Converted %d legacy 'drinks' to 'drink_med'" % _mg_legacy)
        store.CurrentLocation = "room"

    def _check_migration_redirect():
        if getattr(store, "_migration_needs_redirect", False):
            store._migration_needs_redirect = False
            debug_log("[MIGRATE] Redirect callback fired, jumping to Player_Room_Entry")
            renpy.jump("Player_Room_Entry")

    config.interact_callbacks.append(_check_migration_redirect)