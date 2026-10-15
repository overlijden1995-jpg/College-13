# ============================================================
# stepmom_story.rpy... the story of the "stepmom" ROLE on the steps engine (story_steps.rpy,
# docs/plan_role_situations.md). Any girl with GIRLS_CONFIG "role": "stepmom" climbs it (today Shion).
#
#   step 0 cold         he gets talk, gifts, compliments; she cuts every flirt
#   step 1 she_decides  + his hands, a kiss, she touches herself for him, her hand
#   step 2 giving_in    + oral on her, her mouth, her chest, sex, the rimjob
#   step 3 his          + anal, inside her, her pill, the netori call and the ring
#
# THE UNLOCK EVENTS (one per step, each with a version per route):
#   0 -> 1 hand_under_table   Love 200 / Inbt 300 / Obed 150 / evidence 1   at a Sunday dinner (trigger "dinner")
#   1 -> 2 vent_night         Love 350 / Inbt 450 / Obed 300 / blackmail 4   he sleeps alone, last grade >= B (trigger "sleep")
#   2 -> 3 marital_bed        Love 550 / Inbt 600 / Obed 500             a morning he is away (trigger "morning")
#
# THE MARITAL BED (2 -> 3): a morning her husband is away on a trip she texts him home. "On
# my way.": the bedroom she shares with his father, the version of her route (STORY_SCENES), a restricted scene
# (STORY_MARITAL "acts"), then the lines of her new step (STORY_TURN_LINES 3). "I can't today.": she stays on her
# step (story_unlock_cancel) and texts again after the cooldown.
# STEP 2 EVENTS (STORY_MOMENTS, three choices one per stat): distract_father (the apartment in the Evening with her
# husband home), short_vent (she knocks at his dorm room in the Evening, ten minutes, then goes: also at step 3),
# husband_calls (during sex with her, her husband calls; not in the apartment with him, not the vent night).
# STEP 0 EVENTS (docs/plan_story_dynamism.md F1, the cold investor; no warmth, the step cap rules the gains):
# grade_summons (a dry text about his bad exam, STORY_TEXTS chat "grades", steps 0-2), inspection (the hallway),
# mall_errand (she makes him carry her bags), wine_check (she counts the bottles), home_late (the late bus sees a
# black car drop her off: the seed of her secret, narrated over Downtown).
# HER INITIATIVE (F3, one restricted scene each, act by the route that opened her step): her_terms (step 1, the
# apartment, husband out), stolen_minutes (step 2, her husband one room away, four minutes), her_appetite (step 3,
# his dorm at night, the inbt route is anal). Step 3 also keeps her night texts (chats "mine", "stolen_shirt").
# HUSBAND_STEPS (F4, steps 2+, trigger "sex"): his footsteps in the hallway during a scene in the apartment.
# HER STEP'S VOICE OUTSIDE EVENTS (story_steps.rpy): the first word of the day (_story_talk_greet, rod_lines
# "talk_greet.<step>", the days after an unlock read its route), a gift (story_gift_line, "gift_react.<step>"),
# the follow invite (act "outing", step 1: story_locked "outing" / "outing_accept.<step>"), and the afterglow of a
# normal scene at steps 2+ (_story_afterscene, GIRL_SEX_LINES "afterscene.<step>.<route>").
#
# THE VENT NIGHT (1 -> 2): as he goes to bed in his dorm room (alone, her husband home that night), she
# knocks: a fight with his father. The version of her route (STORY_SCENES), then he lets it happen or sends her
# home. Let it happen: a restricted HJ scene (STORY_VENT), and after he finishes she tries to take her turn but
# her husband calls and she has to leave. She is gone before dawn.
# HER TEXTS AT NIGHT (step event "her_night_text", steps 1 and 2): at Night, when she is not with him, more often the
# more she loves him; three replies, one per stat (STORY_TEXTS).
#
# THE HINTS (STORY_HINTS, story_steps.rpy story_unlock_hint): the moment of an unlock came and no route passed (a
# Sunday dinner at step 0, a night in his bed with her husband home at step 1, a morning her husband is away at step
# 2): one narration line on a route, "close" when one is near its limit, else her routes in turn.
# THE SUNDAY DINNER (step event "family_dinner", steps 0 to 3, "planned"): after the first dinner the father invites
# him every Sunday (shion_family.rpy). At the table, one moment of STORY_DINNERS (her own, else her role's) with
# three choices, one per stat (story_test / story_choice_reward); her goodbye by step. When a route of her step 0
# passes, the dinner is the unlock instead: "the hand under the table" (STORY_SCENES), then the lines of her new step.
# The FIRST dinner counts too (author 2026-10-11): its scripted introduction plays, then the unlock when a route
# already passes (it used to play only the "everything is in place" nudge, read as "nothing changed").
# Role lines: the faces every girl has (normal, happy, sexy, smug, shy, angry, sad, surprised), no name, no job.
# ============================================================


