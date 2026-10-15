# ============================================================
# Edge / Cum Denial System
# Triggers when player clicks "Stop now" while Lust >= 80
# She begs to continue — player decides to keep going or stop
# ============================================================

default _edge_denial_count = 0
default _edge_scene_ended = False

init python:

    # Her Control trait at the edge (tester 2026-10-11, the author's go): a submissive PLEADS, deferent, and takes
    # the no as what she wanted (trait_love_loss: it costs her nothing); a femdom DEMANDS, and his no is a refusal
    # she makes him pay for (femdom_react_refused). Keyed by the denial count (0, 1, 2+ = "more").
    _EDGE_CONTROL_BEG = {
        "submissive": {
            0: [
                _("Can we please keep going a little bit longer? I'm... really close."),
                _("Please... not yet. I'll be good. I just need a little more. If you want."),
                _("I'm so close... please? Only if you want me to. But please."),
            ],
            1: [
                _("Again...? I... okay. Please. Just a little more. Please."),
                _("I'm not asking for much. Please let me finish. I'll do anything after."),
            ],
            "more": [
                _("You win! You own me! Just PLEASE let me finish!"),
                _("Please... I'll be good, I'll do whatever you say... just let me cum!"),
                _("I'm yours! Anything you want! Please, PLEASE let me finish!"),
            ],
        },
        "femdom": {
            0: [
                _("Who said you could stop? I'm not done. Back to it."),
                _("Stop? No. I decide when we stop, and I haven't finished. Keep going."),
                _("You don't get to stop here. Finish what you started."),
            ],
            1: [
                _("You stopped again. Cute. Now get back to it, before I lose my patience."),
                _("I don't repeat myself. Keep going. Now."),
            ],
            "more": [
                _("Three times. You are TESTING me. Finish me. That's an order."),
                _("Enough games. Make me cum, or you'll regret every second of this."),
            ],
        },
    }
    _EDGE_CONTROL_STOP = {
        "submissive": [
            _("...Okay. If that's what you want. Thank you for... for taking me this far."),
            _("Yes. We stop. I'm sorry I asked. I'll be good."),
        ],
        "femdom": [
            _("You're leaving me like this. Fine. Remember that I remember."),
            _("Wow. You'll pay for that one. I'll make sure of it."),
        ],
    }
    # The post-cum "Stop" (Cum.rpy _post_cum_central): he came, she did not, and he wants to stop
    _POST_CUM_STOP_PLEA = {
        "submissive": [
            _("Wait... please. You finished, but I... I'm really close. Can we keep going a little? Only if you want."),
            _("Please don't stop yet. I'll do it however you want. I'm just... so close."),
        ],
        "submissive_kept": [
            _("Thank you... thank you. I'll make it quick, I promise."),
            _("You're so good to me. Just a little more..."),
        ],
        "submissive_denied": [
            _("...Okay. You decide. I'm fine. I'm... fine. Thank you for tonight."),
            _("Yes. We stop. I shouldn't have asked. Sorry."),
        ],
        "femdom": [
            _("You're not done. I haven't finished, and that's the part that matters. Get back here."),
            _("Oh, you came, so we're done? No. You finish me first. That's how this works."),
        ],
        "femdom_kept": [
            _("Good. Now make it count."),
            _("That's better. Don't you dare slow down."),
        ],
        "femdom_denied": [
            _("You're walking away from me like this? Noted. Very noted."),
            _("Fine. Go. I won't forget this, and neither will you."),
        ],
    }

    def _edge_control_trait(girl):
        """"submissive" / "femdom" / None: the Control trait that speaks at the edge."""
        if hasattr(girl, "has_trait"):
            for _t in ("submissive", "femdom"):
                if girl.has_trait(_t):
                    return _t
        return None

