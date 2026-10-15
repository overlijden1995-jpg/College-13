# ============================================================
# INTRO — First-time campus tour after trait selection
# ============================================================

label intro:

    # --- Black screen: inner monologue ---
    scene black
    with fade

    PlayerChar "After applying to more universities than I can count, I finally got accepted into one."

    # D1 (docs/plan_shion.md): his father is not rich; his stepmother Shion is, and her money is not his
    PlayerChar "My dad isn't exactly rich. His new wife is, but she made it very clear her money isn't ours."

    PlayerChar "So I managed to get a scholarship. But after paying all the bills, I won't have much money left each week."

    PlayerChar "At least I have a room on campus, food, and a few other things covered. Could be worse."

    pause 0.5

    # --- Campus ---
    scene bg campus
    with fade

    PlayerChar "Damn, this place is huge..."

    PlayerChar "I think my room is somewhere in the back. Let me take a look around first."

    pause 0.3

    # --- Gym ---
    scene bg gym
    with fade

    # Pick a random girl to be at the gym
    python:
        _intro_gym_girl = renpy.random.choice([g for g in girls_on_campus() if g.gid != "tenny"])
        _intro_gym_girl.loc = "gym"
        set_girl_sprite(_intro_gym_girl.gid, pose="standing", at_list=[slot_center])

    PlayerChar "They even have a gym in here."

    # NTW — always dismissive regardless of attractiveness
    if _intro_gym_girl.gid == "ntw":
        PlayerChar "And some {i}fit{/i} people working out too..."
        $ set_scene_expression(_intro_gym_girl, "serious")
        $ Say_Line(_intro_gym_girl, _("Hey, string bean. You gonna use that machine or just taking up space?"))
        PlayerChar "Sorry, I'm new here. Just looking around."
        $ set_scene_expression(_intro_gym_girl, "neutral", eyes="eyes_side")
        $ Say_Line(_intro_gym_girl, _("Cool. Be new somewhere else, I'm busy."))
        PlayerChar "(Well... she's direct.)"

    # Attractiveness-based gym reaction (other girls)
    elif Player.attractiveness <= 25:
        PlayerChar "And some {i}fit{/i} people working out too..."
        $ set_scene_expression(_intro_gym_girl, "serious")
        $ Say_Line(_intro_gym_girl, _("Can I help you with something?"))
        $ set_scene_expression(_intro_gym_girl, "neutral", eyes="eyes_side")
        PlayerChar "(She barely even looked at me. Okay then.)"
        PlayerChar "I definitely need to come here. Studying for exams drained all my energy. I'm completely out of shape."

    elif Player.attractiveness <= 50:
        PlayerChar "And some {i}fit{/i} people working out too..."
        PlayerChar "I need to come here a few times a week. Studying for exams drained all my energy. I'm completely out of shape."

    elif Player.attractiveness <= 75:
        PlayerChar "And some {i}fit{/i} people working out too..."
        $ set_scene_expression(_intro_gym_girl, "happy")
        $ Say_Line(_intro_gym_girl, _("Hey! You new here? Haven't seen you around."))
        PlayerChar "Yeah, just arrived. I should hit this place regularly."
        PlayerChar "She seemed friendly. That's a good sign."

    else:
        PlayerChar "And some {i}fit{/i} people working out too..."
        $ set_scene_expression(_intro_gym_girl, "smile")
        $ Say_Line(_intro_gym_girl, _("Oh, hi! Are you new? I'd remember a face like that."))
        PlayerChar "Yeah, first day. I'll definitely be coming back."
        $ set_scene_expression(_intro_gym_girl, "sexy")
        $ Say_Line(_intro_gym_girl, _("Well... I'm here most mornings. See you around!"))
        PlayerChar "(Alright, that was a great first impression.)"

    # Hide the girl before moving on
    python:
        hide_girl_sprite(_intro_gym_girl)
        _intro_gym_girl.loc = _intro_gym_girl.home

    pause 0.3

    # --- Showers ---
    scene bg showers
    with fade

    PlayerChar "Wait... there's only one shower for all students?"

    PlayerChar "How does that even work? Well, I guess I'll figure it out eventually."

    pause 0.3

    # --- Pool ---
    scene bg pool_day
    with fade

    PlayerChar "Well, at least I already have a place to relax when I'm not in class."

    pause 0.3

    # --- Room ---
    scene bg room_day
    with fade

    PlayerChar "This is it."

    "You spend some time setting up your computer and tidying up the place."

    pause 0.5

    PlayerChar "A room all to myself. I hope everything works out."

    PlayerChar "Now I just need to stay in shape, make some money, and pass every class while also being social."

    PlayerChar "Easy!"

    pause 0.3

    # --- Phone notification ---

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes with a notification."

    BigFansChar "Bella Dolphin just posted new exclusive content! Subscribe now for..."

    PlayerChar "Man, this girl isn't even that relevant anymore and she's still making enough from these videos to buy a car every week..."

    PlayerChar "If I were a girl... But wait, there are some guys with channels too."

    PlayerChar "Of course they need girls to record with, but... If I find someone willing, that could solve my money problem right there."

    PlayerChar "Let me take a closer look at this app..."

    "You open BigFans and scroll through a few channels."

    PlayerChar "Interesting... I could publish some videos to get subscribers and build up passive income over time."

    PlayerChar "But the real money comes from fan requests. People pay extra for specific types of content."

    PlayerChar "First I need to actually record some videos and get some attention on the channel. Let's see how it goes."

    pause 0.3

    PlayerChar "I think my friend knows more about it, let me check my contacts real quick..."

    "You open your contacts and... it's completely empty."

    PlayerChar "Wait... all my contacts are gone?!"

    PlayerChar "Oh right, I had to factory reset this thing last week. Lost everything. Contacts, groups, all of it."

    PlayerChar "Damn. I'll try to remember some numbers and set up a few group chats later."

    PlayerChar "Maybe I can get the girls from class to grab some drinks after. That would be a good way to start."

    pause 0.3

    PlayerChar "Ok, I'll look into this later. Right now I need to get ready for the first week of classes."

    pause 0.3

    # --- Classroom: first day ---
    scene bg ClassRoom
    with fade

    # Tenny arrived early — she's already here when the player walks in
    python:
        _tenny = GIRL_BY_ID.get("tenny") if "tenny" in [g.gid for g in ALL_GIRLS] else None

    if _tenny:
        python:
            _tenny.loc = "classroom"
            set_girl_sprite(_tenny.gid, pose="standing", at_list=[slot_center])

        $ Say_Player(_("(Wow, I thought I got here early, but apparently someone beat me to it.)"))

        $ hide_girl_sprite(_tenny)

    $ Narration(_("The classroom fills up as more students arrive."))

    pause 0.3

    # Place all girls in the classroom
    python:
        _gwen = GIRL_BY_ID["gwen"]
        _rogue = GIRL_BY_ID.get("rogue") if "rogue" in [g.gid for g in ALL_GIRLS] else None
        _ntw = GIRL_BY_ID.get("ntw") if "ntw" in [g.gid for g in ALL_GIRLS] else None
        _gwen.loc = "classroom"
        if _rogue:
            _rogue.loc = "classroom"
        if _ntw:
            _ntw.loc = "classroom"
        if _tenny:
            _tenny.loc = "classroom"

        _intro_all = [_gwen] + [g for g in [_rogue, _ntw, _tenny] if g]
        _n = len(_intro_all)
        _intro_slots = {
            1: [slot_center],
            2: [slot_left, slot_right],
            3: [slot_left, slot_center, slot_right],
            4: [slot_left, slot_center_left, slot_center_right, slot_right],
        }
        _slots = _intro_slots.get(_n, _intro_slots[4])
        for _i, _g in enumerate(_intro_all):
            if _i < len(_slots):
                set_girl_sprite(_g.gid, pose="standing", at_list=[_slots[_i]])

    # --- Professor speech (narration style — no arrow) ---
    ProfessorChar "Let me explain how things work here. You will have an exam every two weeks, always on Friday afternoon."

    ProfessorChar "Attendance for the exams is mandatory. Miss it and it's an automatic F. Regular classes are not mandatory, but I recommend showing up."

    ProfessorChar "Study hard and you'll be rewarded. I also recommend studying in pairs or groups, it can boost your productivity even further."

    ProfessorChar "Now, let's take some time to get to know your classmates. Speed rounds: introduce yourselves and chat. You have one minute per person. Go!"

    # ========================================
    # GWEN — Introduction (attractiveness variants)
    # ========================================

    # Focus on Gwen
    python:
        if _rogue:
            hide_girl_sprite(_rogue)
        if _ntw:
            hide_girl_sprite(_ntw)
        if _tenny:
            hide_girl_sprite(_tenny)
        set_girl_sprite(_gwen.gid, pose="standing", at_list=[slot_center])

    # --- LOW attractiveness (0-25) ---
    if Player.attractiveness <= 25:

        $ set_scene_expression(_gwen, "neutral")
        $ Say_Line(_gwen, _("Hi. I'm Gwen. I draw. I wear black. I hate icebreakers."))
        $ Say_Line(_gwen, _("And you are...?"))

        menu:
            "[Player.Name]. I like sports and computers.":
                $ Change_Status(_gwen, "Love", 10)
                $ set_scene_expression(_gwen, "serious")
                $ Say_Line(_gwen, _("Cool. Good luck with that."))

            "[Player.Name]. Drawing as in Drawterest mood boards or actual art?":
                $ Change_Status(_gwen, "Obed", 10)
                $ Change_Status(_gwen, "Love", -10)
                $ set_scene_expression(_gwen, "confused")
                $ Say_Line(_gwen, _("...I don't even know what to say to that."))

            "I'm [Player.Name]. Interesting style... Do you have piercings anywhere else I can't see?":
                $ Change_Status(_gwen, "Inbt", 5)
                $ set_scene_expression(_gwen, "surprised")
                $ Say_Line(_gwen, _("Wow. That's... a bold choice for a first impression. Read the room, dude."))

        PlayerChar "(Yeah, she's definitely not impressed. I'll have to work harder with this one.)"

    # --- MID attractiveness (26-75) ---
    elif Player.attractiveness <= 75:

        $ set_scene_expression(_gwen, "smug")
        $ Say_Line(_gwen, _("Hi, I'm Gwen. I'm into art. Drawing, mostly. Don't get any funny ideas."))

        menu:
            "[Player.Name]. I like sports and computers... I think.":
                $ Change_Status(_gwen, "Love", 15)
                $ set_scene_expression(_gwen, "bemused")
                $ Say_Line(_gwen, _("Nerds are hitting the gym now too? What a time to be alive."))

            "[Player.Name]. Drawing as in Drawterest mood boards or actual art?":
                $ Change_Status(_gwen, "Obed", 10)
                $ Change_Status(_gwen, "Love", -5)
                $ set_scene_expression(_gwen, "confused")
                $ Say_Line(_gwen, _("What kind of question is that?"))

            "I'm [Player.Name]. Interesting style... Do you have piercings anywhere else I can't see?":
                $ Change_Status(_gwen, "Inbt", 10)
                $ Change_Status(_gwen, "Obed", 5)
                $ set_scene_expression(_gwen, "sly")
                $ Say_Line(_gwen, _("I'll leave that to your imagination. Maybe one day you'll find out."))

    # --- HIGH attractiveness (76-100) ---
    else:

        $ set_scene_expression(_gwen, "happy")
        $ Say_Line(_gwen, _("Hi! I'm Gwen. Art is kind of my thing. Drawing, painting, anything that keeps my hands busy."))
        $ set_scene_expression(_gwen, "smile")
        $ Say_Line(_gwen, _("And... you are?"))

        menu:
            "[Player.Name]. Sports, computers, the usual.":
                $ Change_Status(_gwen, "Love", 25)
                $ set_scene_expression(_gwen, "sexy")
                $ Say_Line(_gwen, _("A jock who knows his way around a keyboard? That's actually kind of hot."))

            "[Player.Name]. An artist? So you're the creative and cute type.":
                $ Change_Status(_gwen, "Obed", 10)
                $ Change_Status(_gwen, "Love", 10)
                $ Change_Status(_gwen, "Inbt", 5)
                $ set_scene_expression(_gwen, "smug")
                $ Say_Line(_gwen, _("Smooth. I'll remember that one."))

            "I'm [Player.Name]. That style really suits you. Do you have piercings anywhere else?":
                $ Change_Status(_gwen, "Inbt", 15)
                $ Change_Status(_gwen, "Obed", 10)
                $ set_scene_expression(_gwen, "sly")
                $ Say_Line(_gwen, _("Maybe. Stick around and you might get a private tour."))

        PlayerChar "(She's definitely interested. Good start.)"

    # Before she can say anything else...
    "Before you can say anything else..."

    ProfessorChar "NEXT! SWITCH!"

    # ========================================
    # ROGUE — Introduction (attractiveness variants)
    # ========================================

    if _rogue:
        # Focus on Rogue
        python:
            hide_girl_sprite(_gwen)
            if _ntw:
                hide_girl_sprite(_ntw)
            if _tenny:
                hide_girl_sprite(_tenny)
            set_girl_sprite(_rogue.gid, pose="standing", at_list=[slot_center])

        # --- LOW attractiveness (0-25) ---
        if Player.attractiveness <= 25:

            $ set_scene_expression(_rogue, "serious")
            $ Say_Line(_rogue, _("Hey. I'm Rogue. Southern food, rock music. Not really into talking."))

            menu:
                "[Player.Name]. I'm kind of new to all of this too.":
                    $ Change_Status(_rogue, "Love", 10)
                    $ set_scene_expression(_rogue, "neutral")
                    $ Say_Line(_rogue, _("Yeah. Okay."))

                "[Player.Name]. Are there any old-school goth shops in town? I see a pattern here.":
                    $ Change_Status(_rogue, "Obed", 10)
                    $ Change_Status(_rogue, "Love", -10)
                    $ set_scene_expression(_rogue, "angry")
                    $ Say_Line(_rogue, _("Old-school? What's that supposed to mean?"))

                "[Player.Name]. I think we could try some new experiences together.":
                    $ Change_Status(_rogue, "Inbt", 5)
                    $ set_scene_expression(_rogue, "uncomfortable")
                    $ Say_Line(_rogue, _("...I barely know you. Slow down."))

            PlayerChar "(She seems guarded. This is going to take patience.)"

        # --- MID attractiveness (26-75) ---
        elif Player.attractiveness <= 75:

            $ set_scene_expression(_rogue, "shy")
            $ Say_Line(_rogue, _("Hey. I'm Rogue. I guess I like southern food. I'm not great with physical contact, but I'm getting used to new experiences."))

            menu:
                "[Player.Name]. I'm kinda lost with all these new things too.":
                    $ Change_Status(_rogue, "Love", 15)
                    $ set_scene_expression(_rogue, "smile")
                    $ Say_Line(_rogue, _("Good to know I'm not the only one figuring things out around here."))

                "[Player.Name]. Are there any old-school goth shops in town? I see a pattern here.":
                    $ Change_Status(_rogue, "Obed", 10)
                    $ Change_Status(_rogue, "Love", -5)
                    $ set_scene_expression(_rogue, "confused")
                    $ Say_Line(_rogue, _("Old-school goth? What do you mean by that?"))

                "[Player.Name]. I think we could try some new experiences together. Especially the touching part.":
                    $ Change_Status(_rogue, "Inbt", 10)
                    $ Change_Status(_rogue, "Obed", 5)
                    $ set_scene_expression(_rogue, "bemused")
                    $ Say_Line(_rogue, _("...You're bold, I'll give you that. But keep trying."))

        # --- HIGH attractiveness (76-100) ---
        else:

            $ set_scene_expression(_rogue, "shy")
            $ Say_Line(_rogue, _("Hey. I'm Rogue. Southern food, quiet places... I don't usually talk this much."))
            $ set_scene_expression(_rogue, "smile")
            $ Say_Line(_rogue, _("But... I guess I can make an exception."))

            menu:
                "[Player.Name]. Same here. New place, new people. Glad to meet someone real.":
                    $ Change_Status(_rogue, "Love", 25)
                    $ set_scene_expression(_rogue, "happy")
                    $ Say_Line(_rogue, _("Real? I like that. Most people here feel... fake."))

                "[Player.Name]. The mysterious type, huh? I'm into it.":
                    $ Change_Status(_rogue, "Obed", 10)
                    $ Change_Status(_rogue, "Love", 10)
                    $ Change_Status(_rogue, "Inbt", 5)
                    $ set_scene_expression(_rogue, "sly")
                    $ Say_Line(_rogue, _("...You're trouble, aren't you? I can tell."))

                "[Player.Name]. New experiences, huh? I'd love to be part of that list.":
                    $ Change_Status(_rogue, "Inbt", 15)
                    $ Change_Status(_rogue, "Obed", 10)
                    $ set_scene_expression(_rogue, "embarrassed")
                    $ Say_Line(_rogue, _("That was... actually kind of smooth. Don't let it go to your head."))

            PlayerChar "(She's warming up already. I like this one.)"

        # Before she can respond further...
        "Before you can continue..."

        ProfessorChar "NEXT! SWITCH!"

    # ========================================
    # NTW — Introduction (indifferent regardless of attractiveness)
    # ========================================

    if _ntw:
        # Focus on NTW
        python:
            hide_girl_sprite(_gwen)
            if _rogue:
                hide_girl_sprite(_rogue)
            if _tenny:
                hide_girl_sprite(_tenny)
            set_girl_sprite(_ntw.gid, pose="standing", at_list=[slot_center])

        $ set_scene_expression(_ntw, "serious")
        $ Say_Line(_ntw, _("Negasonic Teenage Warhead."))

        menu:
            "Uh... ok. My name is [Player.Name].":
                $ Change_Status(_ntw, "Love", -5)
                $ set_scene_expression(_ntw, "neutral", eyes="eyes_side")
                $ Say_Line(_ntw, _("Yeah, cool. See ya."))

            "Holy shit, coolest name ever!":
                $ Change_Status(_ntw, "Love", 10)
                $ set_scene_expression(_ntw, "perplexed")
                $ Say_Line(_ntw, _("Uh? Ok..."))

            "Long name... do you have like a nickname or...?":
                $ Change_Status(_ntw, "Obed", 5)
                $ set_scene_expression(_ntw, "serious")
                $ Say_Line(_ntw, _("No. Use it full."))

            "[Player.Name].":
                $ Change_Status(_ntw, "Love", 10)
                $ set_scene_expression(_ntw, "neutral", eyes="eyes_side")
                $ Say_Line(_ntw, _("Right. See you."))

        PlayerChar "(She really doesn't care, does she?)"

        "Before you can say anything else..."

        ProfessorChar "NEXT! SWITCH!"

    # ========================================
    # TENNY — Introduction (nerd, no attractiveness tiers)
    # ========================================

    if _tenny:
        # Focus on Tenny
        python:
            for _g in _intro_all:
                hide_girl_sprite(_g)
            set_girl_sprite(_tenny.gid, pose="standing", at_list=[slot_center])

        $ set_scene_expression(_tenny, "happy")
        $ Say_Line(_tenny, _("Hey, I'm Gwendolyn Tennyson. Most people here know me as Tenny, since there are already other Gwens around."))

        menu:
            "You look really mature. Definitely over eighteen.":
                $ Change_Status(_tenny, "Love", 1)
                $ set_scene_expression(_tenny, "confused")
                $ Say_Line(_tenny, _("That's... a weird way to start a conversation."))
                $ set_scene_expression(_tenny, "smug")
                $ Say_Line(_tenny, _("Yes, I'm over 18, but I definitely could have started earlier if they'd let me. I'm smart enough for that."))

            "I think we could be great lab partners.":
                $ Change_Status(_tenny, "Love", 15)
                $ set_scene_expression(_tenny, "surprised")
                $ Say_Line(_tenny, _("Wait, really? You actually care about the academic part?"))
                $ set_scene_expression(_tenny, "happy")
                $ Say_Line(_tenny, _("Finally, someone who gets why we're here. I like you already."))

            "Can I call you something else?":
                $ set_scene_expression(_tenny, "neutral", eyes="eyes_side")
                $ Say_Line(_tenny, _("Sure, I guess. What did you have in mind?"))
                call _tenny_nickname from _call_tenny_nickname

        $ Say_Player(_("(Definitely the smartest person in this room. Possibly including the professor. And probably the most modest too.)"))

        "Before you can say anything else..."

        ProfessorChar "NEXT! SWITCH!"

    # ========================================
    # Generic NPCs — quick montage
    # ========================================

    "You go through a few more rounds with other students. Not a lot of personality there, a lot of NPCs."

    pause 0.3

    # --- Professor closing ---
    # Show all girls again (hide first to avoid overlap)
    python:
        for _g in _intro_all:
            hide_girl_sprite(_g)
        _n = len(_intro_all)
        if _n == 1:
            set_girl_sprite(_intro_all[0].gid, pose="standing", at_list=[slot_center])
        elif _n == 2:
            set_girl_sprite(_intro_all[0].gid, pose="standing", at_list=[slot_left])
            set_girl_sprite(_intro_all[1].gid, pose="standing", at_list=[slot_right])
        elif _n == 3:
            set_girl_sprite(_intro_all[0].gid, pose="standing", at_list=[slot_left])
            set_girl_sprite(_intro_all[1].gid, pose="standing", at_list=[slot_center])
            set_girl_sprite(_intro_all[2].gid, pose="standing", at_list=[slot_right])
        else:
            for _i, _g in enumerate(_intro_all):
                set_girl_sprite(_g.gid, pose="standing", at_list=[Transform(xalign=0.30 + _i * 0.25, yalign=2.0)])

    ProfessorChar "Alright, has everyone talked? Good."

    ProfessorChar "Keep it up and I'll see you all in class. Remember: attendance is not mandatory, but three low grades in a row and you lose your scholarship. See you around."

    pause 0.3

    # --- Outro ---
    python:
        for _g in _intro_all:
            hide_girl_sprite(_g)

    # Attractiveness-based closing thoughts
    if Player.attractiveness <= 25:
        if _rogue or _ntw or _tenny:
            PlayerChar "Those girls weren't exactly thrilled to meet me... but the exam info is good to know."
        else:
            PlayerChar "She wasn't exactly thrilled to meet me... but the exam info is good to know."
        PlayerChar "I'll have to prove myself the hard way. No shortcuts."
    elif Player.attractiveness <= 75:
        if _rogue or _ntw or _tenny:
            PlayerChar "Those girls seem interesting... and the exam info is good to know."
        else:
            PlayerChar "That girl seems interesting... and the exam info is good to know."
    else:
        if _ntw and _rogue:
            PlayerChar "Gwen and Rogue seemed into me. Negasonic, not so much. This is going to be a fun semester."
        elif _ntw:
            PlayerChar "Gwen seemed into me. That Negasonic girl though... couldn't care less. Interesting semester ahead."
        elif _rogue:
            PlayerChar "Both of those girls seemed pretty into me. This is going to be a fun semester."
        else:
            PlayerChar "That girl seemed pretty into me. This is going to be a fun semester."
        PlayerChar "The exam stuff is good to know too, I guess."

    if _tenny:
        $ Say_Player(_("And that [_tenny.Name] girl is sharp. Could be useful to have someone around who actually takes studying seriously."))

    scene black
    with fade
    pause 0.5

    PlayerChar "Time to conquer the world."

    # --- Set up the world for actual gameplay ---
    python:
        CurrentLocation = "room"
        Day = 2
        TimeIndex = 0
        Round = 0
        update_all_girls_locations_for_time(Day, TimeIndex)
    return

