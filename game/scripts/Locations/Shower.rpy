# ============================================================
# SHOWER SYSTEM (College Traits)
# ============================================================

default ShowerEntryPath = "direct"      # "direct", "open", "closed"
default ShowerEntryMode = "direct"      # "direct", "open", "enter", "knock"
default _girls_visited_night = set()
default _shower_spot = "showers"        # the SHOWER_SPOTS key the navigation sends to Shower_Entry
# One roll per spot per TIME SLOT (tester 2026-10-10: leaving and re-entering rerolled the girl AND her
# undress state, "she exists to be walked in on"): spot -> {"day","slot","gid","state","mast_rolled"}.
# gid None = the slot rolled empty and stays empty; "state" fills on the first state roll.
default _shower_slot_lock = {}
default _shower_locked_tries = 0        # how many times the player tried the locked door this visit

# SHOWER_SPOTS is read by the outfit / audio / time code of other files: defined before them (init -1)
init -1 python:

    # ---- Shower spots: every place found like the campus showers (Shower_Entry / Shower_Loop) ----
    # The navigation sets _shower_spot before `jump Shower_Entry`; from there on the spot is CurrentLocation.
    #   exit   : where "Leave" / "I will come back later" goes (a label)
    #   paths  : weights of the way he finds her: "direct" (she is already inside, he walks in), "open" (the door
    #            is open: he sees her changing / naked / dressed), "closed" (door closed, water running)
    #   locked : the closed door is locked: "Enter without knocking" only finds the handle stuck
    #   pick   : who can be in there. "campus" = one random girl on campus (50% each, pick_girls_for_showers);
    #            "schedule" = only the girl her schedule puts there right now (the one who lives there)
    #   walkin_from : where a girl must be to walk in on his solo shower (shower_walkin_pool); None = any girl on
    #            campus (the walk-in teleports her there)
    #   text   : the lines that name the place (shower_spot_text; a key the spot lacks falls back to "showers")
    SHOWER_SPOTS = {
        "showers": {
            "exit": "Campus_Entry",
            "paths": (("direct", 40), ("open", 30), ("closed", 30)),
            "locked": False,
            "pick": "campus",
            "walkin_from": None,
            "text": {
                "empty": _("You head to the showers. It looks like nobody else is here right now."),
                "with_follower": _("You head to the showers with [main_girl.Name]."),
                "direct": _("As you step into the showers, you realize [main_girl.Name] is already here."),
                "open": _("You arrive at the showers and notice the door is already open."),
                "closed": _("You arrive at the showers. The door is closed, and you can hear the water running inside."),
                "leave": _("You decide to leave the showers and go back to campus."),
                "leave_doorway": _("You step back from the doorway and leave the showers behind."),
                "nobody": _("You do not hear or see anyone else inside the showers."),
                "mast_arrive": _("You head to the showers and hear the water running."),
                "mast_leave": _("You silently back away and leave the showers."),
                "girl_no_reason": _("Right. Because you always walk into the showers for no reason."),
                "girl_check_on": _("You 'check on me' in the showers a lot, huh?"),
                "girl_here": _("Here? In the showers? ...What did you have in mind?"),
            },
        },
        # The bathroom of the father's apartment (APARTMENT_ROOMS): the door is open, or locked
        "apartment_shower": {
            "exit": "Apartment_Entry",
            "paths": (("direct", 30), ("open", 30), ("closed", 40)),
            "locked": True,
            "pick": "schedule",
            "walkin_from": ("apartment", "apartment_room"),   # she is home, in another room
            "text": {
                "empty": _("You step into the bathroom. Nobody's in here right now."),
                "with_follower": _("You head to the bathroom with [main_girl.Name]."),
                "direct": _("You open the bathroom door and realize [main_girl.Name] is already inside."),
                "open": _("You walk toward the bathroom and notice the door is wide open."),
                "closed": _("The bathroom door is closed, and you can hear the water running inside."),
                "locked": _("You try the handle. The door is locked."),
                "leave": _("You leave the bathroom."),
                "leave_doorway": _("You step back from the doorway and leave the bathroom."),
                "nobody": _("You do not hear or see anyone inside the bathroom."),
                "mast_arrive": _("You walk toward the bathroom and hear the water running."),
                "mast_leave": _("You silently back away from the bathroom door."),
                "girl_no_reason": _("Right. Because you always walk into the bathroom for no reason."),
                "girl_check_on": _("You 'check on me' in the bathroom a lot, huh?"),
                "girl_here": _("Here? In the bathroom? ...What did you have in mind?"),
            },
        },
    }

    def shower_knock_reward(girl, amount):
        """The Love of a knock on her shower door lands once per time slot per girl: knocking again in the
        same slot keeps her reaction but gives nothing (the knock was farmable, tester 2026-10-10)."""
        _slot = (store.Day, store.TimeIndex)
        if getattr(girl, "_knock_reward_slot", None) == _slot:
            print("[SHOWER] knock farm guard: %s already rewarded this slot %s" % (girl.gid, (_slot,)))
            return
        girl._knock_reward_slot = _slot
        Change_Status(girl, "Love", amount)

    # She hears him try the locked door (a locked spot, "Enter without knocking")
    _SHOWER_LOCKED_LINES = [
        _("Hey! Occupied!"),
        _("It's locked for a reason! Give me a minute!"),
        _("Knock first! I'm in the shower!"),
    ]

    def shower_spot_loc():
        """The shower spot he is in (CurrentLocation), the campus showers when he is in none."""
        _loc = getattr(store, "CurrentLocation", "")
        return _loc if _loc in SHOWER_SPOTS else "showers"

    def shower_spot_text(key):
        """A line of the shower spot he is in (English: Narration / Say_Line translate it)."""
        return SHOWER_SPOTS[shower_spot_loc()]["text"].get(key) or SHOWER_SPOTS["showers"]["text"][key]

    def shower_spot_exit():
        """The label "Leave" jumps to from the shower spot he is in."""
        return SHOWER_SPOTS[shower_spot_loc()]["exit"]

    def shower_walkin_pool(spot):
        """The girls who could walk in on his solo shower at `spot` (SHOWER_SPOTS "walkin_from")."""
        _from = SHOWER_SPOTS.get(spot, SHOWER_SPOTS["showers"]).get("walkin_from")
        if _from:
            return [g for g in girls_reachable() if g.loc in _from]
        return girls_on_campus()

    def shower_spot_path(spot):
        """How he finds her this time (a key of the spot's "paths" weights)."""
        _paths = SHOWER_SPOTS[spot]["paths"]
        _roll = renpy.random.randint(1, sum(_w for _p, _w in _paths))
        for _p, _w in _paths:
            _roll -= _w
            if _roll <= 0:
                return _p
        return _paths[-1][0]

    def shower_door_shut(girl, why=""):
        """He saw her (direct / open door) and left without staying: she shuts the door behind him.
        The slot lock's "path" becomes "closed", so coming back in the SAME time slot finds a closed
        door instead of the same discovery scene (author 2026-10-11). One exception, hers by
        dialogue: an exhibitionist leaves the door exactly as it was ("The door will still be open")."""
        if hasattr(girl, "has_trait") and girl.has_trait("exhibitionist"):
            print("[SHOWER] door stays open: %s is an exhibitionist" % getattr(girl, "gid", "?"))
            return
        _spot = shower_spot_loc()
        _l = store._shower_slot_lock.get(_spot)
        if (_l and _l.get("day") == store.Day and _l.get("slot") == store.TimeIndex
                and _l.get("gid") == getattr(girl, "gid", None)):
            _l["path"] = "closed"
            print("[SHOWER] %s: %s shut the door behind him (%s): the next visit this slot finds it closed" % (
                _spot, girl.gid, why or "he left"))