init 1 python:

    STORY_EVENTS.update({
        "hand_under_table": {
            "trigger": "dinner", "scene": "hand_under_table", "label": "_story_hand_under_table",
            # "evidence": his proof of her secret (a girl's own story: shion_hashimoto.rpy, her version of the scene)
            "routes": (("love", {"Love": 200}), ("inbt", {"Inbt": 300}), ("obed", {"Obed": 150}),
                       ("evidence", {"evidence": 1})),
        },
        "vent_night": {
            "trigger": "sleep", "scene": "vent_night", "label": "_story_vent_night", "where": ("room",),
            "visit": True, "alone": True, "requires": "story_vent_night_ready", "cooldown": 7,
            "knock": _("You pull the covers back and reach for the lamp. Before you can turn it off, someone knocks. Three soft knocks, then one hard one."),
            "routes": (("love", {"Love": 350}), ("inbt", {"Inbt": 450}), ("obed", {"Obed": 300}),
                       ("blackmail", {"blackmail": 4})),
        },
        "her_night_text": {
            "trigger": "text", "label": "_story_text", "apart": True, "slot_min": 3, "cooldown": 2,
            "chance": 0.10, "chance_per": {"Love": 0.0005},
        },
        "marital_bed": {
            "trigger": "morning", "label": "_story_marital_bed", "slot_max": 0, "cooldown": 3,
            "requires": "story_husband_on_trip",
            # blackmail: the route spans ALL her unlocks (author, 2026-10-09): 4 -> 6 -> 9 (score = his video
            # leverage + the bar proof x STORY_EVIDENCE_VALUE, capped at 10)
            "routes": (("love", {"Love": 550}), ("inbt", {"Inbt": 600}), ("obed", {"Obed": 500}),
                       ("blackmail", {"blackmail": 6})),
            # the coerced lane lets HIM name the night (story_event_play, "bm_demands"): first entry = scripted
            "bm_demands": ((_("Everything, her way."), None), (_("Only her mouth tonight."), "bj_only")),
        },
        "distract_father": {
            "trigger": "location", "moment": "distract_father", "meet": True, "where": APARTMENT_ROOMS,
            "slot_min": 2, "slot_max": 2, "chance": 0.35, "cooldown": 3, "requires": "story_husband_next_room",
        },
        "short_vent": {
            "trigger": "location", "moment": "short_vent", "where": ("room",), "visit": True, "alone": True,
            "leaves": True, "slot_min": 2, "slot_max": 2, "chance": 0.25, "cooldown": 4,
            "knock": _("A knock at your door. You already know that knock."),
        },
        "husband_calls": {
            "trigger": "sex", "moment": "husband_calls", "chance": 0.3, "cooldown": 3,
            "requires": "story_husband_call_due",
        },
        "family_dinner": {
            "trigger": "dinner", "label": "_story_family_dinner", "planned": True,
        },
        "drugged_dinner": {
            "trigger": "dinner", "label": "_story_drugged_dinner", "planned": True,
            "requires": "story_drugged_dinner_ready",
            # blackmail 9: the bar proof alone (8) is not enough for the last step, he needs at least one real
            # video of her on top of it (or 9+ of video leverage with no proof at all)
            "routes": (("love", {"Love": 700}), ("inbt", {"Inbt": 750}), ("obed", {"Obed": 650}),
                       ("blackmail", {"blackmail": 9})),
            # the coerced lane lets HIM name the night (story_event_play, "bm_demands"): first entry = scripted.
            # demand_late: the ask plays INSIDE the event, after her "come with me" (tester 2026-10-11:
            # picking the condom before the dinner even started felt wrong)
            "bm_demands": ((_("Her way. Nothing between you."), None), (_("With a condom."), "condom")),
            "demand_late": True,
        },
        # ── F2 micro-moments (plan_shion_agency): her ladder alive in free roam ──
        "mall_treat": {
            "trigger": "location", "moment": "mall_treat", "meet": True, "where": ("mall",),
            "chance": 0.30, "cooldown": 4,
        },
        "car_ten_minutes": {
            "trigger": "location", "moment": "car_ten_minutes", "where": ("campus",),
            "slot_min": 1, "slot_max": 2, "chance": 0.18, "cooldown": 5,
        },
        # ── STEP 0, the cold investor: she summons, inspects and uses him; no warmth, small gains (the cap rules) ──
        "grade_summons": {
            "trigger": "text", "label": "_story_text", "apart": True, "slot_max": 2, "cooldown": 4, "chance": 0.5,
            "requires": "story_grade_text_due",
        },
        "inspection": {
            "trigger": "location", "moment": "inspection", "meet": True, "where": APARTMENT_ROOMS,
            "slot_max": 1, "chance": 0.25, "cooldown": 3,
        },
        "mall_errand": {
            "trigger": "location", "moment": "mall_errand", "where": ("mall",), "visit": True,
            "slot_max": 2, "chance": 0.2, "cooldown": 5,
        },
        "wine_check": {
            "trigger": "location", "moment": "wine_check", "meet": True, "where": ("apartment",),
            "slot_min": 2, "chance": 0.15, "cooldown": 4, "requires": "story_husband_out",
        },
        "home_late": {
            "trigger": "downtown_night", "label": "_story_home_late", "chance": 0.15, "cooldown": 6,
        },
        # ── her initiative inside a step (girl-initiated, one restricted scene each) ──
        "her_terms": {
            "trigger": "location", "label": "_story_her_terms", "meet": True, "where": APARTMENT_ROOMS,
            "slot_min": 2, "chance": 0.25, "cooldown": 4, "requires": "story_husband_out",
        },
        "stolen_minutes": {
            "trigger": "location", "label": "_story_stolen_minutes", "meet": True, "where": APARTMENT_ROOMS,
            "slot_min": 1, "chance": 0.2, "cooldown": 3, "requires": "story_husband_next_room",
        },
        "her_appetite": {
            "trigger": "location", "label": "_story_her_appetite", "where": ("room",), "visit": True, "alone": True,
            "slot_min": FEMDOM_TURN_VISIT_SLOT, "chance": 0.2, "cooldown": 3, "leaves": True,
            "knock": _("Three soft knocks, then one hard one. You know that knock."),
        },
        # ── the world almost catches them: his footsteps during a scene in the apartment (steps 2+) ──
        "husband_steps": {
            "trigger": "sex", "moment": "husband_steps", "chance": 0.25, "cooldown": 2,
            "requires": "story_husband_steps_due",
        },
    })

    STORY_STEP_EVENTS["role:stepmom"] = {
        0: ("family_dinner", "grade_summons", "inspection", "mall_errand", "wine_check", "home_late"),
        1: ("family_dinner", "her_night_text", "her_terms", "grade_summons", "mall_treat"),
        2: ("family_dinner", "her_night_text", "distract_father", "short_vent", "husband_calls",
            "stolen_minutes", "husband_steps", "grade_summons", "mall_treat"),
        3: ("family_dinner", "short_vent", "her_night_text", "her_appetite", "husband_steps", "car_ten_minutes"),
        4: ("family_dinner", "short_vent", "her_night_text", "her_appetite", "husband_steps", "car_ten_minutes"),
    }

    # The hints of her unlock (story_unlock_hint): narration, his thoughts after the moment came and nothing happened.
    # "love" = she cares for him, "inbt" = she dares, "obed" = she takes him seriously / obeys, "evidence" = her
    # secret, "blackmail" = what he has on her. Role lines: no name, no job, her husband is his father.
    STORY_HINTS["role:stepmom"] = {
        # after a Sunday dinner (hand_under_table)
        "cold": {
            "love": {
                "far": _("Another dinner, another wall. She treats you like a guest who stayed too long. Maybe if she liked you a little more, next Sunday would go differently."),
                "close": _("For a second tonight, she almost smiled at you. Almost. She's warming up to you... a little more, and the next dinner might not end like this one."),
            },
            "inbt": {
                "far": _("She sat through the whole dinner like a signed contract, every word measured. Maybe if she let her guard down around you, things would change."),
                "close": _("She laughed at something tonight, and her eyes found yours while she did. She's loosening up around you. A little more..."),
            },
            "obed": {
                "far": _("She ran the table like a board meeting, and you were the intern. Maybe if she took you seriously, she'd stop treating you like a boy."),
                "close": _("Tonight she actually waited for you to finish talking. She's starting to take you seriously. Push a little more."),
            },
            "evidence": {
                "far": _("Her phone buzzed twice during dinner, and twice she stepped out to answer it. Whatever she does after she sends you home at night... knowing it might change how she looks at you."),
            },
        },
        # in his bed, on a night her husband is home (vent_night)
        "she_decides": {
            "love": {
                "far": _("Lying in the dark, you think about her. She lets you close now, but only when she decides. Maybe if she cared more, one night she'd come to you."),
                "close": _("You catch yourself listening for a knock that never comes. She's closer than she's ever been. A little more, and one night she might knock."),
            },
            "inbt": {
                "far": _("She plays with you, but she never lets you see her lose control. Maybe if she dared a little more, she wouldn't spend tonight at home."),
                "close": _("Lately she's been bolder, and she knows it. A little more nerve, and she'll stop pretending this is only a game."),
            },
            "obed": {
                "far": _("She still decides everything between you two. Maybe if she listened to you more, she'd come to you instead of making you wait."),
                "close": _("She's started doing what you tell her, and it surprises her more than it surprises you. A little more, and she'll come when you want her."),
            },
            "blackmail": {
                "far": _("You scroll through your phone before you sleep. What you have on her isn't enough to make her come to you. Not yet."),
                "close": _("What you have on her is starting to weigh on her. A little more, and she won't be able to keep you at arm's length."),
            },
        },
        # a morning her husband is away on a trip (marital_bed)
        "giving_in": {
            "love": {
                "far": _("Your father is away, and that apartment is all hers today. Your phone stays quiet. Maybe if she loved you enough to risk it..."),
                "close": _("Your father is away, and part of you expected her to text. She didn't. Not today. But she's close to letting you all the way in."),
            },
            "inbt": {
                "far": _("Your father is out of town, and she doesn't call. There's still one place she won't take you: the bed she shares with him. Maybe if she were bolder..."),
                "close": _("Your father is away. She didn't call, but you can feel it: one more push and she'll stop caring whose bed it is."),
            },
            "obed": {
                "far": _("Your father is out of town, and she's alone in that apartment. She doesn't call you over. She still answers to herself before she answers to you."),
                "close": _("Your father is away. She didn't call, but she obeys you more every day. Soon she'll come when you call her... wherever you want."),
            },
            "blackmail": {
                "far": _("Your father is away, and she knows exactly what's on your phone. It isn't heavy enough yet to pull her across that line. More material would change the math."),
                "close": _("Your father is away. What you hold on her is almost enough to make her open that bedroom herself. One more piece."),
            },
        },
        # a Sunday dinner when the player has a strong drink (drugged_dinner)
        "his": {
            "love": {
                "far": _("Another Sunday dinner. She's yours now, but there's still a wall between you. Something strong enough to knock it down... and knock him out. If she loved you enough."),
                "close": _("She looks at you across the table like she's waiting for you to do something bold. A strong drink in his glass might be all it takes."),
            },
            "inbt": {
                "far": _("Your father drinks his wine, and she watches you over the rim of her glass. She's daring you to push further. Maybe a stronger drink would tip the scales."),
                "close": _("She's ready. You can see it in the way she watches him drink. One strong pour, and the last wall between you comes down."),
            },
            "obed": {
                "far": _("She's yours behind closed doors, but the doors are still closed. Your father sits at the head of the table, oblivious. A strong drink might fix that."),
                "close": _("She obeys you now. All that's left is getting him out of the way. A strong drink in his glass, and the night is yours."),
            },
            "blackmail": {
                "far": _("She watches your pocket more than your plate these days. What you have on her won't carry the last step yet. More footage... and your father would need to be very, very asleep."),
                "close": _("What you hold on her could end her world, and she knows it. One strong drink in his glass tonight, and she won't say no to anything."),
            },
        },
    }

    # Every step is a dict {lane: line} (author, 2026-10-09: "duas rotas distintas... que travam o avanco").
    # Step 0 has no lock yet: the card draws BOTH lanes as blocks, under the lock warning (the screen's own
    # line); from step 1 her lane is locked (story_route_lock) and only its line shows. No spoilers: the
    # night route only says where to look.
    STORY_STATUS_HINTS["role:stepmom"] = {
        "cold": {
            "stats":     _("Raise your stats with her and attend the Sunday dinner."),
            "blackmail": _("Find out where she goes at night after she sends you away."),
            "ready":     _("Everything is in place. Sit through the next Sunday dinner."),
        },
        "she_decides": {
            "stats":     _("Get at least a B on an exam, raise your stats with her, then sleep alone in your room."),
            "blackmail": _("Get at least a B on an exam, then sleep alone in your room. What you hold over her opens her door."),
            "ready":     _("She is ready. Get at least a B on an exam if you haven't, then sleep alone in your room while her husband is home."),
        },
        "giving_in": {
            "stats":     _("Raise your stats with her and wait for a morning when her husband is away."),
            "blackmail": _("Wait for a morning when her husband is away. What you hold on her will do the asking."),
            "ready":     _("She is ready. Wait for a morning when her husband leaves on a trip, and answer her text."),
        },
        "his": {
            "stats":     _("Raise your stats with her and bring a strong drink to the Sunday dinner."),
            "blackmail": _("Bring a strong drink to the Sunday dinner. The bar video alone won't carry this: you need real footage of her too."),
            "ready":     _("Tonight could be the night. Bring a strong drink to the Sunday dinner."),
        },
    }

    # The lines of the step she just reached: gid, else her role -> {step: [(face, line), ...]}. Face None = narration.
    # A "<step>_blackmail" key is the turn said on the COERCION lane (tester 2026-10-11: "You win...
    # I'm yours" read absurd when he cornered her with a camera): bitter arithmetic, never affection.
    STORY_TURN_LINES = {
        "shion": {
            1: [
                (None, _("She studies you for a long moment, the way she studies a contract before she signs it.")),
                ("serious", _("Don't flatter yourself, [Player.Name]. Nothing has changed.")),
                ("smirk", _("But if your hands wander... I might let them. Because I decided to. Not because you earned it.")),
            ],
            "1_blackmail": [
                (None, _("She studies you for a long moment, the way she studies an audit she did not order.")),
                ("serious", _("So that's how you want to play it. Fine. We both know what you saw.")),
                ("normal", _("Nothing here changes out of affection, [Player.Name]. It changes because you hold a camera and I hold a life worth keeping.")),
            ],
            3: [
                ("embarrassed", _("You win, [Player.Name]. Don't make me say it twice.")),
                ("serious", _("In front of your father, nothing changes. I'm still his wife, and you're still my disappointment.")),
                ("sexy", _("Behind his back... I'm yours. And if you ever tell him, I'll deny every word.")),
            ],
            "3_blackmail": [
                ("serious", _("Don't mistake this for winning, [Player.Name]. You didn't win me. You cornered me.")),
                ("normal", _("In front of your father, nothing changes. I'm still his wife. And you are still the boy holding a phone over my life.")),
                ("sexy", _("Behind his back, take what you're taking. ...And one day, when that video is worth nothing, you and I will have a very different conversation.")),
            ],
        },
        "role:stepmom": {
            1: [
                ("normal", _("Don't get any ideas. Nothing has changed.")),
                ("sexy", _("But I might let you touch me. Because I decided it, not because you asked.")),
            ],
            "1_blackmail": [
                ("serious", _("This is not affection. This is arithmetic. Remember that.")),
            ],
            3: [
                ("shy", _("Fine. You win. I'm yours.")),
                ("sexy", _("Don't make me say it twice.")),
            ],
            "3_blackmail": [
                ("serious", _("You didn't win me. You cornered me. There is a difference, and one day you will learn it.")),
            ],
        },
    }

    # ── 0 -> 1: the hand under the table (a Sunday dinner). One version per route; "default" when none passed (QA)
    STORY_SCENES["hand_under_table"] = {
        "role:stepmom": {
            "open": [
                (None, _("Sunday dinner. Your father talks about work, the stock market, the neighbor's dog. She barely touches her plate.")),
                ("@husband", _("Right, honey? Tell him about the gala.")),
                ("normal", _("Your father exaggerates. It was a party with expensive napkins.")),
                (None, _("Her eyes find yours across the table, and stay there a second too long.")),
            ],
            "routes": {
                # she wants him
                "love": [
                    (None, _("Something has changed between you two. She laughs at your jokes now. She asks about your week, and listens to the answer.")),
                    (None, _("Under the table, a hand settles on your knee. Warm. Light. Waiting to see if you pull away.")),
                    (None, _("You don't. You lay your hand over hers.")),
                    ("sexy", _("Your father is right, you know. You've grown up.")),
                    (None, _("Her thumb draws slow circles on your knee while your father talks about mortgage rates.")),
                ],
                # she takes the risk
                "inbt": [
                    (None, _("She's drinking faster than usual tonight. When your father turns to open another bottle, her foot slides up your calf.")),
                    (None, _("Higher. Then her hand, on your thigh, under the tablecloth.")),
                    ("@husband", _("Everything okay, son? You look a little flushed.")),
                    ("smug", _("It's the wine. Pour him another glass, darling. He's a grown man now.")),
                    (None, _("Her hand doesn't move. Not while your father pours. Not while he sits back down.")),
                ],
                # he leads, she follows
                "obed": [
                    (None, _("She has been following your lead lately. Small things. Who pours, who speaks first, who looks away.")),
                    (None, _("Tonight you don't look away. Under the table, you take her wrist and lay her hand on your thigh.")),
                    (None, _("She could pull it back. She doesn't.")),
                    ("normal", _("...Eat your dinner, [Player.Name].")),
                    (None, _("Her hand stays exactly where you put it.")),
                ],
            },
            "default": "love",
            "close": [
                ("@husband", _("I'll get dessert. Don't fight while I'm gone, you two.")),
                (None, _("Her hand stays on your thigh a moment longer. Then it's gone.")),
            ],
        },
    }

    # ── The Sunday dinner (step event "family_dinner"): gid / role -> "open" (variants), "moments", "close" by step.
    # A moment: "steps", "lines", and three "choices" (one per stat): "menu" (his choice), "say" (his line, optional),
    # "pass" / "fail" (what happens; "pass_first" / "fail_first" replace them on her FIRST step: the nerve can pay
    # stats, but she tolerates nothing before her initiative). A test reads half the unlock route of that stat at
    # her step (story_test).
    STORY_DINNERS = {
        "role:stepmom": {
            "open": [
                [(None, _("Sunday dinner at the apartment. Your father carves, talks, and refills every glass but hers. She refills her own."))],
                [(None, _("Sunday dinner. The good plates, the expensive wine, and your father's voice filling every silence."))],
                [(None, _("Dinner with your father and his wife. The candles are lit. Nobody remembers why."))],
            ],
            "moments": [
                {
                    "id": "school", "steps": (0, 1, 2),
                    "lines": [
                        ("@husband", _("So, how's school, son? Keeping those grades up?")),
                        (None, _("She sets her fork down and waits for your answer like it's a quarterly report.")),
                    ],
                    "choices": [
                        {"stat": "Love", "menu": _("Say she's the reason you study harder."),
                         "say": _("Honestly? She's the reason I study harder now."),
                         "pass": [("happy", _("...Flattery. It's working, a little."))],
                         "fail": [("normal", _("Don't thank me. Just don't fail."))]},
                        {"stat": "Obed", "menu": _("Say she'll see your grades when you're ready."),
                         "say": _("You'll see my grades when I'm ready to show them."),
                         "pass": [("smug", _("...Fine. When you're ready. Don't make me wait too long."))],
                         "fail": [("angry", _("You'll show me when I ask. Not a day later."))]},
                        {"stat": "Inbt", "menu": _("Nudge her foot under the table."), "say": None,
                         "pass": [(None, _("She doesn't move her foot away. She doesn't look at you either.")),
                                  ("smug", _("Your father asked you a question, [Player.Name]."))],
                         # her first step: the nerve registers, the foot does not stay
                         "pass_first": [(None, _("Her fork stops halfway. She removes your foot with one precise push of her heel.")),
                                        ("serious", _("Your father asked you a question, [Player.Name]. Answer him."))],
                         "fail": [(None, _("She moves her foot and gives you a look that could freeze the wine."))]},
                    ],
                },
                {
                    "id": "wine", "steps": (0, 1, 2),
                    "lines": [
                        (None, _("Your father tells the same story about his boss for the third time. She refills her glass and stares at the bottom of it.")),
                    ],
                    "choices": [
                        {"stat": "Love", "menu": _("Ask her about her week."),
                         "say": _("How was your week? You never say."),
                         "pass": [("surprised", _("Nobody asks me that.")),
                                  ("happy", _("...Long. It was long. Thank you for asking."))],
                         "fail": [("normal", _("My week is none of your concern."))]},
                        {"stat": "Obed", "menu": _("Take the bottle and pour for her."),
                         "say": _("Sit back. I'll pour."),
                         "pass": [("smug", _("...Go on, then. Not too much."))],
                         "fail": [("angry", _("Nobody pours my wine in my own house."))]},
                        {"stat": "Inbt", "menu": _("Hold her eyes over your glass a little too long."), "say": None,
                         "pass": [(None, _("She holds your look until your father turns back to the table."))],
                         # her first step: a staring contest is a meeting she wins
                         "pass_first": [(None, _("She stares back the way she must stare down a boardroom, one eyebrow up, until you blink first.")),
                                        ("normal", _("Drink your wine, boy."))],
                         "fail": [("normal", _("Eyes on your plate, [Player.Name]."))]},
                    ],
                },
                {
                    "id": "dishes", "steps": (0, 1, 2),
                    "lines": [
                        ("@husband", _("Help %s with the plates, will you, son? The game's about to start.")),
                        (None, _("The kitchen is small. She hands you a plate without looking at you.")),
                    ],
                    "choices": [
                        {"stat": "Love", "menu": _("Tell her this was the best part of your week."),
                         "say": _("This was the best part of my week."),
                         "pass": [("shy", _("...Go, before I say something nice back."))],
                         "fail": [("normal", _("It was just dinner. Don't be dramatic."))]},
                        {"stat": "Obed", "menu": _("Tell her to leave the dishes to you."),
                         "say": _("Leave them. I've got this."),
                         "pass": [("normal", _("...Fine. Don't break anything."))],
                         "fail": [("angry", _("In my kitchen, I give the orders."))]},
                        {"stat": "Inbt", "menu": _("Stand right behind her at the sink."), "say": None,
                         "pass": [(None, _("She doesn't step away. For a moment you can feel her breathing.")),
                                  ("sexy", _("...Your father is twenty feet away."))],
                         # her first step: she makes the space hers again, coldly
                         "pass_first": [(None, _("She goes still for half a second. Then she plants a dripping plate flat against your chest.")),
                                        ("serious", _("Towel. Dry. Two steps back while you do it."))],
                         "fail": [(None, _("She elbows you back a step without even turning around."))]},
                    ],
                },
                {
                    "id": "drink_hint", "steps": (3, 4),
                    "lines": [
                        ("@husband", _("You know what I could go for? A real whiskey. The kind that burns going down.")),
                        (None, _("He swirls his wine and stares at it like it insulted him.")),
                        ("@husband", _("This is fine, but it's not the same. Nothing beats a good, strong drink.")),
                    ],
                    "choices": [
                        {"stat": "Love", "menu": _("Tell him you'll get one for next time."),
                         "say": _("I'll bring you something strong next time. Promise."),
                         "pass": [("@husband", _("Ha! I like that. See, honey? The kid gets it."))],
                         "fail": [("@husband", _("I'll believe it when I see it."))]},
                        {"stat": "Obed", "menu": _("Say he deserves the good stuff."),
                         "say": _("A man like you deserves better than wine."),
                         "pass": [("@husband", _("Damn right! See? This one has taste."))],
                         "fail": [("@husband", _("Don't butter me up, son."))]},
                        {"stat": "Inbt", "menu": _("Glance at her while he talks about drinks."), "say": None,
                         "pass": [(None, _("She catches your look and holds it. Something in her eyes tells you she's thinking the same thing you are."))],
                         "fail": [(None, _("She doesn't notice. She's busy refilling her own glass."))]},
                    ],
                },
                {
                    "id": "toast", "steps": (3, 4),
                    "lines": [
                        ("@husband", _("A toast! To family. To the two people I love most in the world.")),
                        (None, _("She raises her glass and looks straight at you while she drinks.")),
                    ],
                    "choices": [
                        {"stat": "Love", "menu": _("Raise your glass to her."), "say": _("To family."),
                         "pass": [("happy", _("...To family."))],
                         "fail": [("normal", _("To family."))]},
                        {"stat": "Obed", "menu": _("Refill her glass before your father can."), "say": None,
                         "pass": [("smug", _("Thank you, [Player.Name]. Your father could learn a thing or two."))],
                         "fail": [("normal", _("...Thank you."))]},
                        {"stat": "Inbt", "menu": _("Slide your foot up her leg during the toast."), "say": None,
                         "pass": [(None, _("She doesn't even blink. She just drinks, slowly, and lets you."))],
                         "fail": [(None, _("She kicks your ankle under the table."))]},
                    ],
                },
            ],
            "dad_exit": [
                _("I'll get the dessert. Don't go anywhere, you two."),
                _("Let me grab something from the kitchen. Be right back."),
            ],
            "close": {
                0: [("normal", _("If he can find the time."))],
                1: [(None, _("She sets her glass down and looks at you, longer than she needs to.")),
                    ("normal", _("You're getting better at these. The dinners, I mean."))],
                2: [(None, _("She straightens your collar. Her fingers linger.")),
                    ("sexy", _("Next Sunday. Don't make me wait."))],
                3: [(None, _("She presses her hand flat against your chest.")),
                    ("sexy", _("Next week. And every week after that."))],
                4: [(None, _("She brushes her lips past your ear as she clears the plates.")),
                    ("sexy", _("Bring something strong next time. For him."))],
            },
            "dad_return": [
                _("Your father comes back with three plates of something expensive. He sets yours down first."),
                _("Your father returns balancing a tray. The dessert is too pretty to eat, but he's already digging in."),
            ],
            "dessert": {
                0: [(None, _("Dessert passes in silence. She eats like she's reading a contract.")),
                    ("@husband", _("Same time next week, son. Right, honey?")),
                    ("normal", _("We'll see."))],
                1: [(None, _("Dessert is quiet. Once, her spoon taps your plate by accident. She doesn't apologize.")),
                    ("@husband", _("Same time next week, son!")),
                    ("smug", _("Same time."))],
                2: [(None, _("Dessert is slow. She watches you eat the way people watch fire.")),
                    ("@husband", _("Same time next week! I love these Sundays.")),
                    ("normal", _("So do I."))],
                3: [(None, _("Dessert is warm. She laughs at something your father says, and her eyes find yours while she does.")),
                    ("@husband", _("Same time next week, son!")),
                    ("happy", _("He'll be here. Won't you, [Player.Name]?"))],
                4: [(None, _("Dessert is familiar. She eats slowly, watching the two of you with a look you can't quite read.")),
                    ("@husband", _("Same time next week, son!")),
                    ("sexy", _("Of course. We wouldn't miss it."))],
            },
        },
    }

    # ── 2 -> 3: the marital bed (a morning her husband is away: trigger "morning"). She texts, he comes home
    STORY_SCENES["marital_bed"] = {
        "role:stepmom": {
            "open": [
                (None, _("She opens the door in a silk robe and doesn't say a word. She just takes your hand and leads you down the hall.")),
                (None, _("Their bedroom. His side of the bed is still unmade. On the nightstand, a framed photo from their wedding.")),
            ],
            "routes": {
                # she wants him
                "love": [
                    ("shy", _("I'm tired of stolen hours in your dorm. I want you here. In my life. In my bed.")),
                    (None, _("She turns the wedding photo face down without looking at it.")),
                    ("sexy", _("Just once, I want to wake up next to someone who actually sees me.")),
                ],
                # she takes the risk
                "inbt": [
                    (None, _("She picks up the wedding photo, looks at it for a long second, and sets it back down facing the bed.")),
                    ("smug", _("Let him watch. Nothing worth watching has happened in this bed in a long time.")),
                    ("sexy", _("I've wanted to do this since the day I moved in.")),
                ],
                # he leads, she follows
                "obed": [
                    ("shy", _("I kept telling myself: anywhere but here. Not in his bed.")),
                    ("normal", _("...Then tell me where.")),
                    (None, _("You point at the bed. She slips off her robe and lies down on his side.")),
                ],
                # the price of his silence: she brings him to the one bed he can't demand, and keeps the frame
                "blackmail": [
                    (None, _("She stops at the foot of the bed and finally looks at you. Not at your eyes. At the pocket where you keep your phone.")),
                    ("serious", _("So this is what it costs. Fine. But listen carefully: you get what I give you, the way I give it.")),
                    ("smug", _("And when you're done congratulating yourself, remember who chose the room.")),
                ],
            },
            "default": "love",
        },
    }

    # Her texts that morning, his answer, the scene by route, the end (label _story_marital_bed). "declined" = her
    # texts when he can't come (she stays on her step: story_unlock_cancel, the event's cooldown)
    STORY_MARITAL = {
        "role:stepmom": {
            "texts": [
                _("Your father left for his trip at six."),
                _("The apartment is empty."),
                _("Come home. Now."),
            ],
            "declined": [
                _("...Fine."),
                _("He's back in a few days. Be free the next time he leaves."),
            ],
            "acts": {
                "love": ("sex", "cowgirl"),
                "inbt": ("sex", "reverse_cowgirl"),
                "obed": ("sex", "doggy"),
                "blackmail": ("sex", "doggy"),      # impersonal: she won't face him for this one
            },
            "default": "love",
            "no_condom": [
                ("normal", _("No condom? ...Then lie back. I'll use my mouth.")),
            ],
            "no_condom_act": ("bj", None),
            "after": [
                (None, _("Afterwards, she lies on his pillow and laughs, quietly, at nothing.")),
                ("sexy", _("I'm changing these sheets before he gets home. ...Maybe.")),
            ],
        },
    }

    # ── Step-1 moment (plan_shion_agency F2): the mall, her ten minutes, three ways to take a coffee ──
    STORY_MOMENTS["mall_treat"] = {
        "role:stepmom": {
            "lines": [
                (None, _("You run into her at the mall, two bags already hanging from her arm. She hands them to you without asking.")),
                ("normal", _("Good timing. Walk with me.")),
                (None, _("At the counter she pays for her things, then nods at the espresso bar and orders two cups without asking you either.")),
                ("smug", _("Sit. You have ten minutes of my afternoon.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Ask how her week actually went."), "say": None,
                 "pass": [("normal", _("...Long. Expensive. Full of men who talk too much.")),
                          (None, _("She stirs her coffee, and for one second the boardroom face slips.")),
                          ("normal", _("Thank you for asking. Nobody does."))],
                 "fail": [("normal", _("We are not there yet. Drink your coffee."))]},
                {"stat": "Obed", "menu": _("Wait quietly until she puts the phone down."), "say": None,
                 "pass": [("smug", _("Look at that. A boy who knows how to wait.")),
                          (None, _("She puts the phone away sooner than she meant to."))],
                 "fail": [("normal", _("Patience looks forced on you. Work on it."))]},
                {"stat": "Inbt", "menu": _("Tease her about spoiling you."),
                 "say": _("Careful. People will think you're spoiling me."),
                 "pass": [("smirk", _("Let them think. They would be wrong, and you would be carrying bags either way."))],
                 "fail": [("serious", _("They would think you talk too much. Carry the bags."))]},
            ],
            "after": [
                (None, _("Ten minutes later she stands, takes her bags back, and leaves you with the bill for the coffees.")),
                ("smug", _("Same time next week, maybe. If you behave.")),
            ],
        },
    }

    # ── Step 3-4 moment (plan_shion_agency F2): the black car at the campus curb, ten minutes, no sprite
    #    (face "": she stays behind the tinted glass, like the hashimoto nights) ──
    STORY_MOMENTS["car_ten_minutes"] = {
        "role:stepmom": {
            "lines": [
                (None, _("A black car idles at the campus curb with the engine running. The rear window rolls down two fingers.")),
                ("", _("Get in. Ten minutes.")),
                (None, _("Inside it smells like leather and her perfume. The driver is nowhere to be seen.")),
                ("", _("Phone on silent. Those are the rules of this car.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Ask her what's wrong."), "say": None,
                 "pass": [("", _("Nothing is wrong. I had ten free minutes and I chose this. Don't make it bigger than it is.")),
                          (None, _("Her hand finds yours anyway, and stays."))],
                 "fail": [("", _("If something were wrong, you would never hear it from me in a parking lot."))]},
                {"stat": "Obed", "menu": _("Sit still and let her decide the ten minutes."), "say": None,
                 "pass": [(None, _("She takes her time. When she finally leans over, it costs the whole ten minutes and change.")),
                          ("", _("Good boy. Out you go."))],
                 "fail": [("", _("You fidget like a freshman. Out. We'll try again when you can sit still."))]},
                {"stat": "Inbt", "menu": _("Remark on what the tinted windows are for."),
                 "say": _("So this is what the quiet windows are for."),
                 "pass": [("", _("These windows have seen board members cry. They can keep one more secret.")),
                          (None, _("The ten minutes do not involve much talking after that."))],
                 "fail": [("", _("This car is for ten quiet minutes. You just spent two of them on a joke."))]},
            ],
            "after": [
                (None, _("At minute ten exactly, the lock clicks open. Whatever happened in there stays in the leather.")),
                ("", _("Walk away first. I'll wait.")),
            ],
        },
    }

    # ── Step-2 moments (STORY_MOMENTS): lines, three choices one per stat, "after"
    STORY_MOMENTS["distract_father"] = {
        "role:stepmom": {
            "lines": [
                (None, _("Your father is home, glued to the game in the living room. She finds you in the kitchen and stands a little too close.")),
                ("smug", _("He'll be in front of that TV for two hours. Maybe three.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Kiss her, quick and quiet."), "say": None,
                 "pass": [(None, _("She kisses you back, one hand on your chest, listening for the couch.")),
                          ("shy", _("...Go back out there before he wonders."))],
                 "fail": [("normal", _("Not with him in the next room. Are you insane?"))]},
                {"stat": "Obed", "menu": _("Tell her to send him out for something."),
                 "say": _("Send him to the store. Now."),
                 "pass": [(None, _("She walks into the living room. A minute later, the front door closes behind your father.")),
                          ("sexy", _("Twenty minutes. Don't waste them.")),
                          (None, _("You don't. When his car pulls back in, she's fixing her hair in the hallway mirror."))],
                 "fail": [("angry", _("You don't give orders in this house."))]},
                {"stat": "Inbt", "menu": _("Pull her into the pantry."), "say": None,
                 "pass": [(None, _("She lets you. In the dark, her breathing is the loudest thing in the apartment.")),
                          ("@husband", _("%s? Have you seen the remote?")),
                          ("normal", _("Under the cushion, darling!")),
                          (None, _("She doesn't move until his footsteps fade."))],
                 "fail": [(None, _("She slips out of your grip and goes back to the living room without a word."))]},
            ],
        },
    }
    STORY_MOMENTS["short_vent"] = {
        "role:stepmom": {
            "lines": [
                ("sad", _("Ten minutes. I just need ten minutes away from that apartment.")),
                (None, _("She drops onto your bed and stares at your ceiling.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Lie down next to her and listen."), "say": None,
                 "pass": [(None, _("She talks about nothing for a while. Then she goes quiet, her head on your shoulder.")),
                          ("shy", _("...This is the only quiet place I have left."))],
                 "fail": [("normal", _("Don't. I didn't come here to be comforted."))]},
                {"stat": "Obed", "menu": _("Tell her to tell you what happened."), "say": _("Tell me what he did."),
                 "pass": [("sad", _("He forgot. Again. Something small. It's always something small.")),
                          ("normal", _("...Thank you for asking like you actually want to know."))],
                 "fail": [("angry", _("I don't need to be interviewed."))]},
                {"stat": "Inbt", "menu": _("Lock the door."), "say": None,
                 "pass": [(None, _("She hears the lock click and doesn't get up.")),
                          ("sexy", _("Ten minutes, I said. ...Make it twenty."))],
                 "fail": [("normal", _("Unlock it. I'm not staying."))]},
            ],
            "after": [
                (None, _("She leaves before the hallway fills up with students.")),
            ],
        },
    }
    STORY_MOMENTS["husband_calls"] = {
        "role:stepmom": {
            "lines": [
                (None, _("Her phone lights up on the nightstand. Your father's name is on the screen.")),
                ("surprised", _("...It's him.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Stop and let her take it."), "say": None,
                 "pass": [(None, _("She answers, says three calm sentences about a late meeting, and hangs up.")),
                          ("shy", _("...Thank you for stopping."))],
                 "fail": [(None, _("She lets it ring out, rattled.")),
                          ("normal", _("Just... give me a second."))]},
                {"stat": "Obed", "menu": _("Tell her to ignore it."), "say": _("Ignore it."),
                 "pass": [(None, _("She turns the phone face down without a word.")),
                          ("smug", _("...He can wait."))],
                 "fail": [("angry", _("Don't tell me what to do with my husband's calls."))]},
                {"stat": "Inbt", "menu": _("Keep going while it rings."), "say": None,
                 "pass": [(None, _("It rings. And rings. She bites her lip and doesn't make a sound until it stops."))],
                 "fail": [("angry", _("Stop! ...Stop. Just until it stops ringing."))]},
            ],
        },
    }

    # ── Step-0 moments: the cold investor. No warmth, no promise; a pass is a crack, never a smile ──
    STORY_MOMENTS["inspection"] = {
        "role:stepmom": {
            "lines": [
                (None, _("She stops you in the hallway with one look, the way she must stop meetings.")),
                ("normal", _("Stand still.")),
                (None, _("She looks you over, collar to shoes, and finds everything wanting.")),
                ("normal", _("Wrinkled shirt. Yesterday's hair. You go out in public looking like that?")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Fix your collar and thank her for noticing."),
                 "say": _("You're right. Thanks for noticing."),
                 "pass": [("surprised", _("...You're welcome. That's new."))],
                 "fail": [("normal", _("Don't thank me. Just look presentable."))]},
                {"stat": "Obed", "menu": _("Stand straight and let her fix it."), "say": None,
                 "pass": [(None, _("She straightens your collar with two sharp tugs, like she's done it a thousand times for someone else.")),
                          ("normal", _("There. Now you look like someone who lives here."))],
                 "fail": [("angry", _("I'm not your maid. Fix it yourself."))]},
                {"stat": "Inbt", "menu": _("Ask if she inspects everyone this closely."),
                 "say": _("Do you look at everyone this closely?"),
                 "pass": [("smug", _("Only what's under my roof. Everything under my roof gets inspected."))],
                 "fail": [("angry", _("Watch the tone. This is my house."))]},
            ],
        },
    }
    STORY_MOMENTS["mall_errand"] = {
        "role:stepmom": {
            "lines": [
                (None, _("She steps out of a boutique with four bags and spots you before you can pretend you didn't see her.")),
                ("normal", _("You. Good timing. Hold these.")),
                (None, _("She hands you the bags without waiting for an answer and starts walking.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Carry them and keep up with her."), "say": None,
                 "pass": [(None, _("You walk beside her for three stores. She doesn't say much, but she slows her step so you can keep up.")),
                          ("normal", _("...You're more useful than you look. Lunch is on me. Eat fast."))],
                 "fail": [("normal", _("Keep up or hand them back. I don't wait."))]},
                {"stat": "Obed", "menu": _("Hold the bags out and make her take one back."),
                 "say": _("I'm not your porter. Take one."),
                 "pass": [("surprised", _("...")),
                          (None, _("She takes one bag back. She doesn't mention it, but she watches you differently for the rest of the walk."))],
                 "fail": [("angry", _("You'll carry all of them now. That's how that works."))]},
                {"stat": "Inbt", "menu": _("Ask what's in the pink bag."),
                 "say": _("What's in the pink one?"),
                 "pass": [("smug", _("None of your business. ...It's for a gala. Eyes forward.")),
                          (None, _("She almost smiled. Almost."))],
                 "fail": [("angry", _("One more question like that and you'll carry these to the car. The far one."))]},
            ],
        },
    }
    STORY_MOMENTS["wine_check"] = {
        "role:stepmom": {
            "lines": [
                (None, _("You find her in the living room with a ledger and the wine cabinet open.")),
                ("normal", _("Before you ask: yes, I count them. Every week.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Offer to read her the labels."),
                 "say": _("Want a hand with the list?"),
                 "pass": [("surprised", _("...Fine. Read me the labels. Don't drop anything.")),
                          (None, _("Ten minutes of labels and vintages. She corrects your pronunciation twice, and almost enjoys it."))],
                 "fail": [("normal", _("Touch nothing. Watch if you must."))]},
                {"stat": "Obed", "menu": _("Tell her the bottles should lie on their sides."),
                 "say": _("They should be on their sides. The corks dry out."),
                 "pass": [("surprised", _("...He knows about corks.")),
                          ("normal", _("Fine. You rearrange, I count. Carefully."))],
                 "fail": [("angry", _("And YOU learned wine where, exactly? Hands off."))]},
                {"stat": "Inbt", "menu": _("Pour yourself a glass while she watches."), "say": None,
                 "pass": [(None, _("You pour two fingers and hold her stare. She lets you finish it.")),
                          ("smug", _("That one was the cheap shelf, boy. But the nerve was almost expensive."))],
                 "fail": [("angry", _("Put it DOWN. That bottle is worth more than your semester."))]},
            ],
        },
    }
    # On his way to the late bus (trigger "downtown_night"): a black car drops her off. Her voice has no face ("")
    STORY_MOMENTS["home_late"] = {
        "role:stepmom": {
            "lines": [
                (None, _("While you wait for the late bus, a black car with tinted windows stops in front of the building.")),
                (None, _("She steps out. Heels, dark coat, phone to her ear. She ends the call the moment she sees you.")),
                ("", _("...You're still here.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Say the bus is late. Nothing more."),
                 "say": _("Bus is late. That's all."),
                 "pass": [("", _("Hm.")),
                          (None, _("She holds your eyes a second longer than she needs to, then walks past you to the door.")),
                          ("", _("Get home safe."))],
                 "fail": [("", _("Then wait quietly."))]},
                {"stat": "Obed", "menu": _("Note that it's late for a work meeting."),
                 "say": _("Long meeting. At midnight."),
                 "pass": [("", _("The ones that matter end late.")),
                          (None, _("She says it like a closed door. But she noticed that you noticed."))],
                 "fail": [("", _("My hours are not your concern."))]},
                {"stat": "Inbt", "menu": _("Ask whose car that was."),
                 "say": _("Whose car is that?"),
                 "pass": [("", _("A driver's. Good night, [Player.Name].")),
                          (None, _("At the door she stops, back to you, for exactly one breath. Then she's gone."))],
                 "fail": [("", _("Curiosity is expensive in this family. Go home."))]},
            ],
        },
    }
    # Steps 2+: his footsteps in the hallway during a scene in the apartment (trigger "sex", husband next room)
    STORY_MOMENTS["husband_steps"] = {
        "role:stepmom": {
            "lines": [
                (None, _("Footsteps in the hallway. Slow, heavy, getting closer.")),
                ("surprised", _("...He's up. Don't. Move.")),
            ],
            "choices": [
                {"stat": "Love", "menu": _("Freeze and hold her until they pass."), "say": None,
                 "pass": [(None, _("You hold still, her heartbeat loud against your chest, until the steps fade toward the kitchen.")),
                          ("shy", _("...Okay. Okay. Where were we."))],
                 "fail": [("normal", _("Off. OFF. ...False alarm. God."))]},
                {"stat": "Obed", "menu": _("Put your hand over her mouth and keep going slowly."), "say": None,
                 "pass": [(None, _("Her eyes go wide over your fingers. The footsteps stop, then shuffle back the way they came.")),
                          ("sexy", _("You are insane. ...Don't stop."))],
                 "fail": [("angry", _("Have you lost your mind?! Not. Another. Move."))]},
                {"stat": "Inbt", "menu": _("Don't even slow down."), "say": None,
                 "pass": [(None, _("She buries her face in the pillow. The steps pause outside the door for one endless second, then move on.")),
                          ("sexy", _("I hate you. I hate you. Keep going."))],
                 "fail": [(None, _("She goes rigid until the hallway is silent again, then glares at you like you lit the curtains on fire."))]},
            ],
        },
    }

    # ── Her initiative inside a step (labels _story_her_terms / _story_stolen_minutes / _story_her_appetite):
    # "open" lines, one line per route of HER CURRENT step (story_step_route), the act, the end ──
    STORY_HER_TERMS = {
        "role:stepmom": {
            "open": [
                (None, _("She closes the ledger she wasn't reading and looks at you for a long moment.")),
                ("sexy", _("Sit down, [Player.Name]. Hands on your knees.")),
                ("smug", _("Tonight happens the way I say it happens. Nod if you understand.")),
            ],
            "routes": {
                "love": [("sexy", _("Come here. I've been thinking about this all day, and I HATE thinking about you all day."))],
                "inbt": [("smug", _("You get to watch. That's all. One wrong move and this never happens again."))],
                "obed": [("normal", _("...Fine. Tell me what you want tonight. Within reason, boy."))],
                "evidence": [("normal", _("You keep your phone in your pocket and your mouth shut. Those are the terms. Sit."))],
            },
            "acts": {
                "love": ("hj", None), "obed": ("hj", None),
                "inbt": ("masturbate", None), "evidence": ("masturbate", None),
            },
            "default": "love",
            "after": [
                (None, _("Afterwards she fixes her hair in the hallway mirror like nothing happened.")),
                ("normal", _("Not a word about this. To anyone. ...Goodnight, [Player.Name].")),
            ],
        },
    }
    STORY_STOLEN = {
        "role:stepmom": {
            "open": [
                (None, _("She catches your wrist in the hallway. In the living room, the game is loud and your father is louder.")),
                ("sexy", _("Four minutes. He never leaves the couch before the second half.")),
                (None, _("She pulls you into the kitchen, out of the doorway's line of sight.")),
                ("smug", _("Quiet. If you make a sound, I will end you.")),
            ],
            "after": [
                (None, _("She's back at the counter rinsing a glass before the commercial break ends.")),
                ("normal", _("Four minutes. I told you. ...Wipe that look off your face before you walk out there.")),
            ],
        },
    }
    STORY_APPETITE = {
        "role:stepmom": {
            "open": [
                (None, _("She walks in past you without a word, already pulling off her coat.")),
                ("sexy", _("Don't talk. Tonight I'm not here to talk.")),
            ],
            "routes": {
                "love": [("sexy", _("I missed you. Say it back or don't, I'll have you either way."))],
                "inbt": [("smug", _("Your father thinks I'm at a work dinner. Dessert is in your bed, apparently."))],
                "obed": [("normal", _("Tell me how you want me. You've earned the right to answer that."))],
            },
            # (kind, position, anal): the inbt route is the reckless one
            "acts": {
                "love": ("sex", "cowgirl", False),
                "inbt": ("sex", "doggy", True),
                "obed": ("sex", "doggy", False),
            },
            "default": "love",
            "no_condom": [
                ("normal", _("No condom, no sex. My rules haven't changed. ...Sit down, I'll handle you another way.")),
            ],
            "no_condom_act": ("bj", None),
            "after": [
                (None, _("She dresses with the efficiency of someone catching a flight.")),
                ("sexy", _("I was never here. ...Same time next week, maybe. If you behave.")),
            ],
        },
    }

    def story_dinner_moment(girl):
        """A moment of her step for this dinner, never the one of the last dinner when another one fits."""
        _st = story_step(girl)
        _ms = [_m for _m in story_data(STORY_DINNERS, girl, {}).get("moments", ()) if _st in _m.get("steps", ())]
        _last = getattr(girl, "_story_last_dinner", None)
        _fresh = [_m for _m in _ms if _m["id"] != _last] or _ms
        return renpy.random.choice(_fresh) if _fresh else None

    # ── 1 -> 2: the night she runs to his dorm (he goes to bed: trigger "sleep"). One version per route
    STORY_SCENES["vent_night"] = {
        "role:stepmom": {
            "open": [
                (None, _("When you open the door, she's standing in the hallway. Her makeup is ruined, and she's wearing her coat over her pajamas.")),
                # how a grown woman walks into a student dorm at night (tester 2026-10-10): money did
                (None, _("Nobody stopped her downstairs. The night porter waved her through without a word. Her name sits near the top of the campus donor wall, and he knows it.")),
                ("sad", _("I had a fight with your father. I couldn't stay in that apartment one more minute.")),
                (None, _("She walks past you and sits on the edge of your bed like it's the only place left in the city.")),
            ],
            "routes": {
                # she wants him
                "love": [
                    ("sad", _("He talks over me. He always has. You're the only one in that family who listens.")),
                    (None, _("She talks for an hour. About him, about work, about living with a man who never really looks at her.")),
                    ("shy", _("...Why am I telling you this? You, of all people.")),
                    (None, _("When she finally looks up at you, she doesn't look away.")),
                    ("sexy", _("Come here. Don't say anything. Just come here.")),
                ],
                # she takes the risk
                "inbt": [
                    (None, _("She smells of wine. A lot of wine. Outside, a cab is pulling away.")),
                    ("smug", _("Don't look at me like that. I had two glasses. Maybe four.")),
                    ("sexy", _("Do you know what I thought on the way here? That this is the worst idea I've ever had.")),
                    (None, _("She laughs, and reaches for your belt.")),
                    ("sexy", _("And I don't care.")),
                ],
                # he leads, she follows
                "obed": [
                    (None, _("She doesn't explain why she came here instead of anywhere else. She just waits, like she's waiting for you to tell her what happens now.")),
                    ("sad", _("Tell me what to do. I'm so tired of being the one who decides.")),
                    (None, _("You close the door behind her and tell her to take off her coat. She does.")),
                    ("shy", _("...Like that?")),
                ],
                # his videos of her
                "blackmail": [
                    (None, _("But that's not why she's here. She came for something else.")),
                    ("normal", _("Those videos of me. Your father can never see them. Not now. Not after tonight.")),
                    # SHE sets the terms (tester 2026-10-12, his draft: she asked him to name a cost and then decided
                    # without waiting, which is not the woman this scene builds). No promise the game can't keep:
                    # the video stays, and she turns his leverage into a game she runs.
                    ("serious", _("We haven't made arrangements for your silence yet. Your grades say you have a brain. Prove it. Listen closely, boy.")),
                    ("normal", _("You keep your little video. Keep it safe. We both know it never really goes away. As long as it stays between us, you've shown me you're worth something.")),
                    ("angry", _("If your father ever sees it, I'll have your balls on my desk within the hour. Nobody would find the rest of you. I won't repeat that.")),
                    ("smug", _("I'm not a monster. We can even make a game of it. You pretend you have something on me, and I play the scared little victim who'd do anything to keep her secret.")),
                    ("sexy", _("Just remember it's a game, boy. You get exactly what I choose to give you. Tonight, I choose this.")),
                    (None, _("She's already unbuttoning her coat.")),
                ],
            },
            "default": "love",
        },
    }

    # What happens next, by route (label _story_vent_night): "acts" = (act, position) of the scene,
    # "after" = the end of the night, "declined" = he sent her home
    STORY_VENT = {
        "role:stepmom": {
            "acts": {
                "love": ("hj", None),                   # she reaches for him, on her terms
                "inbt": ("hj", None),                   # reckless, a hand under the covers
                "obed": ("hj", None),                   # he guides her hand
                "blackmail": ("hj", None),               # the price of his silence
            },
            "default": "love",
            "after": [
                (None, _("Afterwards, she sits on the edge of the bed for a long time, staring at the wall.")),
                ("normal", _("Your father wakes up at six. I have to be in that bed when he does.")),
                (None, _("She fixes her coat in the dark. At the door, she stops without turning around.")),
                ("sexy", _("This never happened. ...Until next time.")),
            ],
            # he sent her home: she never admits a mistake. The no becomes HER decision (the author, 2026-10-12)
            "declined": [
                ("smug", _("Heh. I enjoyed that more than I should have. Maybe I'll use you as my little toy now and then. Don't get excited, boy. I still call the shots here.")),
                (None, _("She buttons her coat and leaves without looking back.")),
            ],
        },
    }

    # ── Her texts at night (step event "her_night_text"): gid / role -> "chats": her messages ("her"), and three
    # replies of his, one per stat ("reply", her "pass" / "fail" answer). Her texts never claim what did not happen,
    # and SHE never types anything a divorce lawyer could read aloud (the author 2026-10-11, tester "sexts
    # incriminating"): coded, deniable, deletes threads, refuses photos (no_photos). His replies can be reckless.

    # The narration row that closes a night-text thread left hanging (label _story_text): the talk went
    # on, only not worth transcribing (author 2026-10-11, "the player felt lost"). A ROLE voice: it
    # describes the stepmom persona (she wins every exchange), never one girl.
    _STORY_TEXT_CLOSE = [
        _("The two of you keep texting for a while. She finds a way to come out on top of every single exchange."),
        _("The conversation drifts on longer than either of you would admit. Somehow she always gets the last word."),
        _("You trade messages until your eyes get heavy. Win or lose, she types like she has already won."),
    ]

    STORY_TEXTS = {
        "role:stepmom": {
            "chats": [
                {
                    "id": "awake", "steps": (1, 2),
                    "her": [_("Can't sleep."), _("Are you awake?")],
                    "choices": [
                        {"stat": "Love", "reply": _("I'm awake. Want to talk?"),
                         "pass": [_("...Yes. Just for a minute."), _("Tell me something about your day. Anything.")],
                         "fail": [_("Never mind. Go to sleep.")]},
                        {"stat": "Obed", "reply": _("Go to sleep. Text me tomorrow."),
                         "pass": [_("...Fine. Goodnight, then."), _("You're bossy tonight. I don't hate it.")],
                         "fail": [_("Don't tell me what to do.")]},
                        {"stat": "Inbt", "reply": _("Come over."),
                         "pass": [_("...I'm deleting this conversation."), _("That wasn't a no. Goodnight.")],
                         "fail": [_("Absolutely not. Goodnight.")]},
                    ],
                },
                {
                    "id": "dress", "steps": (1, 2),
                    "her": [_("Gala next week. Black or red?")],
                    "choices": [
                        {"stat": "Love", "reply": _("Red. You'd look incredible."),
                         "pass": [_("Red it is. ...Thank you.")],
                         "fail": [_("Hmm. Black, then.")]},
                        {"stat": "Obed", "reply": _("Black. Wear the black one."),
                         "pass": [_("...Black. Fine. Because you said so.")],
                         "fail": [_("I didn't ask for orders.")]},
                        {"stat": "Inbt", "reply": _("Whichever comes off easier."),
                         "pass": [_("You're terrible. ...The red one.")],
                         "fail": [_("Watch your mouth.")]},
                    ],
                },
                {
                    "id": "other_night", "steps": (2,),
                    "her": [_("I keep thinking about the other night.")],
                    "choices": [
                        {"stat": "Love", "reply": _("Me too. I can't stop."),
                         "pass": [_("Good. ...I mean it. Good.")],
                         "fail": [_("Forget I said that.")]},
                        {"stat": "Obed", "reply": _("Then come back. Soon."),
                         "pass": [_("...Maybe I will.")],
                         "fail": [_("You don't get to summon me.")]},
                        {"stat": "Inbt", "reply": _("Tell me what you're thinking about."),
                         "pass": [_("You know exactly what. I'm not typing it.")],
                         "fail": [_("Not over text. Are you insane?")]},
                    ],
                },
                # the grade summons (event "grade_summons" only): dry, cold, repeatable while his grade stays bad
                {
                    "id": "grades", "steps": (0, 1, 2), "only_event": "grade_summons",
                    "her": [_("Your last exam is on my desk."), _("Explain to me why I shouldn't show your father.")],
                    "choices": [
                        {"stat": "Love", "reply": _("I'll do better. I mean that."),
                         "pass": [_("Words. I collect better ones from lawyers every week."), _("...But fine. Prove it.")],
                         "fail": [_("I've heard that one before. From better students.")]},
                        {"stat": "Obed", "reply": _("I'm already studying. You'll see it on the next exam."),
                         "pass": [_("Good. I won't remind you again."), _("The next exam, then. I keep receipts.")],
                         "fail": [_("Don't promise me schedules. Deliver.")]},
                        {"stat": "Inbt", "reply": _("Then show him. I'm not afraid of you."),
                         "pass": [_("...Bold. Stupid, but bold."), _("Keep that nerve. You'll need it in my house.")],
                         "fail": [_("Careful, boy. You have no idea who you're baiting.")]},
                    ],
                },
                # step 3: the woman who owns him checks on her property
                {
                    "id": "mine", "steps": (3,), "not_trait": "submissive",
                    "her": [_("Who are you with right now?")],
                    "choices": [
                        {"stat": "Love", "reply": _("Nobody. Thinking about you, actually."),
                         "pass": [_("Good answer."), _("...I hate how much I liked it.")],
                         "fail": [_("Hm.")]},
                        {"stat": "Obed", "reply": _("Why do you want to know?"),
                         "pass": [_("Because what's mine, I keep track of."), _("Don't make me ask twice.")],
                         "fail": [_("Forget I asked.")]},
                        {"stat": "Inbt", "reply": _("Jealous?"),
                         "pass": [_("Terribly. Now answer the question.")],
                         "fail": [_("Don't flatter yourself.")]},
                    ],
                },
                {
                    "id": "stolen_shirt", "steps": (3,), "not_trait": "submissive",
                    "her": [_("One of your shirts is missing."), _("It isn't lost. That's all you need to know.")],
                    "choices": [
                        {"stat": "Love", "reply": _("Keep it. It looks better on you."),
                         "pass": [_("Obviously."), _("It's being put to good use. Goodnight.")],
                         "fail": [_("Of course I'm keeping it. It wasn't a question.")]},
                        {"stat": "Obed", "reply": _("Bring it back tomorrow. Worn."),
                         "pass": [_("...You've gotten bold. Tomorrow. And I'm deleting this chat.")],
                         "fail": [_("It's MY shirt now. Learn to count your laundry.")]},
                        {"stat": "Inbt", "reply": _("Just the shirt? Send proof."),
                         "pass": [_("Nothing leaves this phone. Ever. You get the real thing or you get nothing.")],
                         "fail": [_("You wish. Goodnight, boy.")]},
                    ],
                },
                # ── step 3, the SUBMISSIVE twins (she lost the femdom: she asks, the old chats demand) ──
                {
                    "id": "mine_sub", "steps": (3,), "trait": "submissive",
                    "her": [_("Is it alright if I text you right now?"), _("I keep rereading our chat. Tell me what you're doing.")],
                    "choices": [
                        {"stat": "Love", "reply": _("Thinking about you, actually."),
                         "pass": [_("...Good."), _("I read that three times. Keep it.")],
                         "fail": [_("Okay. I'll stop bothering you.")]},
                        {"stat": "Obed", "reply": _("Studying. Keep the phone warm until I'm done."),
                         "pass": [_("Yes. ...Tell me when. I'll be here.")],
                         "fail": [_("Alright. Study well.")]},
                        {"stat": "Inbt", "reply": _("Why, were you about to misbehave?"),
                         "pass": [_("I don't do anything you don't know about. Not anymore."), _("...Ask me that in person.")],
                         "fail": [_("No. Goodnight.")]},
                    ],
                },
                {
                    "id": "stolen_shirt_sub", "steps": (3,), "trait": "submissive",
                    "her": [_("I took one of your shirts. I should have asked first."), _("May I keep it? Please.")],
                    "choices": [
                        {"stat": "Love", "reply": _("Keep it. It looks better on you."),
                         "pass": [_("Thank you. You're not getting it back."), _("It's on my side of the bed. That's all I'll write.")],
                         "fail": [_("Thank you. Really.")]},
                        {"stat": "Obed", "reply": _("Bring it back tomorrow. Worn."),
                         "pass": [_("Understood. ...And then I'm deleting this chat."), _("...As you want. Tomorrow.")],
                         "fail": [_("Yes. Tomorrow. Sorry for taking it.")]},
                        {"stat": "Inbt", "reply": _("Just the shirt? Send proof."),
                         "pass": [_("...I can't. You know I can't. Ask me for anything else and it's yes.")],
                         "fail": [_("...You'll have to imagine it. Goodnight.")]},
                    ],
                },
            ],
        },
    }

    def story_husband_on_trip(girl):
        """Her husband is away on a trip and he can leave his room: the morning she calls him home (marital_bed)."""
        _h = girl_husband(girl)
        return _h is store.Dad and dad_on_trip()

    def story_husband_here(girl):
        """Her husband is in the apartment with them right now, in any room (family_room, family_father.rpy)."""
        _h = girl_husband(girl)
        return _h is not None and store.CurrentLocation in APARTMENT_ROOMS and family_room(_h) is not None

    def story_husband_next_room(girl):
        """distract_father: her husband is home, in another room of the apartment than them."""
        return story_husband_here(girl) and family_room(girl_husband(girl)) != store.CurrentLocation

    def story_husband_call_due(girl):
        """husband_calls: a couple of moves into a scene with her, her husband not in the apartment with them."""
        return (girl_husband(girl) is not None
                and store._sub_event_actions_taken >= 2 and not story_husband_here(girl))

    def story_husband_home(girl):
        """Her husband is home tonight (not on a business trip): the fight she runs from (vent_night)."""
        _h = girl_husband(girl)
        return _h is not None and not (_h is store.Dad and dad_on_trip())

    def story_vent_night_ready(girl):
        """vent_night: her husband is home AND his last grade is at least a B."""
        if not story_husband_home(girl):
            return False
        _hist = getattr(store.Player, "grade_history", None) or []
        return bool(_hist) and _hist[-1] in FAMILY_GOOD_GRADES

    def story_drugged_dinner_ready(girl):
        """drugged_dinner: her husband is NOT on a trip (he's home for dinner), the player has a strong drink."""
        _h = girl_husband(girl)
        if _h is not store.Dad or dad_on_trip():
            return False
        return any(store.Player.get_item_count(d) > 0 for d in drinks_of_tier("high"))

    def story_husband_out(girl):
        """Her husband exists but is NOT in the apartment right now (work, a trip): the hours that are theirs."""
        _h = girl_husband(girl)
        return _h is not None and family_room(_h) is None

    def story_grade_text_due(girl):
        """grade_summons: she watches his grades (family_guardian), his last exam grade is a bad one, the fresh
        grade news (family_grades) is not still waiting to play, and she has not already nagged about THIS grade
        (once per exam, not repeating every few days)."""
        _hist = getattr(store.Player, "grade_history", None) or []
        _idx = getattr(store, "_grade_summons_idx", 0) or 0
        return (family_guardian() is girl and bool(_hist) and _hist[-1] in FAMILY_BAD_GRADES
                and not getattr(store, "_family_grade_news", None)
                and _idx < len(_hist))

    def story_husband_steps_due(girl):
        """husband_steps: a scene with her in the apartment, her husband home in another room, a couple of moves in."""
        return story_husband_next_room(girl) and store._sub_event_actions_taken >= 2

    def story_text_pick(girl):
        """A chat of her step for this text, never the one of her last text when another one fits. A chat with
        "only_event" belongs to that event alone (the grade summons), and that event always sends it."""
        _st = story_step(girl)
        _ev = store._story_event_now
        # a chat may be tied to a trait of hers ("trait") or hidden by one ("not_trait"): the broken femdom's
        # step-3 texts have submissive twins (she asks, the old ones demand)
        _cs = [_c for _c in story_data(STORY_TEXTS, girl, {}).get("chats", ())
               if _st in _c.get("steps", ()) and _c.get("only_event") in (None, _ev)
               and (not _c.get("trait") or girl.has_trait(_c["trait"]))
               and not (_c.get("not_trait") and girl.has_trait(_c["not_trait"]))]
        _own = [_c for _c in _cs if _c.get("only_event") == _ev]
        if _own:
            _cs = _own
        _last = getattr(girl, "_story_last_text", None)
        _fresh = [_c for _c in _cs if _c["id"] != _last] or _cs
        return renpy.random.choice(_fresh) if _fresh else None