# ========================================
# Tenny nickname selection (called from intro)
# ========================================

label _tenny_nickname:
    $ _tried_gwenatron = False

label _tenny_nickname_loop:
    menu:
        "Keep calling you Tenny.":
            $ set_scene_expression(_tenny, "neutral")
            $ Say_Line(_tenny, _("Tenny it is. Simple, efficient."))

        "Gwen.":
            $ _tenny.Name = "Gwen"
            $ set_scene_expression(_tenny, "confused")
            $ Say_Line(_tenny, _("But... there's already a Gwen here. You know that, right?"))

        "Gwendolyn.":
            $ _tenny.Name = "Gwendolyn"
            $ set_scene_expression(_tenny, "neutral")
            $ Say_Line(_tenny, _("That's my actual name, so... sure."))

        "Tennyson.":
            $ _tenny.Name = "Tennyson"
            $ set_scene_expression(_tenny, "happy")
            $ Say_Line(_tenny, _("Pretty formal, but okay. At least it keeps the focus on the academic side!"))

        "Gwen 2.":
            $ _tenny.Name = "Gwen 2"
            $ set_scene_expression(_tenny, "angry")
            $ Say_Line(_tenny, _("'Gwen 2'? Seriously? ...Whatever, just don't call me that in public."))

        "Cathy.":
            $ _tenny.Name = "Cathy"
            $ set_scene_expression(_tenny, "surprised")
            $ Say_Line(_tenny, _("Cathy? That's... short for my middle name. How did you know that? Are you stalking me?"))

        "Catherine.":
            $ _tenny.Name = "Catherine"
            $ set_scene_expression(_tenny, "surprised")
            $ Say_Line(_tenny, _("Wait... that's my middle name. How did you know that? Are you a stalker?"))

        "Gwen T.":
            $ _tenny.Name = "Gwen T"
            $ set_scene_expression(_tenny, "happy")
            $ Say_Line(_tenny, _("Gwen T? That's actually kind of practical. I'll take it."))

        "Lucky.":
            $ _tenny.Name = "Lucky"
            $ set_scene_expression(_tenny, "surprised")
            $ Say_Line(_tenny, _("Wait... they haven't called me that in years. How did you know about that?"))

        "Gwennie.":
            $ _tenny.Name = "Gwennie"
            $ set_scene_expression(_tenny, "happy")
            $ Say_Line(_tenny, _("Gwennie? That's... actually kind of cute. I'll allow it."))

        "Red.":
            $ _tenny.Name = "Red"
            $ set_scene_expression(_tenny, "neutral")
            $ Say_Line(_tenny, _("Red? Short and practical. I can work with that."))

        "Gwenatron Destroyer Of Worlds X Red." if not _tried_gwenatron:
            $ _tried_gwenatron = True
            $ set_scene_expression(_tenny, "angry")
            $ Say_Line(_tenny, _("... Are you an idiot?"))
            jump _tenny_nickname_loop

    return
