# ============================================================
# femdom_turn.rpy... the TURN of a canon femdom girl (Shion) (docs/plan_shion.md Fase 3, decision D2; since
# 2026-10-01 on the steps engine, docs/plan_role_situations.md). A femdom girl who is NOT canon loses her femdom to
# his refusals (CORRUPTION_RULES["control"], femdom.rpy); a canon femdom can't lose it (the canon lock in
# check_corruption), so her way is this one: he breaks her control little by little.
# HER STAGE IS HER STEP (story_steps.rpy, femdom_stage = story_step): it only moves by the unlock event of her step,
# which asks for stats by routes. A canon femdom without a story has no turn (stage 0).
#   stage 0: she rules (femdom intensity x1, "no hands until I say", curfew at Night, no lewd photos)
#   stage 1: she lets him touch "because she decided"
#   stage 2: his hands are allowed (no more FEMDOM_FLIRT_HOLD)
#   stage 3: she is his: no curfew, she sends photos, she barely gives orders, she comes to his dorm room at night
# What she lets him DO at each stage is her step's list of acts (STORY_LADDERS), not this file.
# Break points (FEMDOM_TURN_POINTS) count on the Obed route of her unlock events (STORY_BREAK_OBED); "his_act"
# counts once per scene for each act / position:
#   his_act             a sex act or position where HE is in control (scene_control == "him") marked with her
#   her_cum_his_act     she comes in one of those
#   defied              he stood up to one of her orders and won (femdom_defied)
#   resisted_forced_cum he kept her from deciding where he finishes (_player_resist_forced_cum)
#   blackmail_act       an act she did under his blackmail (his videos of her; author: only videos, no other source)
#   talked_back         he stood up to her in one of her punishments (family_grades.rpy: refused the breakup)
#   obeyed              he took her punishment in silence (family_grades.rpy): points DOWN
# What a stage changes: femdom_intensity (FEMDOM_TURN_INTENSITY), the approval penalty of "his" acts
# (FEMDOM_TURN_HIS_PENALTY, approval.rpy), femdom_flirt_mode (no hold from FEMDOM_TURN_NO_HOLD_STAGE),
# apartment_curfew_girl (none from FEMDOM_TURN_NO_CURFEW_STAGE), girl_sends_lewd_photos, her visits to his dorm room
# (girl_comes_to_his_dorm), and her voice: the line modifier femdom_stage_mod ("femdom_s2" / "femdom_s3") in the
# flirts, the sex menu, the scenes and the small talk.
# ============================================================

default _femdom_turn_noted = set()      # (gid, act) already counted as "his_act" this scene (femdom_session_reset)