# The lines of the step she just reached (story_event_play has moved her step already)
label _story_turn_scene(girl):
    python:
        _stl_step = story_step(girl)
        _stl_data = story_data(STORY_TURN_LINES, girl, {})
        # the coercion lane speaks its own turn ("<step>_blackmail") when the block has one
        _stl_lane = story_route_family(store._story_route_now) if store._story_route_now else None
        _stl_lines = (_stl_data.get("%d_%s" % (_stl_step, _stl_lane)) if _stl_lane else None) or _stl_data.get(_stl_step, [])
        print("[STORY] %s: the lines of step %d (route %s, lane %s, %d line(s))" % (
            girl.gid, _stl_step, store._story_route_now, _stl_lane, len(_stl_lines)))
    call story_say(girl, _stl_lines) from _call_story_say_turn
    $ set_scene_expression(girl, "normal", pose="standing")
    return

# The Sunday dinner (step event "family_dinner"): opening narration, one moment, his choice, dad announces exit.
# The sprite exit, close, return, dessert and end-of-night are handled by _apartment_dinner_weekly (shion_family.rpy)
label _story_family_dinner(girl):
    python:
        _sfd = story_data(STORY_DINNERS, girl, {})
        _sfd_m = story_dinner_moment(girl)
        girl._story_last_dinner = _sfd_m["id"] if _sfd_m else None
        _sfd_dad = girl_husband(girl)
        _sfd_exit = _sfd.get("dad_exit")
        print("[STORY] %s: Sunday dinner step %d, moment %s" % (girl.gid, story_step(girl), girl._story_last_dinner))
    call story_say(girl, renpy.random.choice(_sfd.get("open") or [[]])) from _call_story_say_dinner_open
    call story_moment(girl, _sfd_m) from _call_story_moment_dinner
    # dad announces he's going to the kitchen (dialogue only; sprite exit handled by _apartment_dinner_weekly)
    if _sfd_exit and _sfd_dad:
        $ renpy.say(story_husband_char(girl), _tl(renpy.random.choice(_sfd_exit)))
    return