init python:
    import random as _shower_random

    # Máximo geral de garotas que podem estar nos chuveiros
    MAX_SHOWER_GIRLS_IN_SHOWERS = 1

    # ---- Trait-specific shower caught lines ----
    _SHOWER_CAUGHT_LINES = {
        # Caught nude... angry/covering (low approval)
        ("nude_angry", "hardcore_sex"): [
            _("Get the hell out! I don't care what you've seen, LEAVE!"),

            _("You've got three seconds before I throw something at you."),

        ],
        ("nude_angry", "cute_sex"): [
            _("KYAA! D-don't look! Please don't look at me!"),

            _("No no no! This is so embarrassing! Turn around!"),

        ],
        ("nude_angry", "public_shy"): [
            _("What if someone else comes in?! Close the door! GET OUT!"),

            _("Oh god, did anyone else see?! Please tell me no one saw!"),

        ],

        # Caught nude... chill (high approval + seen before)
        ("nude_chill", "hardcore_sex"): [
            _("Again? At this point you're doing it on purpose. Whatever."),

            _("You've seen it all before. Take a picture, it lasts longer."),

        ],
        ("nude_chill", "cute_sex"): [
            _("I-I'm used to you seeing me by now... just don't stare TOO much."),

            _("You've seen me like this before... it's still embarrassing though."),

        ],
        ("nude_chill", "exhibitionist"): [
            _("Mmm, enjoy the show? I left the door unlocked on purpose."),

            _("I was hoping you'd walk in. Like what you see?"),

        ],
        ("nude_chill", "cheater"): [
            _("My {hint}boyfriend{/hint} never gets this kind of view. Lucky you."),

            _("If my {hint}boyfriend{/hint} walked in instead of you, that'd be a problem."),

        ],

        # Caught nude... sexy (high approval, flirty)
        ("nude_sexy", "hardcore_sex"): [
            _("Like what you see? Get in here or get out."),

            _("Stop staring and do something about it."),

        ],
        ("nude_sexy", "cute_sex"): [
            _("I... I don't mind if it's you seeing me..."),

            _("You make me feel safe even when I'm... like this."),

        ],
        ("nude_sexy", "exhibitionist"): [
            _("I don't just want you to look. I want you to enjoy it."),

            _("The door wasn't locked for a reason, you know."),

        ],
        ("nude_sexy", "virgin"): [
            _("This is the most anyone has ever seen of me... and it's you."),

            _("I've never been naked in front of someone before... is this okay?"),

        ],

        # "What did you think" responses
        ("view_amazing", "cute_sex"): [
            _("R-really? You think I look amazing...? *hides face*"),

            _("Don't say things like that when I'm barely dressed..."),

        ],
        ("view_amazing", "hardcore_sex"): [
            _("Obviously. Now stop being weird about it."),

            _("You'd better remember that view. It doesn't come free."),

        ],
        ("view_amazing", "exhibitionist"): [
            _("I know. And I love that you can't look away."),

            _("The look on your face is everything I wanted."),

        ],
        ("view_more", "exhibitionist"): [
            _("Maybe next time I'll give you a private show."),

            _("You want more? I can arrange that."),

        ],
        ("view_more", "cute_sex"): [
            _("M-more?! You're so greedy... but maybe... someday."),

            _("That's... a lot to ask... but I'm not saying never."),

        ],
        ("view_more", "virgin"): [
            _("I've never shown anyone more than this before..."),

            _("You want to see more of me? I... I'll think about it."),

        ],

        # ---- camera_hater ----
        ("nude_angry", "camera_hater"): [
            _("Are you alone?! Please tell me nobody else is out there!"),

            _("Close the door! NOW! If anyone else sees me like this I swear..."),

            _("You better not have your phone on you. I mean it."),

        ],
        ("nude_chill", "camera_hater"): [
            _("It's just you, right? ...Okay. Just do not tell anyone you saw me like this."),

            _("Fine, you've seen me. But if I ever find out you told someone, we're done."),

        ],
        ("nude_sexy", "camera_hater"): [
            _("This stays between us. No one else gets to see me like this. Only you."),

            _("I trust you enough to let you look... but if you ever share this, I will end you."),

        ],
        ("view_amazing", "camera_hater"): [
            _("T-thanks... just keep it to yourself, okay? I do not want people talking."),

            _("You really think so? Just... promise me this stays between us."),

        ],
        ("view_more", "camera_hater"): [
            _("More? Maybe... but only if I know for sure no one else will ever find out."),

            _("I might show you more someday. Behind a locked door. With the curtains drawn."),

        ],

        # ---- cum_slut ----
        ("nude_angry", "cum_slut"): [
            _("Hey! At least buy me dinner first... actually, no, just get in here or get out."),

            _("You scared me! But honestly, I do not really care if you see me naked."),

        ],
        ("nude_chill", "cum_slut"): [
            _("Oh please, like a little nudity is going to bother me. Enjoy the view."),

            _("Bodies are bodies. I am not shy about mine. Are you shy about yours?"),

            _("You act like you have never seen a naked woman before. Relax."),

        ],
        ("nude_sexy", "cum_slut"): [
            _("Like what you see? Because I can think of a few things we could do about it."),

            _("Stop pretending to be embarrassed. We both know what you want."),

            _("You know, the shower is big enough for two..."),

        ],
        ("view_amazing", "cum_slut"): [
            _("I know. And trust me, I look even better up close."),

            _("Amazing? Honey, you have not seen anything yet."),

        ],
        ("view_more", "cum_slut"): [
            _("More? All you had to do was ask. I have no problem with that."),

            _("Get in here and I will show you everything you want to see."),

            _("I was hoping you would say that. Come closer."),

        ],

        # ---- hate_cum ----
        ("nude_angry", "hate_cum"): [
            _("Ew, do NOT look at me! This is a private space! Out! OUT!"),

            _("This is so gross... you just standing there staring at my body. Leave!"),

            _("I do not want anyone seeing me like this. It is disgusting. Go away."),

        ],
        ("nude_chill", "hate_cum"): [
            _("Fine, you have seen me. Can you at least not... leer? It is uncomfortable."),

            _("I am not thrilled about this, but whatever. Just keep your distance."),

        ],
        ("nude_sexy", "hate_cum"): [
            _("I suppose I do not mind you seeing me... just do not make it weird, okay?"),

            _("Looking is fine. Just... keep your hands and everything else to yourself."),

        ],
        ("view_amazing", "hate_cum"): [
            _("Thanks, I guess. Just do not get any gross ideas about it."),

            _("I appreciate the compliment, but please do not make this into something physical."),

        ],
        ("view_more", "hate_cum"): [
            _("More? Let us not get carried away. Looking is one thing, but that is the line."),

            _("I will think about it. But if things get messy, I am done. Literally."),

        ],

        # ---- loyal ----
        ("nude_angry", "loyal"): [
            _("I have a {hint}boyfriend{/hint}! You cannot just walk in on me like this!"),

            _("What would my {hint}boyfriend{/hint} say if he knew you saw me naked?! Get out!"),

            _("This is so wrong... I should not be seen like this by anyone but him."),

        ],
        ("nude_chill", "loyal"): [
            _("My {hint}boyfriend{/hint} would not love this, but... I trust you not to make it weird."),

            _("I know this looks bad, but it was an accident. Let us just forget it happened."),

        ],
        ("nude_sexy", "loyal"): [
            _("I should not be letting you see me like this... but I cannot help it."),

            _("My {hint}boyfriend{/hint} would hate this. So why does part of me not care right now?"),

            _("This is wrong... but the way you look at me makes me forget that."),

        ],
        ("view_amazing", "loyal"): [
            _("You... you should not say things like that to me. I am with someone."),

            _("That is sweet, but... I have a {hint}boyfriend{/hint}. I should not enjoy hearing that."),

        ],
        ("view_more", "loyal"): [
            _("More? I... I cannot. I have someone. Even if part of me wants to."),

            _("You are making this really hard for me. I am supposed to be loyal..."),

        ],

        # ---- public_fetish ----
        ("nude_angry", "public_fetish"): [
            _("Oh my god, you actually walked in! My heart is racing... and not just from fear."),

            _("You scared me! But... honestly? The rush of almost being caught is kind of exciting."),

        ],
        ("nude_chill", "public_fetish"): [
            _("You know, the fact that anyone could walk in right now makes this way more fun."),

            _("I left the door unlocked on purpose. The thrill of being caught is half the fun."),

            _("Honestly? I was hoping someone would walk in. Lucky me, it is you."),

        ],
        ("nude_sexy", "public_fetish"): [
            _("The door is wide open and I am naked. Does that excite you as much as it excites me?"),

            _("Anyone could see us right now. That thought drives me crazy in the best way."),

            _("Imagine if someone else walked in right now... does that not make your heart race?"),

        ],
        ("view_amazing", "public_fetish"): [
            _("Knowing you saw me like this in a place where anyone could catch us? That is the best part."),

            _("The fact that this is a public shower makes it ten times hotter, does it not?"),

        ],
        ("view_more", "public_fetish"): [
            _("More? Right here where anyone could see? ...Yes. Absolutely yes."),

            _("If you want more, leave the door open. I want the risk."),

            _("The more public, the better. I am not even kidding."),

        ],
    }

    _SHOWER_DISCOVER = {
        "exhibitionist": "discovered_trait_exhibitionist",
        "public_fetish": "discovered_trait_public_fetish",
        "camera_lover": "discovered_trait_camera_lover",
        "camera_hater": "discovered_trait_camera_hater",
        "cum_slut": "discovered_trait_cum_slut",
        "hate_cum": "discovered_trait_hate_cum",
        "loyal": "discovered_trait_loyal",
        "hardcore_sex": "discovered_trait_hardcore_sex",
        "cute_sex": "discovered_trait_cute_sex",
        "public_shy": "discovered_trait_public_shy",
        "cheater": "discovered_trait_cheater",
        "virgin": "discovered_trait_virgin",
    }

    def _shower_caught_line(girl, context):
        """Try to get a trait-specific shower caught line."""
        if not hasattr(girl, "has_trait"):
            return None
        trait_order = [
            "exhibitionist", "public_fetish", "camera_lover", "camera_hater",
            "cum_slut", "hate_cum", "loyal", "hardcore_sex", "cute_sex",
            "public_shy", "cheater", "virgin",
        ]
        # the loyal / cheater pools say "my boyfriend" / "him": only true with a male NPC partner
        _has_bf = (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
                   and not girl.get_flag("partner_is_female"))
        for t in trait_order:
            if t in ("loyal", "cheater") and not _has_bf:
                if girl.has_trait(t):
                    print("[SHOWER] %s: %s caught pool skipped for %s (no boyfriend)" % (getattr(girl, "gid", "?"), t, context))
                continue
            if girl.has_trait(t) and (context, t) in _SHOWER_CAUGHT_LINES:
                if t in _SHOWER_DISCOVER and hasattr(girl, "discover"):
                    girl.discover(_SHOWER_DISCOVER[t])
                return renpy.random.choice(_SHOWER_CAUGHT_LINES[(context, t)])
        return None

    # ---- Found in the shower by a girl with a STORY (story_steps.rpy): her step decides, never her stats ----
    # The approval tree of Shower_Caught_Event (shy / bemused / sexy by stats, then CaughtExposureReaction's "do you
    # like what you see") is a college girl who may warm up. A girl with a story reacts as her step is
    # (_shower_story_caught), and her step decides the door when he knocks. Keyed by the step ids of STORY_LADDERS:
    #   face        her face through it (only faces every girl has)
    #   cover       she wraps herself in a towel when he finds her exposed
    #   out         after his answer she throws him out of the bathroom (else he stays: Shower_Loop)
    #   knock       he knocks on the closed door: "refuse" (it stays shut), "towel" / "nude" (she opens like that)
    #   caught      her stats for being found
    #   narr / narr_towel   what she does when he finds her exposed / already in a towel
    #   choices     his answers in menu order: (route, his line, her stats). The route names her reply pool
    # Her lines are rod_lines pools (hers, then her role's), "<key>.<step id>" with trait variants first:
    #   shower_caught.<cat>              her first word (cat of _shower_state_cat: nude / partial / towel)
    #   shower_caught.reply.<route>      her answer to his
    #   shower_knock / shower_knock_open what she says through the closed door / when she opens it
    # A step without an entry, or a key without a pool, keeps the normal reaction (dressed: nothing to hide).
    SHOWER_STORY_STEPS = {
        # nothing between them: outrage and authority, and he is out
        "cold": {
            "face": "angry", "cover": True, "out": True, "knock": "refuse",
            "caught": {"Love": -2},
            "narr": _("She grabs a towel and wraps it around herself without hurrying, never once taking her eyes off you."),
            "narr_towel": _("She pulls her towel tighter. Her eyes never leave you."),
            "choices": (
                ("love", _("Sorry. I didn't know you were in here."), {"Love": 2}),
                ("obed", _("I'm not going to apologize."), {"Obed": 3, "Love": -2}),
                ("inbt", _("Relax. It's just a body."), {"Inbt": 3, "Love": -2}),
            ),
        },
        # she lets him look, exactly as long as SHE decides, then sends him away
        "she_decides": {
            "face": "smug", "cover": True, "out": True, "knock": "refuse",
            "caught": {"Lust": 3},
            "narr": _("She takes her time reaching for the towel. She decides exactly when you've seen enough."),
            "narr_towel": _("She doesn't tighten her towel. She just raises an eyebrow and waits."),
            "choices": (
                ("love", _("Sorry. I'll give you some privacy."), {"Love": 3}),
                ("obed", _("I'm staying right here."), {"Obed": 4}),
                ("inbt", _("Don't cover up on my account."), {"Inbt": 4, "Lust": 2}),
            ),
        },
        # she doesn't cover, and he stays
        "giving_in": {
            "face": "sexy", "cover": False, "out": False, "knock": "towel",
            "caught": {"Lust": 6},
            "narr": _("She doesn't cover herself. She just watches you watching her."),
            "narr_towel": _("Her hand rests on the knot of her towel. She doesn't tighten it."),
            "choices": (
                ("love", _("You're beautiful, you know that?"), {"Love": 4, "Lust": 3}),
                ("obed", _("Leave the towel. Let me look at you."), {"Obed": 4, "Lust": 3}),
                ("inbt", _("Anyone could walk in on us like this."), {"Inbt": 4, "Lust": 3}),
            ),
        },
        # his: she wants him in there
        "his": {
            "face": "happy", "cover": False, "out": False, "knock": "nude",
            "caught": {"Lust": 8, "Love": 2},
            "narr": _("She smiles when she sees it's you, and doesn't reach for the towel at all."),
            "narr_towel": _("She smiles when she sees it's you, and her fingers find the knot of her towel."),
            "choices": (
                ("love", _("You look incredible."), {"Love": 5, "Lust": 4}),
                ("obed", _("Turn around. Slowly."), {"Obed": 5, "Lust": 4}),
                ("inbt", _("Leave the door open."), {"Inbt": 5, "Lust": 4}),
            ),
        },
    }

    def shower_story_step(girl):
        """How she takes being found in the shower on her story step (SHOWER_STORY_STEPS), or None (no story)."""
        _sid = story_voice_id(girl)
        return SHOWER_STORY_STEPS.get(_sid) if _sid else None

    def shower_story_line(girl, key):
        """Her shower line of her story step for `key`, or None (no story, no entry for her step, or no pool)."""
        if shower_story_step(girl) is None:
            return None
        return story_rod_line(girl, _story_keys_with_traits(girl, "%s.%s" % (key, story_voice_id(girl))))

    # --------------------------------------------------------
    # Helper function: check if we should just chill
    # --------------------------------------------------------
    def shower_chill(ap_val, total_seen_val):
        # Alta aprovação + player já viu boobs/pussy pelo menos 1 vez
        return (ap_val is not None) and (ap_val >= 3) and (total_seen_val >= 1)

    # --------------------------------------------------------
    # Encounter bracket for low-tier shower progression
    # 0 = first ever, 1 = second time, 2 = familiar (3-4), 3 = routine (5+)
    # --------------------------------------------------------
    def _shower_enc_bracket(count):
        if count <= 1: return 0
        if count == 2: return 1
        if count <= 4: return 2
        return 3

    # --------------------------------------------------------
    # Encounter-progression lines (low-tier girls, tiers 0-1)
    # Keys: (bracket, state_category, mood)
    # state_category: "nude", "partial", "towel", "dressed"
    # mood: "angry", "shy", "resigned", "familiar", "warming"
    # --------------------------------------------------------
    _SHOWER_ENC_LINES = {
        # ── Bracket 0: FIRST TIME EVER ──
        # Nude
        (0, "nude", "angry"): [
            _("What the--?! GET OUT! I'm NAKED!"),

            _("Are you INSANE?! Close your eyes! CLOSE THEM!"),

            _("Oh my god! Who just walks in like that?! LEAVE!"),

            _("HEY! What do you think you are doing?! I am COMPLETELY naked!"),

            _("Do you not know what a LOCKED DOOR means?! Out! NOW!"),

        ],
        (0, "nude", "shy"): [
            _("Oh my god... n-nobody has ever seen me like this before... please don't look!"),

            _("I... I can not believe this is happening... please just turn around!"),

            _("Kyaa! T-this is the first time anyone has... please close the door!"),

            _("N-no! Don't look! I was not expecting anyone! This is so embarrassing!"),

            _("P-please... just... I need a second... don't stare..."),

        ],
        (0, "nude", "chill"): [
            _("Oh! Well... this is a first. You could have warned me, you know."),

            _("Huh. First time someone has walked in on me like this. Bold move."),

            _("Well, there is a first time for everything, I guess. Do not make it weird."),

            _("Oh. Hi. Well, now you have seen everything. Happy?"),

        ],
        # Partial (underwear/missing_top/missing_bottom)
        (0, "partial", "angry"): [
            _("HEY! I am not dressed! Get out of here!"),

            _("What are you doing?! I am changing! Turn around NOW!"),

            _("Oh my god, do you not know how to knock?! I am half naked!"),

            _("Excuse me?! I am in the middle of changing! LEAVE!"),

        ],
        (0, "partial", "shy"): [
            _("Oh! I... I was not expecting anyone... this is so embarrassing..."),

            _("P-please do not stare... I was not ready for this..."),

            _("I can not believe you just walked in... at least look away!"),

            _("I... this is not what it looks like! I mean... I was just changing!"),

        ],
        (0, "partial", "chill"): [
            _("Oh. Well, it is just underwear. Could be worse, right?"),

            _("First time you have caught me like this. Enjoy the preview, I guess."),

            _("Relax, it is not like you have never seen underwear before. ...Right?"),

        ],
        # Towel
        (0, "towel", "neutral"): [
            _("Oh! I was not expecting company. Good thing I grabbed a towel."),

            _("Well, at least I am covered. You could have knocked, though."),

            _("Ugh, you scared me! Lucky for you I already had a towel on."),

            _("Whoa! Good thing I am a fast grabber. Towel: secured."),

        ],
        # Dressed
        (0, "dressed", "neutral"): [
            _("Oh, hey. I was just about to start. You caught me before anything happened."),

            _("Good timing. Or bad timing, depending on what you were hoping to see."),

            _("I just got here too. Nothing exciting to see... yet."),

            _("Still fully dressed, sorry. You will have to use your imagination."),

        ],

        # ── Bracket 1: SECOND TIME ──
        (1, "nude", "angry"): [
            _("AGAIN?! Seriously?! Did you not learn anything from last time?!"),

            _("You are doing this on PURPOSE! I know it! Get OUT!"),

            _("Not again! Do you have some kind of radar for when I am naked?!"),

            _("Twice now?! What is WRONG with you?! Give me some privacy!"),

            _("I KNEW I should have locked that door. Get out!"),

        ],
        (1, "nude", "shy"): [
            _("Not again... I thought I would be more careful this time..."),

            _("Y-you saw me before and now again... am I cursed or something?"),

            _("Oh no... not again... please do not stare this time..."),

            _("Twice... this can not be a coincidence... can it?"),

        ],
        (1, "nude", "chill"): [
            _("Again? At this point I am starting to think you plan these visits."),

            _("Round two, huh? You are getting predictable."),

            _("You again. I am starting to notice a pattern here."),

            _("Back for an encore? I did not realize I was that memorable."),

        ],
        (1, "partial", "angry"): [
            _("Again?! Do you just WAIT for me to start changing?!"),

            _("You walked in on me AGAIN! Start knocking, seriously!"),

            _("Twice in a row?! You have got some nerve!"),

        ],
        (1, "partial", "shy"): [
            _("This is the second time... I really need to start locking the door..."),

            _("Again? I... I should be more careful, I guess..."),

            _("You really have a talent for catching me at the worst times..."),

        ],
        (1, "partial", "chill"): [
            _("You again? I am starting to think this is intentional."),

            _("Second time catching me half-dressed. Coincidence? Sure."),

            _("At this rate, you will have seen every outfit I own. And everything under it."),

        ],
        (1, "towel", "neutral"): [
            _("You again. At least I was prepared this time."),

            _("Back for round two? Good thing I learned to keep a towel close."),

            _("Oh, you. I had a feeling I would see you again. Towel is staying on, by the way."),

        ],
        (1, "dressed", "neutral"): [
            _("Oh, it is you again. At least I am dressed this time."),

            _("Funny seeing you here again. Relax, I have clothes on."),

            _("You again. Sorry, no free show today."),

            _("Still dressed. I know, what a letdown."),

        ],

        # ── Bracket 2: FAMILIAR (3rd-4th time) ──
        (2, "nude", "angry"): [
            _("Do you EVER knock?! ...Ugh, just hand me a towel."),

            _("At this point I should just expect you. Still annoying though!"),

            _("Three times is not a coincidence anymore. You are doing this on PURPOSE."),

            _("I swear you have a sixth sense for this. Get me a towel. NOW."),

        ],
        (2, "nude", "shy"): [
            _("I... I should be used to this by now, but it is still embarrassing..."),

            _("You keep catching me like this... am I that unlucky?"),

            _("Again... at least you already know what I look like, I guess..."),

            _("At this point I am running out of ways to cover myself around you..."),

        ],
        (2, "nude", "resigned"): [
            _("Sigh... fine. You have seen it all before anyway."),

            _("You know what? I am not even going to scramble for a towel this time."),

            _("At this point, covering up feels more awkward than just... not."),

            _("Oh, hey. Yeah, I am naked. Again. This is just our thing now, apparently."),

        ],
        (2, "partial", "angry"): [
            _("How many times is this going to happen?! ...Whatever, hand me my shirt."),

            _("You again. I am running out of ways to be surprised by this."),

            _("At this point, buy me dinner first. Seriously."),

        ],
        (2, "partial", "shy"): [
            _("By now you have probably memorized this outfit... or lack of it..."),

            _("I keep telling myself to lock the door... and I keep forgetting..."),

            _("You have seen me in my underwear so many times now... this is my life."),

        ],
        (2, "partial", "resigned"): [
            _("You know what? This is basically our thing at this point."),

            _("Honestly, I barely flinched this time. Progress, I guess."),

            _("Oh, you. I was wondering when you would show up. Pull up a chair."),

        ],
        (2, "towel", "neutral"): [
            _("At this point I just keep a towel within arm's reach. Because of YOU."),

            _("I had a feeling you would show up. Hence the towel."),

            _("Towel ready, dignity intact. I am getting good at this."),

        ],
        (2, "dressed", "neutral"): [
            _("Oh, you again. Sorry to disappoint. I am fully dressed this time."),

            _("Look at that, I beat you to the punch. Clothes: on."),

            _("Nothing to see here. Well, nothing you have not seen before."),

            _("Dressed and ready. I know, how boring for you."),

        ],

        # ── Bracket 3: ROUTINE (5th+ time) ──
        (3, "nude", "familiar"): [
            _("Oh, it is you. Can you pass me the shampoo?"),

            _("Hey. I barely noticed you came in. Grab a spot or get out, whatever."),

            _("You again. I stopped covering up for you three visits ago."),

            _("Right on schedule. I swear you have my shower routine memorized."),

            _("Morning. Or afternoon. Whatever. You know the drill by now."),

            _("Oh, hey. Towel is over there if you want one. I clearly do not need one around you anymore."),

        ],
        (3, "nude", "warming"): [
            _("You know, I used to freak out when you walked in. Now it is just... normal."),

            _("Honestly? I would be more surprised if you did NOT show up at this point."),

            _("I stopped locking the door a while ago. I wonder why..."),

            _("At this point you have seen me naked more than my mirror has."),

            _("You are here again. I am starting to think I like the company."),

            _("I left the door unlocked. Take that however you want."),

        ],
        (3, "partial", "familiar"): [
            _("Oh, hey. Same as usual. You would think I would learn to lock the door."),

            _("Look, at this point I am just going to pretend you are furniture."),

            _("You again. I am barely even undressed and you are already here."),

            _("Oh good, you are here. Can you hand me my shirt? It is right there."),

        ],
        (3, "partial", "warming"): [
            _("I could have been dressed by now, but honestly? I did not rush."),

            _("I knew you would probably show up. Did not bother hurrying."),

            _("I heard footsteps and thought, 'That is probably him.' I was right."),

        ],
        (3, "towel", "neutral"): [
            _("Towel: check. You showing up: check. This is becoming a routine."),

            _("I do not even jump anymore when you walk in. Growth."),

            _("At this point, the towel is more for your benefit than mine."),

        ],
        (3, "dressed", "neutral"): [
            _("Fully clothed. I know, boring for you. Better luck next time."),

            _("Before you ask: yes, I am dressed, and no, I was not waiting for you."),

            _("Clothes on. I know, not your favorite version of this scene."),

            _("Dressed. Again. You really need to work on your timing."),

        ],
    }

    def _shower_enc_line(bracket, state, mood):
        """Pick an encounter-progression line, or None."""
        key = (bracket, state, mood)
        pool = _SHOWER_ENC_LINES.get(key)
        if pool:
            return renpy.random.choice(pool)
        return None

    # --------------------------------------------------------
    # Map shower_state to a state_category for encounter lines
    # --------------------------------------------------------
    def _shower_state_cat(state):
        if state == "nude":
            return "nude"
        if state in ("underwear", "missing_top", "missing_bottom"):
            return "partial"
        if state == "towel":
            return "towel"
        return "dressed"

    # --------------------------------------------------------
    # Relationship tier for shower encounters
    # Returns: 0 = stranger/low, 1 = warming up, 2 = comfortable,
    #          3 = intimate, 4 = lovers (had sex many times)
    # --------------------------------------------------------
    def _shower_rel_tier(girl):
        love = getattr(girl, "Love", 0)
        lust = getattr(girl, "Lust", 0)
        inbt = getattr(girl, "Inbt", 0)
        flags = getattr(girl, "intimacy_flags", set()) or set()
        had_sex = "sex" in flags
        sa = getattr(girl, "Sex_acts", {}) or {}
        # Acts only: positions are preferences, adding them to "sex" counted one cowgirl scene twice
        sex_total = girl_act_counts(girl)[0]   # "sex" + "anal"
        total_acts = sum(sa.get(k, 0) for k in ("bj", "hj", "tj", "sex", "anal"))

        _t = SEX_HISTORY_THRESHOLDS
        if had_sex and sex_total >= _t["shower_tier_lovers_sex"] and love >= 700:
            return 4  # lovers — very comfortable, can invite to sex
        if had_sex and sex_total >= _t["shower_tier_intimate_sex"] and love >= 500:
            return 3  # intimate — flirty, teasing, suggestive
        if total_acts >= _t["shower_tier_comfortable_acts"] or (love >= 400 and inbt >= 500):
            return 2  # comfortable — playful, not shy
        if love >= 200 or inbt >= 300:
            return 1  # warming up — still shy but not angry
        return 0      # stranger/low

    # --------------------------------------------------------
    # Relationship-based shower greetings (nude state)
    # These override the default chill/angry reactions
    # --------------------------------------------------------
    _SHOWER_REL_LINES = {
        # Tier 4 — lovers (had sex many times, high love)
        4: [
            _("Missing me already? The water is warm, come join me."),

            _("You know, you do not have to sneak around anymore. Just get in."),

            _("Took you long enough. I was starting to think you forgot about me."),

            _("Are you just going to stand there, or are you going to make this shower worth it?"),

            _("Mmm, perfect timing. I was just thinking about you."),

            _("The door was unlocked for a reason, you know."),

        ],
        # Tier 3 — intimate (had sex a couple times)
        3: [
            _("Well well, look who decided to show up. Like the view?"),

            _("You have seen all of this before... but I do not mind showing you again."),

            _("At this point, I would be surprised if you did NOT walk in on me."),

            _("You keep showing up when I am naked. Starting to think it is not a coincidence."),

            _("Oh, it is you. I was wondering when you would find your way in here."),

        ],
        # Tier 2 — comfortable (some history together)
        2: [
            _("Hey you. I am almost done, but you can stay if you want."),

            _("Getting bold, are we? I do not hate it, though."),

            _("You really like catching me at these moments, huh?"),

            _("I should be annoyed, but honestly... I kind of expected this."),

        ],
        # Tier 1 — warming up
        1: [
            _("Oh! Um... h-hi. I was not expecting company."),

            _("You could have knocked, you know... but it is fine, I guess."),

            _("This is a little awkward... but I trust you, so it is okay."),

        ],
    }

    # Tier 4 — teasing lines after initial greeting
    _SHOWER_REL_TEASE_T4 = [
        _("Are you missing something? Because I have been right here, waiting."),

        _("You know exactly where to find me when you need me."),

        _("Why are you still wearing clothes? That seems like a problem."),

        _("Last time was fun. Want to make this time even better?"),

        _("I left the door open on purpose. You know why."),

    ]

    # Tier 3 — suggestive follow-up
    _SHOWER_REL_TEASE_T3 = [
        _("Keep looking at me like that and I might pull you in here."),

        _("You know, it is rude to stare... unless I want you to."),

        _("I am starting to enjoy these little surprise visits of yours."),

        _("If you are going to keep showing up, you might as well make it worth my time."),

    ]

    # --------------------------------------------------------
    # Select girls that are in the showers in this time slot
    # --------------------------------------------------------
    def pick_girls_for_showers(time_index, spot="showers"):
        """
        Pick exactly 1 girl for this time slot, in the shower spot `spot` (SHOWER_SPOTS).
        Party member (follower) takes priority if present.
        Multi-girl shower events are NOT implemented yet — always cap at 1.
        """
        # Girls visited at night (said goodnight) don't reappear in the showers
        _visited = getattr(store, "_girls_visited_night", set())
        if SHOWER_SPOTS[spot]["pick"] == "schedule":
            # A home bathroom: nobody wanders in. The girl who came with him, or the one her schedule puts there
            # now (an angry one included: she can't avoid her own bathroom, Shower_Caught_Event sends her out)
            for g in store.Party:
                if not g.has_temp_status("angry"):
                    g.loc = spot
                    return [g]
            _here = [g for g in girls_reachable() if g.loc == spot and g.gid not in _visited]
            print("[SHOWER] %s: scheduled here = %s" % (spot, [g.gid for g in _here]))
            return _here[:1]

        # Angry girls avoid the showers when the player is around
        # girls_on_campus: this picker WRITES g.loc, so a girl who is away (giving birth) or lives off campus
        # would be teleported here
        pool = [g for g in girls_on_campus() if not (hasattr(g, "has_temp_status") and g.has_temp_status("angry")) and g.gid not in _visited]
        if not pool:
            return []

        # If player has a follower, she is in the showers
        for g in store.Party:
            if hasattr(g, "has_temp_status") and g.has_temp_status("angry"):
                continue
            g.loc = spot
            return [g]

        # Pick one random girl (50% chance per girl, no fallback)
        renpy.random.shuffle(pool)
        for g in pool:
            if renpy.random.random() < 0.50:
                g.loc = spot
                return [g]

        # Nobody happened to be here
        return []

    # --------------------------------------------------------
    # Set shower state for a girl (generic, usado em open/closed)
    # --------------------------------------------------------
    def setup_shower_state_for_girl(girl, force_nude=False):
        """
        Possible states:
            "nude"
            "underwear"
            "missing_top"
            "missing_bottom"
            "towel"
            "dressed"
        """
        _is_exhib = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")
        _spot = shower_spot_loc()
        _lock = store._shower_slot_lock.get(_spot)
        _lock_hit = (_lock and _lock.get("day") == store.Day and _lock.get("slot") == store.TimeIndex
                     and _lock.get("gid") == girl.gid and _lock.get("state") and not force_nude)
        if _lock_hit:
            # the slot already rolled her state once: re-entering shows the same scene (tester 2026-10-10)
            state = _lock["state"]
        elif force_nude or _is_exhib:
            state = "nude"
        else:
            d = renpy.random.randint(1, 20)

            if d >= 15:
                state = "nude"
            elif d >= 11:
                state = "underwear"
            elif d >= 7:
                state = "missing_top"
            elif d >= 4:
                state = "missing_bottom"
            else:
                state = "dressed"

        if _lock is not None and _lock.get("gid") == girl.gid:
            _lock["state"] = state
        girl.shower_state = state
        girl.shower_outfit = state
        girl.loc = shower_spot_loc()

    # --------------------------------------------------------
    # Apply shower outfit via Outfit_Change
    # --------------------------------------------------------
    def apply_shower_outfit(girl, refresh=True):
        state = getattr(girl, "shower_state", "dressed")
        debug_log("[DEBUG] apply_shower_outfit: gid=%s state=%s refresh=%s clothes_before=%s" % (getattr(girl, "gid", "?"), state, str(refresh), str(getattr(girl, "clothes", {}))))

        # In showers, shoes should be removed unless fully dressed on purpose.
        if state == "nude":
            girl.Collar = False
            girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none", refresh=refresh)

        elif state == "underwear":
            girl.Collar = False
            girl.Outfit_Change(over="none", mid="none", legs="none", shoes="none", refresh=refresh)  # keep chest & panties

        elif state == "missing_top":
            girl.Collar = False
            girl.Outfit_Change(over="none", mid="none", chest="none", shoes="none", refresh=refresh)  # topless

        elif state == "missing_bottom":
            girl.Collar = False
            girl.Outfit_Change(over="none", mid="none", legs="none", panties="none", shoes="none", refresh=refresh)  # bottomless

        elif state == "towel":
            girl.Collar = False
            girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", refresh=refresh)

        else:
            # "dressed" – keep current outfit (including shoes)
            pass

