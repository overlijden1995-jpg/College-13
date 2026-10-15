# ============================================================
# nerd_ramble.rpy... she gets carried away (author's joke: "a nerd yapping for 4 or 5 pages")
# ============================================================
#
# ONCE per run: a rare chance on every face-to-face Chit Chat (label Chit_Chat, ChitChat.rpy) with a girl who has the
# Nerd trait, growing with the days (nerd_ramble_chance). One topic sets her off and she talks for most of the time
# slot. Her "pages" are split by a dip to black (with fade) and a line of narration, and when she finally stops only
# NERD_RAMBLE["leaves"] rounds of the slot are left. Achievement "nerds_talk".
#   NERD_RAMBLES:      gid -> [ramble, ...], "_default" for every other nerd (girl_pool). A ramble = {"id", "pages"}
#   NERD_RAMBLE_ENDS:  gid -> [ending, ...]: she notices the time
#   a line = (face, text) or (face, text, arm): her line (face from POSE_EXPRESSIONS["standing"], arm as in
#            _set_standing_arm: 3 = phone in hand, 4 = hand on hip). face "him" = the player's line, "narr" = narration.
# A nerd knows her facts: every line here is true (or says it is a hypothesis).
# Tenny speaks with her confident voice (canon: astronomy, ancient writing, grandpa's RV and her cousin).
# ============================================================

# The Day it happened (None = not yet this run): it never happens again
default _nerd_ramble_day = None