init python:

    FEMDOM_TURN_BREAK_MAX = 100                 # her break points stop here
    FEMDOM_TURN_POINTS = {
        "his_act": 5,
        "her_cum_his_act": 8,
        "defied": 6,
        "resisted_forced_cum": 4,
        "blackmail_act": 12,
        "talked_back": 6,
        "obeyed": -3,
    }
    FEMDOM_TURN_INTENSITY = (1.0, 0.7, 0.4, 0.15)   # x her femdom intensity, by stage
    FEMDOM_TURN_HIS_PENALTY = (1.0, 0.66, 0.33, 0.0)  # fades the "him" shift of TRAIT_STAT_WEIGHTS["femdom"], by stage
    FEMDOM_TURN_NO_HOLD_STAGE = 2               # from here his hands are allowed (femdom_flirt_mode)
    FEMDOM_TURN_NO_CURFEW_STAGE = 3             # from here she lets him stay at Night (apartment_curfew_girl)
    FEMDOM_TURN_PHOTOS_STAGE = 3                # from here she sends lewd photos on her own (girl_sends_lewd_photos)
    FEMDOM_TURN_VISIT_SLOT = 2                  # her visits to his dorm room: from the Evening
    FEMDOM_TURN_DORM_STAGE = 3                  # from here she lives off campus and still comes to his dorm room when he
                                                # calls her, from the Evening (girl_comes_to_his_dorm, _girl_accepts_invite)

    def femdom_turn_applies(girl):
        """Her femdom is DECLARED canon (GIRLS_CONFIG "traits"): his refusals can't take it, he turns her instead.
        Reads the config, not the live trait: after the break (CANON_BREAK_RULES, she lost the femdom past her
        final step) the turn's stage and bookkeeping keep working; her femdom VOICE and orders die with the trait
        itself (femdom_stage_mod / femdom_intensity check has_trait)."""
        return (girl is not None
                and "femdom" in GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("traits", ()))

    def femdom_stage(girl):
        """Her stage on the turn (0..3) = her story step (story_steps.rpy), a step past the turn's last stage reads
        as that stage (the FEMDOM_TURN_* tables are indexed by it); 0 for a girl who is not on it."""
        return min(story_step(girl), len(FEMDOM_TURN_INTENSITY) - 1) if femdom_turn_applies(girl) else 0

    def femdom_stage_mod(girl):
        """The line modifier of her stage ("femdom_s2" / "femdom_s3"), or None: her base voice is stages 0 and 1.
        A broken femdom (trait gone, CANON_BREAK_RULES) speaks by her traits, never the femdom stage voice."""
        if not (hasattr(girl, "has_trait") and girl.has_trait("femdom")):
            return None
        _s = femdom_stage(girl)
        return "femdom_s%d" % _s if _s >= 2 else None

    def femdom_turn_note(girl, source, detail=""):
        """A break point (FEMDOM_TURN_POINTS[source]): they count on the Obed route of her unlock event
        (story_route_score). They never move her stage: only her unlock event does."""
        if not femdom_turn_applies(girl):
            return
        _pts = FEMDOM_TURN_POINTS.get(source, 0)
        if not _pts:
            return
        if source == "his_act":
            _key = (girl.gid, str(detail))
            if _key in store._femdom_turn_noted:
                return
            store._femdom_turn_noted.add(_key)
        _old = int(getattr(girl, "_femdom_break", 0) or 0)
        girl._femdom_break = max(0, min(FEMDOM_TURN_BREAK_MAX, _old + _pts))
        print("[FEMDOM] turn: %s %s%s %+d -> %d/%d (Obed route %d, stage %d)" % (
            girl.gid, source, (" (%s)" % detail) if detail else "", _pts, girl._femdom_break, FEMDOM_TURN_BREAK_MAX,
            story_route_score(girl, "Obed"), femdom_stage(girl)))
        # Past her gate (final story step) every DOMINANT turn source also feeds the control corruption: at that
        # point she barely gives orders, so plain refusals alone would never reach 15/30. "defied" already counts
        # through femdom_defied (it would double), "obeyed" is the opposite direction.
        if (source in ("his_act", "her_cum_his_act", "resisted_forced_cum", "blackmail_act", "talked_back")
                and trait_canon_breakable(girl, "femdom")):
            _femdom_count_refusal(girl, "turn:%s" % source)

    def girl_comes_to_his_dorm(girl):
        """She lives off campus, but comes to his dorm room when he invites her (Evening / Night) from her story
        step FEMDOM_TURN_DORM_STAGE: the nights she lies to her husband (shion_netori.rpy). Reads her STORY, not
        the femdom stage: losing the trait (CANON_BREAK_RULES) must never take her visits away."""
        return (story_key(girl) is not None and story_step(girl) >= FEMDOM_TURN_DORM_STAGE
                and store.CurrentLocation == "room" and store.TimeIndex >= FEMDOM_TURN_VISIT_SLOT)

    def girl_sends_lewd_photos(girl):
        """She sends lewd photos on her own (the Wait photo events): a girl with a STORY only from its step 3
        (a girl without one always does). Reads the story, not the femdom stage: losing the trait must not
        re-lock her photos, and story_step is 0 for every no-story girl (they'd all go silent)."""
        return story_key(girl) is None or story_step(girl) >= FEMDOM_TURN_PHOTOS_STAGE