# 0 -> 1, the door of the hand under the table (plan_shion_agency F1): the scene's route lines already
# played and her hand is on his knee. Leaving it there = the step (the turn lines). Moving it away =
# story_unlock_cancel: she recovers without missing a beat, the dinner goes on, the event waits its
# cooldown. The decline costs a little warmth, never a scene.
label _story_hand_under_table(girl):
    menu:
        "Leave her hand where it is.":
            pass
        "Move her hand higher yourself.":
            # the push HE makes (tester 2026-10-11: "at no point did we actually challenge her"): same
            # unlock, his tempo. She covers the surprise fast, and files it away.
            $ Narration(_("You put your hand over hers and slide it higher up your leg. For half a second, her fingers forget what they were doing."))
            $ set_scene_expression(girl, "surprised", pose="standing")
            $ Say_Line(girl, _("..."))
            $ set_scene_expression(girl, "smirk", pose="standing")
            $ Say_Line(girl, _("Noted, [Player.Name]. Interesting."))
            python:
                Change_Status(girl, "Obed", 5)
                print("[STORY] hand_under_table: he pushed her hand higher (Obed +5)")
        "Move her hand away, gently.":
            $ Narration(_("You put your hand over hers and move it back, gently, to her own side of the table. She lets you."))
            $ set_scene_expression(girl, "normal", pose="standing")
            $ Say_Line(girl, _("...Noted."))
            $ Say_Line(girl, _("Pass the salad, [Player.Name]."))
            python:
                Change_Status(girl, "Love", -5)
                story_unlock_cancel(girl, "hand_under_table")
            return
    call _story_turn_scene(girl) from _call_story_turn_scene_hut
    return