label EdgeDenial(girl, scene_type):
    $ store._edge_scene_ended = False
    $ debug_log("[DEBUG] EdgeDenial: entered for %s scene=%s lust=%d denial_count=%d" % (girl.gid, scene_type, girl.Lust, _edge_denial_count))

    python:
        _ed_count = store._edge_denial_count
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cute = girl.has_trait("cute_sex")
        _is_cs = girl.has_trait("cum_slut")
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

        _ed_ctl = _edge_control_trait(girl)

        if _ed_count == 0:
            if _ed_ctl:
                _beg_line = renpy.random.choice(_EDGE_CONTROL_BEG[_ed_ctl][0])
            elif _is_hc:
                _beg_line = renpy.random.choice([
                    _("What... what are you doing? Don't stop! I was so close!"),
                    _("No no no, keep going! I'm right there, don't you dare stop!"),
                    _("You're seriously stopping NOW?! I'm about to cum!"),
                ])
            elif _is_cute:
                _beg_line = renpy.random.choice([
                    _("W-why did you stop...? I was... I was almost there..."),
                    _("Please... don't stop now... I need just a little more..."),
                    _("No... please keep going... I was so close..."),
                ])
            elif _is_cs:
                _beg_line = renpy.random.choice([
                    _("Don't stop! I'm so close... please, I need to cum!"),
                    _("Why would you stop?! I'm right on the edge!"),
                ])
            else:
                _beg_line = renpy.random.choice([
                    _("Hey... why did you stop? I was getting close..."),
                    _("Don't stop now... I was almost there..."),
                    _("Wait... keep going, I'm so close..."),
                ])
        elif _ed_count == 1:
            if _ed_ctl:
                _beg_line = renpy.random.choice(_EDGE_CONTROL_BEG[_ed_ctl][1])
            elif _is_hc:
                _beg_line = renpy.random.choice([
                    _("AGAIN?! You're doing this on purpose! Just let me cum already!"),
                    _("Stop teasing me! I can't take it! Let me finish!"),
                ])
            elif _is_cute:
                _beg_line = renpy.random.choice([
                    _("Not again... please... I can't handle this... I need it so bad..."),
                    _("You're being so mean... please, I'm begging you... let me finish..."),
                ])
            elif _is_cs:
                _beg_line = renpy.random.choice([
                    _("Please! I'll do anything! Just let me cum!"),
                    _("I can't take the teasing... please, I need to cum so bad..."),
                ])
            else:
                _beg_line = renpy.random.choice([
                    _("Come on... not again... please just let me finish..."),
                    _("You're killing me... please, I need this..."),
                ])
        else:
            # "you own me" is submissive, not hardcore (docs/plan_femdom.md D3); a femdom orders him back
            if _ed_ctl:
                _beg_line = renpy.random.choice(_EDGE_CONTROL_BEG[_ed_ctl]["more"])
            elif _is_hc:
                _beg_line = renpy.random.choice([
                    _("I swear to god... if you don't let me cum right now I'll lose my mind!"),
                    _("Please! I can't take anymore! I'll do anything! Just let me cum!"),
                ])
            elif _is_cute:
                _beg_line = renpy.random.choice([
                    _("I can't... I can't take it anymore... please... I'll do anything you want... just let me..."),
                    _("I'm going crazy... please... I need it... I'll be good, I promise..."),
                ])
            elif _is_cs:
                _beg_line = renpy.random.choice([
                    _("I'll swallow everything! I'll do whatever you want! PLEASE just let me cum!"),
                    _("I'm losing my mind... I need to cum so bad it hurts... please..."),
                ])
            else:
                _beg_line = renpy.random.choice([
                    _("Please... I'll do anything... I can't take this anymore..."),
                    _("I've never been this desperate... please just let me finish..."),
                ])

            if _has_bf and not girl.has_trait("cheater"):
                # each part translated BEFORE the join (a joined line has no pair); _format_partner_line below fills %(pl)s
                _beg_line = _tl(_beg_line) + _tl(_(" I've never begged my %(pl)s like this..."))

    $ Say_Line(girl, _format_partner_line(girl, _beg_line))

    # Lust stays high but doesn't overflow
    $ girl.Lust = min(99, max(girl.Lust, 90))

    menu:
        "Keep going":
            $ store._edge_denial_count += 1
            if store._edge_denial_count <= 3:
                python:
                    _deny_obed = 5 + (store._edge_denial_count * 3)
                    _deny_inbt = 3 + (store._edge_denial_count * 2)
                    Change_Status(girl, "Obed", _deny_obed)
                    Change_Status(girl, "Inbt", _deny_inbt)
                    Change_Status(girl, "Love", 5)
                    if store._edge_denial_count >= 3:
                        girl.check_corruption("pace")
                        unlock_achievement("edge_lord")
                    debug_log("[DEBUG] EdgeDenial: continued, count=%d obed+%d inbt+%d love+5" % (store._edge_denial_count, _deny_obed, _deny_inbt))

        "No, stop.":
            $ store._edge_denial_count += 1
            python:
                _stop_obed = 8 + (store._edge_denial_count * 5)
                Change_Status(girl, "Obed", _stop_obed)
                Change_Status(girl, "Love", trait_love_loss(girl, -3))   # denied: nothing to a submissive, more to a femdom
                if store._edge_denial_count >= 2:
                    girl.check_corruption("pace")
                debug_log("[DEBUG] EdgeDenial: stopped, count=%d obed+%d love-3" % (store._edge_denial_count, _stop_obed))

            python:
                if _ed_ctl:
                    _stop_line = renpy.random.choice(_EDGE_CONTROL_STOP[_ed_ctl])
                elif _is_cute:
                    _stop_line = renpy.random.choice([
                        _("No... please... you can't just leave me like this..."),
                        _("That's so cruel... I was right there..."),
                    ])
                elif _is_hc:
                    _stop_line = renpy.random.choice([
                        _("You're a bastard. You know that, right?"),
                        _("I can't believe you're stopping. You're going to pay for this later."),
                    ])
                else:
                    _stop_line = renpy.random.choice([
                        _("Really? You're just going to leave me hanging?"),
                        _("That's... wow. Okay. Fine."),
                    ])
            $ Say_Line(girl, _stop_line)
            if _ed_ctl == "femdom":
                # his no to her order: counted and paid (femdom.rpy)
                $ femdom_react_refused(girl, "stop", scene_type)
            $ girl.Lust = max(60, girl.Lust - 20)
            $ store._edge_scene_ended = True
            $ store._hard_cum_ready = True
            $ store._edge_denial_count = 0

    return

