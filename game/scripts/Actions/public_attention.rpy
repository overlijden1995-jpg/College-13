# ============================================================
# PUBLIC ATTENTION SYSTEM (Unified Crowd Level 0-100)
# Tracks how much attention the player and girl draw during
# sex scenes. When attention reaches the threshold, an observer
# catches them. Works for all location types: public,
# semi-private (showers, dressing rooms), and private (rooms).
# ============================================================

init python:

    # ============================================================
    # CROWD CONFIG — crowd level ranges (0-100) by location + time
    # Randomized from (min, max) once at scene start.
    # 0 = completely empty, 100 = instant catch.
    # TimeIndex: 0=morning, 1=afternoon, 2=evening, 3=night
    # ============================================================

    CROWD_CONFIG = {
        # Public locations (open, people see directly)
        "campus":    {0: (15, 40), 1: (30, 60), 2: (20, 45), 3: (5, 15)},
        "pool":      {0: (10, 30), 1: (25, 50), 2: (20, 40), 3: (0, 5)},
        "gym":       {0: (15, 35), 1: (30, 55), 2: (20, 40), 3: (0, 5)},
        "classroom": {0: (40, 70), 1: (50, 80), 2: (25, 50), 3: (0, 5)},
        "hall":      {0: (15, 35), 1: (20, 40), 2: (10, 25), 3: (5, 15)},
        "mall":      {0: (20, 45), 1: (40, 70), 2: (35, 60), 3: (0, 0)},
        # Semi-private locations (enclosed, people hear but don't see)
        "showers":        {0: (5, 15), 1: (10, 25), 2: (5, 15), 3: (0, 5)},
        "shower":         {0: (5, 15), 1: (10, 25), 2: (5, 15), 3: (0, 5)},
        "dressing_room":  {0: (10, 20), 1: (15, 30), 2: (10, 20), 3: (0, 0)},
        "restaurant_restroom": {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)},
    }

    # ============================================================
    # LOCATION CATCH CONFIG — per-location observer & consequences
    # ============================================================

    LOCATION_CATCH_CONFIG = {
        "campus": {
            "observer": _("Teacher"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        },
        "pool": {
            "observer": _("Coach"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        },
        "gym": {
            "observer": _("Coach"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        },
        "classroom": {
            "observer": _("Teacher"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        },
        "hall": {
            "observer": _("Teacher"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        },
        "mall": {
            "observer": _("Security Guard"),
            "study_penalty": False,
            "kicked_out": True,
            "go_to": "campus",
            "semi_private": False,
        },
        "showers": {
            "observer": _("Supervisor"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": True,
        },
        "shower": {
            "observer": _("Supervisor"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": True,
        },
        "dressing_room": {
            "observer": _("Attendant"),
            "study_penalty": False,
            "kicked_out": True,
            "go_to": "mall",
            "semi_private": True,
        },
        "restaurant_restroom": {
            "observer": _("Waiter"),
            "study_penalty": False,
            "kicked_out": True,
            "go_to": "campus",
            "semi_private": True,
        },
    }

    # Attention threshold — when reached, they get caught
    _ATTENTION_MAX = 100

    # Warning thresholds (percentage of max)
    _ATTENTION_WARN_LOW = 30
    _ATTENTION_WARN_MID = 60
    _ATTENTION_WARN_HIGH = 85

    # Base attention per action type
    _ATTENTION_BASE = {
        "keep_going":  8,
        "speed_up":   15,
        "speed_down":  3,
        "strip":      12,
        "start_scene": 5,
    }

    # Reincidence study penalty escalation
    _CAUGHT_STUDY_PENALTIES = [5, 10, 15]

    # ============================================================
    # WARNING TEXT — 3 tiers per location (low / mid / high)
    # ============================================================

    _ATTENTION_WARNINGS = {
        "campus": [
            _("A few students walking by glance in your direction."),
            _("People nearby are whispering and looking over at you two."),
            _("A small crowd has gathered. Someone pulls out their phone. This is getting dangerous."),
        ],
        "pool": [
            _("The sound of splashing echoes. Someone at the far end of the pool looks your way."),
            _("A couple of swimmers have stopped to stare. The water has gone quiet."),
            _("Everyone at the pool is watching. You hear someone say 'Is that...?' You need to stop."),
        ],
        "gym": [
            _("Someone on the treadmill takes their earbuds out, looking confused."),
            _("Several gym-goers have stopped their workouts. The weight room has gone oddly silent."),
            _("Almost everyone in the gym is staring. Someone just left in a hurry, probably to tell someone."),
        ],
        "classroom": [
            _("A student in the back row turns around, eyes wide."),
            _("Half the class is pretending not to watch. The other half isn't pretending."),
            _("The entire classroom is dead silent. Everyone is staring. You hear footsteps in the hallway."),
        ],
        "hall": [
            _("A passing student does a double take."),
            _("People in the hallway are slowing down, pretending to check their phones."),
            _("A group of students has stopped completely. One of them is giggling nervously. This won't stay quiet."),
        ],
        "mall": [
            _("A shopper passing by does a double take and walks faster."),
            _("Several people have stopped browsing. A store clerk is watching with wide eyes."),
            _("The entire area has gone quiet. Someone is pointing. A security guard reaches for his radio."),
        ],
        "showers": [
            _("You hear the water in the next stall turn off. There's a pause... then it turns back on."),
            _("The shower curtain in the neighboring stall shifts slightly. Was someone peeking?"),
            _("The showers have gone quiet. It feels like everyone stopped to listen. You hear whispers near the entrance."),
        ],
        "shower": [
            _("You hear the water in the next stall turn off. There's a pause... then it turns back on."),
            _("The shower curtain in the neighboring stall shifts slightly. Was someone peeking?"),
            _("The showers have gone quiet. It feels like everyone stopped to listen. You hear whispers near the entrance."),
        ],
        "dressing_room": [
            _("You hear the click of heels outside the curtain. Someone pauses nearby."),
            _("A knock on the dressing room wall. 'Everything okay in there?' the attendant calls out."),
            _("The attendant is right outside. 'Other customers are complaining. I need you to finish up in there.'"),
        ],
    }

    # ============================================================
    # OBSERVER ARRIVAL TEXT — who shows up when caught
    # ============================================================

    _OBSERVER_ARRIVAL = {
        "campus": [
            _("A professor walking across the quad spots you and marches over furiously."),
            _("A professor rounds the corner and freezes. Then his face goes red with anger."),
            _("A teacher on their way to the parking lot stops dead in their tracks."),
        ],
        "pool": [
            _("The pool supervisor bursts through the locker room door, whistle in hand."),
            _("Coach walks out of his office and sees you through the glass. He storms over."),
            _("The lifeguard blows her whistle so hard it echoes off the walls."),
        ],
        "gym": [
            _("Coach slams the equipment room door open. He was in there the whole time."),
            _("The PE teacher walks in carrying new dumbbells. They hit the floor with a clang."),
            _("A teacher doing their evening jog stops at the gym entrance, jaw dropping."),
        ],
        "classroom": [
            _("The classroom door swings open. The professor walks in early for the next class."),
            _("A teacher passing by hears the noise, opens the door, and finds you mid-act."),
            _("The janitor opens the door to clean the room. His mop clatters to the floor."),
        ],
        "hall": [
            _("A professor steps out of their office and catches you right there in the hallway."),
            _("The vice-principal rounds the corner carrying a stack of papers. They scatter everywhere."),
            _("A teacher coming back from lunch spots you and nearly drops their coffee."),
        ],
        "mall": [
            _("A mall security guard rounds the corner and stops dead. His walkie-talkie crackles."),
            _("The store manager steps out and catches you. She reaches for the phone immediately."),
            _("A security guard shines his flashlight your way. 'Hey! What the hell are you doing?!'"),
        ],
        "showers": [
            _("The dorm supervisor barges into the shower area after students reported the noise."),
            _("A student runs to get the supervisor. Moments later, the stall door is pulled open."),
            _("The shower attendant storms in after hearing complaints. She finds you two mid-act."),
        ],
        "shower": [
            _("The dorm supervisor barges into the shower area after students reported the noise."),
            _("A student runs to get the supervisor. Moments later, the stall door is pulled open."),
            _("The shower attendant storms in after hearing complaints. She finds you two mid-act."),
        ],
        "dressing_room": [
            _("The attendant pulls the curtain open after repeated complaints from other customers."),
            _("The store manager herself comes over and yanks the dressing room curtain aside."),
            _("An attendant knocks hard on the door. 'That's IT. I'm opening this.' She does."),
        ],
    }

    # ============================================================
    # OBSERVER REACTIONS — generic lines (work for any authority)
    # ============================================================

    # CAUGHT_: interactions.rpy owns the name _OBSERVER_REACTIONS (the witness mood dict, init order Chat >
    # Actions): sharing it made random.choice run on the DICT here, KeyError: 0 on every max-attention catch
    # (tester 2026-10-10)
    _CAUGHT_OBSERVER_REACTIONS = [
        _("What on EARTH do you two think you're doing?!"),
        _("Are you SERIOUS right now?! HERE of all places?!"),
        _("I cannot believe what I'm seeing. This is absolutely unacceptable!"),
        _("You two! Stop that RIGHT NOW!"),
    ]

    # ============================================================
    # OBSERVER PUNISHMENT — per consequence type
    # ============================================================

    _OBSERVER_DISMISS = {
        "school": [
            _("Both of you, get dressed and go to your rooms. NOW."),
        ],
        "commercial": [
            _("Both of you, get dressed and get out of here. NOW."),
        ],
    }

    _OBSERVER_PENALTY_FIRST = {
        "school": _("Your grades on the next exam will be reduced as punishment. Don't let this happen again."),
        "commercial": _("You're banned from this place for the rest of the day. Don't come back."),
    }

    _OBSERVER_PENALTY_SECOND = {
        "school": _("This is the SECOND time I've had to deal with you two. The penalty will be much harsher."),
        "commercial": _("This is the SECOND time?! I'm calling the police if it happens again."),
    }

    _OBSERVER_PENALTY_THIRD = {
        "school": _("AGAIN?! I'm running out of patience. One more time and I'm taking this to the dean."),
        "commercial": _("AGAIN?! That's it. Security, escort them out. You're done here."),
    }

    # ============================================================
    # EXHIB CAUGHT LINES — girl dialogue when caught (trait-based)
    # ============================================================

    _EXHIB_CAUGHT_LINES = [
        _("Oh, sorry... I was almost there. Could you give us like two more minutes?"),
        _("Ugh, really? Right when it was getting good... Fine, fine."),
        _("Sorry... just a few more seconds would have been nice."),
        _("Aww, come on! We were putting on such a good show for everyone..."),
        _("You couldn't have waited just a LITTLE longer? I was so close..."),
    ]

    _FETISH_CAUGHT_LINES = [
        _("Mmm... getting caught is kind of the best part though, isn't it?"),
        _("Oh no, we got caught... my heart is racing so fast right now..."),
        _("Sorry... the risk of someone seeing us just made it feel SO much better..."),
        _("I knew someone would catch us eventually... and honestly? Worth it."),
        _("I... I can't help it. The thrill of doing it here is just..."),
    ]

    # ============================================================
    # SEMI-PRIVATE GIRL REACTIONS — during warnings in enclosed spaces
    # ============================================================

    _SEMI_PRIVATE_GIRL_SHY = [
        _("shhh! Someone's going to hear us!"),
        _("Wait... did you hear that? I think someone's there..."),
        _("Keep it down! These walls are thin!"),
        _("Oh god, what if someone walks in?!"),
    ]

    _SEMI_PRIVATE_GIRL_EXHIB = [
        _("Let them listen~"),
        _("Mmm... I don't care if someone hears."),
        _("The steam hides everything. Probably."),
        _("Someone peeking? Good for them."),
    ]

    # ============================================================
    # SEMI-PRIVATE AMBIENT FLAVOR — extra lines for atmosphere
    # (shown randomly between warnings in enclosed locations)
    # ============================================================

    _SEMI_PRIVATE_AMBIENT = [
        _("A soft giggle echoes from nearby. Someone definitely heard that."),
        _("You hear whispered voices near the entrance. 'Did you hear that?' 'Hear what?'"),
        _("Someone drops something nearby. The timing feels... suspicious."),
        _("A girl walks past and does a quick double take before hurrying away."),
        _("You catch a glimpse of someone's shadow lingering outside for a moment too long."),
        _("Through the steam, you notice someone peeking around the corner before ducking away."),
        _("It's hard to tell if anyone else is still here."),
        _("You hear footsteps approaching... then retreating. False alarm."),
        _("The background noise drowns out most sounds. At least you hope it does."),
    ]

    # ============================================================
    # FUNCTIONS
    # ============================================================

    def get_crowd_level(loc=None):
        """Return a crowd level (0-100) for the given location and current time.
        Randomized from the (min, max) range in CROWD_CONFIG.
        Rooms always return 0 (they use the NPC walk-in system instead)."""
        if loc is None:
            loc = getattr(store, "CurrentLocation", "room")
        ti = getattr(store, "TimeIndex", 0)
        cfg = CROWD_CONFIG.get(loc)
        if cfg is None:
            return 0
        rng = cfg.get(ti, (0, 0))
        if rng[0] >= rng[1]:
            return rng[0]
        return renpy.random.randint(rng[0], rng[1])

    def _get_catch_config(loc=None):
        """Return the LOCATION_CATCH_CONFIG entry for the given location."""
        if loc is None:
            loc = getattr(store, "CurrentLocation", "room")
        return LOCATION_CATCH_CONFIG.get(loc, {
            "observer": _("Teacher"),
            "study_penalty": True,
            "kicked_out": False,
            "go_to": "room",
            "semi_private": False,
        })

    def _get_penalty_type(loc=None):
        """Return 'school' or 'commercial' based on location config."""
        cfg = _get_catch_config(loc)
        if cfg.get("kicked_out", False):
            return "commercial"
        return "school"

    def public_attention_reset():
        """Reset attention at the start of a new sex scene.
        Skipped during threesome switches so risk carries over between girls."""
        if getattr(store, "_threesome_mode", False):
            debug_log("[PUBLIC] Skipping attention reset (threesome switch)")
            return
        store._public_attention = 0
        store._public_caught = False
        store._pa_warn_shown = 0
        store._pa_ambient_count = 0

    def public_attention_tick(girl, action="keep_going", speed=0):
        """
        Called each action tick during a sex scene.
        Uses store._crowd_level (set at scene start) as the multiplier.
        Returns True if they just got caught (attention >= max).
        """
        if getattr(store, "_scene_restricted", False):
            return False
        crowd = getattr(store, "_crowd_level", 0)
        if crowd <= 0:
            return False

        if getattr(store, "_public_caught", False):
            return False

        base = _ATTENTION_BASE.get(action, 8)
        mult = crowd / 50.0
        speed_bonus = speed * 2
        gain = int((base + speed_bonus) * mult)

        if gain < 1:
            gain = 1

        store._public_attention = getattr(store, "_public_attention", 0) + gain
        print("[PA] tick: action=%s speed=%d crowd=%d mult=%.2f gain=%d total=%d" % (action, speed, crowd, mult, gain, store._public_attention))

        # Trait-based lust bonuses for risky acts
        if girl.has_trait("exhibitionist"):
            girl.Lust = min(100, girl.Lust + 2)
        elif girl.has_trait("public_fetish"):
            girl.Lust = min(100, girl.Lust + 1)

        # Show warning hints at thresholds
        _pa_show_warning_if_needed(girl)

        # Semi-private ambient flavor (random, between warnings)
        _pa_semi_private_ambient(girl)

        # Check threshold
        if store._public_attention >= _ATTENTION_MAX:
            store._public_caught = True
            print("[PA] CAUGHT! attention=%d" % store._public_attention)
            return True

        return False

    def _pa_show_warning_if_needed(girl):
        """Show location-specific warning narration at attention thresholds.
        In semi-private locations, girl also reacts based on traits."""
        attn = getattr(store, "_public_attention", 0)
        shown = getattr(store, "_pa_warn_shown", 0)
        loc = getattr(store, "CurrentLocation", "room")
        warnings = _ATTENTION_WARNINGS.get(loc)
        if warnings is None:
            return

        _fired = False
        if shown < 1 and attn >= _ATTENTION_WARN_LOW:
            store._pa_warn_shown = 1
            renpy.say(None, _tl(warnings[0]))
            _fired = True
        elif shown < 2 and attn >= _ATTENTION_WARN_MID:
            store._pa_warn_shown = 2
            renpy.say(None, _tl(warnings[1]))
            _fired = True
        elif shown < 3 and attn >= _ATTENTION_WARN_HIGH:
            store._pa_warn_shown = 3
            renpy.say(None, _tl(warnings[2]))
            _fired = True

        # In semi-private locations, girl reacts to each warning
        if _fired:
            cfg = _get_catch_config(loc)
            if cfg.get("semi_private", False):
                if girl.has_trait("public_shy"):
                    _gl = _tl(renpy.random.choice(_SEMI_PRIVATE_GIRL_SHY))
                    Say_Line(girl, _gl)
                    if hasattr(girl, "discover"):
                        girl.discover("discovered_trait_public_shy")
                elif girl.has_trait("exhibitionist") or girl.has_trait("public_fetish"):
                    _gl = _tl(renpy.random.choice(_SEMI_PRIVATE_GIRL_EXHIB))
                    Say_Line(girl, _gl)
                    girl.Lust = min(100, girl.Lust + 2)
                    if hasattr(girl, "discover"):
                        if girl.has_trait("exhibitionist"):
                            girl.discover("discovered_trait_exhibitionist")
                        if girl.has_trait("public_fetish"):
                            girl.discover("discovered_trait_public_fetish")

    def _pa_semi_private_ambient(girl):
        """Random ambient flavor for semi-private locations (between warnings)."""
        loc = getattr(store, "CurrentLocation", "room")
        cfg = _get_catch_config(loc)
        if not cfg.get("semi_private", False):
            return

        _amb_count = getattr(store, "_pa_ambient_count", 0)
        if _amb_count >= 3:
            return

        if renpy.random.random() > 0.10:
            return

        store._pa_ambient_count = _amb_count + 1
        line = _tl(renpy.random.choice(_SEMI_PRIVATE_AMBIENT))
        renpy.say(None, line)

    def _caught_keeps_going(girl):
        """True if the girl would keep going when caught (exhib/public_fetish)."""
        return girl.has_trait("exhibitionist") or girl.has_trait("public_fetish")

    def _get_caught_penalty_index(girl):
        """Return how many times they've been caught before (0-based)."""
        return girl.GetActionCount("caught_public_sex")

    def _get_study_penalty(girl):
        """Return the study_level penalty based on reincidence."""
        idx = _get_caught_penalty_index(girl)
        if idx >= len(_CAUGHT_STUDY_PENALTIES):
            return _CAUGHT_STUDY_PENALTIES[-1]
        return _CAUGHT_STUDY_PENALTIES[idx]

    def _get_player_gf_not_involved(active_girl):
        """Return the player's GF if she exists and is NOT the active girl, else None.
        The rumor lines show her ON CAMPUS (hallway, classmates): a girlfriend who is away never qualifies."""
        for g in girls_reachable():
            if g.gid != active_girl.gid and hasattr(g, "is_dating_player") and g.is_dating_player():
                return g
        return None


# ============================================================
# CAUGHT IN LOCATION — called when attention >= max
# Label name kept for backward compatibility with existing calls
# ============================================================

label caught_in_public(girl, scene_type):

    $ _cap_is_shy = girl.has_trait("public_shy")
    $ _cap_is_exhib = girl.has_trait("exhibitionist")
    $ _cap_is_fetish = girl.has_trait("public_fetish")
    $ _cap_loc = CurrentLocation

    # Look up location-specific config
    python:
        _cap_cfg = _get_catch_config(_cap_loc)
        _cap_observer_name = _tl(_cap_cfg.get("observer", _("Teacher")))
        _cap_observer_char = Character(_cap_observer_name, color="#FF6666")
        _cap_penalty_type = _get_penalty_type(_cap_loc)
        _cap_has_study_penalty = _cap_cfg.get("study_penalty", True)
        _cap_is_kicked_out = _cap_cfg.get("kicked_out", False)
        _cap_go_to = _cap_cfg.get("go_to", "room")
        _cap_times_caught = _get_caught_penalty_index(girl)
        _cap_penalty = _get_study_penalty(girl) if _cap_has_study_penalty else 0

    # Register the action
    $ girl.RegisterAction("caught_public_sex")

    # Study penalty (school locations only)
    if _cap_has_study_penalty:
        $ Player.study_level = max(0, Player.study_level - _cap_penalty)
        $ girl.study_level = max(0, girl.study_level - _cap_penalty)

    # --- Observer arrival ---
    python:
        _arrival_lines = _OBSERVER_ARRIVAL.get(_cap_loc, [
            _("Someone spots you and storms over."),
        ])
        _cap_arrival = _tl(renpy.random.choice(_arrival_lines))

    "[_cap_arrival]"

    # --- Observer's initial reaction ---
    python:
        _cap_reaction = _tl(renpy.random.choice(_CAUGHT_OBSERVER_REACTIONS))
    $ renpy.say(_cap_observer_char, _cap_reaction)

    # --- Girl's reaction based on traits ---
    if _cap_is_shy:
        "She immediately freezes and pulls away."
        $ Say_Line(girl, _("Oh god... oh no no no..."))
        "She covers her face, mortified. She looks like she wants the ground to swallow her."
        $ Change_Status(girl, "Love", -15)
        $ Change_Status(girl, "Obed", 10)
        $ Change_Status(girl, "Inbt", 8)
        if hasattr(girl, "discover"):
            $ girl.discover("discovered_trait_public_shy")

    elif _cap_is_exhib or _cap_is_fetish:
        # She does NOT stop — the observer has to yell again
        python:
            _cap_narr = _tl(_("She doesn't stop. She heard the %s, but she keeps going as if nothing happened.")) % _cap_observer_name
        "[_cap_narr]"

        # Observer's second reaction — scene_type specific
        python:
            # the part she has on him, said in the professor's line: translated here (a .format slot shows it as it is)
            _body_part_map = {
                "bj": _("mouth"),
                "hj": _("hand"),
                "tj": _("chest"),
                "cowgirl": _("hips"),
                "reverse_cowgirl": _("hips"),
            }
            _body_part = _tl(_body_part_map.get(scene_type, _("body")))
            _gn = girl.Name
            _pn = store.Player.Name
            _teacher_yell = [
                _("{0}! Take your {1} off {2} RIGHT NOW! WHAT THE HELL?!"),
                _("{0}! Get your {1} off of him THIS INSTANT! ARE YOU OUT OF YOUR MIND?!"),
                _("{0}! Remove your {1} from that boy IMMEDIATELY! I SAID NOW!"),
            ]
            _cap_yell = _tl(renpy.random.choice(_teacher_yell)).format(_gn, _body_part, _pn)

        $ renpy.say(_cap_observer_char, _cap_yell)

        # NOW she stops — end the sex scene visually
        call _cum_dispatch_end(girl, scene_type, dress_up=False) from _call_end_caught

        "She finally pulls away, looking more annoyed than embarrassed."

        if _cap_is_exhib:
            $ Say_Line(girl, _tl(renpy.random.choice(_EXHIB_CAUGHT_LINES)))
            python:
                _cap_obs_narr = _tl(_("The %s's face turns an even deeper shade of red.")) % _cap_observer_name
            "[_cap_obs_narr]"
            if hasattr(girl, "discover"):
                $ girl.discover("discovered_trait_exhibitionist")
        else:
            $ Say_Line(girl, _tl(renpy.random.choice(_FETISH_CAUGHT_LINES)))
            python:
                _cap_obs_narr = _tl(_("The %s stares in disbelief.")) % _cap_observer_name
            "[_cap_obs_narr]"
            if hasattr(girl, "discover"):
                $ girl.discover("discovered_trait_public_fetish")

        $ Change_Status(girl, "Obed", 12)
        $ Change_Status(girl, "Inbt", 10)
        $ girl.Lust = min(100, girl.Lust + 10)

    else:
        # Normal girl — stops immediately, trait-aware reaction
        $ set_scene_expression(girl, "embarrassed", blush="2")
        "She pulls away from you immediately, face burning with shame."
        "There's no way to talk your way out of this."
        if girl.has_trait("hardcore_sex"):
            $ Say_Line(girl, _("Seriously?! We were just getting started and THIS happens?! Ugh, what a waste."))
            $ Change_Status(girl, "Love", -5)
        elif girl.has_trait("cum_slut") or (hasattr(girl, "Obed") and girl.Obed >= 700):
            $ Say_Line(girl, _("Oh god, that was so embarrassing... but... it was kind of exciting too, wasn't it?"))
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Change_Status(girl, "Love", -5)
        elif girl.has_trait("cute_sex") or girl.has_trait("loyal"):
            $ Say_Line(girl, _("I knew this was a bad idea... I KNEW it. What were we thinking?!"))
            $ Change_Status(girl, "Love", -15)
        elif girl.Love >= 500:
            $ Say_Line(girl, _("I can't believe we did this... I TOLD you this was risky!"))
            $ Change_Status(girl, "Love", -10)
        else:
            $ Say_Line(girl, _("This is YOUR fault. I never should have let you talk me into this."))
            $ Change_Status(girl, "Love", -15)
        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 5)

    # --- Observer's punishment ---
    python:
        _cap_dismiss = _tl(renpy.random.choice(_OBSERVER_DISMISS.get(_cap_penalty_type, _OBSERVER_DISMISS["school"])))
    $ renpy.say(_cap_observer_char, _cap_dismiss)

    if _cap_times_caught == 0:
        python:
            _cap_pen_line = _tl(_OBSERVER_PENALTY_FIRST.get(_cap_penalty_type, _OBSERVER_PENALTY_FIRST["school"]))
        $ renpy.say(_cap_observer_char, _cap_pen_line)
        if _cap_has_study_penalty:
            "You and [girl.Name] each lost {b}[_cap_penalty]{/b} study points."
    elif _cap_times_caught == 1:
        python:
            _cap_pen_line = _tl(_OBSERVER_PENALTY_SECOND.get(_cap_penalty_type, _OBSERVER_PENALTY_SECOND["school"]))
        $ renpy.say(_cap_observer_char, _cap_pen_line)
        if _cap_has_study_penalty:
            "You and [girl.Name] each lost {b}[_cap_penalty]{/b} study points."
    else:
        python:
            _cap_pen_line = _tl(_OBSERVER_PENALTY_THIRD.get(_cap_penalty_type, _OBSERVER_PENALTY_THIRD["school"]))
        $ renpy.say(_cap_observer_char, _cap_pen_line)
        if _cap_has_study_penalty:
            "You and [girl.Name] each lost {b}[_cap_penalty]{/b} study points."

    # --- GF suspicion: if the player has a GF who is NOT the girl involved ---
    python:
        _cap_gf = _get_player_gf_not_involved(girl)
    if _cap_gf is not None:
        $ _cap_susp_gain = 15 + (_cap_times_caught * 5)

        $ _cap_rumor_roll = renpy.random.randint(1, 5)
        if _cap_rumor_roll == 1:
            "Later that day, you notice [_cap_gf.Name] looking at her phone with a strange expression."
            "Word travels fast around campus. Your girlfriend has heard some... rumors about you."
        elif _cap_rumor_roll == 2:
            "By evening, [_cap_gf.Name] is unusually quiet. Someone must have told her what happened."
            "You catch her glancing at you with a mix of hurt and suspicion."
        elif _cap_rumor_roll == 3:
            "A classmate whispers something to [_cap_gf.Name] in the hallway. She turns to look at you."
            "Her eyes narrow. She's definitely heard something."
        elif _cap_rumor_roll == 4:
            "You overhear someone in the hall: \"Did you hear about [Player.Name] and [girl.Name]?\""
            "If that reached your ears, it definitely reached [_cap_gf.Name]'s."
        else:
            "[_cap_gf.Name] sends you a cold text: \"We need to talk later.\""
            "Rumors spread like wildfire on campus. She knows something happened."

        $ _cap_gf.suspicion = min(100, getattr(_cap_gf, "suspicion", 0) + _cap_susp_gain)

    # --- Full reset: dress girl, clear all sex state, send player away ---
    python:
        force_scene_reset(girl, angry_days=0, reason="caught_public")
        girl.loc = girl_home_loc(girl)
        hide_girl_sprite(girl)
        store.Party = []
        public_attention_reset()

    "You get dressed as fast as you can and leave, alone."

    $ navigate_to(_cap_go_to, None)
    call Set_Scene(entry=True) from _call_Set_Scene_caught_public

    jump main_loop