# 1 -> 2: the night she runs to his dorm, after the version of her route (STORY_SCENES "vent_night"). He lets it
# happen (a restricted HJ scene; after he finishes, she tries her turn but her husband calls) or sends her home.
# Either way she is gone before dawn, and he goes to sleep (do_sleep goes on)
label _story_vent_night(girl):
    python:
        _svn = story_data(STORY_VENT, girl, {})
        _svn_route = store._story_route_now if store._story_route_now in _svn.get("acts", {}) else _svn.get("default", "love")
        _svn_kind, _svn_pos = _svn["acts"][_svn_route]
        print("[STORY] %s: vent night, route %s -> %s %s" % (girl.gid, _svn_route, _svn_kind, _svn_pos))
    if _svn_route == "obed":
        # the route line just said "take off your coat. She does.": the sprite obeys it too, jacket off
        # (tester 2026-10-11 asked for the visual beat)
        $ girl.Outfit_Change(over="none", refresh=True)
    $ Narration(_("You sit next to her. She leans against you, and you put your arm around her. Your hand rests on her thigh."))
    $ set_scene_expression(girl, "shy", pose="standing")
    $ Say_Line(girl, _("You know, you've been good this week. Your grades, your attitude... I think you deserve a reward."))
    $ set_scene_expression(girl, "sexy", pose="standing")
    $ Narration(_("Her hand finds yours and moves it higher."))
    menu:
        "Let it happen":
            $ _svn_go = True
        "Send her home":
            $ _svn_go = False
    if not _svn_go:
        $ story_unlock_cancel(girl, "vent_night")
        call story_say(girl, _svn["declined"]) from _call_story_say_vent_declined
    else:
        call story_restricted_scene(girl, _svn_kind, _svn_pos) from _call_story_restricted_vent
        # after his finish: she wants her turn, but her husband calls
        $ set_scene_expression(girl, "smug", pose="standing")
        $ Say_Line(girl, _("You had your fun. Now it's my turn."))
        $ set_scene_expression(girl, "sexy", pose="standing")
        $ Narration(_("She leans in closer, her fingers trailing down your chest..."))
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Her phone buzzes on the nightstand. She freezes."))
        python:
            _set_standing_arm(girl, 3)
            _svn_h = girl_husband(girl)
            _svn_who = Character(_svn_h.Name, who_color=_svn_h.color) if _svn_h else None
            print("[STORY] %s: vent night phone call from %s" % (girl.gid, _svn_h.gid if _svn_h else "?"))
        $ set_scene_expression(girl, "serious", pose="standing")
        $ Say_Line(girl, _("It's him..."))
        $ Narration(_("She picks up the phone. Her voice changes instantly."))
        $ set_scene_expression(girl, "normal", pose="standing")
        $ Say_Line(girl, _("Hey, honey. No, I'm still at the office. Late meeting."))
        if _svn_who:
            $ renpy.say(_svn_who, _tl(_("You're working too hard. Come home.")))
        $ set_scene_expression(girl, "sad", pose="standing")
        $ Say_Line(girl, _("I know. I'm leaving now. Go back to sleep."))
        $ Narration(_("She hangs up and stares at the phone for a moment."))
        python:
            _set_standing_arm(girl, 1)
        $ set_scene_expression(girl, "serious", pose="standing")
        $ Say_Line(girl, _("I have to go."))
        call story_say(girl, _svn["after"]) from _call_story_say_vent_after
    python:
        _set_standing_arm(girl, 0)
        girl.loc = girl_home_loc(girl)
        hide_girl_sprite(girl)
        print("[STORY] %s: she goes home before dawn (%s)" % (girl.gid, girl.loc))
    return

