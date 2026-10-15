init python:

    # ================================================================
    # NEVER HAVE I EVER (NHIE) — Hangout Night Minigame
    # ================================================================

    NHIE_CATEGORY_GATES = {
        "safe": 0,
        "lewd": 2,
        "sexual": 5,
        "nuclear": 8,
    }

    # ------------------------------------------------------------------
    # STATEMENT REGISTRY
    # ------------------------------------------------------------------
    # check(girl) -> True if she HAS done it (she drinks)
    # player_check() -> True if the player has done it (he drinks)
    # tags: "player_only" = only appears in player menu
    #        "needs_bf"   = only when NPC partner is present
    # drama_weight: 1-5, higher = AI prefers it for drama
    # ------------------------------------------------------------------

    # NOTE: entries contain lambdas (check/player_check). NEVER bind a raw entry
    # (or a list of them) to a store variable in label code -> save/pickle crash.
    # Use _nhie_public() / NHIE_BY_ID (see SAVE SAFETY block below).
    NHIE_STATEMENTS = [

        # ======================== SAFE ========================

        {
            "id": "blackout_drunk",
            "text": _("...been so drunk I forgot what happened."),
            "category": "safe",
            "check": lambda g: g.has_trait("lightweight") or getattr(g, "_blackout_count", 0) > 0,
            "player_check": lambda: getattr(store.Player, "_blackout_count", 0) > 0,
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "lightweight": ("embarrassed", [
                    _("It doesn't take much for me, okay?"),
                    _("One beer too many and I'm gone."),
                ]),
                "heavy_drinker": ("smirk", [
                    _("It took a whole bar to put me down, for the record."),
                ]),
                "nerd": ("embarrassed", [
                    _("I'm not proud of it. The hangover killed my study schedule."),
                ]),
                "gym_rat": ("happy", [
                    _("After a party and leg day? Yeah, I was done."),
                ]),
                "default": ("shy", [
                    _("Yeah... that was a wild night."),
                    _("I woke up with no idea how I got home."),
                ]),
            },
            "skip_reactions": {
                "lightweight": ("surprised", [
                    _("Somehow I always remember. Even the embarrassing parts."),
                ]),
                "heavy_drinker": ("smirk", [
                    _("Takes a lot more than a few drinks to make me lose a night."),
                ]),
                "nerd": ("smirk", [
                    _("I know my limits."),
                ]),
                "default": ("normal", [
                    _("I pace myself. Usually."),
                ]),
            },
        },
        {
            "id": "exercised_today",
            "text": _("...actually worked out today."),
            "category": "safe",
            "check": lambda g: g.has_trait("gym_rat"),
            "player_check": lambda: getattr(store.Player, "_last_workout_day", -1) == store.Day,
            "drama_weight": 1,
            "tags": set(),
            "drink_reactions": {
                "gym_rat": ("happy", [
                    _("Obviously. Never miss a day."),
                    _("Leg day was brutal, but I survived."),
                ]),
                "nerd": ("embarrassed", [
                    _("I walked to the library... that counts, right?"),
                ]),
                "default": ("happy", [
                    _("Does walking fast to class count?"),
                ]),
            },
            "skip_reactions": {
                "gym_rat": ("surprised", [
                    _("Rest day. Even champions need recovery."),
                ]),
                "nerd": ("happy", [
                    _("Exercise? On purpose? No thanks."),
                ]),
                "default": ("normal", [
                    _("Not today... maybe tomorrow."),
                ]),
            },
        },
        {
            "id": "bought_useless_online",
            "text": _("...bought something completely useless online."),
            "category": "safe",
            "check": lambda g: not g.has_trait("poor"),
            "player_check": lambda: True,
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "rich": ("happy", [
                    _("Are you kidding? I do that like three times a day."),
                    _("My cart is always full of random stuff. No regrets."),
                ]),
                "poor": ("embarrassed", [
                    _("...once. And I still regret it."),
                ]),
                "default": ("happy", [
                    _("Who hasn't? Free shipping is dangerous."),
                    _("Late night shopping hits different."),
                ]),
            },
            "skip_reactions": {
                "poor": ("smirk", [
                    _("I only buy what I actually need."),
                    _("Some of us have to watch our budget."),
                ]),
                "rich": ("surprised", [
                    _("Wait, really? Not even once?"),
                    _("How?! I can't even go a week without buying something dumb."),
                ]),
                "default": ("surprised", [
                    _("Seriously? You have way more self-control than me."),
                ]),
            },
        },
        {
            "id": "got_f_grade",
            "text": _("...got an F on an exam."),
            "category": "safe",
            "check": lambda g: "F" in getattr(g, "grade_history", []),
            "player_check": lambda: "F" in getattr(store.Player, "grade_history", []),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "nerd": ("embarrassed", [
                    _("It was ONE time, okay?!"),
                    _("I don't want to talk about it..."),
                    _("I was going through something that week!"),
                ]),
                "gym_rat": ("happy", [
                    _("Who cares? I was too busy at the gym."),
                    _("Grades aren't gains. I know my priorities."),
                ]),
                "default": ("shy", [
                    _("Yeah... that was a rough week."),
                    _("I may have partied a little too hard before that one."),
                ]),
            },
            "skip_reactions": {
                "nerd": ("smirk", [
                    _("Never. My GPA is spotless."),
                    _("Some of us actually open our textbooks."),
                ]),
                "gym_rat": ("surprised", [
                    _("Wait... do I even check my grades?"),
                    _("Honestly? I have no idea what my grades are."),
                ]),
                "default": ("happy", [
                    _("Nope! Somehow I always scrape by."),
                ]),
            },
        },
        {
            "id": "fallen_asleep_class",
            "text": _("...fallen asleep in class."),
            "category": "safe",
            "check": lambda g: not g.has_trait("nerd"),
            "player_check": lambda: True,
            "drama_weight": 1,
            "tags": set(),
            "drink_reactions": {
                "nerd": ("embarrassed", [
                    _("It was ONE time! The professor was so boring."),
                ]),
                "gym_rat": ("happy", [
                    _("After leg day? Every time."),
                ]),
                "default": ("happy", [
                    _("Honestly, some classes are just free nap time."),
                ]),
            },
            "skip_reactions": {
                "nerd": ("smirk", [
                    _("I would never. Every lecture matters."),
                ]),
                "default": ("normal", [
                    _("Somehow I always stay awake. Barely."),
                ]),
            },
        },
        {
            "id": "cried_movie",
            "text": _("...cried during a movie."),
            "category": "safe",
            "check": lambda g: True,
            "player_check": lambda: True,
            "drama_weight": 1,
            "tags": set(),
            "drink_reactions": {
                "hardcore_sex": ("embarrassed", [
                    _("Shut up. It was a really sad movie, okay?"),
                ]),
                "cute_sex": ("happy", [
                    _("I cry at everything. Commercials, too."),
                ]),
                "default": ("shy", [
                    _("The ending just hit me, you know?"),
                ]),
            },
            "skip_reactions": {
                "hardcore_sex": ("smirk", [
                    _("I don't cry. Ever."),
                ]),
                "default": ("normal", [
                    _("I came close, but I held it together."),
                ]),
            },
        },
        {
            "id": "ate_cjohnson_hotdog",
            "text": _("...eaten a hot dog from C. Johnson's cart."),
            "category": "safe",
            "check": lambda g: True if g.has_trait("poor") else (False if g.has_trait("rich") else renpy.random.random() < 0.5),
            "player_check": lambda: getattr(store.Player, "_hotdog_count", 0) > 0,
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "poor": ("happy", [
                    _("Best deal on campus. I eat there every week."),
                    _("When you're on a budget, C. Johnson is a lifesaver."),
                ]),
                "rich": ("embarrassed", [
                    _("...once. And I regretted it immediately."),
                    _("I was desperate, okay? Never again."),
                ]),
                "default": ("happy", [
                    _("Those hot dogs hit different after a long day."),
                    _("C. Johnson is a campus legend. Of course I've eaten there."),
                ]),
            },
            "skip_reactions": {
                "poor": ("surprised", [
                    _("Wait, seriously? It's the cheapest food on campus!"),
                ]),
                "rich": ("smirk", [
                    _("I have standards. That cart is... questionable."),
                    _("Do you know what goes into those things? No thank you."),
                ]),
                "default": ("normal", [
                    _("Never tried it. Heard it's pretty good though."),
                    _("Same here. Maybe one day."),
                ]),
            },
        },

        # ======================== LEWD ========================

        {
            "id": "kissed_in_room",
            "text": _("...kissed someone in this room."),
            "category": "lewd",
            "check": lambda g: "kiss" in getattr(g, "intimacy_flags", set()),
            "player_check": lambda: any("kiss" in getattr(g, "intimacy_flags", set()) for g in _hangout_girls_list()),
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "_gf": ("shy", [
                    _("...yeah. And it was really nice."),
                    _("You already know who."),
                ]),
                "cute_sex": ("shy", [
                    _("It was really sweet, actually."),
                ]),
                "exhibitionist": ("smirk", [
                    _("And I'd do it again right now."),
                ]),
                "default": ("shy", [
                    _("...yeah. Not saying who, though."),
                    _("Guilty. But I'm not giving names."),
                ]),
            },
            "skip_reactions": {
                "cute_sex": ("shy", [
                    _("Not yet..."),
                ]),
                "exhibitionist": ("smirk", [
                    _("The night is young."),
                ]),
                "default": ("normal", [
                    _("Nope. Not yet."),
                ]),
            },
        },
        {
            "id": "sexy_photo",
            "text": _("...sent a sexy photo of myself to someone."),
            "category": "lewd",
            # Real data: she sent the player a phone photo; traits cover "someone else"
            "check": lambda g: _nhie_girl_sent_photo(g) or g.has_trait("camera_lover") or g.has_trait("exhibitionist"),
            "player_check": lambda: False,
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "camera_lover": ("smirk", [
                    _("I look good. Why not share?"),
                    _("I have a whole folder. Don't judge me."),
                ]),
                "exhibitionist": ("smirk", [
                    _("I love the attention. Sue me."),
                ]),
                "public_shy": ("embarrassed", [
                    _("It was for someone special, okay? No one else saw it."),
                ]),
                "camera_hater": ("embarrassed", [
                    _("I was pressured into it... never again."),
                ]),
                "default": ("shy", [
                    _("It was a one-time thing. I was feeling bold."),
                ]),
            },
            "skip_reactions": {
                "camera_lover": ("surprised", [
                    _("Really? Never? Not even one?"),
                ]),
                "camera_hater": ("normal", [
                    _("Never. My photos are mine."),
                ]),
                "default": ("normal", [
                    _("Nah, too risky."),
                ]),
            },
        },
        {
            "id": "sent_dick_pic",
            "text": _("...sent or received an unsolicited nude."),
            "category": "lewd",
            "check": lambda g: getattr(g, "_dick_pics_received", 0) > 0,
            "player_check": lambda: any(getattr(g, "_dick_pics_received", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "public_shy": ("embarrassed", [
                    _("I didn't ask for it! It just... appeared on my phone."),
                ]),
                "exhibitionist": ("smirk", [
                    _("Got one. Didn't mind it, honestly."),
                ]),
                "default": ("uncomfortable", [
                    _("Yeah... that happened. Not my favorite memory."),
                ]),
            },
            "skip_reactions": {
                "public_shy": ("happy", [
                    _("Thank god, no."),
                ]),
                "default": ("normal", [
                    _("Nope. Lucky me."),
                ]),
            },
        },
        {
            "id": "fantasized_here",
            "text": _("...fantasized about someone in this room."),
            "category": "lewd",
            "check": lambda g: g.Love > 400 or g.Lust > 30,
            "player_check": lambda: True,
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "_gf": ("shy", [
                    _("...obviously. You know who."),
                ]),
                "cute_sex": ("shy", [
                    _("...it's hard not to when they're this close."),
                ]),
                "exhibitionist": ("smirk", [
                    _("More than once, honestly."),
                ]),
                "default": ("shy", [
                    _("...guilty. Next question."),
                ]),
            },
            "skip_reactions": {
                "default": ("normal", [
                    _("Nope. Totally focused on the game."),
                ]),
            },
        },
        {
            "id": "liked_spanking",
            "text": _("...enjoyed being spanked, or spanking someone."),
            "category": "lewd",
            # hardcore_sex drinks on the trait alone only when her sex life predates the player: rough sex before him
            # (_nhie_hardcore_before_player). Anyone else, a girl he deflowered included, only on a spank she really
            # enjoyed (_nhie_liked_spanking, her SpankLog). The player: anyone he spanked (_nhie_spanked). Never
            # Slaps: that counts HER slapping the player for a lewd flirt, not a spanking
            "check": lambda g: _nhie_hardcore_before_player(g) or _nhie_liked_spanking(g),
            "player_check": lambda: any(_nhie_spanked(g) for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "hardcore_sex": ("smirk", [
                    _("What? It feels good. Don't judge me."),
                    _("Harder is better. I said what I said."),
                ]),
                "cute_sex": ("embarrassed", [
                    _("I... didn't think I'd like it, but..."),
                    _("It just... happened. And I didn't hate it."),
                ]),
                "default": ("shy", [
                    _("Okay, fine. Maybe I liked it a little."),
                ]),
            },
            "skip_reactions": {
                # femdom first (docs/plan_femdom.md 7): she would be the one doing the spanking
                "femdom": ("smirk", [
                    _("Not yet. But I already know whose ass I'd pick."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Not yet... but I'd like to find out."),
                ]),
                "cute_sex": ("happy", [
                    _("Yeah, that's not really my thing."),
                ]),
                "default": ("neutral", [
                    _("Nope. Not my style."),
                ]),
            },
        },
        {
            "id": "touched_self_thinking",
            "text": _("...touched myself thinking about someone in this room."),
            "category": "lewd",
            "check": lambda g: g.Love > 500 or getattr(g, "Sex_acts", {}).get("masturbate", 0) > 0,
            "player_check": lambda: True,
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "cum_slut": ("smirk", [
                    _("What? They're hot. Can you blame me?"),
                ]),
                "cute_sex": ("embarrassed", [
                    _("Please don't look at me right now..."),
                ]),
                "exhibitionist": ("smirk", [
                    _("And I don't regret it one bit."),
                ]),
                "default": ("embarrassed", [
                    _("...next question, please."),
                    _("Yeah... I'm not explaining this one."),
                ]),
            },
            "skip_reactions": {
                "default": ("normal", [
                    _("Can't say I have."),
                ]),
            },
        },
        {
            "id": "received_oral",
            "text": _("...had someone go down on me."),
            "category": "lewd",
            # Exposure["lick_pussy"] is never incremented — cunnilingus is tracked in Sex_acts["oral"]
            "check": lambda g: getattr(g, "Sex_acts", {}).get("oral", 0) > 0,
            # Player: literally received oral (a blowjob)
            "player_check": lambda: any("bj" in getattr(g, "intimacy_flags", set()) for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                # femdom first (docs/plan_femdom.md 7): oral on her is hers to command
                "femdom": ("smug", [
                    _("Obviously. And I decided when it was good enough."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Obviously. And I loved it."),
                ]),
                "cute_sex": ("shy", [
                    _("It was... really nice, actually."),
                ]),
                "default": ("shy", [
                    _("...yeah. Moving on."),
                ]),
            },
            "skip_reactions": {
                "femdom": ("smirk", [
                    _("Not yet. Someone will have to earn that privilege."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Not yet. Somebody should fix that."),
                ]),
                "default": ("normal", [
                    _("Not yet."),
                ]),
            },
        },
        {
            "id": "walked_in_changing",
            "text": _("...been walked in on while getting changed."),
            "category": "lewd",
            # Shower walk-ins are tracked both ways: player walked in on her / she walked in on him
            "check": lambda g: g.GetActionCount("player_walked_in_shower") > 0 if hasattr(g, "GetActionCount") else False,
            "player_check": lambda: any(g.GetActionCount("girl_walked_in_shower") > 0 for g in ALL_GIRLS if hasattr(g, "GetActionCount")),
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "exhibitionist": ("smirk", [
                    _("I may or may not have left the door unlocked on purpose."),
                ]),
                "public_shy": ("embarrassed", [
                    _("I screamed so loud. It was awful."),
                ]),
                "default": ("shy", [
                    _("It was so awkward. We just stared at each other."),
                ]),
            },
            "skip_reactions": {
                "public_shy": ("happy", [
                    _("I always lock the door. Always."),
                ]),
                "default": ("normal", [
                    _("Nope. I'm careful about that."),
                ]),
            },
        },
        {
            "id": "slept_same_bed",
            "text": _("...shared a bed with someone and pretended nothing happened."),
            "category": "lewd",
            # "sleepover" was never added to intimacy_flags — sleepovers register the "slept_together" action
            "check": lambda g: (g.GetActionCount("slept_together") > 0 if hasattr(g, "GetActionCount") else False) or renpy.random.random() < 0.3,
            "player_check": lambda: any(g.GetActionCount("slept_together") > 0 for g in ALL_GIRLS if hasattr(g, "GetActionCount")),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "cute_sex": ("shy", [
                    _("We just cuddled. It was really sweet, actually."),
                ]),
                "exhibitionist": ("smirk", [
                    _("And it didn't stay 'just sleeping' for long."),
                ]),
                "default": ("shy", [
                    _("We both pretended we didn't notice anything."),
                ]),
            },
            "skip_reactions": {
                "default": ("normal", [
                    _("I keep my bed to myself."),
                ]),
            },
        },

        # ======================== SEXUAL ========================

        {
            "id": "sex_no_condom",
            "text": _("...had sex without a condom."),
            "category": "sexual",
            "check": lambda g: getattr(g, "raw_sex_count", 0) > 0,
            "player_check": lambda: any(getattr(g, "raw_sex_count", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "_gf_cum_slut": ("smirk", [
                    _("Raw feels so much better. Right, babe?"),
                    _("And it was totally worth it."),
                ]),
                "cum_slut": ("smirk", [
                    _("Raw is the only way. No comparison."),
                    _("Condoms ruin everything. I said what I said."),
                ]),
                "cum_slut_new": ("shy", [
                    _("It felt so much better than I thought it would."),
                    _("I didn't plan it... but I don't regret it at all."),
                ]),
                "hate_cum": ("worried", [
                    _("He swore he'd be careful. I was so stressed the whole time."),
                ]),
                "default": ("embarrassed", [
                    _("It just... happened in the moment. Bad decision."),
                    _("Yeah... not my smartest choice."),
                ]),
            },
            "skip_reactions": {
                "cum_slut": ("shy", [
                    _("Not yet... but I think about it more than I should."),
                ]),
                "hate_cum": ("smirk", [
                    _("Never. I don't take chances."),
                ]),
                "default": ("normal", [
                    _("Nope. Safety first."),
                ]),
            },
        },
        {
            "id": "cum_inside",
            "text": _("...let someone finish inside me, or finished inside someone."),
            "category": "sexual",
            "check": lambda g: getattr(g, "CreampieCounts", 0) > 0,
            "player_check": lambda: any(getattr(g, "CreampieCounts", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "_gf_cum_slut": ("smirk", [
                    _("That's why we're so good together."),
                    _("And I'd let him do it again. Every time."),
                ]),
                "_gf": ("shy", [
                    _("...yeah. With someone special."),
                    _("Don't look at me like that. It was worth it."),
                ]),
                "cum_slut": ("smirk", [
                    _("Best feeling ever. I said what I said."),
                    _("I love that feeling. No shame."),
                ]),
                "cum_slut_new": ("shy", [
                    _("...Yeah. And I liked it way more than I thought I would."),
                    _("I didn't expect to like that feeling so much. I really did."),
                ]),
                "hate_cum": ("angry", [
                    _("He didn't pull out in time. I was furious."),
                    _("I'm still mad about it, honestly."),
                ]),
                "default": ("embarrassed", [
                    _("It just... happened. In the heat of the moment."),
                    _("We got carried away. Not my proudest moment."),
                ]),
            },
            "skip_reactions": {
                "cum_slut": ("shy", [
                    _("Never... but I kind of want to know what it feels like."),
                ]),
                "hate_cum": ("disgusted", [
                    _("Absolutely not. That's disgusting."),
                ]),
                "default": ("normal", [
                    _("No way. Too risky."),
                ]),
            },
        },
        {
            "id": "sex_in_public",
            "text": _("...had sex in public."),
            "category": "sexual",
            "check": lambda g: getattr(g, "CorruptionPublicHeavyActs", 0) > 0,
            "player_check": lambda: any(getattr(g, "CorruptionPublicHeavyActs", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "public_fetish": ("smirk", [
                    _("The thrill is what makes it good."),
                    _("Getting caught is half the fun."),
                ]),
                "exhibitionist": ("smirk", [
                    _("I love the rush. Nothing beats it."),
                ]),
                "public_shy": ("embarrassed", [
                    _("We almost got caught. My heart was pounding the entire time."),
                ]),
                "default": ("shy", [
                    _("It was spontaneous... and terrifying."),
                    _("I kept looking around the whole time."),
                ]),
            },
            "skip_reactions": {
                "public_fetish": ("smirk", [
                    _("Not yet... but I've definitely thought about it."),
                ]),
                "public_shy": ("worried", [
                    _("God, no. I'd die of embarrassment."),
                ]),
                "default": ("normal", [
                    _("Nope. I like walls and doors, thanks."),
                ]),
            },
        },
        {
            "id": "sex_three_times_day",
            "text": _("...had sex more than three times in one day."),
            "category": "sexual",
            # Real per-day data from Sex_act_locations (was a lifetime-total proxy)
            "check": lambda g: _nhie_max_sex_in_one_day(g) > 3,
            "player_check": lambda: _nhie_player_max_sex_in_one_day() > 3,
            "drama_weight": 2,
            "tags": set(),
            "drink_reactions": {
                "cum_slut": ("smirk", [
                    _("Honestly? That was a good day."),
                    _("I could've gone for more."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("What? Sometimes you're just in the mood all day."),
                ]),
                "default": ("embarrassed", [
                    _("That was... an intense day."),
                    _("We just couldn't stop. Don't judge me."),
                ]),
            },
            "skip_reactions": {
                "cum_slut": ("surprised", [
                    _("Three times? In one day? ...Impressive."),
                ]),
                "default": ("normal", [
                    _("That sounds exhausting."),
                ]),
            },
        },
        {
            "id": "atm",
            "text": _("...gone from anal to... something else oral."),
            "category": "sexual",
            "check": lambda g: getattr(g, "_atm_count", 0) > 0,
            "player_check": lambda: any(getattr(g, "_atm_count", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "cum_slut": ("smirk", [
                    _("What? It was hot."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Don't knock it till you try it."),
                ]),
                "anal_lover": ("embarrassed", [
                    _("...it just kind of happened."),
                ]),
                "anal_lover_new": ("embarrassed", [
                    _("...it just kind of happened."),
                ]),
                "default": ("embarrassed", [
                    _("I don't want to talk about it."),
                ]),
            },
            "skip_reactions": {
                "anal_hater": ("disgusted", [
                    _("That is absolutely disgusting."),
                    _("I would literally never."),
                ]),
                "hate_cum": ("disgusted", [
                    _("Ew. No. Just no."),
                ]),
                "default": ("normal", [
                    _("Hard pass on that one."),
                ]),
            },
        },
        {
            "id": "recorded_sex_video",
            "text": _("...recorded a sex video."),
            "category": "sexual",
            "check": lambda g: any(v.get("girl_gid") == g.gid for v in getattr(store.Player, "recorded_videos", [])),
            "player_check": lambda: len(getattr(store.Player, "recorded_videos", [])) > 0,
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "camera_lover": ("smirk", [
                    _("I looked great in it, too."),
                    _("I wanted to make sure we'd remember that night."),
                ]),
                "exhibitionist": ("smirk", [
                    _("And I'd do it again. No regrets."),
                ]),
                "camera_hater": ("embarrassed", [
                    _("He talked me into it... I kind of regret it."),
                ]),
                "default": ("shy", [
                    _("It was a mutual decision. Still makes me nervous though."),
                    _("Yeah... that exists somewhere. Let's move on."),
                ]),
            },
            "skip_reactions": {
                "camera_hater": ("angry", [
                    _("Never. I don't trust anyone with that."),
                ]),
                "camera_lover": ("surprised", [
                    _("Not yet... but I'm not against it."),
                ]),
                "default": ("normal", [
                    _("No way. Too much risk."),
                ]),
            },
        },
        {
            "id": "had_threesome",
            "text": _("...had a threesome."),
            "category": "sexual",
            "check": lambda g: any(g.get_history_with(og.gid, "threesome") > 0 for og in ALL_GIRLS if og.gid != g.gid),
            "player_check": lambda: any(any(g.get_history_with(og.gid, "threesome") > 0 for og in ALL_GIRLS if og.gid != g.gid) for g in ALL_GIRLS),
            "drama_weight": 5,
            "tags": set(),
            "drink_reactions": {
                "exhibitionist": ("smirk", [
                    _("Best night of my life, honestly."),
                    _("Why limit yourself to one person?"),
                ]),
                "default": ("embarrassed", [
                    _("Okay... yeah. That happened."),
                    _("It was a one-time thing... I think."),
                ]),
            },
            "skip_reactions": {
                "exhibitionist": ("smirk", [
                    _("Not yet. But I'm not saying never."),
                ]),
                "loyal": ("normal", [
                    _("No. I don't share."),
                ]),
                "default": ("normal", [
                    _("Nope. That's a lot to coordinate."),
                ]),
            },
        },
        {
            "id": "enjoyed_anal",
            "text": _("...enjoyed anal more than I expected."),
            "category": "sexual",
            # anal_lover drinks on the trait only once she has had anal: with the player, with her partner or before
            # (experienced / past discovering it). A virgin who loves the IDEA has nothing to confess yet
            "check": lambda g: (g.has_trait("anal_lover") and (getattr(g, "Sex_acts", {}).get("anal", 0) > 0 or not trait_is_new(g, "anal_lover")))
                               or getattr(g, "Sex_acts", {}).get("anal", 0) > 3,
            "player_check": lambda: any(getattr(g, "Sex_acts", {}).get("anal", 0) > 3 for g in ALL_GIRLS),
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "anal_lover": ("smirk", [
                    _("More than expected? I expected to love it, and I did."),
                    _("What can I say... some things just feel right."),
                ]),
                "anal_lover_new": ("embarrassed", [
                    _("Way more than I expected... I'm still a little surprised."),
                    _("I didn't think I'd like it. I really, really did."),
                ]),
                "anal_hater": ("embarrassed", [
                    _("I... okay, maybe once. But I'm not doing that again."),
                ]),
                "default": ("shy", [
                    _("It surprised me, okay? Don't look at me like that."),
                    _("I didn't plan it... it just kind of happened."),
                ]),
            },
            "skip_reactions": {
                "anal_hater": ("angry", [
                    _("Absolutely not. Never happening."),
                    _("That's a hard no. Forever."),
                ]),
                "anal_lover": ("surprised", [
                    _("Wait... why are you looking at me?"),
                ]),
                "default": ("neutral", [
                    _("Haven't tried, don't plan to."),
                ]),
            },
        },
        {
            "id": "cum_on_face",
            "text": _("...had someone finish on my face, or finished on someone's face."),
            "category": "sexual",
            "check": lambda g: getattr(g, "CumLog", {}).get("face", 0) > 0,
            "player_check": lambda: any(getattr(g, "CumLog", {}).get("face", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "cum_slut": ("smirk", [
                    _("And I'd do it again."),
                    _("What? It's hot."),
                ]),
                "hate_cum": ("angry", [
                    _("He didn't warn me. I'm still mad about it."),
                ]),
                "default": ("embarrassed", [
                    _("It was... an experience. Let's leave it at that."),
                ]),
            },
            "skip_reactions": {
                "cum_slut": ("smirk", [
                    _("Not yet... but I wouldn't say no."),
                ]),
                "hate_cum": ("disgusted", [
                    _("God, no. That sounds awful."),
                ]),
                "default": ("normal", [
                    _("Nope. And I'm fine with that."),
                ]),
            },
        },
        {
            "id": "forced_swallow",
            "text": _("...been forced to swallow, or forced someone to."),
            "category": "sexual",
            "check": lambda g: getattr(g, "ForcedSwallowCounts", 0) > 0,
            "player_check": lambda: any(getattr(g, "ForcedSwallowCounts", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "cum_slut": ("smirk", [
                    _("'Forced' is a strong word... I didn't exactly fight it."),
                ]),
                "hate_cum": ("angry", [
                    _("Don't even get me started. That was disgusting."),
                    _("I almost threw up. Never again."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("It was kind of hot, actually."),
                ]),
                "default": ("embarrassed", [
                    _("I... didn't really have a choice in the moment."),
                ]),
            },
            "skip_reactions": {
                # femdom first (docs/plan_femdom.md 7): nobody forces her
                "femdom": ("smirk", [
                    _("Nobody forces me to do anything. It works the other way around."),
                ]),
                "hate_cum": ("disgusted", [
                    _("If anyone tried that with me, they'd regret it."),
                ]),
                "cum_slut": ("smirk", [
                    _("'Forced'? I'd volunteer."),
                ]),
                "default": ("normal", [
                    _("No. And I'd like to keep it that way."),
                ]),
            },
        },
        {
            "id": "lost_virginity",
            "text": _("...lost my virginity."),
            "category": "sexual",
            "check": lambda g: not g.has_trait("virgin"),
            "player_check": lambda: True,
            "drama_weight": 4,
            "tags": set(),
            "drink_reactions": {
                "cute_sex": ("shy", [
                    _("It was special. I don't regret it."),
                    _("It was with someone I cared about."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Finally got it over with. Best decision ever."),
                ]),
                "default": ("shy", [
                    _("Yeah... it happened. No details."),
                ]),
            },
            "skip_reactions": {
                "virgin": ("embarrassed", [
                    _("...can we move on?"),
                    _("I'm waiting for the right person, okay?"),
                ]),
                "default": ("normal", [
                    _("Nope."),
                ]),
            },
        },
        {
            "id": "took_virginity",
            "text": _("...been someone's first time."),
            "category": "sexual",
            "check": lambda g: False,
            "player_check": lambda: any(getattr(g, "virginity_taken_by_player", False) for g in ALL_GIRLS),
            "drama_weight": 3,
            "tags": set(),
        },

        # ======================== NUCLEAR ========================

        {
            "id": "cheated_partner",
            "text": _("...cheated on my partner."),
            "category": "nuclear",
            "check": lambda g: getattr(g, "CheatMaxTier", 0) > 0,
            # Player cheated on HIS girlfriend (PlayerCheatCount = times he cheated WITH that girl)
            "player_check": lambda: _nhie_player_cheated(),
            "drama_weight": 5,
            # No needs_bf: without her partner present, drinking reveals she HAS one
            # (player: "She is dating someone" banner; girls: girl_learns_has_bf).
            # With him present it becomes a confession to his face (suspicion +30).
            "tags": set(),
            "drink_reactions": {
                "cheater": ("smirk", [
                    _("It is what it is."),
                    _("I don't feel that bad about it, honestly."),
                ]),
                "loyal": ("embarrassed", [
                    _("I felt terrible. I still do."),
                    _("It was the worst mistake I've made."),
                ]),
                "default": ("embarrassed", [
                    _("...I'm not proud of it."),
                    _("Can we not dwell on this one?"),
                ]),
            },
            "skip_reactions": {
                "cheater": ("smirk", [
                    _("Not technically, no."),
                ]),
                "loyal": ("normal", [
                    _("Never. I'd never do that to someone."),
                ]),
                "default": ("normal", [
                    _("No. I couldn't live with myself."),
                ]),
            },
        },
        {
            "id": "sex_for_money",
            "text": _("...done something sexual for money, or paid someone to."),
            "category": "nuclear",
            "check": lambda g: getattr(g, "_financial_times", 0) > 0,
            "player_check": lambda: any(getattr(g, "_financial_times", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 5,
            "tags": set(),
            "drink_reactions": {
                "poor": ("embarrassed", [
                    _("I needed the money... it was a rough month."),
                    _("When you're broke, you do what you have to."),
                ]),
                "rich": ("embarrassed", [
                    _("It wasn't about the money... it's complicated."),
                ]),
                "default": ("embarrassed", [
                    _("I'd rather not get into it."),
                    _("...yeah. Let's move on."),
                ]),
            },
            "skip_reactions": {
                "poor": ("normal", [
                    _("Even when I'm broke, I have limits."),
                ]),
                "default": ("normal", [
                    _("No, and I never would."),
                ]),
            },
        },
        {
            "id": "been_blackmailed",
            "text": _("...been blackmailed, or blackmailed someone."),
            "category": "nuclear",
            # She WAS blackmailed (_nhie_blackmailed): she gave in (_blackmail_times) or told him to post it
            # (_blackmail_refused, blackmail_note_refused). A girl who only ever refused speaks from
            # drink_reactions_refused (drink_variant): nobody used her secrets, it was no "scary time in her life".
            # A skip line only plays when nobody ever tried
            "check": lambda g: _nhie_blackmailed(g),
            "player_check": lambda: any(_nhie_blackmailed(g) for g in ALL_GIRLS),
            "drink_variant": lambda g: "refused" if _nhie_blackmail_refused_only(g) else None,
            "drama_weight": 5,
            "tags": set(),
            "drink_reactions": {
                "loyal": ("angry", [
                    _("Someone used my secrets against me. It was horrible."),
                ]),
                "hardcore_sex": ("angry", [
                    _("Yeah. And?"),
                ]),
                "default": ("worried", [
                    _("...it was a really scary time in my life."),
                    _("I don't like talking about it."),
                ]),
            },
            "drink_reactions_refused": {
                "hardcore_sex": ("angry", [
                    _("They tried. I told them to go to hell."),
                ]),
                "default": ("worried", [
                    _("I don't like talking about it."),
                ]),
            },
            "skip_reactions": {
                "loyal": ("worried", [
                    _("God, that's terrifying. I hope that never happens to me."),
                ]),
                "hardcore_sex": ("smirk", [
                    _("Anyone who tries that with me would regret it."),
                ]),
                "default": ("normal", [
                    _("No, thankfully."),
                ]),
            },
        },
        {
            "id": "same_sex_curious",
            "text": _("...been curious about being with someone of the same sex."),
            "category": "nuclear",
            "check": lambda g: g.has_trait("bisexual") or g.has_trait("lesbian"),
            "player_check": lambda: False,
            "drama_weight": 3,
            "tags": set(),
            "drink_reactions": {
                "lesbian": ("smirk", [
                    _("Curious? I'm way past curious."),
                    _("That's putting it mildly."),
                ]),
                "exhibitionist": ("smirk", [
                    _("What? People are attractive. All kinds."),
                ]),
                "default": ("shy", [
                    _("...maybe a little. Is that weird?"),
                    _("I've thought about it. That's all I'll say."),
                ]),
            },
            "skip_reactions": {
                "default": ("normal", [
                    _("Not really, no."),
                ]),
            },
        },
        {
            "id": "recorded_without_consent",
            "text": _("...recorded someone without their knowledge, or been recorded without knowing."),
            "category": "nuclear",
            "check": lambda g: any(v.get("subject") == "self" and not v.get("consensual", True) for v in getattr(g, "video_seen_history", [])),
            "player_check": lambda: any(not v.get("consensual", True) for v in getattr(store.Player, "recorded_videos", [])),
            "drama_weight": 5,
            "tags": set(),
            "drink_reactions": {
                "camera_hater": ("angry", [
                    _("Someone recorded me without asking. I'm still furious."),
                    _("If I ever find out who did it... they'll regret it."),
                    _("I found that video and I wanted to scream."),
                ]),
                "camera_lover": ("embarrassed", [
                    _("Someone recorded me without asking... honestly, I didn't hate the result."),
                    _("I mean... was the angle at least good?"),
                ]),
                "default": ("uncomfortable", [
                    _("Yeah... it happened. I don't really want to talk about it."),
                    _("Finding that out was... not a great day."),
                    _("I still don't know how to feel about it."),
                ]),
            },
            "skip_reactions": {
                "camera_hater": ("disgusted", [
                    _("If anyone ever did that to me, I'd destroy their phone."),
                    _("That's disgusting. I'd never forgive someone for that."),
                ]),
                "camera_lover": ("surprised", [
                    _("At least ask first, you know?"),
                ]),
                "default": ("worried", [
                    _("No, thank god."),
                    _("That would be such a violation of trust."),
                ]),
            },
        },
        {
            "id": "paid_for_sex",
            "text": _("...paid someone for sex."),
            "category": "nuclear",
            "check": lambda g: False,
            "player_check": lambda: any(getattr(g, "_financial_times", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 4,
            "tags": {"player_only"},
        },
        {
            "id": "dated_multiple",
            "text": _("...been in a relationship with more than one person at the same time."),
            "category": "nuclear",
            "check": lambda g: g.is_dating_player() and len([og for og in ALL_GIRLS if og.gid != g.gid and og.is_dating_player()]) > 0,
            "player_check": lambda: len([g for g in ALL_GIRLS if g.is_dating_player()]) > 1,
            "drama_weight": 5,
            "tags": set(),
            "drink_reactions": {
                "cheater": ("smirk", [
                    _("They didn't need to know about each other."),
                    _("What? I was young. Kind of."),
                ]),
                "loyal": ("embarrassed", [
                    _("I'm not proud of it. I hurt people."),
                ]),
                "default": ("embarrassed", [
                    _("It was a mess. I don't recommend it."),
                ]),
            },
            "skip_reactions": {
                "loyal": ("normal", [
                    _("Never. One person is enough."),
                ]),
                "default": ("normal", [
                    _("No, I can barely handle one relationship."),
                ]),
            },
        },
        {
            "id": "ntr_watched",
            "text": _("...let my partner watch me with someone else."),
            "category": "nuclear",
            "check": lambda g: getattr(g, "_ntr_active", False),
            "player_check": lambda: False,   # "my partner watch me" is her side of NTR
            "drama_weight": 5,
            "tags": {"needs_bf"},
            "drink_reactions": {
                "voyeur": ("smirk", [
                    _("It was his idea, but... I liked it too."),
                ]),
                "exhibitionist": ("smirk", [
                    _("Knowing someone was watching made it so much better."),
                ]),
                "default": ("embarrassed", [
                    _("It's... complicated. But yeah."),
                    _("We have an arrangement. That's all I'll say."),
                ]),
            },
            "skip_reactions": {
                "voyeur": ("surprised", [
                    _("Not from that side, no."),
                ]),
                "default": ("normal", [
                    _("No way. That's way too much."),
                ]),
            },
        },
        {
            "id": "stolen_partner",
            "text": _("...taken someone away from their partner on purpose."),
            "category": "nuclear",
            "check": lambda g: False,
            # Set when a girl dumps her NPC partner because of the player (interactions/npc_partner breakup paths)
            "player_check": lambda: any(getattr(g, "_left_partner_for_player", False) for g in ALL_GIRLS),
            "drama_weight": 5,
            "tags": {"player_only"},
        },
        {
            "id": "lied_protection",
            "text": _("...lied about using protection."),
            "category": "nuclear",
            "check": lambda g: False,
            # Incremented in _condom_stealth_success (StealthCondom.rpy) — condom removed without her knowing
            "player_check": lambda: any(getattr(g, "_stealth_condom_count", 0) > 0 for g in ALL_GIRLS),
            "drama_weight": 5,
            "tags": {"player_only"},
        },
    ]

    # ------------------------------------------------------------------
    # FILTERING & PICKING
    # ------------------------------------------------------------------

    def _nhie_player_cheated(min_count=1):
        """True if the player has cheated on his girlfriend at least min_count times.
        girl.PlayerCheatCount = times the player cheated on his GF WITH that girl
        (incremented by inc_player_cheat)."""
        _total = 0
        for _g in ALL_GIRLS:
            _total += int(getattr(_g, "PlayerCheatCount", 0) or 0)
        return _total >= min_count

    # Sex_act_locations entries: {"act", "location", "day", "method"}.
    # _scene_escalation() logs one "sex" entry per penetration session
    # (plus the position name), so "sex" entries per day == sessions per day.
    _NHIE_INTIMATE_ACTS = ("sex", "bj", "hj", "tj", "oral", "anal")

    def _nhie_days_with_acts(girl, acts):
        """{day: count} of logged acts (from `acts`) for this girl."""
        _d = {}
        for _h in getattr(girl, "Sex_act_locations", None) or []:
            if _h.get("act") in acts:
                _day = _h.get("day", 0)
                _d[_day] = _d.get(_day, 0) + 1
        return _d

    def _nhie_max_sex_in_one_day(girl):
        _d = _nhie_days_with_acts(girl, ("sex",))
        return max(_d.values()) if _d else 0

    def _nhie_player_max_sex_in_one_day():
        _tot = {}
        for _g in ALL_GIRLS:
            for _day, _n in _nhie_days_with_acts(_g, ("sex",)).items():
                _tot[_day] = _tot.get(_day, 0) + _n
        return max(_tot.values()) if _tot else 0

    def _nhie_player_two_girls_same_day():
        """True if the player was intimate with 2+ different girls on the same day."""
        _by_day = {}
        for _g in ALL_GIRLS:
            for _day in _nhie_days_with_acts(_g, _NHIE_INTIMATE_ACTS).keys():
                _by_day.setdefault(_day, set()).add(_g.gid)
        return any(len(_s) >= 2 for _s in _by_day.values())

    def _nhie_partner_present(girl):
        """True if this girl's NPC partner is at the hangout right now."""
        if not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
            return False
        if not _npc_is_active():
            return False
        return getattr(store._h_npc, "girl_gid", None) == girl.gid

    def _nhie_girl_sent_photo(girl):
        """She sent the player a photo via the phone photo system."""
        for _p in getattr(store.Player, "received_photos", None) or []:
            if _p.get("girl_gid") == girl.gid:
                return True
        return False

    # liked_spanking. Her spank record (girl.SpankLog, SubEvents.rpy spank_note): every ASS spank she took, light or
    # heavy (SpankHer, the Truth or Dare spank dares, the pillow refusal, his flirt slap; never a face slap), who gave
    # it and whether she enjoyed it then, plus the ones she gave in the girl-on-girl dare ("given_enjoyed").
    # None = a save older than the record: the legacy reading, her heavy spank days
    # (CorruptionHeavySpankDays, all his) liked per spank_enjoyed (SpankHer's reaction for her traits)

    def _nhie_hardcore_before_player(girl):
        """hardcore_sex whose sex life predates the player (experienced, or not deflowered by him): rough sex before
        him to confess. A girl he deflowered (or a virgin) has only her spank record."""
        if not girl.has_trait("hardcore_sex"):
            return False
        _before = trait_is_veteran(girl, "hardcore_sex") and not getattr(girl, "virginity_taken_by_player", False)
        print("[NHIE] liked_spanking %s: hardcore_sex, sex life before the player=%s" % (girl.gid, _before))
        return _before

    def _nhie_spanked(girl):
        """The player spanked her (old save: at least one heavy spank day)."""
        _log = getattr(girl, "SpankLog", None)
        if _log is None:
            return int(getattr(girl, "CorruptionHeavySpankDays", 0) or 0) > 0
        return _log.get("by_player", 0) > 0

    def _nhie_liked_spanking(girl):
        """She enjoyed a spank she took, or one she gave (old save: spanked, and SpankHer's reaction for her traits
        is pleasure)."""
        _log = getattr(girl, "SpankLog", None)
        if _log is None:
            _liked = _nhie_spanked(girl) and spank_enjoyed(girl)
        else:
            _liked = _log.get("enjoyed", 0) > 0 or _log.get("given_enjoyed", 0) > 0
        print("[NHIE] liked_spanking %s: record=%s (legacy heavy spank days %d) -> liked=%s" % (
            girl.gid, _log, int(getattr(girl, "CorruptionHeavySpankDays", 0) or 0), _liked))
        return _liked

    # been_blackmailed. The blackmails she gave in to (_blackmail_times) and the ones she refused (_blackmail_refused,
    # interactions.rpy blackmail_note_refused)
    def _nhie_blackmailed(girl):
        """Someone blackmailed her: she gave in, or she refused."""
        return (int(getattr(girl, "_blackmail_times", 0) or 0) > 0
                or int(getattr(girl, "_blackmail_refused", 0) or 0) > 0)

    def _nhie_blackmail_refused_only(girl):
        """She was blackmailed and never gave in: every attempt ended in her refusal."""
        return (int(getattr(girl, "_blackmail_times", 0) or 0) == 0
                and int(getattr(girl, "_blackmail_refused", 0) or 0) > 0)

    # ------------------------------------------------------------------
    # SAVE SAFETY (pickle)
    # Statement entries carry lambdas ("check" / "player_check" / "drink_variant"). Any store
    # variable bound in label code (_nhie_stmt, _nhie_all_items, loop vars) is
    # pickled on save, and lambdas cannot be pickled ("Can't pickle <lambda>").
    # Label code must only hold PUBLIC copies (_nhie_public, callables stripped);
    # callables are resolved by id (_nhie_full / NHIE_BY_ID) at check time.
    # ------------------------------------------------------------------
    NHIE_BY_ID = {s["id"]: s for s in NHIE_STATEMENTS}

    def _nhie_public(stmt):
        """Picklable copy of a statement (top-level callables stripped)."""
        if stmt is None:
            return None
        return {k: v for k, v in stmt.items() if not callable(v)}

    def _nhie_full(stmt):
        """Registry entry (with callables) for a public copy; falls back to arg."""
        if stmt is None:
            return None
        return NHIE_BY_ID.get(stmt.get("id"), stmt)

    def _nhie_available(used_ids, drunk_level, has_npc, for_who="any"):
        out = []
        for s in NHIE_STATEMENTS:
            if s["id"] in used_ids:
                continue
            gate = NHIE_CATEGORY_GATES.get(s["category"], 0)
            if drunk_level < gate:
                continue
            _tags = s.get("tags", set())
            if "needs_bf" in _tags and not has_npc:
                continue
            if "player_only" in _tags and for_who != "player":
                continue
            if for_who == "npc" and "player_only" in _tags:
                continue
            out.append(s)
        return out

    def _nhie_player_menu_items(used_ids, has_npc, drunk_level):
        """Return ALL unused player-eligible statements as (stmt, is_locked), sorted by category."""
        items = []
        for s in NHIE_STATEMENTS:
            if s["id"] in used_ids:
                continue
            _tags = s.get("tags", set())
            if "needs_bf" in _tags and not has_npc:
                continue
            gate = NHIE_CATEGORY_GATES.get(s["category"], 0)
            locked = drunk_level < gate
            items.append((_nhie_public(s), locked))
        _cat_order = {"safe": 0, "lewd": 1, "sexual": 2, "nuclear": 3}
        items.sort(key=lambda x: (_cat_order.get(x[0]["category"], 99), x[0]["id"]))
        return items

    def _nhie_pick_unique(pool):
        """Pick a line avoiding repeats within the same round."""
        _recent = getattr(store, "_nhie_round_lines", set())
        _fresh = [l for l in pool if l not in _recent]
        _pick = renpy.random.choice(_fresh) if _fresh else renpy.random.choice(pool)
        _recent.add(_pick)
        store._nhie_round_lines = _recent
        return _pick

    # "Bold" at the table: she picks the harder statements and answers / calls him out without blushing.
    # femdom counts (docs/plan_femdom.md 7). The stat multipliers of _nhie_apply_all_consequences keep their own lists.
    NHIE_BOLD_TRAITS = ("hardcore_sex", "exhibitionist", "femdom")

    def _nhie_is_bold(girl):
        return any(girl.has_trait(_t) for _t in NHIE_BOLD_TRAITS)

    def _nhie_pick_for_girl(girl, used_ids, has_npc):
        _drunk = get_drunk(girl)
        pool = _nhie_available(used_ids, _drunk, has_npc, for_who="girl")
        pool = [s for s in pool if "player_only" not in s.get("tags", set())]
        if not pool:
            return None

        _bold = _nhie_is_bold(girl) or _drunk >= 8
        if girl.has_trait("femdom"):
            print("[FEMDOM] %s picks her NHIE statement as bold" % girl.gid)
        _max_cat = "nuclear" if _drunk >= 8 else ("sexual" if _drunk >= 5 or _bold else ("lewd" if _drunk >= 2 else "safe"))
        _cat_order = ["safe", "lewd", "sexual", "nuclear"]
        _max_idx = _cat_order.index(_max_cat)

        weighted = []
        for s in pool:
            _ci = _cat_order.index(s["category"])
            if _ci > _max_idx:
                continue
            w = s.get("drama_weight", 1)
            if _bold and _ci >= 2:
                w += 2
            if not s["check"](girl):
                w += 1
            weighted.append((s, w))

        if not weighted:
            return _nhie_public(renpy.random.choice(pool)) if pool else None

        _total = sum(w for _, w in weighted)
        _r = renpy.random.random() * _total
        _acc = 0
        for s, w in weighted:
            _acc += w
            if _r <= _acc:
                return _nhie_public(s)
        return _nhie_public(weighted[-1][0])

    def _nhie_pick_for_npc(npc, gf, used_ids):
        _drunk = get_drunk(npc)
        has_npc = True
        pool = _nhie_available(used_ids, _drunk, has_npc, for_who="npc")
        if not pool:
            return None

        _susp = getattr(npc, "suspicion", 0)
        _hostile = getattr(npc, "friendship_with_player", 200) < 200

        weighted = []
        for s in pool:
            w = s.get("drama_weight", 1)
            if _susp > 30 and s["category"] in ("sexual", "nuclear"):
                w += 3
            if _hostile and s.get("tags", set()) & {"player_only"}:
                continue
            if _susp > 50 and "needs_bf" in s.get("tags", set()):
                w += 2
            if gf and s["check"](gf) and s["category"] in ("sexual", "nuclear"):
                w += 2
            weighted.append((s, w))

        if not weighted:
            return _nhie_public(renpy.random.choice(pool)) if pool else None

        _total = sum(w for _, w in weighted)
        _r = renpy.random.random() * _total
        _acc = 0
        for s, w in weighted:
            _acc += w
            if _r <= _acc:
                return _nhie_public(s)
        return _nhie_public(weighted[-1][0])

    # ------------------------------------------------------------------
    # CHECK WHO DRINKS
    # ------------------------------------------------------------------

    def _nhie_check_all(stmt, girls, npc):
        result = {}
        stmt = _nhie_full(stmt)  # label passes public copies (no callables); resolve by id
        try:
            result["player"] = bool(stmt["player_check"]())
        except Exception as e:
            print("[NHIE] player_check error: %s" % e)
            result["player"] = False

        for g in girls:
            try:
                result[g.gid] = bool(stmt["check"](g))
            except Exception as e:
                print("[NHIE] check error for %s: %s" % (g.gid, e))
                result[g.gid] = False

        if npc:
            _cat = stmt["category"]
            if _cat == "safe":
                result["npc"] = renpy.random.random() < 0.6
            elif _cat == "lewd":
                result["npc"] = renpy.random.random() < 0.25
            else:
                result["npc"] = False

        return result

    # ------------------------------------------------------------------
    # REACTIONS
    # ------------------------------------------------------------------

    NHIE_DRINK_LINES = {
        "safe": [
            _("Guilty!"),
            _("Yeah, that's me."),
            _("Can't deny that one."),
            _("Oh, definitely."),
            _("Who hasn't, honestly?"),
            _("Yep. Not even sorry."),
            _("Ha! Called out."),
        ],
        "lewd": [
            _("...fine."),
            _("Don't judge me."),
            _("It's not as bad as it sounds!"),
            _("Okay, okay, I'll drink to that."),
            _("That was supposed to be a secret..."),
            _("How do you even KNOW that?"),
            _("...I plead the fifth. Okay, fine, drinking."),
        ],
        "sexual": [
            _("..."),
            _("You didn't hear that from me."),
            _("I can't believe I'm admitting this."),
            _("Can we just... move on?"),
            _("What happens at the party stays at the party, right?"),
            _("Nobody repeat this tomorrow."),
            _("I hate this game."),
        ],
        "nuclear": [
            _("..."),
            _("I... yeah."),
            _("I'm not proud of it."),
            _("This game was a mistake."),
            _("Let's just... keep going."),
            _("Don't ask. Please."),
        ],
    }

    NHIE_DRINK_LINES_TRAIT = {
        "hardcore_sex": {
            "lewd":    [_("What? I'm not ashamed."), _("Yeah, and I'd do it again."), _("Is that supposed to be shocking?")],
            "sexual":  [_("So what? It was fun."), _("Guilty. Not sorry."), _("I'd do it again right now.")],
            "nuclear": [_("Guilty as charged."), _("Yeah. And?"), _("I regret nothing.")],
        },
        "cute_sex": {
            "lewd":    [_("Um... yes... please don't look at me like that."), _("Okay, fine, but it was really innocent!"), _("It's not what you think! Well... maybe a little.")],
            "sexual":  [_("Oh my god, I can't believe I'm drinking to this..."), _("Please forget I just did that..."), _("This is so embarrassing... I want to hide.")],
            "nuclear": [_("I... I need a moment after that..."), _("Can the floor swallow me up now?"), _("I'm never playing this again...")],
        },
        "exhibitionist": {
            "lewd":    [_("Oh please, like that's a secret."), _("And I enjoyed every second."), _("Everyone knew that already.")],
            "sexual":  [_("Want details?"), _("Ha! You should have seen the look on their face."), _("What? It was exciting.")],
            "nuclear": [_("And? It was a rush."), _("Yeah. Best night of my life."), _("I'm not going to pretend I didn't love it.")],
        },
        "loyal": {
            "sexual":  [_("...it's complicated."), _("I don't want to talk about it."), _("That was... a different time.")],
            "nuclear": [_("I'm not proud of that."), _("Please don't tell anyone."), _("I wish I could take it back.")],
        },
        "cheater": {
            "lewd":    [_("What? A girl has needs."), _("Don't act so surprised."), _("Like none of you have ever...")],
            "sexual":  [_("Yeah, well, things happen."), _("Life's too short to say no."), _("I had my reasons.")],
            "nuclear": [_("It is what it is."), _("I don't owe anyone an explanation."), _("Judge me all you want.")],
        },
        "nerd": {
            "safe":    [_("According to statistics, this is extremely common."), _("It's actually a perfectly normal thing to do."), _("I read that most people have, so...")],
            "lewd":    [_("I've... done research on the topic."), _("It was purely... academic curiosity."), _("The internet is a dangerous place, okay?")],
        },
        "public_shy": {
            "lewd":    [_("Can we just pretend I didn't drink?"), _("I'm going to regret admitting this..."), _("...please stop staring.")],
            "sexual":  [_("Oh god, why did I drink..."), _("Nobody was supposed to know that..."), _("I want to disappear right now.")],
        },
    }

    NHIE_DRINK_LINES_BOLD = [
        _("What? I'm not ashamed."),
        _("Yeah, and I'd do it again."),
        _("Is that supposed to be shocking?"),
        _("Guilty as charged."),
        _("Oh please, like that's a secret."),
        _("And? It was fun."),
    ]

    NHIE_SKIP_LINES_GENERIC = {
        "safe": [
            _("Nope."),
            _("Not me."),
            _("Can't relate."),
            _("I'm good."),
            _("Never."),
            _("Not this one."),
        ],
        "lewd": [
            _("I'll pass on this one."),
            _("Nope, not me."),
            _("Clean on this one."),
            _("My glass stays full."),
        ],
        "sexual": [
            _("...no, not that."),
            _("Not that one."),
            _("I'll keep my glass down, thanks."),
        ],
        "nuclear": [
            _("Absolutely not. No way."),
            _("Yeah, no. Not happening."),
            _("Not even close."),
        ],
    }

    NHIE_SKIP_LINES_TRAIT = {
        # femdom first (docs/plan_femdom.md 7): not her, and she tells the table what to do next
        "femdom":       [_("Not me. Next, and make it a better one."), _("Nope. Someone ask something worth my time."), _("Not me. Keep going, I'm waiting.")],
        "hardcore_sex": [_("Boring."), _("Ugh, really? That's the question?"), _("Wake me up when it gets interesting.")],
        "cute_sex":     [_("Thank goodness, no."), _("Oh no, never!"), _("Nuh-uh, not me.")],
        "exhibitionist": [_("Not yet, anyway."), _("Give me time."), _("Hmm, maybe I should try that...")],
        "nerd":         [_("Statistically unlikely for me."), _("I have better things to do."), _("My data says no.")],
        "public_shy":   [_("No! God, no."), _("I would never..."), _("That sounds terrifying.")],
        "cheater":      [_("Not that one. Yet."), _("I've done worse, but not that."), _("Hmm, not yet.")],
    }

    # Player drinks: narration per category (was a single fixed line)
    NHIE_PLAYER_DRINK_LINES = {
        "safe": [
            _("You take a drink. Some things you just can't deny."),
            _("You shrug and take a sip. Guilty."),
            _("You raise your glass. Everyone has done that."),
        ],
        "lewd": [
            _("You take a drink. A couple of eyebrows go up."),
            _("You sip, trying to look casual about it."),
            _("You drink. The girls exchange a look."),
        ],
        "sexual": [
            _("You take a long drink. The room gets a little quieter."),
            _("You drink without a word. Nobody misses it."),
            _("You take a drink and avoid the stares."),
        ],
        "nuclear": [
            _("You drink. The silence afterwards is heavy."),
            _("You take a slow sip. All eyes are on you now."),
            _("You drink, and you can feel the mood shift."),
        ],
    }

    # Girls react to the PLAYER's sexual/nuclear confessions.
    # Keyed by relationship to the player, then by statement category -> (expr, lines)
    #   gf        = dating the player and did NOT drink on this one
    #   gf_shared = dating the player and ALSO drank (both guilty)
    #   crush     = Love > 300, not dating, did not drink
    #   bold      = _nhie_is_bold (hardcore_sex / exhibitionist / femdom), did not drink
    #   default   = everyone else
    NHIE_PLAYER_CONFESS_REACT = {
        "gf": {
            "sexual":  ("worried", [
                _("Wait... with who?"),
                _("You never told me about that."),
                _("Okay. We are talking about that later."),
            ]),
            "nuclear": ("angry", [
                _("I don't even know what to say to you."),
                _("Wow. Good to know who I'm dating."),
                _("That's... we are definitely talking about this later."),
            ]),
        },
        "gf_shared": {
            "sexual":  ("shy", [
                _("Guess we're both guilty on that one..."),
                _("Yeah, that one's on both of us."),
                _("Don't look at me. You were there too."),
            ]),
            "nuclear": ("embarrassed", [
                _("...I'm not saying anything."),
                _("That's between us. Drink and move on."),
                _("Okay, that one is complicated. Next."),
            ]),
        },
        "crush": {
            "sexual":  ("surprised", [
                _("Oh. I didn't know that about you."),
                _("Look at you, full of surprises."),
                _("I'm learning a lot tonight."),
            ]),
            "nuclear": ("uncomfortable", [
                _("That's... a lot."),
                _("I'm going to need a minute with that one."),
                _("I really thought you were different."),
            ]),
        },
        "bold": {
            "sexual":  ("smirk", [
                _("Ohh, look at you."),
                _("Now we're getting somewhere."),
                _("Finally, something interesting."),
            ]),
            "nuclear": ("smirk", [
                _("Damn. Respect, honestly."),
                _("Okay, that one is dark. I like it."),
                _("You're worse than me. Impressive."),
            ]),
        },
        "default": {
            "sexual":  ("surprised", [
                _("Didn't expect that from you."),
                _("Well. That's new."),
                _("Wow. Okay then."),
            ]),
            "nuclear": ("uncomfortable", [
                _("I... wow. Okay."),
                _("That's heavy."),
                _("Someone change the subject. Please."),
            ]),
        },
    }

    # Girlfriend answers her partner's confrontation (after an NPC drama line)
    NHIE_GF_DEFEND_LINES = {
        "cheater": ("smirk", [
            _("Relax. It's a game."),
            _("Don't start. Not here."),
            _("You asked me to play, remember?"),
        ]),
        "loyal": ("sad", [
            _("I... I know. I'm sorry."),
            _("Please don't look at me like that."),
            _("Can we not do this in front of everyone?"),
        ]),
        "default": ("worried", [
            _("It's not what you think."),
            _("We'll talk about it later, okay?"),
            _("Babe, it's just a stupid game."),
        ]),
    }

    # The player's confession is ABOUT a girl at the table. She did not drink
    # (it is his confession), but everyone can connect the dots.
    #   guilty     = she is complicit and it is embarrassing for her (she took
    #                the money, she left her partner for him, she lost her
    #                virginity to him, she is the one he cheated with...)
    #                -> nervous deflection + blush
    #   suspicious = she does not know it was her (secret recording, stealth
    #                condom) -> worried, wonders if he means her
    NHIE_IMPLICATED = {
        "paid_for_sex":             ("guilty", lambda g: getattr(g, "_financial_times", 0) > 0),
        "stolen_partner":           ("guilty", lambda g: getattr(g, "_left_partner_for_player", False)),
        "took_virginity":           ("guilty", lambda g: getattr(g, "virginity_taken_by_player", False)),
        "cheated_partner":          ("guilty", lambda g: getattr(g, "PlayerCheatCount", 0) > 0 and not g.is_dating_player()),
        "walked_in_changing":       ("guilty", lambda g: g.GetActionCount("girl_walked_in_shower") > 0 if hasattr(g, "GetActionCount") else False),
        "recorded_without_consent": ("suspicious", lambda g: any(v.get("girl_gid") == g.gid and not v.get("consensual", True) for v in getattr(store.Player, "recorded_videos", []))),
        "lied_protection":          ("suspicious", lambda g: getattr(g, "_stealth_condom_count", 0) > 0),
    }

    # tone -> (expression, blush 0-2, lines)
    NHIE_IMPLICATED_LINES = {
        "guilty": {
            "default": ("nervous", 2, [
                _("...Why is everyone looking at me?"),
                _("Ha. Ha ha. Anyway. Who's next?"),
                _("I... need another drink. Right now."),
                _("Can we just skip this one? Please?"),
            ]),
            "shy": ("embarrassed", 2, [
                _("...Please don't. Not this one."),
                _("I'm going to the bathroom. Don't wait for me."),
                _("Oh god. Oh god, oh god."),
            ]),
            "bold": ("smirk", 1, [
                _("What? Don't look at me like that."),
                _("Yeah, yeah. Moving on."),
                _("Relax, it's a game. ...Next."),
            ]),
        },
        "suspicious": {
            "default": ("worried", 0, [
                _("...You're not talking about me. Right?"),
                _("Wait. Who? ...Never mind. I don't want to know."),
                _("That better not be about anyone in this room."),
            ]),
        },
    }

    # Statement-specific flavor, mixed into the tone pool when present
    NHIE_IMPLICATED_FLAVOR = {
        "paid_for_sex": {
            "default": [
                _("It's... not what it sounds like. Next question."),
                _("...Can we not?"),
            ],
            "bold": [
                _("Money well spent, if you ask me."),
                _("What? He got his money's worth."),
            ],
        },
        "stolen_partner": {
            "default": [
                _("It wasn't like that. I made my own choice."),
                _("...Nobody 'took' me anywhere, okay?"),
            ],
        },
        "took_virginity": {
            "default": [
                _("Is it warm in here? It feels warm in here."),
                _("...I'm not saying anything. Next."),
            ],
            "shy": [
                _("Please don't look at me. Please."),
            ],
        },
        "cheated_partner": {
            "default": [
                _("I... need some air."),
                _("Okay, wow, look at the time."),
            ],
        },
        "walked_in_changing": {
            "default": [
                _("In my defense, the door wasn't locked."),
                _("I didn't see anything! ...Much."),
            ],
        },
        "recorded_without_consent": {
            "default": [
                _("Wait. If that's about someone here, we have a problem."),
                _("...You better not be talking about me."),
            ],
        },
    }

    def _nhie_implicated_reactions(stmt, girls, drinkers):
        """Girls who did NOT drink but are the subject of the player's confession.
        Returns [(girl, expr, blush, line)] in table order."""
        _spec = NHIE_IMPLICATED.get(stmt["id"])
        if not _spec or not drinkers.get("player", False):
            return []
        _kind, _fn = _spec
        out = []
        for g in girls:
            if drinkers.get(g.gid, False):
                continue
            try:
                if not _fn(g):
                    continue
            except Exception as e:
                print("[NHIE] implicated check error for %s: %s" % (g.gid, e))
                continue
            _tone = "default"
            if _kind == "guilty":
                if _nhie_is_bold(g):
                    _tone = "bold"
                elif g.has_trait("cute_sex") or g.has_trait("public_shy"):
                    _tone = "shy"
            _expr, _blush, _pool = NHIE_IMPLICATED_LINES[_kind][_tone]
            _pool = list(_pool) + list(NHIE_IMPLICATED_FLAVOR.get(stmt["id"], {}).get(_tone, []))
            out.append((g, _expr, _blush, renpy.random.choice(_pool)))
            print("[NHIE] Implicated: %s kind=%s tone=%s on '%s'" % (g.gid, _kind, _tone, stmt["id"]))
        return out

    # ------------------------------------------------------------------
    # PLAYER TRUTH / LIE / BLUFF
    # ------------------------------------------------------------------
    # The player always chooses to drink or not. The game keeps knowing the
    # truth (player_check). States:
    #   truth & drink      = confession (everything that already exists)
    #   truth & no drink   = LIE  -> girls who KNOW react (below)
    #   no truth & no drink= truth
    #   no truth & drink   = BLUFF -> girls BELIEVE it (confession path)
    #
    # NHIE_PLAYER_TRUTH_KNOWN: "she was there / it involved her" -> she knows
    # he should have drunk. Secondhand knowledge comes from knows_with_player
    # (witnessed, saw a video, heard it in a previous NHIE).
    NHIE_PLAYER_TRUTH_KNOWN = {
        "kissed_in_room":      lambda g: "kiss" in getattr(g, "intimacy_flags", set()),
        "sent_dick_pic":       lambda g: getattr(g, "_dick_pics_received", 0) > 0,
        "received_oral":       lambda g: "bj" in getattr(g, "intimacy_flags", set()),
        "walked_in_changing":  lambda g: g.GetActionCount("girl_walked_in_shower") > 0 if hasattr(g, "GetActionCount") else False,
        "slept_same_bed":      lambda g: g.GetActionCount("slept_together") > 0 if hasattr(g, "GetActionCount") else False,
        "sex_no_condom":       lambda g: getattr(g, "raw_sex_count", 0) > 0,
        "sex_in_public":       lambda g: getattr(g, "CorruptionPublicHeavyActs", 0) > 0,
        "sex_three_times_day": lambda g: _nhie_max_sex_in_one_day(g) > 3,
        "atm":                 lambda g: getattr(g, "_atm_count", 0) > 0,
        "recorded_sex_video":       lambda g: any(v.get("girl_gid") == g.gid for v in getattr(store.Player, "recorded_videos", [])),
        "recorded_without_consent": lambda g: any(v.get("subject") == "self" and not v.get("consensual", True) for v in getattr(g, "video_seen_history", [])),
        "had_threesome":       lambda g: any(g.get_history_with(og.gid, "threesome") > 0 for og in ALL_GIRLS if og.gid != g.gid),
        "enjoyed_anal":        lambda g: getattr(g, "Sex_acts", {}).get("anal", 0) > 3,
        "took_virginity":      lambda g: getattr(g, "virginity_taken_by_player", False),
        "cheated_partner":     lambda g: getattr(g, "PlayerCheatCount", 0) > 0 or (g.GetActionCount("caught_player_cheating") > 0 if hasattr(g, "GetActionCount") else False),
        "paid_for_sex":        lambda g: getattr(g, "_financial_times", 0) > 0,
        "dated_multiple":      lambda g: g.is_dating_player() and bool(getattr(g, "harem_accepted", None)),
        "stolen_partner":      lambda g: getattr(g, "_left_partner_for_player", False),
        "lied_protection":     lambda g: g.GetActionCount("stealth_condom_discovered") > 0 if hasattr(g, "GetActionCount") else False,
        "blackout_drunk":      lambda g: hangout_get_player_alcohol() >= 12,   # everyone can see he is wasted right now
        "exercised_today":     lambda g: _buddy_get_count(g, "workout") > 0 if callable(globals().get("_buddy_get_count")) else False,
    }

    def _nhie_girl_knows_player_truth(stmt, girl):
        """'direct' (she was involved), 'secondhand' (she knows he did it with
        another girl, via knows_with_player), or None."""
        _fn = NHIE_PLAYER_TRUTH_KNOWN.get(stmt["id"])
        if _fn:
            try:
                if _fn(girl):
                    return "direct"
            except Exception as e:
                print("[NHIE-LIE] truth-known check error for %s: %s" % (girl.gid, e))
        _kmap = NHIE_KNOWLEDGE_MAP.get(stmt["id"])
        if _kmap:
            _act = _kmap[0]
            _kw = getattr(girl, "knows_with_player", {}) or {}
            for og in ALL_GIRLS:
                if og.gid != girl.gid and _act in _kw.get(og.gid, set()):
                    return "secondhand"
        return None

    # Caught lying: who speaks, by relationship / trait
    NHIE_LIE_CALLOUT = {
        "gf": ("smug", [
            _("Wow. Am I that forgettable?"),
            _("Not drinking? Should I be offended?"),
            _("Your memory is terrible, babe. Drink."),
        ]),
        "gf_intimate": ("worried", [
            _("...So I'm the thing you don't admit. Noted."),
            _("You're really going to pretend that never happened? In front of me?"),
        ]),
        "bold": ("smirk", [
            _("Liar. Drink."),
            _("Oh, you're not drinking? Want me to help your memory?"),
            _("Cute. Everyone, he's lying."),
        ]),
        "default": ("sly", [
            _("Hm. That's not how I remember it."),
            _("Funny. Your glass looks very full."),
            _("Are we sure about that? Really sure?"),
        ]),
        "secondhand": ("smug", [
            _("Funny. That's not what I heard."),
            _("Someone told me a very different story."),
        ]),
    }

    # She knows but keeps quiet (narration with %s = her name)
    NHIE_LIE_SILENT_NARR = {
        "shy": [
            _("%s glances at you and says nothing."),
            _("%s suddenly finds her glass very interesting."),
        ],
        "secondhand": [
            _("%s raises an eyebrow, but keeps her mouth shut."),
            _("%s smiles to herself and lets it slide."),
        ],
    }

    # Bluff: a bold girl may doubt him (no evidence, no stat effect)
    NHIE_BLUFF_DOUBT = [
        _("Sure you did."),
        _("Uh huh. Details, or it didn't happen."),
    ]

    # Player chose not to drink (neutral, whether or not it was a lie)
    NHIE_PLAYER_PASS_LINES = [
        _("You leave your glass where it is."),
        _("You keep your hands off your glass."),
    ]

    # Love loss of the girl who caught the lie, by statement category (x1.5 if she is dating him)
    NHIE_LIE_CAUGHT_LOVE = {"safe": -2, "lewd": -3, "sexual": -8, "nuclear": -12}

    def _nhie_lie_reactions(stmt, girls):
        """Reactions to the player NOT drinking when he should have.
        Returns (spoken, narrations):
          spoken     = (girl, expr, blush, line) or None  -> counts as CAUGHT
          narrations = [(girl, expr, blush, text)]        -> she knows, says nothing"""
        _cat = stmt["category"]
        _direct, _second = [], []
        for g in girls:
            _k = _nhie_girl_knows_player_truth(stmt, g)
            if _k == "direct":
                _direct.append(g)
            elif _k == "secondhand":
                _second.append(g)
        spoken = None
        narrations = []

        def _is_bold(g):
            return _nhie_is_bold(g) or g.has_trait("cheater")

        def _is_shy(g):
            return g.has_trait("cute_sex") or g.has_trait("public_shy")

        # 1) Direct knowers: GF > bold > default speak; shy stays silent (exposing him exposes her)
        _cands = [g for g in _direct if not _is_shy(g)]
        if _cands:
            _gfs = [g for g in _cands if g.is_dating_player()]
            _bolds = [g for g in _cands if _is_bold(g)]
            if _gfs:
                _who = max(_gfs, key=lambda g: g.Love)
                _key = "gf_intimate" if _cat in ("sexual", "nuclear") else "gf"
            elif _bolds:
                _who = _bolds[0]
                _key = "bold"
            else:
                _who = _cands[0]
                _key = "default"
            _e, _pool = NHIE_LIE_CALLOUT[_key]
            spoken = (_who, _e, 0, renpy.random.choice(_pool))
        for g in _direct:
            if _is_shy(g) and (spoken is None or spoken[0] is not g):
                narrations.append((g, "nervous", 1, _tl(renpy.random.choice(NHIE_LIE_SILENT_NARR["shy"])) % g.Name))
                break

        # 2) Secondhand knowers: expose only if jealous / bold, else a silent smirk
        if spoken is None and _second:
            _exposers = [g for g in _second if getattr(g, "Jealousy", 0) >= 300 or _is_bold(g)]
            if _exposers:
                _e, _pool = NHIE_LIE_CALLOUT["secondhand"]
                spoken = (_exposers[0], _e, 0, renpy.random.choice(_pool))
            elif not narrations:
                g = _second[0]
                narrations.append((g, "smug", 0, _tl(renpy.random.choice(NHIE_LIE_SILENT_NARR["secondhand"])) % g.Name))

        print("[NHIE-LIE] reactions: direct=%s secondhand=%s caught_by=%s" % (
            [g.gid for g in _direct], [g.gid for g in _second], spoken[0].gid if spoken else None))
        return spoken, narrations[:1]

    def _nhie_bluff_doubt(stmt, girls):
        """30% chance: a bold girl who has no evidence doubts a bluff. Returns (girl, line) or None."""
        if stmt["category"] not in ("sexual", "nuclear"):
            return None
        _bolds = [g for g in girls if _nhie_is_bold(g) and _nhie_girl_knows_player_truth(stmt, g) is None]
        if _bolds and renpy.random.random() < 0.3:
            return (renpy.random.choice(_bolds), renpy.random.choice(NHIE_BLUFF_DOUBT))
        return None

    # Girl announcing her statement: expression by category (was always "smirk")
    NHIE_SPEAK_EXPR = {"safe": "happy", "lewd": "smirk", "sexual": "sly", "nuclear": "serious"}

    NHIE_NPC_DRINK_LINES = [
        _("Hey, I'm only human."),
        _("Alright, fair enough."),
        _("That one got me."),
    ]

    NHIE_NPC_REACT_LEWD = [
        _("Huh. Interesting."),
        _("That's... good to know."),
        _("Well. Okay then."),
        _("Hm. Noted."),
    ]

    NHIE_NPC_REACT_SEXUAL = [
        _("Wait, seriously?"),
        _("Babe...?"),
        _("Since when?"),
        _("I... didn't know that."),
    ]

    NHIE_NPC_REACT_NUCLEAR = [
        _("What the hell?"),
        _("Are you serious right now?"),
        _("We're going to talk about this later."),
        _("I don't even know what to say."),
    ]

    # ------------------------------------------------------------------
    # PLAYER DISCOVERIES — what the player learns from a girl's answer
    # ------------------------------------------------------------------
    # A trait-flavored drink/skip reaction is evidence of that trait (same
    # rule scene_pick_line uses with _MOD_DISCOVER_MAP): the player discovers
    # it -> discovery banner + PERSONALITY hint on the status screen.
    # (statement id, trait) or (statement id, trait, "drink"/"skip") pairs whose reaction LINE
    # does not evidence the trait (tone, deflection, or a reaction any girl would have):
    # the line still plays, nothing is revealed. Identity statements and lines that name the
    # taste stay out of this set and keep discovering.
    _NHIE_NO_DISCOVER = {
        ("bought_useless_online", "poor", "drink"),      # "...once. And I still regret it." names no money fact
        ("got_f_grade", "gym_rat", "skip"),              # not checking grades says nothing about the gym
        ("cried_movie", "hardcore_sex"),                 # "Shut up. It was a really sad movie" / "I don't cry. Ever."
        ("cried_movie", "cute_sex"),                     # "I cry at everything"
        ("kissed_in_room", "cute_sex"),                  # "It was really sweet" / "Not yet..."
        ("kissed_in_room", "exhibitionist"),             # "The night is young" is flirt tone
        ("sexy_photo", "camera_lover", "skip"),          # surprise at others, not her own camera love
        ("sent_dick_pic", "public_shy"),                 # "I didn't ask for it!" / "Thank god, no."
        ("sent_dick_pic", "exhibitionist"),              # not minding a received nude is not being-seen
        ("fantasized_here", "cute_sex"),                 # flirty tone
        ("fantasized_here", "exhibitionist"),            # "More than once" names nothing
        ("liked_spanking", "cute_sex", "drink"),         # shy admission of liking a ROUGH act
        ("touched_self_thinking", "cum_slut"),           # "They're hot. Can you blame me?" has no cum in it
        ("touched_self_thinking", "cute_sex"),           # embarrassment tone
        ("touched_self_thinking", "exhibitionist"),      # "I don't regret it" names nothing
        ("received_oral", "hardcore_sex"),               # loving oral is not a rough taste
        ("received_oral", "cute_sex"),                   # "really nice" tone
        ("walked_in_changing", "public_shy", "drink"),   # screaming when walked in on is any girl
        ("slept_same_bed", "cute_sex"),                  # cuddling sweetness is tone
        ("slept_same_bed", "exhibitionist"),             # escalation brag, nothing about being seen
        ("sex_in_public", "public_shy", "drink"),        # "heart pounding" matches the default pool
        ("sex_three_times_day", "cum_slut"),             # libido, not cum
        ("sex_three_times_day", "hardcore_sex"),         # "in the mood all day" is libido
        ("atm", "cum_slut"),                             # "It was hot" names nothing
        ("atm", "hardcore_sex"),                         # "Don't knock it" is bravado
        ("atm", "anal_lover"),                           # "it just kind of happened" names nothing
        ("atm", "anal_hater"),                           # disgust at ATM is any girl (default: "Hard pass")
        ("atm", "hate_cum"),                             # same: universal ick
        ("recorded_sex_video", "exhibitionist"),         # "I'd do it again" names nothing
        ("recorded_sex_video", "camera_lover", "skip"),  # "not against it" is too tepid to banner
        ("had_threesome", "exhibitionist"),              # threesome enthusiasm is not being-seen
        ("enjoyed_anal", "anal_lover", "skip"),          # "why are you looking at me?" deflects
        ("lost_virginity", "cute_sex"),                  # "it was special" is any girl's first time
        ("lost_virginity", "hardcore_sex"),              # "got it over with" is tone
        ("been_blackmailed", "loyal"),                   # being wronged says nothing about fidelity
        ("been_blackmailed", "hardcore_sex"),            # defiance tone
        ("same_sex_curious", "exhibitionist"),           # "people are attractive" is not being-seen
        ("recorded_without_consent", "camera_hater"),    # fury at a violation is any girl
        ("recorded_without_consent", "camera_lover", "skip"),  # "at least ask first" is too weak
        ("ntr_watched", "voyeur", "drink"),              # liking BEING watched is not voyeur evidence
    }

    def _nhie_no_discover(stmt_id, trait, drank):
        """True when this statement's reaction line for this trait must not reveal it."""
        return ((stmt_id, trait) in _NHIE_NO_DISCOVER
                or (stmt_id, trait, "drink" if drank else "skip") in _NHIE_NO_DISCOVER)

    def _nhie_discover_trait(girl, trait):
        if not trait or trait == "default" or not hasattr(girl, "discover"):
            return
        if hasattr(girl, "has_trait") and not girl.has_trait(trait):
            return
        girl.discover("discovered_trait_%s" % trait)

    # Facts revealed by DRINKING on a statement (beyond trait reactions):
    # sexuality, dating status, tolerance, gym habit, camera/exhib, anal
    def _nhie_player_learns(stmt, girl):
        _sid = stmt["id"]
        if _sid == "same_sex_curious":
            for _t in ("lesbian", "bisexual"):
                _nhie_discover_trait(girl, _t)
        elif _sid == "blackout_drunk":
            _nhie_discover_trait(girl, "lightweight")
        elif _sid == "exercised_today":
            _nhie_discover_trait(girl, "gym_rat")
        elif _sid == "sexy_photo":
            # If she never sent the player a photo, she drank because of the trait
            if not _nhie_girl_sent_photo(girl):
                for _t in ("camera_lover", "exhibitionist"):
                    _nhie_discover_trait(girl, _t)
        elif _sid == "enjoyed_anal":
            _nhie_discover_trait(girl, "anal_lover")
        elif _sid in ("cheated_partner", "ntr_watched"):
            # She just admitted having a partner
            if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                _discover_partner(girl)
                girl.discover("discovered_relationship")

    def _nhie_custom_reaction(girl, custom, drank, stmt_id=None):
        """Her line from a statement's own drink_reactions / skip_reactions: a girlfriend's "_gf_<trait>" / "_gf"
        first, then the first trait entry she has (dict order), then "default". None: the generic pools answer.
        Drinking, an eager trait she is still discovering speaks only through its "<trait>_first" / "_new" entry
        (trait_line_keys): she did it, but she is no veteran. Skip lines never claim she did it: no stage there."""
        if hasattr(girl, "is_dating_player") and girl.is_dating_player():
            for _key, (_cexpr, _clines) in custom.items():
                if _key.startswith("_gf_"):
                    _req_trait = _key[4:]
                    if girl.has_trait(_req_trait):
                        if not _nhie_no_discover(stmt_id, _req_trait, drank):
                            _nhie_discover_trait(girl, _req_trait)
                        return (_cexpr, _nhie_pick_unique(_clines))
            if "_gf" in custom:
                _ge, _gl = custom["_gf"]
                return (_ge, _nhie_pick_unique(_gl))
        for _trait in custom:
            if _trait == "default" or _trait.startswith("_gf") or _trait.endswith(("_first", "_new")):
                continue
            if not girl.has_trait(_trait):
                continue
            for _k in (trait_line_keys(girl, _trait) if drank else [_trait]):
                if _k in custom:
                    _cexpr, _clines = custom[_k]
                    if not _nhie_no_discover(stmt_id, _trait, drank):
                        _nhie_discover_trait(girl, _trait)
                    return (_cexpr, _nhie_pick_unique(_clines))
        if "default" in custom:
            _de, _dl = custom["default"]
            return (_de, _nhie_pick_unique(_dl))
        return None

    def _nhie_girl_drink_reaction(girl, stmt):
        _custom = stmt.get("drink_reactions", {})
        # what really happened to her may pick another pool: "drink_variant" (girl -> name or None) reads
        # "drink_reactions_<name>" (the callable lives on the registry entry: the label passes public copies)
        _variant_fn = _nhie_full(stmt).get("drink_variant")
        _variant = _variant_fn(girl) if callable(_variant_fn) else None
        if _variant and stmt.get("drink_reactions_%s" % _variant):
            _custom = stmt["drink_reactions_%s" % _variant]
            print("[NHIE] %s drinks on '%s' with the '%s' reactions" % (girl.gid, stmt["id"], _variant))
        if _custom:
            _r = _nhie_custom_reaction(girl, _custom, True, stmt["id"])
            if _r:
                return _r

        _cat = stmt["category"]
        _bold = _nhie_is_bold(girl) or get_drunk(girl) >= 10

        for _tk, _tpools in NHIE_DRINK_LINES_TRAIT.items():
            if girl.has_trait(_tk) and _cat in _tpools:
                _expr = "smirk" if _tk in ("hardcore_sex", "exhibitionist", "cheater") else ("embarrassed" if _cat in ("sexual", "nuclear") else "shy")
                # only these pools voice their trait: exhibitionist ("everyone knew that already",
                # "want details?") and nerd ("I've done research"); the rest are tone
                if _tk in ("exhibitionist", "nerd"):
                    _nhie_discover_trait(girl, _tk)
                return (_expr, _nhie_pick_unique(_tpools[_cat]))

        if _bold and _cat in ("lewd", "sexual"):
            _expr = "smirk"
            _line = _nhie_pick_unique(NHIE_DRINK_LINES_BOLD)
        elif _cat == "nuclear":
            _expr = "embarrassed"
            _line = _nhie_pick_unique(NHIE_DRINK_LINES["nuclear"])
        elif _cat == "sexual":
            _expr = "embarrassed"
            _line = _nhie_pick_unique(NHIE_DRINK_LINES["sexual"])
        elif _cat == "lewd":
            _expr = "shy"
            _line = _nhie_pick_unique(NHIE_DRINK_LINES["lewd"])
        else:
            _expr = "happy"
            _line = _nhie_pick_unique(NHIE_DRINK_LINES["safe"])
        return (_expr, _line)

    def _nhie_girl_skip_reaction(girl, stmt):
        _custom = stmt.get("skip_reactions", {})
        if _custom:
            _r = _nhie_custom_reaction(girl, _custom, False, stmt["id"])
            if _r:
                return _r

        _cat = stmt["category"]
        for _tk, _tpool in NHIE_SKIP_LINES_TRAIT.items():
            if girl.has_trait(_tk):
                # femdom skip lines order the table around (control voice), nerd talks statistics;
                # the other skip pools are tone and reveal nothing
                if _tk in ("femdom", "nerd"):
                    _nhie_discover_trait(girl, _tk)
                return ("normal", _nhie_pick_unique(_tpool))

        _pool = NHIE_SKIP_LINES_GENERIC.get(_cat, NHIE_SKIP_LINES_GENERIC["safe"])
        return ("normal", _nhie_pick_unique(_pool))

    def _nhie_npc_drama(npc, gf, stmt, player_also_drank=False):
        _cat = stmt["category"]
        _susp = getattr(npc, "suspicion", 0)
        if _cat == "lewd":
            _line = renpy.random.choice(NHIE_NPC_REACT_LEWD)
            _add = 2
        elif _cat == "sexual":
            _add = 5 if _susp < 30 else 8
            _line = renpy.random.choice(NHIE_NPC_REACT_SEXUAL)
        elif _cat == "nuclear":
            _add = 10 if _susp < 50 else 15
            _line = renpy.random.choice(NHIE_NPC_REACT_NUCLEAR)
        else:
            return (None, 0)
        _kmap = NHIE_KNOWLEDGE_MAP.get(stmt["id"])
        if player_also_drank and _kmap and _kmap[1]:
            _add = int(_add * 2)
            print("[NHIE] NPC drama DOUBLED: player+GF both drank on with_player stmt")
        # NTR arrangement he already agreed to: nothing to be suspicious about
        if stmt["id"] == "ntr_watched" and getattr(npc, "_ntr_active", False):
            return (None, 0)
        # She admitted cheating to his face: he KNOWS now, not just suspects
        if stmt["id"] == "cheated_partner":
            _add = max(_add, 30)
        return (_line, _add)

    def _nhie_gf_defend_line(girl):
        """(expr, line) — how the girlfriend answers her partner's confrontation."""
        if girl.has_trait("cheater"):
            _key = "cheater"
        elif girl.has_trait("loyal"):
            _key = "loyal"
        else:
            _key = "default"
        _e, _pool = NHIE_GF_DEFEND_LINES[_key]
        return (_e, renpy.random.choice(_pool))

    def _nhie_player_confess_reaction(stmt, girls, drinkers, npc=None, exclude=None):
        """One girl reacts to the player's sexual/nuclear confession.
        Returns (girl, expr, line) or None. Priority: GF > crush > bold > default.
        A GF whose own NPC partner is in the room (secret relationship) cannot
        react as a girlfriend in front of him — she falls back to the crush pool.
        `exclude` = gids that already reacted as implicated (the confession was about them)."""
        _cat = stmt["category"]
        if exclude:
            girls = [g for g in girls if g.gid not in exclude]
        if _cat not in ("sexual", "nuclear") or not girls:
            return None
        _npc_gf_gid = getattr(npc, "girl_gid", None) if npc is not None else None
        _gf = None
        _crush = None
        _bold = None
        for g in girls:
            if g.is_dating_player() and not (g.has_npc_partner() and _npc_gf_gid == g.gid):
                if _gf is None or g.Love > _gf.Love:
                    _gf = g
            elif g.Love > 300 and not drinkers.get(g.gid, False):
                if _crush is None or g.Love > _crush.Love:
                    _crush = g
            elif _nhie_is_bold(g) and not drinkers.get(g.gid, False):
                _bold = g
        if _gf is not None:
            _who = _gf
            _rel = "gf_shared" if drinkers.get(_gf.gid, False) else "gf"
        elif _crush is not None:
            _who = _crush
            _rel = "crush"
        elif _bold is not None:
            _who = _bold
            _rel = "bold"
        else:
            _who = renpy.random.choice(girls)
            _rel = "default"
        _e, _pool = NHIE_PLAYER_CONFESS_REACT[_rel][_cat]
        print("[NHIE] Player confession reaction: %s rel=%s cat=%s" % (_who.gid, _rel, _cat))
        return (_who, _e, renpy.random.choice(_pool))

    NHIE_NOBODY_LINES = [
        _("Nobody drinks. A clean slate on this one."),
        _("Glasses stay on the table. Looks like nobody's guilty."),
        _("Not a single sip. That's a first."),
    ]

    # ------------------------------------------------------------------
    # KNOWLEDGE MAP — statement ID -> (act_key, with_player)
    # ------------------------------------------------------------------

    # with_player=True entries also feed _nhie_check_jealousy (watchers who like
    # the player get jealous) and knows_with_player (ToD truths, group dates).
    NHIE_KNOWLEDGE_MAP = {
        "kissed_in_room": ("kiss", True),
        "touched_self_thinking": ("masturbate", True),
        "fantasized_here": ("fantasize", True),
        "slept_same_bed": ("sleepover", True),

        "received_oral": ("oral", False),
        "liked_spanking": ("slap", False),
        "sexy_photo": ("photo", False),
        "sex_no_condom": ("sex", False),
        "cum_inside": ("creampie", False),
        "sex_in_public": ("sex", False),
        "sex_three_times_day": ("sex", False),
        "atm": ("anal", False),
        "had_threesome": ("threesome", False),
        "enjoyed_anal": ("anal", False),
        "cum_on_face": ("facial", False),
        "forced_swallow": ("bj", False),
        "lost_virginity": ("sex", False),
        "recorded_sex_video": ("recorded", False),
        "recorded_without_consent": ("recorded", False),
        "sex_for_money": ("paid", False),
        "been_blackmailed": ("blackmailed", False),
        "dated_multiple": ("dating", True),
        "ntr_watched": ("ntr", True),
    }

    # Statements whose DRINK also reveals a relationship fact to the other girls
    _NHIE_REVEALS_PARTNER = {"cheated_partner", "ntr_watched"}
    _NHIE_REVEALS_ORIENTATION = {"same_sex_curious"}

    def _nhie_propagate_knowledge(stmt, girls, drinkers):
        """Every other girl at the table learns what a drinker just admitted."""
        _sid = stmt["id"]
        _kmap = NHIE_KNOWLEDGE_MAP.get(_sid)
        _reveals_partner = _sid in _NHIE_REVEALS_PARTNER
        _reveals_orient = _sid in _NHIE_REVEALS_ORIENTATION
        if not (_kmap or _reveals_partner or _reveals_orient):
            return
        for g in girls:
            if not drinkers.get(g.gid, False):
                continue
            for other in girls:
                if other.gid == g.gid:
                    continue
                if _kmap:
                    girl_learns_act(other, g, _kmap[0], with_player=_kmap[1])
                if _reveals_partner and hasattr(g, "has_npc_partner") and g.has_npc_partner():
                    girl_learns_has_bf(other, g)
                if _reveals_orient:
                    girl_learns_lesbian(other, g)   # no-op unless she has the lesbian trait
            print("[NHIE] Knowledge: %s revealed '%s' (act=%s partner=%s orient=%s)" % (
                g.gid, _sid, _kmap, _reveals_partner, _reveals_orient))

    def _nhie_update_npc_love(npc, stmt, player_also_drank=False):
        _cat = stmt["category"]
        if _cat == "sexual":
            _loss = renpy.random.randint(5, 15)
        elif _cat == "nuclear":
            _loss = renpy.random.randint(15, 30)
        else:
            return 0
        _kmap = NHIE_KNOWLEDGE_MAP.get(stmt["id"])
        if player_also_drank and _kmap and _kmap[1]:
            _loss = int(_loss * 1.5)
        # change_love mirrors the value into girl._npc_love (survives save/load)
        npc.change_love(-_loss)
        print("[NHIE] NPC love_for_girl -%d -> %d" % (_loss, npc.love_for_girl))
        return _loss

    def _nhie_check_jealousy(stmt, girls, drinkers):
        _kmap = NHIE_KNOWLEDGE_MAP.get(stmt["id"])
        if not _kmap:
            return []
        _act, _wp = _kmap
        if not _wp:
            return []
        _jealous = []
        for watcher in girls:
            if drinkers.get(watcher.gid, False):
                continue
            if not (watcher.Love > 200 or watcher.is_dating_player()):
                continue
            for drinker in girls:
                if drinker.gid == watcher.gid:
                    continue
                if not drinkers.get(drinker.gid, False):
                    continue
                _add = 10 if watcher.is_dating_player() else 5
                if watcher.has_trait("monogamous"):
                    _add = int(_add * 1.5)
                elif watcher.has_trait("polyamorous"):
                    _add = int(_add * 0.5)
                Change_Status(watcher, "Jealousy", _add, show_popup=False)
                _jealous.append((watcher, drinker, _add))
                print("[NHIE] Jealousy: %s +%d (saw %s on '%s') -> %d" % (watcher.gid, _add, drinker.gid, stmt["id"], watcher.Jealousy))
                break
        return _jealous

    NHIE_JEALOUSY_GF = [
        _("Wait... you did that? With who?"),
        _("That's... interesting to know."),
        _("Hm. I'll remember that."),
    ]

    NHIE_JEALOUSY_CRUSH = [
        _("Oh... cool. I guess."),
        _("That's... nice for you."),
    ]

    # ------------------------------------------------------------------
    # CONSEQUENCES — stat changes from revelations
    # ------------------------------------------------------------------

    NHIE_CAT_CONSEQUENCES = {
        "safe":    {"girl_like_bond": 3,  "girl_like_shock": 0,   "bf_loyalty": 0,   "npc_friendship": 0,   "love_rival": 0,   "player_inbt": 0,  "girl_obed": 0,  "shared_love": 2},
        "lewd":    {"girl_like_bond": 5,  "girl_like_shock": -5,  "bf_loyalty": -3,  "npc_friendship": -3,  "love_rival": -3,  "player_inbt": 3,  "girl_obed": 2,  "shared_love": 3},
        "sexual":  {"girl_like_bond": 8,  "girl_like_shock": -10, "bf_loyalty": -8,  "npc_friendship": -8,  "love_rival": -5,  "player_inbt": 5,  "girl_obed": 5,  "shared_love": 5},
        "nuclear": {"girl_like_bond": 10, "girl_like_shock": -15, "bf_loyalty": -15, "npc_friendship": -12, "love_rival": -10, "player_inbt": 8,  "girl_obed": 8,  "shared_love": 5},
    }

    NHIE_STMT_OVERRIDES = {
        "cheated_partner":          {"bf_loyalty": -30, "girl_like_shock": -25, "love_rival": -15, "girl_obed": 8},
        "sex_for_money":            {"girl_like_shock": -20, "bf_loyalty": -20, "girl_obed": 10},
        "been_blackmailed":         {"girl_like_shock": 5,  "girl_like_bond": 15, "girl_obed": 12},
        "ntr_watched":              {"bf_loyalty": -20, "girl_like_shock": -15, "player_inbt": 10},
        "dated_multiple":           {"bf_loyalty": -20, "girl_like_shock": -15, "love_rival": -12},
        "cum_inside":               {"bf_loyalty": -12, "girl_like_shock": -8},
        "had_threesome":            {"girl_like_shock": -12, "player_inbt": 8},
        "recorded_sex_video":       {"bf_loyalty": -15, "girl_like_shock": -10, "girl_obed": 8},
        "recorded_without_consent": {"girl_like_shock": -20, "player_inbt": 10, "girl_obed": 10},
        "forced_swallow":           {"girl_like_shock": -8, "player_inbt": 8},
        "lost_virginity": {"girl_like_shock": -5, "shared_love": 3},
        "stolen_partner":           {"bf_loyalty": -15, "girl_like_shock": -15},
        "lied_protection":          {"bf_loyalty": -20, "girl_like_shock": -15, "player_inbt": 10},
    }

    # Per-statement trait relevance: which traits amplify shock or dampen it
    # shock = traits that make the watcher MORE shocked (x1.8)
    # unfazed = traits that make the watcher LESS shocked (x0.3)
    # bond = traits that amplify bonding between co-drinkers (x1.5 both, +2 one)
    NHIE_TRAIT_REACTIONS = {
        "enjoyed_anal":       {"shock": ["anal_hater"],                "unfazed": ["anal_lover"],                        "bond": ["anal_lover"]},
        "atm":                {"shock": ["anal_hater", "hate_cum"],   "unfazed": ["anal_lover", "hardcore_sex"]},
        "cum_on_face":        {"shock": ["hate_cum"],                 "unfazed": ["cum_slut"],                         "bond": ["cum_slut"]},
        "forced_swallow":     {"shock": ["hate_cum"],                 "unfazed": ["cum_slut", "hardcore_sex"]},
        "cum_inside":         {"shock": ["hate_cum"],                 "unfazed": ["cum_slut"]},
        "sex_in_public":      {"shock": ["public_shy"],                "unfazed": ["public_fetish", "exhibitionist"],    "bond": ["public_fetish"]},
        "sexy_photo":         {"shock": ["camera_hater", "public_shy"], "unfazed": ["camera_lover", "exhibitionist"]},
        "recorded_sex_video":       {"shock": ["camera_hater"],              "unfazed": ["camera_lover", "exhibitionist"]},
        "recorded_without_consent": {"shock": ["camera_hater", "public_shy"], "unfazed": ["camera_lover"]},
        "liked_spanking":     {"shock": ["cute_sex"],                    "unfazed": ["hardcore_sex"],                          "bond": ["hardcore_sex"]},
        "cheated_partner":    {"shock": ["loyal"],                     "unfazed": ["cheater"]},
        "dated_multiple":     {"shock": ["loyal"],                    "unfazed": ["cheater"]},
        "had_threesome":      {"shock": ["loyal"],                    "unfazed": ["exhibitionist", "cheater"]},
        "ntr_watched":        {"shock": ["loyal"],                    "unfazed": ["voyeur", "exhibitionist"]},
        "sex_for_money":      {"shock": ["loyal"],                    "unfazed": []},
        "been_blackmailed":   {"shock": [],                           "unfazed": [],                                    "bond": ["loyal", "cute_sex"]},
        "walked_in_changing": {"shock": ["public_shy"],                "unfazed": ["exhibitionist"]},
        "stolen_partner":     {"shock": ["loyal"],                     "unfazed": ["cheater"]},
        "lied_protection":    {"shock": ["loyal"],                     "unfazed": ["cheater"]},
    }

    # Reaction dialogue pools

    NHIE_BOND_NARRATION = [
        _("%s and %s exchange a look and laugh, clearly bonding over this one."),
        _("%s and %s share a knowing smile."),
        _("%s nudges %s, both of them grinning."),
    ]

    NHIE_SHOCK_NARRATION = [
        _("%s stares at %s, clearly taken aback."),
        _("%s looks at %s differently now."),
        _("You notice %s's expression shift as she processes what %s just admitted."),
    ]

    NHIE_SHOCK_DIALOGUE = {
        "loyal": [
            _("I really didn't expect that from you."),
            _("Wow. That changes how I see you, honestly."),
        ],
        "cute_sex": [
            _("That's... intense. Are you sure you're okay with sharing that?"),
            _("I don't know what to say to that..."),
        ],
        "default": [
            _("Okay, that one surprised me."),
            _("I'm going to pretend I didn't hear that."),
            _("Noted. Filing that one away."),
        ],
    }

    NHIE_LOVE_LOSS_NARRATION = [
        _("%s's smile fades. Something about that hit close to home."),
        _("%s goes quiet, staring at her glass."),
    ]

    NHIE_LOVE_LOSS_GF_DIALOGUE = [
        _("Wait... you did that with someone else?"),
        _("I thought... I thought I was special to you."),
        _("That's not what I wanted to hear tonight."),
    ]

    NHIE_LOVE_LOSS_CRUSH_DIALOGUE = [
        _("Oh. I see how it is."),
        _("Good for you, I guess."),
        _("...right."),
    ]

    NHIE_LOYALTY_NARRATION = [
        _("%s looks like she immediately regrets saying that out loud."),
        _("%s covers her face with her hands, embarrassed."),
    ]

    NHIE_NPC_COLD_NARRATION = [
        _("%s gives you a cold, measured look after that one."),
        _("%s's jaw tightens. You can tell that didn't sit well."),
        _("%s shifts uncomfortably, eyes narrowing in your direction."),
    ]

    def _nhie_apply_all_consequences(stmt, girls, drinkers, npc):
        _cat = stmt["category"]
        _defaults = dict(NHIE_CAT_CONSEQUENCES.get(_cat, NHIE_CAT_CONSEQUENCES["safe"]))
        _overrides = NHIE_STMT_OVERRIDES.get(stmt["id"], {})
        _cons = dict(_defaults)
        _cons.update(_overrides)

        results = {
            "bonds": [],
            "shocks": [],
            "love_losses": [],
            "player_love_losses": [],   # rival jealousy caused by the PLAYER's own confession (verbal reaction handled in-round)
            "loyalty_losses": [],
            "inbt_changes": [],
            "obed_changes": [],
            "shared_love_changes": [],
            "npc_friendship_change": 0,
            "cheating_revealed": [],
        }

        _drinker_girls = [g for g in girls if drinkers.get(g.gid, False)]
        _sober_girls = [g for g in girls if not drinkers.get(g.gid, False)]
        _player_drank = drinkers.get("player", False)

        _kmap = NHIE_KNOWLEDGE_MAP.get(stmt["id"])
        _is_with_player = _kmap[1] if _kmap else False

        _trait_map = NHIE_TRAIT_REACTIONS.get(stmt["id"], {})

        # Girl_like bonding between co-drinkers
        _bond = _cons.get("girl_like_bond", 0)
        _bond_traits = _trait_map.get("bond", [])
        if _bond > 0 and len(_drinker_girls) >= 2:
            for i, g1 in enumerate(_drinker_girls):
                for g2 in _drinker_girls[i+1:]:
                    _amt = _bond
                    _bt_found = False
                    for _t in _bond_traits:
                        if g1.has_trait(_t) and g2.has_trait(_t):
                            _amt = int(_amt * 1.5)
                            _bt_found = True
                            break
                        elif g1.has_trait(_t) or g2.has_trait(_t):
                            _amt += 2
                            _bt_found = True
                            break
                    if not _bt_found:
                        if g1.has_trait("exhibitionist") or g2.has_trait("exhibitionist"):
                            _amt += 2
                        if g1.has_trait("hardcore_sex") or g2.has_trait("hardcore_sex"):
                            _amt += 2
                    g1.add_like_for(g2.gid, _amt)
                    g2.add_like_for(g1.gid, _amt)
                    results["bonds"].append((g1, g2, _amt))
                    print("[NHIE-CONS] Bond: %s <-> %s +%d" % (g1.gid, g2.gid, _amt))

        # Girl_like shock (non-drinkers react to drinkers)
        _shock_base = _cons.get("girl_like_shock", 0)
        _shock_traits = _trait_map.get("shock", [])
        _unfazed_traits = _trait_map.get("unfazed", [])
        if _shock_base < 0 and _drinker_girls and _sober_girls:
            for watcher in _sober_girls:
                for revealer in _drinker_girls:
                    _amt = _shock_base
                    _found = False
                    for _t in _shock_traits:
                        if watcher.has_trait(_t):
                            _amt = int(_amt * 1.8)
                            _found = True
                            break
                    if not _found:
                        for _t in _unfazed_traits:
                            if watcher.has_trait(_t):
                                _amt = int(_amt * 0.3)
                                _found = True
                                break
                    if not _found:
                        if watcher.has_trait("loyal"):
                            _amt = int(_amt * 1.5)
                        elif watcher.has_trait("cute_sex"):
                            _amt = int(_amt * 1.3)
                        elif watcher.has_trait("cheater"):
                            _amt = int(_amt * 0.4)
                        elif watcher.has_trait("hardcore_sex") or watcher.has_trait("exhibitionist"):
                            _amt = int(_amt * 0.6)
                    watcher.add_like_for(revealer.gid, _amt)
                    results["shocks"].append((watcher, revealer, _amt))
                    print("[NHIE-CONS] Shock: %s -> %s %d" % (watcher.gid, revealer.gid, _amt))

        # Love loss from rival jealousy (with_player revelations)
        _love_rival = _cons.get("love_rival", 0)
        if _love_rival < 0 and _is_with_player and _drinker_girls:
            for watcher in _sober_girls:
                if not (watcher.Love > 200 or watcher.is_dating_player()):
                    continue
                _amt = _love_rival
                if watcher.has_trait("monogamous"):
                    _amt = int(_amt * 1.5)
                elif watcher.has_trait("polyamorous"):
                    _amt = int(_amt * 0.3)
                if watcher.is_dating_player():
                    _amt = int(_amt * 1.5)
                Change_Status(watcher, "Love", _amt)
                results["love_losses"].append((watcher, _amt))
                print("[NHIE-CONS] Love loss: %s %d" % (watcher.gid, _amt))

        # Love loss when the PLAYER confesses a sexual/nuclear act and a girl who
        # cares about him did NOT share it (she wasn't the one). Same scale as
        # love_rival above; girls who also drank get shared_love instead.
        if _love_rival < 0 and _player_drank and _cat in ("sexual", "nuclear"):
            for watcher in _sober_girls:
                if not (watcher.Love > 200 or watcher.is_dating_player()):
                    continue
                _amt = _love_rival
                if watcher.has_trait("monogamous"):
                    _amt = int(_amt * 1.5)
                elif watcher.has_trait("polyamorous"):
                    _amt = int(_amt * 0.3)
                if watcher.is_dating_player():
                    _amt = int(_amt * 1.5)
                Change_Status(watcher, "Love", _amt)
                results["player_love_losses"].append((watcher, _amt))
                print("[NHIE-CONS] Love loss (player confession): %s %d" % (watcher.gid, _amt))

        # bf_loyalty erosion for drinkers with NPC partners
        _loyalty = _cons.get("bf_loyalty", 0)
        if _loyalty < 0:
            for g in _drinker_girls:
                if not g.has_npc_partner():
                    continue
                _amt = _loyalty
                if g.has_trait("loyal"):
                    _amt = int(_amt * 0.5)
                elif g.has_trait("cheater"):
                    _amt = int(_amt * 1.5)
                g.change_bf_loyalty(_amt)
                results["loyalty_losses"].append((g, _amt))
                print("[NHIE-CONS] bf_loyalty: %s %d -> %d" % (g.gid, _amt, g.bf_loyalty))

        # NPC friendship_with_player when player drinks on sexual/nuclear
        _npc_friend = _cons.get("npc_friendship", 0)
        if npc and _player_drank and _npc_friend < 0:
            _amt = _npc_friend
            _npc_gf_gid = getattr(npc, "girl_gid", None)
            if _npc_gf_gid and _is_with_player:
                for g in _drinker_girls:
                    if g.gid == _npc_gf_gid:
                        _amt = int(_amt * 2)
                        break
            npc.change_friendship(_amt)   # mirrors into girl._npc_friendship
            results["npc_friendship_change"] = _amt
            print("[NHIE-CONS] NPC friendship: %d -> %d" % (_amt, npc.friendship_with_player))

        # Cheating knowledge propagation
        _cheat_stmts = {"cheated_partner"}
        if stmt["id"] in _cheat_stmts:
            for g in _drinker_girls:
                if g.has_npc_partner() or getattr(g, "CheatMaxTier", 0) > 0:
                    for other in girls:
                        if other.gid != g.gid:
                            girl_learns_cheating(other, g)
                    results["cheating_revealed"].append(g)
                    print("[NHIE-CONS] Cheating revealed: %s" % g.gid)

        # Player Inbt: all girls get +Inbt when player reveals bold/dark things
        _p_inbt = _cons.get("player_inbt", 0)
        if _p_inbt > 0 and _player_drank:
            for g in girls:
                _amt = _p_inbt
                if g.has_trait("cute_sex"):
                    _amt = int(_amt * 1.5)
                elif g.has_trait("hardcore_sex") or g.has_trait("exhibitionist"):
                    _amt = int(_amt * 0.5)
                Change_Status(g, "Inbt", _amt, show_popup=False)   # keeps _girl_save in sync
                results["inbt_changes"].append((g, _amt))
                print("[NHIE-CONS] Inbt: %s +%d -> %d" % (g.gid, _amt, g.Inbt))

        # Girl Obed: drinker girls get +Obed from exposing themselves
        _g_obed = _cons.get("girl_obed", 0)
        if _g_obed > 0:
            for g in _drinker_girls:
                _amt = _g_obed
                if g.has_trait("cute_sex") or g.has_trait("loyal"):
                    _amt = int(_amt * 1.3)
                elif g.has_trait("exhibitionist"):
                    _amt = int(_amt * 0.5)
                elif g.has_trait("hardcore_sex"):
                    _amt = int(_amt * 0.7)
                Change_Status(g, "Obed", _amt, show_popup=False)
                results["obed_changes"].append((g, _amt))
                print("[NHIE-CONS] Obed: %s +%d -> %d" % (g.gid, _amt, g.Obed))

        # Shared Love: bonding when both player AND girl drank on same thing
        _s_love = _cons.get("shared_love", 0)
        if _s_love > 0 and _player_drank:
            for g in _drinker_girls:
                _amt = _s_love
                Change_Status(g, "Love", _amt, show_popup=False)
                results["shared_love_changes"].append((g, _amt))
                print("[NHIE-CONS] Shared Love: %s +%d -> %d" % (g.gid, _amt, g.Love))

        return results

    def _nhie_pick_reactions(cons):
        reactions = []

        if cons["shocks"]:
            _worst = min(cons["shocks"], key=lambda x: x[2])
            if _worst[2] <= -8:
                reactions.append(("shock", _worst))

        if cons["love_losses"]:
            _worst = min(cons["love_losses"], key=lambda x: x[1])
            if _worst[1] <= -8:
                reactions.append(("love_loss", _worst))

        if cons["npc_friendship_change"] <= -5:
            reactions.append(("npc_cold", cons["npc_friendship_change"]))

        if cons["loyalty_losses"]:
            _worst = min(cons["loyalty_losses"], key=lambda x: x[1])
            if _worst[1] <= -10:
                reactions.append(("loyalty", _worst))

        if cons["bonds"]:
            _best = max(cons["bonds"], key=lambda x: x[2])
            if _best[2] >= 5:
                reactions.append(("bond", _best))

        return reactions[:2]


# ======================================================================
# ROUND LABEL
# ======================================================================

label nhie_round:

    python:
        if not hasattr(store, "_nhie_used_ids") or store._nhie_used_ids is None:
            store._nhie_used_ids = set()

        _nhie_girls = _hangout_girls_list()
        _nhie_has_npc = _npc_is_active()
        _nhie_npc_obj = getattr(store, "_h_npc", None) if _nhie_has_npc else None

        _nhie_turns = [("player", None)]
        for _ng in _nhie_girls:
            _nhie_turns.append(("girl", _ng))
        if _nhie_has_npc and _nhie_npc_obj:
            _nhie_turns.append(("npc", _nhie_npc_obj))

        _nhie_tidx = 0
        _nhie_stmt = None

        print("[NHIE] Round start: %d turns, npc=%s, girls=%s" % (
            len(_nhie_turns), _nhie_has_npc,
            [g.gid for g in _nhie_girls]))

    $ Narration(_("A new round of Never Have I Ever begins. Everyone raises their glass."))

    label .nhie_turn:
        if _nhie_tidx >= len(_nhie_turns):
            jump .nhie_end_round

        python:
            _nhie_ttype, _nhie_tobj = _nhie_turns[_nhie_tidx]
            print("[NHIE] Turn %d: %s (%s)" % (
                _nhie_tidx, _nhie_ttype,
                getattr(_nhie_tobj, "Name", "player") if _nhie_tobj else "player"))

        if _nhie_ttype == "player":
            jump .nhie_player_turn
        elif _nhie_ttype == "npc":
            jump .nhie_npc_turn
        else:
            jump .nhie_girl_turn

    # ------ PLAYER TURN ------

    label .nhie_player_turn:
        python:
            _p_alc = hangout_get_player_alcohol()
            _nhie_all_items = _nhie_player_menu_items(store._nhie_used_ids, _nhie_has_npc, _p_alc)
            _nhie_has_available = any(not lk for _, lk in _nhie_all_items)

        if not _nhie_has_available:
            $ Narration(_("You can't think of anything new to say. The round ends here."))
            jump .nhie_end_round

        python:
            _nhie_menu_items = []
            for _ms, _mlocked in _nhie_all_items:
                if _mlocked:
                    _lt = "{color=#666}" + _tl(_ms["text"]) + " {size=-4}{i}(" + _tl(_("need to be drunker")) + "){/i}{/size}{/color}"
                    _nhie_menu_items.append((_lt, None))
                else:
                    _nhie_menu_items.append((_tl(_ms["text"]), _ms["id"]))

        $ store._menu_scroll_threshold = 7
        $ renpy.say(None, _tl(_("Never have I ever...")), interact=False)
        $ _nhie_picked_id = renpy.display_menu(_nhie_menu_items)
        $ store._menu_scroll_threshold = 14

        python:
            # Public copy only: raw entries carry lambdas and _nhie_stmt is a store var (pickled)
            _nhie_stmt = _nhie_public(NHIE_BY_ID.get(_nhie_picked_id))
            store._nhie_used_ids.add(_nhie_picked_id)
            store._nhie_action = fmt_safe(_tl(_nhie_stmt["text"]), gender_fmt(False))      # the player says it

        $ Say_Player(_("Never have I ever [_nhie_action]"))

        jump .nhie_check_drinks

    # ------ GIRL TURN ------

    label .nhie_girl_turn:
        python:
            _nhie_stmt = _nhie_pick_for_girl(_nhie_tobj, store._nhie_used_ids, _nhie_has_npc)
            if _nhie_stmt:
                store._nhie_used_ids.add(_nhie_stmt["id"])

        if _nhie_stmt is None:
            $ _nhie_skip_name = getattr(_nhie_tobj, "Name", "?")
            $ Narration(_("[_nhie_skip_name] thinks for a moment but can't come up with anything."))
            $ _nhie_tidx += 1
            jump .nhie_turn

        $ set_scene_expression(_nhie_tobj, NHIE_SPEAK_EXPR.get(_nhie_stmt["category"], "smirk"))
        $ store._nhie_action = fmt_safe(_tl(_nhie_stmt["text"]), gender_fmt(True))      # a girl says it
        $ Say_Line(_nhie_tobj, _("Never have I ever [_nhie_action]"))

        jump .nhie_check_drinks

    # ------ NPC TURN ------

    label .nhie_npc_turn:
        python:
            _nhie_gf = None
            for _ng2 in _nhie_girls:
                if _ng2.has_npc_partner() and getattr(_nhie_npc_obj, "girl_gid", None) == _ng2.gid:
                    _nhie_gf = _ng2
                    break
            if not _nhie_gf and _nhie_girls:
                _nhie_gf = _nhie_girls[0]
            _nhie_stmt = _nhie_pick_for_npc(_nhie_npc_obj, _nhie_gf, store._nhie_used_ids)
            if _nhie_stmt:
                store._nhie_used_ids.add(_nhie_stmt["id"])

        if _nhie_stmt is None:
            $ _nhie_npc_skip = getattr(_nhie_npc_obj, "Name", "?")
            $ Narration(_("[_nhie_npc_skip] shrugs and passes."))
            $ _nhie_tidx += 1
            jump .nhie_turn

        $ store._nhie_action = fmt_safe(_tl(_nhie_stmt["text"]), gender_fmt(getattr(_nhie_npc_obj, "gender", "male") == "female"))
        $ Character(_nhie_npc_obj.Name, color=_nhie_npc_obj.color)(_tl(_("Never have I ever [_nhie_action]")))

        jump .nhie_check_drinks

    # ------ CHECK WHO DRINKS ------

    label .nhie_check_drinks:
        python:
            _nhie_drinkers = _nhie_check_all(_nhie_stmt, _nhie_girls, _nhie_npc_obj if _nhie_has_npc else None)
            print("[NHIE] Drinkers (truth): %s" % {k: v for k, v in _nhie_drinkers.items()})

            # -- The player CHOOSES whether to drink. The game keeps the truth. --
            _nhie_truth = bool(_nhie_drinkers.get("player", False))
            _nhie_show_menu = True
            _nhie_opt_drink = _tl(_("Take a drink")) + " {size=-4}{color=#8ca0b4}" + (_tl(_("(you have)")) if _nhie_truth else _tl(_("(bluff)"))) + "{/color}{/size}"
            _nhie_opt_pass = _tl(_("Don't drink")) + " {size=-4}{color=#8ca0b4}" + (_tl(_("(lie)")) if _nhie_truth else _tl(_("(you haven't)"))) + "{/color}{/size}"

        if _nhie_show_menu:
            menu:
                "[_nhie_opt_drink]":
                    $ _nhie_drinkers["player"] = True
                "[_nhie_opt_pass]":
                    $ _nhie_drinkers["player"] = False

        python:
            _nhie_player_lied = _nhie_truth and not _nhie_drinkers.get("player", False)
            _nhie_player_bluffed = (not _nhie_truth) and _nhie_drinkers.get("player", False)
            if _nhie_player_lied:
                store.Player._nhie_lies = getattr(store.Player, "_nhie_lies", 0) + 1
            if _nhie_player_bluffed:
                store.Player._nhie_bluffs = getattr(store.Player, "_nhie_bluffs", 0) + 1
            _nhie_any_drank = any(_nhie_drinkers.values())   # recomputed after the choice
            _nhie_lie_spoken = None
            _nhie_lie_narr = []
            print("[NHIE-LIE] stmt=%s truth=%s drank=%s lied=%s bluffed=%s (lies=%d caught=%d bluffs=%d)" % (
                _nhie_stmt["id"], _nhie_truth, _nhie_drinkers.get("player", False), _nhie_player_lied, _nhie_player_bluffed,
                getattr(store.Player, "_nhie_lies", 0), getattr(store.Player, "_nhie_lies_caught", 0), getattr(store.Player, "_nhie_bluffs", 0)))

        # -- Player passes (truth or lie) --
        if _nhie_show_menu and not _nhie_drinkers.get("player", False):
            $ Narration(_tl(renpy.random.choice(NHIE_PLAYER_PASS_LINES)))

            if _nhie_player_lied:
                # Girls who KNOW he should have drunk
                python:
                    _nhie_lie_spoken, _nhie_lie_narr = _nhie_lie_reactions(_nhie_stmt, _nhie_girls)

                if _nhie_lie_spoken is not None:
                    python:
                        _nhie_lg, _nhie_lexpr, _nhie_lblush, _nhie_lline = _nhie_lie_spoken
                        # Caught: she feels hidden / dismissed; the table sees him flinch
                        _nhie_l_love = NHIE_LIE_CAUGHT_LOVE.get(_nhie_stmt["category"], -3)
                        if _nhie_lg.is_dating_player():
                            _nhie_l_love = int(_nhie_l_love * 1.5)
                        Change_Status(_nhie_lg, "Love", _nhie_l_love, show_popup=False)
                        for _lw in _nhie_girls:
                            Change_Status(_lw, "Inbt", -3, show_popup=False)
                        store.Player._nhie_lies_caught = getattr(store.Player, "_nhie_lies_caught", 0) + 1
                        print("[NHIE-LIE] CAUGHT by %s: Love %d, table Inbt -3" % (_nhie_lg.gid, _nhie_l_love))
                    $ set_scene_expression(_nhie_lg, _nhie_lexpr, blush=_nhie_lblush)
                    $ Say_Line(_nhie_lg, _tl(_nhie_lline))

                if _nhie_lie_narr:
                    python:
                        _nhie_ng, _nhie_nexpr, _nhie_nblush, _nhie_ntext = _nhie_lie_narr[0]
                    $ set_scene_expression(_nhie_ng, _nhie_nexpr, blush=_nhie_nblush)
                    $ Narration(_nhie_ntext)

        if not _nhie_any_drank:
            # A call-out ("Liar. Drink.") already filled this beat; "nobody's guilty" would contradict it
            if _nhie_lie_spoken is None:
                $ Narration(_tl(renpy.random.choice(NHIE_NOBODY_LINES)))
            # Still show girl skip reactions even when nobody drank
            $ print("[NHIE] Nobody drank -> showing skip reactions for all girls")
            $ store._nhie_round_lines = set()
            $ _nhie_gi = 0
            jump .nhie_girl_drink_loop

        # -- Player drinks (confession, or a bluff everyone believes) --
        if _nhie_drinkers.get("player", False):
            $ tod_drink_player(1)
            $ Narration(_tl(renpy.random.choice(NHIE_PLAYER_DRINK_LINES.get(_nhie_stmt["category"], NHIE_PLAYER_DRINK_LINES["safe"]))))

            if _nhie_player_bluffed:
                python:
                    _nhie_bd = _nhie_bluff_doubt(_nhie_stmt, _nhie_girls)
                if _nhie_bd is not None:
                    python:
                        _nhie_bd_girl, _nhie_bd_line = _nhie_bd
                    $ set_scene_expression(_nhie_bd_girl, "smirk")
                    $ Say_Line(_nhie_bd_girl, _tl(_nhie_bd_line))

            # Girls the confession is ABOUT react first (nervous/blushing, or suspicious)
            python:
                _nhie_impl = _nhie_implicated_reactions(_nhie_stmt, _nhie_girls, _nhie_drinkers)
                _nhie_impl_gids = set(_ig.gid for _ig, _, _, _ in _nhie_impl)
                _nhie_ii = 0

            label .nhie_implicated_loop:
                if _nhie_ii >= len(_nhie_impl):
                    jump .nhie_after_implicated
                python:
                    _nhie_ig, _nhie_iexpr, _nhie_iblush, _nhie_iline = _nhie_impl[_nhie_ii]
                $ set_scene_expression(_nhie_ig, _nhie_iexpr, blush=_nhie_iblush)
                $ Say_Line(_nhie_ig, _tl(_nhie_iline))
                $ _nhie_ii += 1
                jump .nhie_implicated_loop

            label .nhie_after_implicated:
                pass

            # Then one other girl reacts to the confession (sexual/nuclear only)
            python:
                _nhie_pc_react = _nhie_player_confess_reaction(_nhie_stmt, _nhie_girls, _nhie_drinkers, _nhie_npc_obj if _nhie_has_npc else None, exclude=_nhie_impl_gids)
            if _nhie_pc_react is not None:
                python:
                    _nhie_pc_girl, _nhie_pc_expr, _nhie_pc_line = _nhie_pc_react
                $ set_scene_expression(_nhie_pc_girl, _nhie_pc_expr)
                $ Say_Line(_nhie_pc_girl, _tl(_nhie_pc_line))

        # -- Girls drink (iterate) --
        $ store._nhie_round_lines = set()
        $ _nhie_gi = 0

        label .nhie_girl_drink_loop:
            if _nhie_gi >= len(_nhie_girls):
                jump .nhie_npc_drink

            python:
                _nhie_rg = _nhie_girls[_nhie_gi]
                _nhie_rg_drank = _nhie_drinkers.get(_nhie_rg.gid, False)
                print("[NHIE-GIRL-LOOP] gi=%d gid=%s drank=%s" % (_nhie_gi, _nhie_rg.gid, _nhie_rg_drank))

            if _nhie_rg_drank:
                $ tod_drink(_nhie_rg, 1)
                if _nhie_ttype == "girl" and _nhie_rg is _nhie_tobj:
                    python:
                        _nhie_player_learns(_nhie_stmt, _nhie_rg)
                        print("[NHIE-GIRL-LOOP] %s DRINK (proposer, silent sip)" % _nhie_rg.gid)
                    $ set_scene_expression(_nhie_rg, "smirk")
                    "[_nhie_rg.Name] quietly takes a sip, smiling at her own question."
                else:
                    python:
                        _nhie_rexpr, _nhie_rline = _nhie_girl_drink_reaction(_nhie_rg, _nhie_stmt)
                        _nhie_player_learns(_nhie_stmt, _nhie_rg)
                        print("[NHIE-GIRL-LOOP] %s DRINK: expr=%s line=%s" % (_nhie_rg.gid, _nhie_rexpr, _nhie_rline[:40]))
                    $ set_scene_expression(_nhie_rg, _nhie_rexpr)
                    $ Say_Line(_nhie_rg, _tl(_nhie_rline))
            else:
                python:
                    _nhie_skip = _nhie_girl_skip_reaction(_nhie_rg, _nhie_stmt)
                    print("[NHIE-GIRL-LOOP] %s SKIP: reaction=%s" % (_nhie_rg.gid, _nhie_skip[1][:40] if _nhie_skip else "None"))
                if _nhie_skip is not None:
                    python:
                        _nhie_sexpr, _nhie_sline = _nhie_skip
                    $ set_scene_expression(_nhie_rg, _nhie_sexpr)
                    $ Say_Line(_nhie_rg, _tl(_nhie_sline))

            $ _nhie_gi += 1
            jump .nhie_girl_drink_loop

        # -- NPC drinks + drama --
        label .nhie_npc_drink:
            if not _nhie_has_npc:
                jump .nhie_knowledge

            if _nhie_drinkers.get("npc", False):
                $ tod_drink(_nhie_npc_obj, 1)
                $ Character(_nhie_npc_obj.Name, color=_nhie_npc_obj.color)(_tl(renpy.random.choice(NHIE_NPC_DRINK_LINES)))

            # NPC drama: girlfriend drank on sexual/nuclear
            if _nhie_stmt["category"] in ("sexual", "nuclear"):
                python:
                    _nhie_gf_reacted = None
                    for _ng3 in _nhie_girls:
                        if _nhie_drinkers.get(_ng3.gid, False) and _ng3.has_npc_partner():
                            if getattr(_nhie_npc_obj, "girl_gid", None) == _ng3.gid:
                                _nhie_gf_reacted = _ng3
                                break

                if _nhie_gf_reacted is not None:
                    python:
                        _nhie_p_also = _nhie_drinkers.get("player", False)
                        _nhie_drama_line, _nhie_drama_susp = _nhie_npc_drama(_nhie_npc_obj, _nhie_gf_reacted, _nhie_stmt, _nhie_p_also)
                    if _nhie_drama_line is not None:
                        $ Character(_nhie_npc_obj.Name, color=_nhie_npc_obj.color)(_tl(_nhie_drama_line))
                        if _nhie_drama_susp > 0:
                            $ _nhie_npc_obj.suspicion = min(100, getattr(_nhie_npc_obj, "suspicion", 0) + _nhie_drama_susp)
                            $ _nhie_gf_reacted._npc_suspicion = _nhie_npc_obj.suspicion
                            $ print("[NHIE] NPC suspicion +%d -> %d" % (_nhie_drama_susp, _nhie_npc_obj.suspicion))

                        $ _nhie_update_npc_love(_nhie_npc_obj, _nhie_stmt, _nhie_drinkers.get("player", False))

                        # GF answers her partner (trait-flavored: cheater deflects, loyal apologizes)
                        python:
                            _nhie_gfd_expr, _nhie_gfd_line = _nhie_gf_defend_line(_nhie_gf_reacted)
                        $ set_scene_expression(_nhie_gf_reacted, _nhie_gfd_expr)
                        $ Say_Line(_nhie_gf_reacted, _tl(_nhie_gfd_line))
                    else:
                        $ set_scene_expression(_nhie_gf_reacted, "worried")

        # -- Knowledge propagation + Jealousy --
        label .nhie_knowledge:
            $ _nhie_propagate_knowledge(_nhie_stmt, _nhie_girls, _nhie_drinkers)

            python:
                _nhie_jealous_list = _nhie_check_jealousy(_nhie_stmt, _nhie_girls, _nhie_drinkers)
                _nhie_ji = 0

        label .nhie_jealousy_loop:
            if _nhie_ji >= len(_nhie_jealous_list):
                jump .nhie_consequences

            python:
                _nhie_jw, _nhie_jd, _nhie_ja = _nhie_jealous_list[_nhie_ji]

            if _nhie_ja >= 10:
                $ set_scene_expression(_nhie_jw, "angry")
            else:
                $ set_scene_expression(_nhie_jw, "worried")

            if _nhie_jw.is_dating_player():
                $ Say_Line(_nhie_jw, _tl(renpy.random.choice(NHIE_JEALOUSY_GF)))
            else:
                $ Say_Line(_nhie_jw, _tl(renpy.random.choice(NHIE_JEALOUSY_CRUSH)))

            $ _nhie_ji += 1
            jump .nhie_jealousy_loop

        # -- Consequences: friendship, loyalty, love changes + reactions --
        label .nhie_consequences:
            python:
                _nhie_cons = _nhie_apply_all_consequences(_nhie_stmt, _nhie_girls, _nhie_drinkers, _nhie_npc_obj if _nhie_has_npc else None)
                _nhie_reactions = _nhie_pick_reactions(_nhie_cons)
                _nhie_ri = 0

        label .nhie_reaction_loop:
            if _nhie_ri >= len(_nhie_reactions):
                jump .nhie_after_drinks

            python:
                _nhie_rtype, _nhie_rdata = _nhie_reactions[_nhie_ri]

            if _nhie_rtype == "shock":
                python:
                    _nhie_r_watcher, _nhie_r_revealer, _nhie_r_amt = _nhie_rdata
                $ Narration(_tl(renpy.random.choice(NHIE_SHOCK_NARRATION)) % (_nhie_r_watcher.Name, _nhie_r_revealer.Name))
                python:
                    if _nhie_r_watcher.has_trait("loyal"):
                        _nhie_r_pool = NHIE_SHOCK_DIALOGUE["loyal"]
                    elif _nhie_r_watcher.has_trait("cute_sex"):
                        _nhie_r_pool = NHIE_SHOCK_DIALOGUE["cute_sex"]
                    else:
                        _nhie_r_pool = NHIE_SHOCK_DIALOGUE["default"]
                $ set_scene_expression(_nhie_r_watcher, "uncomfortable")
                $ Say_Line(_nhie_r_watcher, _tl(renpy.random.choice(_nhie_r_pool)))

            elif _nhie_rtype == "love_loss":
                python:
                    _nhie_r_lg, _nhie_r_lamt = _nhie_rdata
                $ Narration(_tl(renpy.random.choice(NHIE_LOVE_LOSS_NARRATION)) % _nhie_r_lg.Name)
                if _nhie_r_lg.is_dating_player():
                    $ set_scene_expression(_nhie_r_lg, "sad")
                    $ Say_Line(_nhie_r_lg, _tl(renpy.random.choice(NHIE_LOVE_LOSS_GF_DIALOGUE)))
                else:
                    $ set_scene_expression(_nhie_r_lg, "worried")
                    $ Say_Line(_nhie_r_lg, _tl(renpy.random.choice(NHIE_LOVE_LOSS_CRUSH_DIALOGUE)))

            elif _nhie_rtype == "npc_cold":
                if _nhie_npc_obj is not None:
                    $ Narration(_tl(renpy.random.choice(NHIE_NPC_COLD_NARRATION)) % _nhie_npc_obj.Name)

            elif _nhie_rtype == "loyalty":
                python:
                    _nhie_r_loyg, _nhie_r_loyamt = _nhie_rdata
                $ set_scene_expression(_nhie_r_loyg, "embarrassed")
                $ Narration(_tl(renpy.random.choice(NHIE_LOYALTY_NARRATION)) % _nhie_r_loyg.Name)

            elif _nhie_rtype == "bond":
                python:
                    _nhie_r_bg1, _nhie_r_bg2, _nhie_r_bamt = _nhie_rdata
                $ Narration(_tl(renpy.random.choice(NHIE_BOND_NARRATION)) % (_nhie_r_bg1.Name, _nhie_r_bg2.Name))

            $ _nhie_ri += 1
            jump .nhie_reaction_loop

        label .nhie_after_drinks:
            $ _nhie_tidx += 1
            jump .nhie_turn

    # ------ END OF ROUND ------

    label .nhie_end_round:
        $ Narration(_("The round is over. Everyone takes a sip to wrap things up."))

        python:
            tod_drink_player(1)
            for _ng4 in _hangout_girls_list():
                tod_drink(_ng4, 1)

            _nhie_npc_sick = False
            if _npc_is_active():
                tod_drink(store._h_npc, 1)
                if tod_rolls_sick(store._h_npc):
                    _nhie_npc_sick = True

            _nhie_sick_who = None
            if tod_player_rolls_sick():
                _nhie_sick_who = "player"
            else:
                for _ng5 in _hangout_girls_list():
                    if tod_rolls_sick(_ng5):
                        _nhie_sick_who = _ng5
                        break

            print("[NHIE-ROUND-END] npc_sick=%s sick_who=%s" % (_nhie_npc_sick, _nhie_sick_who))

        if _nhie_npc_sick:
            $ print("[NHIE-ROUND-END] NPC pass-out (girls=%d)" % len(_hangout_girls_list()))
            if len(_hangout_girls_list()) == 1:
                call _npc_pass_out_1girl_event from _call_npc_po_1g_nhie
            else:
                call _npc_pass_out_event from _call_npc_po_nhie

        if _nhie_sick_who is not None:
            call _tod_get_sick(_nhie_sick_who) from _call_nhie_get_sick

        $ print("[NHIE-ROUND-END] Returning from nhie_round")
        return