# ============================================================
# SHOWER ENTRY
# ============================================================

label Shower_Entry:

    # Which shower spot (SHOWER_SPOTS): the navigation set _shower_spot before the jump
    $ CurrentLocation = _shower_spot if _shower_spot in SHOWER_SPOTS else "showers"
    $ print("[SHOWER] Shower_Entry: spot=%s" % CurrentLocation)

    python:
        # Decide which girls are here in this time slot. The FIRST entry of the slot rolls; the slot
        # lock replays the same answer (same girl, same state, or the same empty room) until the clock
        # moves. A follower walking in WITH him is the one exception: she takes the shower and the lock.
        _ssl = store._shower_slot_lock.get(CurrentLocation)
        _ssl_valid = bool(_ssl) and _ssl.get("day") == Day and _ssl.get("slot") == TimeIndex
        _ssl_party = [g for g in store.Party if not (hasattr(g, "has_temp_status") and g.has_temp_status("angry"))]
        _ssl_fresh = not _ssl_valid or bool(_ssl_party)
        if _ssl_valid and not _ssl_party:
            if _ssl.get("gid") is None:
                girls_here = []
            else:
                _ssl_girl = GIRL_BY_ID.get(_ssl["gid"])
                _ssl_ok = (_ssl_girl is not None and not girl_is_away(_ssl_girl)
                           and not (hasattr(_ssl_girl, "has_temp_status") and _ssl_girl.has_temp_status("angry")))
                girls_here = [_ssl_girl] if _ssl_ok else []
                if girls_here:
                    _ssl_girl.loc = CurrentLocation
            print("[SHOWER] %s: slot lock replay (day %s slot %s): %s" % (
                CurrentLocation, Day, TimeIndex, girls_here[0].gid if girls_here else "empty"))
        else:
            girls_here = pick_girls_for_showers(TimeIndex, CurrentLocation)
            store._shower_slot_lock[CurrentLocation] = {
                "day": Day, "slot": TimeIndex,
                "gid": girls_here[0].gid if girls_here else None,
                "state": None, "mast_rolled": False,
            }
            print("[SHOWER] %s: slot lock set (day %s slot %s): %s" % (
                CurrentLocation, Day, TimeIndex, girls_here[0].gid if girls_here else "empty"))
        main_girl = girls_here[0] if girls_here else None
        girls_count = len(girls_here)

        # Ensure only the picked girl(s) are at showers; move everyone else away
        for _sg in ALL_GIRLS:
            if _sg not in girls_here and _sg.loc == CurrentLocation:
                _sg.loc = _sg.home

    # --------------------------------------------------------
    # Case 1: nobody here → player enters directly alone
    # --------------------------------------------------------
    if not main_girl:
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_17
        $ Narration(shower_spot_text("empty"))
        jump Shower_Loop

    # --------------------------------------------------------
    # Shower masturbation event — same logic as bedroom
    # Only fires for a single non-follower girl, after Day 3
    # Blocked for ex who hasn't had the cheating confrontation
    # --------------------------------------------------------
    python:
        _shower_mast_chance = 0.0
        _ex_block_shower = (main_girl and hasattr(main_girl, "is_ex_of_player") and main_girl.is_ex_of_player() and not getattr(main_girl, "_ex_confrontation_done", False))
        # a girl with a story: only once her step opens it (act "shower_masturbate", STORY_LADDERS)
        _story_block_shower = bool(main_girl) and story_act_locked(main_girl, "shower_masturbate")
        if _story_block_shower:
            print("[SHOWER] %s: no masturbation event, her story step %s locks it" % (main_girl.gid, story_step_id(main_girl)))
        if main_girl and girls_count == 1 and main_girl not in store.Party and Day > 3 and not _ex_block_shower and not _story_block_shower:
            _s_lust = getattr(main_girl, "Lust", 0)
            if _s_lust >= 80:
                _shower_mast_chance = 1.0
            else:
                _shower_mast_chance = 0.10 + (_s_lust / 100.0) * 0.90

    # one masturbation-event roll per slot: walking out and back in never re-spins it (tester 2026-10-10)
    python:
        _ssl_now = store._shower_slot_lock.get(CurrentLocation)
        _mast_may_roll = _shower_mast_chance > 0 and not (_ssl_now and _ssl_now.get("mast_rolled"))
        if _ssl_now is not None and _mast_may_roll:
            _ssl_now["mast_rolled"] = True
    if _mast_may_roll and renpy.random.random() < _shower_mast_chance:
        call caught_masturbating_shower(main_girl) from _call_caught_masturbating_shower
        if _return == "left":
            return
        # Masturbation scene ended — restore outfit before entering shower loop
        $ scene_full_cleanup(main_girl)
        jump Shower_Loop

    # --------------------------------------------------------
    # Case 2: choose entry path
    #   - direct : entrada direta, até 2 garotas, nude/towel/dressed
    #   - open   : porta aberta, sempre 1 garota
    #   - closed : porta fechada, sempre 1 garota
    # --------------------------------------------------------
    python:
        # If the main girl is a Party follower, always use "direct" (no surprise discovery)
        _main_is_follower = (girls_here[0] in store.Party) if girls_here else False
        if _main_is_follower:
            ShowerEntryPath = "direct"
        else:
            # the PATH rolls once per slot too (tester 2026-10-11: the state lock held, but a re-entry
            # rolled a new door and she flipped between nude and dressed through it)
            _ssl_pl = store._shower_slot_lock.get(CurrentLocation)
            _ssl_pl_hit = (_ssl_pl and _ssl_pl.get("day") == Day and _ssl_pl.get("slot") == TimeIndex
                           and _ssl_pl.get("gid") == main_girl.gid and _ssl_pl.get("path"))
            ShowerEntryPath = _ssl_pl["path"] if _ssl_pl_hit else shower_spot_path(CurrentLocation)
            if _ssl_pl is not None and _ssl_pl.get("gid") == main_girl.gid:
                _ssl_pl["path"] = ShowerEntryPath
        print("[SHOWER] %s: %s found by the %s path" % (CurrentLocation, main_girl.gid, ShowerEntryPath))

        # Hard cap: only 1 girl in showers (multi-girl events not implemented yet)
        girls_here = [girls_here[0]] if girls_here else []
        main_girl = girls_here[0] if girls_here else None
        girls_count = 1

        # Para "open", usamos o setup padrão (pode ter partes faltando)
        if ShowerEntryPath == "open":
            setup_shower_state_for_girl(main_girl, force_nude=False)
            apply_shower_outfit(main_girl)
        # Para "closed", vamos setar só da main_girl quando for necessário
        # Para "direct", tratamos estados abaixo (apenas nude/towel/dressed)

    # --------------------------------------------------------
    # PATH: DIRECT – entrada direta no vestiário (até 2 garotas)
    # - Somente estados: "nude", "towel", "dressed"
    # - Não passamos pelo BG da porta, vamos direto para showers
    # - Posições:
    #     main_girl -> slot_center
    #     segunda garota (se existir) -> slot_right
    # --------------------------------------------------------
    if ShowerEntryPath == "direct":
        $ ShowerEntryMode = "direct"
        $ CurrentGirl = main_girl

        # Cena base: showers BG com sprites
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_18

        python:
            allowed_states = ["nude", "towel", "dressed"]

            for g in girls_here:
                _dlock = store._shower_slot_lock.get(CurrentLocation)
                _dlock_hit = (_dlock and _dlock.get("day") == Day and _dlock.get("slot") == TimeIndex
                              and _dlock.get("gid") == g.gid and _dlock.get("state") in allowed_states)
                # Followers arrive WITH the player — always dressed
                if g in store.Party:
                    state = "dressed"
                elif _dlock_hit:
                    # the slot already rolled her state once (tester 2026-10-10)
                    state = _dlock["state"]
                elif hasattr(g, "has_trait") and g.has_trait("exhibitionist"):
                    state = "nude"
                else:
                    state = renpy.random.choice(allowed_states)
                if _dlock is not None and _dlock.get("gid") == g.gid:
                    _dlock["state"] = state
                g.shower_state = state
                g.shower_outfit = state
                g.loc = CurrentLocation

                if state == "nude":
                    g.Collar = False
                    g.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                elif state == "towel":
                    g.Collar = False
                    g.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none")
                else:
                    g.WearPreset("casual", apply_now=True)

            # main_girl no centro
            pose_main = getattr(main_girl, "default_pose", "standing")
            main_girl.SpriteLoc = StageCenter
            set_girl_sprite(main_girl.gid, pose=pose_main, at_list=[slot_center])

        # If the main girl was already following the player (Party), skip discovery entirely
        if main_girl in store.Party:
            $ Narration(shower_spot_text("with_follower"))

            # Follower arrives WITH you — she starts getting ready, not "caught"
            python:
                _inbt = getattr(main_girl, "Inbt", 0)
                _flags = getattr(main_girl, "intimacy_flags", set()) or set()
                _seen_nude = (getattr(main_girl, "Exposure", None) or {}).get("saw_boobs", 0) + (getattr(main_girl, "Exposure", None) or {}).get("saw_pussy", 0)
            if _inbt >= 700 or _seen_nude >= 3:
                $ set_scene_expression(main_girl, "smile")
                $ Say_Line(main_girl, renpy.random.choice([_("So... are we showering together, or are you just going to watch?"), _("I hope you're planning to join me in there~"), _("Don't pretend you came here just for the water.")]))
            elif _inbt >= 400:
                $ set_scene_expression(main_girl, "shy")
                $ Say_Line(main_girl, renpy.random.choice([_("I guess we're... showering at the same time, huh?"), _("Just... don't stare too much, okay?"), _("This is a little awkward, but... let's just get in.")]))
            else:
                $ set_scene_expression(main_girl, "normal")
                $ Say_Line(main_girl, renpy.random.choice([_("Alright, let's just... keep it normal."), _("I'll take this side, you take that side."), _("Try not to make this weird, okay?")]))

            jump Shower_Loop
        else:
            $ Narration(shower_spot_text("direct"))

        # Reações da garota principal (cenário direto)
        call Shower_Caught_Event(main_girl, CurrentLocation, mode="direct") from _call_Shower_Caught_Event
        return

    # --------------------------------------------------------
    # PATH: DOOR OPEN – porta já aberta (1 garota)
    # --------------------------------------------------------
    if ShowerEntryPath == "open":
        $ ShowerEntryMode = "open"
        $ CurrentGirl = main_girl

        # Base showers background
        call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_19

        python:
            pose = getattr(main_girl, "default_pose", "standing")
            main_girl.SpriteLoc = None
            set_girl_sprite(main_girl.gid, pose=pose, at_list=[slot_door_open])

        # Porta como overlay
        show door_open zorder 151

        $ Narration(shower_spot_text("open"))

        call Shower_Caught_Event(main_girl, CurrentLocation, mode="open") from _call_Shower_Caught_Event_1

        hide door_open
        python:
            main_girl.SpriteLoc = StageCenter
            set_girl_sprite(main_girl.gid, pose="standing", at_list=[slot_center])
        return

    # --------------------------------------------------------
    # PATH: DOOR CLOSED – corredor com porta (1 garota)
    # --------------------------------------------------------
    if ShowerEntryPath == "closed":
        $ ShowerEntryMode = "closed"
        scene bg Door
        $ Narration(shower_spot_text("closed"))

        python:
            setup_shower_state_for_girl(main_girl, force_nude=True)
            store._shower_locked_tries = 0

    label .closed_door:

        menu:
            "What do you do?"
            "Knock":
                $ ShowerEntryMode = "knock"
                play sound "audio/Knock.mp3" noloop
                $ Narration(_("You knock on the door and wait for a response."))

                $ Say_Line(main_girl, _("Who is it?"))
                $ Say_Player(_("It is me."))

                # A girl with a story: her step decides the door, whatever her stats (SHOWER_STORY_STEPS "knock")
                $ _knock_step = shower_story_step(main_girl)
                $ _knock_line = shower_story_line(main_girl, "shower_knock")
                if _knock_line:
                    $ Say_Line(main_girl, _knock_line)
                    $ print("[SHOWER] %s: knock on her story step %s -> %s" % (main_girl.gid, story_step_id(main_girl), _knock_step["knock"]))
                    if _knock_step["knock"] == "refuse":
                        $ shower_knock_reward(main_girl, 1)
                        $ Narration(_("You decide to respect her wishes and walk away."))
                        jump expression shower_spot_exit()

                    python:
                        main_girl.shower_state = _knock_step["knock"]
                        apply_shower_outfit(main_girl, refresh=False)
                    $ CurrentGirl = main_girl
                    call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_shower_story_knock
                    python:
                        apply_shower_outfit(main_girl)
                        pose_main = getattr(main_girl, "default_pose", "standing")
                        set_girl_sprite(main_girl.gid, pose=pose_main, at_list=[slot_center])
                    $ set_scene_expression(main_girl, _knock_step["face"])
                    if main_girl.shower_state == "towel":
                        $ Narration(_("[main_girl.Name] cracks the door open, now wrapped in a towel."))
                    else:
                        $ Narration(_("[main_girl.Name] does not bother to cover herself as you step inside."))
                        $ main_girl.RegisterAction("player_saw_boobs")
                        $ main_girl.RegisterAction("player_saw_pussy")
                    $ _knock_open = shower_story_line(main_girl, "shower_knock_open")
                    if _knock_open:
                        $ Say_Line(main_girl, _knock_open)
                    return

                $ ap = ApprovalCheck(main_girl, T=1100, Type="LOI", Spread=150)

                if ap <= 0:
                    $ Say_Line(main_girl, _("I am in the middle of a shower, do not come in!"))
                    $ Say_Line(main_girl, _("Please give me some privacy."))
                    $ shower_knock_reward(main_girl, 1)
                    $ Narration(_("You decide to respect her wishes and walk away."))
                    jump expression shower_spot_exit()

                elif ap in (1, 2):
                    $ Say_Line(main_girl, _("Oh, it is you. Can you give me a second to grab a towel?"))
                    $ Narration(_("You wait outside while she turns off the water and moves around inside."))
                    $ Narration(_("After a short moment, you hear the door unlock."))
                    $ shower_knock_reward(main_girl, 3)

                    python:
                        main_girl.shower_state = "towel"

                    $ CurrentGirl = main_girl
                    call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_20

                    python:
                        apply_shower_outfit(main_girl)
                        pose_main = getattr(main_girl, "default_pose", "standing")
                        set_girl_sprite(main_girl.gid, pose=pose_main, at_list=[slot_center])

                    $ set_scene_expression(main_girl, "shy")
                    $ Narration(_("[main_girl.Name] cracks the door open, now wrapped in a towel."))
                    $ Say_Line(main_girl, _("You can come in, just... do not stare too much."))
                    return

                else:
                    $ shower_knock_reward(main_girl, 5)
                    $ Say_Line(main_girl, _("Oh, hey. You can come in if you want."))

                    python:
                        main_girl.shower_state = "nude"
                        apply_shower_outfit(main_girl, refresh=False)

                    $ CurrentGirl = main_girl
                    call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_21

                    python:
                        apply_shower_outfit(main_girl)
                        pose_main = getattr(main_girl, "default_pose", "standing")
                        set_girl_sprite(main_girl.gid, pose=pose_main, at_list=[slot_center])

                    $ set_scene_expression(main_girl, "sexy")
                    $ Narration(_("[main_girl.Name] does not bother to cover herself as you step inside."))
                    $ Say_Line(main_girl, _("Relax, I do not mind if you see a little more."))

                    $ _exp_b = main_girl.RegisterAction("player_saw_boobs")
                    $ _exp_p = main_girl.RegisterAction("player_saw_pussy")
                    if (_exp_b["first_time"] or _exp_p["first_time"]) and not main_girl.has_trait("exhibitionist"):
                        call CaughtExposureReaction(main_girl, "boobs" if _exp_b["first_time"] else "pussy") from _call_CaughtExposureReaction

                    return

            "Enter without knocking":
                if SHOWER_SPOTS[CurrentLocation]["locked"]:
                    # A locked door (the bathroom of a home): the handle doesn't turn, and she hears it
                    $ Narration(shower_spot_text("locked"))
                    python:
                        store._shower_locked_tries += 1
                        _locked_sline = None
                        _lock_step = shower_story_step(main_girl)
                        if _lock_step and _shower_locked_tries > 1:
                            _locked_sline = shower_story_line(main_girl, "shower_locked_retry")
                        elif _lock_step:
                            _locked_sline = shower_story_line(main_girl, "shower_locked")
                    if _locked_sline:
                        $ Say_Line(main_girl, _locked_sline)
                    else:
                        $ Say_Line(main_girl, _tl(renpy.random.choice(_SHOWER_LOCKED_LINES)))
                    if _shower_locked_tries > 1 and _lock_step:
                        $ Change_Status(main_girl, "Love", -5)
                        $ Change_Status(main_girl, "Obed", -5)
                    $ print("[SHOWER] %s: tried the locked door of %s (try %d)" % (CurrentLocation, main_girl.gid, _shower_locked_tries))
                    jump .closed_door
                $ ShowerEntryMode = "enter"
                $ Narration(_("You grab the handle and step inside without announcing yourself."))

                $ CurrentGirl = main_girl
                $ main_girl.SpriteLoc = StageCenter
                call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_22

                python:
                    apply_shower_outfit(main_girl)
                    pose_main = getattr(main_girl, "default_pose", "standing")
                    set_girl_sprite(main_girl.gid, pose=pose_main, at_list=[slot_center])

                call Shower_Caught_Event(main_girl, CurrentLocation, mode="closed_enter") from _call_Shower_Caught_Event_2
                return

            "Leave it for later":
                $ Narration(_("You decide to leave whoever is inside in peace for now."))
                jump expression shower_spot_exit()