# A text of hers at night (step event "her_night_text"): her messages, his reply (one per stat), her answer
label _story_text(girl):
    python:
        _stx = story_text_pick(girl)
        girl._story_last_text = _stx["id"] if _stx else None
        _stx_msgs = list(_stx["her"]) if _stx else []
        _stx_is_grade = (store._story_event_now == "grade_summons")
        if _stx_is_grade and (getattr(store, "_grade_summons_idx", 0) or 0) == 0:
            _stx_msgs.insert(0, _("You know I'm friends with the dean, right? I have access to everything in this college."))
        print("[STORY] %s texts him at step %d: %s (grade_summons=%s)" % (girl.gid, story_step(girl), girl._story_last_text, _stx_is_grade))
    if _stx:
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. Someone sent you a message."))
        while _stx_msgs:
            call _phone_typing(girl, choices=[]) from _story_text_typing
            $ phone_add_msg(girl.gid, girl.gid, _tl(_stx_msgs.pop(0)))
        python:
            _stx_choices = [(_tl(_c["reply"]), "reply_%d" % _i) for _i, _c in enumerate(_stx["choices"])]
        call screen phone_chat_screen(girl, choices=_stx_choices)
        python:
            _stx_pick = [_i for _i, _ch in enumerate(_stx_choices) if _ch[1] == _return]
        if _stx_pick:
            python:
                _stx_c = _stx["choices"][_stx_pick[0]]
                phone_add_msg(girl.gid, "player", _stx_choices[_stx_pick[0]][0])
                _stx_ok = story_test(girl, _stx_c["stat"])
                _stx_msgs = list(_stx_c["pass" if _stx_ok else "fail"])
                _stx_last = (_stx_msgs or [""])[-1]
                print("[STORY] %s: he replies %s -> %s" % (girl.gid, _stx_c["stat"], _stx_ok))
            while _stx_msgs:
                call _phone_typing(girl, choices=[]) from _story_text_reply_typing
                $ phone_add_msg(girl.gid, girl.gid, _tl(_stx_msgs.pop(0)))
            $ story_choice_reward(girl, _stx_c["stat"], _stx_ok)
            # The thread doesn't just stop mid-air (author 2026-10-11, "the player felt lost"): one
            # narration row says the talk went on, only not worth transcribing. Never on a fail (she
            # cut it short on purpose), never after her own goodbye, never on the cold grade summons.
            if (_stx_ok and not _stx_is_grade
                    and "goodnight" not in _stx_last.lower() and "go to sleep" not in _stx_last.lower()):
                $ phone_add_msg(girl.gid, "system", _tl(renpy.random.choice(_STORY_TEXT_CLOSE)), "system")
            call screen phone_chat_screen(girl, choices=[])
        if _stx_is_grade:
            $ store._grade_summons_idx = len(getattr(store.Player, "grade_history", None) or [])
    return

# Step 0, on his way to the late bus (trigger "downtown_night"): a black car drops her off, and she buys his
# silence with a look. Narrated over the Downtown picture, her voice with no face
label _story_home_late(girl):
    python:
        hide_girl_sprite(girl)
        print("[STORY] %s: home_late (Day %d)" % (girl.gid, Day))
    scene expression ("bg downtown_night" if TimeIndex >= NIGHT_INDEX else "bg downtown")
    with fade
    call story_moment(girl, story_moment_data(girl, "home_late")) from _call_story_moment_home_late
    return

# Step 1, her terms (step event "her_terms"): she decides to use what her step opened. The route that opened her
# step picks the act (STORY_HER_TERMS "acts"); a restricted scene, then the room goes back to normal
label _story_her_terms(girl):
    python:
        _sht = story_data(STORY_HER_TERMS, girl, {})
        _sht_route = story_step_route(girl)
        if _sht_route not in _sht.get("acts", {}):
            _sht_route = _sht.get("default", "love")
        _sht_kind, _sht_pos = _sht["acts"][_sht_route]
        print("[STORY] %s: her terms, route %s -> %s" % (girl.gid, _sht_route, _sht_kind))
    call story_say(girl, _sht.get("open")) from _call_story_say_terms_open
    call story_say(girl, _sht.get("routes", {}).get(_sht_route)) from _call_story_say_terms_route
    call story_restricted_scene(girl, _sht_kind, _sht_pos) from _call_story_restricted_terms
    call story_say(girl, _sht.get("after")) from _call_story_say_terms_after
    return