init python:

    NERD_RAMBLE = {
        "chance": 0.01,      # per face-to-face Chit Chat on Day 1...
        "per_day": 0.005,    # ...plus this for every day after it...
        "max_chance": 0.20,  # ...up to this (Day 39 on)
        "leaves": 10,        # rounds left in the slot when she stops
        "min_eats": 40,      # she only gets carried away with at least this much of the slot to eat
        "love": 6,           # he listened to all of it
    }

    # Before her first page
    NERD_RAMBLE_SPARK = [
        _("Something lights up behind her eyes. You get the feeling you won't be going anywhere for a while."),
        _("She suddenly perks up, like someone flipped a switch."),
        _("Her whole face changes. Whatever she's about to say, she's been dying to say it."),
    ]

    # Between her pages, after the dip to black: [after page 1], [after page 2], [after page 3 and on]
    NERD_RAMBLE_BREAKS = [
        [
            _("Some time later. She hasn't slowed down. If anything, she's speeding up."),
            _("A while later. You nod. You've been nodding for a while now."),
            _("Some time later. You open your mouth to say something. She's already three facts ahead."),
        ],
        [
            _("Much later. She's drawing diagrams in the air with both hands now."),
            _("Much later. You try to say something. She raises one finger. She isn't done."),
            _("Much later. Somewhere along the way, you stopped keeping track of the time."),
        ],
        [
            _("Even later. She takes a breath. You think it's over. It is not over."),
            _("Even later. You've stopped trying to get a word in. Honestly, you're kind of into it now."),
            _("Even later. She hasn't repeated herself once. You're not sure if that's impressive or terrifying."),
        ],
    ]

    NERD_RAMBLES = {
        "tenny": [
            # Olbers' paradox, Poe's Eureka, the cosmic microwave background
            {"id": "night_sky", "pages": [
                [
                    ("thinking", _("Okay, random question. Why is the sky dark at night?"), 4),
                    ("him", _("Because... the sun went down?")),
                    ("smirk", _("Wrong. Well, right. But wrong in the most interesting way possible.")),
                    ("happy", _("Think about it. If the universe went on forever, and it was full of stars everywhere, then every direction you look would end on a star.")),
                    ("serious", _("Every single direction. So the whole sky should be as bright as the surface of the sun. Day AND night.")),
                    ("smile", _("It's called Olbers' paradox. Kepler was already worried about it in 1610. It's named after Olbers because he wrote about it in the 1820s. Classic.")),
                ],
                [
                    ("thinking", _("So people tried to explain it away. Maybe dust blocks the light, right? Clouds of gas and dust between the stars.")),
                    ("smirk", _("Nope. The dust would soak up all that light, heat up, and end up glowing just as bright. You can't hide that much energy. Physics doesn't let you.")),
                    ("happy", _("And here's my favorite part. You know who came up with the right answer first? Edgar Allan Poe.")),
                    ("him", _("The raven guy?")),
                    ("laugh", _("The raven guy! In 1848 he wrote this weird prose poem about the universe called Eureka, and in the middle of it he says the sky is dark because the light from the farthest stars hasn't had time to reach us yet.")),
                    ("serious", _("A horror writer, guessing it decades before anyone could prove it. I think about that a lot.")),
                ],
                [
                    ("normal", _("Because that's the real answer. The universe isn't infinitely old. It's about thirteen point eight billion years old.")),
                    ("thinking", _("So light has only had so long to travel. Past a certain distance, whatever's out there, its light just hasn't gotten here. That's what the observable universe means.")),
                    ("happy", _("And on top of that, space is expanding, so light from really distant galaxies gets stretched on the way here. Out of visible light, into infrared, and further.")),
                    ("him", _("Stretched.")),
                    ("smile", _("Stretched! Redshift. It's kind of like a siren dropping in pitch as it drives away. Kind of. Don't quote me on the 'kind of', the real math is about space itself stretching.")),
                ],
                [
                    ("serious", _("Now here's the part that keeps me up at night. The sky actually IS glowing. In every direction. Just not in a color you can see.")),
                    ("happy", _("The cosmic microwave background. Leftover light from when the whole universe was hot, glowing gas, about three hundred and eighty thousand years after it started.")),
                    ("thinking", _("It's been stretched so much that now it's microwaves. About two point seven degrees above absolute zero. It's everywhere you look. It's behind everything.")),
                    ("happy", _("Hold on, I have the map on my phone. Look at it. That's a baby picture of the entire universe."), 3),
                    ("smirk", _("And the static on old TVs, between channels? A tiny bit of it was that glow. People were watching the leftovers of the Big Bang and complaining there was nothing on."), 4),
                    ("laugh", _("Two guys at Bell Labs found it by accident in the sixties. They thought the noise in their antenna was pigeon droppings. They literally cleaned out the pigeons first.")),
                ],
            ]},
            # Linear A, Alice Kober, Michael Ventris and the palace receipts
            {"id": "lost_scripts", "pages": [
                [
                    ("thinking", _("Can I tell you about the most frustrating thing in the world?"), 4),
                    ("him", _("Is it me?")),
                    ("smirk", _("Today? Second place. First place is Linear A.")),
                    ("happy", _("It's a writing system from Crete. The Minoans used it almost four thousand years ago. We have over a thousand inscriptions. And nobody on Earth can read a single sentence.")),
                    ("serious", _("We understand the numbers. We can tell that a lot of it is lists. But the language itself? Gone. It doesn't match anything we know.")),
                    ("thinking", _("There's one word at the bottom of the lists, next to the sums, that probably means 'total'. Probably. That's about all we've got.")),
                ],
                [
                    ("smile", _("Now, its little sister, Linear B? That one got cracked. And the story is so good.")),
                    ("thinking", _("A woman named Alice Kober spent years sorting its signs into these huge grids. On index cards she cut by hand from scrap paper, because paper was scarce after the war.")),
                    ("sad", _("She died in 1950. Two years before anyone solved it. Her grids are a huge part of why it got solved at all.")),
                    ("happy", _("And the guy who finished it, Michael Ventris, wasn't even a professional linguist. He was an architect! He'd been obsessed with it since he was fourteen.")),
                    ("laugh", _("Even he thought it would turn out to be Etruscan. It was Greek. An early form of Greek. He was wrong about his own discovery and still cracked it.")),
                    ("him", _("So what did the tablets say? Some kind of epic?")),
                ],
                [
                    ("laugh", _("That's the best part. They're receipts.")),
                    ("smile", _("Inventories. Sheep. Wheat. Chariot wheels, and which ones are broken. Thousands of years of mystery, and it's the palace accounting department.")),
                    ("thinking", _("And they only survived by accident. The tablets were just dried clay, meant to be wiped and reused. Then the palaces burned down, and the fire baked them hard.")),
                    ("happy", _("A disaster saved the paperwork. History is so petty. I love it.")),
                    ("serious", _("Meanwhile, the Minoan tablets with Linear A just sit there. Same island. Some of the same signs. Not a word.")),
                ],
                [
                    ("thinking", _("So people tried the obvious thing on Linear A. Take the sound values from Linear B, since they share a lot of signs, and read it out loud.")),
                    ("annoyed", _("And you get words! You can actually pronounce them! They just don't mean anything in any language we know. It's like hearing someone talk through a wall.")),
                    ("serious", _("And every few years somebody announces they've finally cracked it. Usually with a press release and zero peer review.")),
                    ("annoyed", _("Do the research FIRST. Then have the press conference. It is not that hard.")),
                    ("smirk", _("Anyway. I may or may not have a notebook where I try my own sign lists. It's a hobby. A healthy hobby.")),
                    ("happy", _("Here, look. That's my sign chart. I color coded it. Don't laugh."), 3),
                ],
            ]},
            # Paper maps in grandpa's RV, Mercator, great circles, the town of Agloe
            {"id": "maps", "pages": [
                [
                    ("happy", _("You know what I did every summer as a kid? I planned the routes. The whole trip. On paper maps."), 4),
                    ("smirk", _("Grandpa drove, my cousin complained, and I sat in the back of that old RV with a highlighter like I was running a space mission.")),
                    ("him", _("Sounds fun.")),
                    ("thinking", _("It was! But that's also how I found out that every map you've ever seen is lying to you.")),
                    ("serious", _("Not a little. A lot. You can't flatten a sphere onto paper without stretching something. It's mathematically impossible. Someone proved it.")),
                ],
                [
                    ("thinking", _("So every mapmaker picks what to ruin. The classic one, the map on every classroom wall, is the Mercator projection. From 1569.")),
                    ("happy", _("And it's genius for what it was made for. Sailors. On a Mercator map, if you draw a straight line and keep your compass on the same heading, you follow that line. That's huge on a ship.")),
                    ("annoyed", _("The price is size. The farther from the equator, the bigger everything gets. Greenland looks about as big as Africa.")),
                    ("serious", _("Africa is about fourteen times bigger. Fourteen. You could fit the US, China, India and most of Europe inside it.")),
                    ("him", _("Wait, really?")),
                    ("laugh", _("Really! I made my cousin stare at a globe for an hour. He still doesn't believe me. He's wrong about a lot of things.")),
                ],
                [
                    ("thinking", _("Here's another one. Flights from New York to Europe go way up north, over Canada. On a flat map it looks like a huge detour.")),
                    ("smile", _("On a globe, it's the straight line. The shortest path. A great circle. The map makes the shortcut look like the long way around.")),
                    ("happy", _("That's why I always kept a little globe in the RV. Grandpa thought it was a toy. It was a calculator.")),
                    ("him", _("Of course it was.")),
                    ("smirk", _("Don't 'of course' me. It got us to a campsite in the middle of nowhere on one tank of gas and a prayer. Planning matters.")),
                ],
                [
                    ("thinking", _("Okay, last thing. Did you know mapmakers used to put fake places on their maps on purpose?")),
                    ("smile", _("Trap towns. If your fake town showed up on somebody else's map, you knew they copied you.")),
                    ("happy", _("In the 1930s, two mapmakers invented a town in New York called Agloe. A dot at a dirt road crossing. Nothing there. The name is just their initials scrambled.")),
                    ("laugh", _("Then somebody actually built a general store at that exact spot and called it the Agloe General Store. Because that's what the map said it was!")),
                    ("serious", _("So when another map company put Agloe on their map, and the first company tried to call them out for copying, it didn't work. Agloe was real now.")),
                    ("happy", _("The map made the town real. A lie turned into a place. That might be my favorite thing I've ever read.")),
                ],
            ]},
        ],
        "_default": [
            # Feathered dinosaurs, birds are dinosaurs, T. rex vs Stegosaurus, the asteroid
            {"id": "feathers", "pages": [
                [
                    ("thinking", _("Can I ask you something? When you picture a velociraptor, what do you see?"), 4),
                    ("him", _("Big. Scary. Scaly. Opens doors in a kitchen.")),
                    ("annoyed", _("Okay, so, almost everything you just said is wrong, and I need you to know I'm not mad at you. I'm mad at Hollywood.")),
                    ("serious", _("A real Velociraptor was about the size of a turkey. A big turkey, with a long tail. The ones in the movies were sized like a different dinosaur. Bigger, even.")),
                    ("happy", _("And it had feathers. We KNOW it had feathers. Somebody found the little bumps on its arm bone where the big wing feathers attached. Quill knobs. Same as on birds today.")),
                    ("narr", _("She pulls out her phone and shows you a picture of a turkey. Then a raptor skeleton. Then the turkey again."), 3),
                ],
                [
                    ("smile", _("And it's not just raptors. There are fossils from China with the feathers preserved right there in the rock. Fluffy little dinosaurs. Some of them had four wings."), 4),
                    ("thinking", _("Microraptor! Feathers on its arms AND its legs. Scientists even worked out the color of its feathers. Black, with a shine to it, like a crow.")),
                    ("happy", _("They do it by looking at tiny pigment structures under a microscope. Melanosomes. Their shape tells you the color. From a fossil. That still blows my mind.")),
                    ("him", _("So dinosaurs were... birds?")),
                    ("laugh", _("Other way around! Birds ARE dinosaurs. Every pigeon you've ever seen is a dinosaur. The chicken in your sandwich is a dinosaur.")),
                ],
                [
                    ("serious", _("Here's one that breaks people. Tyrannosaurus rex lived closer in time to us than to Stegosaurus.")),
                    ("happy", _("Stegosaurus was around about a hundred and fifty million years ago. T. rex, about sixty eight million. That's a gap of over eighty million years. We're only sixty six million years away from T. rex.")),
                    ("thinking", _("So every picture with the two of them fighting? It's like a painting of a knight fighting a fighter jet. Actually, it's worse. Way worse.")),
                    ("him", _("That's... actually kind of crazy.")),
                    ("smirk", _("Right? Dinosaurs were around for so long that some of them were ancient history to OTHER dinosaurs.")),
                ],
                [
                    ("thinking", _("And the way it ended is wild too. An asteroid, about ten kilometers across, hit what's now Mexico. The crater is still there, buried under the Yucatan.")),
                    ("serious", _("Around three quarters of all species were gone after that. But a few birds made it. Small ones living on the ground, probably. That part is still a hypothesis. A good one, but a hypothesis.")),
                    ("happy", _("Which means every bird alive today comes from the few that survived the end of the world. The pigeon is a survivor of the apocalypse. Respect the pigeon.")),
                    ("laugh", _("So the next time a pigeon steals your fries, remember. You got robbed by a dinosaur.")),
                ],
            ]},
            # Octopuses: three hearts, blue blood, thinking arms, colorblind camouflage, Inky
            {"id": "octopus", "pages": [
                [
                    ("happy", _("Okay, I have to tell someone this or I'll explode. Octopuses."), 4),
                    ("him", _("Octopuses?")),
                    ("smile", _("Octopuses. The word is Greek, not Latin, so 'octopi' was never really right. 'Octopodes' technically is. Dictionaries gave up and accept all of it now. Anyway.")),
                    ("thinking", _("They have three hearts. Two just for the gills, and one for the rest of the body. And the main one stops beating while they swim, which is why they'd rather crawl.")),
                    ("happy", _("And their blood is blue! It uses copper to carry oxygen instead of iron. Copper. Like an old penny.")),
                ],
                [
                    ("thinking", _("Now the brain part. An octopus has around five hundred million neurons. And about two thirds of them aren't in its head. They're in its arms.")),
                    ("serious", _("Each arm can handle a lot on its own. Touch something, check it out, decide if it's food, without the brain approving every little step.")),
                    ("happy", _("Because the suckers can taste! They have chemical sensors. An octopus touching something is also tasting it. Every handshake is a snack review.")),
                    ("him", _("That's disgusting.")),
                    ("laugh", _("That's AMAZING. Imagine tasting your keyboard every time you type.")),
                ],
                [
                    ("thinking", _("And the camouflage. They change color and even skin texture in a fraction of a second. Bumps, ridges, spots, whatever it takes to look like a rock.")),
                    ("serious", _("Here's the problem. Most of them are probably colorblind. Their eyes only have one kind of light receptor. So how do they match colors they can't see?")),
                    ("smirk", _("Nobody's completely sure. One hypothesis says their weird U-shaped pupils let them pick up color another way. Another one says their skin might sense light directly.")),
                    ("annoyed", _("Both are interesting. Both are still hypotheses. People love repeating them like facts, and it drives me up the wall.")),
                ],
                [
                    ("happy", _("And they escape. All the time. There was one in New Zealand called Inky. In 2016 he got out of his tank at night, crossed the floor and slipped down a drain pipe that went straight to the ocean.")),
                    ("laugh", _("Gone. Just gone. Living his best life in the sea. The staff only figured out how from the trail he left behind.")),
                    ("sad", _("The only sad part is they don't live long. Most octopuses only live a year or two. All that brain, and almost no time to use it.")),
                    ("smile", _("Maybe that's why they're so curious. If you only had two years, you'd want to open every jar too.")),
                ],
            ]},
            # Roman concrete: the Pantheon, volcanic ash and seawater, self-healing lime, rusting rebar
            {"id": "roman_concrete", "pages": [
                [
                    ("thinking", _("Have you ever wondered why Roman buildings are still standing, when a modern bridge needs big repairs after fifty years?"), 4),
                    ("him", _("Because... they built them better?")),
                    ("smirk", _("Kind of! But not the way you'd think. Their concrete was weaker than ours. Way weaker. And it outlived everything.")),
                    ("happy", _("The Pantheon in Rome has a concrete dome that's almost two thousand years old. It's still the biggest concrete dome in the world without any steel inside.")),
                    ("serious", _("Two thousand years. Rain, earthquakes, tourists. Still up.")),
                ],
                [
                    ("thinking", _("Part of the secret is volcanic ash. They mixed lime with ash from around the Bay of Naples. And the ash is what makes it weird.")),
                    ("happy", _("Some of their harbor walls have been sitting in seawater for two thousand years. Modern concrete in seawater falls apart. Theirs got STRONGER.")),
                    ("serious", _("Researchers found that the seawater soaking through it grows new mineral crystals inside the cracks. The ocean has been reinforcing their walls for free.")),
                    ("him", _("The ocean. For free.")),
                    ("laugh", _("For free! Meanwhile, we pay contractors.")),
                ],
                [
                    ("thinking", _("And then a few years ago, a team at MIT looked at the little white lumps of lime all through Roman concrete.")),
                    ("normal", _("Everyone thought those lumps were just sloppy mixing. Bad quality control, basically.")),
                    ("happy", _("Turns out they might be the point. If you mix it hot, with quicklime, the lumps stay inside like tiny reserves. When a crack forms and water gets in, the lime reacts and fills the crack back up.")),
                    ("smile", _("Self-healing concrete. Two thousand years ago. Probably on purpose. They tested it and it works, but nobody's found a Roman manual that says 'do it this way', so... probably.")),
                    ("smirk", _("Evidence, not a confession. Still counts.")),
                ],
                [
                    ("serious", _("Now here's why ours doesn't last. Modern concrete has steel bars inside to make it strong. Rebar.")),
                    ("thinking", _("Which is great, until water gets in. The steel rusts, rust takes up more space than steel, and it cracks the concrete from the inside.")),
                    ("annoyed", _("So a lot of modern concrete is designed to last maybe fifty to a hundred years. The Romans had no steel inside, so nothing could rust.")),
                    ("happy", _("And now people are studying their recipe. Seriously. Two thousand years later, we're taking notes from the Romans.")),
                    ("laugh", _("Every time I walk past a building with cracks in it, I want to stop and give it a lecture.")),
                ],
            ]},
        ],
    }

    # After her last page, with the slot almost gone
    NERD_RAMBLE_ENDS = {
        "tenny": [
            [
                ("narr", _("She finally stops to breathe and glances at the time.")),
                ("surprised", _("Wait. Is that the time? How long was I talking?")),
                ("him", _("A while.")),
                ("embarrassed", _("Okay. I may have gotten slightly carried away. Slightly.")),
                ("smirk", _("In my defense, it was a really good topic. And you didn't run, Dweeb. I noticed. That's worth something.")),
            ],
            [
                ("narr", _("She trails off in the middle of a sentence and checks the time. Her face falls.")),
                ("startled", _("No way. I've been going this whole time? Why didn't you stop me?")),
                ("him", _("I tried. You were on a roll.")),
                ("embarrassed", _("Ugh. My cousin says I came without an off switch. I hate it when he's right.")),
                ("smile", _("Thanks for actually listening, though. Most people tap out way earlier. You're weirdly good at this.")),
            ],
        ],
        "_default": [
            [
                ("narr", _("She finally stops to breathe and glances at the time.")),
                ("surprised", _("Wait. What time is it? How long have I been talking?")),
                ("him", _("A while.")),
                ("embarrassed", _("Oh no. I did it again. I get going and I just... don't stop. I'm so sorry.")),
                ("smile", _("But you actually listened. The whole time. Most people walk away after five minutes. Thank you.")),
            ],
            [
                ("narr", _("At last she trails off and looks around, like she's just waking up.")),
                ("startled", _("Oh my god. It's that late? I've been talking this whole time, haven't I?")),
                ("him", _("Pretty much.")),
                ("shy", _("Sorry. Really. When I get excited about something, my mouth just keeps going.")),
                ("happy", _("You didn't even try to escape. That's... actually really nice. Next time you pick the topic. Maybe.")),
            ],
        ],
    }

    def nerd_ramble_chance():
        """Her chance on one Chit Chat today: rare at first, likelier as the days go by."""
        _days = max(0, store.Day - 1)
        return min(NERD_RAMBLE["max_chance"], NERD_RAMBLE["chance"] + NERD_RAMBLE["per_day"] * _days)

    def nerd_ramble_roll(girl):
        """Chit_Chat: does she get carried away this time? Once per run (any nerd), face to face (not on the phone,
        not while time is locked), never angry or sad, and only with at least NERD_RAMBLE["min_eats"] rounds to eat
        before the NERD_RAMBLE["leaves"] she leaves in the slot."""
        if store._nerd_ramble_day is not None or not girl.has_trait("nerd"):
            return False
        if getattr(store, "_phone_mode", False) or getattr(store, "_time_locked", False):
            return False
        if girl.has_temp_status("angry") or girl.has_temp_status("sad"):
            return False
        if 100 - store.Round - NERD_RAMBLE["leaves"] < NERD_RAMBLE["min_eats"]:
            return False
        _chance = nerd_ramble_chance()
        _hit = renpy.random.random() < _chance
        print("[NERD_RAMBLE] %s roll: %s (Day %d, chance %.3f, Round %d)" % (girl.gid, "HIT" if _hit else "miss", store.Day, _chance, store.Round))
        return _hit

    def _nerd_ramble_say(girl, lines):
        """Plays one page (or her ending): her lines with their face and arm, his lines, the narration."""
        for _ln in lines:
            _face, _text = _ln[0], _ln[1]
            if _face == "him":
                Say_Player(_text)
                continue
            if len(_ln) > 2:
                _set_standing_arm(girl, _ln[2])
            if _face == "narr":
                Narration(_text)
                continue
            set_scene_expression(girl, _face)
            Say_Line(girl, _text)