# ============================================================
# SHOWER LOOP – after you are inside and finished initial scene
# ============================================================

label Shower_Loop:

    # If player is no longer in showers (time change moved us), redirect
    if CurrentLocation not in SHOWER_SPOTS:
        $ debug_log("[SHOWER] Location changed to %s, redirecting" % CurrentLocation)
        call Set_Scene(entry=True) from _call_Set_Scene_shower_loc_change
        jump expression _get_location_loop(CurrentLocation)

    $ print("[SHOWER_LOOP] === ENTERING SHOWER LOOP === CurrentLocation=%s" % CurrentLocation)
    $ _shower_girls_here = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
    $ print("[SHOWER_LOOP] girls_here=%s" % [g.Name for g in _shower_girls_here])
    $ resolve_npc_for_location(CurrentLocation)
    $ build_location_roster(_shower_girls_here, store._npc_on_scene)

    menu:
        "Chat" if _shower_girls_here:
            $ debug_log("[SHOWER] Chat: before do_talk, CurrentLocation=%s" % CurrentLocation)
            call do_talk(CurrentLocation, TimeIndex) from _call_do_talk_shower
            $ debug_log("[SHOWER] Chat: after do_talk, CurrentLocation=%s" % CurrentLocation)
            if CurrentLocation not in SHOWER_SPOTS:
                $ debug_log("[SHOWER] Chat: location changed! Redirecting to %s" % CurrentLocation)
                call Set_Scene(entry=True) from _call_Set_Scene_shower_redir
                jump expression _get_location_loop(CurrentLocation)
            jump Shower_Loop

        "Shower" if (100 - Round) >= TIME_COSTS["shower"]:
            if len(_shower_girls_here) == 1:
                $ _shower_partner = _shower_girls_here[0]
                python:
                    _invite_lines = [
                        _("Want to shower together?"),

                        _("How about we save water and share?"),

                        _("Room for two under that water?"),

                        _("I need a shower. You coming?"),

                        _("Shower time. Room for two if you're interested."),

                    ]
                $ Narration(_tl(renpy.random.choice(_invite_lines)))
                python:
                    _sg_best = max(getattr(_shower_partner, "Love", 0), getattr(_shower_partner, "Inbt", 0))
                if _sg_best >= 200:
                    python:
                        _accept_lines = [
                            _("Sure... just don't stare too much."),

                            _("Okay... but keep your hands to yourself. For now."),

                            _("I was hoping you'd ask."),

                            _("Why not? I could use a rinse too."),

                        ]
                    $ Say_Line(_shower_partner, _tl(renpy.random.choice(_accept_lines)))
                    $ Change_Status(_shower_partner, "Love", 5)
                    $ Change_Status(_shower_partner, "Inbt", 5)

                    python:
                        _strip_top_lines = [
                            _("She pulls her top off, dropping it casually to the side."),

                            _("She reaches for the hem of her shirt and lifts it over her head."),

                            _("With a quick pull, she removes her top and tosses it aside."),

                        ]
                    $ Narration(_tl(renpy.random.choice(_strip_top_lines)))
                    $ _shower_partner.Outfit_Change(over="none", mid="none", chest="none")
                    $ set_girl_sprite(_shower_partner, pose="standing", at_list=[slot_center])
                    call CheckExposure(_shower_partner) from _call_CheckExposure_shower_top

                    python:
                        _strip_bot_lines = [
                            _("She slides her bottoms down, stepping out of them."),

                            _("She hooks her thumbs into her waistband and pushes everything down."),

                            _("Without hesitation, she pushes the rest off and kicks them aside."),

                        ]
                    $ Narration(_tl(renpy.random.choice(_strip_bot_lines)))
                    $ _shower_partner.shower_state = "nude"
                    $ apply_shower_outfit(_shower_partner, refresh=False)
                    $ set_girl_sprite(_shower_partner, pose="standing", at_list=[slot_center])
                    call CheckExposure(_shower_partner) from _call_CheckExposure_shower_bot

                    $ debug_log("[SHOWER_RUB] energy=%s girl=%s Love=%s Obed=%s Inbt=%s" % (Player.energy, _shower_partner.gid, getattr(_shower_partner, "Love", 0), getattr(_shower_partner, "Obed", 0), getattr(_shower_partner, "Inbt", 0)))
                    if Player.energy > 0:
                        $ _st_rub = rub_check(_shower_partner)
                        $ debug_log("[SHOWER_RUB] rub_check result: accepted=%s outcome=%s score=%s reasons=%s" % (_st_rub.get("accepted"), _st_rub.get("outcome"), _st_rub.get("score"), _st_rub.get("reasons")))
                        if _st_rub["accepted"]:
                            $ debug_log("[DEBUG] SHOWER rub: path=%s stage=%s" % (getattr(_shower_partner, "_cheat_escalation_path", 0), getattr(_shower_partner, "_cheat_sex_stage", 0)))
                            if _is_on_cheat_path(_shower_partner) and _cheat_stage(_shower_partner) < 1:
                                $ Say_Line(_shower_partner, _cheat_rub_first_line(_shower_partner))
                                $ store._path1_rub_first_line_pending = True
                            else:
                                $ store._path1_rub_first_line_pending = False
                                python:
                                    _st_narr = _tl(renpy.random.choice([
                                        _("Taking advantage of the soap and the closeness, she presses her back against you and starts grinding slowly."),

                                        _("As the warm water runs down both of you, she turns around and presses her back against you."),

                                        _("She asks you to help with the soap on her back. As your hands slide down, she doesn't stop you."),

                                        _("The steam fills the room. She leans back into you, letting the water flow between your bodies."),

                                    ]))
                                "[_st_narr]"
                                python:
                                    _st_rub_lines = [
                                        _("Mmm... don't stop."),

                                        _("That feels... really nice."),

                                        _("You're not just washing anymore, are you...?"),

                                    ]
                                $ Say_Line(_shower_partner, _tl(renpy.random.choice(_st_rub_lines)))
                            $ unlock_achievement("soap_time")
                            python:
                                _shower_partner._saved_outfit = None
                            python:
                                session_cum_reset()
                                store._player_exhausted = False
                                store._hate_cum_scene_aborted = False
                                store._condom_removed_midscene = False
                                store._creampie_consent = "denied"
                                store._player_exposed_this_session = True
                                store._cheat_rub_just_done = False
                                store._cheat_tip_just_done = False
                            if not girl_has_pose(_shower_partner, "reverse_cowgirl"):
                                call LD_RubLaunch(_shower_partner) from _call_LD_RubLaunch_shower_invite
                                call LD_ApplySpeed(_shower_partner, 1) from _call_LD_ApplySpeed_shower_invite
                            else:
                                call RCG_RubLaunch(_shower_partner) from _call_RCG_RubLaunch_shower_invite
                                $ rcg_speed = 1
                                call RCG_ApplySpeed(_shower_partner, 1) from _call_RCG_ApplySpeed_shower
                            $ mark_intimacy(_shower_partner, "rub")
                            $ Change_Status(_shower_partner, "Love", 5)
                            $ Change_Status(_shower_partner, "Inbt", 5)
                            if _is_on_cheat_path(_shower_partner):
                                $ _advance_cheat_stage(_shower_partner, 1)
                            if not girl_has_pose(_shower_partner, "reverse_cowgirl"):
                                call LD_RubControlMenu(_shower_partner) from _call_LD_RubControlMenu_shower_invite
                            else:
                                call RCG_RubControlMenu(_shower_partner) from _call_RCG_RubControlMenu_shower_invite
                            if _is_on_cheat_path(_shower_partner):
                                call _cheat_afterscene(_shower_partner, "rub") from _call_cheat_after_shower_rub_invite
                            python:
                                _shower_partner.Cum = []
                                _shower_partner._mouth_cum_persist = False
                                scene_full_cleanup(_shower_partner)
                            $ Narration(_("She grabs a towel from the rack and wraps it around herself."))
                            $ _shower_partner.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")
                            $ set_girl_sprite(_shower_partner, pose="standing", at_list=[slot_center])
                            call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_rub
                            jump Shower_Loop
                        else:
                            $ Narration(_("You shower together. The warm water and close proximity make it hard to focus on anything else."))
                            $ _shower_partner.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")
                            $ set_girl_sprite(_shower_partner, pose="standing", at_list=[slot_center])
                            call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_norub
                    else:
                        $ Narration(_("You shower together. The warm water and close proximity make it hard to focus on anything else."))
                        $ _shower_partner.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")
                        $ set_girl_sprite(_shower_partner, pose="standing", at_list=[slot_center])
                        call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_norub2
                else:
                    python:
                        _decline_lines = [
                            _("I... I'm not comfortable with that yet."),

                            _("Maybe when I know you better..."),

                            _("Not yet. I'll wait until you're done."),

                        ]
                    $ Say_Line(_shower_partner, _tl(renpy.random.choice(_decline_lines)))
                    call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_declined
                    $ session_cum_reset()
                    $ Narration(_("You take a quick shower on your own."))
            else:
                call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_solo
                $ session_cum_reset()
                $ Narration(_("You take a quick, refreshing shower. You feel clean and refreshed."))
            jump Shower_Loop

        "{color=#555555}Shower (not enough time){/color}" if (100 - Round) < TIME_COSTS["shower"]:
            $ Narration(_("You don't have enough time for a shower right now."))
            jump Shower_Loop

        "Wait a bit":
            $ debug_log("[SHOWER] Wait: before Apply_Time_Cost, CurrentLocation=%s" % CurrentLocation)
            call Apply_Time_Cost(TIME_COSTS["shower_wait"]) from _call_Apply_Time_Cost_shower_wait
            $ debug_log("[SHOWER] Wait: after Apply_Time_Cost, CurrentLocation=%s" % CurrentLocation)
            jump Shower_Loop

        "Leave":
            call Apply_Time_Cost(TIME_COSTS["shower_wait"]) from _call_Apply_Time_Cost_21
            python:
                for _lg in ALL_GIRLS:
                    if _lg.loc == CurrentLocation and getattr(_lg, "shower_state", None) in ("towel", "nude"):
                        _lg.WearPreset("casual", apply_now=False)
                        _lg.shower_state = "dressed"
            $ Narration(shower_spot_text("leave"))
            jump expression shower_spot_exit()

# ============================================================
# CAUGHT IN THE SHOWERS – girl reactions, towel, exposure
# ============================================================

# ============================================================
# Found in the shower by a girl with a story (SHOWER_STORY_STEPS)
# ============================================================
# Whatever her stats: her step's face, the towel or not, her first word, his answer, her reply, and on the steps
# that say so she throws him out. first_line: her "shower_caught.<cat>.<step>" line, picked by Shower_Caught_Event.
# ============================================================

label _shower_story_caught(girl, mode, first_line):
    python:
        _ssc = shower_story_step(girl)
        _ssc_state = getattr(girl, "shower_state", "dressed")
        # same counters as the rest of Shower_Caught_Event: the encounter, and what he saw
        girl.RegisterAction("shower_caught")
        if _ssc_state in ("nude", "underwear", "missing_top"):
            girl.RegisterAction("player_saw_boobs")
        if _ssc_state in ("nude", "underwear", "missing_bottom"):
            girl.RegisterAction("player_saw_pussy")
        print("[SHOWER] %s: story step %s, found %s (%s): cover=%s out=%s" % (
            girl.gid, story_step_id(girl), _ssc_state, mode, _ssc["cover"], _ssc["out"]))

    $ set_scene_expression(girl, _ssc["face"])
    if _ssc_state == "towel":
        $ Narration(_ssc["narr_towel"])
    else:
        if _ssc["cover"]:
            python:
                if _ssc_state == "nude":
                    girl.shower_state = "towel"
                    girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none")
                else:
                    girl.Outfit_Change(over="towel")
        $ Narration(_ssc["narr"])
    $ Say_Line(girl, first_line)

    python:
        for _ssc_stat, _ssc_amt in _ssc["caught"].items():
            Change_Status(girl, _ssc_stat, _ssc_amt)
        _ssc_route = renpy.display_menu([(_tl(_ssc_cap), _ssc_key) for _ssc_key, _ssc_cap, _ssc_st in _ssc["choices"]])
        _ssc_reply = shower_story_line(girl, "shower_caught.reply.%s" % _ssc_route)
        if _ssc_reply:
            Say_Line(girl, _ssc_reply)
        for _ssc_key, _ssc_cap, _ssc_st in _ssc["choices"]:
            if _ssc_key == _ssc_route:
                for _ssc_stat, _ssc_amt in _ssc_st.items():
                    Change_Status(girl, _ssc_stat, _ssc_amt)
        print("[SHOWER] %s: he answered '%s'%s" % (girl.gid, _ssc_route, ", she throws him out" if _ssc["out"] else ""))

    if _ssc["out"]:
        # she throws him out of the bathroom, and the door shuts behind him for the rest of the slot
        $ shower_door_shut(girl, "her story step throws him out")
        $ Narration(shower_spot_text("leave_doorway" if mode == "open" else "leave"))
        hide door_open
        jump expression shower_spot_exit()
    return