# Step 2, stolen minutes (step event "stolen_minutes"): her husband one room away, four minutes in the kitchen
label _story_stolen_minutes(girl):
    python:
        _ssm = story_data(STORY_STOLEN, girl, {})
        print("[STORY] %s: stolen minutes (her husband in the next room)" % girl.gid)
    call story_say(girl, _ssm.get("open")) from _call_story_say_stolen_open
    call story_restricted_scene(girl, "bj") from _call_story_restricted_stolen
    call story_say(girl, _ssm.get("after")) from _call_story_say_stolen_after
    return

# Step 3, her appetite (step event "her_appetite"): she comes to his dorm at night already decided. The route that
# opened her step picks the act (STORY_APPETITE "acts", the inbt route is anal); she goes home after ("leaves")
label _story_her_appetite(girl):
    python:
        _sha = story_data(STORY_APPETITE, girl, {})
        _sha_route = story_step_route(girl)
        if _sha_route not in _sha.get("acts", {}):
            _sha_route = _sha.get("default", "love")
        _sha_kind, _sha_pos, _sha_anal = _sha["acts"][_sha_route]
        print("[STORY] %s: her appetite, route %s -> %s %s%s" % (
            girl.gid, _sha_route, _sha_kind, _sha_pos, " (anal)" if _sha_anal else ""))
    call story_say(girl, _sha.get("open")) from _call_story_say_appetite_open
    call story_say(girl, _sha.get("routes", {}).get(_sha_route)) from _call_story_say_appetite_route
    call story_restricted_scene(girl, _sha_kind, _sha_pos, _sha.get("no_condom"), _sha.get("no_condom_act", ("bj", None)), _sha_anal) from _call_story_restricted_appetite
    call story_say(girl, _sha.get("after")) from _call_story_say_appetite_after
    return