# She talks until only NERD_RAMBLE["leaves"] rounds of the slot are left (nerd_ramble_roll made sure there is room:
# the slot never changes here)
label _nerd_ramble(girl):
    python:
        _nr = renpy.random.choice(girl_pool(NERD_RAMBLES, girl, "nerd ramble"))
        _nr_end = renpy.random.choice(girl_pool(NERD_RAMBLE_ENDS, girl, "nerd ramble end"))
        _nr_eats = max(0, 100 - NERD_RAMBLE["leaves"] - Round)
        _nr_page = 0
        _nerd_ramble_day = Day
        girl.RegisterAction("chitchat")
        girl.RegisterAction("nerd_ramble")
        print("[NERD_RAMBLE] %s: '%s', %d pages, eats %d rounds (Round %d)" % (girl.gid, _nr["id"], len(_nr["pages"]), _nr_eats, Round))
    $ Narration(renpy.random.choice(NERD_RAMBLE_SPARK))
    while _nr_page < len(_nr["pages"]):
        if _nr_page > 0:
            # the screen dips to black between her pages: time goes by
            with fade
            $ Narration(renpy.random.choice(NERD_RAMBLE_BREAKS[min(_nr_page, len(NERD_RAMBLE_BREAKS)) - 1]))
        $ _nerd_ramble_say(girl, _nr["pages"][_nr_page])
        $ _nr_page += 1
    with fade
    call Apply_Time_Cost(_nr_eats) from _call_Apply_Time_Cost_nerd_ramble
    $ _nerd_ramble_say(girl, _nr_end)
    python:
        _set_standing_arm(girl, 0)
        set_scene_expression(girl, "normal")
        Change_Status(girl, "Love", NERD_RAMBLE["love"])
        girl.discover("discovered_trait_nerd")
        unlock_achievement("nerds_talk")
    $ renpy.fix_rollback()
    return