label Shower_Caught_Event(girl, loc, mode=None):

    if not girl:
        $ Narration(shower_spot_text("nobody"))
        return

    # --- Ex who hasn't had the cheating confrontation: skip event ---
    if hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
        $ Narration(_("You hear someone inside but decide not to go in."))
        return

    # --- Angry girl: she leaves immediately ---
    if hasattr(girl, "has_temp_status") and girl.has_temp_status("angry"):
        python:
            _ag_spot_lines = [
                _tl(_("You step inside and see %s. She freezes, water still running down her body.")) % girl.Name,
                _tl(_("You walk in and find %s mid-shower. Her eyes snap to you immediately.")) % girl.Name,
                _tl(_("%s is standing under the water. She notices you and her breath catches for a moment.")) % girl.Name,
            ]
            Narration(_tl(renpy.random.choice(_ag_spot_lines)))
        python:
            _ag_hesitate_lines = [
                _("For a split second, her eyes wander over you... then her jaw clenches and the anger returns."),

                _("She hesitates, lips parting slightly... but then she remembers why she is furious with you."),

                _("Something flickers in her expression -- desire, maybe -- but it is gone as fast as it came."),

            ]
            Narration(_tl(renpy.random.choice(_ag_hesitate_lines)))
        python:
            _ag_leave_lines = [
                _("No. I'm still mad at you. Don't even look at me."),

                _("Don't think seeing me like this changes anything. I'm STILL angry."),

                _("I was here first. But I'd rather leave than share this space with you right now."),

                _("You have some nerve showing up here. I'm done."),

            ]
            Say_Line(girl, _tl(renpy.random.choice(_ag_leave_lines)))
            Narration(_tl(_("%s quickly wraps herself in a towel, grabs her things, and storms out.")) % girl.Name)
            girl.WearPreset("casual", apply_now=False)
            girl.loc = girl.home
            hide_girl_sprite(girl)
        return

    $ CurrentGirl = girl

    # --- A girl with a story: her step's reaction whatever her stats or traits (a state without a pool falls through) ---
    $ _ssc_line = shower_story_line(girl, "shower_caught.%s" % _shower_state_cat(getattr(girl, "shower_state", "dressed")))
    if _ssc_line:
        call _shower_story_caught(girl, mode, _ssc_line) from _call_shower_story_caught
        return

    # --- Public shy girl: extra panic on first few encounters ---
    python:
        _is_public_shy = hasattr(girl, "has_trait") and girl.has_trait("public_shy")
        _shy_enc_total = girl.GetActionCount("shower_caught") if hasattr(girl, "GetActionCount") else 0
    if _is_public_shy and _shy_enc_total < 3:
        python:
            _shy_shower_lines = [
                _("AAAH! D-don't look! I'm... oh god, why didn't I lock the door?!"),

                _("W-what are you doing here?! Turn around! Turn around RIGHT NOW!"),

                _("No no no no... someone is here... this is literally my worst nightmare..."),

            ]
        $ set_scene_expression(girl, "scared", blush=2)
        $ Say_Line(girl, _tl(renpy.random.choice(_shy_shower_lines)))
        "She scrambles to cover herself, face burning red."

    # Track encounter count for progression
    $ _sh_enc = girl.RegisterAction("shower_caught")
    $ _sh_enc_count = _sh_enc["total"]
    $ _sh_bracket = _shower_enc_bracket(_sh_enc_count)

    python:
        state = getattr(girl, "shower_state", "dressed")
        exposure = getattr(girl, "Exposure", None) or {}
        times_boobs = exposure.get("saw_boobs", 0)
        times_pussy = exposure.get("saw_pussy", 0)
        total_seen = times_boobs + times_pussy
        inbt_val = getattr(girl, "Inbt", 0)
        _sh_tier = _shower_rel_tier(girl)
        _sh_state_cat = _shower_state_cat(state)

    # --------------------------------------------------------
    # RELATIONSHIP-AWARE REACTIONS (tier >= 2 and exposed)
    # Overrides the normal approval-based reactions when the
    # player and girl have a strong relationship / sexual history.
    # --------------------------------------------------------
    if _sh_tier >= 2 and state in ("nude", "underwear", "missing_top", "missing_bottom"):

        # Register exposure
        if state in ("nude", "underwear", "missing_top"):
            $ girl.RegisterAction("player_saw_boobs")
        if state in ("nude", "underwear", "missing_bottom"):
            $ girl.RegisterAction("player_saw_pussy")

        # ── Tier 4: Lovers — surprised, RCG tease, back to standing ──
        if _sh_tier == 4:
            # Initial surprise
            $ set_scene_expression(girl, "surprised")
            python:
                _sh_surprise = renpy.random.choice([
                    _("Oh! You scared me!"),

                    _("Hey! You could have knocked!"),

                    _("Ah! I did not hear you come in!"),

                ])
            $ Say_Line(girl, _sh_surprise)
            $ Narration(_("[girl.Name] jumps a little, but when she sees it is you, her expression softens."))

            # If door was open/closed (not direct), narrate entering
            if mode in ("open", "enter", "knock"):
                hide door_open
                $ Narration(_("You step inside and close the door behind you."))

            # Recognizes the player, relaxes into sexy
            $ set_scene_expression(girl, "sexy")
            python:
                _sh_relax = renpy.random.choice([
                    _("Oh, it is just you. You scared me for a second."),

                    _("Oh... hey you. Almost gave me a heart attack."),

                    _("God, it is you. I thought it was someone else for a moment."),

                ])
            $ Say_Line(girl, _sh_relax)

            # Switch to rear pose for the tease
            $ girl.Collar = False
            $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
            if not girl_has_pose(girl, "reverse_cowgirl"):
                call LD_Launch(girl) from _call_LD_Launch_shower_rel
            else:
                call RCG_Launch(girl) from _call_RCG_Launch_shower_rel

            # Teasing line in rear position
            $ set_scene_expression(girl, "sexy")
            python:
                _sh_rcg_tease = renpy.random.choice([
                    _("Are you missing something? Because I have been right here, waiting."),

                    _("Since you are already here... why not make it worth your while?"),

                    _("You keep finding me like this. Starting to think you plan it."),

                    _("The water is warm, I am here... what are you waiting for?"),

                    _("Last time was fun. Want to make this time even better?"),

                    _("You know, you do not have to pretend you came here just to shower."),

                ])
            $ Say_Line(girl, _sh_rcg_tease)
            $ Change_Status(girl, "Lust", 12)
            $ Change_Status(girl, "Love", 3)

            # Back to standing after the tease
            if not girl_has_pose(girl, "reverse_cowgirl"):
                call LD_End(girl) from _call_LD_End_shower_tease_back
            else:
                call RCG_End(girl) from _call_RCG_End_shower_tease_back

            menu:
                "Rub against her":
                    $ Say_Player(_("Let me get behind you..."))
                    $ set_scene_expression(girl, "lipbite")
                    python:
                        _sh_rub = renpy.random.choice([
                            _("Just... just rubbing, okay?"),

                            _("Mmm... okay, but keep it outside."),

                            _("You better not try anything funny..."),

                        ])
                    $ Say_Line(girl, _sh_rub)
                    $ girl.Collar = False
                    $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                    $ girl._saved_outfit = None
                    python:
                        session_cum_reset()
                        store._player_exhausted = False
                        store._hate_cum_scene_aborted = False
                        store._condom_removed_midscene = False
                        store._creampie_consent = "denied"
                        store._player_exposed_this_session = True
                    if not girl_has_pose(girl, "reverse_cowgirl"):
                        call LD_RubLaunch(girl) from _call_LD_RubLaunch_shower_rel
                        call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_shower_rub_rel
                    else:
                        call RCG_RubLaunch(girl) from _call_RCG_RubLaunch_shower_rel
                        $ rcg_speed = 1
                        call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_shower_rub_rel
                    $ mark_intimacy(girl, "rub")
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 5)
                    if not girl_has_pose(girl, "reverse_cowgirl"):
                        call LD_RubControlMenu(girl) from _call_LD_RubControlMenu_shower_rel
                    else:
                        call RCG_RubControlMenu(girl) from _call_RCG_RubControlMenu_shower_rel

                    # Clean up scene layers + threads, then shower cleans cum + dress up
                    python:
                        girl.Cum = []
                        girl._mouth_cum_persist = False
                        scene_full_cleanup(girl)
                        girl.RestoreOutfit()
                        set_girl_sprite(girl, pose="standing")

                "Get in with her":
                    $ Say_Player(_("You do not have to ask me twice."))
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _sh_yes = renpy.random.choice([
                            _("Good answer."),

                            _("I was hoping you would say that."),

                            _("Took you long enough to decide."),

                        ])
                    $ Say_Line(girl, _sh_yes)
                    $ Change_Status(girl, "Lust", 10)
                    $ Change_Status(girl, "Love", 5)
                    # Cheat path gate: she won't go further if not at right stage
                    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False) and _cheat_stage(girl) < 2:
                        python:
                            _cep = getattr(girl, "_cheat_escalation_path", 0)
                            if _cep == 1:
                                _sh_deny = _("This is nice but... I have a {hint}%(pl)s{/hint}. We can rub a little but nothing more. Not here.")
                            elif _cep == 2:
                                _sh_deny = _("I want to... but not yet. I'm not ready to go that far. Let's just... feel each other for now.")
                            else:
                                _sh_deny = _("Not in the shower where anyone could walk in. Somewhere more private... where we can really take our time.")
                        $ Say_Line(girl, _format_partner_line(girl, _sh_deny))
                    # Ensure she stays nude (shower) and reset saved outfit to nude state
                    $ girl.Collar = False
                    $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                    $ girl._saved_outfit = None
                    # No pre-marking: sex_menu -> start_scene counts "sex" when penetration really happens
                    call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_shower_rel

                "Tease her back":
                    $ Say_Player(_("Maybe I just came to enjoy the view."))
                    $ set_scene_expression(girl, "bemused")
                    python:
                        _sh_tease_reply = renpy.random.choice([
                            _("The view is free. Everything else has a price."),

                            _("You are such a tease. Fine, but you owe me later."),

                            _("Keep playing hard to get. See how long that lasts."),

                            _("Suit yourself. But the offer does not last forever."),

                        ])
                    $ Say_Line(girl, _sh_tease_reply)
                    $ Change_Status(girl, "Lust", 5)
                    $ Change_Status(girl, "Inbt", 8)

                "Just admire her":
                    $ Say_Player(_("I just wanted to see you. You look incredible."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _sh_sweet_reply = renpy.random.choice([
                            _("You always know what to say, do you not?"),

                            _("That is sweet. Now get out before I change my mind about letting you stay."),

                            _("Careful. Sweet talk like that might get you pulled in here."),

                        ])
                    $ Say_Line(girl, _sh_sweet_reply)
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Lust", 3)

            return

        # ── Tier 3: Intimate — flirty and suggestive ──
        elif _sh_tier == 3:
            $ set_scene_expression(girl, "sexy")
            $ _sh_greet = renpy.random.choice(_SHOWER_REL_LINES[3])
            $ Say_Line(girl, _sh_greet)
            $ Change_Status(girl, "Lust", 8)

            $ _sh_tease = _tl(renpy.random.choice(_SHOWER_REL_TEASE_T3))
            $ Say_Line(girl, _sh_tease)

            menu:
                "You looked amazing. I could not look away.":
                    $ Say_Player(_("You looked amazing. I could not look away."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _sh_flattered = renpy.random.choice([
                            _("Flattery will get you everywhere with me."),

                            _("I know. But it is nice to hear you say it."),

                            _("You always did have good taste."),

                        ])
                    $ Say_Line(girl, _sh_flattered)
                    $ Change_Status(girl, "Love", 6)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Change_Status(girl, "Lust", 5)

                "Honestly? I want to see more.":
                    $ Say_Player(_("Honestly? I want to see more."))
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _sh_more = renpy.random.choice([
                            _("Maybe next time I will let you see everything. If you earn it."),

                            _("Greedy. I like that about you."),

                            _("You want more? Then you had better make it worth my while."),

                        ])
                    $ Say_Line(girl, _sh_more)
                    $ Change_Status(girl, "Inbt", 12)
                    $ Change_Status(girl, "Lust", 6)
                    $ Change_Status(girl, "Love", 3)

                "Sorry, just passing through.":
                    $ Say_Player(_("Sorry, just passing through."))
                    $ set_scene_expression(girl, "bemused")
                    $ Say_Line(girl, _("Sure you were. Your eyes say otherwise."))
                    $ Change_Status(girl, "Love", 2)

            return

        # ── Tier 2: Comfortable — playful, not shy ──
        else:
            $ set_scene_expression(girl, "bemused")
            $ _sh_greet = renpy.random.choice(_SHOWER_REL_LINES[2])
            $ Say_Line(girl, _sh_greet)
            $ Change_Status(girl, "Lust", 4)
            $ Change_Status(girl, "Love", 1)

            menu:
                "Sorry, I did not mean to startle you.":
                    $ Say_Player(_("Sorry, I did not mean to startle you."))
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("It is fine. Honestly, I do not mind when it is you."))
                    $ Change_Status(girl, "Love", 4)

                "I do not mind the view, to be honest.":
                    $ Say_Player(_("I do not mind the view, to be honest."))
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _sh_view = renpy.random.choice([
                            _("I noticed. Your face gives you away every time."),

                            _("Then take a good look. I am not hiding anything."),

                            _("You are getting bolder. I kind of like it."),

                        ])
                    $ Say_Line(girl, _sh_view)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 3)

                "I will leave you to it.":
                    $ Say_Player(_("I will leave you to it."))
                    $ set_scene_expression(girl, "normal")
                    $ Say_Line(girl, _("You do not have to leave, but suit yourself."))
                    $ Change_Status(girl, "Love", 2)

            return

    # --------------------------------------------------------
    # SPECIAL HANDLING: DOOR OPEN MODE
    # --------------------------------------------------------
    if mode == "open":

        $ set_scene_expression(girl, "surprised")

        if state == "nude":
            # Bracket-adjusted approval threshold
            python:
                _open_T = 1200
                if _sh_tier <= 1:
                    if _sh_bracket == 1:   _open_T = 1150
                    elif _sh_bracket == 2: _open_T = 1100
                    elif _sh_bracket >= 3: _open_T = 1000
            $ ap_seen = ApprovalCheck(girl, T=_open_T, Type="LOI", Spread=150)
            $ set_scene_expression(girl, "sexy" if girl.has_trait("exhibitionist") else "surprised")

            # Bracket-aware narration (exhibitionist gets confident narration)
            if girl.has_trait("exhibitionist"):
                if _sh_bracket == 0:
                    $ Narration(_("[girl.Name] notices you in the doorway. She does not flinch or reach for a towel."))
                elif _sh_bracket <= 2:
                    $ Narration(_("[girl.Name] spots you and a knowing smile crosses her face."))
                else:
                    $ Narration(_("[girl.Name] glances at you, completely at ease."))
            elif _sh_tier <= 1 and _sh_bracket == 0:
                $ Narration(_("[girl.Name] freezes. This is the first time you have ever seen her like this."))
            elif _sh_tier <= 1 and _sh_bracket == 1:
                $ Narration(_("[girl.Name] spots you and her eyes widen. She recognizes this situation."))
            elif _sh_tier <= 1 and _sh_bracket == 2:
                $ Narration(_("[girl.Name] notices you in the doorway. She barely flinches this time."))
            elif _sh_tier <= 1 and _sh_bracket >= 3:
                $ Narration(_("[girl.Name] glances at you, completely unsurprised."))
            else:
                $ Narration(_("[girl.Name] jumps a little, clearly startled by your sudden presence in the doorway."))

            # Exhibitionist: never covers up, stays confident regardless of approval
            if girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "sexy")
                $ Change_Status(girl, "Lust", 8)
                $ _scl = _shower_caught_line(girl, "nude_chill")
                if _scl:
                    $ Say_Line(girl, _scl)
                else:
                    $ Say_Line(girl, _("Well? Are you just going to stand there?"))

            # Bracket 3 routine: skip anger, go straight to familiar/warming
            elif _sh_tier <= 1 and _sh_bracket >= 3 and ap_seen >= 1:
                $ girl.Outfit_Change(over="towel")
                python:
                    _enc_mood = "warming" if ap_seen >= 3 else "familiar"
                    _enc_line = _shower_enc_line(3, "nude", _enc_mood)
                if ap_seen >= 3:
                    $ set_scene_expression(girl, "sexy")
                else:
                    $ set_scene_expression(girl, "bemused")
                $ Change_Status(girl, "Lust", 6)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("At this point, I would be more surprised if you did NOT show up."))

            # Bracket 0 first-time: no chill override, full intensity
            elif _sh_tier <= 1 and _sh_bracket == 0:
                if ap_seen <= 2:
                    $ girl.Outfit_Change(over="towel")
                    python:
                        _enc_mood = "angry" if ap_seen <= 1 else "shy"
                        _enc_line = _shower_enc_line(0, "nude", _enc_mood)
                    if ap_seen <= 1:
                        $ girl.shower_state = "towel"
                        $ girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none")
                        $ set_scene_expression(girl, "angry")
                        $ Narration(_("She scrambles for a towel and wraps it around herself, clearly shocked."))
                        $ Change_Status(girl, "Love", -2)
                    else:
                        $ girl.shower_state = "towel"
                        $ girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none")
                        $ set_scene_expression(girl, "shy")
                        $ Narration(_("She quickly grabs a towel, face turning bright red."))
                        $ Change_Status(girl, "Love", -1)
                        $ Change_Status(girl, "Lust", 3)
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ Say_Line(girl, _("What are you doing here?! I am naked!"))
                else:
                    $ set_scene_expression(girl, "bemused")
                    $ girl.Outfit_Change(over="towel")
                    $ Change_Status(girl, "Lust", 5)
                    python:
                        _enc_line = _shower_enc_line(0, "nude", "chill")
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ Say_Line(girl, _("Well, this is a first. Try to knock next time."))

            # Brackets 1-2 or tier 2+: existing logic with bracket-aware lines
            elif shower_chill(ap_seen, total_seen) and _sh_bracket > 0:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "sexy")
                $ Change_Status(girl, "Lust", 8)
                $ _scl = _shower_caught_line(girl, "nude_chill")
                if _scl:
                    $ Say_Line(girl, _scl)
                elif _sh_bracket >= 1 and _sh_tier <= 1:
                    python:
                        _enc_line = _shower_enc_line(_sh_bracket, "nude", "chill")
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ Say_Line(girl, _("You really like catching me off guard, do you not?"))
                else:
                    $ Say_Line(girl, _("You really like catching me off guard, do you not?"))
                    $ Say_Line(girl, _("Since you have already seen everything, I will not make a scene."))
            elif ap_seen <= 1:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "angry")
                $ Narration(_("She quickly grabs a towel and wraps it tightly around herself."))
                $ Change_Status(girl, "Love", -3)
                if _sh_bracket >= 1 and _sh_tier <= 1:
                    python:
                        _enc_line = _shower_enc_line(_sh_bracket, "nude", "angry")
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ _scl = _shower_caught_line(girl, "nude_angry")
                        if _scl:
                            $ Say_Line(girl, _scl)
                        else:
                            $ Say_Line(girl, _("Hey! You cannot just stand there like that!"))
                else:
                    $ _scl = _shower_caught_line(girl, "nude_angry")
                    if _scl:
                        $ Say_Line(girl, _scl)
                    else:
                        $ Say_Line(girl, _("Hey! You cannot just stand there like that!"))
            elif ap_seen in (2, 3):
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "shy")
                $ Narration(_("She covers herself with a towel, cheeks still flushed."))
                $ Change_Status(girl, "Love", -1)
                $ Change_Status(girl, "Lust", 5)
                if _sh_bracket >= 1 and _sh_tier <= 1:
                    python:
                        _enc_line = _shower_enc_line(_sh_bracket, "nude", "shy")
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ Say_Line(girl, _("Next time, at least give me a little warning..."))
                else:
                    $ Say_Line(girl, _("Next time, at least give me a little warning..."))
            else:
                $ set_scene_expression(girl, "sexy")
                $ Narration(_("She does not seem particularly bothered about being naked in front of you."))
                $ Change_Status(girl, "Lust", 10)
                if total_seen >= 3 or inbt_val >= 700:
                    $ _scl = _shower_caught_line(girl, "nude_sexy")
                    if _scl:
                        $ Say_Line(girl, _scl)
                    else:
                        $ Say_Line(girl, _("Door was open and you liked the view, huh?"))
                        $ Say_Line(girl, _("Did you like what you saw?"))
                else:
                    $ Say_Line(girl, _("Guess you caught me at a bad time... or a good one, depending on you."))

            $ _exp_b = girl.RegisterAction("player_saw_boobs")
            $ _exp_p = girl.RegisterAction("player_saw_pussy")
            if (_exp_b["first_time"] or _exp_p["first_time"]) and not girl.has_trait("exhibitionist"):
                call CaughtExposureReaction(girl, "boobs" if _exp_b["first_time"] else "pussy") from _call_CaughtExposureReaction_1

        elif state in ("underwear", "missing_top", "missing_bottom"):
            $ set_scene_expression(girl, "surprised")
            # Bracket-aware narration for partial
            if _sh_tier <= 1 and _sh_bracket == 0:
                $ Narration(_("[girl.Name] freezes. This is the first time you have caught her like this."))
            elif _sh_tier <= 1 and _sh_bracket >= 3:
                $ Narration(_("[girl.Name] notices you but barely reacts. She is used to this by now."))
            else:
                $ Narration(_("[girl.Name] freezes for a moment when she sees you standing there in the doorway."))

            # Bracket-adjusted threshold
            python:
                _open_pT = 1150
                if _sh_tier <= 1:
                    if _sh_bracket == 1:   _open_pT = 1100
                    elif _sh_bracket == 2: _open_pT = 1050
                    elif _sh_bracket >= 3: _open_pT = 950
            $ ap_partial = ApprovalCheck(girl, T=_open_pT, Type="LOI", Spread=150)

            python:
                _exp_b = {"first_time": False}
                _exp_p = {"first_time": False}
                if state in ("underwear", "missing_top"):
                    _exp_b = girl.RegisterAction("player_saw_boobs")
                if state in ("underwear", "missing_bottom"):
                    _exp_p = girl.RegisterAction("player_saw_pussy")
            if (_exp_b["first_time"] or _exp_p["first_time"]) and not girl.has_trait("exhibitionist"):
                call CaughtExposureReaction(girl, "boobs" if _exp_b["first_time"] else "pussy") from _call_CaughtExposureReaction_2

            # Exhibitionist: does not bother covering up
            if girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "sexy")
                $ Change_Status(girl, "Lust", 6)
                $ Say_Line(girl, _("Take a good look. I am not covering up for you."))

            # Bracket 3 routine: partial state barely matters
            elif _sh_tier <= 1 and _sh_bracket >= 3 and ap_partial >= 1:
                $ girl.Outfit_Change(over="towel")
                python:
                    _enc_mood = "warming" if ap_partial >= 3 else "familiar"
                    _enc_line = _shower_enc_line(3, "partial", _enc_mood)
                if ap_partial >= 3:
                    $ set_scene_expression(girl, "bemused")
                else:
                    $ set_scene_expression(girl, "normal")
                $ Change_Status(girl, "Lust", 4)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("You again. I barely even care at this point."))
            elif shower_chill(ap_partial, total_seen):
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "sexy")
                $ Change_Status(girl, "Lust", 6)
                $ Say_Line(girl, _("You really have a talent for showing up at the right moment."))
                $ Say_Line(girl, _("Since you have already seen more than this, I will let it slide."))
            elif inbt_val >= 700 or total_seen >= 3:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "sexy")
                $ Change_Status(girl, "Lust", 4)
                $ Say_Line(girl, _("You really have a talent for showing up at interesting moments."))
                $ Say_Line(girl, _("So? Did you like the view?"))
            else:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "perplexed")
                $ Change_Status(girl, "Love", -2)
                if _sh_tier <= 1 and _sh_bracket >= 1:
                    python:
                        _enc_mood = "angry" if ap_partial <= 1 else "shy"
                        _enc_line = _shower_enc_line(_sh_bracket, "partial", _enc_mood)
                    if _enc_line:
                        $ Say_Line(girl, _enc_line)
                    else:
                        $ Say_Line(girl, _("Hey, try to knock next time! I was getting changed here!"))
                else:
                    $ Say_Line(girl, _("Hey, try to knock next time! I was getting changed here!"))

        elif state == "towel":
            $ set_scene_expression(girl, "shy")
            $ Narration(_("[girl.Name] is already wrapped in a towel when you appear in the open doorway."))
            if _sh_tier <= 1 and _sh_bracket >= 3:
                $ set_scene_expression(girl, "normal")
                python:
                    _enc_line = _shower_enc_line(3, "towel", "neutral")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Towel ready. I knew you would show up eventually."))
            elif _sh_tier <= 1 and _sh_bracket >= 1:
                $ Change_Status(girl, "Love", -1)
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "towel", "neutral")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Hey, try to knock next time. I could have been naked."))
            else:
                $ Change_Status(girl, "Love", -1)
                if inbt_val >= 700 and total_seen >= 3:
                    $ set_scene_expression(girl, "bemused")
                    $ Say_Line(girl, _("You know, if you wanted to see more, you could at least say so."))
                else:
                    $ Say_Line(girl, _("Hey, try to knock next time. I could have been naked."))

        else:  # dressed
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] is fully dressed when she notices you in the doorway."))
            if _sh_tier <= 1 and _sh_bracket >= 3:
                python:
                    _enc_line = _shower_enc_line(3, "dressed", "neutral")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Fully dressed this time. Disappointed?"))
            elif _sh_tier <= 1 and _sh_bracket >= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "dressed", "neutral")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Change_Status(girl, "Love", -1)
                    $ Say_Line(girl, _("Hey, try to knock next time. I could have been naked."))
            else:
                $ Change_Status(girl, "Love", -1)
                $ Say_Line(girl, _("Hey, try to knock next time. I could have been naked."))

        if girl.has_trait("exhibitionist") and state in ("nude", "underwear", "missing_top", "missing_bottom"):
            menu:
                "I am definitely enjoying the view.":
                    $ Say_Player(_("I am definitely enjoying the view."))
                    $ set_scene_expression(girl, "sexy")
                    $ Say_Line(girl, _("Good. That is the whole point of leaving the door open."))
                    $ Change_Status(girl, "Love", 3)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 5)

                "You left the door open on purpose, did you not?":
                    $ Say_Player(_("You left the door open on purpose, did you not?"))
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("Maybe. Or maybe I just do not care who sees."))
                    $ Say_Line(girl, _("Either way, you are welcome."))
                    $ Change_Status(girl, "Love", 2)
                    $ Change_Status(girl, "Inbt", 5)
                    $ Change_Status(girl, "Lust", 3)

                "Sorry, I will come back later.":
                    $ Say_Player(_("Sorry, I will come back later."))
                    $ set_scene_expression(girl, "bemused")
                    $ Say_Line(girl, _("Your loss. The door will still be open."))
                    $ Change_Status(girl, "Love", -1)
                    $ shower_door_shut(girl, "come back later (exhibitionist keeps it open)")
                    $ Narration(shower_spot_text("leave_doorway"))
                    call Apply_Time_Cost(TIME_COSTS["shower_wait"]) from _call_Apply_Time_Cost_22
                    jump expression shower_spot_exit()
        else:
            menu:
                "The door was open, it is not my fault.":
                    $ Say_Player(_("The door was open, it is not my fault."))
                    if state == "dressed":
                        $ set_scene_expression(girl, "normal")
                        $ Say_Line(girl, _("I guess that is true. My mistake for leaving it like that."))
                        $ Change_Status(girl, "Love", +1)
                    else:
                        $ set_scene_expression(girl, "perplexed")
                        $ Say_Line(girl, _("Well... You have a point"))
                        $ Change_Status(girl, "Love", +1)
                        $ Change_Status(girl, "Inbt", +5)

                "I do not regret anything.":
                    $ Say_Player(_("I do not regret anything."))
                    python:
                        inbt_val_local = getattr(girl, "Inbt", 0)
                    if inbt_val_local >= 700 or total_seen >= 3:
                        $ set_scene_expression(girl, "sexy")
                        $ Say_Line(girl, _("Bold. You really are enjoying this, huh?"))
                        $ Say_Line(girl, _("Just do not complain if I tease you back next time."))
                        $ Change_Status(girl, "Inbt", +8)
                        $ Change_Status(girl, "Lust", +2, max_val=100)
                    else:
                        $ set_scene_expression(girl, "angry")
                        $ Say_Line(girl, _("Wow. At least pretend to be sorry."))
                        $ Change_Status(girl, "Love", -1)
                        $ Change_Status(girl, "Obed", +1)

                "Sorry, I will come back later.":
                    $ Say_Player(_("Sorry, I will come back later."))
                    $ set_scene_expression(girl, "normal")
                    $ Say_Line(girl, _("Fine. Next time, just knock first."))
                    $ Change_Status(girl, "Love", +1)
                    $ shower_door_shut(girl, "come back later")
                    $ Narration(shower_spot_text("leave_doorway"))
                    call Apply_Time_Cost(TIME_COSTS["shower_wait"]) from _call_Apply_Time_Cost_22a
                    jump expression shower_spot_exit()

        # --- "What did you think?" for the open-door path ---
        python:
            _was_exposed_open = state in ("nude", "underwear", "missing_top", "missing_bottom")
            _is_exhib_open = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")
            _not_angry_open = False
            if _is_exhib_open and _was_exposed_open:
                _not_angry_open = True
            elif state == "nude" and ap_seen >= 3:
                _not_angry_open = True
            elif state in ("underwear", "missing_top", "missing_bottom"):
                if inbt_val >= 650 or total_seen >= 3:
                    _not_angry_open = True
                elif ap_partial >= 3:
                    _not_angry_open = True

        if _was_exposed_open and _not_angry_open:
            $ set_scene_expression(girl, "sexy")
            $ Say_Line(girl, _("So... what did you think of the view?"))

            if state == "nude" or state == "underwear":
                $ girl.RegisterAction("player_saw_boobs")
                $ girl.RegisterAction("player_saw_pussy")
            elif state == "missing_top":
                $ girl.RegisterAction("player_saw_boobs")
            elif state == "missing_bottom":
                $ girl.RegisterAction("player_saw_pussy")

            menu:
                "You looked amazing. I could not look away.":
                    $ Say_Player(_("You looked amazing. I could not look away."))
                    $ set_scene_expression(girl, "smile")
                    $ _scl = _shower_caught_line(girl, "view_amazing")
                    if _scl:
                        $ Say_Line(girl, _scl)
                    else:
                        $ Say_Line(girl, _("Flattery will get you everywhere, you know."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 3)

                "Honestly? I want to see more.":
                    $ Say_Player(_("Honestly? I want to see more."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        $ _scl = _shower_caught_line(girl, "view_more")
                        if _scl:
                            $ Say_Line(girl, _scl)
                        else:
                            $ Say_Line(girl, _("Maybe next time I will not bother with the towel at all."))
                        $ Change_Status(girl, "Inbt", 12)
                        $ Change_Status(girl, "Lust", 5)
                        $ Change_Status(girl, "Love", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        $ Say_Line(girl, _("Slow down, tiger. You have not earned that yet."))
                        $ Change_Status(girl, "Obed", 3)
                        $ Change_Status(girl, "Inbt", 5)

                "I did not really see anything.":
                    $ Say_Player(_("I did not really see anything."))
                    $ set_scene_expression(girl, "perplexed")
                    $ Say_Line(girl, _("Really? Because your eyes told a different story."))
                    $ Change_Status(girl, "Love", -2)

        return

    # ========================================================
    # DEFAULT HANDLING (direct / closed-enter)
    # ========================================================

    if state == "nude":
        # Bracket-adjusted approval threshold
        python:
            _def_T = 1200
            if _sh_tier <= 1:
                if _sh_bracket == 1:   _def_T = 1150
                elif _sh_bracket == 2: _def_T = 1100
                elif _sh_bracket >= 3: _def_T = 1000
        $ ap_seen = ApprovalCheck(girl, T=_def_T, Type="LOI", Spread=150)
        $ set_scene_expression(girl, "sexy" if girl.has_trait("exhibitionist") else "surprised")

        # Bracket-aware narration (exhibitionist gets confident narration)
        if girl.has_trait("exhibitionist"):
            if _sh_bracket == 0:
                $ Narration(_("[girl.Name] notices you walk in. She does not flinch or reach for a towel."))
            elif _sh_bracket <= 2:
                $ Narration(_("[girl.Name] spots you and a knowing smile crosses her face."))
            else:
                $ Narration(_("[girl.Name] glances your way, completely at ease with your presence."))
        elif _sh_tier <= 1 and _sh_bracket == 0:
            $ Narration(_("[girl.Name] freezes completely. This is the first time you have ever walked in on her naked."))
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ Narration(_("[girl.Name] spots you and her eyes widen. She recognizes this situation all too well."))
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ Narration(_("[girl.Name] notices you. She flinches, but recovers quickly this time."))
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ Narration(_("[girl.Name] glances your way, completely unsurprised by your entrance."))
        else:
            $ Narration(_("[girl.Name] jumps a little, clearly startled by your sudden entrance."))

        # Exhibitionist: never covers up, stays confident
        if girl.has_trait("exhibitionist"):
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 8)
            $ _scl = _shower_caught_line(girl, "nude_chill")
            if _scl:
                $ Say_Line(girl, _scl)
            else:
                $ Say_Line(girl, _("Well? Are you just going to stand there?"))

        # Bracket 3 routine: skip anger, familiar/warming
        elif _sh_tier <= 1 and _sh_bracket >= 3 and ap_seen >= 1:
            $ girl.Outfit_Change(over="towel")
            python:
                _enc_mood = "warming" if ap_seen >= 3 else "familiar"
                _enc_line = _shower_enc_line(3, "nude", _enc_mood)
            if ap_seen >= 3:
                $ set_scene_expression(girl, "sexy")
            else:
                $ set_scene_expression(girl, "bemused")
            $ Change_Status(girl, "Lust", 6)
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("At this point, I would be more surprised if you did NOT show up."))

        # Bracket 0 first-time: no chill override, full intensity
        elif _sh_tier <= 1 and _sh_bracket == 0:
            if ap_seen <= 2:
                $ girl.shower_state = "towel"
                $ girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none")
                python:
                    _enc_mood = "angry" if ap_seen <= 1 else "shy"
                    _enc_line = _shower_enc_line(0, "nude", _enc_mood)
                if ap_seen <= 1:
                    $ set_scene_expression(girl, "angry")
                    $ Narration(_("She scrambles for a towel, wrapping it around herself in a panic."))
                    $ Change_Status(girl, "Love", -2)
                else:
                    $ set_scene_expression(girl, "shy")
                    $ Narration(_("She quickly grabs a towel, face turning a deep shade of red."))
                    $ Change_Status(girl, "Love", -1)
                    $ Change_Status(girl, "Lust", 3)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("What are you doing here?! I am naked!"))
            else:
                $ set_scene_expression(girl, "bemused")
                $ girl.Outfit_Change(over="towel")
                $ Change_Status(girl, "Lust", 5)
                python:
                    _enc_line = _shower_enc_line(0, "nude", "chill")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Well, this is a first. Try to knock next time."))

        # Brackets 1-2 or tier 2+: existing logic with bracket-aware dialogue
        elif shower_chill(ap_seen, total_seen) and _sh_bracket > 0:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 8)
            $ _scl = _shower_caught_line(girl, "nude_chill")
            if _scl:
                $ Say_Line(girl, _scl)
            elif _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "nude", "chill")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("You really picked your timing, did you not?"))
            else:
                $ Say_Line(girl, _("You really picked your timing, did you not?"))
                $ Say_Line(girl, _("You have already seen everything anyway..."))
        elif ap_seen <= 1:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "angry")
            $ Narration(_("She quickly grabs a towel and wraps it tightly around herself."))
            $ Change_Status(girl, "Love", -3)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "nude", "angry")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ _scl = _shower_caught_line(girl, "nude_angry")
                    if _scl:
                        $ Say_Line(girl, _scl)
            else:
                $ _scl = _shower_caught_line(girl, "nude_angry")
                if _scl:
                    $ Say_Line(girl, _scl)
        elif ap_seen in (2, 3):
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "shy")
            $ Narration(_("She grabs a towel and wraps it around herself, still blushing."))
            $ Change_Status(girl, "Love", -1)
            $ Change_Status(girl, "Lust", 5)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "nude", "shy")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        else:
            $ set_scene_expression(girl, "sexy")
            $ Narration(_("She does not seem particularly bothered about being naked in front of you."))
            $ Change_Status(girl, "Lust", 10)
            if total_seen >= 3 or inbt_val >= 700:
                $ _scl = _shower_caught_line(girl, "nude_sexy")
                if _scl:
                    $ Say_Line(girl, _scl)
                else:
                    $ Say_Line(girl, _("You have seen me like this more than once now."))
                    $ Say_Line(girl, _("Did you like what you saw this time too?"))

        $ _exp_b = girl.RegisterAction("player_saw_boobs")
        $ _exp_p = girl.RegisterAction("player_saw_pussy")
        if (_exp_b["first_time"] or _exp_p["first_time"]) and not girl.has_trait("exhibitionist"):
            call CaughtExposureReaction(girl, "boobs" if _exp_b["first_time"] else "pussy") from _call_CaughtExposureReaction_3

    elif state == "missing_top":
        # Bracket-adjusted approval threshold
        python:
            _def_T_top = 1150
            if _sh_tier <= 1:
                if _sh_bracket == 1:   _def_T_top = 1100
                elif _sh_bracket == 2: _def_T_top = 1050
                elif _sh_bracket >= 3: _def_T_top = 950
        $ ap_top = ApprovalCheck(girl, T=_def_T_top, Type="LOI", Spread=150)
        $ set_scene_expression(girl, "surprised")

        # Bracket-aware narration
        if _sh_tier <= 1 and _sh_bracket == 0:
            $ Narration(_("[girl.Name] freezes. This is the first time you have caught her with her top off."))
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ Narration(_("[girl.Name] instinctively covers her chest. She remembers last time all too well."))
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ Narration(_("[girl.Name] flinches, but her hands only half-rise to cover herself. She is getting used to this."))
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ Narration(_("[girl.Name] barely reacts to your entrance. Her chest is exposed, and she does not rush to cover it."))
        else:
            $ Narration(_("[girl.Name] freezes for a second, realizing her chest is completely exposed in front of you."))

        # Exhibitionist: does not bother covering up
        if girl.has_trait("exhibitionist"):
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 6)
            $ Say_Line(girl, _("Like what you see? I am not covering up for you."))

        # Bracket 3 routine: skip anger
        elif _sh_tier <= 1 and _sh_bracket >= 3 and ap_top >= 1:
            $ girl.Outfit_Change(over="towel")
            python:
                _enc_mood = "warming" if ap_top >= 3 else "familiar"
                _enc_line = _shower_enc_line(3, "partial", _enc_mood)
            if ap_top >= 3:
                $ set_scene_expression(girl, "sexy")
            else:
                $ set_scene_expression(girl, "bemused")
            $ Change_Status(girl, "Lust", 5)
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("You and my chest are becoming old friends at this point."))

        # Bracket 0 first-time: full intensity
        elif _sh_tier <= 1 and _sh_bracket == 0:
            if ap_top <= 1:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "angry")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "angry")
                $ Narration(_("She scrambles for a towel and covers her chest in a panic."))
                $ Change_Status(girl, "Love", -3)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            elif ap_top in (2, 3):
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "shy")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "shy")
                $ Narration(_("She quickly pulls a towel over her chest, cheeks burning red."))
                $ Change_Status(girl, "Love", -1)
                $ Change_Status(girl, "Lust", 3)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            else:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "bemused")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "chill")
                $ Change_Status(girl, "Lust", 5)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Well, this is a first. Try not to make it a habit."))

        # Brackets 1-2 or tier 2+: existing logic with bracket-aware dialogue
        elif shower_chill(ap_top, total_seen) and _sh_bracket > 0:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 6)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "chill" if _sh_bracket <= 1 else "resigned")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("You really enjoy walking in at moments like this, do you not?"))
            else:
                $ Say_Line(girl, _("You really enjoy walking in at moments like this, do you not?"))
                $ Say_Line(girl, _("You have already seen them before anyway."))
        elif ap_top <= 1:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "angry")
            $ Narration(_("She scrambles for a towel and covers her chest, clearly annoyed."))
            $ Change_Status(girl, "Love", -3)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "angry")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        elif ap_top in (2, 3):
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "shy")
            $ Narration(_("She quickly pulls a towel over her chest, cheeks flushed."))
            $ Change_Status(girl, "Love", -1)
            $ Change_Status(girl, "Lust", 3)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "shy")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        else:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "bemused")
            $ Narration(_("She makes a half-hearted attempt to cover her chest, but does not seem truly upset."))
            $ Change_Status(girl, "Lust", 5)
            if total_seen >= 2 or inbt_val >= 650:
                $ Say_Line(girl, _("You have already seen these before anyway."))

        $ _exp_b = girl.RegisterAction("player_saw_boobs")
        if _exp_b["first_time"] and not girl.has_trait("exhibitionist"):
            call CaughtExposureReaction(girl, "boobs") from _call_CaughtExposureReaction_4

    elif state == "missing_bottom":
        # Bracket-adjusted approval threshold
        python:
            _def_T_bot = 1150
            if _sh_tier <= 1:
                if _sh_bracket == 1:   _def_T_bot = 1100
                elif _sh_bracket == 2: _def_T_bot = 1050
                elif _sh_bracket >= 3: _def_T_bot = 950
        $ ap_bottom = ApprovalCheck(girl, T=_def_T_bot, Type="LOI", Spread=150)
        $ set_scene_expression(girl, "surprised")

        # Bracket-aware narration
        if _sh_tier <= 1 and _sh_bracket == 0:
            $ Narration(_("[girl.Name] goes rigid. This is the first time you have caught her bottomless."))
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ Narration(_("[girl.Name] stiffens. She knows this scenario too well by now."))
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ Narration(_("[girl.Name] notices you, but barely flinches. She has been through this before."))
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ Narration(_("[girl.Name] glances over casually. Being bottomless around you barely registers anymore."))
        else:
            $ Narration(_("[girl.Name] stiffens as she realizes you have a clear view of her lower half."))

        # Exhibitionist: does not bother covering up
        if girl.has_trait("exhibitionist"):
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 6)
            $ Say_Line(girl, _("Enjoying the view? I know I would be."))

        # Bracket 3 routine: skip anger
        elif _sh_tier <= 1 and _sh_bracket >= 3 and ap_bottom >= 1:
            $ girl.Outfit_Change(over="towel")
            python:
                _enc_mood = "warming" if ap_bottom >= 3 else "familiar"
                _enc_line = _shower_enc_line(3, "partial", _enc_mood)
            if ap_bottom >= 3:
                $ set_scene_expression(girl, "sexy")
            else:
                $ set_scene_expression(girl, "bemused")
            $ Change_Status(girl, "Lust", 5)
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("You have seen everything down there so many times, what is the point of hiding?"))

        # Bracket 0 first-time: full intensity
        elif _sh_tier <= 1 and _sh_bracket == 0:
            if ap_bottom <= 1:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "angry")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "angry")
                $ Narration(_("She grabs a towel and yanks it down over her hips in a panic."))
                $ Change_Status(girl, "Love", -3)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            elif ap_bottom in (2, 3):
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "shy")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "shy")
                $ Narration(_("She quickly covers herself below the waist, turning bright red."))
                $ Change_Status(girl, "Love", -1)
                $ Change_Status(girl, "Lust", 3)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            else:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "bemused")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "chill")
                $ Change_Status(girl, "Lust", 5)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("Well, now you have seen everything. Happy?"))

        # Brackets 1-2 or tier 2+: existing logic with bracket-aware dialogue
        elif shower_chill(ap_bottom, total_seen) and _sh_bracket > 0:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 6)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "chill" if _sh_bracket <= 1 else "resigned")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("You really like catching me like this, do you not?"))
            else:
                $ Say_Line(girl, _("You really like catching me like this, do you not?"))
                $ Say_Line(girl, _("You have already seen more than this before."))
        elif ap_bottom <= 1:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "angry")
            $ Narration(_("She grabs a towel and yanks it down over her hips, clearly upset."))
            $ Change_Status(girl, "Love", -3)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "angry")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        elif ap_bottom in (2, 3):
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "shy")
            $ Narration(_("She quickly covers herself, glancing away with a deep blush."))
            $ Change_Status(girl, "Love", -1)
            $ Change_Status(girl, "Lust", 3)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "shy")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        else:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "bemused")
            $ Narration(_("She covers just enough to be decent, but does not seem that bothered."))
            $ Change_Status(girl, "Lust", 5)
            if total_seen >= 2 or inbt_val >= 650:
                $ Say_Line(girl, _("You really like looking down there, do you not?"))

        $ _exp_p = girl.RegisterAction("player_saw_pussy")
        if _exp_p["first_time"] and not girl.has_trait("exhibitionist"):
            call CaughtExposureReaction(girl, "pussy") from _call_CaughtExposureReaction_5

    elif state == "underwear":
        # Bracket-adjusted approval threshold
        python:
            _def_T_und = 1100
            if _sh_tier <= 1:
                if _sh_bracket == 1:   _def_T_und = 1050
                elif _sh_bracket == 2: _def_T_und = 1000
                elif _sh_bracket >= 3: _def_T_und = 900
        $ ap_under = ApprovalCheck(girl, T=_def_T_und, Type="LOI", Spread=150)
        $ set_scene_expression(girl, "surprised")

        # Bracket-aware narration
        if _sh_tier <= 1 and _sh_bracket == 0:
            $ Narration(_("[girl.Name] is standing there in just her underwear, and from the look on her face, this is the first time you have caught her like this."))
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ Narration(_("[girl.Name] is in her underwear again. She sighs the moment she sees you."))
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ Narration(_("[girl.Name] is in her underwear. She glances at you but barely reacts."))
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ Narration(_("[girl.Name] is in her underwear. She does not even bother turning away."))
        else:
            $ Narration(_("[girl.Name] is standing there in just her underwear when you step in."))

        # Bracket 3 routine: skip anger
        if _sh_tier <= 1 and _sh_bracket >= 3 and ap_under >= 1:
            $ girl.Outfit_Change(over="towel")
            python:
                _enc_mood = "warming" if ap_under >= 3 else "familiar"
                _enc_line = _shower_enc_line(3, "partial", _enc_mood)
            if ap_under >= 3:
                $ set_scene_expression(girl, "sexy")
            else:
                $ set_scene_expression(girl, "bemused")
            $ Change_Status(girl, "Lust", 4)
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("At this point, my underwear might as well be a swimsuit to you."))

        # Bracket 0 first-time: full intensity
        elif _sh_tier <= 1 and _sh_bracket == 0:
            if ap_under <= 1:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "angry")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "angry")
                $ Narration(_("She snatches a towel and wraps it around herself in a flash."))
                $ Change_Status(girl, "Love", -2)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            elif ap_under in (2, 3):
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "shy")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "shy")
                $ Narration(_("She folds her arms over herself, face turning pink."))
                $ Change_Status(girl, "Love", -1)
                $ Change_Status(girl, "Lust", 2)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
            else:
                $ girl.Outfit_Change(over="towel")
                $ set_scene_expression(girl, "bemused")
                python:
                    _enc_line = _shower_enc_line(0, "partial", "chill")
                $ Change_Status(girl, "Lust", 4)
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("It is just underwear. Could be worse, I guess."))

        # Brackets 1-2 or tier 2+: bracket-aware dialogue
        elif shower_chill(ap_under, total_seen) and _sh_bracket > 0:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "sexy")
            $ Change_Status(girl, "Lust", 5)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "chill" if _sh_bracket <= 1 else "resigned")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
                else:
                    $ Say_Line(girl, _("You always manage to walk in at the exact moment, do you not?"))
            else:
                $ Say_Line(girl, _("You always manage to walk in at the exact moment, do you not?"))
                $ Say_Line(girl, _("Considering what you have already seen, this is not that bad."))
        elif ap_under <= 1:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "angry")
            $ Narration(_("She snatches a towel and wraps it around herself, clearly annoyed."))
            $ Change_Status(girl, "Love", -2)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "angry")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        elif ap_under in (2, 3):
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "shy")
            $ Narration(_("She folds her arms over herself a bit, clearly embarrassed."))
            $ Change_Status(girl, "Love", -1)
            $ Change_Status(girl, "Lust", 2)
            if _sh_bracket >= 1 and _sh_tier <= 1:
                python:
                    _enc_line = _shower_enc_line(_sh_bracket, "partial", "shy")
                if _enc_line:
                    $ Say_Line(girl, _enc_line)
        else:
            $ girl.Outfit_Change(over="towel")
            $ set_scene_expression(girl, "bemused")
            $ Narration(_("She gives you a look, but still pulls a towel around herself."))
            $ Change_Status(girl, "Lust", 4)
            if inbt_val >= 650:
                $ Say_Line(girl, _("If you stare that much, I might start charging you for the show."))

    elif state == "towel":
        # Bracket-aware towel narration
        if _sh_tier <= 1 and _sh_bracket == 0:
            $ set_scene_expression(girl, "shy")
            $ Narration(_("[girl.Name] is wrapped in a towel. She jumps a little when you walk in."))
            python:
                _enc_line = _shower_enc_line(0, "towel", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ set_scene_expression(girl, "shy")
            $ Narration(_("[girl.Name] is already wrapped in a towel. She gives you a knowing look."))
            python:
                _enc_line = _shower_enc_line(1, "towel", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ set_scene_expression(girl, "bemused")
            $ Narration(_("[girl.Name] is in a towel. She barely reacts to your entrance."))
            python:
                _enc_line = _shower_enc_line(2, "towel", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] is wrapped in a towel. She does not even look up."))
            python:
                _enc_line = _shower_enc_line(3, "towel", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
        else:
            $ set_scene_expression(girl, "shy")
            $ Narration(_("[girl.Name] is already wrapped in a towel when you step in."))

    else:
        # Dressed — bracket-aware narration
        if _sh_tier <= 1 and _sh_bracket == 0:
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] is still fully dressed. She looks at you quizzically."))
            python:
                _enc_line = _shower_enc_line(0, "dressed", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("Oh, hey. I was just about to start. Did you need something?"))
        elif _sh_tier <= 1 and _sh_bracket == 1:
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] is dressed. She seems relieved you caught her before undressing."))
            python:
                _enc_line = _shower_enc_line(1, "dressed", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("Good thing you came now and not two minutes later."))
        elif _sh_tier <= 1 and _sh_bracket == 2:
            $ set_scene_expression(girl, "bemused")
            $ Narration(_("[girl.Name] is still dressed. She barely acknowledges your entrance."))
            python:
                _enc_line = _shower_enc_line(2, "dressed", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("Let me guess... wrong door again?"))
        elif _sh_tier <= 1 and _sh_bracket >= 3:
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] is dressed. She does not even look surprised to see you."))
            python:
                _enc_line = _shower_enc_line(3, "dressed", "neutral")
            if _enc_line:
                $ Say_Line(girl, _enc_line)
            else:
                $ Say_Line(girl, _("You know, at this point I just expect you."))
        else:
            $ set_scene_expression(girl, "normal")
            $ Narration(_("[girl.Name] seems to be finishing up her shower, mostly covered."))
            $ Say_Line(girl, _("Hey. I was just wrapping up here."))

    # --------------------------------------------------------
    # Simple interaction between player and girl once you are inside
    # --------------------------------------------------------
    if girl.has_trait("exhibitionist") and state in ("nude", "underwear", "missing_top", "missing_bottom"):
        $ set_scene_expression(girl, "sexy")
        python:
            _si_exhib = renpy.random.choice([
                (_("So, are you just going to stand there, or are you getting in too?"), _("I do not bite... unless you want me to.")),
                (_("You look like you have never seen a naked girl before."), _("Relax. I am not covering up for anyone.")),
                (_("I left the door unlocked for a reason."), _("Guess you figured that out already.")),
                (_("Go ahead and stare. I do not mind."), _("In fact, I kind of like it.")),
                (_("Most people would be embarrassed right now."), _("Lucky for you, I am not most people.")),
            ])
        $ Say_Line(girl, _si_exhib[0])
        $ Say_Line(girl, _si_exhib[1])
    elif state == "nude":
        if 'ap_seen' in locals() and ap_seen >= 4:
            $ set_scene_expression(girl, "sexy")
            if total_seen >= 3 or inbt_val >= 700:
                python:
                    _si_nude_high = renpy.random.choice([
                        (_("So, are you just going to stand there, or are you getting in too?"), _("And yes, I know you enjoyed the view.")),
                        (_("You could at least close the door behind you."), _("Unless you WANT someone else to see.")),
                        (_("I was wondering when you would show up."), _("You are getting predictable, you know that?")),
                        (_("My eyes are up here."), _("...Not that I mind where yours were looking.")),
                        (_("You know, a normal person would knock."), _("But then again, I do not think either of us qualifies as normal anymore.")),
                    ])
                $ Say_Line(girl, _si_nude_high[0])
                $ Say_Line(girl, _si_nude_high[1])
            else:
                python:
                    _si_nude_ok = renpy.random.choice([
                        _("So, are you just going to stand there, or are you getting in too?"),

                        _("Well, you are already here. Might as well stay."),

                        _("Next time, at least clear your throat or something."),

                    ])
                $ Say_Line(girl, _si_nude_ok)
        else:
            $ set_scene_expression(girl, "uncomfortable")
            python:
                _si_nude_low = renpy.random.choice([
                    _("You could at least give a little warning before barging in."),

                    _("Is it really that hard to knock?"),

                    _("I did not invite you in here. Please at least look away."),

                    _("Can you just... close the door? Please?"),

                ])
            $ Say_Line(girl, _si_nude_low)
    elif state == "towel":
        $ set_scene_expression(girl, "shy")
        python:
            _si_towel = renpy.random.choice([
                _("I was just finishing my shower. Did you need something?"),

                _("Oh, I was about to get dressed. What is it?"),

                _("At least I had a towel ready this time. What do you want?"),

                _("I just got out of the shower. Is something wrong?"),

                _("You caught me at an okay time, I guess. What is up?"),

            ])
        $ Say_Line(girl, _si_towel)
    elif state in ("underwear", "missing_top", "missing_bottom"):
        if inbt_val >= 650 or total_seen >= 3:
            $ set_scene_expression(girl, "sexy")
            python:
                _si_partial_high = renpy.random.choice([
                    _("Next time, try knocking first. Or do you like catching me like this?"),

                    _("You always seem to walk in at the best moments. Coincidence?"),

                    _("At this point I should just stop getting dressed around here."),

                    _("Keep staring like that and I might start giving you a full show."),

                ])
            $ Say_Line(girl, _si_partial_high)
        else:
            $ set_scene_expression(girl, "embarrassed")
            python:
                _si_partial_low = renpy.random.choice([
                    _("Next time, try knocking first, okay?"),

                    _("I was changing... could you at least turn around?"),

                    _("This is embarrassing... please do not stare."),

                    _("I wish you would announce yourself before walking in..."),

                ])
            $ Say_Line(girl, _si_partial_low)

    # --- "What did you think?"... she asks if she wasn't angry and was exposed ---
    python:
        _was_exposed = state in ("nude", "underwear", "missing_top", "missing_bottom")
        _is_exhib = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")
        _not_angry = False
        if _is_exhib and _was_exposed:
            _not_angry = True
        elif state == "nude" and 'ap_seen' in dir() and ap_seen >= 3:
            _not_angry = True
        elif state in ("underwear", "missing_top", "missing_bottom"):
            if inbt_val >= 650 or total_seen >= 3:
                _not_angry = True
            elif state == "underwear" and 'ap_under' in dir() and ap_under >= 3:
                _not_angry = True
            elif state == "missing_top" and 'ap_top' in dir() and ap_top >= 3:
                _not_angry = True
            elif state == "missing_bottom" and 'ap_bottom' in dir() and ap_bottom >= 3:
                _not_angry = True
        if _was_exposed and _not_angry and shower_chill(None, 0) == False:
            # chill girls already commented... only ask if she wasn't in chill mode
            pass

    if _was_exposed and _not_angry:
        $ set_scene_expression(girl, "sexy")
        python:
            _view_question = renpy.random.choice([
                _("So... what did you think of the view?"),

                _("You are staring. Do I look that good?"),

                _("I can feel your eyes on me, you know."),

                _("See something you like?"),

                _("Enjoying yourself over there?"),

            ])
        $ Say_Line(girl, _view_question)

        # Register both saw_boobs and saw_pussy together
        if state == "nude" or state == "underwear":
            $ girl.RegisterAction("player_saw_boobs")
            $ girl.RegisterAction("player_saw_pussy")
        elif state == "missing_top":
            $ girl.RegisterAction("player_saw_boobs")
        elif state == "missing_bottom":
            $ girl.RegisterAction("player_saw_pussy")

        # Pick a random menu variant (3 pools)
        $ _view_menu_roll = renpy.random.randint(1, 3)

        if _view_menu_roll == 1:
            menu:
                "You looked amazing. I could not look away.":
                    $ Say_Player(_("You looked amazing. I could not look away."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Flattery will get you everywhere, you know."),

                            _("That is sweet. Keep talking like that."),

                            _("Smooth. Very smooth."),

                            _("You always know what to say, do you not?"),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 3)

                "Honestly? I want to see more.":
                    $ Say_Player(_("Honestly? I want to see more."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Maybe next time I will not bother with the towel at all."),

                                _("Greedy. I respect that, though."),

                                _("Keep being that honest and you just might."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 12)
                        $ Change_Status(girl, "Lust", 5)
                        $ Change_Status(girl, "Love", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("Slow down, tiger. You have not earned that yet."),

                                _("You are getting ahead of yourself there."),

                                _("Easy. One step at a time."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 3)
                        $ Change_Status(girl, "Inbt", 5)

                "I did not really see anything.":
                    $ Say_Player(_("I did not really see anything."))
                    $ set_scene_expression(girl, "perplexed")
                    python:
                        _vr = renpy.random.choice([
                            _("Really? Because your eyes told a different story."),

                            _("Your face is bright red. Try again."),

                            _("Sure you did not. That is why you are still standing there."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", -2)

        elif _view_menu_roll == 2:
            menu:
                "I am definitely not complaining.":
                    $ Say_Player(_("I am definitely not complaining."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Good. Because I was not planning to apologize."),

                            _("Neither am I, honestly."),

                            _("Well, at least you are honest about it."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 4)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 2)

                "You should leave the door open more often.":
                    $ Say_Player(_("You should leave the door open more often."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Maybe I will. If you ask nicely."),

                                _("Who says I did not leave it open on purpose?"),

                                _("Do not tempt me. I might actually do it."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 12)
                        $ Change_Status(girl, "Lust", 4)
                        $ Change_Status(girl, "Love", 2)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("In your dreams, maybe."),

                                _("Do not push your luck."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)
                        $ Change_Status(girl, "Inbt", 5)

                "Sorry, I will give you some space.":
                    $ Say_Player(_("Sorry, I will give you some space."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("...Thanks. That is actually kind of sweet."),

                            _("Well, at least you have manners sometimes."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 3)

        else:
            menu:
                "I could get used to this.":
                    $ Say_Player(_("I could get used to this."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Do not get TOO used to it. This was a special occasion."),

                            _("Who says I could not get used to the attention?"),

                            _("Careful. I might hold you to that."),

                            _("I bet you could. But I decide when the show starts."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 4)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Change_Status(girl, "Lust", 2)

                "Tell me the truth, did you leave the door open on purpose?":
                    $ Say_Player(_("Tell me the truth, did you leave the door open on purpose?"))
                    if inbt_val >= 600 or total_seen >= 3:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("...Maybe. What are you going to do about it?"),

                                _("I will never tell. But I also will not lock it next time."),

                                _("What if I did? Would that change anything?"),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 15)
                        $ Change_Status(girl, "Lust", 5)
                        $ Change_Status(girl, "Love", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("As if! It was an accident, obviously."),

                                _("Do not flatter yourself. The lock is just broken."),

                                _("You wish. I just forgot."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)
                        $ Change_Status(girl, "Inbt", 5)

                "I really did not mean to walk in on you.":
                    $ Say_Player(_("I really did not mean to walk in on you."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("I know. You looked just as surprised as I was."),

                            _("I believe you. This time."),

                            _("That is what you said last time too, but okay."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

        return

    # ── State-specific player response menus ──

    # DRESSED — player teases about missing the show
    if state == "dressed":
        $ _dressed_menu_roll = renpy.random.randint(1, 4)

        if _dressed_menu_roll == 1:
            menu:
                "Too bad... I will be quicker next time.":
                    $ Say_Player(_("Too bad... I will be quicker next time."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Oh? So you are admitting you are trying to catch me?"),

                                _("Big talk. We will see about that."),

                                _("Quicker? Sounds like a challenge. I accept."),

                                _("Maybe I will slow down next time. Just to make it fair."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 8)
                        $ Change_Status(girl, "Lust", 2)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("Excuse me? That is creepy, not flattering."),

                                _("Do not make this weird. I am dressed. End of story."),

                                _("Yeah, no. How about you just knock next time?"),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)

                "I was not expecting anything different, do not get me wrong.":
                    $ Say_Player(_("I was not expecting anything different, do not get me wrong."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Sure you were not. Your face says otherwise."),

                            _("Uh huh. Very convincing."),

                            shower_spot_text("girl_no_reason"),

                            _("That was almost believable. Almost."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 3)

                "I will leave you to it.":
                    $ Say_Player(_("I will leave you to it."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Thanks. I appreciate that."),

                            _("...You do not HAVE to leave, but okay."),

                            _("That is probably for the best."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

        elif _dressed_menu_roll == 2:
            menu:
                "Wanna change that?":
                    $ Say_Player(_("Wanna change that?"))
                    if inbt_val >= 600 or total_seen >= 3:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("...Are you asking me to undress? Bold."),

                                _("Maybe. If you ask nicely enough."),

                                _("You first. Fair is fair."),

                                _("Hmm... tempting offer. I will think about it."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 12)
                        $ Change_Status(girl, "Lust", 4)
                        $ Change_Status(girl, "Love", 2)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("Wow. Just... wow. No."),

                                _("In your dreams, maybe."),

                                _("That is NOT how this works."),

                                _("You are lucky I find that more funny than offensive."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 3)
                        $ Change_Status(girl, "Inbt", 3)

                "Just checking on you. Carry on.":
                    $ Say_Player(_("Just checking on you. Carry on."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("That is sweet. Weird, but sweet."),

                            shower_spot_text("girl_check_on"),

                            _("How thoughtful. Now get out so I can actually shower."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 3)

                "Well, at least I know you are safe.":
                    $ Say_Player(_("Well, at least I know you are safe."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Safe from what? Shampoo attacks?"),

                            _("My hero. Now please leave before I undress."),

                            _("That is actually kind of cute. But still... knock next time."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

        elif _dressed_menu_roll == 3:
            menu:
                "I will just have to come back at a better time.":
                    $ Say_Player(_("I will just have to come back at a better time."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Define 'better.' For you, or for me?"),

                                _("Careful what you wish for. You might actually succeed."),

                                _("I will make sure to NOT lock the door. Just for you."),

                                _("Maybe next time I will forget my towel. Accidentally, of course."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 10)
                        $ Change_Status(girl, "Lust", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("Or you could just... not come at all?"),

                                _("There is no 'better time' for this. Stop trying."),

                                _("How about never? Is never a good time?"),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)

                "Good, I prefer talking to you with clothes on anyway.":
                    $ Say_Player(_("Good, I prefer talking to you with clothes on anyway."))
                    $ set_scene_expression(girl, "perplexed")
                    python:
                        _vr = renpy.random.choice([
                            _("...Was that supposed to be a compliment? I honestly can not tell."),

                            _("Ouch? Or... thanks? I am confused."),

                            _("That might be the most backhanded thing anyone has ever said to me."),

                            _("Smooth. Real smooth."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

                "Sorry, wrong room.":
                    $ Say_Player(_("Sorry, wrong room."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Sure it was. You always end up in the 'wrong room.'"),

                            _("The 'wrong room' that you keep walking into. Right."),

                            _("Mmhm. Very convincing exit strategy."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

        else:
            menu:
                "Damn. Fully dressed. My luck is terrible.":
                    $ Say_Player(_("Damn. Fully dressed. My luck is terrible."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "smile")
                        python:
                            _vr = renpy.random.choice([
                                _("Ha! At least you are honest about it."),

                                _("Terrible luck? Or am I just faster than you?"),

                                _("Maybe your luck will change. Who knows?"),

                                _("Keep showing up and the odds are bound to shift eventually."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Love", 3)
                        $ Change_Status(girl, "Inbt", 5)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("Your 'luck'? Excuse me?"),

                                _("That is not luck. That is me being smart about locks."),

                                _("And it is going to STAY terrible. Trust me."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)

                "Honestly, you look good either way.":
                    $ Say_Player(_("Honestly, you look good either way."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("That was actually sweet. Points for that."),

                            _("Okay, that one got me. Well played."),

                            _("Flattery noted. And appreciated."),

                            _("You are getting better at this. Keep practicing."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 3)

                "I will get out of your way.":
                    $ Say_Player(_("I will get out of your way."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Okay. See you later then."),

                            _("You are sweet for not making this weird."),

                            _("Go on. I need to finish up anyway."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

        return

    # TOWEL — player responds to towel state
    if state == "towel":
        $ _towel_menu_roll = renpy.random.randint(1, 3)

        if _towel_menu_roll == 1:
            menu:
                "That towel is doing a lot of heavy lifting right now.":
                    $ Say_Player(_("That towel is doing a lot of heavy lifting right now."))
                    if inbt_val >= 500 or total_seen >= 2:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Jealous of a towel? That is a new low."),

                                _("One tug and it is gone. Do not tempt me."),

                                _("It is working harder than you, that is for sure."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 8)
                        $ Change_Status(girl, "Lust", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("And it is going to KEEP doing its job. Eyes up."),

                                _("Are you seriously commenting on my towel right now?"),

                                _("It is doing fine. Unlike your manners."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)
                        $ Change_Status(girl, "Inbt", 3)

                "Sorry, I did not mean to startle you.":
                    $ Say_Player(_("Sorry, I did not mean to startle you."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("It is fine. You just caught me off guard."),

                            _("Do not worry about it. These things happen."),

                            _("At least you did not scream. That would have been worse."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

                "I will leave you to it.":
                    $ Say_Player(_("I will leave you to it."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Thanks. I appreciate that."),

                            _("...You do not HAVE to leave, but okay."),

                            _("That is probably for the best."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

        elif _towel_menu_roll == 2:
            menu:
                "I was just passing by. Bad timing.":
                    $ Say_Player(_("I was just passing by. Bad timing."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("Or good timing, depending on how you look at it."),

                            _("Sure, 'just passing by.' You always seem to pass by at the right moment."),

                            _("Bad timing? Or perfect timing?"),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

                "You could always lose the towel, you know.":
                    $ Say_Player(_("You could always lose the towel, you know."))
                    if inbt_val >= 600 or total_seen >= 3:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Maybe. You first, though."),

                                _("And give you the satisfaction? ...Maybe."),

                                _("Ask me again when you have earned it."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 10)
                        $ Change_Status(girl, "Lust", 4)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("And YOU could learn to knock. We all have dreams."),

                                _("Absolutely not. Get out."),

                                _("The audacity. Honestly."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 3)
                        $ Change_Status(girl, "Inbt", 3)

                "I will get out of your way.":
                    $ Say_Player(_("I will get out of your way."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Okay. See you later then."),

                            _("You are sweet for not making this weird."),

                            _("Go on. I need to get dressed anyway."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

        else:
            menu:
                "You know, you could always invite me in.":
                    $ Say_Player(_("You know, you could always invite me in."))
                    if inbt_val >= 650 or total_seen >= 3:
                        $ set_scene_expression(girl, "sexy")
                        python:
                            _vr = renpy.random.choice([
                                _("Maybe if you ask a bit nicer than that."),

                                _("Tempting. But you would have to earn it."),

                                _("Do not give me ideas. I might actually consider it."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Inbt", 10)
                        $ Change_Status(girl, "Lust", 3)
                    else:
                        $ set_scene_expression(girl, "bemused")
                        python:
                            _vr = renpy.random.choice([
                                _("In your dreams. Now shoo."),

                                _("You have got some nerve. I will give you that."),

                                _("Absolutely not. But nice try."),

                            ])
                        $ Say_Line(girl, _vr)
                        $ Change_Status(girl, "Obed", 2)
                        $ Change_Status(girl, "Inbt", 5)

                "Well, this is awkward. Sorry about that.":
                    $ Say_Player(_("Well, this is awkward. Sorry about that."))
                    $ set_scene_expression(girl, "smile")
                    python:
                        _vr = renpy.random.choice([
                            _("A little. But at least you are polite about it."),

                            _("It is only awkward if you make it awkward."),

                            _("Do not apologize too much. It makes it weirder."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 2)

                "I did not see anything. Promise.":
                    $ Say_Player(_("I did not see anything. Promise."))
                    $ set_scene_expression(girl, "normal")
                    python:
                        _vr = renpy.random.choice([
                            _("Liar. But I will let it slide this time."),

                            _("Your red face says otherwise, but sure."),

                            _("I do not believe you at all, but thanks for trying."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Love", 1)

        return

    # GENERIC non-exposed fallback (underwear states with non-exposed flow)
    $ _default_menu_roll = renpy.random.randint(1, 3)

    if _default_menu_roll == 1:
        menu:
            "Sorry, I did not mean to startle you.":
                $ Say_Player(_("Sorry, I did not mean to startle you."))
                $ set_scene_expression(girl, "smile")
                python:
                    _vr = renpy.random.choice([
                        _("It is fine. You just caught me off guard."),

                        _("Do not worry about it. These things happen."),

                        _("You scared me a little, but it is okay."),

                        _("At least you did not scream. That would have been worse."),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 2)

            "I do not mind the view, to be honest.":
                $ Say_Player(_("I do not mind the view, to be honest."))
                if inbt_val >= 650 or total_seen >= 3:
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _vr = renpy.random.choice([
                            _("I noticed. Maybe I do not mind being looked at either."),

                            _("Well, you are not exactly looking away, are you?"),

                            _("Careful. I might start putting on a show."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Lust", 2)
                else:
                    $ set_scene_expression(girl, "bemused")
                    python:
                        _vr = renpy.random.choice([
                            _("You are way too honest sometimes."),

                            _("Bold of you to say that while I am standing here."),

                            _("That is... weirdly flattering. Now stop staring."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Obed", 2)
                    $ Change_Status(girl, "Inbt", 5)

            "I will leave you to it.":
                $ Say_Player(_("I will leave you to it."))
                $ set_scene_expression(girl, "normal")
                python:
                    _vr = renpy.random.choice([
                        _("Thanks. I appreciate that."),

                        _("...You do not HAVE to leave, but okay."),

                        _("That is probably for the best."),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 1)

    elif _default_menu_roll == 2:
        menu:
            "I was just passing by. Bad timing.":
                $ Say_Player(_("I was just passing by. Bad timing."))
                $ set_scene_expression(girl, "smile")
                python:
                    _vr = renpy.random.choice([
                        _("Or good timing, depending on how you look at it."),

                        _("Sure, 'just passing by.' You always seem to pass by at the right moment."),

                        _("It is fine. I have had worse interruptions."),

                        _("Bad timing? Or perfect timing?"),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 2)

            "I have to admit, you look great.":
                $ Say_Player(_("I have to admit, you look great."))
                if inbt_val >= 650 or total_seen >= 3:
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _vr = renpy.random.choice([
                            _("Keep talking like that and I might let you stay."),

                            _("I know. But it is nice to hear you say it."),

                            _("Flattery works on me more than you think."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Change_Status(girl, "Lust", 2)
                    $ Change_Status(girl, "Love", 2)
                else:
                    $ set_scene_expression(girl, "bemused")
                    python:
                        _vr = renpy.random.choice([
                            _("Thanks, but you should probably look somewhere else."),

                            _("Smooth. Now please turn around."),

                            _("I would say thank you, but this is still awkward."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Obed", 2)
                    $ Change_Status(girl, "Inbt", 5)

            "I will get out of your way.":
                $ Say_Player(_("I will get out of your way."))
                $ set_scene_expression(girl, "normal")
                python:
                    _vr = renpy.random.choice([
                        _("Okay. See you later then."),

                        _("You are sweet for not making this weird."),

                        _("Go on. I need to finish up anyway."),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 1)

    else:
        menu:
            "Well, this is awkward. Sorry about that.":
                $ Say_Player(_("Well, this is awkward. Sorry about that."))
                $ set_scene_expression(girl, "smile")
                python:
                    _vr = renpy.random.choice([
                        _("A little. But at least you are polite about it."),

                        _("It is only awkward if you make it awkward."),

                        _("Could be worse. You could have brought a camera."),

                        _("Do not apologize too much. It makes it weirder."),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 2)

            "You know, you could always invite me in.":
                $ Say_Player(_("You know, you could always invite me in."))
                if inbt_val >= 650 or total_seen >= 3:
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _vr = renpy.random.choice([
                            _("Maybe if you ask a bit nicer than that."),

                            _("Tempting. But you would have to earn it."),

                            _("Do not give me ideas. I might actually consider it."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Inbt", 10)
                    $ Change_Status(girl, "Lust", 3)
                else:
                    $ set_scene_expression(girl, "bemused")
                    python:
                        _vr = renpy.random.choice([
                            _("In your dreams. Now shoo."),

                            _("You have got some nerve. I will give you that."),

                            _("Absolutely not. But nice try."),

                        ])
                    $ Say_Line(girl, _vr)
                    $ Change_Status(girl, "Obed", 2)
                    $ Change_Status(girl, "Inbt", 5)

            "I did not see anything. Promise.":
                $ Say_Player(_("I did not see anything. Promise."))
                $ set_scene_expression(girl, "normal")
                python:
                    _vr = renpy.random.choice([
                        _("Liar. But I will let it slide this time."),

                        _("Your red face says otherwise, but sure."),

                        _("I do not believe you at all, but thanks for trying."),

                    ])
                $ Say_Line(girl, _vr)
                $ Change_Status(girl, "Love", 1)

    return

# ============================================================
# CAUGHT MASTURBATING IN SHOWER
# Same structure as bedroom caught_masturbating but adapted
# for the shower setting (public location, already nude, water sounds)
# ============================================================
label caught_masturbating_shower(girl):

    call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_shower_mast

    # Save outfit BEFORE stripping so we can restore after the scene
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    # Show door overlay — player hears something from outside
    show door_open zorder 151

    $ Narration(shower_spot_text("mast_arrive"))
    $ Narration(_("But mixed with the sound of water, you hear something else... soft moaning."))
    $ Narration(_("You quietly step closer and peek around the corner."))

    # Hide door — player steps inside
    hide door_open
    with dissolve

    # Full nude in shower
    python:
        girl.Collar = False
        girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")

    # Launch masturbation scene with eyes closed + moaning mouth
    python:
        state = sprite_state.setdefault(girl.Id, {})
        state["eyes"] = "eyes_closed"
        state["mouth"] = renpy.random.choice(["mouth_open_teeth", "mouth_sch", "mouth_serious"])
        _mpose = getattr(girl, "mast_pose", "cowgirl")
        if _mpose == "laying_down":
            store.laying_speed = 2
        elif _mpose == "doggy":
            store.doggy_speed = 2
        else:
            store._cg_eyes_locked = True
            store._cg_force_static = True
            store.cowgirl_guy_arms_visible = False
            store.cowgirl_speed = 2

    call MASTURBATE_Launch_Caught(girl) from _call_MASTURBATE_Launch_Caught_shower

    $ girl.RegisterAction("girl_caught_masturbating")
    $ unlock_achievement("shower_masturbation")
    $ _mast_fantasy_count = 0

    $ Narration(_("[girl.Name] is leaning against the shower wall, eyes closed, completely lost in the moment."))
    $ Narration(_("The steam and running water mask any sound you might make."))
    $ store._recorded_this_session = False

label .shower_watch_loop:

    menu:
        "Keep watching":
            python:
                _girl_lust_gain(girl, 4)
                _mast_fantasy_count += 1

            # --- Fantasy moans: she whispers her fantasies ---
            python:
                _fantasy_chance = 0
                if _mast_fantasy_count >= 2:
                    _fantasy_chance = min(25 + (girl.Lust - 40), 60) if girl.Lust >= 40 else 15
                _do_fantasy = _fantasy_chance > 0 and renpy.random.randint(1, 100) <= _fantasy_chance
            if _do_fantasy:
                $ _fline = _pick_masturbation_fantasy(girl)
                $ Say_Line(girl, _fline)

            # Sex escalation: she moans about needing more
            python:
                _wl_flags = getattr(girl, "intimacy_flags", set()) or set()
                _wl_has_history = bool(_wl_flags & {"sex", "bj", "hj", "tj"})
                _wl_chance = 0
                if girl.Lust >= 80 and _wl_has_history:
                    _wl_chance = min(15 + (girl.Lust - 80), 40)
                _wl_wants = _wl_chance > 0 and renpy.random.randint(1, 100) <= _wl_chance
            if _wl_wants:
                $ Narration(_("Her moaning gets louder, echoing off the shower tiles."))
                $ Say_Line(girl, _pick_masturbation_fantasy(girl))
                menu:
                    "Step in and offer yourself":
                        jump .shower_show_presence_for_sex
                    "Keep watching quietly":
                        pass

            if girl.Lust >= 100:
                call GirlCumming(girl, "masturbate", getattr(girl, "mast_pose", "cowgirl"), scene_override="secret_masturbate") from _call_GirlCumming_shower_mast
                if not store._cg_eyes_locked:
                    jump .shower_reaction
            jump .shower_watch_loop

        "Show your presence":
            jump .shower_show_presence

        "Record her quietly" if not getattr(store, "_recorded_this_session", False):
            jump .shower_record

        "Leave quietly":
            $ Narration(shower_spot_text("mast_leave"))
            call COWGIRL_End(girl, dress_up=False, was_secret=True) from _call_COWGIRL_End_shower_mast_leave
            $ girl.WearPreset("casual", apply_now=False)
            $ girl.shower_state = "dressed"
            jump expression shower_spot_exit()

label .shower_show_presence_for_sex:
    $ _mast_presence_break(girl)

    $ Say_Player(_("Need a hand? Or... something else?"))
    $ set_scene_expression(girl, "embarrassed")

    # Cheat path gate: she won't just "get in here" if she hasn't broken
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        python:
            _cep = getattr(girl, "_cheat_escalation_path", 0)
            if _cep == 1:
                _mast_deny = [
                    _("How long were you... NO! I have a {hint}%(pl)s{/hint}! This is... I was just... Leave! NOW!"),

                    _("Oh my god you SAW that?! I have a {hint}%(pl)s{/hint}! This doesn't mean ANYTHING! Get OUT!"),

                    _("You're disgusting! I was just... I have a %(pl)s! This is PRIVATE! LEAVE!"),

                ]
            elif _cep == 2:
                _mast_deny = [
                    _("How long were you... god, I'm so embarrassed. I have a {hint}%(pl)s{/hint}... I can't just... no. Not like this."),

                    _("You caught me... but I have a {hint}%(pl)s{/hint}. I can't let this go further. Not now."),

                    _("I was thinking about... never mind. I have someone. This can't happen. Go."),

                ]
            else:
                _mast_deny = [
                    _("Of course you'd show up NOW... but I have a {hint}%(pl)s{/hint}. Even %(pp)s doesn't deserve this. ...Go."),

                    _("Great timing... but no. I have a {hint}%(pl)s{/hint} and even though %(pp)s ignores me, I can't do THIS. Leave."),

                    _("You saw nothing. I have a {hint}%(pl)s{/hint}. ...Even if %(pp)s doesn't deserve my loyalty. Just go."),

                ]
        $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_mast_deny))))
        $ Change_Status(girl, "Inbt", 5)
        $ Change_Status(girl, "Lust", 10)
        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_mast_deny
        $ girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")
        $ scene_full_cleanup(girl)
        return
    else:
        $ Say_Line(girl, _("How long were you...?! ...Don't answer that. Just... get in here."))
        $ set_scene_expression(girl, "lusty")

    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_sexesc
    # Ensure she stays nude (shower) and reset saved outfit to nude state
    $ girl.Collar = False
    $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
    $ girl._saved_outfit = None
    call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_shower_mast
    return

label .shower_show_presence:

    $ _mast_presence_break(girl)

    $ Say_Line(girl, _("W-What?! How long have you been standing there?!"))
    $ Say_Player(_("Long enough. The steam didn't hide much."))
    $ Say_Line(girl, _("Oh my god... this is so embarrassing..."))

    jump .shower_reaction

label .shower_reaction:

    # Stat check — can we stay?
    python:
        _mb_cfg = ApprovalRuleFor(girl=girl, action="masturbate", category="sex")
        _ap_result = ApprovalCheck(girl, T=_mb_cfg["T"], Type=_mb_cfg["Type"], Spread=_mb_cfg["Spread"], Bonus=_mb_cfg["Bonus"], Variation=_mb_cfg["Variation"], ReturnData=True, Action="masturbate")
        _ap_ok = _ap_result["accepted"]
        if _ap_ok and girl.has_npc_partner():
            _ap_ok = get_effective_cheat_attitude(girl, action="masturbate") >= 3

    if _ap_ok:
        menu:
            "Can I keep watching?":
                $ Say_Line(girl, _("Fine... but if anyone else walks in, you're dead."))
                $ _mast_presence_resume(girl)
                call MASTURBATE_ApplySpeed(girl, _mast_speed(girl)) from _call_MASTURBATE_ApplySpeed_shower
                $ renpy.hide("cowgirl_guy")
                call MASTURBATE_ControlMenu(girl) from _call_MASTURBATE_ControlMenu_shower
                return

            "Offer something more":
                # Cheat path gate
                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False) and _cheat_stage(girl) < 2:
                    python:
                        _cep = getattr(girl, "_cheat_escalation_path", 0)
                        if _cep == 1:
                            _offer_deny = _("I... no. I have a {hint}%(pl)s{/hint}. What you saw was private. We can't go further.")
                        elif _cep == 2:
                            _offer_deny = _("I appreciate the offer but... I'm not ready for that. Not here, not now.")
                        else:
                            _offer_deny = _("As tempting as that is... not here. Too risky. Somewhere we can do this properly without interruptions.")
                    $ Say_Line(girl, _format_partner_line(girl, _offer_deny))
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_offer_deny
                    $ scene_full_cleanup(girl)
                    return
                call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_offer
                # Ensure she stays nude (shower) and reset saved outfit to nude state
                $ girl.Collar = False
                $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                $ girl._saved_outfit = None
                $ Say_Line(girl, shower_spot_text("girl_here"))
                call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_shower_offer
                return

            "Leave":
                $ Change_Status(girl, "Obed", -10)
                $ Say_Line(girl, _("Please just go. And forget you saw this."))
                call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_leave2
                $ scene_full_cleanup(girl)
                $ girl.WearPreset("casual", apply_now=False)
                $ girl.shower_state = "dressed"
                return "left"
    elif girl.has_trait("exhibitionist") or girl.has_trait("public_fetish"):
        python:
            _exhib_tease_shower = [
                _("No free show for you! But... did you enjoy what you saw?"),
                _("Hey! Show's over. But I bet you liked the preview, didn't you?"),
                _("Caught me, huh? Well... no encore today. Maybe next time, if you're lucky."),
                _("You're such a perv. But honestly? Knowing you watched was kind of hot."),
            ]
            set_scene_expression(girl, "embarrassed", blush="1")
            Say_Line(girl, _tl(renpy.random.choice(_exhib_tease_shower)))
        $ Change_Status(girl, "Lust", 5)
        $ Change_Status(girl, "Obed", 5)
        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_exhib_mast
        $ scene_full_cleanup(girl)
        $ girl.WearPreset("casual", apply_now=False)
        $ girl.shower_state = "dressed"
        return
    else:
        python:
            Say_Line(girl, _("GET OUT! Are you serious right now?!"))
            girl.set_temp_status("angry", 1)
            set_scene_expression(girl, "angry")
        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_shower_kick
        $ scene_full_cleanup(girl)
        $ girl.WearPreset("casual", apply_now=False)
        $ girl.shower_state = "dressed"
        # she storms off for REAL: her loc used to stay in the bathroom, so the tracker swore she was
        # still in there while the room showed empty (tester 2026-10-11, "spooky")
        $ girl.loc = girl_home_loc(girl)
        $ hide_girl_sprite(girl)
        jump expression shower_spot_exit()

label .shower_record:

    $ store._recorded_this_session = True
    python:
        vid = {
            "girl_gid": girl.gid,
            "type": "masturbate",
            "location": CurrentLocation,
            "committed": False,
            "consensual": False,
            "face_hidden": False,
            "hd": Player.has_item("tekmix_camera"),
        }
        _tag_coercion_on_vid(vid)
        store.Player.recorded_videos.append(vid)

    $ Narration(_("You carefully take out your phone and record a short video through the steam."))
    $ Narration(_("The sound of water covers the click. She doesn't notice."))
    jump .shower_watch_loop