# 2 -> 3: the marital bed. A morning her husband is away she texts him home; he goes (the bedroom she shares with his
# father: the version of her route, a restricted scene, the end of her turn) or he can't (she stays on her step and
# asks again after the cooldown). Going takes him there: Wait returns after it (_story_morning_moved)
label _story_marital_bed(girl):
    python:
        _smb = story_data(STORY_MARITAL, girl, {})
        _smb_route = store._story_route_now if store._story_route_now in _smb.get("acts", {}) else _smb.get("default", "love")
        _smb_kind, _smb_pos = _smb["acts"][_smb_route]
        _smb_msgs = list(_smb["texts"])
        print("[STORY] %s: marital bed, route %s -> %s %s" % (girl.gid, _smb_route, _smb_kind, _smb_pos))
    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. Someone sent you a message."))
    while _smb_msgs:
        call _phone_typing(girl, choices=[]) from _story_marital_typing
        $ phone_add_msg(girl.gid, girl.gid, _tl(_smb_msgs.pop(0)))
    python:
        _smb_choices = [(_tl(_("On my way.")), "go"), (_tl(_("I can't today.")), "no")]
    call screen phone_chat_screen(girl, choices=_smb_choices)
    if _return != "go":
        python:
            story_unlock_cancel(girl, "marital_bed")
            _smb_msgs = list(_smb["declined"]) if _return == "no" else []
            if _return == "no":
                phone_add_msg(girl.gid, "player", _smb_choices[1][0])
        while _smb_msgs:
            call _phone_typing(girl, choices=[]) from _story_marital_declined_typing
            $ phone_add_msg(girl.gid, girl.gid, _tl(_smb_msgs.pop(0)))
        call screen phone_chat_screen(girl, choices=[])
        return
    $ phone_add_msg(girl.gid, "player", _smb_choices[0][0])
    call screen phone_chat_screen(girl, auto_close=1.0, choices=[])

    scene black
    with fade
    $ Narration(_("You take the first bus across town."))
    python:
        _smb_room = girl_home_loc(girl)
        navigate_to(_smb_room, None)
        girl.loc = _smb_room
    call Set_Scene(entry=True) from _call_Set_Scene_marital_bed
    call story_route_scene(girl, "marital_bed") from _call_story_route_scene_marital
    # ── Multi-phase restricted scene (phase 1: BJ, phase 2: RCG if energy) ──
    python:
        time_lock()
        store._scene_restricted = True
        store.door_locked = True
        store._interruption_happened = True
        store._witness_check_done = True
        store._npc_witness_check_done = True
        store._condom_removed_midscene = False
        store._creampie_consent = False
        store._player_exposed_this_session = False
        session_cum_reset()
        _scene_exit_flags_reset()
        print("[STORY] %s: marital bed multi-phase scene" % girl.gid)

    # ── Phase 1: BJ (one cum ends it) ──
    # her rule said OUT LOUD first (tester 2026-10-11: her grab-reaction scolded "I told you to warn
    # me" and she never had): now she tells him, and breaking it is a real choice
    $ set_scene_expression(girl, "serious", pose="standing")
    $ Say_Line(girl, _("One rule. You warn me before you finish. Say nothing else, just warn me."))
    call start_scene(girl, "bj") from _call_start_scene_marital_bj

    python:
        _smb_has_energy = store.Player.energy > 0
        _smb_bailed = False   # he lifts her off and ends the show (the .marital_ask menu): no happy "after"
        _smb_bj_only = (store._story_bm_demand == "bj_only")   # the extraction he named at the gate (coerced lane)
        print("[STORY] marital bed: BJ done, energy=%d, can_continue=%s, bj_only=%s" % (
            store.Player.energy, _smb_has_energy, _smb_bj_only))
    call Set_Scene(entry=True) from _call_Set_Scene_marital_between

    if _smb_bj_only:
        # The demand he picked ends the night here (plan_shion_agency, "o 2"): the step still climbs,
        # no second phase, no fury, and the bed verdict below stays out of a night she set no stakes on.
        $ set_scene_expression(girl, "normal", pose="standing")
        $ Say_Line(girl, _("That's all you're taking tonight? ...Noted."))
        $ print("[STORY] marital bed: demand bj_only, phase 2 skipped")
    elif not _smb_has_energy:
        # ── No energy: she is furious, scene aborted. The step she just gained goes back too (review
        # 2026-10-10): story_step_up ran before this label, and a failed unlock never keeps the step (the
        # same rule as vent_night's "Send her home" and the dinner's "Never mind"); the event waits its
        # cooldown and the morning comes again.
        $ set_scene_expression(girl, "angry", pose="standing")
        $ Say_Line(girl, _("That's it? You came all the way here just to embarrass yourself?"))
        $ Say_Line(girl, _("I am a spectacle. I deserve someone who can keep up with me."))
        $ set_scene_expression(girl, "disgusted", pose="standing")
        $ Say_Line(girl, _("Get dressed. And go straight to a gym, you weakling."))
        $ Change_Status(girl, "Love", -15)
        $ Change_Status(girl, "Obed", -10)
        $ girl.set_temp_status("angry", 1, reason="marital_bed_no_energy")
        $ story_unlock_cancel(girl, "marital_bed")
    else:
        # ── Phase 2: RCG (she is in control) ──
        $ set_scene_expression(girl, "smug", pose="standing")
        $ Say_Line(girl, _("Not bad. But we're not done yet."))
        $ set_scene_expression(girl, "sexy", pose="standing")
        $ Say_Line(girl, _("Lie down. And put a condom on. We're doing this my way."))

        # ── Condom: she always has one; player's is consumed if he has it ──
        python:
            _smb_player_has_condom = Player.has_item("condom") or Player.has_item("japanese_condom")
        if not _smb_player_has_condom:
            $ set_scene_expression(girl, "angry", pose="standing")
            $ Say_Line(girl, _("You came here without a condom? Are you serious?"))
            $ set_scene_expression(girl, "serious", pose="standing")
            $ Say_Line(girl, _("Lucky for you, I keep some in the nightstand. Don't ever come unprepared again."))
        else:
            python:
                if Player.has_item("condom"):
                    Player.remove_item("condom")
                else:
                    Player.remove_item("japanese_condom")

        $ Narration(_("She pushes you onto the bed and climbs over you, facing away."))

        python:
            store.condom_active = True
            condom_break_reset()
            _scene_exit_flags_reset()
            session_cum_reset()
            store._condom_rip_attempted = True
            store.Player.Focus = 0
            print("[STORY] marital bed phase 2: condom on (player_had=%s), RCG start" % _smb_player_has_condom)

        # RCG launch: hide standing sprite (keeps room background), full scene init
        $ hide_girl_sprite(girl)
        call RCG_Launch(girl) from _call_RCG_Launch_marital_bed

        # Start at just the tip, high above him (she barely has him inside)
        python:
            store.rcg_started = True
            store.rcg_tip_mode = True
            store._srcg_extra_lift = 45
        call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_marital_tip

        # ── Teasing phase: she rides the tip slowly, Focus builds ──
        $ set_scene_expression(girl, "smug")
        $ Say_Line(girl, _("Feel that? That's all you're getting."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ Narration(_("She barely moves. Just enough to drive you insane."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ Say_Line(girl, _("I set the pace here. Not you."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ set_scene_expression(girl, "sexy")
        $ Say_Line(girl, _("Don't even think about moving. This is my show."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ Say_Line(girl, _("You want more? Too bad."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ Narration(_("She grinds against you in slow, deliberate circles."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ set_scene_expression(girl, "smug")
        $ Narration(_("Every time you try to push deeper, she pulls away."))
        $ renpy.pause()
        $ add_player_focus(10)

        $ Narration(_("You feel yourself getting dangerously close."))
        $ renpy.pause()
        $ add_player_focus(10)

        # ── Edge: she stops, Focus drops ──
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_marital_edge

        $ set_scene_expression(girl, "smug")
        $ Say_Line(girl, _("Not yet."))
        $ renpy.pause()
        python:
            Player.Focus = max(0, Player.Focus - 50)
        $ Say_Line(girl, _("You don't get to finish until I say so."))
        $ renpy.pause()

        # She resumes at tip
        call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_marital_resume
        $ renpy.pause()

        # Begging must not be the only door (tester 2026-10-10). The demand is always visible and HER
        # STATS answer it: Inbt 600 (this unlock's own inbt route limit; the violet bar players read as
        # blue) or Obed 550 lets his audacity land; under it she restarts her game. Walking out is the
        # engine's "no" to an unlock (story_unlock_cancel, the drugged dinner's "Never mind" rule).
        label .marital_ask:
        menu:
            "Please... I need more.":
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("That's what I wanted to hear."))
                $ renpy.pause()

            "I don't beg. Move your hips.":
                python:
                    _smb_demand_ok = girl.Inbt >= 600 or girl.Obed >= 550
                    print("[STORY] marital bed demand: Inbt=%d Obed=%d -> %s" % (
                        girl.Inbt, girl.Obed, "she allows it" if _smb_demand_ok else "she starts over"))
                if _smb_demand_ok:
                    # bubbles don't block: one pause per line, or they replace each other unread
                    # (tester 2026-10-11, "texto passando extremamente rapido")
                    $ set_scene_expression(girl, "surprised")
                    $ Narration(_("Her rhythm stops. For a moment, the only sound in the room is her breathing."))
                    $ renpy.pause()
                    $ set_scene_expression(girl, "sexy")
                    $ Say_Line(girl, _("...Look at you. Giving orders in my bed."))
                    $ renpy.pause()
                    $ Say_Line(girl, _("One time, I'll allow it."))
                    $ Change_Status(girl, "Obed", 5)
                    $ renpy.pause()
                else:
                    $ set_scene_expression(girl, "smug")
                    $ Say_Line(girl, _("Orders? From you? That's adorable."))
                    $ renpy.pause()
                    python:
                        Player.Focus = max(0, Player.Focus - 30)
                    $ Narration(_("She lifts herself until you almost slip out, and holds there."))
                    $ renpy.pause()
                    $ Say_Line(girl, _("We start over. And this time, you'll ask nicely."))
                    $ renpy.pause()
                    jump .marital_ask

            "Lift her off and end this.":
                $ _smb_bailed = True
                $ store.rcg_speed = 0
                call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_marital_bail
                $ Narration(_("You take her by the hips, lift her off you, and sit up."))
                $ renpy.pause()
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("...Excuse me?"))
                $ renpy.pause()
                $ Say_Player(_("I'm not spending the night being rationed. We're done here."))
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Then we are done. Get out of my bedroom."))
                $ renpy.pause()
                python:
                    Change_Status(girl, "Love", -10)
                    Change_Status(girl, "Obed", -5)
                    girl.set_temp_status("angry", 1, reason="marital_bed_walkout")
                    story_unlock_cancel(girl, "marital_bed")
                    store._post_cum_pending = False
                    store._rcg_girl = None
                    store._srcg_girl = None
                    scene_full_cleanup(girl)
                jump .marital_cleanup

        # ── Descent: she sinks onto him slowly, then slams down ──
        $ Narration(_("She starts lowering herself... slowly."))
        python:
            # tip mode stays on so the extra lift applies during the descent
            for _smb_step in [38, 30, 22, 14, 8, 3]:
                store._srcg_extra_lift = _smb_step
                _srcg_apply_speed(girl, 1)
                renpy.pause(0.18)
            # slam: fully seated (speed 0 = drawn position = deepest penetration)
            store.rcg_tip_mode = False
            store._srcg_extra_lift = 0
            _srcg_apply_speed(girl, 0)
        with vpunch
        $ renpy.pause(0.8)

        python:
            store.rcg_speed = 2
            girl.Lust = 95
        call RCG_ApplySpeed(girl, 2) from _call_RCG_ApplySpeed_marital_bed

        python:
            mark_intimacy(girl, "sex")
            mark_intimacy(girl, "reverse_cowgirl")
            Change_Status(girl, "Love", 15)
            Change_Status(girl, "Inbt", 10)
            Change_Status(girl, "Obed", 5)

        call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_marital_bed

        # ── Post-cum: auto-end (no menu in this event) ──
        if store._rcg_girl is not None:
            if not getattr(girl, "Cum", False):
                # Condom cum: slow wind-down before stopping
                $ store.rcg_speed = 1
                call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_marital_winddown
                $ renpy.pause(3.0)
            $ store.rcg_speed = 0
            call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_marital_still
            $ Narration(_("She slowly lifts herself off you."))
            $ renpy.pause(1.5)

        python:
            store._post_cum_pending = False
            store._rcg_girl = None
            store._srcg_girl = None
            scene_full_cleanup(girl)

    # ── Final cleanup ── (.marital_cleanup: the walk-out lands here with the RCG already ended)
    label .marital_cleanup:
    python:
        store._scene_restricted = False
        store._scene_angry_abort = False
        store._player_exhausted = False
        store.door_locked = False
        store._interruption_happened = False
        store._witness_check_done = False
        store._npc_witness_check_done = False
        store._srcg_extra_lift = 0
        time_unlock()
    call Set_Scene(entry=True) from _call_Set_Scene_marital_after

    if _smb_bj_only and not _smb_bailed:
        # a mouth-only extraction: the step's turn lines play, the bed verdict does not
        call _story_turn_scene(girl) from _call_story_turn_scene_marital_bjonly
    if _smb_has_energy and not _smb_bailed and not _smb_bj_only:
        # Her verdict is HER orgasm, never his round count (the author 2026-10-10; tester: five rounds
        # in a row and she sounded let down). She came: the warm after, plus a nod when he kept pace
        # for three or more finishes. She did not: she says exactly why, and the warm after stays shut.
        python:
            _smb_her_cums = store._session_orgasms_by_girl.get(girl.gid, 0)
            _smb_his_rounds = sum(_v for _v in store._session_cum.values())
            print("[STORY] marital bed verdict: her orgasms=%d, his finishes=%d" % (_smb_her_cums, _smb_his_rounds))
        if _smb_her_cums > 0:
            $ set_scene_expression(girl, "happy")
            call story_say(girl, _smb["after"]) from _call_story_say_marital_after
            if _smb_his_rounds >= 3:
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _tl(_("...And that stamina. I lost count. Do not let it go to your head.")))
        else:
            $ set_scene_expression(girl, "normal")
            $ Say_Line(girl, _tl(_("Impressive stamina. Entirely wasted: you finished over and over, and I finished nothing.")))
            $ Say_Line(girl, _tl(_("Next time, slower. A woman is not a finish line. ...Goodnight, [Player.Name].")))
        call _story_turn_scene(girl) from _call_story_turn_scene_marital

    $ _smb_cost = max(1, 100 - Round)
    call Apply_Time_Cost(_smb_cost) from _call_Apply_Time_Cost_marital
    $ store._story_morning_moved = True
    return

# ── 3 -> 4: the drugged dinner. A Sunday dinner where the player gives dad a strong drink. He passes out.
#    She takes the player in doggy, raw, and demands the creampie. The final step unlocks.
label _story_drugged_dinner(girl):
    python:
        _sdd_husband = story_husband_char(girl)
        _sdd_route = store._story_route_now or "love"
        _sdd_owned = player_owned_drinks()
        print("[STORY] %s: drugged dinner, route %s, owned drinks %s" % (girl.gid, _sdd_route, _sdd_owned))

    # ── Dinner opening: dad is in a great mood ──
    call story_say(girl, [
        (None, _("Sunday dinner. Your father pours the wine, talks about work, and laughs at his own jokes. He's in a good mood tonight.")),
        ("@husband", _("You know what would make this night perfect? A proper drink. Not this wine stuff.")),
        ("@husband", _("Something with kick. Something that burns.")),
        (None, _("He looks at you like he just gave you a mission.")),
    ]) from _call_story_say_drugged_open

    # ── Drink menu: list owned drinks + "Never mind" ──
    python:
        _sdd_menu = []
        for _did, _cnt in _sdd_owned:
            _d = drink_info(_did)
            _sdd_menu.append((_tl(_d["label"]), _did))
        _sdd_menu.append((_tl(_("Never mind.")), "none"))

    $ _sdd_pick = renpy.display_menu(_sdd_menu)

    if _sdd_pick == "none":
        call story_say(girl, [
            ("@husband", _("No? Ah well. Maybe next time.")),
        ]) from _call_story_say_drugged_nevermind
        $ story_unlock_cancel(girl, "drugged_dinner")
        return

    # ── Player offers a drink ──
    python:
        _sdd_info = drink_info(_sdd_pick)
        _sdd_tier = _sdd_info["tier"]
        _sdd_name = _tl(_sdd_info["label"])
        player_consume_drink(_sdd_pick)
        print("[STORY] %s: offered %s (tier %s)" % (girl.gid, _sdd_pick, _sdd_tier))

    if _sdd_tier != "high":
        # LOW or MED: dad enjoys it but stays awake. Event fails.
        call story_say(girl, [
            ("@husband", _("Oh, nice! Thanks, son.")),
            (None, _("He takes a long sip and nods appreciatively.")),
            ("@husband", _("Good stuff. Not strong enough to knock me out, though!")),
            (None, _("He laughs and pats his chest. The dinner continues normally.")),
        ]) from _call_story_say_drugged_weak
        $ story_unlock_cancel(girl, "drugged_dinner")
        return

    # ── HIGH tier: dad drinks, gets drowsy, passes out ──
    call story_say(girl, [
        ("@husband", _("Now THAT'S what I'm talking about!")),
        (None, _("He pours himself a generous glass and drinks it like water.")),
        ("@husband", _("Whew! That's the real stuff right there.")),
    ]) from _call_story_say_drugged_strong

    $ renpy.pause(1.0)

    call story_say(girl, [
        (None, _("He pours another. Then another. His voice gets louder, his words slower.")),
        ("@husband", _("You know... you're a good kid. Best thing I ever did was... bring you here...")),
        (None, _("His head sinks. His glass tilts. She catches it before it spills.")),
        (None, _("He's out cold.")),
    ]) from _call_story_say_drugged_passout

    # out cold for the rest of the slot: the drinks' nap (family_father.rpy _family_drink): off scene, and not "in the
    # room" with them (husband_in_room), so nothing of her ladder is held back by him
    python:
        _sdd_dad = girl_husband(girl)
        if _sdd_dad is not None:
            _sdd_dad._nap = (Day, TimeIndex)
            print("[STORY] %s: her husband passes out (nap, Day %d slot %d)" % (girl.gid, Day, TimeIndex))
    call Set_Scene(entry=False) from _call_Set_Scene_drugged_nap

    $ renpy.pause(1.5)

    # ── She reacts ──
    call story_say(girl, [
        (None, _("She watches him for a long moment, then looks at you.")),
    ]) from _call_story_say_drugged_react

    if _sdd_route == "love":
        call story_say(girl, [
            ("surprised", _("Did you plan this?")),
            (None, _("She doesn't wait for an answer.")),
            ("sexy", _("...Come with me.")),
        ]) from _call_story_say_drugged_react_love
    elif _sdd_route == "obed":
        call story_say(girl, [
            ("smirk", _("Well played.")),
            ("sexy", _("Bedroom. Now.")),
        ]) from _call_story_say_drugged_react_obed
    elif _sdd_route == "blackmail":
        call story_say(girl, [
            ("serious", _("...You planned this. Of course you did. You collect leverage the way other boys collect excuses.")),
            ("sexy", _("Fine. Tonight you get everything. Not for what's on your phone. Because I decided I feel like it.")),
        ]) from _call_story_say_drugged_react_bm
    else:
        call story_say(girl, [
            ("serious", _("You did this on purpose.")),
            ("sexy", _("...Good.")),
            (None, _("She takes your hand and pulls you to the bedroom.")),
        ]) from _call_story_say_drugged_react_inbt

    # The last door (plan_shion_agency F1): even over his unconscious father, walking away is allowed.
    # The unlock never survives a no (story_unlock_cancel), and she does not forgive being left
    # standing in the middle of her own crime scene.
    menu:
        "Follow her.":
            # the demand, at its natural beat (demand_late): only on the coerced lane
            python:
                if (store._story_route_now in ("blackmail", "evidence") and store._story_bm_demand is None
                        and STORY_EVENTS["drugged_dinner"].get("bm_demands")):
                    store._story_bm_demand = renpy.display_menu(
                        [(_tl(_bd_cap), _bd_mode) for _bd_cap, _bd_mode in STORY_EVENTS["drugged_dinner"]["bm_demands"]])
                    print("[STORY] drugged dinner late demand -> %s" % store._story_bm_demand)
        "Not like this. Walk away.":
            $ Say_Player(_("...Not like this."))
            call story_say(girl, [
                ("angry", _("You put your own father to sleep at my table, and NOW you find a conscience?")),
                ("serious", _("Help me carry him to the couch. Then get out of my home.")),
            ]) from _call_story_say_drugged_walkout
            python:
                Change_Status(girl, "Love", -10)
                Change_Status(girl, "Obed", -5)
                girl.set_temp_status("angry", 1, reason="drugged_dinner_walkout")
                story_unlock_cancel(girl, "drugged_dinner")
            $ Narration(_("You take the late bus home. Your head is somewhere else entirely."))
            $ navigate_to("room", None)
            return

    # ── Scene setup: doggy, raw, she wants it inside (_force_creampie). A restricted scene of her story: the clock waits,
    #    nobody walks in, and his finish does not end it (_scene_cum_continues: the post-cum menu, keep going) ──
    python:
        _sdd_condom = (store._story_bm_demand == "condom")   # the demand he named (late ask above, coerced lane)
        time_lock()
        store._scene_restricted = True
        store._scene_cum_continues = True
        store._force_creampie = not _sdd_condom
        store.door_locked = True
        store._interruption_happened = True
        store._witness_check_done = True
        store._npc_witness_check_done = True
        store._condom_removed_midscene = False
        store._creampie_consent = "allowed" if not _sdd_condom else False
        store._player_exposed_this_session = False
        session_cum_reset()
        _scene_exit_flags_reset()
        # his demand at the gate decides the night (plan_shion_agency, "o 2"): her way is bare; his
        # "With a condom." keeps one on, his own if he brought it
        store.condom_active = _sdd_condom
        if _sdd_condom:
            condom_break_reset()
            if Player.has_item("condom"):
                Player.remove_item("condom")
            elif Player.has_item("japanese_condom"):
                Player.remove_item("japanese_condom")
        print("[STORY] %s: drugged dinner scene start (doggy, condom=%s, force_creampie=%s)" % (
            girl.gid, _sdd_condom, store._force_creampie))

    if _sdd_condom:
        call story_say(girl, [
            ("normal", _("A condom. ...So you do have limits after all. Fine. Tonight, your rules.")),
        ]) from _call_story_say_drugged_setup_condom
    else:
        call story_say(girl, [
            ("sexy", _("No condom. Not tonight.")),
            ("lusty", _("Don't hold back.")),
        ]) from _call_story_say_drugged_setup

    python:
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 15)
        Change_Status(girl, "Obed", 10)

    # ── Doggy scene: the whole scene flow (intimacy, his finish, the post-cum menu: keep going / stop) ──
    call start_scene(girl, "sex", "doggy") from _call_start_scene_drugged

    # ── Post-scene cleanup ──
    python:
        store._scene_restricted = False
        store._scene_cum_continues = False
        store._force_creampie = False
        store._scene_angry_abort = False
        store._player_exhausted = False
        store.door_locked = False
        store._interruption_happened = False
        store._witness_check_done = False
        store._npc_witness_check_done = False
        time_unlock()
    call Set_Scene(entry=True) from _call_Set_Scene_drugged_after

    # ── After lines: the surrender ──
    $ set_scene_expression(girl, "happy")

    if _sdd_route == "love":
        call story_say(girl, [
            ("happy", _("I've been wanting this. Wanting you. All of you.")),
            ("sexy", _("No more rules. No more holding back.")),
        ]) from _call_story_say_drugged_after_love
    elif _sdd_route == "obed":
        call story_say(girl, [
            ("shy", _("I didn't think I'd ever say this to you.")),
            ("sexy", _("You're in charge now. Completely.")),
        ]) from _call_story_say_drugged_after_obed
    elif _sdd_route == "blackmail":
        call story_say(girl, [
            ("sexy", _("Go on then. Take your prize. We both know you'll delete nothing, and I'll pretend I don't care.")),
            ("smug", _("Lucky for you... tonight I really don't.")),
        ]) from _call_story_say_drugged_after_bm
    else:
        call story_say(girl, [
            ("serious", _("You took what you wanted. Just like I knew you would.")),
            ("sexy", _("Don't stop now.")),
        ]) from _call_story_say_drugged_after_inbt

    python:
        store._drugged_dinner_done = True
        _sdd_cost = max(1, 100 - Round)
    call Apply_Time_Cost(_sdd_cost) from _call_Apply_Time_Cost_drugged
    return