# ============================================================
# The post-cum "Stop" (Cum.rpy _post_cum_central): he came, she is still on the edge, he wants to stop.
# A submissive pleads for a little more, a femdom demands it; "Keep going" resumes the scene (the post-cum
# loop of start_scene re-enters the position's menu), "No" ends it with her trait's reaction.
# ============================================================
label _post_cum_stop_plea(girl, scene_type):
    python:
        _pcp_trait = _edge_control_trait(girl)
        _pcp_edge = (getattr(girl, "Lust", 0) >= 85
                     and store._session_orgasms_by_girl.get(getattr(girl, "gid", None), 0) == 0
                     and not getattr(store, "_scene_restricted", False)
                     and not getattr(store, "_scene_angry_abort", False))
    if _pcp_trait is None or not _pcp_edge:
        return
    $ print("[EDGE] post-cum stop: %s (%s) on the edge, she speaks before the scene ends" % (girl.gid, _pcp_trait))
    # the cleanup's "left on the edge" line is this one
    $ store._edge_end_said = girl.gid
    $ set_scene_expression(girl, "shy" if _pcp_trait == "submissive" else "angry")
    $ Say_Line(girl, _tl(renpy.random.choice(_POST_CUM_STOP_PLEA[_pcp_trait])))
    menu:
        "Keep going":
            $ store._post_cum_result = "continue"
            $ Change_Status(girl, "Love", 5)
            $ Say_Line(girl, _tl(renpy.random.choice(_POST_CUM_STOP_PLEA[_pcp_trait + "_kept"])))
        "No. We're done.":
            $ Change_Status(girl, "Obed", 5)
            $ Change_Status(girl, "Love", trait_love_loss(girl, -3))
            $ Say_Line(girl, _tl(renpy.random.choice(_POST_CUM_STOP_PLEA[_pcp_trait + "_denied"])))
            if _pcp_trait == "femdom":
                $ femdom_react_refused(girl, "stop", scene_type)
    $ set_scene_expression(girl, "normal")
    return
