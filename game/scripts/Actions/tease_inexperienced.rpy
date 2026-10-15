# ============================================================
# tease_inexperienced.rpy — "Low experience" tease reactions
# ============================================================
#
# Adds "_first" / "_new" reaction keys to existing TEASE_OPTIONS entries.
# The resolver in tease.rpy tries trait_discovery_keys() before the trait:
# "<trait>_first" (her very first time, trait_is_first) then "<trait>_new"
# (her first few times, trait_is_new). Falls back to the experienced pool
# when no discovery key exists for a given tease.
# A line that says "my first time" / "I've never" goes in "_first" ONLY:
# "_new" also plays on her 2nd and 3rd time.
#
# These reactions are for girls who HAVE the trait but haven't
# done the relevant act enough to reference past experience.
# Same stat changes as the experienced version (the balance
# system handles the rest).
# ============================================================

init 1 python:

    # ── cum_threat: cum_slut discovering she wants it ─────────
    if "cum_threat" in TEASE_OPTIONS:
        TEASE_OPTIONS["cum_threat"]["reactions"]["cum_slut_first"] = {
            "lines": [
                _("You're going to... inside me? I've never... oh god, yes, I want to find out what it feels like..."),
                _("I've been thinking about this... what it would be like... please, I want to know..."),
                _("I've never felt that before... but something about the idea makes me... please do it..."),
            ],
            "stats": {"Inbt": 8, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["cum_threat"]["reactions"]["cum_slut_new"] = {
            "lines": [
                _("Inside me? I... yes. I don't know why I want it this badly, but I do."),
                _("Don't tease me like that... I'm still figuring out how much I want it. A lot. The answer is a lot."),
                _("Oh god... say that again. I can't believe how much I want it."),
            ],
            "stats": {"Inbt": 8, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["cum_threat"]["reactions"]["hate_cum_new"] = {
            "lines": [
                _("Don't! I've always been grossed out by that... please keep it away from me!"),
                _("I don't want to find out what that feels like! Pull out when you're close!"),
                _("I've never dealt with that and I don't want to start now! Keep it away!"),
            ],
            "stats": {"Love": -5, "Obed": -3},
            "expression": "angry",
        }

    # ── cum_threat (anal reactions): discovering anal cum ──────
    if "cum_threat" in TEASE_OPTIONS and "reactions_anal" in TEASE_OPTIONS["cum_threat"]:
        TEASE_OPTIONS["cum_threat"]["reactions_anal"]["anal_lover_first"] = {
            "lines": [
                _("In my... back there? I've never... but I want to know what it feels like..."),
                _("I've never felt that before... inside there... but the idea is making me so excited..."),
                _("You want to finish in there? I've never tried that... but yes. I want to experience it."),
            ],
            "stats": {"Inbt": 8, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["cum_threat"]["reactions_anal"]["anal_lover_new"] = {
            "lines": [
                _("In there? ...Yes. I don't understand why that sounds so good, but it does."),
                _("Finish in my... oh god. I'm still getting used to this and I already want that."),
                _("You want to cum back there? Say it slower... I want to think about it."),
            ],
            "stats": {"Inbt": 8, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["cum_threat"]["reactions_anal"]["anal_hater_new"] = {
            "lines": [
                _("You want to cum in THERE?! I've heard that's even worse! No way!"),
                _("Inside my... no! This is already bad enough without adding THAT to it!"),
                _("Don't you dare! I've never felt that and I don't want to find out!"),
            ],
            "stats": {"Love": -3, "Obed": -2},
            "expression": "angry",
        }

    # ── atm_taste: first time tasting after anal ──────────────
    if "atm_taste" in TEASE_OPTIONS:
        TEASE_OPTIONS["atm_taste"]["reactions"]["anal_lover_first"] = {
            "lines": [
                _("It's... different. I don't know how I feel about it yet... but I'm not going to stop."),
                _("So that's what it tastes like? It's... honestly not as bad as I expected."),
                _("My first time trying this... it's weird. But I'm curious enough to keep going."),
            ],
            "stats": {"Inbt": 5, "Obed": 2},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["anal_lover_new"] = {
            "lines": [
                _("It's... different. I don't know how I feel about it yet... but I'm not going to stop."),
                _("It's so wrong... and I still can't believe I'm into this."),
                _("I don't know what's happening to me... I actually want to keep going."),
            ],
            "stats": {"Inbt": 5, "Obed": 2},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["anal_hater_new"] = {
            "lines": [
                _("I've never... is this what it tastes like?! Oh god that's horrible!"),
                _("I didn't even know people DID this! It's... I think I'm going to be sick..."),
            ],
            # says it was HER ass: _tease_menu leaves it out on a cross ATM (it was another girl's)
            "own_ass_lines": [
                _("That was in my... and now it's in my MOUTH?! This is the worst first time ever!"),
            ],
            "stats": {"Love": -3, "Obed": 2},
            "expression": "angry",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["cum_slut_first"] = {
            "lines": [
                _("That's... a new flavor. I've never tasted anything like... I think I don't mind it?"),
                _("My first time tasting... all of that. It's a lot to process but... not terrible?"),
                _("I didn't expect this to be part of my first experience but... I'm curious about everything."),
            ],
            "stats": {"Inbt": 5, "Obed": 2},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["cum_slut_new"] = {
            "lines": [
                _("Mmm... it's filthy, and I'm still not sure I should like it this much."),
                _("I keep telling myself it's gross... so why don't I want to stop?"),
                _("That taste... I don't get it. I just know I want more of it."),
            ],
            "stats": {"Inbt": 5, "Obed": 2},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["hate_cum_new"] = {
            "lines": [
                _("You want me to taste THAT?! I've never even... ugh! This is my worst nightmare!"),
                _("My mouth was the one safe place and now... oh god the taste... I KNEW I'd hate this!"),
                _("I've always dreaded something like this... and it's even worse than I imagined!"),
            ],
            "stats": {"Love": -5, "Obed": 3},
            "expression": "angry",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["hardcore_sex_first"] = {
            "lines": [
                _("That's... filthy. I didn't think I'd be into something this extreme on my first... but I might be."),
                _("This is way beyond what I expected from a first time... and I'm not stopping. Interesting."),
                _("I've never done anything this intense before. I didn't know I had this in me."),
            ],
            "stats": {"Inbt": 6, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["hardcore_sex_new"] = {
            "lines": [
                _("That's filthy... and I don't hate it. What is happening to me?"),
                _("This is so dirty... and I'm not stopping. I don't even recognize myself."),
                _("I didn't think I'd go this far... and I want to go further."),
            ],
            "stats": {"Inbt": 6, "Obed": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["atm_taste"]["reactions"]["cute_sex_new"] = {
            "lines": [
                _("Why would you... that's so... I've never even... please don't make me..."),
                _("I didn't know people actually... that's... I can't even look at you right now..."),
                _("My first time and you want me to... that's really overwhelming..."),
            ],
            "stats": {"Love": -3, "Obed": 2},
            "expression": "sad",
        }

    # ── breed_talk: cum_slut discovering breeding fantasy ──────
    if "breed_talk" in TEASE_OPTIONS:
        TEASE_OPTIONS["breed_talk"]["reactions"]["cum_slut_first"] = {
            "lines": [
                _("Pregnant? I've never even... but something about you saying that makes me feel..."),
                _("I don't know why, but hearing you say that... even though I've never... it excites me..."),
                _("The idea of being... by you... I've never thought about it before but now I can't stop..."),
            ],
            "stats": {"Inbt": 6, "Obed": 3},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["breed_talk"]["reactions"]["cum_slut_new"] = {
            "lines": [
                _("Don't say things like that... it does something to me and I don't even know why."),
                _("Pregnant? ...God, why does that make me want you to cum even more?"),
                _("I shouldn't like hearing that. I really shouldn't. Say it again."),
            ],
            "stats": {"Inbt": 6, "Obed": 3},
            "expression": "lipbite",
        }

    # ── humiliate: first-time reactions (less veteran pushback) ──
    if "humiliate" in TEASE_OPTIONS:
        TEASE_OPTIONS["humiliate"]["reactions"]["hardcore_sex_first"] = {
            "lines": [
                _("That should bother me but... it's my first time and somehow it doesn't. Say it again."),
                _("I don't know why hearing that turns me on... I've never been called that before..."),
                _("Keep talking like that... I'm discovering things about myself I didn't know..."),
            ],
            "stats": {"Obed": 5, "Inbt": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["humiliate"]["reactions"]["hardcore_sex_new"] = {
            "lines": [
                _("Keep talking like that... I'm discovering things about myself I didn't know..."),
                _("That should make me mad... so why does it make me want you more?"),
                _("Say it again... I'm still getting used to how much I like that."),
            ],
            "stats": {"Obed": 5, "Inbt": 5},
            "expression": "lipbite",
        }
        TEASE_OPTIONS["humiliate"]["reactions"]["cute_sex_new"] = {
            "lines": [
                _("Why would you say that to me... this is my first time... that's so hurtful..."),
                _("I'm already so nervous and you're calling me... that's not fair..."),
                _("Please don't... I've never done this before and you're making me feel terrible..."),
            ],
            "stats": {"Love": -5, "Obed": 3},
            "expression": "sad",
        }
