# ============================================================
# GROUP VIDEO REACTIONS
# Same structure as VIDEO_ constants in interactions.rpy,
# but with group-aware text (girl knows others in the chat see it).
# ============================================================

default _scripted_group_convos_seen = set()

init python:

    def _group_unique_choice(pool):
        """Pick from pool without repeating lines another girl already used in this batch.
        Falls back to '...' when every line is taken. Outside a group batch (store._group_used_lines
        is None) behaves like renpy.random.choice."""
        _rng = renpy.random.choice
        _used = getattr(store, "_group_used_lines", None)
        if _used is None or not pool:
            return _rng(pool)
        try:
            _avail = [_l for _l in pool if _l not in _used]
            if not _avail:
                return "..."
            _pick = _rng(_avail)
            _used.add(_pick)
            return _pick
        except TypeError:
            return _rng(pool)

    # ==========================================================
    # 1. GROUP_VIDEO_SELF_LINES — video is of THIS girl, sent in group
    # ==========================================================
    GROUP_VIDEO_SELF_LINES = {
        "hj": [
            _("You sent that HERE?! Everyone can see me doing that with my hand!"),
            _("Oh my god... the whole group just saw me giving you a handjob..."),
            _("You couldn't send this privately?! Now everyone knows what my hands do!"),
        ],
        "bj": [
            _("You're showing everyone me on my knees for you?! In the GROUP?!"),
            _("The whole chat just saw my mouth on you... I want to disappear."),
            _("Everyone just watched me go down on you. Thanks for that."),
        ],
        "tj": [
            _("My chest... on display... in the GROUP CHAT?! Are you insane?!"),
            _("Everyone in this chat just saw my tits around you. I'm dying."),
            _("You sent a titjob video to the GROUP?! Have you lost your mind?!"),
        ],
        "cowgirl": [
            _("The whole group just saw me riding you?! What is WRONG with you?!"),
            _("You sent THAT here?! Everyone can see me bouncing on top of you!"),
            _("I'm on top of you... and every girl in this chat just watched it."),
        ],
        "creampie": [
            _("You showed everyone you finishing inside me?! IN THE GROUP?!"),
            _("The whole chat can see it dripping out of me... I want to die."),
            _("A creampie video... in the GROUP CHAT?! Are you trying to ruin me?!"),
        ],
        "doggy": [
            _("That's me... from behind... oh god."),
            _("You recorded us doing it doggy style?!"),
            _("I can't believe you're showing people this..."),
        ],
        "anal": [
            _("That's... my ass... you recorded THAT?!"),
            _("You filmed us doing anal?! Delete this immediately!"),
            _("Oh my god, everyone can see you in my ass..."),
        ],
        "laying_down": [
            _("That's me... laying there while you... oh god, the whole group can see."),
            _("You sent THAT here?! Everyone can see you on top of me!"),
            _("The entire chat just watched you pin me down... I can't believe this."),
        ],
        "masturbate": [
            _("You sent THAT to the group?! That's the most private thing I have!"),
            _("Everyone just saw me touching myself... in the group chat. I hate you."),
            _("My most personal video... shared with the entire group. Unbelievable."),
        ],
    }

    # ==========================================================
    # 1b. GROUP_VIDEO_ABANDONED_SELF_LINES — pre-partner video shown after she got a partner
    # ==========================================================
    GROUP_VIDEO_ABANDONED_SELF_LINES = {
        # ── Protective: angry + group embarrassment ──
        ("protective", "hj"): [
            _("Delete that! Everyone can see this and I'm with %(pl)s now!"),
            _("You're showing THAT to the group?! I'm with someone now! Take it down!"),
            _("Everyone in this chat just saw me from before %(pl)s... delete it!"),
        ],
        ("protective", "bj"): [
            _("You sent THAT to the GROUP?! I'm with %(pl)s! Everyone can see me doing that!"),
            _("Delete it! The whole group doesn't need to see me doing that! I'm with %(pl)s!"),
            _("Everyone just watched me do THAT and I'm in a relationship now?! Delete it!"),
        ],
        ("protective", "tj"): [
            _("The whole group can see that?! I'm with %(pl)s now! Take it down!"),
            _("You're sharing THAT with everyone?! Delete it! I've moved on!"),
            _("Everyone in this chat... and I'm with %(pl)s... delete that right now!"),
        ],
        ("protective", "cowgirl"): [
            _("You showed the GROUP me riding you?! I'm with %(pl)s! Delete that NOW!"),
            _("Everyone just saw that?! I'm with someone now! Why would you share this?!"),
            _("The whole chat can see me on top of you and I'm in a RELATIONSHIP! Delete it!"),
        ],
        ("protective", "creampie"): [
            _("EVERYONE just saw you finish inside me?! I'm with %(pl)s! DELETE IT!"),
            _("You sent a creampie video to the GROUP CHAT?! I'm with %(pl)s! Are you insane?!"),
            _("If %(pl)s sees this group chat, my life is OVER. Delete it right now!"),
        ],
        ("protective", "anal"): [
            _("You shared THAT with EVERYONE?! I'm with %(pl)s now! Delete it immediately!"),
            _("The whole group just saw me do THAT and I'm in a relationship?! You're dead!"),
            _("Delete it! Everyone just saw my most private moment and I'm with %(pl)s!"),
        ],
        ("protective", "laying_down"): [
            _("The whole group saw you on top of me?! I'm with %(pl)s now! Delete it!"),
            _("Everyone just saw that?! I'm in a relationship! Take it down NOW!"),
            _("You showed the GROUP that video?! I'm with %(pl)s! Delete it immediately!"),
        ],
        ("protective", "masturbate"): [
            _("You sent THAT to the group?! I was single then! I'm with %(pl)s now! Delete it!"),
            _("Everyone just saw my private video! I'm in a relationship! Take it down!"),
            _("The whole chat can see me touching myself?! I'm with %(pl)s! Delete that!"),
        ],
        # ── Indifferent: dismissive in group context ──
        ("indifferent", "hj"): [
            _("The group seeing me do that? At this point, who cares. We've done worse since."),
            _("Whatever. Everyone here probably guessed we were still doing stuff anyway."),
            _("Old video, new audience. Not like it changes anything between us."),
        ],
        ("indifferent", "bj"): [
            _("Oh, the whole group can see that? Sure. Not exactly a secret anymore."),
            _("Everyone seeing me do that? Add it to the list of things I can't take back."),
            _("The group seeing an old video of me... honestly, whatever. We all know what's going on."),
        ],
        ("indifferent", "tj"): [
            _("The whole chat seeing my chest? Not the most embarrassing thing at this point."),
            _("Whatever. Everyone here has probably figured out we're still a thing."),
            _("An old titjob video in the group? Fine. Not like I can deny anything at this point."),
        ],
        ("indifferent", "cowgirl"): [
            _("Everyone just watched me ride... at this point, what's one more secret out?"),
            _("The group seeing that? Whatever. %(Pp)s would be mad about everything else too."),
            _("Not like anyone in this chat is surprised at this point."),
        ],
        ("indifferent", "creampie"): [
            _("A creampie video in the group chat. Sure. Why not. We've done worse since."),
            _("Whatever. The video is the least of my problems at this point."),
            _("Everyone seeing that? Honestly, I'm past caring. We all know what happened."),
        ],
        ("indifferent", "anal"): [
            _("The group seeing THAT? At this point, nothing surprises me anymore."),
            _("Sure, everyone can see that. Not like I have any secrets left."),
            _("An anal video in the group? Fine. Whatever. It happened."),
        ],
        ("indifferent", "laying_down"): [
            _("The group seeing that? Whatever. Not like it's news that we were together."),
            _("Everyone seeing me under you? Sure. Add it to the pile."),
            _("That old video in the group? Fine. We've done way more since then anyway."),
        ],
        ("indifferent", "masturbate"): [
            _("A solo video of me in the group? That barely registers compared to everything else."),
            _("Everyone seeing me touch myself? That's actually the tamest thing you could've shown."),
            _("Whatever. I've done worse with you since and the group probably knows anyway."),
        ],
        # ── Enthusiastic: thrilled in group context ──
        ("enthusiastic", "hj"): [
            _("Let the group see~ %(Pp)s doesn't make me feel half as good as you do~"),
            _("Ooh, everyone gets to see my skills? Fine by me~"),
            _("The whole chat seeing that? Good. I look amazing~"),
        ],
        ("enthusiastic", "bj"): [
            _("Everyone can see that? Perfect. Let them know what I can do~"),
            _("Mmm, showing off my skills to the whole group? I don't mind at all~"),
            _("The chat seeing me do that? Good. I want them to see how good I am~"),
        ],
        ("enthusiastic", "tj"): [
            _("Everyone seeing my chest like that? I love it. Post more~"),
            _("The whole group just saw that? Nice. I look incredible~"),
            _("Mmm, my titjob video for the whole chat? Let them be jealous~"),
        ],
        ("enthusiastic", "cowgirl"): [
            _("The group seeing me ride? Good. Let everyone know I'm the best~"),
            _("Everyone watching that? Perfect. They can see what they're missing~"),
            _("Mmm, the whole chat gets to watch me on top of you? I love it~"),
        ],
        ("enthusiastic", "creampie"): [
            _("You finishing inside me, shown to the group? That's the hottest thing ever~"),
            _("Everyone seeing that? Mmm, let them be jealous of what we have~"),
            _("A creampie video for the whole chat? Bold. I love it. Film more~"),
        ],
        ("enthusiastic", "anal"): [
            _("THAT video in the group? Oh, you're bold~ I like it. Let's make more~"),
            _("Everyone seeing my most scandalous video? Good. Let them know~"),
            _("The group just saw THAT? Fine by me. Let's give them a sequel~"),
        ],
        ("enthusiastic", "laying_down"): [
            _("The group seeing you on top of me? Love it. Let them see who owns me~"),
            _("Everyone watching that? Good. Let them know how good you are~"),
            _("Mmm, that angle is so hot. Glad the whole chat got to see it~"),
        ],
        ("enthusiastic", "masturbate"): [
            _("My private show for the whole group? I actually love that. Want a live version?"),
            _("Everyone watching my solo? They should see what I do when I'm with you~"),
            _("The chat seeing me touch myself? Hot. Next time film something even better~"),
        ],
    }

    # ==========================================================
    # 2. GROUP_VIDEO_OTHER_LINES — video is of a DIFFERENT girl, sent in group
    # ==========================================================
    GROUP_VIDEO_OTHER_LINES = {
        "hj": [
            _("You're showing the whole group another girl jerking you off? Bold."),
            _("Everyone just saw some girl's hand on you. Did you think this through?"),
            _("A handjob video... in the group chat. You really don't care, do you?"),
        ],
        "bj": [
            _("You just showed the whole group another girl sucking you off. Wow."),
            _("A blowjob from another girl... sent to ALL of us? Seriously?"),
            _("Everyone in this chat just watched some girl go down on you. Classy."),
        ],
        "tj": [
            _("Another girl's tits... shared with the whole group? Really?"),
            _("You sent a titjob video to all of us? What were you thinking?"),
            _("The whole group just saw some girl's chest around you. Nice move."),
        ],
        "cowgirl": [
            _("Another girl riding you... and you sent it to everyone? Wow."),
            _("The whole group just watched some girl on top of you. Was that the plan?"),
            _("A cowgirl video shared with all of us? You're shameless."),
        ],
        "doggy": [
            _("She's taking it from behind... wow."),
            _("Doggy style? She really let you film that?"),
            _("I can see everything from this angle..."),
        ],
        "anal": [
            _("Wait... is that her ass?! You did ANAL?!"),
            _("She let you do that to her butt AND film it?!"),
            _("Oh my god, that's going in her ass..."),
        ],
        "creampie": [
            _("You finished inside another girl and sent it to the GROUP?! What?!"),
            _("The whole chat just saw you creampie someone else. Are you insane?"),
            _("A creampie video... in the group chat?! Everyone just saw that!"),
        ],
        "laying_down": [
            _("You're on top of her... and you sent it to the group?! Seriously?!"),
            _("The whole chat just saw you pin another girl down. Wow."),
            _("That's her underneath you... everyone in this chat just watched that."),
        ],
        "masturbate": [
            _("You're sharing videos of some girl touching herself... to the group?"),
            _("Everyone just saw another girl's private moment. Why here?"),
            _("A masturbation video in the group chat? You have no boundaries."),
        ],
    }

    # ==========================================================
    # 3. GROUP_VIDEO_NONCONSENSUAL_LINES
    # ==========================================================
    GROUP_VIDEO_NONCONSENSUAL_LINES = [
        _("You filmed me without asking AND sent it to the GROUP?! I'm going to kill you!"),
        _("I didn't consent to being recorded and now EVERYONE in this chat has seen it?!"),
        _("You secretly recorded me and shared it with the whole group?! That's BEYOND messed up!"),
    ]

    # ==========================================================
    # 3b. GROUP_VIDEO_CUCKOLD_THREESOME — cuckold/threesome reactions in group
    # ==========================================================

    # Subject sees her cuckold video in group (BF was watching, everyone sees)
    GROUP_CUCKOLD_SELF_CHEATER = [
        _("Everyone in this chat just saw my boyfriend hold the camera while I... okay yes, I loved it."),
        _("The whole group knows my BF watched? Whatever. He was into it and so was I~"),
        _("You shared THAT with the group? Fine. They can all know I'm a terrible girlfriend."),
    ]
    GROUP_CUCKOLD_SELF_LOYAL = [
        _("EVERYONE just saw my boyfriend recording me?! In the GROUP CHAT?! I'm going to die!"),
        _("The whole group knows what happened?! That my boyfriend SAW?! Delete it! NOW!"),
        _("I can't believe everyone in this chat just found out about this... I feel so exposed..."),
    ]
    GROUP_CUCKOLD_SELF_CAMERA_LOVER = [
        _("The footage looks amazing but... the whole GROUP knows my boyfriend filmed it? That's a lot."),
        _("Great video quality... terrible choice of audience. Everyone knows my BF was the cameraman now."),
        _("I look incredible but knowing the group knows my boyfriend was RIGHT THERE watching..."),
    ]
    GROUP_CUCKOLD_SELF_CAMERA_HATER = [
        _("You put that in the GROUP?! My boyfriend filmed me against my wishes AND now EVERYONE sees?!"),
        _("I HATE being filmed and you shared it with the WHOLE CHAT?! My boyfriend recorded this! I'll destroy you BOTH!"),
        _("Everyone in this group just saw something I never wanted filmed in the first place! And my BF helped! I'M DONE!"),
    ]
    GROUP_CUCKOLD_SELF_DEFAULT = [
        _("The whole group just found out my boyfriend was there... recording... oh my god."),
        _("Everyone in this chat now knows my boyfriend watched me do that. This is humiliating."),
        _("You sent THAT to the group?! Everyone knows my boyfriend was right there filming?!"),
    ]

    # Subject sees her threesome video in group (another girl was watching/recording)
    GROUP_THREESOME_SELF_EXHIBITIONIST = [
        _("The whole group knows another girl watched me? GOOD. Let them all be jealous~"),
        _("Everyone in this chat can see I had an audience. And I put on a show worth watching."),
        _("A girl watched me and now the group knows? I love this. More people should watch me."),
    ]
    GROUP_THREESOME_SELF_SHY = [
        _("EVERYONE knows another girl was watching me?! In the group chat?! I want to disappear!"),
        _("The group found out someone else SAW me like that?! This is a nightmare!"),
        _("She was watching and now the whole group knows... I've never been more embarrassed in my life."),
    ]
    GROUP_THREESOME_SELF_DEFAULT = [
        _("The whole group just learned another girl was in the room... that's really personal..."),
        _("Everyone in this chat knows someone else was there watching. That's so exposing."),
        _("You shared THAT with the group? Now everyone knows another girl saw everything..."),
    ]

    # Recorder girl sees the video she filmed shared in group
    GROUP_THREESOME_RECORDER_CAMERA_LOVER = [
        _("That's MY camerawork! I should get credited! Everyone look at those angles!"),
        _("You're showing MY footage to the group? At least credit the cinematographer!"),
        _("I filmed that! Look at the quality! Everyone in this chat is welcome."),
    ]
    GROUP_THREESOME_RECORDER_CAMERA_HATER = [
        _("You showed the group the video I filmed?! I didn't want anyone knowing I was there!"),
        _("Everyone in this chat now knows I held the camera?! I never wanted to be involved!"),
        _("WHY would you share that?! Now the whole group knows I was in the room watching!"),
    ]
    GROUP_THREESOME_RECORDER_DEFAULT = [
        _("Hey! I didn't say you could show people that! The group didn't need to know I filmed it!"),
        _("You put MY recording in the group chat?! I thought that was private!"),
        _("Everyone in this chat just found out I was the camerawoman. Thanks for nothing."),
    ]

    # Uninvolved girls reacting to cuckold/threesome in group
    GROUP_UNINVOLVED_CUCKOLD = [
        _("Wait... her BOYFRIEND was there?! Recording?! What kind of relationship is that?!"),
        _("Am I seeing this right? Her BF held the camera? In the GROUP CHAT?! That's insane!"),
        _("Her boyfriend WATCHED and everyone in this group just found out?! This is wild!"),
    ]
    GROUP_UNINVOLVED_THREESOME = [
        _("Another girl was THERE?! Watching?! And now the whole group knows?!"),
        _("Someone else was in the room filming?! And you're sharing it with ALL of us?!"),
        _("Wait, another girl recorded this?! And now the whole chat is seeing it?! Wow!"),
    ]

    # Both subject + recorder in group: scripted exchange
    GROUP_THREESOME_BOTH_PRESENT = {
        "subject_initial": [
            _("Wait, you shared THAT?! And [recorder] is RIGHT HERE in this chat?!"),
            _("Everyone in this group just saw that... and [recorder] is reading this too?!"),
            _("Oh god... [recorder] is in this group... she filmed that... and now everyone knows..."),
        ],
        "recorder_camera_lover": [
            _("The footage speaks for itself! Everyone can appreciate my work~"),
            _("I'm proud of what I captured! The group chat is lucky to see this!"),
            _("You're welcome, everyone. That's MY camerawork you're admiring."),
        ],
        "recorder_camera_hater": [
            _("I didn't want anyone knowing I was involved! Why would you put this HERE?!"),
            _("Great, now the whole group knows I filmed that. I never should have agreed."),
            _("I'm mortified. Everyone in this chat knows I was there. I was holding the phone."),
        ],
        "recorder_default": [
            _("I... didn't think he'd show everyone. That was supposed to stay between us."),
            _("Hey! I filmed that in private! The group didn't need to see it!"),
            _("Wow, okay. So everyone knows I was there now. Cool. Thanks for the heads up."),
        ],
    }

    # ==========================================================
    # 4. GROUP_VIDEO_TRAIT_LINES
    # ==========================================================
    GROUP_VIDEO_TRAIT_LINES = {
        # camera_lover
        ("camera_lover", "self", "hj"): [
            _("My hand looks SO good in this shot... and the whole group gets to see it? Perfect."),
            _("The angle on my wrist, my nails... everyone in the chat can appreciate the aesthetics."),
        ],
        ("camera_lover", "self", "bj"): [
            _("My lips look incredible on camera... and the group gets to witness it. You're welcome."),
            _("Everyone in the chat can see how good I look on my knees. The camera loves me."),
            _("A blowjob video this gorgeous deserves a group audience, honestly."),
        ],
        ("camera_lover", "self", "tj"): [
            _("My chest on camera like that... the group is getting a SHOW. I look unreal."),
            _("Everyone can see how perfect my tits look in this video. No filter needed."),
        ],
        ("camera_lover", "self", "cowgirl"): [
            _("Me on top, on camera, shared with the group? I look like a goddess riding you."),
            _("The whole chat can see me in control... the camera angle is chef's kiss."),
            _("Everyone watching me ride you on video... I've never looked better."),
        ],
        ("camera_lover", "self", "penetration"): [
            _("Full sex tape and I look THIS good? The group is blessed to witness this."),
            _("Everyone in the chat can see every detail... and I look flawless. No complaints here."),
        ],
        ("camera_lover", "self", "creampie"): [
            _("A creampie on camera... and the whole group saw? The shot was actually gorgeous though."),
            _("Everyone watched you finish inside me on video... I should be embarrassed but I just look so hot."),
        ],
        ("camera_lover", "self", "masturbate"): [
            _("Me touching myself, on film, for the whole group? I bet I look incredible. Everyone is staring."),
            _("The group watching me get off on camera... the lighting was perfect. I look gorgeous."),
            _("A solo video of me in the group chat? I hope everyone screenshots it."),
        ],
        ("camera_lover", "other", "hj"): [
            _("A handjob video? The angle is okay but my hands are way prettier. Film me for the group."),
            _("Everyone can see her hand on you... the framing is decent but I'd look better."),
        ],
        ("camera_lover", "other", "bj"): [
            _("The camera work on her blowjob is fine... but the group would go crazy for MY lips instead."),
            _("Everyone watching her go down on camera... nice angle, wrong girl though."),
        ],
        ("camera_lover", "other", "tj"): [
            _("Her chest on camera for the whole group? Okay, but mine would look way better in that shot."),
            _("Everyone can see her titjob... the framing is wasted on her. I'd steal that angle."),
        ],
        ("camera_lover", "other", "cowgirl"): [
            _("Her riding you on camera for the group? Cute. But I'd look ten times better on top."),
            _("The whole chat watching her bounce on camera... wasted potential. I'd own that shot."),
        ],
        ("camera_lover", "other", "penetration"): [
            _("A sex video of her for the group? The production value is there but the star isn't. Cast me."),
            _("Everyone saw her on camera... she's fine but the group deserves to see ME in action."),
        ],
        ("camera_lover", "other", "creampie"): [
            _("A creampie on camera for the whole group... bold shot. I'd make it look way hotter though."),
            _("Everyone watching her get filled on video... nice cinematography, wrong actress."),
        ],
        ("camera_lover", "other", "masturbate"): [
            _("Her solo video in the group? The lighting is okay but I'd give a way better performance on camera."),
            _("Everyone watching her touch herself on film... amateur cinematography. Film me instead."),
        ],
        # camera_hater
        ("camera_hater", "self", "hj"): [
            _("My hand on you, on camera, in the GROUP?! Delete this before anyone screenshots it!"),
            _("You filmed a handjob and sent it to everyone?! I TOLD you no cameras!"),
        ],
        ("camera_hater", "self", "bj"): [
            _("My face, my mouth, on camera, in the GROUP CHAT?! This is a nightmare! Delete it NOW!"),
            _("You filmed me sucking you off and showed EVERYONE?! I will never forgive you for this!"),
            _("A blowjob on camera shared with the group... my face is RIGHT THERE! Delete everything!"),
        ],
        ("camera_hater", "self", "tj"): [
            _("My chest on camera for the WHOLE GROUP to see?! I'm going to destroy that phone!"),
            _("You filmed my tits and shared it with everyone?! This is the worst thing you've ever done!"),
        ],
        ("camera_hater", "self", "cowgirl"): [
            _("Me riding you, on camera, for the ENTIRE GROUP?! You can see my face, my body, everything!"),
            _("You filmed me on top and shared it with the chat?! The camera caught every detail! I'm dying!"),
        ],
        ("camera_hater", "self", "penetration"): [
            _("A full SEX TAPE of me shared with the group?! On CAMERA?! I want to disappear forever!"),
            _("You filmed us having sex and showed EVERYONE?! This is why cameras should be illegal!"),
        ],
        ("camera_hater", "self", "creampie"): [
            _("A CREAMPIE on camera in the GROUP CHAT?! That's the most humiliating thing possible on film!"),
            _("You posted the creampie in the GROUP CHAT?! That was supposed to stay between us! I will smash every camera you own!"),
            _("Everyone just saw a creampie on camera... MY creampie... I want every copy deleted NOW!"),
        ],
        ("camera_hater", "self", "masturbate"): [
            _("My most PRIVATE moment on camera AND in the group chat?! I will never feel safe with a phone near me again!"),
            _("You filmed me touching MYSELF and shared it with EVERYONE?! That's the most personal video possible!"),
            _("This is the worst thing you could have filmed. The MOST intimate, private moment. And the whole group has it."),
        ],
        ("camera_hater", "other", "creampie"): [
            _("Filmed a creampie and showed the group?! That's the worst possible thing to have on camera!"),
            _("A creampie... on video... in the group chat. Cameras are a plague on this world."),
            _("She got creampied on camera and the whole group saw?! This is why cameras should be banned!"),
        ],
        ("camera_hater", "other", "penetration"): [
            _("You filmed her having sex and sent it to everyone?! Cameras have no boundaries!"),
            _("The group just watched her get fucked on camera... this is exactly why I hate filming."),
            _("Sex on camera shared with the group... nothing is sacred anymore. Cameras ruin everything."),
        ],
        ("camera_hater", "other", "cowgirl"): [
            _("You filmed her riding you and shared it with everyone?! Her face, her body, all on camera!"),
            _("The group watched her on top of you on video... cameras steal every shred of privacy!"),
            _("Cowgirl on camera in the group chat?! She's completely exposed and everyone can see!"),
        ],
        ("camera_hater", "other", "bj"): [
            _("You filmed her sucking you off and showed the GROUP?! That's so degrading on camera!"),
            _("A blowjob on video shared with everyone... cameras make everything ten times worse."),
            _("The whole group watched that on camera?! Her mouth on you for everyone to see?! Disgusting!"),
        ],
        ("camera_hater", "other", "hj"): [
            _("You filmed her jerking you off and sent it to the chat?! Why does everything need to be filmed?!"),
            _("A handjob on camera for the whole group... is nothing off limits for you and your camera?"),
            _("The group saw her hand on you on video?! Cameras turn everything into a spectacle!"),
        ],
        ("camera_hater", "other", "tj"): [
            _("You filmed her chest on you and shared it with the GROUP?! Her tits on camera for everyone?! Vile!"),
            _("A titjob on video sent to the whole chat?! Cameras turn intimacy into a spectacle! Disgusting!"),
        ],
        ("camera_hater", "other", "masturbate"): [
            _("You saved a video of her touching herself and showed the GROUP?! That's the most private thing possible on camera!"),
            _("Her solo moment on film for the whole chat?! Cameras have zero boundaries! Delete it!"),
        ],
        # cum_slut + creampie
        ("cum_slut", "self", "creampie"): [
            _("Everyone can see you filling me up... honestly? That's kind of hot."),
            _("The whole group watching your cum inside me... I shouldn't like this but I do."),
            _("A creampie in the group chat... and all I can think is I want them to see you do it again."),
        ],
        ("cum_slut", "other", "creampie"): [
            _("You came inside her and showed the group? I want everyone to see you do that to ME."),
            _("She got a creampie and the whole chat knows? ...Next time, fill me up instead."),
            _("The group saw you cum inside her... I bet she didn't even appreciate it like I would."),
        ],
        # hate_cum + creampie
        ("hate_cum", "self", "creampie"): [
            _("The whole group just saw you cum inside me... that's so gross... why does my body tingle watching it back?!"),
            _("Everyone can see your cum dripping out of me... I hate this... but I've watched it three times already. For evidence. To be mad."),
            _("A creampie in the group chat?! My pussy was SO full... I mean, that's DISGUSTING and everyone saw!"),
        ],
        ("hate_cum", "other", "creampie"): [
            _("I can't believe you two are doing that... why would she let you fill up her pussy with all that cum... so deep... into her poor little pussy... and... OMG, forget it. GROSS!"),
            _("The whole group just watched you pump her full... all that cum flooding her insides... she just took it ALL... that's so... ugh. I need to stop rewatching this."),
            _("You came inside her and showed everyone?! Look at how much is dripping out of her... her pussy is just overflowing with your... I'm NOT fascinated. I'm disgusted."),
            _("She let you fill her up like that?! All that warm cum deep inside her... she didn't even try to stop you... that's so irresponsible. And I can't stop watching."),
        ],
        ("hate_cum", "self", "penetration"): [
            _("The whole group watching you fuck me... at least you didn't cum inside... even though my body was kind of... begging for it. Forget I said that!"),
            _("Everyone saw us having sex... the way you were thrusting... I could feel you getting close... good thing you didn't finish in me. Right? ...Right."),
            _("The group watched you inside me... so deep... I hate that everyone can see how wet I was. And no, I was NOT hoping you'd cum."),
        ],
        ("hate_cum", "other", "penetration"): [
            _("The group just watched you fuck her raw like that... she was taking every inch... I mean, that's gross. I'm not imagining anything."),
            _("You sent everyone a video of you deep inside her... the way she was moaning... disgusting. I watched it twice to fully judge you."),
            _("Everyone watching you pound her... she looked like she was about to lose it... that's so wrong to share. I'm definitely not rewinding this part."),
        ],
        ("hate_cum", "self", "cowgirl"): [
            _("The whole group can see me riding you... I was in control and I still couldn't stop... ugh, everyone knows how much I wanted it!"),
            _("Everyone watching me on top of you... going deeper each time... I hate that the group can see how desperate I looked. I wasn't desperate. Shut up."),
            _("Me riding you in the group chat... the way my hips kept moving on their own... I look like I was addicted to it. I WASN'T. My body is a liar."),
        ],
        ("hate_cum", "other", "cowgirl"): [
            _("She's riding you without a condom?! Is she insane?! If she keeps bouncing like that he's going to lose it and fill her up... all that cum rushing into her... that's SO stupid. I watched it four times."),
            _("No protection and she's on top like that?! One slip and her poor pussy is overflowing with... ugh. She's in control and she's CHOOSING to risk it. That's disgusting. And mesmerizing."),
            _("The whole group can see she's raw on top of you... going faster and faster... she could stop any time but she WON'T... if he cums inside her like that... I can't even. Why am I still watching?!"),
        ],
        ("hate_cum", "self", "bj"): [
            _("The whole group saw my mouth on you... and I know exactly what you were thinking about finishing... DON'T. Even in your fantasies. ...Unless you already did."),
            _("Everyone watching me suck you off... my lips around you... the group can probably tell I was enjoying it more than I should. I wasn't. Stop looking at me."),
            _("My mouth on you for the entire chat to see... I could taste how close you were... that's disgusting information and I don't know why I shared it. Forget I said anything."),
        ],
        ("hate_cum", "other", "bj"): [
            _("The group watched her go down on you... her mouth just... taking all of you... that's so gross. She seemed to really like it though. Not that I would."),
            _("Everyone just saw her lips wrapped around you... I wonder if she could taste... UGH, why am I thinking about that?! Disgusting!"),
        ],
        ("hate_cum", "self", "hj"): [
            _("The whole group saw my hand on you... stroking like that... I could feel you throbbing... I hate that everyone knows how into it I looked."),
            _("Everyone watching me jerk you off... my fingers were so close to... never mind. The point is the group shouldn't see this!"),
            _("My hand wrapped around you in the group chat... I could feel it twitching... getting harder... that's SO gross to see on video. I only watched it again to confirm how gross it was."),
        ],
        ("hate_cum", "other", "hj"): [
            _("The group watched her hand on you... working you like that... she looked like she wanted MORE than just her hand involved. Gross. I don't relate."),
            _("Everyone just saw her stroking you... her grip tightening... that's so... anyway. I'm judging, not enjoying. Obviously."),
        ],
        ("hate_cum", "self", "tj"): [
            _("The whole group watching your... thing... between my tits... that's so vulgar... why can't I stop replaying it?! For ANGER reasons!"),
            _("Everyone saw my chest wrapped around you like that... it's humiliating... and warm... and I definitely didn't squeeze tighter on purpose."),
            _("Your... thing sliding between my boobs for the entire chat... I can see how hard you were... that's disgusting. The warmth I felt was purely body heat. PURELY."),
        ],
        ("hate_cum", "self", "masturbate"): [
            _("Everyone in the group watching me pleasure myself... at least this is the ONE act without your disgusting mess."),
            _("The group saw me... doing that. Privately. But at least I was safe from any... fluids."),
            _("A video of me alone... I guess that's the only type where I don't have to worry about your mess."),
        ],
        ("hate_cum", "other", "tj"): [
            _("The group watched her tits around you like that... all slippery and... UGH. Revolting. I zoomed in to judge the angle. That's all."),
            _("Everyone saw her chest wrapped around you... she just let it slide between them... that's so gross. My tits would never... I mean, I would NEVER."),
        ],
        ("hate_cum", "other", "masturbate"): [
            _("The group watching her touch herself... at least there's no disgusting mess involved. That's the ONE redeeming quality. I watched twice to confirm."),
            _("Everyone saw her solo video... no gross fluids, just her. That's... fine. I'm not fascinated. I'm relieved it's clean."),
        ],
        # cum_slut (non-creampie)
        ("cum_slut", "self", "hj"): [
            _("My hand covered in your cum... and the whole group can see? Mmm, I want more."),
            _("Everyone watching me stroke you like that... they can tell how much I love feeling you throb."),
        ],
        ("cum_slut", "self", "bj"): [
            _("The whole group can see my mouth on you... I hope they noticed how eager I was."),
            _("Everyone watching me swallow you... the group knows exactly what kind of girl I am now. Good."),
            _("My lips wrapped around you for the whole chat to see... and I'd do it again right now."),
        ],
        ("cum_slut", "self", "tj"): [
            _("My tits around you for the whole group... I love how messy it gets between them."),
            _("Everyone can see your cum on my chest... honestly that's the best part of the video."),
        ],
        ("cum_slut", "self", "cowgirl"): [
            _("The whole group watching me ride you... they can see how desperate I was to make you cum."),
            _("Me on top, bouncing, for the entire chat... I was trying to drain every drop out of you."),
        ],
        ("cum_slut", "self", "penetration"): [
            _("The group just watched you inside me... I hope they could see how wet I was for it."),
            _("Everyone saw us having sex... and I wanted every last drop. The group can judge all they want."),
        ],
        ("cum_slut", "self", "masturbate"): [
            _("The whole group can see how wet I get thinking about your cum... I don't care who's watching."),
            _("Everyone watching me touch myself... I was thinking about you filling me up. They can probably tell."),
            _("My solo video in the group... they don't know what I was imagining. But you do."),
        ],
        ("cum_slut", "other", "hj"): [
            _("Her hand on you in the group chat... I bet she didn't even appreciate it. I would."),
            _("Everyone watching her stroke you... she's wasting it. My hands would do so much better."),
        ],
        ("cum_slut", "other", "bj"): [
            _("The group just watched her suck you off... I wonder if she swallowed. I definitely would."),
            _("Her mouth on you for the whole chat to see... I'm jealous and the group can probably tell."),
        ],
        ("cum_slut", "other", "tj"): [
            _("Her tits around you in the group chat... I bet mine would feel better for you."),
            _("Everyone watching her titjob... she probably didn't even want the mess. I'd love it."),
        ],
        ("cum_slut", "other", "cowgirl"): [
            _("Her riding you for the whole group... I'd ride you harder. Everyone would see the difference."),
            _("The chat watched her on top... she was holding back. I wouldn't."),
        ],
        ("cum_slut", "other", "penetration"): [
            _("The group just saw you inside her... next time let everyone watch you do that to ME."),
            _("Everyone watching her take you... she looked satisfied but I'd beg for more. The group would see."),
        ],
        ("cum_slut", "other", "masturbate"): [
            _("The group watching her touch herself... she's probably thinking about you. I know I would be."),
            _("Her solo video in the chat... cute. But I bet she wishes you were there to finish inside her~"),
        ],

        # ── cum_slut NO HISTORY — girl hasn't been with the player ──
        ("cum_slut", "other_nohist", "creampie"): [
            _("He came inside her...? I'm so jealous. I want that so badly."),
            _("A creampie... I've been dreaming about something like that. She's so lucky."),
        ],
        ("cum_slut", "other_nohist", "penetration"): [
            _("She gets to have him inside her and I don't? That's not fair..."),
            _("Watching this is torture. I want him so bad it hurts."),
        ],
        ("cum_slut", "other_nohist", "hj"): [
            _("She has her hands on him... I wish that was me right now."),
            _("I'd give anything to touch him like that. She doesn't even look that into it."),
        ],
        ("cum_slut", "other_nohist", "bj"): [
            _("She gets to taste him and I don't? Life is cruel."),
            _("I'd swallow every drop if I had the chance. She doesn't know how lucky she is."),
        ],
        ("cum_slut", "other_nohist", "tj"): [
            _("His cum between her tits... I want that to be me so badly."),
            _("She gets the titjob and the cum? I'm dying of jealousy over here."),
        ],
        ("cum_slut", "other_nohist", "cowgirl"): [
            _("She's riding him... god I wish I was in her place right now."),
            _("I'd ride him so much better. If only I had the chance..."),
        ],
        ("cum_slut", "other_nohist", "masturbate"): [
            _("She's touching herself thinking about him... honestly same."),
            _("At least she got close enough to have a video. I'm still waiting for my turn."),
        ],
        ("cum_slut", "other_nohist", "anal"): [
            _("Anal...? I've been curious about that. She's braver than me."),
            _("He went in her ass? I wonder what that feels like... I want to find out."),
        ],
        ("cum_slut", "other_nohist", "any"): [
            _("She's so lucky to be with him. I haven't even had the chance yet..."),
            _("Watching this just makes me want him more. When is it MY turn?"),
        ],

        # hardcore_sex + penetration
        ("hardcore_sex", "self", "penetration"): [
            _("The whole group can see you going at it... and you were too gentle. Go harder."),
            _("Everyone just watched us and honestly? It looks tame. Harder next time."),
        ],
        ("hardcore_sex", "other", "penetration"): [
            _("She can barely take it and the whole group can see. I wouldn't break that easy."),
            _("Everyone watching her struggle? I could handle way more. Film me next."),
        ],
        ("hardcore_sex", "self", "creampie"): [
            _("Rough AND a creampie, and the whole group saw? ...I'm not even embarrassed. More."),
            _("Everyone just watched you go all in on me. And I loved every second."),
        ],
        ("hardcore_sex", "other", "creampie"): [
            _("The whole group saw you go hard and finish inside her? Do that to me next. Publicly."),
            _("Rough creampie shared with everyone? Bold. But I can take it harder."),
        ],
        ("hardcore_sex", "self", "hj"): [
            _("A handjob? That's it? The group can see I was barely trying. Grab me harder next time."),
            _("Everyone watching me stroke you gently... boring. I want the group to see me WRECK you."),
        ],
        ("hardcore_sex", "self", "bj"): [
            _("The whole group watching me go easy on you? Shove it deeper next time. Let them see me gag."),
            _("Everyone saw that tame blowjob... I want the group to watch me choke on it. Do it rougher."),
        ],
        ("hardcore_sex", "self", "tj"): [
            _("Everyone watched that soft titjob... the group should see you thrust between them like you mean it."),
            _("Everyone saw how gentle you were with my tits? Next time squeeze them hard and go faster."),
        ],
        # being used is submissive, not hardcore (docs/plan_femdom.md D3)
        ("submissive", "self", "tj"): [
            _("My tits around you for the group to see... and you were so gentle? Squeeze them harder, use me."),
            _("The whole group saw me on my knees with my tits around you. I did exactly what you told me to."),
            _("Everyone can see I'm yours now. Next time just tell me how you want them, and I'll do it."),
        ],
        ("hardcore_sex", "self", "cowgirl"): [
            _("Me on top for the whole group... and I was being nice? Next time I'm breaking you. Let them watch."),
            _("Everyone saw me riding you gently? The group should see me slam down until you can't breathe."),
        ],
        ("hardcore_sex", "self", "masturbate"): [
            _("Me touching myself for the whole group? Boring. I need someone to actually WRECK me. This is nothing."),
            _("Everyone watching my solo video... that's the tamest thing I do. The group should see what happens when you go rough."),
        ],
        ("hardcore_sex", "other", "hj"): [
            _("The group watched her give a handjob... that grip looked weak. I'd squeeze harder."),
            _("Everyone saw her soft little strokes... the group can tell she doesn't know how to be rough."),
        ],
        ("hardcore_sex", "other", "bj"): [
            _("The whole group watched her suck you off... she barely went deep. I'd throat it for everyone to see."),
            _("Everyone saw that gentle blowjob... the group knows I could handle it way rougher."),
        ],
        ("hardcore_sex", "other", "tj"): [
            _("Her tits around you for the group... she was so careful. I'd let you pound between mine."),
            _("Everyone watching that soft titjob... the group can compare when it's my turn. I won't be gentle."),
        ],
        ("hardcore_sex", "other", "cowgirl"): [
            _("Her riding you for the whole group... she was barely bouncing. I'd ride you into the ground."),
            _("Everyone watched her weak cowgirl... the group would lose their minds seeing how I ride."),
        ],
        ("hardcore_sex", "other", "masturbate"): [
            _("The group watching her touch herself... that's it? She needs someone to pin her down and do it properly."),
            _("Everyone saw her solo act... weak. I'd show the group what real intensity looks like."),
        ],

        # ── hardcore_sex NO HISTORY — girl hasn't been with the player ──
        ("hardcore_sex", "other_nohist", "penetration"): [
            _("That's how he does it? I bet I could handle way more than that."),
            _("Interesting technique... but I'd want it rougher if it was me."),
        ],
        ("hardcore_sex", "other_nohist", "creampie"): [
            _("He came inside her? Bold. I wonder what that would feel like from him."),
            _("A creampie on camera... that takes guts. I respect that."),
        ],
        ("hardcore_sex", "other_nohist", "hj"): [
            _("A handjob? That's all she got? If that was me, we wouldn't stop there."),
            _("She looks bored giving that handjob. I'd put way more energy into it."),
        ],
        ("hardcore_sex", "other_nohist", "bj"): [
            _("She could go deeper. If I ever get the chance, I'd show him what a real blowjob looks like."),
            _("That blowjob looks tame. I bet I could do better."),
        ],
        ("hardcore_sex", "other_nohist", "tj"): [
            _("A titjob? Cute. If he ever tried that with me, it wouldn't be so gentle."),
            _("She's being so careful with it... boring. I'd squeeze harder."),
        ],
        ("hardcore_sex", "other_nohist", "cowgirl"): [
            _("She rides like she's afraid of breaking something. I'd go way harder."),
            _("That's cowgirl? More like a slow dance. I could show him what real riding looks like."),
        ],
        ("hardcore_sex", "other_nohist", "masturbate"): [
            _("Touching herself for the camera? She looks too gentle about it. I'd make a show of it."),
            _("Her solo game is weak. If I ever did that for him, it would be intense."),
        ],
        ("hardcore_sex", "other_nohist", "anal"): [
            _("Anal? And she barely reacted? If that was me, the whole campus would hear."),
            _("She took it in the ass like it was nothing. I wonder if I could handle it better."),
        ],
        ("hardcore_sex", "other_nohist", "any"): [
            _("Not bad... but I could do better. If he ever comes to me, he'll see real intensity."),
            _("She looks like she's holding back. I wouldn't hold back at all."),
        ],

        # cute_sex + penetration
        ("cute_sex", "self", "penetration"): [
            _("That looks so intense... and everyone saw it? Was I okay? This is so exposing..."),
            _("The whole group watching something so intimate... I wanted it gentler and more private."),
        ],
        ("cute_sex", "other", "penetration"): [
            _("That looks rough... and everyone had to watch? I hope she was alright."),
            _("The whole group saw that? You should be gentler... especially when others can see."),
        ],
        ("cute_sex", "self", "creampie"): [
            _("It was so gentle... and then you finished inside... and the whole group SAW?!"),
            _("That intimate moment shared with everyone... I'm blushing so hard right now."),
        ],
        ("cute_sex", "other", "creampie"): [
            _("So tender... then a creampie... and everyone in the chat just watched. That's personal."),
            _("The whole group seeing something so intimate... doesn't that feel wrong to you?"),
        ],
        ("cute_sex", "self", "hj"): [
            _("It was so tender... just my hand in yours... and the whole group is watching? That's too intimate..."),
            _("Everyone can see how gently I was touching you... the group shouldn't see something so personal."),
        ],
        ("cute_sex", "self", "bj"): [
            _("I was trying to be so sweet and careful... and the group saw all of it? That was just for us..."),
            _("Everyone watching me be so gentle with my mouth... the group makes it feel so exposed..."),
        ],
        ("cute_sex", "self", "tj"): [
            _("It was so soft and warm between us... and the whole group is watching? That feels too vulnerable..."),
            _("Everyone can see how tenderly I held you against my chest... the group shouldn't be part of this..."),
        ],
        ("cute_sex", "self", "cowgirl"): [
            _("Me on top, going slow, feeling every moment... and the whole group saw? That was our private rhythm..."),
            _("Everyone watched me ride you so softly... the group seeing that feels like they stole something..."),
        ],
        ("cute_sex", "self", "masturbate"): [
            _("Me touching myself... that's so intimate and private... and the whole group just watched? I feel so exposed..."),
            _("Everyone seeing something that personal... I was being so gentle with myself... the group shouldn't see that..."),
        ],
        ("cute_sex", "other", "hj"): [
            _("Her hand on you so gently... the group watching something that sweet feels wrong."),
            _("Everyone saw that tender moment... I hope she's okay with the group knowing."),
        ],
        ("cute_sex", "other", "bj"): [
            _("She looked so gentle and careful... the group shouldn't have seen something that intimate."),
            _("Everyone watching her be so sweet with her mouth... that was personal, not for the chat."),
        ],
        ("cute_sex", "other", "tj"): [
            _("That looked so soft and warm... the whole group watching feels like an invasion of her privacy."),
            _("Everyone saw her chest around you so gently... that shouldn't be shared with a group..."),
        ],
        ("cute_sex", "other", "cowgirl"): [
            _("Her riding you so softly... the whole group watching feels like we're intruding on something private."),
            _("Everyone saw her gentle rhythm... that kind of intimacy shouldn't be shared with a chat."),
        ],
        ("cute_sex", "other", "masturbate"): [
            _("Her touching herself... shared with the group? That's such a private, vulnerable moment..."),
            _("Everyone watching something so intimate and personal... the group shouldn't see her like that..."),
        ],
        # public_fetish
        ("public_fetish", "self", "hj"): [
            _("My hand on you, shared with the group... the risk of everyone seeing makes it so much hotter."),
            _("Everyone in the chat watching me stroke you... I'm getting excited just knowing they can see."),
        ],
        ("public_fetish", "self", "bj"): [
            _("The whole group watching me suck you off... my heart is racing and not from embarrassment."),
            _("Everyone seeing my mouth on you... the thrill of the group knowing is intoxicating."),
        ],
        ("public_fetish", "self", "tj"): [
            _("My tits around you for the whole chat... the exposure is making me tingle everywhere."),
            _("The group seeing my chest like that... knowing they're all watching makes it so much better."),
        ],
        ("public_fetish", "self", "cowgirl"): [
            _("Riding you for the whole chat to see... the group exposure is driving me crazy."),
            _("Everyone watching me on top... knowing they can all see me bouncing is such a rush."),
        ],
        ("public_fetish", "self", "penetration"): [
            _("The whole group watching us have sex... the risk, the exposure... I'm already turned on again."),
            _("Everyone seeing you inside me... the thrill of the group knowing is better than the sex itself."),
        ],
        ("public_fetish", "self", "creampie"): [
            _("A creampie in the group chat... every girl seeing you finish inside me... the danger is thrilling."),
            _("The whole group watching your cum drip out of me... the exposure makes it ten times hotter."),
        ],
        ("public_fetish", "self", "masturbate"): [
            _("Me touching myself, shared with the group... the risk of everyone seeing my most private act is intoxicating."),
            _("The whole chat watching me get off... knowing everyone can see makes the thrill so much better."),
        ],
        ("public_fetish", "other", "hj"): [
            _("A handjob shared with the whole group... the boldness of that is exciting to me."),
            _("Everyone seeing her hand on you in the chat... the risk of sharing that is thrilling."),
        ],
        ("public_fetish", "other", "bj"): [
            _("A blowjob in the group chat... the audacity of everyone seeing that is so hot."),
            _("The whole group watching her mouth on you... sharing something that explicit is a rush."),
        ],
        ("public_fetish", "other", "tj"): [
            _("Her tits shared with the whole chat... the exposure of that is exciting to watch."),
            _("Everyone seeing a titjob in the group... the openness of sharing that is thrilling."),
        ],
        ("public_fetish", "other", "cowgirl"): [
            _("Her riding you for the entire group... the risk of everyone seeing that is exciting."),
            _("The whole chat watching her on top... sharing something that exposed is a thrill."),
        ],
        ("public_fetish", "other", "penetration"): [
            _("Full sex in the group chat... the bravery of sharing that with everyone is electric."),
            _("The whole group watching them have sex... the public exposure is making me feel things."),
        ],
        ("public_fetish", "other", "creampie"): [
            _("A creampie shared with the entire group... the audacity of that exposure is incredible."),
            _("Everyone watching a creampie in the chat... sharing that with the group is so bold and exciting."),
        ],
        ("public_fetish", "other", "masturbate"): [
            _("Her touching herself shared with the whole group... the boldness of exposing something that private is exciting."),
            _("Everyone watching her solo moment together... sharing something that intimate with the chat is a rush."),
        ],
        # public_shy
        ("public_shy", "self", "hj"): [
            _("My HAND on you in the group chat?! What if someone screenshots it?! Delete it please!"),
            _("Everyone just saw me giving a handjob... if this gets outside the chat I'm finished!"),
        ],
        ("public_shy", "self", "bj"): [
            _("My FACE is right there giving a blowjob and the whole GROUP can see?! I'm going to be sick!"),
            _("Everyone in the chat saw my mouth on you... if anyone saves this my life is OVER!"),
            _("A blowjob in the group chat where everyone can screenshot?! Delete it NOW!"),
        ],
        ("public_shy", "self", "tj"): [
            _("My CHEST on display in the group?! What if someone forwards this?! I'm hyperventilating!"),
            _("Everyone just saw my tits in the chat... if this leaks I will never recover!"),
        ],
        ("public_shy", "self", "cowgirl"): [
            _("Me RIDING you in the group?! My face, my body, everything visible! Delete it immediately!"),
            _("The whole chat saw me on top of you... if someone shares this outside the group...!"),
        ],
        ("public_shy", "self", "penetration"): [
            _("A SEX VIDEO of me in the group chat?! What if someone screen records?! I can't breathe!"),
            _("Everyone just watched us have sex... if this gets out I will literally die! DELETE IT!"),
        ],
        ("public_shy", "self", "creampie"): [
            _("A CREAMPIE of me in the group?! That's the most exposing thing possible! If anyone screenshots...!"),
            _("Everyone saw you finish inside me... if that video leaves this chat my life is ruined! DELETE!"),
            _("A creampie shared with the group... I'm shaking... please promise no one will share this further!"),
        ],
        ("public_shy", "self", "masturbate"): [
            _("My most PRIVATE moment shared with the GROUP?! If anyone screenshots me touching myself I'm FINISHED!"),
            _("Everyone just saw me doing THAT?! That's the most personal thing possible! What if someone saves it?!"),
        ],
        ("public_shy", "other", "creampie"): [
            _("A CREAMPIE sent to the whole group?! What if someone screenshots THAT?! It'll be everywhere!"),
            _("You came inside her and shared it with everyone?! If that gets out her life is RUINED!"),
            _("The group saw a creampie?! That's the kind of thing that ends up leaked! Delete it NOW!"),
        ],
        ("public_shy", "other", "penetration"): [
            _("You shared a sex video with the whole group?! Anyone could save this! Think about that!"),
            _("Everyone just watched her have sex... if someone screenshots this it's over for her!"),
            _("A full sex video in the group chat?! What if this gets forwarded?! Please delete it!"),
        ],
        ("public_shy", "other", "cowgirl"): [
            _("Her riding you in the group chat?! Her face, her body, everything exposed! What if someone shares this?!"),
            _("The whole group watched her on top of you... if anyone screenshots that she's done for!"),
        ],
        ("public_shy", "other", "bj"): [
            _("A blowjob video in the GROUP?! Her face is RIGHT THERE! What if someone recognizes her?!"),
            _("Everyone saw her going down on you?! If that gets shared outside this chat...!"),
        ],
        ("public_shy", "other", "hj"): [
            _("You shared that with the whole group?! What if someone sends it outside the chat?!"),
            _("A handjob video for everyone to see... at least her face isn't as visible but STILL!"),
        ],
        ("public_shy", "other", "tj"): [
            _("Her CHEST in the group chat?! If someone saves that she'll be mortified! Why would you share that?!"),
            _("Everyone saw a titjob video... what if this gets forwarded?! Think about her privacy!"),
        ],
        ("public_shy", "other", "masturbate"): [
            _("You shared her touching HERSELF with the GROUP?! That's the most private thing possible! What if someone saves it?!"),
            _("Everyone just saw her most intimate moment... if that gets out of this chat she'll be destroyed!"),
        ],
        # virgin
        ("virgin", "self", "hj"): [
            _("My first time ever touching someone like that... and the whole group just watched? That was so new to me..."),
            _("Everyone just saw me give my first handjob... I barely knew what I was doing and the group SAW."),
        ],
        ("virgin", "self", "bj"): [
            _("My first time using my mouth on someone... and the whole group watched? I'm mortified..."),
            _("Everyone saw me go down on you for the first time... I had no idea what I was doing and the chat KNOWS."),
        ],
        ("virgin", "self", "tj"): [
            _("My first time doing that with my chest... and the group saw? That was so new and scary for me..."),
            _("Everyone watched my first titjob... I was so nervous and the whole chat could probably tell."),
        ],
        ("virgin", "self", "cowgirl"): [
            _("My first time on top of someone... and the group watched? I was shaking and everyone could see..."),
            _("Everyone saw me ride you for the first time... I barely knew what to do and the whole chat witnessed it."),
        ],
        ("virgin", "self", "creampie"): [
            _("My first time and you finished INSIDE me... and the GROUP saw?! That's the most overwhelming thing ever!"),
            _("Everyone watched you fill me up for the first time... I didn't even know what to expect and the whole chat knows."),
            _("A creampie on my first time, shared with the group... I'm still processing what happened and everyone already SAW."),
        ],
        ("virgin", "self", "masturbate"): [
            _("A video of me touching myself... when I've barely explored my own body... and the group just watched?!"),
            _("Everyone saw me doing something so private... I'm still figuring myself out and the whole chat KNOWS."),
        ],
        ("virgin", "other", "hj"): [
            _("A handjob from another girl shared with the group... meanwhile I haven't even done THAT. The chat is seeing everything."),
            _("Everyone watching her give a handjob while I'm still... inexperienced. The group can probably guess."),
        ],
        ("virgin", "other", "bj"): [
            _("The group just watched her go down on you... I've never even done that. Everyone can see how far behind I am."),
            _("A blowjob shared with the whole chat... I wouldn't even know where to start. The group doesn't need to know that."),
        ],
        ("virgin", "other", "tj"): [
            _("Her chest on you for the whole group... I've never done anything like that. Everyone can see what I'm missing."),
            _("A titjob shared with the chat... something I've never experienced. The group probably thinks I'm so innocent."),
        ],
        ("virgin", "other", "cowgirl"): [
            _("The group just watched her ride you... I've never been on top of anyone. Everyone can see she's way ahead of me."),
            _("Her riding you shared with the whole chat... I can barely imagine doing that. The group is seeing things I haven't."),
        ],
        ("virgin", "other", "penetration"): [
            _("Was that her first time? And the whole group just watched? That's so exposing..."),
            _("She let you film her having sex AND you shared it with everyone? I haven't even... wow."),
        ],
        ("virgin", "other", "creampie"): [
            _("A creampie shared with the group... I haven't even had sex and the chat is watching THIS? That's intense."),
            _("Everyone saw you finish inside her... I can barely process what that would feel like. The group is way ahead of me."),
        ],
        ("virgin", "other", "masturbate"): [
            _("Her touching herself shared with the group... at least that's something I can relate to. But the chat seeing it..."),
            _("Everyone watching her solo video... that's personal. Even I would be mortified if the group saw mine."),
        ],
        ("virgin", "self", "penetration"): [
            _("My first time having sex... and every girl in this chat just saw it. Oh god."),
            _("You shared my virginity being taken with the group?! That's the most personal thing EVER!"),
        ],
        # voyeur
        ("voyeur", "self", "hj"): [
            _("Watching my own hand on you while the group watches too... there's something exciting about that shared viewing."),
            _("The group seeing my handjob video at the same time as me... weirdly thrilling to watch myself with an audience."),
        ],
        ("voyeur", "self", "bj"): [
            _("Watching my mouth on you while the whole group watches... seeing myself from this angle with everyone is surreal."),
            _("The group and I watching me go down on you at the same time... I can't stop replaying it."),
        ],
        ("voyeur", "self", "tj"): [
            _("Watching my chest around you while the group sees it too... seeing myself like that with an audience is exciting."),
            _("The whole chat watching my titjob along with me... I look better than I expected. I keep rewatching."),
        ],
        ("voyeur", "self", "cowgirl"): [
            _("Watching myself ride you with the whole group... seeing my own body move like that is strangely hypnotic."),
            _("The group and I watching me on top together... I didn't know I looked like that. I can't look away."),
        ],
        ("voyeur", "self", "penetration"): [
            _("Watching myself have sex while the whole group watches... seeing it happen from outside is strangely addictive."),
            _("The group and I watching us together... the shared viewing of something so intimate is a rush."),
        ],
        ("voyeur", "self", "creampie"): [
            _("Watching you finish inside me while the group sees it too... seeing that moment from outside is intense."),
            _("The whole chat watching the creampie along with me... I've replayed that ending so many times."),
        ],
        ("voyeur", "self", "masturbate"): [
            _("Watching myself touch myself while the group watches... seeing my own pleasure from outside is surreal."),
            _("The whole chat and I watching my solo video together... it's like being a voyeur of my own body."),
        ],
        ("voyeur", "other", "hj"): [
            _("Watching her hand on you with the whole group... the shared viewing of her technique is exciting."),
            _("The group all seeing her handjob together... I love watching this with an audience."),
        ],
        ("voyeur", "other", "bj"): [
            _("Watching her mouth on you with everyone in the chat... the group viewing of this blowjob is addictive."),
            _("The whole group watching her go down on you together... I can't stop staring."),
        ],
        ("voyeur", "other", "tj"): [
            _("Watching her chest on you with the whole group... everyone staring at the same thing is thrilling."),
            _("The group all seeing her titjob together... there's something electric about the shared viewing."),
        ],
        ("voyeur", "other", "cowgirl"): [
            _("Watching her ride you with everyone in the chat... the group screening of her on top is incredible."),
            _("The whole group seeing her bounce together... I love that we're all watching this at the same time."),
        ],
        ("voyeur", "other", "penetration"): [
            _("Watching her have sex with you while the group watches... the shared viewing of something this intimate is a rush."),
            _("The whole group watching them together... seeing it with an audience makes it even more exciting."),
        ],
        ("voyeur", "other", "masturbate"): [
            _("Watching her touch herself with the whole group... seeing something that private with an audience is thrilling."),
            _("The group all seeing her solo moment together... I can't stop watching and I know everyone else is too."),
        ],
        ("voyeur", "other", "creampie"): [
            _("The whole group watching that go inside her... I can't be the only one staring."),
            _("Everyone just saw that creampie together. This is the best group chat ever."),
        ],
        # exhibitionist
        ("exhibitionist", "self", "hj"): [
            _("My hand on you, and the whole group gets to watch? Good. I hope they're enjoying the show."),
            _("Everyone seeing me stroke you... I want them ALL to see how good I am with my hands."),
        ],
        ("exhibitionist", "self", "bj"): [
            _("The whole group watching me suck you off? Perfect. I hope they can't look away."),
            _("Everyone seeing my lips on you... let them stare. I look amazing on my knees."),
        ],
        ("exhibitionist", "self", "tj"): [
            _("My tits out for the whole group? I'm proud of them. Let everyone see what they're missing."),
            _("Everyone watching my chest around you... I hope every girl in the chat is jealous."),
        ],
        ("exhibitionist", "self", "cowgirl"): [
            _("Riding you for the entire group... let them all see how I move. I'm putting on a show."),
            _("Everyone watching me on top? I want them to see every bounce. This is MY spotlight."),
        ],
        ("exhibitionist", "self", "penetration"): [
            _("Full sex for the whole group to see... and I want them to watch every second of it."),
            _("Everyone seeing you inside me? I love it. Let the whole chat see what they're missing."),
        ],
        ("exhibitionist", "self", "creampie"): [
            _("A creampie for the whole group... let them all see you fill me up. I'm not ashamed."),
            _("Everyone watching your cum drip out of me... I want them to see. Every. Drop."),
        ],
        ("exhibitionist", "self", "masturbate"): [
            _("Everyone in this chat just watched me get off. And I want them to replay it. Over and over."),
            _("The whole group seeing me touch myself? I came harder knowing they were all watching."),
            _("A solo show for the entire group? Best content I've ever made."),
        ],
        ("exhibitionist", "other", "hj"): [
            _("Her hand on you for the whole group... that's bold. I respect it. I'd show off more though."),
            _("Everyone watching her give a handjob... she's brave. I want to be the next one on display."),
        ],
        ("exhibitionist", "other", "bj"): [
            _("The group watching her suck you off... she's not shy. I love that. Film me next."),
            _("Everyone saw her mouth on you... she's got guts sharing that. I'd go further for the group."),
        ],
        ("exhibitionist", "other", "tj"): [
            _("Her chest out for the whole group... confident. But mine are better. Film me instead."),
            _("Everyone watching her titjob... she's bold. I want the group to see MY tits next."),
        ],
        ("exhibitionist", "other", "cowgirl"): [
            _("Her riding you for the entire chat... she owns it. I'd put on an even better show."),
            _("The group watching her on top... she's fearless. Let me show everyone how I ride next."),
        ],
        ("exhibitionist", "other", "penetration"): [
            _("Full sex shared with the group... she's living my dream. I want to be on display like that."),
            _("Everyone watching her have sex... the bravery. I'd love the group to see me next."),
        ],
        ("exhibitionist", "other", "creampie"): [
            _("A creampie shared with the whole group... she let everyone see everything. I'm impressed."),
            _("The group watching her get filled... that level of exposure is something I aspire to."),
        ],
        ("exhibitionist", "other", "masturbate"): [
            _("Her touching herself shared with the group? That takes guts. I'd give them a better solo show though."),
            _("Everyone watching her most private moment... she's bold for sharing that. I want my turn on display."),
        ],

        # ── exhibitionist NO HISTORY — girl hasn't been with the player ──
        ("exhibitionist", "other_nohist", "penetration"): [
            _("She's on camera getting fucked and everyone can see? I'm so jealous of the attention."),
            _("The whole group watching her... I want that kind of spotlight so badly."),
        ],
        ("exhibitionist", "other_nohist", "creampie"): [
            _("A creampie on camera for everyone? That's the dream. I wish it was me."),
            _("She got filled on video and shared it... I need that kind of exposure in my life."),
        ],
        ("exhibitionist", "other_nohist", "hj"): [
            _("Her hands on him, on camera, shared with everyone? I want to be on display like that."),
            _("A handjob for the whole group to see... I'd love that kind of attention."),
        ],
        ("exhibitionist", "other_nohist", "bj"): [
            _("Everyone watching her go down on him? I'd love the group to see me do that someday."),
            _("A blowjob on display for the chat... she's living my fantasy right now."),
        ],
        ("exhibitionist", "other_nohist", "tj"): [
            _("Her tits wrapped around him for everyone to see? I want that spotlight."),
            _("A titjob shared with the group... the attention must feel amazing."),
        ],
        ("exhibitionist", "other_nohist", "cowgirl"): [
            _("She's riding him on camera for everyone? God, I want to be seen like that."),
            _("Cowgirl on display... the exhibitionist in me is screaming with envy."),
        ],
        ("exhibitionist", "other_nohist", "masturbate"): [
            _("She shared her most private moment with the group? Bold. I respect it and I want my own."),
            _("Touching herself for the chat to see... I'd love to put on a show like that."),
        ],
        ("exhibitionist", "other_nohist", "anal"): [
            _("Anal on camera shared with everyone? That's intense. I want to be that exposed."),
            _("The whole group saw her take it in the ass... I'm jealous of the attention, not the act."),
        ],
        ("exhibitionist", "other_nohist", "any"): [
            _("She got all the attention and I got nothing. When is it my turn to be on display?"),
            _("I want the spotlight so bad. She's lucky she got filmed."),
        ],

        # cheater
        ("cheater", "self", "hj"): [
            _("My hand on you shared with the group? Evidence of my naughty side. I love the danger~"),
            _("Everyone watching me give you a handjob... the whole chat knows I'm a bad girl now."),
        ],
        ("cheater", "self", "bj"): [
            _("The group watching me on my knees for you? Proof I'm naughty. Let them stare~"),
            _("Everyone just saw me go down on you in the chat. The scandal is delicious."),
        ],
        ("cheater", "self", "tj"): [
            _("My chest on you shared with the group? The girls can see what a bad girl I am~"),
            _("Everyone watching my titjob... more evidence of me being naughty. I don't mind at all."),
        ],
        ("cheater", "self", "cowgirl"): [
            _("The group watching me ride you? Every girl in this chat knows I take what I want~"),
            _("Me on top, shared with everyone... proof I'm in control and loving every second."),
        ],
        ("cheater", "self", "penetration"): [
            _("A sex video of me shared with the group? Every girl knows now. And I don't care~"),
            _("The whole chat just saw proof I'm sleeping with you. Dangerous and exciting."),
        ],
        ("cheater", "self", "creampie"): [
            _("A creampie in the group chat? Maximum evidence of being naughty. I love the risk~"),
            _("Everyone saw you finish inside me... the most scandalous proof possible. And I want more."),
        ],
        ("cheater", "self", "masturbate"): [
            _("Me touching myself shared with the group? Every girl knows what I do in private. Good~"),
            _("The whole chat watching my solo video... the group has a taste of my naughty side."),
        ],
        ("cheater", "other", "creampie"): [
            _("You creampied another girl and showed the whole group? Save some for us~"),
            _("Everyone in the chat just saw you finish inside her. We all want a turn now."),
        ],
        ("cheater", "other", "hj"): [
            _("Another girl's hand on you shared with the group? We all know you get around. Save some for us~"),
            _("The chat saw her handjob... the whole group knows you're naughty. Not that it's a surprise."),
        ],
        ("cheater", "other", "bj"): [
            _("Another girl going down on you for the whole group? Bold. We all want a turn though~"),
            _("The chat just watched her blow you. The group knows you collect girls. I'm not judging."),
        ],
        ("cheater", "other", "tj"): [
            _("Another girl's chest on you shared with the group? We can all see you have options~"),
            _("The chat watching her titjob... the whole group knows what you're up to. As always."),
        ],
        ("cheater", "other", "cowgirl"): [
            _("Another girl riding you for the whole group? She's not your only option and everyone knows it~"),
            _("The chat watching her on top... the group can see you keep busy. Save some energy for us."),
        ],
        ("cheater", "other", "penetration"): [
            _("A sex video with another girl in the group? We all know you get around. Keep sharing~"),
            _("The chat just watched you with her. The whole group is your audience now. Enjoy it."),
        ],
        ("cheater", "other", "masturbate"): [
            _("Another girl's solo video shared with the group? You collect every type of content~"),
            _("The chat watching her touch herself... the group knows you have girls doing everything for you."),
        ],
        # loyal
        # loyal (base = single, no BF -- despair at breaking principles + forbidden arousal, group exposure adds shame)
        ("loyal", "self", "hj"): [
            _("The whole group saw my hand on you... I always had principles. Now everyone has proof I don't."),
            _("Everyone watching me do that... I swore I was better than this. The shame is unbearable. So is the thrill."),
        ],
        ("loyal", "self", "bj"): [
            _("The group saw me on my knees... I had standards. Values. Now everyone knows what my mouth was doing."),
            _("Everyone just watched me go down on you... the girl I used to be would be horrified. I can't tell if I am."),
        ],
        ("loyal", "self", "tj"): [
            _("My chest around you for the whole group... I always kept my dignity. Now everyone's seen me throw it away."),
            _("Everyone saw my tits wrapped around you... I had boundaries once. The group has evidence they're gone."),
        ],
        ("loyal", "self", "cowgirl"): [
            _("I rode you and the group saw... I CHOSE to climb on top. I can't blame anyone else. And the whole chat witnessed my fall from grace."),
            _("Everyone saw me on top of you... all my principles, gone. I was in control and I still gave in. The group knows exactly who I am now."),
        ],
        ("loyal", "self", "penetration"): [
            _("A sex video of me in the group... I gave myself to you and now everyone knows. Every principle I had, shattered for the whole chat to see."),
            _("Everyone watched me have sex... I always believed this should be sacred. The group having proof of my surrender... the shame burns. So does the desire."),
        ],
        ("loyal", "self", "creampie"): [
            _("A CREAMPIE in the group chat... you filled me up and the whole group watched it drip out. Everything I ever stood for... gone. Replaced by your cum."),
            _("Everyone saw you finish inside me... the most principled girl in the chat, full of cum for all to see. I should be destroyed. Part of me is alive for the first time."),
            _("The group watched your cum pour out of me... I swore I'd never be this girl. Now there's evidence for everyone. And I want it again. That's the worst part."),
        ],
        ("loyal", "self", "masturbate"): [
            _("A video of me touching myself, shared with the group... even my private moments betray the person I thought I was."),
            _("Everyone watching me pleasure myself... I always kept that sacred. Now the whole chat knows I've abandoned even that boundary."),
        ],
        ("loyal", "other", "hj"): [
            _("A handjob in the group... I believe in commitment. But I watched her hand on you longer than I should have."),
            _("Everyone saw her doing that... I value loyalty above all. So why am I still looking at this?"),
        ],
        ("loyal", "other", "bj"): [
            _("A blowjob shared with the group... I shouldn't be watching this. I value principles. But I haven't scrolled past it."),
            _("Everyone watching her mouth on you... I believe in meaningful connections. This should disgust me. It's not."),
        ],
        ("loyal", "other", "tj"): [
            _("Her chest on you in the group chat... I have values. Standards. But I keep looking at this."),
            _("Everyone seeing a titjob... I'm the principled one in this group. So why am I replaying it?"),
        ],
        ("loyal", "other", "cowgirl"): [
            _("Her riding you for the whole group to see... I value commitment. But watching her on top of you is making me question things."),
            _("Everyone saw her bounce on you... I'm the loyal one. The good one. But this video is testing that."),
        ],
        ("loyal", "other", "penetration"): [
            _("A full sex video in the GROUP... I believe this should be private and meaningful. Watching this is making me feel things I shouldn't."),
            _("Everyone watching you inside her... my principles say this is wrong. My body doesn't seem to care right now."),
        ],
        ("loyal", "other", "creampie"): [
            _("A creampie in the group... the most intimate act, shared with everyone. Everything I believe in says look away. I can't."),
            _("Everyone saw you finish inside her... I value loyalty and commitment above all. So why did that make my heart race?"),
        ],
        ("loyal", "other", "masturbate"): [
            _("Her touching herself shared with the group... I have principles. Values. But I haven't scrolled past this video."),
            _("Everyone watching her solo moment... I believe in boundaries and privacy. So why am I still looking at this?"),
        ],

        # anal_lover
        ("anal_lover", "self", "anal"): [
            _("My ass looks INCREDIBLE in this video... the group is getting a premium show~"),
            _("Everyone in the chat can see how much I love it... and I look amazing doing it."),
            _("Anal on camera for the group? I'm not even embarrassed. I'm proud."),
            _("That's my ass taking it like a champ. You're welcome."),
            _("Mmm, watching myself get fucked in the ass... I look good."),
        ],
        ("anal_lover", "other", "anal"): [
            _("Anal? Nice... but I bet I could take it better. Just saying."),
            _("She's having fun... but she doesn't love it like I would. Trust me."),
            _("The whole group is watching her do anal... I could put on a much better show."),
            _("She took it in the ass? Nice. Welcome to the club."),
            _("Look at her taking anal... not bad at all."),
        ],

        # anal_hater
        ("anal_hater", "self", "anal"): [
            _("You sent THAT to the group?! Everyone can see me in pain! Delete it NOW!"),
            _("The whole chat just watched me doing something I HATE. I want to disappear."),
            _("My most humiliating moment shared with EVERYONE?! I will NEVER forgive you!"),
            _("You're showing people THAT?! My ass was supposed to be private!"),
            _("I can't believe you filmed that... I hated every second and now everyone can see."),
        ],
        ("anal_hater", "other", "anal"): [
            _("Anal? Ugh... that poor girl. I could never do that. My stomach hurts just watching."),
            _("Everyone in the chat watching that... I turned away. That looks painful."),
            _("She's doing anal and you're SHARING it?! That's private AND awful!"),
            _("She let you do THAT to her butt? Poor girl..."),
            _("Her ass... oh god. I would never let anyone do that to me."),
        ],

        # hardcore_sex + anal
        ("hardcore_sex", "self", "anal"): [
            _("Yeah, that's me getting my ass wrecked. Send it to everyone."),
            _("My ass took a beating and I loved every second. Proof right there."),
        ],
        ("hardcore_sex", "other", "anal"): [
            _("She took it in the ass like that? Respect."),
            _("That's some intense anal... she can handle it."),
        ],

        # cute_sex + anal
        ("cute_sex", "self", "anal"): [
            _("P-please don't show anyone my... back there... please..."),
            _("You filmed that?! That's so embarrassing... my butt..."),
        ],
        ("cute_sex", "other", "anal"): [
            _("She did... that? In her... oh my..."),
            _("I can't even watch this... her poor butt..."),
        ],
        # lesbian — self (her video shared in group)
        ("lesbian", "self", "penetration"): [
            _("A man inside me... shared with the WHOLE GROUP?! Everyone here just saw a lesbian get..."),
            _("Everyone in this chat now has proof that I slept with a man. My life is ruined."),
        ],
        ("lesbian", "self", "creampie"): [
            _("A man came inside me AND it's in the group chat?! If my girlfriend sees this..."),
            _("A creampie video of a lesbian... shared with everyone. I want to disappear."),
        ],
        ("lesbian", "self", "bj"): [
            _("Everyone just saw me with a man in my mouth. I'm a LESBIAN. This can't be happening."),
            _("A blowjob video of me... in the group. A lesbian on her knees for a man. Great."),
        ],
        ("lesbian", "self", "masturbate"): [
            _("My most private moment shared with the group... at least there's no man involved."),
            _("Everyone watching me pleasure myself... at least this doesn't ruin my reputation as a lesbian."),
        ],
        ("lesbian", "self", "any"): [
            _("The whole group just saw me doing things with a man. I'm supposed to be a LESBIAN."),
            _("Everyone here now knows... this can never leave this chat."),
        ],
        # lesbian — other (she watches another girl's video, she is lesbian)
        ("lesbian", "other", "masturbate"): [
            _("Her touching herself... yeah, every girl does that. But the group didn't need to see it."),
            _("A solo video? Nothing shocking there. We all have our private moments."),
        ],
        ("lesbian", "other", "penetration"): [
            _("She's letting a man inside her? I'll never understand straight girls..."),
            _("Watching a man thrust into someone... everyone in the group seems to like this but me."),
        ],
        ("lesbian", "other", "any"): [
            _("A girl doing that with a man? Not my thing but I guess everyone else enjoys it."),
            _("I don't get the appeal. But you do you."),
        ],
        # lesbian + virgin combined (girl has BOTH traits)
        ("lesbian_virgin", "self", "hj"): [
            _("My first time touching a man like that... and I'm a LESBIAN... and the GROUP just saw it."),
            _("A handjob. My first sexual act ever. With a GUY. Shared with everyone. This is a nightmare."),
        ],
        ("lesbian_virgin", "self", "bj"): [
            _("My first time with someone in my mouth... and it's a MAN... and the whole group WATCHED."),
            _("I'm a lesbian who just gave her first blowjob to a guy. And everyone in this chat saw it."),
        ],
        ("lesbian_virgin", "self", "tj"): [
            _("My first time using my chest like that... on a MAN... and the group just saw everything."),
            _("A titjob. My first one. With a guy. In the group chat. I want to cease to exist."),
        ],
        ("lesbian_virgin", "self", "cowgirl"): [
            _("My first time... riding a MAN... and every girl in this chat just watched a lesbian lose it."),
            _("Everyone saw me on top of a guy for the first time. I'm a lesbian. I want to disappear."),
        ],
        ("lesbian_virgin", "self", "penetration"): [
            _("A man took my virginity... and the group just watched it happen to a LESBIAN. End me."),
            _("My first time having sex... with a MAN... shared with the whole group. I'm supposed to be gay."),
        ],
        ("lesbian_virgin", "self", "creampie"): [
            _("A man came inside me on my FIRST TIME... and I'm a LESBIAN... and the GROUP saw it all."),
            _("My virginity AND a creampie from a guy... shared with everyone. I'm a lesbian. Kill me now."),
        ],
        ("lesbian_virgin", "self", "masturbate"): [
            _("My first time on camera... at least it's just me. No man involved. But the group still SAW."),
            _("A solo video of me... at least there's no guy in it. But the whole group watching is mortifying."),
        ],
        ("lesbian_virgin", "other", "hj"): [
            _("A handjob video in the group... straight girl stuff. Not something I'd ever want to try."),
            _("Her hand on a guy... I've never done that and I never will. Not my thing."),
        ],
        ("lesbian_virgin", "other", "bj"): [
            _("Her mouth on a man... shared with the group. I'll never understand the appeal."),
            _("A blowjob in the group chat. Something I've never done and have zero interest in doing."),
        ],
        ("lesbian_virgin", "other", "penetration"): [
            _("She's having sex with a guy... and the group is watching. I'd never let a man do that."),
            _("A man inside her... shared with everyone. Straight girls can have that experience."),
        ],
        ("lesbian_virgin", "other", "creampie"): [
            _("A creampie in the group... that's intense even for straight girls. Definitely not for me."),
            _("He finished inside her and the group saw it. I can't even imagine wanting that."),
        ],
        ("lesbian_virgin", "other", "masturbate"): [
            _("Her touching herself shared with the group... I relate to that part at least. But the group seeing it..."),
            _("A solo video... nothing wrong with that. But the whole chat watching is a lot."),
        ],
        ("lesbian_virgin", "other", "any"): [
            _("Another girl doing that with a man... I've never done anything and I don't plan to. Not with a guy."),
            _("Watching her with a guy in the group chat. I'm a virgin AND a lesbian. That world is alien to me."),
        ],
    }

    # ==========================================================
    # 4b. GROUP_VIDEO_ATM_LINES — ATM-specific trait reactions
    # Fires when the video has "atm" flag set, in the group chat AND in a private chat (video_atm_pool).
    # Keys: (trait_or_default, subject); (trait_or_default, subject, "group") holds the lines that name the
    # group, heard only in the group chat. "<trait>_new": an eager trait she is still discovering (trait_line_keys).
    # ==========================================================
    GROUP_VIDEO_ATM_LINES = {
        # --- self (girl sees her OWN ATM video) ---
        ("_default", "self"): [
            _("You filmed me doing THAT?! Tasting where it just was?!"),
        ],
        ("_default", "self", "group"): [
            _("Ass to mouth... on camera... and the whole group just saw it."),
        ],
        ("hardcore_sex", "self"): [
            _("Ass to mouth on camera. That's filthy. I love it."),
            _("Yeah, I went ass to mouth. And I'd do it again. Film that too."),
        ],
        ("cute_sex", "self"): [
            _("I... I put my mouth on... after it was in my... oh god, people can SEE this?!"),
        ],
        ("cute_sex", "self", "group"): [
            _("That's me doing... THAT... and everyone in the chat just watched..."),
        ],
        ("cute_sex_hate_cum", "self"): [
            _("You recorded me tasting that after it was in my ass?! That's the worst thing you could have filmed!"),
        ],
        ("cute_sex_hate_cum", "self", "group"): [
            _("I hated doing that SO MUCH and you put it on camera for the GROUP?!"),
        ],
        ("anal_lover", "self"): [
            _("Watching myself go ass to mouth... I'd do it again right now."),
        ],
        ("anal_lover", "self", "group"): [
            _("Ass to mouth on video? The group gets to see the real me~"),
        ],
        ("anal_lover_new", "self"): [
            _("That's me going ass to mouth... I didn't know I'd like that. I still can't believe it."),
            _("Watching it back is so weird... I never thought I'd be into that. And I was."),
        ],
        ("anal_hater", "self"): [
            _("I already hated having it in my ass, and then you made me taste it AND filmed it?!"),
        ],
        ("anal_hater", "self", "group"): [
            _("The worst moment of my life is now on camera for everyone. Thanks."),
        ],

        # --- other (girl sees ANOTHER girl's ATM video) ---
        ("_default", "other"): [
            _("She went... from her ass... to her mouth? And you FILMED it?"),
        ],
        ("_default", "other", "group"): [
            _("Ass to mouth shared with the group?! That's... a lot."),
        ],
        ("hardcore_sex", "other"): [
            _("Ass to mouth? She's got guts. Literally."),
            _("She went ass to mouth? Bold. I respect it."),
        ],
        ("cute_sex", "other"): [
            _("She put her mouth on it after... I think I'm going to be sick..."),
            _("She did THAT after it was in her... I can't even look..."),
        ],
        ("cute_sex_hate_cum", "other"): [
            _("She tasted THAT? After it was in her ASS? That's revolting..."),
            _("I feel so bad for her... tasting that after it was THERE..."),
        ],
        ("anal_lover", "other"): [
            _("She went ass to mouth? Mmm... I'm jealous."),
            _("Ass to mouth... and she looked like she enjoyed it? Nice."),
        ],
        ("anal_hater", "other"): [
            _("She tasted it after it was in her ass?! Poor thing..."),
            _("Ass to mouth?! How could she stand that? My stomach hurts just thinking about it."),
        ],
    }

    # ==========================================================
    # 4c. GROUP_VIDEO_ANAL_CREAMPIE_LINES — anal creampie reactions
    # Fires when the video has "anal_creampie" flag set on a creampie vid (group chat AND private chat).
    # Keys: subject ("self" or "other"); (subject, "group"): lines that name the group, group chat only
    # ==========================================================
    GROUP_VIDEO_ANAL_CREAMPIE_LINES = {
        "self": [
            _("You came in my ASS and filmed it?! That's so much worse!"),
            _("My ass... full of your cum... on camera. I want to die."),
        ],
        ("self", "group"): [
            _("An anal creampie video?! In the GROUP?! Everyone just saw THAT?!"),
        ],
        "other": [
            _("You came in her ass AND recorded it? You're insane."),
            _("She took a creampie in her butt? Wow..."),
        ],
        ("other", "group"): [
            _("An anal creampie... shared with the whole group. That's intense."),
        ],
    }

    def video_group_table_pool(table, key, in_group):
        """A pool from a GROUP_VIDEO_* table the private chat shares: the key's lines (any chat) plus, in the group
        chat only, its "group" entry (lines that name the group)."""
        _gkey = (key if isinstance(key, tuple) else (key,)) + ("group",)
        return list(table.get(key, [])) + (list(table.get(_gkey, [])) if in_group else [])

    # ATM video: the first entry she matches picks the pool (the combo first). An eager trait she is still
    # discovering speaks only through its discovery key (trait_line_keys); without one the next entry speaks
    _VIDEO_ATM_TRAIT_ORDER = (
        ("cute_sex_hate_cum", ("cute_sex", "hate_cum")),
        ("anal_lover",        ("anal_lover",)),
        ("anal_hater",        ("anal_hater",)),
        ("hardcore_sex",      ("hardcore_sex",)),
        ("cute_sex",          ("cute_sex",)),
    )

    def video_atm_pool(girl, subject, in_group):
        """Her reaction pool to an ATM video (subject "self" / "other"), private chat or group chat."""
        _ht = getattr(girl, "has_trait", None)
        for _key, _needs in _VIDEO_ATM_TRAIT_ORDER:
            if not (_ht and all(_ht(_t) for _t in _needs)):
                continue
            for _k in (trait_line_keys(girl, _key) if len(_needs) == 1 else [_key]):
                _pool = video_group_table_pool(GROUP_VIDEO_ATM_LINES, (_k, subject), in_group)
                if _pool:
                    return _pool
        return video_group_table_pool(GROUP_VIDEO_ATM_LINES, ("_default", subject), in_group)

    # ==========================================================
    # 5. GROUP_VIDEO_PLAYER_GF_LINES — player has a GF, girl reacts in group
    # ==========================================================
    GROUP_VIDEO_PLAYER_GF_LINES = {
        ("self", "close"): [
            _("You sent this to the GROUP while you have a girlfriend?! Everyone can see!"),
            _("Does {0} know you're sharing our video with OTHER GIRLS?! This is so wrong!"),
            _("If {0} finds out you shared this with the group... we're ALL done."),
        ],
        ("self", "friendly"): [
            _("You have a girlfriend and you're sharing this with the whole group? Wow."),
            _("Does {0} know the group is watching this? ...Part of me doesn't even care."),
            _("Everyone in this chat can see us... while you date {0}. This is messy."),
        ],
        ("self", "distant"): [
            _("{0} has no idea the whole group just saw this, does she? Good."),
            _("Shared with the group behind {0}'s back. This is getting bold."),
            _("I've stopped feeling guilty about {0}. Especially in front of everyone."),
        ],
        ("self", "hostile"): [
            _("{0} is clueless and the whole group knows it now. Whatever."),
            _("Everyone in this chat can see what you do behind {0}'s back. I love it."),
            _("Does {0} even exist to you? Because the group sure knows she doesn't matter."),
        ],
        ("self", "cheater"): [
            _("Cheating on {0} AND sharing the proof with the group? Bold move~ I love it."),
            _("The whole chat just saw you cheat on {0}. And I'm living for it."),
            _("{0} could never compete. And now the whole group knows it."),
        ],
        ("other", "close"): [
            _("You're cheating on {0} with other girls AND sharing it with the group?! Horrible!"),
            _("Does {0} know you show this stuff to groups of girls?! This is wrong!"),
            _("Everyone in this chat just saw proof you cheat on {0}. That's terrible."),
        ],
        ("other", "friendly"): [
            _("Does {0} know the whole group is watching your other girls? ...Still watching though."),
            _("You cheat AND share it with everyone? {0} would be devastated."),
            _("The group just saw you with another girl while you date {0}. Messy."),
        ],
        ("other", "distant"): [
            _("The whole group knows more about your side girls than {0} does at this point."),
            _("Another girl behind {0}'s back, shared with everyone. You're collecting witnesses."),
            _("The group is basically your cheating diary now. {0} is the only one who doesn't know."),
        ],
        ("other", "hostile"): [
            _("{0} is a joke and the whole group can see the proof now. Whatever."),
            _("More girls behind {0}'s back? The group is enjoying the show."),
            _("Everyone in this chat sees what {0} doesn't. Honestly, just dump her already."),
        ],
        ("other", "cheater"): [
            _("So the whole group gets to watch you cheat on {0}? Bad boy~ Keep sharing."),
            _("Everyone in this chat knows {0} is clueless. And we love it."),
            _("{0} has no idea and the whole group has front row seats. Beautiful."),
        ],
    }

    # ==========================================================
    # 6. GROUP_VIDEO_PLAYER_GF_TYPE_LINES
    # ==========================================================
    GROUP_VIDEO_PLAYER_GF_TYPE_LINES = {
        ("self", "hj"): [
            _("A handjob video shared with the group while you have a girlfriend? Everyone just saw that!"),
            _("The whole chat knows I touched you like that... while you date {0}. Wow."),
        ],
        ("self", "bj"): [
            _("You shared me sucking you off with the GROUP while you date {0}?!"),
            _("Every girl in this chat just saw my mouth on you... behind {0}'s back."),
        ],
        ("self", "penetration"): [
            _("Sex tape shared with the group while you have a girlfriend?! EVERYONE can see!"),
            _("The whole chat just saw proof you're sleeping with me behind {0}'s back."),
        ],
        ("self", "creampie"): [
            _("You creampied me AND shared it with the group while dating {0}?! Are you INSANE?!"),
            _("Everyone in this chat just saw you finish inside me behind {0}'s back!"),
        ],
        ("other", "hj"): [
            _("Handjobs from other girls shared with the group while dating {0}? Shameless."),
            _("The whole chat just saw another girl's hand on you. Does {0} know?"),
        ],
        ("other", "bj"): [
            _("Blowjobs from other girls sent to the GROUP while you date {0}? Wow."),
            _("Everyone just watched some girl go down on you behind {0}'s back."),
        ],
        ("other", "penetration"): [
            _("You're sleeping around behind {0}'s back AND sharing it with the group?!"),
            _("The whole chat just saw you with another girl while you have a girlfriend."),
        ],
        ("self", "cowgirl"): [
            _("Me riding you shared with the group while you date {0}?! Everyone just saw that!"),
            _("The whole chat watched me on top of you behind {0}'s back."),
        ],
        ("other", "cowgirl"): [
            _("Another girl riding you, shared with everyone, while you date {0}. Shameless."),
            _("The group just watched her on top of you behind {0}'s back."),
        ],
        ("other", "creampie"): [
            _("You finished inside someone else, shared with the group, AND you have a girlfriend?!"),
            _("The whole chat just saw you creampie another girl while dating {0}. Monster."),
        ],
        ("self", "tj"): [
            _("My tits around you... shared with the GROUP... while you date {0}?!"),
            _("Every girl in this chat just saw my chest on you behind {0}'s back."),
        ],
        ("other", "tj"): [
            _("Another girl's tits on you shared with the group while you date {0}? Classy."),
            _("The whole chat saw a titjob from someone else behind {0}'s back."),
        ],
    }

    # ==========================================================
    # 7. GROUP_VIDEO_BF_TYPE_LINES — she has a BF, type-specific, in group
    # ==========================================================
    GROUP_VIDEO_BF_TYPE_LINES = {
        ("self", "hj"): [
            _("Everyone in this chat just saw me give a handjob... and I have a boyfriend..."),
            _("My boyfriend would die if he knew the whole group saw me doing that..."),
        ],
        ("self", "bj"): [
            _("The group just saw me going down on you... and I have a BOYFRIEND..."),
            _("My boyfriend can never know the whole chat watched me do this..."),
        ],
        ("self", "penetration"): [
            _("A sex tape of me... shared with the group... while I have a boyfriend. Oh god."),
            _("Every girl in this chat just saw me cheat on my boyfriend. I'm done."),
        ],
        ("self", "creampie"): [
            _("You finished inside me AND shared it with the group?! I have a BOYFRIEND!"),
            _("The whole chat just saw a creampie... and I have a boyfriend. I'm ruined."),
        ],
        ("other", "hj"): [
            _("I have a boyfriend and the whole group just watched me watch a handjob. Great."),
            _("Sending handjob videos to the group when you know I'm in a relationship? Classy."),
        ],
        ("other", "bj"): [
            _("I have a boyfriend and the group just saw me receive a blowjob video. Nice."),
            _("Sending blowjobs to someone with a boyfriend... in the group chat? Really?"),
        ],
        ("other", "penetration"): [
            _("I have a boyfriend and the whole group knows I'm watching sex videos. Perfect."),
            _("Everyone in this chat knows I just watched that... and I have a boyfriend."),
        ],
        ("self", "cowgirl"): [
            _("The whole group saw me riding you... and I have a boyfriend. This is a nightmare."),
            _("Everyone just watched me on top of you while I'm in a relationship..."),
        ],
        ("other", "cowgirl"): [
            _("Another girl on top of you, shared with the group, while I have a boyfriend. Wonderful."),
            _("I'm in a relationship and the group just saw me receive this. Why, just why?"),
        ],
        ("other", "creampie"): [
            _("A creampie video in the group while I have a boyfriend? Everyone can see this!"),
            _("I have a boyfriend and the whole group knows I just watched you cum inside another girl."),
        ],
        ("self", "tj"): [
            _("The group just saw my tits around you... and I have a boyfriend. I want to die."),
            _("A titjob on camera, shared with everyone, while I'm in a relationship..."),
        ],
        ("other", "tj"): [
            _("I have a boyfriend and the group just watched a titjob video. Why am I here?"),
            _("Titjob videos to the group when I'm in a relationship? You have no shame."),
        ],
    }

    # ==========================================================
    # 7b. GROUP_VIDEO_GF_TYPE_LINES — she has a GF, type-specific, in group
    # ==========================================================
    GROUP_VIDEO_GF_TYPE_LINES = {
        ("self", "hj"): [
            _("Everyone in this chat just saw me give a man a handjob... and I have a girlfriend..."),
            _("My girlfriend would die if she knew the whole group saw me doing that to a guy..."),
        ],
        ("self", "bj"): [
            _("The group just saw me going down on a man... and I have a GIRLFRIEND..."),
            _("My girlfriend can never know the whole chat watched me suck a guy's cock..."),
        ],
        ("self", "penetration"): [
            _("A sex tape of me with a man... shared with the group... while I have a girlfriend. Oh god."),
            _("Every girl in this chat just saw me take a cock while I'm supposed to be with a woman. I'm done."),
        ],
        ("self", "creampie"): [
            _("A man finished inside me AND it's shared with the group?! I have a GIRLFRIEND!"),
            _("The whole chat just saw a guy creampie me... and I have a girlfriend. I'm ruined."),
        ],
        ("other", "hj"): [
            _("I have a girlfriend and the whole group just watched me watch a handjob. Great."),
            _("Sending handjob videos to the group when you know I'm with a woman? Classy."),
        ],
        ("other", "bj"): [
            _("I have a girlfriend and the group just saw me receive a blowjob video. Nice."),
            _("Sending blowjobs to someone with a girlfriend... in the group chat? Really?"),
        ],
        ("other", "penetration"): [
            _("I have a girlfriend and the whole group knows I'm watching straight sex videos. Perfect."),
            _("Everyone in this chat knows I just watched that... and I have a girlfriend."),
        ],
        ("self", "cowgirl"): [
            _("The whole group saw me riding a man... and I have a girlfriend. This is a nightmare."),
            _("Everyone just watched me on top of a guy while I'm in a relationship with a woman..."),
        ],
        ("other", "cowgirl"): [
            _("Another girl on top of you, shared with the group, while I have a girlfriend. Wonderful."),
            _("I'm with a woman and the group just saw me receive this. Why, just why?"),
        ],
        ("other", "creampie"): [
            _("A creampie video in the group while I have a girlfriend? Everyone can see this!"),
            _("I have a girlfriend and the whole group knows I just watched you cum inside another girl."),
        ],
        ("self", "tj"): [
            _("The group just saw my tits around a man... and I have a girlfriend. I want to die."),
            _("A titjob for a guy on camera, shared with everyone, while I'm with a woman..."),
        ],
        ("other", "tj"): [
            _("I have a girlfriend and the group just watched a titjob video. Why am I here?"),
            _("Titjob videos to the group when I'm in a relationship with a woman? You have no shame."),
        ],
    }

    # ==========================================================
    # 8. GROUP_VIDEO_BF_SELF_LINES — she has a BF, video of herself, in group
    # ==========================================================
    GROUP_VIDEO_BF_SELF_LINES = {
        "in_love": [
            _("My boyfriend... and the whole group just saw this. I'm going to be sick."),
            _("If my boyfriend finds out the group watched this... my life is over."),
            _("This could ruin my relationship. And everyone in this chat is a witness."),
        ],
        "normal": [
            _("My boyfriend can never know the group saw this... promise me. ALL of you."),
            _("He can't find out this video was shared with everyone..."),
            _("Part of me doesn't care... but the whole group seeing it makes it worse."),
        ],
        "strained": [
            _("My boyfriend... I'm past saving now. Especially with everyone watching."),
            _("Another video of me cheating, now shared with the whole group. Great collection."),
            _("The whole group seeing this barely bothers me anymore. That's sad."),
        ],
        "miserable": [
            _("My boyfriend would leave me if he saw this. The whole group already has. Whatever."),
            _("I stopped caring what he thinks. And now the group knows everything too."),
            _("He'd be crushed. But honestly, the group seeing it doesn't change anything."),
        ],
        "cheater": [
            _("My boyfriend has no idea and the whole group just saw. Keep it secret, girls~"),
            _("He'd never suspect. And now the group is in on it. Fun."),
            _("My boyfriend is clueless. The group knows more about my sex life than he does."),
        ],
    }

    # ==========================================================
    # 9. GROUP_VIDEO_BF_OTHER_LINES — she has a BF, video of another girl, in group
    # ==========================================================
    GROUP_VIDEO_BF_OTHER_LINES = {
        "in_love": [
            _("I have a boyfriend and you're sending this to the group?! Not appropriate!"),
            _("Everyone in this chat knows I just watched this... and I have a boyfriend. Stop."),
            _("This is disrespectful to my relationship and the whole group is watching!"),
        ],
        "normal": [
            _("My boyfriend would lose it knowing the group saw me receive this..."),
            _("I shouldn't be watching this in a group chat... I have a boyfriend."),
            _("If my boyfriend finds out the whole group got this video..."),
        ],
        "strained": [
            _("I know I have a boyfriend... but the group watching together makes this exciting."),
            _("My boyfriend never does anything this hot... and now the whole group knows I think so."),
            _("I've watched enough of these in front of everyone to stop pretending I don't like them."),
        ],
        "miserable": [
            _("My boyfriend is boring. At least the group chat is entertaining."),
            _("Who cares about my boyfriend? The group just got the best content."),
            _("My boyfriend could never. And the whole group probably agrees."),
        ],
        "cheater": [
            _("My boyfriend has no idea I watch these with the group. He's irrelevant."),
            _("Send more to the group. My boyfriend doesn't need to know any of us saw this."),
            _("The group chat is more exciting than my relationship. Keep sharing."),
        ],
    }

    # ==========================================================
    # 8b. GROUP_VIDEO_BF_WATCHING_SELF — BF IS in the group, video of herself
    # ==========================================================
    GROUP_VIDEO_BF_WATCHING_SELF_LINES = {
        "in_love": [
            _("%(Pp)s just saw that... right here in the group... it's over."),
            _("%(pl)s is in this group. %(Pp)s just watched that. I can't breathe."),
        ],
        "normal": [
            _("%(pl)s is RIGHT HERE in this chat... %(pp)s saw everything..."),
            _("%(Pp)s just watched that with everyone else. There is no hiding this now."),
        ],
        "strained": [
            _("%(Pp)s saw it. Right here. In front of everyone. Maybe it is for the best."),
            _("%(pl)s is in this group and just watched that. I stopped caring."),
        ],
        "miserable": [
            _("%(pl)s is in the chat? Good. Let %(po)s see. I do not care anymore."),
            _("%(Pp)s just saw it. Big deal. What is %(pp)s going to do about it?"),
        ],
        "cheater": [
            _("%(pl)s just watched that in real time~ Oops."),
            _("%(Pp)s is in this group and just saw everything. Surprise~"),
        ],
    }

    # ==========================================================
    # 9b. GROUP_VIDEO_BF_WATCHING_OTHER — BF IS in the group, video of another girl
    # ==========================================================
    GROUP_VIDEO_BF_WATCHING_OTHER_LINES = {
        "in_love": [
            _("%(pl)s is watching this right next to me in the chat... this is so awkward."),
            _("%(Pp)s is in the group too. We are both seeing this right now. Great."),
        ],
        "normal": [
            _("%(pl)s just watched this video too... awkward."),
            _("%(Pp)s is in this group. We are both watching this together now."),
        ],
        "strained": [
            _("%(pl)s is here too but honestly? This is more exciting than anything %(pp)s does."),
            _("%(Pp)s is watching too? Good. Maybe %(pp)s will learn something from it."),
        ],
        "miserable": [
            _("%(pl)s is in this chat. So what? %(Pp)s is boring and this is not."),
            _("%(Pp)s is here too? I could not care less about %(poss)s reaction."),
        ],
        "cheater": [
            _("%(pl)s is watching the same video as me~ And I am enjoying it way more."),
            _("%(Pp)s is here too? Even better. Watching this together is kind of thrilling~"),
        ],
    }

    # ==========================================================
    # 10. GROUP_VIDEO_SELF_FIRST_LINES — first time seeing herself on video, in group
    # ==========================================================
    GROUP_VIDEO_SELF_FIRST_LINES = {
        "hj": [
            _("My first time seeing myself on video... and the whole GROUP gets to see it too?!"),
            _("I've never watched myself do this before... and everyone in this chat is watching with me!"),
        ],
        "bj": [
            _("First time seeing myself like this on video... and the whole group just saw it too!"),
            _("I've never watched myself go down on anyone before... and the GROUP had to be my audience?!"),
        ],
        "tj": [
            _("I've never seen myself doing a titjob on camera... and now the whole GROUP has too!"),
            _("My first time seeing my chest on video like that... shared with everyone. Great."),
        ],
        "cowgirl": [
            _("I've never seen myself ride someone on video... and the group just watched along!"),
            _("First time watching myself on top... with the entire chat as my audience!"),
        ],
        "creampie": [
            _("I've never seen a video of someone finishing inside me... and the GROUP just saw it first!"),
            _("First time watching a creampie of me... and the entire chat watched along. Oh god."),
        ],
        "laying_down": [
            _("I've never seen myself from that angle before... with you on top... and the GROUP saw it too?!"),
            _("First time watching myself get pinned down on video... shared with everyone. Perfect."),
        ],
        "masturbate": [
            _("I've never seen myself doing that on video... and the GROUP is watching with me?!"),
            _("My most private moment on camera for the first time... shared with everyone!"),
        ],
    }

    # ==========================================================
    # 11. GROUP_VIDEO_SELF_VETERAN_LINES — veteran (5+ acts), in group
    # ==========================================================
    GROUP_VIDEO_SELF_VETERAN_LINES = {
        "hj": [
            _("Another handjob video of me? The group already knows I'm good at these~"),
            _("At this point the whole group has seen my technique. You're welcome."),
        ],
        "bj": [
            _("The group has seen enough of these to know I'm the best at it~"),
            _("Another blowjob video? The chat already knows my mouth is talented."),
        ],
        "tj": [
            _("The group has quite the collection of my tits by now. I'm a regular star~"),
            _("Another titjob for the chat? They already know I'm the best."),
        ],
        "cowgirl": [
            _("The group has seen me ride you so many times by now. They know I'm the best~"),
            _("Another cowgirl video for the chat? I've perfected it. Everyone can see."),
        ],
        "creampie": [
            _("Another creampie video for the group? At this point they've lost count too~"),
            _("The chat has seen you finish inside me so many times. We're old news."),
        ],
        "laying_down": [
            _("The group already knows exactly how I look underneath you. I'm used to it~"),
            _("Another one of me laying there? The chat has seen this angle plenty by now."),
        ],
        "masturbate": [
            _("The group has seen me do this so many times. I'm basically their entertainment~"),
            _("Another solo video? The chat already knows exactly what I do by myself."),
        ],
    }

    # ==========================================================
    # 12. GROUP_VIDEO_SELF_AWARE_LINES — self-aware follow-up, in group
    # ==========================================================
    GROUP_VIDEO_SELF_AWARE_LINES = {
        ("camera_hater", "has_videos"): [
            _("...Wait. The group has seen videos of ME too. Oh god, everyone knows I'm a hypocrite."),
            _("...And I let you film me too. Now the whole chat knows I'm no better."),
        ],
        ("camera_lover", "has_videos"): [
            _("...But the group can confirm: my videos are way better than hers."),
            _("...Everyone in this chat knows my footage has better angles."),
        ],
        ("camera_lover", "no_videos"): [
            _("...Film me next and share it. I'll give the group something ACTUALLY worth watching."),
            _("...The group deserves better content. Like me. Film me."),
        ],
        ("hate_cum", "has_creampies"): [
            _("...The group already knows you've done the same to me. I can't judge in front of everyone."),
            _("...Everyone in this chat knows I've let you finish inside me too. I'm a hypocrite."),
        ],
        ("hate_cum", "no_creampies"): [
            _("...At least the group knows you've never done THAT to me. I still have my dignity."),
            _("...The chat knows I've done things with you too. But at least not that."),
        ],
        ("cum_slut", "has_creampies"): [
            _("...The group already knows you fill me up too. We're all in this mess together."),
            _("...I mean, everyone in this chat knows I beg for it too. Can't judge."),
        ],
        ("cum_slut", "no_creampies"): [
            _("...Not like I'm any different, and the group probably knows it."),
            _("...Everyone in this chat knows I love what you do to me too."),
        ],
        ("cheater", "has_bf"): [
            _("...The group knows I cheat on my boyfriend too. We're all terrible here."),
            _("...Everyone in this chat is watching me be a hypocrite. Whatever."),
        ],
        ("cheater", "no_bf"): [
            _("...I've been the other woman before. The group probably already guessed that."),
            _("...Not like I'm any better. The chat knows it."),
        ],
        ("loyal", "has_bf"): [
            _("...Not that I'm any better. I have a boyfriend too and the group KNOWS it."),
            _("...Everyone in this chat knows I'm just as guilty. What am I doing?"),
        ],
        ("loyal", "no_bf"): [
            _("...Not that the group thinks I'm innocent either. I've done things with you too."),
            _("...I'd like to act superior but the chat knows better."),
        ],
        ("hardcore_sex", "has_sex_vids"): [
            _("...The group has seen you go just as rough on me. I can't talk."),
            _("...Everyone in this chat knows I take it the same way. Hypocrite mode off."),
        ],
        ("hardcore_sex", "no_sex_vids"): [
            _("...Not that I can talk. The group knows I can handle just as much."),
            _("...Everyone in this chat knows I'd take it harder. Just not on camera."),
        ],
        ("cute_sex", "has_sex_vids"): [
            _("...The group has seen our videos too. At least ours are romantic."),
            _("...Everyone knows we have our own sweet moments. At least ours are better."),
        ],
        ("cute_sex", "no_sex_vids"): [
            _("...I can't judge in front of everyone. You're just as sweet with me."),
            _("...The group doesn't need to know everything... but I'm no different."),
        ],
        ("exhibitionist", "has_videos"): [
            _("...Who am I kidding? The group has videos of me too and I love it."),
            _("...I literally enjoy when the group sees my stuff. I'm no different."),
        ],
        ("exhibitionist", "no_videos"): [
            _("...Film me next. I want the group to see MY version."),
            _("...Honestly? I'd love it if the group had videos of me too."),
        ],
        ("public_shy", "has_videos"): [
            _("...Oh god, the group has videos of ME too. If my boyfriend finds this chat..."),
            _("...Wait, you have stuff on me too. And the whole group can see. I'm panicking."),
        ],
        ("public_shy", "no_videos"): [
            _("...What if you film ME and share it with the group next? I'd die!"),
            _("...At least there's no video of ME in this chat. Please keep it that way."),
        ],
        ("voyeur", "any"): [
            _("...And the whole group can see me watching it. I'm part of the problem."),
            _("...I'm literally enjoying this with an audience. No shame left."),
            _("...The group knows I watched the whole thing. Twice. I regret nothing."),
        ],
        ("_default", "has_videos"): [
            _("...Not that the group doesn't already have proof of ME doing the same things."),
            _("...Everyone in this chat knows I'm not innocent either. You have my videos."),
            _("...The group has seen plenty of me too. I can't really talk."),
        ],
        ("_default", "no_videos"): [
            _("...Not that the group thinks I'm innocent. I've done things with you too."),
            _("...I'm not exactly clean here and the whole chat probably knows it."),
            _("...At least there's no video of ME in this chat. Yet."),
        ],
    }

    # ==========================================================
    # 13. GROUP_VIDEO_GF_CHEATING_SHOCK — GF sees video of another girl in group
    # ==========================================================
    GROUP_VIDEO_GF_CHEATING_SHOCK = {
        "hj": [
            _("Is that another girl's hand on you?! And you sent it to the GROUP?!"),
            _("A handjob from another girl... shared with EVERYONE?! Are you KIDDING?!"),
        ],
        "bj": [
            _("She's sucking you off?! AND YOU SENT THIS TO THE GROUP?!"),
            _("Another girl going down on you, shared with everyone?! I'm going to be sick!"),
        ],
        "tj": [
            _("Another girl's tits on you?! And the WHOLE GROUP just saw?!"),
            _("A titjob from someone else, sent to EVERYONE?! Have you lost your mind?!"),
        ],
        "cowgirl": [
            _("She's RIDING you?! And you sent this to the ENTIRE GROUP?!"),
            _("Another girl on top of you shared with everyone?! HOW DARE YOU?!"),
        ],
        "sex": [
            _("You're having SEX with someone else?! AND THE WHOLE GROUP KNOWS?!"),
            _("A sex tape with another girl, sent to EVERYONE?! YOU'RE DEAD TO ME!"),
        ],
        "creampie": [
            _("You FINISHED INSIDE HER?! AND SHARED IT WITH THE GROUP?! I'M DONE!"),
            _("A creampie for another girl, sent to EVERYONE?! EVERYONE JUST SAW THAT!"),
        ],
        "masturbate": [
            _("You saved another girl touching herself AND sent it to the GROUP?!"),
            _("Someone else's private video shared with EVERYONE?! While you date ME?!"),
        ],
        "anal": [
            _("You did THAT with another girl?! AND THE ENTIRE GROUP JUST WATCHED?!"),
            _("Anal with someone else shared with EVERYONE?! I can't even..."),
        ],
    }

    # ==========================================================
    # 14. GROUP_VIDEO_GF_CHEATING_SHOCK_DEFAULT
    # ==========================================================
    GROUP_VIDEO_GF_CHEATING_SHOCK_DEFAULT = [
        _("Are you cheating on me?! AND YOU SENT PROOF TO THE ENTIRE GROUP?!"),
        _("What the FUCK is this?! Another girl?! AND EVERYONE IN THIS CHAT JUST SAW?!"),
        _("You're with someone else AND you let the whole group watch?! YOU'RE INSANE!"),
    ]

    # ==========================================================
    # 15. GROUP_VIDEO_GF_CHEATING_BREAKUP
    # ==========================================================
    GROUP_VIDEO_GF_CHEATING_BREAKUP = [
        _("We're DONE. And the whole group just witnessed it. Don't EVER talk to me again."),
        _("It's OVER. Everyone in this chat saw what you did. Lose my number. ALL of you are witnesses."),
        _("I'm breaking up with you RIGHT NOW in front of everyone. We're FINISHED."),
        _("Congratulations. You just lost me, and the whole group watched it happen. We're OVER."),
    ]

    # ==========================================================
    # 16. GROUP_VIDEO_FULL_REACTION_PANIC — other girl recognized, panic, in group
    # ==========================================================
    GROUP_VIDEO_FULL_REACTION_PANIC = {
        "cowgirl": [
            _("That's {name} riding you?! And the whole GROUP just saw?!"),
            _("Is {name} on top of you?! Shared with EVERYONE?! I can't believe this!"),
            _("{name} bouncing on you... and the whole chat is watching?! This is insane!"),
        ],
        "bj": [
            _("That's {name}'s mouth on you?! And the GROUP just saw?!"),
            _("Is {name} sucking you off in front of everyone?! In the CHAT?!"),
            _("{name} going down on you... shared with the whole group?! What?!"),
        ],
        "hj": [
            _("Is that {name}'s hand on you?! And the GROUP got this?!"),
            _("That's {name} jerking you off?! Shared with EVERYONE?! Seriously?!"),
            _("{name} touching you like that... and the whole chat saw?!"),
        ],
        "tj": [
            _("That's {name}'s chest around you?! And the WHOLE GROUP just watched?!"),
            _("Is {name} giving you a titjob?! In front of EVERYONE in this chat?!"),
            _("{name}'s tits on you... shared with the group?! Oh my god!"),
        ],
        "creampie": [
            _("You finished inside {name}?! AND SHARED IT WITH THE GROUP?! WHAT?!"),
            _("That's a creampie of {name}?! The whole CHAT just saw?! Are you insane?!"),
            _("You came inside {name} and everyone in this group knows?! I can't!"),
        ],
        "penetration": [
            _("You're having sex with {name}?! And the GROUP just watched?!"),
            _("That's {name} having sex with you?! Shared with EVERYONE?!"),
            _("A sex tape of {name}... sent to the whole group?! This is crazy!"),
        ],
        "any": [
            _("Is that {name}?! And you sent this to the ENTIRE GROUP?!"),
            _("That's {name} in this video?! The whole CHAT just saw?!"),
            _("You shared a video of {name} with EVERYONE in this group?!"),
        ],
    }

    # ==========================================================
    # 17. GROUP_VIDEO_FULL_REACTION_HORNY — other girl recognized, horny, in group
    # ==========================================================
    GROUP_VIDEO_FULL_REACTION_HORNY = {
        "cowgirl": [
            _("{name} riding you? Shared with the group? She's got moves, I'll give her that~"),
            _("The whole chat just saw {name} on top... I'm weirdly turned on watching with everyone."),
            _("Everyone in this chat is watching {name} bounce on you. Lucky girl~"),
        ],
        "bj": [
            _("{name} going down on you? In the group? ...She knows what she's doing~"),
            _("The group just watched {name}'s mouth on you. I'm not jealous, I'm impressed."),
            _("Everyone can see {name} on her knees. She looks like she enjoys it~"),
        ],
        "hj": [
            _("{name} working you with her hand in front of everyone? She's got technique~"),
            _("The group just saw {name} give you a handjob. She's good at it, I'll admit."),
            _("Everyone watching {name} touch you... and I'm the one getting turned on."),
        ],
        "tj": [
            _("{name}'s chest around you? Shared with the group? Those are impressive~"),
            _("The whole chat just saw {name}'s titjob. I have to admit she looks amazing."),
            _("Everyone watching {name}'s tits on you... even I'm impressed."),
        ],
        "creampie": [
            _("You filled {name} up and showed the group? She looked like she loved it~"),
            _("The whole chat just saw you finish inside {name}. That was hot, not gonna lie."),
            _("Creampie of {name} in the group? I'm jealous. Do that to me next~"),
        ],
        "penetration": [
            _("{name} taking you? Shared with everyone? She looks so into it~"),
            _("The group just watched you with {name}. She can definitely handle you."),
            _("Everyone seeing {name} have sex with you... I'm not jealous, I'm inspired~"),
        ],
        "any": [
            _("That's {name}? In the group chat? ...Honestly? That's hot."),
            _("Everyone just saw {name} in action. I'm not mad. I'm intrigued~"),
            _("The group watching {name} with you? She's got nothing to be embarrassed about."),
        ],
    }

    # ==========================================================
    # 18. GROUP_VIDEO_BF_JEALOUSY_PANIC — she has BF, recognizes other girl, panic
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_PANIC = {
        "hj": [
            _("That's {name} touching you?! I have a boyfriend and the GROUP just saw this?!"),
            _("Is {name} giving you a handjob?! Shared with everyone?! I have a BOYFRIEND!"),
            _("{name}'s hand on you... the group saw... and I have a boyfriend. This is bad."),
        ],
        "bj": [
            _("{name} sucking you off?! In the group chat?! I have a boyfriend and I'm freaking out!"),
            _("That's {name}'s mouth on you?! Everyone saw?! I shouldn't even be looking!"),
            _("The group just watched {name} blow you and I have a BOYFRIEND. Why am I still here?!"),
        ],
        "tj": [
            _("{name}'s tits around you?! In the group?! I have a boyfriend! Why is this here?!"),
            _("That's {name} giving a titjob?! Shared with everyone?! My boyfriend can never know!"),
            _("The group saw {name}'s chest on you... I have a boyfriend and I can't unsee this."),
        ],
        "cowgirl": [
            _("{name} riding you?! In the group chat?! I have a boyfriend! Stop sending these!"),
            _("That's {name} on top?! Everyone saw?! My boyfriend would lose it!"),
            _("The group watched {name} bounce on you... I have a boyfriend and I can't handle this."),
        ],
        "creampie": [
            _("You finished inside {name}?! The GROUP saw?! I have a boyfriend and I'm PANICKING!"),
            _("A creampie of {name} in front of everyone?! I have a BOYFRIEND! This is too much!"),
            _("The whole group saw you cum inside {name}... I have a boyfriend. I need to leave."),
        ],
        "penetration": [
            _("That's you having sex with {name}?! In the GROUP?! I have a boyfriend!"),
            _("{name} and you... sex... shared with everyone... I have a BOYFRIEND!"),
            _("The group just watched a sex tape of {name}... I have a boyfriend and I'm spiraling."),
        ],
        "any": [
            _("That's {name}?! In the group?! I have a boyfriend! Why would you share this?!"),
            _("Is that {name} in this video?! Everyone saw?! I'm in a RELATIONSHIP!"),
            _("The group just saw {name} with you... I have a boyfriend. I need to go."),
        ],
    }

    # ==========================================================
    # 19. GROUP_VIDEO_BF_JEALOUSY_HORNY — she has BF, recognizes other girl, horny
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_HORNY = {
        "hj": [
            _("{name} touching you... shared with the group... and I have a boyfriend. Why is this hot?"),
            _("I have a boyfriend but {name}'s technique in front of everyone... I'm impressed~"),
            _("The group saw {name}'s handjob and honestly? My boyfriend could never do this to me."),
        ],
        "bj": [
            _("{name} going down on you in the group chat... I have a boyfriend but I can't stop watching."),
            _("My boyfriend would hate this but {name} looks so good on her knees in front of everyone~"),
            _("The group just saw {name} blow you. I have a boyfriend but... more please."),
        ],
        "tj": [
            _("{name}'s tits in the group chat... I have a boyfriend but those are impressive~"),
            _("My boyfriend could never compare to watching {name} in front of everyone."),
            _("The group saw {name}'s chest on you. I have a boyfriend. I don't care right now."),
        ],
        "cowgirl": [
            _("{name} riding you in the group chat... I have a boyfriend but I'm mesmerized."),
            _("My boyfriend is nothing compared to watching {name} bounce in front of everyone~"),
            _("The group saw {name} on top. I have a boyfriend. But this is hotter than he'll ever be."),
        ],
        "creampie": [
            _("You filled {name} up in the group chat... I have a boyfriend but I want that too."),
            _("My boyfriend could never make me feel what I feel watching {name} get creampied~"),
            _("The group saw you cum inside {name}. I have a boyfriend. Do that to me instead."),
        ],
        "penetration": [
            _("{name} with you, shared with everyone... my boyfriend could never compare."),
            _("I have a boyfriend but watching {name} in the group is making me question everything."),
            _("The group saw {name} have sex with you. My boyfriend is irrelevant right now."),
        ],
        "any": [
            _("That's {name}? In the group? I have a boyfriend but... wow."),
            _("My boyfriend doesn't need to know the group chat is making me feel things~"),
            _("The group saw {name} with you. I have a boyfriend. I wish I didn't right now."),
        ],
    }

    # ==========================================================
    # 20. GROUP_VIDEO_BOTH_COMMITTED_PANIC
    # ==========================================================
    GROUP_VIDEO_BOTH_COMMITTED_PANIC = [
        _("She has a boyfriend too?! And the whole GROUP just saw?! How many of us are cheating?!"),
        _("Another girl with a boyfriend?! The group is watching this unfold and it's terrifying!"),
        _("She's taken too?! Everyone in this chat is a witness to this mess!"),
        _("Wait, she has a boyfriend AND the group just saw?! This has to stop!"),
    ]

    # ==========================================================
    # 21. GROUP_VIDEO_BOTH_COMMITTED_HORNY
    # ==========================================================
    GROUP_VIDEO_BOTH_COMMITTED_HORNY = [
        _("She has a boyfriend too? And the group gets to watch? Mmm, we're all bad girls here~"),
        _("Another taken girl, shared with everyone... the group is basically a cheating support group~"),
        _("She's taken too? The whole group knows your cock makes committed girls melt~"),
        _("So she has a boyfriend AND the group is watching? We're all in this together~"),
    ]

    # ==========================================================
    # 22. GROUP_VIDEO_BOTH_COMMITTED_LINES
    # ==========================================================
    GROUP_VIDEO_BOTH_COMMITTED_LINES = [
        _("She has a boyfriend too? And the whole group just found out? Are you collecting taken girls?"),
        _("She's in a relationship AND the group just saw? How many of us have boyfriends?!"),
        _("Another girl with a boyfriend? The group chat is becoming a cheaters' convention."),
        _("She's taken too?! The whole group knows now. You really do love committed girls."),
        _("Hold on, she has a boyfriend too? And the group is watching? This is a mess."),
    ]

    # ==========================================================
    # 23. GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_PANIC
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_PANIC = {
        "hj": [
            _("She has a boyfriend AND is touching you?! The group just saw two cheaters!"),
        ],
        "bj": [
            _("She has a boyfriend AND is sucking you off?! Everyone in this chat just witnessed double cheating!"),
        ],
        "cowgirl": [
            _("She has a boyfriend AND is riding you?! The group is watching two cheaters go at it!"),
        ],
        "creampie": [
            _("She has a boyfriend, you came inside, AND the group saw?! This is a disaster!"),
        ],
        "penetration": [
            _("She has a boyfriend AND the group just watched you two have sex?! We're all guilty!"),
        ],
        "any": [
            _("She has a boyfriend too?! And the whole group just watched?! We're ALL in trouble!"),
        ],
    }

    # ==========================================================
    # 24. GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_HORNY
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_HORNY = {
        "hj": [
            _("She has a boyfriend AND is touching you? And the group knows? We're all naughty~"),
        ],
        "bj": [
            _("She's cheating with her mouth AND the group saw? We taken girls really can't resist you~"),
        ],
        "cowgirl": [
            _("Riding you while cheating, in front of the group? I want my turn next~"),
        ],
        "creampie": [
            _("She has a boyfriend AND let you fill her up? The group saw two cheaters in love~"),
        ],
        "penetration": [
            _("Two cheaters having sex, shared with the group? We all know that feeling~"),
        ],
        "any": [
            _("She's taken too? And the group is watching? We're a whole club of naughty girls~"),
        ],
    }

    # ==========================================================
    # 25. GROUP_VIDEO_BF_JEALOUSY_SAME_ACT
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_SAME_ACT = {
        "hj": [
            _("She touches you the same way I do... and the group just saw. I feel exposed."),
            _("The whole group watching {name} do what I do... while I have a boyfriend. Ouch."),
            _("She does the same thing I do to you... and everyone in this chat knows it."),
        ],
        "bj": [
            _("She goes down on you the same way I do... and the group just watched."),
            _("The whole chat saw {name} use her mouth like I do... while I have a boyfriend."),
            _("She blows you the same way... and every girl in this group knows."),
        ],
        "tj": [
            _("She uses her chest like I do... and the whole group just saw both of us."),
            _("The group can compare our titjobs now... while I have a boyfriend. Great."),
            _("{name} does the same thing with her tits... and the whole chat watched."),
        ],
        "cowgirl": [
            _("She rides you like I do... and the whole group just watched."),
            _("The chat saw {name} on top... same as me. And I have a boyfriend."),
            _("She bounces on you the same way... and every girl here just saw."),
        ],
        "creampie": [
            _("She lets you finish inside like I do... and the group just saw both of us."),
            _("The whole chat knows she takes your cum just like me... while I have a boyfriend."),
            _("{name} gets creampied the same way... and the whole group is watching."),
        ],
        "penetration": [
            _("She has sex with you just like I do... and the group just saw it all."),
            _("The whole chat saw {name} with you... same as me. While I have a boyfriend."),
            _("She takes you the same way I do... and everyone in this group knows now."),
        ],
        "any": [
            _("She does the same things I do... and the whole group can compare now."),
            _("The chat just saw {name} with you. Same things I do. While I have a boyfriend."),
            _("She's doing what I do... and every girl in this group just watched."),
        ],
    }

    # ==========================================================
    # 26. GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED
    # ==========================================================
    GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED = {
        "hj": [
            _("She has a boyfriend AND she's touching you? And the group saw? We're both cheating."),
            _("Two girls with boyfriends and the group watching us react to handjob videos. Wow."),
        ],
        "bj": [
            _("She has a boyfriend AND is blowing you? The group is witnessing a cheating epidemic."),
            _("Two taken girls, one blowjob video, the whole group watching. What a mess."),
        ],
        "tj": [
            _("She has a boyfriend AND is using her chest? The whole group can see we're both cheaters."),
            _("Two taken girls watching titjob videos in a group chat. Rock bottom."),
        ],
        "cowgirl": [
            _("She has a boyfriend AND rides you? The whole group is watching us both cheat."),
            _("Two taken girls watching cowgirl videos together. This group is a disaster."),
        ],
        "creampie": [
            _("She has a boyfriend AND lets you finish inside? The group is watching double cheating."),
            _("Two girls with boyfriends watching creampie videos. The group knows everything."),
        ],
        "penetration": [
            _("She has a boyfriend AND sleeps with you? The group is watching two cheating disasters."),
            _("Two taken girls watching sex tapes together. This group is messy."),
        ],
        "any": [
            _("She has a boyfriend too? The whole group knows we're both cheaters now."),
            _("Two committed girls watching this together in the group. We're both terrible."),
        ],
    }

    # ==========================================================
    # 27. GROUP_VIDEO_DATING_PLAYER_LINES — she dates the player, in group
    # ==========================================================
    GROUP_VIDEO_DATING_PLAYER_LINES = {
        "other": {
            "cheater": [
                _("You're sharing other girls with OUR group, babe?! Bold move~ At least I'm the main one."),
                _("The whole group gets to see your side pieces? Fine, baby. Just remember who's number one~"),
                _("Everyone in this chat knows you cheat on me, love. I should care more. I don't~"),
            ],
            "loyal": [
                _("You're showing OUR group videos of other girls?! While we're DATING, baby?!"),
                _("The whole group just saw you cheat on me, babe! Everyone is a witness!"),
                _("I'm your GIRLFRIEND and you shared that with the group?! I'm heartbroken, love!"),
            ],
            "cum_slut": [
                _("You did that with another girl and shared it with the group, baby? Do it to me instead!"),
                _("The whole chat saw you with someone else, love. I want my turn~"),
                _("Everyone watching you with another girl... I'm jealous, babe. That should be ME."),
            ],
            "hate_cum": [
                _("You did THAT to another girl and showed the group, baby?! While dating ME?! Disgusting!"),
                _("The whole chat saw what you do to other girls, love. That's revolting. And we're DATING."),
            ],
            "hardcore_sex": [
                _("You're rough with other girls AND show the group, babe?! Be that rough with ME!"),
                _("The whole chat saw you go hard on someone else, baby. Why not me? I can take more."),
            ],
            "cute_sex": [
                _("You're that gentle with another girl, baby... and the group just saw? That hurts..."),
                _("Everyone in the chat saw you be sweet with someone else, love. While we're DATING. Ouch."),
            ],
            "camera_lover": [
                _("You filmed another girl AND shared with the group, baby?! Where's MY starring role?!"),
                _("The whole chat saw someone else on camera, love. I should be your leading lady!"),
            ],
            "camera_hater": [
                _("You film other girls and share with the group while dating ME, babe?! HORRIBLE!"),
                _("The whole group saw your disgusting camera hobby, baby. We're DATING!"),
            ],
            "_furious": [
                _("EVERYONE in this chat just saw you cheat on me, babe?! In OUR GROUP?!"),
                _("The whole group is watching proof that my boyfriend cheats! Great job, love!"),
                _("You shared this HERE?! Where EVERYONE can see?! While we're DATING, baby?!"),
            ],
            "_heartbroken": [
                _("You shared that with our group, baby... while we're together... I'm so hurt..."),
                _("The whole group just saw you with someone else, love. While I'm your girlfriend. I'm broken."),
                _("Everyone in this chat can see what you did to me, babe. To us. I can't stop crying."),
            ],
            "_default": [
                _("The whole GROUP just saw you with another girl, babe?! While we're DATING?!"),
                _("You shared a video of another girl in OUR group chat, baby?! Unbelievable!"),
                _("Every girl in this chat just saw my boyfriend with someone else, love. Great."),
            ],
        },
        "self": {
            "camera_lover": [
                _("Babe! You shared our video with the group?! ...I look amazing though, so I'll allow it."),
                _("The girls are seeing me with my boyfriend and honestly? The angle is perfection. Good job, love."),
                _("Our video in the group chat... well, at least everyone can see how gorgeous I am, honey~"),
            ],
            "camera_hater": [
                _("Are you SERIOUS right now?! Our private video in the GROUP?! I trusted you, babe!"),
                _("Baby, the group just saw our intimate moment?! Delete it from the chat RIGHT NOW!"),
                _("You promised those were just for us! The whole GROUP, babe?! I'm so angry!"),
            ],
            "exhibitionist": [
                _("Mmm, the whole group just saw us together? ...That's honestly kind of exciting, babe~"),
                _("Everyone watching our video... I should be embarrassed but I'm getting turned on, love."),
                _("Let them watch, baby. Now they all know what I get every night~"),
            ],
            "public_shy": [
                _("BABE! The GROUP just saw us?! Everyone is watching! I want to disappear!"),
                _("Our private video... in the group chat, baby?! I'm going to have a panic attack!"),
                _("Honey, WHY?! Now all the girls have seen me like that! I can't face them!"),
            ],
            "cum_slut": [
                _("The group just saw us together... mmm, they can see how good you treat me, baby~"),
                _("Everyone watching what we do? Fine by me, love. They should be jealous of what I get~"),
                _("Our video in the group, babe? Good. Let them see exactly why I'm addicted to you~"),
            ],
            "hate_cum": [
                _("Babe, the group just saw us?! That was already uncomfortable enough without an audience!"),
                _("Everyone watching THAT part?! I hated it and now the whole group SAW, baby!"),
            ],
            "cheater": [
                _("Our video in the group? Bold move, babe. The girls can see what they're missing~"),
                _("The group watching us? Good. Let them know you're taken. Well... mostly~"),
                _("Sharing our little secret with the group, baby? Naughty. I love it."),
            ],
            "loyal": [
                _("You shared our video with the group?! Baby, that was supposed to be OURS! Just ours!"),
                _("Our intimate moment... in the group chat, love?! I'm mortified! That was so special!"),
                _("Babe, that was OUR moment... private... and now every girl in the group has seen it..."),
            ],
            "hardcore_sex": [
                _("The group saw how rough you are with me, babe? Good. Now they know what I can handle."),
                _("Everyone watching us go at it, baby? They should take notes."),
                _("Our video in the group... let them see. Nobody can match what we do, love."),
            ],
            "cute_sex": [
                _("Our sweet moment... shared with the group, baby?! That was so personal..."),
                _("The whole group saw how gentle you are with me, love... I'm blushing so hard..."),
                _("Babe... that was our special time together... and now everyone saw how tender you are with me..."),
            ],
            "voyeur": [
                _("Watching our own video with the group... honestly, that's kind of hot, babe."),
                _("The whole group seeing us... and I'm watching it WITH them, love. Surreal but exciting."),
            ],
            "virgin": [
                _("You shared the video of my FIRST TIME with the GROUP, baby?! I will NEVER forgive you!"),
                _("Everyone just saw me lose my virginity?! In the group chat?! Babe, I'm DYING!"),
                _("My first time... OUR first time... and the whole group just watched it?! HOW COULD YOU?!"),
            ],
            "public_fetish": [
                _("Our video shared with the group, babe? The thrill of everyone seeing us... I'm into it~"),
                _("The whole group watching our video together... that's actually exciting, love~"),
                _("Mmm, everyone can see what we do together, baby. I like that more than I should~"),
            ],
            "_default": [
                _("You shared our video with the group, babe?! Everyone just saw that!"),
                _("The whole group watched our private moment, baby. Was that really necessary?"),
                _("Baby... why the group? That was between us... now all the girls have seen everything..."),
            ],
        },
    }

    # ==========================================================
    # 30. GROUP_VIDEO_EX_VIEWER_LINES — viewer is player's ex, in group
    # ==========================================================
    GROUP_VIDEO_EX_VIEWER_LINES = {
        ("self",): [
            _("So you're still sharing videos of me after we broke up? Classy, really classy."),
            _("We're not together anymore and the group still gets to see this? You have no shame."),
            _("A video of your EX in the group chat? You really haven't moved on, have you?"),
            _("We broke up. That video was from when I still called you 'baby'. Delete it."),
            _("Sharing our old videos with the group... those were from when we were happy. Stop it."),
        ],
        ("other",): [
            _("Already moved on to someone new AND sharing it with the group? Got it. Totally over it."),
            _("Seeing your new videos after we broke up... in the group chat. That stings more than I expected."),
            _("You replaced me and now everyone gets to see her? Okay. Cool. I'm fine."),
            _("We broke up and now I get to watch you with other girls in the group. Wonderful."),
            _("New girl already... I used to be the one in those videos. Whatever."),
            _("So the group gets to see your new thing. Cool. I'm not jealous. I'm NOT."),
        ],
    }

    # ==========================================================
    # 31. GROUP_VIDEO_OF_GF_NEUTRAL — 3rd girl sees video of player's GF (neutral, no suggestive)
    # ==========================================================
    GROUP_VIDEO_OF_GF_NEUTRAL_LINES = {
        "hj": [
            _("That's your girlfriend's hand on you... and the whole group is seeing it? Does she know?"),
            _("A handjob from your girlfriend... shared with all of us? That's private, dude."),
        ],
        "bj": [
            _("Your girlfriend going down on you... sent to the group? Does she know everyone saw that?"),
            _("That's your actual girlfriend in that video... and the group is watching? Wow."),
        ],
        "tj": [
            _("Your girlfriend's... okay, does SHE know the group is watching this?"),
            _("That's your girlfriend. In the group chat. Does she know about this?"),
        ],
        "cowgirl": [
            _("Your girlfriend riding you... and you sent it to all of us? Does she know?"),
            _("That's your actual girlfriend on top of you... shared with the group. Bold."),
        ],
        "creampie": [
            _("You finished inside your girlfriend AND shared it with the group? Does she know?!"),
            _("A creampie with your actual girlfriend... shared with everyone? That's intense."),
        ],
        "masturbate": [
            _("Your girlfriend touching herself... and the group is watching? Does she know?"),
            _("That's your girlfriend's private moment shared with all of us. Does she know?"),
        ],
        "_default": [
            _("That's your girlfriend in that video... and the group just saw it. Does she know?"),
            _("You sent a video of your actual girlfriend to the group chat? Wow."),
            _("I hope your girlfriend agreed to the whole group seeing that..."),
        ],
    }

    # ==========================================================
    # 29. GROUP_VIDEO_BLENDED_LINES — context + trait + subject + type, in group
    # Same keys as VIDEO_BLENDED_LINES. Group-aware versions.
    # ==========================================================
    GROUP_VIDEO_BLENDED_LINES = {
        # =============================================
        #  BF CONTEXT — she has a boyfriend
        # =============================================
        # -- bf + hate_cum --
        ("bf", "hate_cum", "self", "creampie"): [
            _("The group just saw you cum inside me... I HATED it and I have a boyfriend. Kill me."),
            _("Everyone in this chat knows you finished inside me. Disgusting. And I have a BOYFRIEND."),
        ],
        ("bf", "hate_cum", "self", "penetration"): [
            _("The group saw us together... I feel dirty. And everyone knows I have a boyfriend."),
            _("Everyone just watched me cheat on my boyfriend. At least you didn't finish inside..."),
        ],
        ("bf", "hate_cum", "self", "cowgirl"): [
            _("The group just watched me ride you... with a boyfriend at home. I feel sick."),
            _("Everyone saw me on top... I have a boyfriend and I hate everything about this."),
        ],
        ("bf", "hate_cum", "self", "bj"): [
            _("The group saw my mouth on you... I have a boyfriend and this makes me sick."),
            _("Everyone just watched me go down on you while I have a boyfriend. Disgusting."),
        ],
        ("bf", "hate_cum", "self", "hj"): [
            _("The whole group saw my hand on you... I have a boyfriend. I feel dirty."),
            _("Everyone just watched me jerk you off while I'm in a relationship. Gross."),
        ],
        ("bf", "hate_cum", "other", "creampie"): [
            _("You came inside another girl and showed the group?! I have a BF and that's revolting!"),
            _("The group just saw a creampie and I have a boyfriend watching this... disgusting!"),
        ],
        ("bf", "hate_cum", "other", "any"): [
            _("Sending this to the group while I have a boyfriend? That's nasty on every level."),
            _("The group watched that and I have a boyfriend. I don't want any part of this."),
        ],
        # -- bf + cum_slut --
        ("bf", "cum_slut", "self", "creampie"): [
            _("The group just saw you fill me up... I have a boyfriend but honestly it's hot."),
            _("Everyone watched you cum inside me. My boyfriend has no idea. The group does though~"),
        ],
        ("bf", "cum_slut", "self", "penetration"): [
            _("The group saw us together... I have a boyfriend but I looked good~"),
            _("Everyone just watched me cheat and honestly? I enjoyed every second. And the group knows."),
        ],
        ("bf", "cum_slut", "self", "cowgirl"): [
            _("The group watched me ride you behind my boyfriend's back. And I look amazing~"),
            _("Everyone saw me on top while I have a boyfriend. My technique is flawless though."),
        ],
        ("bf", "cum_slut", "self", "bj"): [
            _("The group saw me use my mouth on you while I have a boyfriend. I'm talented though~"),
            _("Everyone watched me blow you behind my boyfriend's back. Not ashamed."),
        ],
        ("bf", "cum_slut", "self", "hj"): [
            _("The group saw me touch you while I have a boyfriend. Light work~"),
            _("Everyone knows my hand was on you behind my boyfriend's back. Whatever."),
        ],
        ("bf", "cum_slut", "other", "creampie"): [
            _("You came inside another girl and showed the group? I have a BF but I'm jealous~"),
            _("The group saw that creampie... I have a boyfriend but I want that for myself."),
        ],
        ("bf", "cum_slut", "other", "penetration"): [
            _("You slept with another girl and the group saw? I have a BF but she's lucky."),
            _("Everyone watched you with her. I have a boyfriend. Still jealous though~"),
        ],
        ("bf", "cum_slut", "other", "cowgirl"): [
            _("She rides you in the group chat? I have a boyfriend but she's got competition~"),
            _("The group watched her on top. I have a BF but I'd ride you better."),
        ],
        # -- bf + camera_lover --
        ("bf", "camera_lover", "self", "creampie"): [
            _("A creampie on camera, shared with the group, while I have a BF? The footage is hot though."),
            _("Everyone saw you finish inside me on film. I have a BF. But the angle is perfect."),
        ],
        ("bf", "camera_lover", "self", "bj"): [
            _("The whole group saw me sucking you off on film. I have a BF but... I look amazing doing it."),
            _("Everyone watched that footage of my mouth on you. My boyfriend can never know, but the shot is perfect."),
        ],
        ("bf", "camera_lover", "self", "hj"): [
            _("My hand on you, shared with everyone. I have a boyfriend but the angle is incredible."),
            _("The group saw me stroking you on camera. I should feel guilty... but I just want a reshoot."),
        ],
        ("bf", "camera_lover", "self", "tj"): [
            _("You between my breasts, on film, shared with the group. My BF would die. But the footage is art."),
            _("Everyone saw my chest on camera doing that. I have a boyfriend but honestly? Great cinematography."),
        ],
        ("bf", "camera_lover", "self", "penetration"): [
            _("The whole group saw you fucking me on camera. My boyfriend can never find out... but let's film more."),
            _("Everyone watched that recording of us. I have a BF. But I look so good getting taken like that."),
        ],
        ("bf", "camera_lover", "self", "cowgirl"): [
            _("The whole group saw me riding you on film. I have a boyfriend... but I look incredible on top."),
            _("Everyone watched that footage of me on top. My BF would lose it. But the performance was flawless."),
        ],
        ("bf", "camera_lover", "other", "any"): [
            _("Another girl on your camera, shown to the group? I have a BF but film me better next time."),
            _("The group saw her footage while I have a boyfriend. My videos would blow theirs away."),
        ],
        # -- bf + camera_hater --
        ("bf", "camera_hater", "self", "creampie"): [
            _("Filmed, creampied, shared with the GROUP, and I have a BOYFRIEND?! Delete everything NOW!"),
            _("The group saw evidence of EVERYTHING. Camera + creampie + cheating. I want to die."),
        ],
        ("bf", "camera_hater", "self", "cowgirl"): [
            _("The group saw me RIDING you on camera?! I have a BOYFRIEND and I HATE being filmed! DELETE IT!"),
            _("Everyone saw me on top of you... on video... while I have a boyfriend. I want to disappear."),
        ],
        ("bf", "camera_hater", "self", "bj"): [
            _("The whole group saw me giving you a BLOWJOB on camera?! I have a BOYFRIEND! I'm DONE!"),
            _("A video of me with your... in my mouth. Shared with the GROUP. While cheating. Kill me now."),
        ],
        ("bf", "camera_hater", "self", "tj"): [
            _("The group saw my CHEST on camera doing THAT?! I have a BOYFRIEND! This is humiliating!"),
            _("Everyone saw the titjob video. I hate cameras, I have a boyfriend, and I want to scream."),
        ],
        ("bf", "camera_hater", "self", "hj"): [
            _("The group saw me jerking you off on video?! I have a BOYFRIEND! Even a handjob is too much!"),
            _("A handjob video shared with everyone... while cheating... and I HATE cameras. Perfect nightmare."),
        ],
        ("bf", "camera_hater", "self", "any"): [
            _("On camera, in the group, while I have a boyfriend?! This is my nightmare! DELETE IT!"),
            _("The whole group just saw me on film. I HATE cameras AND I have a boyfriend!"),
        ],
        ("bf", "camera_hater", "other", "any"): [
            _("I have a BF and you're sharing filmed footage in the group?! Cameras are the worst!"),
            _("Filming girls and sharing with the group while I'm in a relationship?! Despicable!"),
        ],
        # -- bf + cheater --
        ("bf", "cheater", "self", "creampie"): [
            _("Cheating on my BF with a creampie AND the group saw? Dangerous. I love it~"),
            _("The group knows you fill me up behind my BF's back. The thrill is unreal."),
        ],
        ("bf", "cheater", "self", "penetration"): [
            _("The group knows I cheat on my BF with you. Evidence and witnesses. Thrilling~"),
            _("Everyone saw proof I sleep with you behind my BF's back. The danger is exciting."),
        ],
        ("bf", "cheater", "self", "cowgirl"): [
            _("The group saw me ride you behind my BF's back. Everyone's a witness now~"),
            _("Riding you while cheating AND the group watched? Maximum naughty."),
        ],
        ("bf", "cheater", "self", "bj"): [
            _("The group saw me blow you behind my BF's back. What a scandalous chat~"),
            _("Going down on you, cheating, and the whole group knows. Living dangerously."),
        ],
        ("bf", "cheater", "self", "hj"): [
            _("The group saw me jerk you off behind my BF's back. Light cheating with witnesses~"),
            _("A handjob behind my BF's back, watched by the group. Just getting started."),
        ],
        ("bf", "cheater", "other", "creampie"): [
            _("Other girls getting creampied and the group gets to watch? We're all bad here~"),
            _("The group saw you finish in another girl. My BF is clueless. This is fun."),
        ],
        ("bf", "cheater", "other", "any"): [
            _("Other girls in the group while I cheat on my BF? We're a whole network~"),
            _("The group watches your conquests. My BF has no idea. Keep sharing~"),
        ],
        # -- bf + loyal --
        ("bf", "loyal", "self", "creampie"): [
            _("The group saw you finish inside me... I have a BF... everyone is a witness to my shame."),
            _("A creampie shared with the group. I have a boyfriend. I'm the worst person alive."),
        ],
        ("bf", "loyal", "self", "penetration"): [
            _("The group saw us have sex. I have a boyfriend. Everyone knows I'm a cheater now."),
            _("Everyone watched me betray my boyfriend. The guilt with an audience is unbearable."),
        ],
        ("bf", "loyal", "self", "cowgirl"): [
            _("The group watched me ride you while I have a boyfriend. The shame with witnesses..."),
            _("On top of you, cheating, and the whole group knows. I'm the worst girlfriend ever."),
        ],
        ("bf", "loyal", "self", "bj"): [
            _("The group saw my mouth on you while I have a BF. Everyone knows I'm unfaithful now."),
            _("Going down on you behind my BF's back... and the group is witnessing my betrayal."),
        ],
        ("bf", "loyal", "self", "hj"): [
            _("Even a handjob... the group saw. I have a BF. I'm supposed to be loyal..."),
            _("The whole group knows I touched you while having a boyfriend. I'm so ashamed."),
        ],
        ("bf", "loyal", "other", "creampie"): [
            _("A creampie shared with the group while I have a BF? This is wrong on every level!"),
            _("The group watched you finish inside her. I have a boyfriend. Everything about this is terrible."),
        ],
        ("bf", "loyal", "other", "any"): [
            _("I have a BF and the group is watching your videos? I shouldn't even be in this chat!"),
            _("The whole group saw that. I have a boyfriend. I believe in loyalty. This is wrong."),
        ],
        # -- bf + hardcore_sex --
        ("bf", "hardcore_sex", "self", "creampie"): [
            _("Rough AND a creampie, shared with the group, while I have a BF? My kind of scandal."),
            _("The group saw you go hard and finish inside me. My BF could never. Everyone knows now."),
        ],
        ("bf", "hardcore_sex", "self", "penetration"): [
            _("The group saw how rough you are with me while I have a BF. He could never match that."),
            _("Everyone watched you pound me behind my BF's back. They know he's not enough."),
        ],
        ("bf", "hardcore_sex", "self", "cowgirl"): [
            _("The group saw me ride you hard while I have a BF. He could never make me move like that."),
            _("Everyone watched me go wild on top. My BF is boring. The group knows it now."),
        ],
        ("bf", "hardcore_sex", "other", "penetration"): [
            _("The group saw you go hard on another girl. I have a BF but you're rougher than him."),
            _("Everyone watching you pound her. I have a boyfriend but she clearly needed someone rougher."),
        ],
        ("bf", "hardcore_sex", "other", "cowgirl"): [
            _("She rides you hard in the group chat? I have a BF but she's living my fantasy."),
            _("The group saw her go wild on you. My boyfriend is boring. She's lucky."),
        ],
        # -- bf + cute_sex --
        ("bf", "cute_sex", "self", "creampie"): [
            _("So tender... then you finished inside... and the group SAW. I have a BF. This is bittersweet."),
            _("Everyone saw us be intimate and then the creampie. I have a boyfriend. This hurts."),
        ],
        ("bf", "cute_sex", "self", "penetration"): [
            _("The group saw how gentle you are with me... I have a BF and it looks so loving. I feel guilty."),
            _("Everyone watching us be intimate while I have a boyfriend... the guilt is crushing."),
        ],
        ("bf", "cute_sex", "self", "cowgirl"): [
            _("The group saw me slowly ride you... I have a BF and it looked so intimate. I feel terrible."),
            _("Everyone watched me gently ride you while I cheat on my boyfriend. The group knows my shame."),
        ],
        ("bf", "cute_sex", "other", "penetration"): [
            _("The group saw how gentle you are with her... I have a BF. It made me feel things..."),
            _("Everyone watched you be sweet with another girl. I have a boyfriend. Why does this affect me?"),
        ],
        ("bf", "cute_sex", "other", "cowgirl"): [
            _("She rides you gently in the group... I have a BF but that looks so intimate..."),
            _("The group saw her slowly ride you. I have a boyfriend. It made me sad."),
        ],
        # -- bf + exhibitionist --
        ("bf", "exhibitionist", "self", "creampie"): [
            _("Creampie on video, shared with the group, while I have a BF? Maximum exposure. I love it."),
            _("The group saw you fill me up. I have a BF. The audience makes it hotter~"),
        ],
        ("bf", "exhibitionist", "self", "any"): [
            _("On display in the group while I have a BF? The exposure is thrilling~"),
            _("The group watching me cheat on my boyfriend... I should be scared but I'm excited."),
        ],
        # -- bf + public_shy --
        ("bf", "public_shy", "self", "creampie"): [
            _("A creampie video in the GROUP while I have a BF?! If he sees this chat I'm DONE!"),
            _("Everyone saw you finish inside me! I have a BOYFRIEND! The group is evidence!"),
        ],
        ("bf", "public_shy", "self", "any"): [
            _("The GROUP saw this while I have a BF?! This is my worst nightmare with witnesses!"),
            _("Everyone in this chat is evidence of my cheating! I have a BOYFRIEND! I'm panicking!"),
        ],
        # -- bf + voyeur --
        ("bf", "voyeur", "other", "creampie"): [
            _("Watching you finish inside her with the group... I have a BF but I can't stop looking."),
            _("The whole group is watching this creampie. I have a boyfriend. I'm glued to my screen."),
        ],
        ("bf", "voyeur", "other", "penetration"): [
            _("The group is watching this together... I have a BF but it's exciting watching with everyone."),
            _("Everyone seeing this at the same time. I have a boyfriend. The shared viewing is thrilling."),
        ],
        ("bf", "voyeur", "other", "cowgirl"): [
            _("The group watching her ride you... I have a BF but this shared viewing is intoxicating."),
            _("Everyone saw her on top at the same time. I have a boyfriend. The group experience is hot."),
        ],
        # -- bf + virgin --
        ("bf", "virgin", "self", "any"): [
            _("My first time... shared with the group... and I have a BF. Everyone just saw everything."),
            _("The group watched me lose my virginity while I have a boyfriend. I want to disappear."),
        ],
        ("bf", "virgin", "other", "any"): [
            _("Her first time in the group? I have a BF and I've never even... the group saw all of it."),
            _("She did THAT while having a BF? I have one too and I haven't even... the group just saw."),
        ],
        # -- bf + public_fetish --
        ("bf", "public_fetish", "self", "any"): [
            _("Shared with the group while I have a BF? The public scandal is making me excited~"),
            _("The whole group plus a boyfriend? Maximum risk. Maximum thrill."),
        ],
        ("bf", "public_fetish", "other", "any"): [
            _("Shared with the group while I have a BF? The daring of it all... exciting."),
            _("The group watching while I have a boyfriend... there's something risky and thrilling."),
        ],
        # -- bf + voyeur self --
        ("bf", "voyeur", "self", "any"): [
            _("Watching myself with the group... I have a BF. It's strange but exciting with an audience."),
            _("The group is watching me with you. I have a boyfriend. Seeing it with others is surreal."),
        ],
        # -- bf + exhibitionist other --
        ("bf", "exhibitionist", "other", "any"): [
            _("Another girl on display for the group? I have a BF but the exposure is exciting."),
            _("She's on show for the whole group. I have a boyfriend but I appreciate the spectacle."),
        ],
        # -- bf + public_shy other --
        ("bf", "public_shy", "other", "any"): [
            _("You're sharing this with the group while I have a BF?! What if someone screenshots?!"),
            _("The group saw that! I have a boyfriend! If he finds this chat we're ALL in trouble!"),
        ],

        # =============================================
        #  PLAYER_GF CONTEXT — player has a girlfriend
        # =============================================
        ("player_gf", "cum_slut", "self", "creampie"): [
            _("You creampied me behind {0}'s back AND showed the group? I loved every drop though~"),
            _("The group saw you fill me up while dating {0}. And I want more~"),
        ],
        ("player_gf", "cum_slut", "self", "penetration"): [
            _("The group saw us together behind {0}'s back. And honestly, I looked great~"),
            _("Everyone watched you with me while dating {0}. Not sorry. I want more."),
        ],
        ("player_gf", "cum_slut", "self", "cowgirl"): [
            _("Riding you behind {0}'s back in the group chat? I looked amazing doing it~"),
            _("The group watched me on top while you date {0}. I'm not ashamed."),
        ],
        ("player_gf", "cum_slut", "other", "creampie"): [
            _("You creampied another girl behind {0}'s back and the group saw? I want my turn!"),
            _("The group watched you fill someone else while dating {0}. Next time it's me~"),
        ],
        ("player_gf", "hate_cum", "self", "creampie"): [
            _("The group saw you finish inside me behind {0}'s back?! That's disgusting AND wrong!"),
            _("Everyone in this chat knows you creampied me while dating {0}. I feel sick!"),
        ],
        ("player_gf", "hate_cum", "self", "any"): [
            _("The group saw us together behind {0}'s back. Gross AND disrespectful to {0}."),
            _("Everyone watched that while you date {0}. I feel dirty and the group knows it."),
        ],
        ("player_gf", "camera_lover", "self", "creampie"): [
            _("Filmed a creampie behind {0}'s back AND shared with the group? The footage is hot though."),
            _("Everyone saw you finish inside me. {0} has no idea. At least the angle is perfect."),
        ],
        ("player_gf", "camera_lover", "self", "any"): [
            _("On camera behind {0}'s back, shared with the group? I look amazing at least."),
            _("The group saw your cheating footage. {0} doesn't know. My performance is stellar though."),
        ],
        ("player_gf", "camera_hater", "self", "any"): [
            _("Filmed AND shared with the group behind {0}'s back?! Cameras + cheating + group = NIGHTMARE!"),
            _("The whole group saw me on camera while you date {0}?! Delete this from the chat NOW!"),
        ],
        ("player_gf", "cheater", "self", "creampie"): [
            _("Cheating on {0} with a creampie AND the group saw? I love the danger~"),
            _("The group knows you fill me up behind {0}'s back. Bold sharing. I approve~"),
        ],
        ("player_gf", "cheater", "self", "penetration"): [
            _("The group has proof you cheat on {0} with me. Exciting~"),
            _("Everyone saw us together behind {0}'s back. What a naughty group chat."),
        ],
        ("player_gf", "cheater", "self", "cowgirl"): [
            _("Riding you behind {0}'s back in the group? Maximum scandal. Love it~"),
            _("The group watched me on top while you date {0}. Everyone's a witness to the fun."),
        ],
        ("player_gf", "cheater", "other", "creampie"): [
            _("Creampied another girl behind {0}'s back and showed the group? You collect girls~"),
            _("The group saw you cheat on {0} with a creampie. We're all accessories now~"),
        ],
        ("player_gf", "loyal", "self", "creampie"): [
            _("The group saw you finish inside me behind {0}'s back. I feel terrible. Everyone knows."),
            _("A creampie in the group while you date {0}. The guilt with witnesses is unbearable."),
        ],
        ("player_gf", "loyal", "self", "any"): [
            _("The group saw us together while you date {0}. I'm ashamed in front of everyone."),
            _("Everyone knows we did this behind {0}'s back. I'm supposed to be better than this."),
        ],
        ("player_gf", "hardcore_sex", "self", "penetration"): [
            _("The group saw you go rough on me behind {0}'s back. {0} could never do that."),
            _("Hard sex behind {0}'s back, shared with the group. Your girlfriend is missing out."),
        ],
        ("player_gf", "hardcore_sex", "self", "cowgirl"): [
            _("Hard riding behind {0}'s back in the group? Your girlfriend wishes she could do this."),
            _("The group watched me go wild on top while you date {0}. {0} is missing out."),
        ],
        ("player_gf", "hardcore_sex", "self", "creampie"): [
            _("Rough AND a creampie behind {0}'s back, shown to the group? Your GF can't compare."),
            _("The group saw you go all in on me while dating {0}. She'll never know what she's missing."),
        ],
        ("player_gf", "cute_sex", "self", "penetration"): [
            _("So gentle with me behind {0}'s back... and the group saw. Are you like this with her too?"),
            _("The group watched something so intimate. You date {0}. I feel special and guilty."),
        ],
        ("player_gf", "cute_sex", "self", "cowgirl"): [
            _("Riding you gently behind {0}'s back in the group... so intimate with witnesses."),
            _("The group saw us be tender while you date {0}. Everyone knows this was more than just sex."),
        ],
        ("player_gf", "cute_sex", "self", "creampie"): [
            _("So sweet... then a creampie... behind {0}'s back... in the GROUP. That's deeply personal."),
            _("The group saw something so intimate. You finished inside me while dating {0}. I'm conflicted."),
        ],
        ("player_gf", "voyeur", "self", "any"): [
            _("Watching our video with the group while you date {0}... strange but exciting."),
            _("The group is watching us together while {0} has no idea. The voyeur in me loves it."),
        ],
        ("player_gf", "voyeur", "other", "any"): [
            _("The group watching your cheating videos together... while {0} is clueless. I love watching."),
            _("Everyone watching this behind {0}'s back. The shared experience makes it even better."),
        ],
        ("player_gf", "camera_lover", "other", "any"): [
            _("You filmed another girl behind {0}'s back and showed the group? Film me next!"),
            _("The group saw another girl's footage while {0} is clueless. My turn on camera!"),
        ],
        ("player_gf", "camera_hater", "other", "any"): [
            _("Filming other girls behind {0}'s back and sharing with the group?! Cameras are evil!"),
            _("The group saw your footage while {0} has no idea. Cameras and cheating and groups. Gross."),
        ],
        ("player_gf", "hardcore_sex", "other", "any"): [
            _("You go rough on other girls behind {0}'s back and show the group? Be rough with ME."),
            _("The group saw you being rough while {0} is clueless. You're wasted on her."),
        ],
        ("player_gf", "cute_sex", "other", "any"): [
            _("You're sweet with other girls behind {0}'s back in the group? Are you like this with everyone?"),
            _("The group saw you be gentle with someone else while dating {0}. That stings."),
        ],
        ("player_gf", "exhibitionist", "self", "any"): [
            _("Our video shared with the group behind {0}'s back? The exposure is thrilling~"),
            _("The group seeing us while {0} is clueless? Maximum scandal. I'm into it."),
        ],
        ("player_gf", "exhibitionist", "other", "any"): [
            _("Another girl on display in the group behind {0}'s back? Bold. I'm impressed."),
            _("The group watching while {0} knows nothing? She should see what she's missing."),
        ],
        ("player_gf", "public_shy", "self", "any"): [
            _("The GROUP saw us behind {0}'s back?! If she finds this chat I'm DEAD!"),
            _("Everyone in this chat is proof you cheated on {0}! I'm panicking!"),
        ],
        ("player_gf", "public_shy", "other", "any"): [
            _("You're sharing this in the group while dating {0}?! What if she sees the chat?!"),
            _("The group has proof you cheat on {0}! If she finds this we're ALL in trouble!"),
        ],
        ("player_gf", "public_fetish", "self", "any"): [
            _("Behind {0}'s back AND shared with the group? The danger is intoxicating."),
            _("The group watching while {0} is clueless? Public, risky, perfect."),
        ],
        ("player_gf", "virgin", "self", "any"): [
            _("My first time... behind {0}'s back... shared with the GROUP. That's too much."),
            _("You shared my virginity video in the group while dating {0}?! I can't even!"),
        ],

        # =============================================
        #  DATING CONTEXT — she IS the player's GF
        # =============================================
        ("dating", "cum_slut", "other", "creampie"): [
            _("You came inside another girl and showed OUR group?! ...I'm jealous. Do me next."),
            _("The group watched you fill someone else while we're DATING. I want that load instead~"),
        ],
        ("dating", "cum_slut", "self", "creampie"): [
            _("Our creampie shared with the group? Everyone can see how much I love it~"),
            _("The group saw you fill me up. They should be jealous."),
        ],
        ("dating", "hate_cum", "other", "creampie"): [
            _("You came inside another girl and showed the GROUP?! We're DATING! That's revolting!"),
            _("The group just saw you creampie someone else while dating ME! Disgusting AND disloyal!"),
        ],
        ("dating", "hate_cum", "self", "creampie"): [
            _("Our creampie in the GROUP?! Everyone saw that disgusting mess! While we're DATING!"),
            _("The group saw you finish inside me. I hated it. And now everyone KNOWS I did it!"),
        ],
        ("dating", "camera_lover", "self", "any"): [
            _("Our video in the group? At least I look incredible, babe~"),
            _("The group watching our performance? The footage is perfect. I'm not even mad."),
        ],
        ("dating", "camera_hater", "self", "any"): [
            _("You shared our video with the GROUP?! We're DATING! I trusted you! DELETE IT!"),
            _("Our private video in the group chat?! I HATE cameras and I hate this!"),
        ],
        ("dating", "camera_hater", "other", "any"): [
            _("Filming other girls and sharing with OUR group?! We're DATING! Cameras are the worst!"),
            _("The group saw your disgusting camera hobby while we date! No more filming ANYONE!"),
        ],
        ("dating", "cum_slut", "self", "any"): [
            _("Our video in the group? The girls can see how good you are to me. I'm proud~"),
            _("Everyone watching us together? Fine. They should know what they're missing."),
        ],
        ("dating", "hate_cum", "self", "any"): [
            _("Our video in the GROUP?! While we're DATING?! Everyone saw! That's humiliating!"),
            _("The group watched us and I'm your GIRLFRIEND! This is embarrassing and gross!"),
        ],
        ("dating", "cheater", "self", "any"): [
            _("Our video in the group? Bold, babe. The girls can see you're mine... mostly~"),
            _("The group watching us? Good. But we both know I'm not JUST yours~"),
        ],
        ("dating", "cheater", "other", "any"): [
            _("Other girls in OUR group while we date? You're shameless. Just like me~"),
            _("The group watching you cheat on me? I should be mad. But I do the same thing~"),
        ],
        ("dating", "loyal", "self", "any"): [
            _("Our private moment in the GROUP?! We're DATING! That was supposed to be OURS!"),
            _("You shared us with the group?! I'm loyal to you and you do THIS?!"),
        ],
        ("dating", "loyal", "other", "any"): [
            _("Other girls in OUR group?! We're DATING! I'm LOYAL to you! This is BETRAYAL!"),
            _("The group just watched you cheat! I've been nothing but faithful! I'm heartbroken!"),
        ],
        ("dating", "hardcore_sex", "self", "any"): [
            _("The group saw how rough we get? Good. Now they know what they're missing."),
            _("Everyone watching us go at it? They should take notes. We go hard."),
        ],
        ("dating", "hardcore_sex", "other", "any"): [
            _("You go rough on other girls and show OUR group?! While we DATE?! Be rough with ME!"),
            _("The group saw you being rough with someone else while dating me?! I can take MORE!"),
        ],
        ("dating", "cute_sex", "self", "any"): [
            _("Our sweet moment shared with the group... that was supposed to be just us, babe."),
            _("The group saw how gentle you are with me... that's really personal to share..."),
        ],
        ("dating", "cute_sex", "other", "any"): [
            _("You're gentle with OTHER girls and share it with OUR group?! While we DATE?!"),
            _("The group saw you be sweet with someone else. While dating ME. That hurts..."),
        ],
        ("dating", "exhibitionist", "self", "any"): [
            _("Our video in the group? Everyone watching their eyes out? I'm excited~"),
            _("The group seeing us together? I should be embarrassed but I love the attention."),
        ],
        ("dating", "exhibitionist", "other", "any"): [
            _("Other girls on display in OUR group? ...I want to be the star, not them."),
            _("The group watching her while we date? I should be the one on display!"),
        ],
        ("dating", "public_shy", "self", "any"): [
            _("Our video in the GROUP?! Everyone saw?! We're DATING and I'm going to DIE!"),
            _("The group watched our private moment! While we're TOGETHER?! I'm panicking!"),
        ],
        ("dating", "public_shy", "other", "any"): [
            _("You shared that in OUR group while we DATE?! What if someone screenshots?!"),
            _("The group saw that! We're DATING! If anyone shares this chat I'm DONE!"),
        ],
        ("dating", "public_fetish", "self", "any"): [
            _("Our video shared with the group? The risk with an audience? Thrilling, babe."),
            _("Everyone watching us together... the danger in the group makes it exciting~"),
        ],
        ("dating", "public_fetish", "other", "any"): [
            _("Other girls shared with the group while we date? Risky. Exciting. Complicated."),
            _("The group watching while we're together? Dangerous. But I like danger."),
        ],
        ("dating", "voyeur", "self", "any"): [
            _("Watching our own video with the group... it's surreal. And kind of hot, babe."),
            _("The group watching us and I'm watching WITH them. Strangely exciting."),
        ],
        ("dating", "voyeur", "other", "any"): [
            _("The group watching another girl while we date... I shouldn't enjoy this. But I do."),
            _("Everyone seeing her while I'm your girlfriend... the shared watching is addictive."),
        ],
        ("dating", "virgin", "self", "any"): [
            _("You shared my FIRST TIME with the GROUP?! We're DATING! That was MY moment!"),
            _("My virginity video in the group chat while we're TOGETHER?! Unforgivable!"),
        ],
        ("dating", "virgin", "other", "any"): [
            _("Someone's first time shared with the group while we DATE?! That's so wrong!"),
            _("The group saw her first time. We're dating. Everything about this is terrible."),
        ],

        # =============================================
        #  BOTH CONTEXT — both player and girl have partners
        # =============================================
        ("both", "cheater", "self", "any"): [
            _("Both of us cheating, proof in the group. The girls can see what bad people we are~"),
            _("Evidence of double cheating shared with the group? This chat is a crime scene~"),
        ],
        ("both", "cum_slut", "self", "creampie"): [
            _("You filled me up while we both cheat, and the group saw. Scandalous and hot~"),
            _("A creampie while we both have partners, in the group? The girls are getting a show~"),
        ],
        ("both", "hate_cum", "self", "creampie"): [
            _("The group saw a creampie while we BOTH cheat?! Disgusting on every level! Everyone knows!"),
            _("You finished inside me, we both have partners, and the GROUP SAW?! I'm going to be sick!"),
        ],
        ("both", "camera_lover", "self", "any"): [
            _("Double cheating on camera shared with the group? The footage is scandalous and amazing."),
            _("The group saw us both cheat on film. Dangerous. But I look incredible."),
        ],
        ("both", "camera_hater", "self", "any"): [
            _("Both of us cheating ON CAMERA shared with the GROUP?! Delete everything! NOW!"),
            _("Evidence of double cheating in the group chat?! I HATE cameras! Delete this!"),
        ],
        ("both", "cute_sex", "self", "any"): [
            _("So tender while we both cheat... and the group saw. It looked so loving. We're terrible."),
            _("The group watched us be sweet while we betray our partners. Heartbreaking."),
        ],
        ("both", "hardcore_sex", "self", "any"): [
            _("Rough while we both cheat, shown to the group? Maximum scandal. Maximum hot."),
            _("The group saw us go hard while betraying our partners. Bold content."),
        ],
        ("both", "loyal", "self", "any"): [
            _("Both of us cheating, shared with the group. I'm supposed to be loyal. Everyone knows now."),
            _("The group saw us betray our partners. I'm ashamed in front of everyone."),
        ],
        ("both", "voyeur", "self", "any"): [
            _("Watching us both cheat with the group... surreal. And I can't stop rewatching."),
            _("The group is watching double cheating. And I'm watching right along with them."),
        ],
        ("both", "exhibitionist", "self", "any"): [
            _("Both cheating AND on display for the group? Maximum exposure. Maximum thrill~"),
            _("The group watching us both betray our partners? The scandal is intoxicating."),
        ],
        ("both", "public_shy", "self", "any"): [
            _("Both of us cheating AND the group SAW?! If our partners find this chat...!"),
            _("The group has proof we BOTH cheat! If anyone talks we're ALL ruined!"),
        ],
        ("both", "hate_cum", "other", "any"): [
            _("The group saw us both cheat with that video? Disgusting. Everyone is a witness."),
            _("Both have partners, watching gross videos in a group. We're all terrible people."),
        ],
        ("both", "public_fetish", "self", "any"): [
            _("Both cheating, shared with the group? The public risk with an audience is incredible."),
            _("The group watching us both betray our partners? So dangerous. So hot."),
        ],
        ("both", "virgin", "self", "any"): [
            _("My first time while we both cheat, shared with the GROUP? Too much."),
            _("The group saw my virginity taken while we both have partners. I can't even..."),
        ],
    }

    # ==========================================================
    # 30. GROUP_VIDEO_OTHER_GIRL_BF_LINES — other girl in video has a BF, in group
    # ==========================================================
    GROUP_VIDEO_OTHER_GIRL_BF_LINES = {
        # -- camera_hater --
        ("camera_hater", "cowgirl"): [
            _("She has a BF, riding you on camera, shared with the GROUP?! Delete this chat!"),
            _("On top of you on film while her BF is clueless, shown to everyone? Horrifying!"),
        ],
        ("camera_hater", "creampie"): [
            _("She has a BF, creampied on camera, AND the group saw?! You're destroying lives!"),
            _("Filmed getting filled while her BF is clueless, shared with the group? MONSTER!"),
        ],
        ("camera_hater", "bj"): [
            _("She has a BF, blowing you on camera, and the GROUP saw?! Cameras ruin everything!"),
            _("Her mouth on you on film while her BF is clueless, shared with everyone?! Disgusting!"),
        ],
        ("camera_hater", "hj"): [
            _("She has a BF, touching you on camera, shared with the GROUP?! This shouldn't exist!"),
            _("Filmed her hand on you while her BF has no idea, shown to everyone? Vile!"),
        ],
        ("camera_hater", "any"): [
            _("She has a BF, filmed, AND shared with the group?! I hate everything about cameras!"),
            _("Recording someone's girlfriend and sharing with the group? Peak awful."),
        ],
        # -- camera_lover --
        ("camera_lover", "cowgirl"): [
            _("Riding you on camera with a BF, shown to the group? The shot is amazing though."),
            _("On top of you, filmed, shared with everyone while her BF is clueless? Film me next."),
        ],
        ("camera_lover", "creampie"): [
            _("Creampie on camera with a BF, shared with the group? Dangerous footage. Hot angles."),
            _("Filmed getting filled while her BF is clueless? And the group saw? Great content."),
        ],
        ("camera_lover", "bj"): [
            _("BJ on camera with a BF, shared with the group? She knows how to perform. Nice angle."),
            _("Going down on film while her BF is clueless? The group got quality content."),
        ],
        ("camera_lover", "any"): [
            _("She has a BF, is on camera, and the group just saw? Film me next. I'll do better."),
            _("Camera-ready while cheating, shared with everyone? I'd give a better show."),
        ],
        # -- hate_cum --
        ("hate_cum", "creampie"): [
            _("She has a BF, got creampied, and the GROUP saw?! Disgusting on every level!"),
            _("Her BF is clueless, you finished inside, and everyone in this chat knows? Revolting!"),
        ],
        ("hate_cum", "cowgirl"): [
            _("She rides you with a BF? And the group watched? Everyone here is disgusted."),
            _("On top while her BF is clueless, shared with the chat? Shameless. Both of you."),
        ],
        ("hate_cum", "bj"): [
            _("Her mouth on you while she has a BF? The group just watched. That poor guy."),
            _("BJ behind her BF's back shared with the group? Everyone knows how gross this is."),
        ],
        ("hate_cum", "hj"): [
            _("Her hand on you while she has a BF? Shared with the group? Shameless."),
            _("Touching you behind her BF's back, shown to everyone? No shame at all."),
        ],
        ("hate_cum", "tj"): [
            _("Her chest on you while she has a BF? The group just saw. Her BF deserves better."),
            _("A titjob behind her BF's back shared with the group? Both disgusting."),
        ],
        ("hate_cum", "any"): [
            _("She has a BF and the group is watching? Gross. Everyone agrees, I'm sure."),
            _("Her BF is clueless and the whole group saw. Everyone here should feel bad."),
        ],
        # -- cum_slut --
        ("cum_slut", "creampie"): [
            _("She has a BF and let you fill her up? The group just saw. I want that too~"),
            _("Creampied behind her BF's back, shared with the group? Lucky girl. Next time me."),
        ],
        ("cum_slut", "cowgirl"): [
            _("Riding you while her BF is clueless, shared with the group? I'd do it better~"),
            _("On top behind her BF's back for the whole group? She's bold. Competition though."),
        ],
        ("cum_slut", "bj"): [
            _("BJ behind her BF's back, shared with the group? She knows what she likes. Same~"),
            _("Going down while cheating, shown to everyone? Good taste. I do the same."),
        ],
        ("cum_slut", "hj"): [
            _("Handjob behind her BF's back in the group? Light work. I go further."),
            _("Her hand on you while cheating, shown to everyone? That's just a warmup."),
        ],
        ("cum_slut", "tj"): [
            _("Tits on you behind her BF's back, shared with the group? Nice. I'd do it better."),
            _("Titjob while cheating, shown to everyone? Bold. I've got better ones though~"),
        ],
        ("cum_slut", "any"): [
            _("She does this with a BF? Shared with the group? Can't judge. I want the same."),
            _("Cheating on her BF, shown to everyone? The group knows we're all the same."),
        ],
        # -- cheater --
        ("cheater", "creampie"): [
            _("She's cheating AND got creampied, shared with the group? We're a whole club~"),
            _("Her BF is clueless, you filled her up, the group watched? Add me to the cheaters club."),
        ],
        ("cheater", "cowgirl"): [
            _("Riding you while cheating, shown to the group? My kind of girl. We're the same~"),
            _("On top behind her BF's back for everyone? We cheaters have good taste."),
        ],
        ("cheater", "bj"): [
            _("BJ while cheating, shared with the group? No judgement from this chat member~"),
            _("Going down behind her BF's back for the group? I do the same. Solidarity."),
        ],
        ("cheater", "hj"): [
            _("Handjob while cheating in the group? That's just a warm-up. We all start somewhere."),
            _("Her hand on you behind her BF's back for everyone? Amateur hour. But welcome~"),
        ],
        ("cheater", "tj"): [
            _("Titjob while cheating in the group chat? She's creative. I've done worse~"),
            _("Her chest on you behind her BF's back for everyone? We're all bad here."),
        ],
        ("cheater", "any"): [
            _("She cheats too? The group is basically a cheaters' support group at this point~"),
            _("Another cheater in the group? Welcome to the club. We're all terrible here."),
        ],
        # -- loyal --
        ("loyal", "creampie"): [
            _("She has a BF and got creampied? The GROUP saw?! That poor man! Everyone knows!"),
            _("Her BF is clueless, she got filled, the group witnessed? That's devastating betrayal."),
        ],
        ("loyal", "cowgirl"): [
            _("Riding you with a BF, shown to the group? That's heartless. Everyone here agrees."),
            _("On top while her BF is clueless, the whole group watching? That poor guy."),
        ],
        ("loyal", "bj"): [
            _("Her mouth on you while she has a BF? The group just witnessed a betrayal."),
            _("BJ behind her BF's back, shown to everyone? I feel terrible for him."),
        ],
        ("loyal", "hj"): [
            _("Even a handjob behind her BF's back, shared with the group? Still a betrayal."),
            _("Her hand on you while her BF trusts her, shown to everyone? That's wrong."),
        ],
        ("loyal", "tj"): [
            _("Titjob behind her BF's back, shared with the group? Her BF deserves better."),
            _("Her chest on you while cheating, shown to everyone? Loyalty means nothing to her."),
        ],
        ("loyal", "any"): [
            _("She has a BF and does this? The group witnessing it makes the betrayal worse."),
            _("Cheating on her BF with the whole group watching? Doesn't she feel any guilt?"),
        ],
        # -- hardcore_sex --
        ("hardcore_sex", "cowgirl"): [
            _("Riding you hard with a BF, shared with the group? He clearly can't satisfy her."),
            _("Going wild on top behind her BF's back for the group? He must be pathetic in bed."),
        ],
        ("hardcore_sex", "bj"): [
            _("Aggressive BJ behind her BF's back, shown to the group? She needs someone rougher."),
            _("Going hard with her mouth while cheating, shared with everyone? Her BF is boring."),
        ],
        ("hardcore_sex", "hj"): [
            _("Working you hard while her BF is clueless, shown to the group? He can't compete."),
            _("Her grip behind her BF's back for the whole group? She wants more than he gives."),
        ],
        ("hardcore_sex", "tj"): [
            _("Intense titjob behind her BF's back, shown to the group? She wants it rough."),
            _("Her chest on you aggressively while cheating, for the whole group? She's not holding back."),
        ],
        ("hardcore_sex", "creampie"): [
            _("Rough AND creampied behind her BF's back, shown to the group? She went all in."),
            _("Pounded and filled while her BF is clueless, for everyone to see? Respect."),
        ],
        ("hardcore_sex", "any"): [
            _("She goes hard behind her BF's back and the group saw? He must be too soft for her."),
            _("Cheating rough, shown to the group? Her BF can't keep up. The chat knows it."),
        ],
        # -- cute_sex --
        ("cute_sex", "cowgirl"): [
            _("Slowly riding you with a BF, shown to the group? That's heartbreakingly intimate."),
            _("Gentle on top while her BF is clueless, for the whole group? That's so personal."),
        ],
        ("cute_sex", "bj"): [
            _("Gentle BJ behind her BF's back, shown to the group? It looked so loving. Poor guy."),
            _("So tender with her mouth while cheating, shared with everyone? Bittersweet."),
        ],
        ("cute_sex", "hj"): [
            _("Soft touch behind her BF's back, shown to the group? It looked almost loving."),
            _("Her gentle hand while cheating, shared with everyone? That's intimate betrayal."),
        ],
        ("cute_sex", "tj"): [
            _("Sweet titjob while her BF is clueless, shown to the group? Poor guy. She looks so gentle."),
            _("Her chest on you tenderly while cheating, for the group? Heartbreaking."),
        ],
        ("cute_sex", "creampie"): [
            _("Gentle and then filled up behind her BF's back, shown to the group? Tragically romantic."),
            _("So sweet... then a creampie... while her BF is clueless. The group saw something very personal."),
        ],
        ("cute_sex", "any"): [
            _("She looks sweet doing this with a BF? The group witnessing it makes it sadder."),
            _("Gentle cheating shared with the group? That's the most bittersweet kind of betrayal."),
        ],
        # -- exhibitionist --
        ("exhibitionist", "cowgirl"): [
            _("Riding while cheating for the group? On display for everyone. Goals."),
            _("On top with a BF, shown to the whole chat? Maximum scandal. Impressive."),
        ],
        ("exhibitionist", "creampie"): [
            _("Creampie while cheating, shown to the group? Maximum exposure AND risk. Incredible."),
            _("Filled up behind her BF's back for everyone to see? That's the ultimate scandal."),
        ],
        ("exhibitionist", "any"): [
            _("Cheating on camera for the whole group? She loves being seen. I respect that."),
            _("On display while her BF is clueless, shared with everyone? The scandal is exquisite."),
        ],
        # -- public_shy --
        ("public_shy", "cowgirl"): [
            _("On top, filmed, cheating, in the GROUP?! If her BF finds this chat it's OVER!"),
            _("Riding on camera while cheating, shown to everyone?! She should be terrified!"),
        ],
        ("public_shy", "creampie"): [
            _("Creampie on camera, cheating, in the GROUP?! If this leaks she's DESTROYED!"),
            _("Filled on film while cheating, shared with everyone?! That's the worst evidence!"),
        ],
        ("public_shy", "any"): [
            _("She has a BF, it's on camera, and the GROUP saw?! If this leaks she's finished!"),
            _("Cheating on video shared with the group?! I'm panicking FOR her!"),
        ],
        # -- voyeur --
        ("voyeur", "cowgirl"): [
            _("Watching her ride while cheating with the group... everyone can see the forbidden thrill."),
            _("The group watching her on top while she cheats. We're all voyeurs now."),
        ],
        ("voyeur", "creampie"): [
            _("Watching a cheating creampie with the group... the shared forbidden viewing is incredible."),
            _("The group saw her get filled while cheating. We're all watching together. Intense."),
        ],
        ("voyeur", "any"): [
            _("Watching her cheat with the group... the shared taboo makes it even more exciting."),
            _("The group witnessing her cheat together. We're all part of this forbidden show."),
        ],
        # -- virgin --
        ("virgin", "any"): [
            _("She has a BF and did THIS? Shared with the group? I haven't even... the chat saw everything."),
            _("She's cheating while I haven't even done anything. And the group witnessed it all."),
        ],
        # -- _default --
        ("_default", "creampie"): [
            _("She has a BF and got creampied? The group just saw. That's another level of betrayal."),
            _("Her BF is clueless, you finished inside, and the whole group watched. Yikes."),
        ],
        ("_default", "cowgirl"): [
            _("She has a BF and rides you? The group just watched her cheat on him."),
            _("On top while her BF is clueless, for the whole group. She's not even pretending."),
        ],
        ("_default", "bj"): [
            _("She has a BF and her mouth is on you? The group just saw. Does she kiss him after?"),
            _("BJ behind her BF's back for the whole group. She doesn't seem to care."),
        ],
        ("_default", "hj"): [
            _("She has a BF and is touching you? The group just witnessed her cheating."),
            _("Her hand on you behind her BF's back, shown to everyone. Her BF would flip."),
        ],
        ("_default", "tj"): [
            _("She has a BF and uses her chest on you? The group just saw. No shame."),
            _("Titjob behind her BF's back for the whole group. Her BF probably has no idea."),
        ],
        ("_default", "penetration"): [
            _("She has a BF and sleeps with you? The group just watched her cheat."),
            _("Sex behind her BF's back, shared with the group. That's straight up betrayal."),
        ],
        ("_default", "any"): [
            _("She has a BF and does this? The group just saw. She's not who he thinks she is."),
            _("Cheating behind her BF's back, shared with the group. Everyone here is a witness."),
        ],
    }

    # ==========================================================
    # 31. GROUP_VIDEO_COMBO_LINES — 2-trait combos, in group
    # ==========================================================
    GROUP_VIDEO_COMBO_LINES = {
        (frozenset(["camera_lover", "cheater"]), "self", "any"): [
            _("Cheating on camera AND shared with the group? The whole chat is evidence. I love it."),
            _("My bad behavior filmed for the group? Maximum scandal. Maximum hot."),
        ],
        (frozenset(["camera_lover", "cheater"]), "other", "any"): [
            _("You're filming cheaters and sharing with the group? Film ME cheating next."),
            _("Another girl on camera for the group? I'd cheat more photogenically."),
        ],
        (frozenset(["camera_lover", "cum_slut"]), "self", "creampie"): [
            _("The group saw you cum inside me on camera? Great footage. I look amazing with your load~"),
            _("Creampie on film for the group? Perfect angle on the best part. I'm keeping this."),
        ],
        (frozenset(["camera_lover", "cum_slut"]), "self", "any"): [
            _("On camera AND loving it, shared with the group? I look incredible. As always~"),
            _("The group saw my best performance? Great. They should know I'm the best."),
        ],
        (frozenset(["camera_lover", "cum_slut"]), "other", "creampie"): [
            _("Creampie on camera shared with the group? That should be ME getting filled on film~"),
            _("The group saw her get your load on camera? I'm jealous of both the camera and the cum."),
        ],
        (frozenset(["camera_hater", "loyal"]), "self", "any"): [
            _("Filmed AND shared with the GROUP?! I broke my own rules and now there's proof for everyone! Delete NOW!"),
            _("On camera, shown to the group... I swore I'd never do this. I hate cameras and I hate what I've become."),
            _("The group has footage of me crossing every line I set for myself. Delete it before I lose my mind!"),
        ],
        (frozenset(["camera_hater", "loyal"]), "other", "any"): [
            _("Filmed and shared with the group? Cameras ruin everything and this feels so wrong to watch."),
            _("The group got this on film? I hate cameras, and watching this makes me question everything."),
        ],
        (frozenset(["camera_lover", "hate_cum"]), "self", "creampie"): [
            _("Great angle but disgusting act, shared with the group. The footage is good but I feel sick."),
            _("The group saw amazing cinematography of a revolting creampie. Conflicted doesn't cover it."),
        ],
        (frozenset(["camera_lover", "hate_cum"]), "other", "creampie"): [
            _("Nice footage, disgusting act, shared with the group. I'm watching for the camera work only."),
            _("The group got quality footage of something revolting. The angle is great. The act isn't."),
        ],
        (frozenset(["camera_lover", "hate_cum"]), "self", "any"): [
            _("I look amazing on film but hated what we did. And the group saw. Conflicted."),
            _("Great footage of something I regret, shared with everyone. At least I'm photogenic."),
        ],
        (frozenset(["camera_lover", "hate_cum"]), "other", "any"): [
            _("Decent footage of something gross, shared with the group. I only watch for the cinematography."),
            _("The group got footage I have mixed feelings about. Camera work: A+. Content: F."),
        ],
        (frozenset(["camera_hater", "hate_cum"]), "self", "creampie"): [
            _("Filmed, creampied, and shown to the GROUP?! I hate cameras AND that! DELETE EVERYTHING!"),
            _("The group saw the worst possible combination on camera. I want to die. Delete it NOW."),
        ],
        (frozenset(["camera_hater", "hate_cum"]), "self", "any"): [
            _("On camera doing things I hate, shown to the group? My nightmare has an audience!"),
            _("The group saw me on a camera doing something disgusting. I hate everything. Delete it."),
        ],
        (frozenset(["cum_slut", "cheater"]), "self", "creampie"): [
            _("Cheating with a creampie, shared with the group? Everyone can see I'm a naughty girl~"),
            _("The group has evidence of my cheating creampie. Dangerous. And I love it~"),
        ],
        (frozenset(["cum_slut", "cheater"]), "other", "creampie"): [
            _("She got creampied while cheating and the group saw? Save some for the rest of us~"),
            _("The group watched another cheater get filled. I want my turn in front of everyone."),
        ],
        (frozenset(["cum_slut", "cheater"]), "self", "any"): [
            _("Cheating evidence in the group? I look too good. The girls should be jealous~"),
            _("The group has proof I'm naughty. And I look amazing doing it."),
        ],
        (frozenset(["cum_slut", "cheater"]), "other", "any"): [
            _("Other cheaters in the group? As long as I get my turn too~"),
            _("The group watches everyone cheat? We're all perfect for each other."),
        ],
        (frozenset(["cum_slut", "hardcore_sex"]), "self", "creampie"): [
            _("Hard AND a creampie, shown to the group? The chat just saw my best performance~"),
            _("The group watched you go rough and fill me up. They should take notes."),
        ],
        (frozenset(["cum_slut", "hardcore_sex"]), "self", "penetration"): [
            _("The group saw you go rough on me? Good. They know I can take anything."),
            _("Hard sex shared with the group? Everyone can see I don't break easy."),
        ],
        (frozenset(["cum_slut", "hardcore_sex"]), "other", "creampie"): [
            _("Rough creampie shown to the group? I can take that harder. Film me next."),
            _("The group saw you go hard and finish inside her? Do that to me for the chat~"),
        ],
        (frozenset(["hate_cum", "loyal"]), "self", "creampie"): [
            _("The group saw you finish inside me... I swore I'd never let this happen. The shame is unbearable."),
            _("A creampie, shared with everyone... I feel disgusting and I broke every promise I made to myself."),
            _("Everyone in the group knows I let you cum inside me. I can't even look at myself."),
        ],
        (frozenset(["hate_cum", "loyal"]), "other", "creampie"): [
            _("A creampie shared with the group... that's revolting. And watching it makes me feel like I'm losing my principles too."),
            _("The group watching someone get filled like that... disgusting. And I can't pretend I didn't watch."),
        ],
        (frozenset(["hate_cum", "loyal"]), "self", "any"): [
            _("The group saw what I did... I feel sick with myself. I was supposed to be better than this."),
            _("Everyone knows now. I broke my own principles and I feel disgusting in front of all of them."),
            _("Shared with the whole group... the shame of what I've become is suffocating."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "creampie"): [
            _("The whole group can see your cum dripping out of me on film... I'm getting wet again just thinking about it."),
            _("Everyone in the chat watching me take a creampie on camera... best content I've ever made."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "penetration"): [
            _("The whole group watching me get pounded on film... this is exactly what I live for."),
            _("Every thrust on camera, shared with everyone... I'm SO into this. I look incredible."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "bj"): [
            _("The group seeing my lips wrapped around you like that... I look incredible doing it."),
            _("My blowjob on camera, shared with everyone... my lips deserve this kind of audience."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "hj"): [
            _("Even a handjob is content when the whole group is watching. I make everything look hot."),
            _("My hand on you, on film, in the group chat... I love knowing everyone can see."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "tj"): [
            _("My tits squeezing you on camera for the whole group... this is premium content. You're welcome."),
            _("The group watching my boobs on film like that... they're going to love every second."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "cowgirl"): [
            _("Me riding you on camera for the group... they get to see me in control. Perfect."),
            _("Bouncing on you on film for everyone to watch... I look better than anyone doing this."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "self", "any"): [
            _("On camera and on display for the group... this is my dream content. Show everyone."),
            _("The group watching me on film... perfect. I was born for this audience."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "creampie"): [
            _("Her creampie in the group chat is cute. Film mine next... I'd take it better for the audience."),
            _("She took your cum on camera for everyone... not bad. But I'd steal the show."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "penetration"): [
            _("The group got her sex tape... film me next. I'll give them something worth watching."),
            _("She looks okay getting fucked on camera for everyone. I'd perform way better though."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "bj"): [
            _("Her blowjob in the group chat... my technique on camera would get way more attention."),
            _("She's sucking you off for the whole group... film me instead. Upgrade."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "hj"): [
            _("A handjob shared with the group... tame. Film me and give them real content."),
            _("Her hand on you for everyone to see... my hands look better on camera. Just saying."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "tj"): [
            _("Her titjob in the group... mine would blow their minds. Film me next."),
            _("Decent boobs on camera for everyone. But mine are better. The group deserves an upgrade."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "cowgirl"): [
            _("She rides okay in the group footage. Put me on top next... I'll steal the spotlight."),
            _("Cowgirl footage of her in the chat... I ride harder and look better. Film me."),
        ],
        (frozenset(["exhibitionist", "camera_lover"]), "other", "any"): [
            _("Her footage in the group is cute. Film ME next. I'll give the chat a real show."),
            _("The group got her content... I'd put on a way better show for everyone."),
        ],
        (frozenset(["public_shy", "camera_hater"]), "self", "any"): [
            _("Filmed AND shown to the GROUP?! I'm having a panic attack! EVERYONE can see! DELETE!"),
            _("On camera in the group chat?! My worst nightmare with the worst audience! DELETE IT!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "creampie"): [
            _("A creampie FILMED and shared with the GROUP?! Cameras AND exposure?! If someone saves that she's finished!"),
            _("You filmed a creampie and sent it to everyone?! That's the worst combo! Camera + group + THAT?! Delete it!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "penetration"): [
            _("Sex on camera shared with the whole group?! Cameras are evil and everyone can see! What if it leaks?!"),
            _("Filmed her having sex and sent it to the chat?! That poor girl! Cameras AND public exposure?! Nightmare!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "cowgirl"): [
            _("Her riding you ON CAMERA for the whole group?! Every angle, every movement captured! Delete this!"),
            _("Cowgirl filmed and shared with everyone?! Her face, her body, all on camera for the group! Horrible!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "bj"): [
            _("A blowjob FILMED and sent to the group?! Her face on camera doing THAT?! What if someone screenshots?!"),
            _("You filmed her sucking you off and showed everyone?! Cameras + group exposure = her worst nightmare!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "hj"): [
            _("Filmed a handjob and shared with the chat?! Cameras make everything permanent! What if this gets out?!"),
            _("A handjob on video for the whole group... cameras capturing everything and everyone watching! Awful!"),
        ],
        (frozenset(["public_shy", "camera_hater"]), "other", "any"): [
            _("That poor girl on camera for the whole group! What if someone screenshots?! Horrible!"),
            _("Filmed and shared with everyone? I'm terrified for her. And for all of us in this chat."),
            _("On camera AND in the group chat?! That's double the exposure! Cameras and groups don't mix!"),
            _("She's on film for the whole group to see... cameras are a curse and sharing makes it worse!"),
        ],
        (frozenset(["hardcore_sex", "cheater"]), "self", "penetration"): [
            _("Rough cheating evidence in the group? Everyone can see I like it hard. Good~"),
            _("The group saw me cheat roughly? The danger and the intensity... perfect."),
        ],
        (frozenset(["hardcore_sex", "cheater"]), "other", "penetration"): [
            _("She cheats rough and the group saw? Competition. I can take it harder."),
            _("The group watched her go rough while cheating? Film me next. I won't break."),
        ],
        (frozenset(["cute_sex", "loyal"]), "self", "any"): [
            _("It looks so tender... and that makes it worse. The group can see I gave in completely."),
            _("Something so intimate shared with everyone... I wasn't supposed to feel this way. The guilt is crushing."),
            _("The gentleness makes the betrayal of my own values even more painful. And the whole group saw."),
        ],
        (frozenset(["cute_sex", "loyal"]), "other", "any"): [
            _("You're so gentle with her... the group watching this is stirring something I shouldn't feel."),
            _("Seeing you be sweet with someone else in front of everyone... it's confusing and it aches."),
        ],
        (frozenset(["voyeur", "cum_slut"]), "other", "creampie"): [
            _("Watching a creampie with the group... I love the shared viewing experience~"),
            _("The group watching this ending together? I can't look away. More please."),
        ],
        (frozenset(["voyeur", "cum_slut"]), "other", "any"): [
            _("Watching with the group? The shared experience makes it even better~"),
            _("Everyone in the chat enjoying this together. I love a group viewing session."),
        ],
        (frozenset(["voyeur", "camera_lover"]), "self", "any"): [
            _("Watching myself on camera with the group? Double voyeur experience. Love it."),
            _("The group is watching me on film AND I'm watching with them. Perfect."),
        ],
        (frozenset(["voyeur", "camera_lover"]), "other", "any"): [
            _("Great footage to watch with the group. The camera work and the audience? Chef's kiss."),
            _("Watching quality footage with the group? Best group activity ever."),
        ],
        (frozenset(["exhibitionist", "cheater"]), "self", "any"): [
            _("Cheating on display for the group? Maximum scandal AND exposure. I live for this~"),
            _("The group watching me cheat? The exhibitionist thrill AND the danger? Perfect."),
        ],
        (frozenset(["exhibitionist", "cheater"]), "other", "any"): [
            _("She cheats on display for the group? Bold. But I'd put on a better scandal~"),
            _("Another cheating exhibitionist for the group? Competition for the spotlight."),
        ],
        (frozenset(["hate_cum", "cute_sex"]), "self", "creampie"): [
            _("So gentle... then that disgusting ending... and the GROUP SAW?! It was supposed to be sweet!"),
            _("The group saw something tender turn gross. I wanted gentle. Not a creampie for an audience!"),
        ],
        (frozenset(["hate_cum", "cute_sex"]), "self", "any"): [
            _("The sweet part was nice but the group seeing everything else? I hate it."),
            _("The group saw us be gentle. The rest of what happened? Disgusting. With witnesses."),
        ],
        (frozenset(["public_fetish", "cheater"]), "self", "any"): [
            _("Cheating in the group chat? The public risk AND the naughtiness? I'm soaking~"),
            _("The group as witnesses to my cheating? The danger is intoxicating."),
        ],
        (frozenset(["public_fetish", "cheater"]), "other", "any"): [
            _("Public cheating in the group? The danger with an audience is thrilling. I want in."),
            _("The group watching forbidden content? The risk factor with witnesses is incredible."),
        ],
        (frozenset(["exhibitionist", "cum_slut"]), "self", "creampie"): [
            _("Everyone can see your cum dripping out of me and I WANT them to. Every girl in this chat should be jealous."),
            _("The whole group watching me full of your cum? This is the best thing that's ever happened to me."),
        ],
    }

    # ==========================================================
    # 32. GROUP_VIDEO_LOCATION_LINES — location follow-up, in group
    # ==========================================================
    GROUP_VIDEO_LOCATION_LINES = {
        # PUBLIC + self
        ("self", "public", "_default", "any"): [
            _("You did this with me in public AND shared with the group?! Everyone knows WHERE too!"),
            _("The group knows we did this in public?! The location AND the video?! Too much!"),
        ],
        ("self", "public", "public_fetish", "any"): [
            _("In public AND shared with the group? The double exposure is thrilling~"),
            _("The group knows we did this somewhere public? The risk just doubled. I love it."),
        ],
        ("self", "public", "public_shy", "any"): [
            _("The group knows WHERE we did this?! In PUBLIC?! If anyone goes there they'll KNOW!"),
            _("Public AND shared with everyone?! The location + the group = my worst nightmare!"),
        ],
        ("self", "public", "exhibitionist", "any"): [
            _("Public AND the group watching? Maximum exposure on every level~"),
            _("The group knows we did this in public? They should come watch next time."),
        ],
        ("self", "public", "camera_lover", "any"): [
            _("Filmed in public AND shared with the group? Great location scouting. And I look amazing."),
            _("Public filming shared with the group? The outdoor lighting was perfect. And the audience is too."),
        ],
        ("self", "public", "camera_hater", "any"): [
            _("Filmed in PUBLIC and shared with the GROUP?! The location alone is bad enough! DELETE!"),
            _("On camera in public for the group?! Everyone knows WHERE and WHAT! This is a nightmare!"),
        ],
        # PUBLIC + other
        ("other", "public", "_default", "any"): [
            _("You did this in public with another girl AND showed the group? Everyone knows the spot!"),
            _("The group knows where you do this with other girls? The location is exposed too."),
        ],
        ("other", "public", "public_fetish", "any"): [
            _("In public with another girl, shared with the group? Risky on every level. Exciting."),
            _("The group knows you do this in public? The outdoor scandal is thrilling."),
        ],
        ("other", "public", "public_shy", "any"): [
            _("In PUBLIC with another girl AND the group knows?! If someone recognizes the location!"),
            _("Public AND shared with everyone?! What if someone from the group goes there?!"),
        ],
        ("other", "public", "voyeur", "any"): [
            _("Watching a public encounter with the group... the outdoor setting makes it even better."),
            _("The group seeing this public moment together. The shared viewing is incredible."),
        ],
        # PRIVATE + self
        ("self", "private", "_default", "any"): [
            _("At least it was somewhere private... but the group seeing it defeats the purpose."),
            _("Private location but shared with the group? The privacy is gone now."),
        ],
        ("self", "private", "exhibitionist", "any"): [
            _("Private location but the group watching? I wish we'd done it somewhere public instead~"),
            _("The group is watching but the location was private? Next time, somewhere riskier."),
        ],
        ("self", "private", "public_shy", "any"): [
            _("At least the location was private... but the GROUP STILL SAW! That's bad enough!"),
            _("Private location but the whole group watched anyway?! The video cancels the privacy!"),
        ],
        ("self", "private", "camera_lover", "any"): [
            _("Private setting but shared with the group? Indoor lighting works. And the audience is good."),
            _("The location was intimate but the group saw. At least I look great in every setting."),
        ],
        ("self", "private", "camera_hater", "any"): [
            _("It was private and you STILL shared it with the group?! The whole point was privacy!"),
            _("Private location means PRIVATE! The group was NOT supposed to see this!"),
        ],
        # PRIVATE + other
        ("other", "private", "_default", "any"): [
            _("Private location with another girl but shared with the group? Not private anymore."),
            _("The group saw what you do behind closed doors with other girls. So much for privacy."),
        ],
        ("other", "private", "voyeur", "any"): [
            _("Watching a private moment with the group... the intimacy makes it even more exciting."),
            _("The group peeking into a private moment together. The taboo of shared voyeurism."),
        ],
        ("other", "private", "public_shy", "any"): [
            _("At least it was private... but the group SAW! What if someone recognizes the room?!"),
            _("Private but shared with everyone?! The location doesn't matter if the GROUP has it!"),
        ],
    }

    # ==========================================================
    # 33. GROUP_VIDEO_FULL_REACTION — location + act + trait, in group
    # ==========================================================
    GROUP_VIDEO_FULL_REACTION = {
        # PUBLIC + _default
        ("public", "cowgirl", "_default"): [
            _("{name} riding you in public shared with the group?! Everyone saw!"),
            _("The whole group watched {name} on top in public?! That's crazy!"),
            _("{name} bouncing on you outdoors for the whole group? Unreal."),
        ],
        ("public", "bj", "_default"): [
            _("{name} going down on you in public, shared with the group?!"),
            _("The group just watched {name}'s mouth on you in public! Everyone knows!"),
            _("A public BJ from {name} shown to the whole group? Bold."),
        ],
        ("public", "hj", "_default"): [
            _("{name}'s hand on you in public, shared with the group?"),
            _("The group watched {name} touch you in public. Everyone saw."),
            _("A public handjob from {name} for the whole chat? Really?"),
        ],
        ("public", "tj", "_default"): [
            _("{name}'s tits on you in public, shared with the group?!"),
            _("The whole group saw {name}'s chest on you outdoors!"),
            _("Public titjob from {name} for the whole chat? Everyone saw."),
        ],
        ("public", "creampie", "_default"): [
            _("You creampied {name} in PUBLIC and shared with the GROUP?!"),
            _("The group saw you finish inside {name} outdoors?! Everyone knows!"),
            _("A public creampie of {name} for the whole chat?! Insane!"),
        ],
        ("public", "penetration", "_default"): [
            _("Sex with {name} in public, shared with the group?! Everyone saw!"),
            _("The whole group watched you with {name} outdoors. Bold sharing."),
            _("{name} having sex with you in public for the group? Crazy."),
        ],
        ("public", "any", "_default"): [
            _("That's {name} in public and the group just saw? Everyone knows!"),
            _("The whole group watched {name} outdoors. Bold."),
            _("{name} in public shared with the group? Everyone just saw."),
        ],
        # PRIVATE + _default
        ("private", "cowgirl", "_default"): [
            _("{name} riding you in private, shared with the group? Not private now."),
            _("The group watched {name} on top. So much for the intimate setting."),
            _("{name} bouncing in private for the whole group? Shared moment."),
        ],
        ("private", "bj", "_default"): [
            _("{name} going down in private, shown to the group? Everyone saw."),
            _("The group watched {name}'s private BJ. Not so private anymore."),
            _("{name}'s mouth on you behind closed doors, shared with the chat."),
        ],
        ("private", "hj", "_default"): [
            _("{name}'s hand on you privately, shared with the group."),
            _("The group saw {name}'s private handjob. Everyone knows now."),
            _("{name} touching you behind closed doors for the whole chat."),
        ],
        ("private", "tj", "_default"): [
            _("{name}'s tits on you in private, shown to the group."),
            _("The group watched {name}'s intimate titjob. Not private anymore."),
            _("{name}'s chest on you behind closed doors, shared with everyone."),
        ],
        ("private", "creampie", "_default"): [
            _("You creampied {name} in private and showed the GROUP?!"),
            _("The group saw you finish inside {name} behind closed doors. Wow."),
            _("A private creampie of {name} shared with the whole chat."),
        ],
        ("private", "penetration", "_default"): [
            _("Sex with {name} in private, shared with the group."),
            _("The group watched a private moment between you and {name}."),
            _("{name} and you behind closed doors for the whole chat."),
        ],
        ("private", "any", "_default"): [
            _("{name} in private, shown to the group. Not private anymore."),
            _("The group saw {name}'s private moment. The intimacy is gone."),
            _("A private video of {name} shared with the whole chat."),
        ],
        # PUBLIC + traits
        ("public", "any", "cum_slut"): [
            _("{name} in public for the group? And I bet she loved every second~"),
            _("Public AND shared with the group? {name} is living her best life."),
        ],
        ("public", "any", "hate_cum"): [
            _("{name} in public AND the group saw?! That's humiliating for everyone involved!"),
            _("Public AND shared with the group? That's gross. {name} should feel worse."),
        ],
        ("public", "any", "camera_lover"): [
            _("{name} in public on camera for the group? Nice outdoor shots. But film me next."),
            _("Public footage of {name} for the group? Great lighting. I'd look better though."),
        ],
        ("public", "any", "camera_hater"): [
            _("{name} filmed in public AND shared with the group?! Cameras ruin everything!"),
            _("Public filming shared with the group?! That's two levels of wrong! Delete!"),
        ],
        ("public", "any", "cheater"): [
            _("{name} in public shared with the group? We're all bad girls here~"),
            _("Public AND in the group? The scandal is getting better with every video~"),
        ],
        ("public", "any", "loyal"): [
            _("{name} in public shared with the group? That's wrong on every level."),
            _("The group watching public footage? Loyalty and privacy mean nothing here."),
        ],
        ("public", "any", "hardcore_sex"): [
            _("{name} going hard in public, shared with the group? She can barely handle it."),
            _("Rough in public for the group? I could take it harder. In public. For everyone."),
        ],
        ("public", "any", "cute_sex"): [
            _("{name} being gentle in public, shared with the group? That's sweet and public."),
            _("Tender public moments shared with the group? That's intimate. And very exposed."),
        ],
        ("public", "any", "voyeur"): [
            _("Watching {name} in public with the group... the outdoor setting makes it better."),
            _("The group watching public footage together? I love shared viewing experiences."),
        ],
        ("public", "any", "exhibitionist"): [
            _("{name} in public for the group? Maximum exposure. I want that level of display~"),
            _("Public AND shared with everyone? The exhibitionist dream. I'm jealous."),
        ],
        ("public", "any", "public_fetish"): [
            _("{name} in public for the group? The double public exposure is thrilling~"),
            _("Public footage shared with a public group? The layers of exposure are incredible."),
        ],
        ("public", "any", "public_shy"): [
            _("{name} in PUBLIC for the GROUP?! If anyone recognizes the location...!"),
            _("Public AND shared?! If someone from the group goes there they'll KNOW!"),
        ],
        ("public", "any", "virgin"): [
            _("{name} doing that in public? And the group saw? I haven't even done that anywhere..."),
            _("Public AND for the group? She's way braver than me. I haven't even..."),
        ],
        # PRIVATE + traits
        ("private", "any", "cum_slut"): [
            _("{name} in private for the group? Intimate. But I want my own private video~"),
            _("Private footage shared with the group? {name} looks good. I'd look better."),
        ],
        ("private", "any", "hate_cum"): [
            _("{name}'s private moment shared with the group? That's gross AND invasive!"),
            _("Private footage in the group? That was supposed to be intimate. Now it's disgusting."),
        ],
        ("private", "any", "camera_lover"): [
            _("{name} in private on camera for the group? Intimate setting. Great footage. Film me next."),
            _("Private footage shared with the group? Nice angle. I'd perform better in that room."),
        ],
        ("private", "any", "camera_hater"): [
            _("{name} filmed privately and shared with the GROUP?! The whole point was PRIVACY!"),
            _("Private footage shared with everyone?! Cameras destroy intimate moments! Delete!"),
        ],
        ("private", "any", "cheater"): [
            _("{name} in private for the group? Behind closed doors doesn't matter when the group sees~"),
            _("Private footage in the group? We're all watching each other's secrets. Fun~"),
        ],
        ("private", "any", "loyal"): [
            _("{name}'s private moment shared with the group? That's a violation of trust."),
            _("The group seeing something so private? Loyalty and privacy go hand in hand. This breaks both."),
        ],
        ("private", "any", "voyeur"): [
            _("Watching {name}'s private moment with the group... the intimacy makes it better."),
            _("The group peeking into {name}'s private video? The shared voyeurism is intoxicating."),
        ],
        ("private", "any", "exhibitionist"): [
            _("{name} in private but shown to the group? She should go public next time~"),
            _("Private but the group watching? Halfway there. Full public next time."),
        ],
    }

    # ==========================================================
    # HELPER: Get group video line with fallback to original
    # ==========================================================
    # ==========================================================
    # 34. GROUP_VIDEO_GIRL_PRESENT — video girl is IN the group chat
    # The reactor addresses her directly by name.
    # Keys: vid_type → list of lines with {name} placeholder
    # ==========================================================
    GROUP_VIDEO_GIRL_PRESENT = {
        "hj": [
            _("{name}... is that YOUR hand on him?! What the hell!"),
            _("{name}?! Girl, you gave him a handjob?! I'm looking at it right now!"),
            _("Wait, {name}?! That's YOU jerking him off?! Oh my god!"),
        ],
        "bj": [
            _("{name}?! That's YOU sucking his dick?! I can't believe what I'm watching!"),
            _("{name}... girl, your mouth is on him right now in this video! What?!"),
            _("Is that you on your knees, {name}?! Going down on him?! Seriously?!"),
        ],
        "tj": [
            _("{name}?! Those are YOUR tits around his dick?! What am I watching?!"),
            _("{name}... girl, I'm looking at your chest wrapped around him right now!"),
            _("Wait, {name}?! You gave him a titjob?! I can see EVERYTHING!"),
        ],
        "cowgirl": [
            _("{name}?! You're RIDING him?! I'm literally watching you bounce on him!"),
            _("{name}... girl, is that you on top?! I can see everything from here!"),
            _("That's YOU on top of him, {name}?! Oh my god, you're really going at it!"),
        ],
        "creampie": [
            _("{name}?! He came INSIDE you?! I can literally see it!"),
            _("{name}... girl, did he just finish inside you?! I'm watching it drip out!"),
            _("Oh my god {name}, is that a creampie?! He really came inside you?!"),
        ],
        "masturbate": [
            _("{name}... is that you touching yourself?! Girl, WHAT?!"),
            _("{name}?! That's YOU?! I'm watching you do THAT right now!"),
            _("Wait, {name}?! You're pleasuring yourself in this video?! Oh my god!"),
        ],
        "sex": [
            _("{name}?! You're having SEX with him?! I'm looking at it right now!"),
            _("{name}... girl, that's you and him going at it! I can see everything!"),
            _("That's YOU with him, {name}?! A full sex tape?! Oh my god!"),
        ],
        "penetration": [
            _("{name}?! You're having SEX with him?! I'm looking at it right now!"),
            _("{name}... girl, that's you and him going at it! I can see everything!"),
            _("That's YOU with him, {name}?! A full sex tape?! Oh my god!"),
        ],
        "anal": [
            _("{name}?! He's doing THAT to you?! I can't believe I'm watching this!"),
            _("{name}... girl, is that anal?! What am I looking at right now?!"),
            _("That's YOU, {name}?! Anal?! Oh my god!"),
        ],
    }

    # Non-consensual version — reactor warns the video girl she was secretly filmed
    GROUP_VIDEO_GIRL_PRESENT_NONCONSENSUAL = {
        "hj": [
            _("{name}... girl, did you know he filmed your hand on him?! Did you agree to this?!"),
            _("{name}?! I don't think you know this exists... he recorded you giving a handjob!"),
        ],
        "bj": [
            _("{name}... did you know he filmed you sucking his dick?! This looks secret!"),
            _("{name}?! Girl, I don't think you knew he was recording! Your mouth is on him!"),
        ],
        "tj": [
            _("{name}... he filmed your tits on him and I don't think you knew! Did you agree to this?!"),
            _("{name}?! Girl, this looks like he secretly recorded your titjob!"),
        ],
        "cowgirl": [
            _("{name}... did you know he filmed you riding him?! This doesn't look consensual!"),
            _("{name}?! Girl, I think he secretly recorded you on top! Did you know about this?!"),
        ],
        "creampie": [
            _("{name}... he filmed himself cumming inside you and you don't look like you knew! Oh my god!"),
            _("{name}?! Girl, he secretly recorded the creampie! Did you know this video exists?!"),
        ],
        "masturbate": [
            _("{name}... did you know he filmed you touching yourself?! This is NOT okay!"),
            _("{name}?! Girl, he secretly recorded you masturbating! You need to know about this!"),
        ],
        "sex": [
            _("{name}... he filmed you two having sex and I don't think you knew about it!"),
            _("{name}?! Girl, this looks secretly recorded! You're having sex and you have no idea!"),
        ],
        "penetration": [
            _("{name}... he filmed you two having sex and I don't think you knew about it!"),
            _("{name}?! Girl, this looks secretly recorded! You're having sex and you have no idea!"),
        ],
        "anal": [
            _("{name}... he filmed THAT without you knowing! This is so messed up!"),
            _("{name}?! Girl, I think he secretly recorded the anal! Did you know?!"),
        ],
    }

    # Video girl is present AND has a boyfriend
    GROUP_VIDEO_GIRL_PRESENT_BF = {
        "hj": [
            _("{name}... your hand is on him and you're with %(pl)s?! Girl, what are you doing?!"),
            _("{name}?! A handjob?! What about %(pl)s?! I'm looking right at it!"),
        ],
        "bj": [
            _("{name}... you're sucking his dick while you're with %(pl)s?! Girl!"),
            _("{name}?! Your mouth is on him and you're with %(pl)s?! What is going on?!"),
        ],
        "tj": [
            _("{name}... your tits are around him while you're with %(pl)s?! Girl, explain!"),
            _("{name}?! A titjob while you're with %(pl)s?! I'm seeing this right now!"),
        ],
        "cowgirl": [
            _("{name}... you're RIDING him while you're with %(pl)s?! Girl, are you insane?!"),
            _("{name}?! You're on top of him and you're with %(pl)s?! I see everything!"),
        ],
        "creampie": [
            _("{name}... he came INSIDE you and you're with %(pl)s?! Oh my god, girl!"),
            _("{name}?! A creampie?! What about %(pl)s?! I'm watching this right now!"),
        ],
        "masturbate": [
            _("{name}... you're touching yourself for him while you're with %(pl)s?! Girl!"),
            _("{name}?! Masturbating for him?! You're with %(pl)s! What are you doing?!"),
        ],
        "sex": [
            _("{name}... you're fucking him while you're with %(pl)s?! I can see it right here!"),
            _("{name}?! A sex tape?! You're with %(pl)s, girl! What is this?!"),
        ],
        "penetration": [
            _("{name}... you're fucking him while you're with %(pl)s?! I can see it right here!"),
            _("{name}?! A sex tape?! You're with %(pl)s, girl! What is this?!"),
        ],
        "creampie_no_bf": [
            _("{name}... he came INSIDE you?! Girl! Am I really seeing this right now?! Oh my god!"),
            _("{name}?! A CREAMPIE?! He finished inside you?! I can literally see it!"),
        ],
    }

    # ==========================================================
    # 35. GROUP_VIDEO_SELF_SEXY — video girl sees her OWN video in group
    # She has camera_lover / exhibitionist / high Inbt and addresses
    # the OTHER girl in the group with flirty/sexy lines.
    # {other} = other girl's name, {player} = player name
    # Keys: (trait, vid_type)
    # ==========================================================
    GROUP_VIDEO_SELF_SEXY = {
        # ── camera_lover ──
        ("camera_lover", "hj"): [
            _("{other}, don't you think my hand looks good on him~?"),
            _("Look at that angle! I told him to film me, I look amazing~"),
            _("Not gonna lie, I look SO good doing this on camera~"),
        ],
        ("camera_lover", "bj"): [
            _("Look at me~ Don't I look pretty with his dick in my mouth?"),
            _("Girl, he filmed the whole thing! And honestly? I look incredible~"),
            _("{other}! The camera loves me, doesn't it? Even on my knees~"),
        ],
        ("camera_lover", "tj"): [
            _("{other}, don't my tits look amazing around him? The camera doesn't lie~"),
            _("He couldn't stop filming my chest. I get it though~"),
            _("Look at that! My boobs on camera always look SO good~"),
        ],
        ("camera_lover", "cowgirl"): [
            _("Look at me riding him! Don't I look hot on camera~?"),
            _("He filmed me bouncing on top! The angle is perfect~"),
            _("{other}, watching me ride him must be something, right~? I love being filmed~"),
        ],
        ("camera_lover", "creampie"): [
            _("He came inside me AND filmed it! The whole thing looks so hot~"),
            _("Wait, he recorded finishing inside me! I can't stop rewatching it~"),
            _("{other}, don't you think that creampie looks good on camera? I do~"),
        ],
        ("camera_lover", "masturbate"): [
            _("I look SO good touching myself on camera~ Don't you think?"),
            _("He wanted to film me doing this and honestly I love it~"),
            _("{other}, the lighting is perfect too! I look amazing, right~?"),
        ],
        ("camera_lover", "any"): [
            _("Honestly? I look incredible in this video~ The camera loves me!"),
            _("He filmed the whole thing and I don't even mind~"),
            _("{other}! Don't I look good? The camera always gets my best side~"),
        ],
        # ── exhibitionist ──
        ("exhibitionist", "hj"): [
            _("Knowing you can see my hand on him? That kinda turns me on~"),
            _("{other}! You're watching me jerk him off and honestly? I love that~"),
            _("The fact that you're seeing this right now makes it even hotter~"),
        ],
        ("exhibitionist", "bj"): [
            _("You're watching me suck his dick right now and I LOVE that~"),
            _("{other}! Knowing you can see me on my knees? That's the best part~"),
            _("Me going down on him AND you watching? That's so hot~"),
        ],
        ("exhibitionist", "tj"): [
            _("You're looking at my tits right now and honestly? Enjoy the view~"),
            _("My chest on display for you too? I don't mind at ALL~"),
            _("{other}, knowing you can see my boobs around him makes this even better~"),
        ],
        ("exhibitionist", "cowgirl"): [
            _("You're watching me ride him and honestly? That makes it hotter~"),
            _("{other}, knowing you can see me bouncing on top of him? I love it~"),
            _("I hope you're enjoying watching me ride him as much as I am~"),
        ],
        ("exhibitionist", "creampie"): [
            _("He came inside me and you can SEE it! Isn't that so hot~?"),
            _("{other}, you just watched him fill me up! And I loved every second~"),
            _("Knowing you watched him cum inside me? That's SO thrilling~"),
        ],
        ("exhibitionist", "masturbate"): [
            _("You're watching me touch myself and honestly? I love that you can see~"),
            _("Me pleasuring myself while you watch? That's the dream~"),
            _("{other}, knowing you can see me doing this? Makes it SO much better~"),
        ],
        ("exhibitionist", "any"): [
            _("You watching this? Good~ I like when people see me~"),
            _("Knowing you can see everything? That makes it even hotter~"),
            _("{other}, I'm glad you're seeing this! I love being watched~"),
        ],
        # ── high_inbt (high inhibition loss — she's comfortable being sexual) ──
        ("high_inbt", "hj"): [
            _("{other}, don't you think his dick fits nicely in my hand~?"),
            _("Look how hard he gets for me~ My hand does wonders~"),
        ],
        ("high_inbt", "bj"): [
            _("Girl! Don't you think his big dick fits so well in my mouth~?"),
            _("Look at me taking it all~ He tasted so good~"),
        ],
        ("high_inbt", "tj"): [
            _("His dick between my tits looks so good, right~?"),
            _("{other}, my boobs were made for this! Don't you think~?"),
        ],
        ("high_inbt", "cowgirl"): [
            _("{other}! Don't you think his big dick fits so well in my pussy~?"),
            _("I was bouncing so hard! He felt SO good inside me~"),
            _("Look at me riding him! His dick fills me up perfectly~"),
        ],
        ("high_inbt", "creampie"): [
            _("Oh my god, he filled me up SO good! Look at all that cum~"),
            _("He came SO much inside me! It felt amazing~"),
            _("{other}, I could feel it filling me up! Best feeling ever~"),
        ],
        ("high_inbt", "masturbate"): [
            _("I was SO wet when I recorded this~ Do I look good?"),
            _("I couldn't help myself! I was thinking about him the whole time~"),
        ],
        ("high_inbt", "any"): [
            _("He's SO good! You have no idea what you're missing~"),
            _("{other}, I had SO much fun! He knows exactly what he's doing~"),
        ],
        # ── hate_cum (repressed desire — she pretends to hate it but can't hide the excitement) ──
        ("hate_cum", "hj"): [
            _("{other}, I was just... touching it. That's all. It's not like I wanted to feel it throb in my hand... ugh, forget it!"),
            _("My hand was on him and I could feel him getting close... I pulled away obviously! ...Eventually."),
        ],
        ("hate_cum", "bj"): [
            _("{other}, I know what it looks like but I was NOT enjoying having him in my mouth... I just got carried away. That's it!"),
            _("His dick was in my mouth and I could feel him throbbing... I stopped before anything happened! ...I think."),
            _("Don't judge me, {other}! I didn't LIKE sucking him off... my body was just... reacting on its own!"),
        ],
        ("hate_cum", "tj"): [
            _("My tits around him... it was just a titjob, {other}! It's not like I wanted him to finish between them... much."),
            _("{other}, I could feel how hard he was between my boobs... that doesn't mean I WANTED it! My body just reacted!"),
        ],
        ("hate_cum", "cowgirl"): [
            _("{other}... I was riding him and I could feel EVERYTHING... every inch... I didn't want him to cum inside, obviously! But the way he fit..."),
            _("I was on top and he was so deep... {other}, I almost lost control. ALMOST. I would never actually let him finish inside me. ...Probably."),
            _("Being on top with nothing between us... so raw and so... NO. I'm not into that. Stop looking at me like that, {other}!"),
        ],
        ("hate_cum", "penetration"): [
            _("{other}... we were having sex and I could feel him throbbing inside me... I'm glad he pulled out. I think. My body disagrees."),
            _("He was inside me and it felt so... I mean it was FINE. Just sex. Normal sex. I definitely wasn't begging for more in my head."),
        ],
        ("hate_cum", "creampie"): [
            _("{other}... he came inside me. Every. Single. Drop. And I... I felt it all... filling me up... that's so disgusting... why can't I stop watching this?!"),
            _("He finished inside me and I could feel his cum flooding my pussy... that's SO gross, {other}... so warm and... NO. I hated it. I HATED it!"),
            _("{other}, look at all that cum dripping out of me... that's revolting... my pussy was SO full... I'm rewatching this to be angry, not because it's... ugh!"),
        ],
        ("hate_cum", "any"): [
            _("{other}... it was fine. Just... normal stuff. Nothing I enjoyed too much. Stop smiling at me!"),
            _("Don't read into it, {other}. I did what I did and I'm NOT thinking about doing it again. ...Much."),
        ],
    }

    # ==========================================================
    # 36. GROUP_VIDEO_REACTOR_CAMERA — stat-tiered reactor lines
    # When the REACTOR (not the video girl) has camera_lover/exhibitionist.
    # Split by stat level: low (barely know each other) vs high (close).
    # {name} = video girl name, {player} = player name
    # ==========================================================
    GROUP_VIDEO_REACTOR_CAMERA = {
        # ── camera_lover, low stats (Love < 30, Inbt < 20) ──
        ("camera_lover", "low"): [
            _("Ok, [Player.Name] knows how to work a camera... but you shouldn't share this with me! We barely know each other!"),
            _("The filming is actually good... but this is way too personal! I don't know you like that, {name}!"),
            _("Gotta admit, the camera work is nice... but I'm not comfortable seeing this! We're not that close!"),
            _("That's a well-shot video, I'll give him that... but please don't include me in this! We barely talk!"),
        ],
        # ── camera_lover, mid stats (Love 30-60 or Inbt 20-40) ──
        ("camera_lover", "mid"): [
            _("Ok the angles are really good... [Player.Name] knows what he's doing with a camera~"),
            _("Not gonna lie, the filming quality? Chef's kiss. He should film more often~"),
            _("That's actually well filmed... I appreciate a good camera angle, {name}~"),
            _("The way he filmed that... ok, I'm impressed. He has talent~"),
        ],
        # ── camera_lover, high stats (Love > 60 or Inbt > 40) ──
        ("camera_lover", "high"): [
            _("Ok but seriously, [Player.Name] should film ME next~ I'd look even better~"),
            _("Film me next, [Player.Name]~ I promise I'll give a better performance than {name}~"),
            _("The camera work is amazing but imagine what he could do filming ME~ Just saying~"),
            _("{name} looks good but... he hasn't seen what I can do on camera yet~"),
        ],
        # ── exhibitionist, low stats ──
        ("exhibitionist", "low"): [
            _("That's... bold. Sharing something like this. But I don't know you well enough for this!"),
            _("Being that exposed... it's something. But we're not close enough for me to be seeing this!"),
            _("I get the thrill but... we barely know each other! This is too much!"),
            _("There's something about being on display like that... but not with people I barely know!"),
        ],
        # ── exhibitionist, mid stats ──
        ("exhibitionist", "mid"): [
            _("There's something thrilling about being seen like that... I kinda get it, {name}~"),
            _("The exposure... it's exciting, isn't it? I might understand more than you think~"),
            _("Being that bold on camera... I respect it. There's a thrill in being watched~"),
            _("I won't lie, something about this being out there is... exciting~"),
        ],
        # ── exhibitionist, high stats ──
        ("exhibitionist", "high"): [
            _("Honestly {name}? Seeing this makes me want to be filmed too~ The thrill of being watched..."),
            _("I want that. Being seen like that, being on display... [Player.Name], I'm next~"),
            _("{name}, you look amazing being so exposed~ I want people to see ME like that too~"),
            _("The way everyone can see you... that's SO hot. I need that feeling~"),
        ],
    }

    # Video girl is present — trait-colored follow-ups from the reactor
    GROUP_VIDEO_GIRL_PRESENT_TRAIT = {
        ("camera_lover", "self_vid"): [
            _("Honestly {name}, the angles are great though. He should film ME next."),
            _("{name}, you look good on camera, I'll give you that. I'd look better though."),
        ],
        ("camera_hater", "self_vid"): [
            _("{name}, he FILMED you?! Cameras are the worst! Make him delete this!"),
            _("This is awful, {name}. Being on camera like this... I'm so sorry."),
        ],
        ("cum_slut", "creampie"): [
            _("Not gonna lie {name}... that creampie looked hot. I'm jealous~"),
            _("{name}, he filled you up like that? I want my turn honestly~"),
        ],
        ("cum_slut", "any"): [
            _("Okay {name}... I'm not even mad. That looked really good~"),
            _("{name}, I have to admit, that's hot. But I do it better."),
        ],
        ("hate_cum", "creampie"): [
            _("{name}... he came inside you?! Why would you let him fill up your pussy like that... so deep... all that cum... OMG, forget it. GROSS!"),
            _("Oh god {name}... all that cum flooding inside your poor little pussy... that's so disgusting... did you feel it? I mean... ugh, never mind!"),
            _("{name}, I can't believe you let him finish inside... look at all of it dripping out... that's revolting. I can't stop looking but it's REVOLTING."),
        ],
        ("hate_cum", "cowgirl"): [
            _("{name}! You're riding him raw?! If you keep going like that he's going to lose it inside you... all that cum rushing in... that's SO reckless, girl!"),
            _("No protection, {name}?! On top like that?! You're in control so STOP before he... fills you... with... ugh. Just be careful!"),
        ],
        ("hate_cum", "penetration"): [
            _("{name}... raw?! What if he can't pull out in time? Your poor pussy would be overflowing with his... ugh, that's so dangerous! ...Did he pull out?"),
            _("No condom, {name}?! You're letting him go raw inside you... if he finishes like that... I can't even think about it. That's so irresponsible!"),
        ],
        ("hate_cum", "bj"): [
            _("{name}... your mouth is on... ugh, that's nasty. What if he finishes? ...Did he? Not that I care."),
            _("Your mouth, {name}?! That's disgusting. I hope you pulled away before the gross part... ...did you?"),
        ],
        ("hate_cum", "hj"): [
            _("{name}, at least aim it away from yourself... the mess is the worst part. Not that I'm thinking about the mess."),
            _("A handjob, {name}? Fine, I guess. Just... don't let it get on you. That's the gross part."),
        ],
        ("hate_cum", "any"): [
            _("{name}, that's... ugh. I don't want to see this. ...But I can't stop watching either."),
            _("I didn't need to see that, {name}. That's gross. ...Why am I still looking?"),
        ],
        ("cheater", "any"): [
            _("Naughty, {name}~ I love the drama honestly~"),
            _("{name}, you're bad. I like that about you though. Keep going~"),
        ],
        ("loyal", "any"): [
            _("{name}... how could you do this? I thought you were better than this."),
            _("I'm disappointed, {name}. Loyalty means everything and this is wrong."),
        ],
        ("exhibitionist", "any"): [
            _("{name}, honestly? You look good. I'd want people to see me too~"),
            _("Not bad, {name}. The exposure is kind of thrilling, isn't it?"),
        ],
        ("voyeur", "any"): [
            _("I can't stop watching this, {name}... it's intense."),
            _("{name}... I know I shouldn't be this into it. But I am."),
        ],
        ("public_shy", "any"): [
            _("{name}... what if this gets out?! I'm panicking for you!"),
            _("This is terrifying, {name}! What if someone else finds this?!"),
        ],
        ("public_fetish", "any"): [
            _("The fact that this exists is kind of thrilling, {name}~"),
            _("{name}, knowing people could see this... it's exciting honestly."),
        ],
        ("hardcore_sex", "penetration"): [
            _("{name}, he should go harder on you. I can tell you can take more."),
            _("That looked tame, {name}. He's rougher with me. Just saying."),
        ],
        ("cute_sex", "any"): [
            _("{name}... that looked really intimate. I feel bad seeing this."),
            _("That was so personal, {name}... I feel like I shouldn't be watching."),
        ],
        ("virgin", "any"): [
            _("{name}... you've done THAT? I haven't even... wow."),
            _("I can't believe you did that, {name}. I haven't even started..."),
        ],
    }

    def _cheater_applies(girl):
        """'cheater' trait only matters for line selection when the girl has a boyfriend."""
        return girl.has_trait("cheater") and hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

    def _loyal_applies(girl):
        """'loyal' trait only matters for line selection when the girl has a boyfriend."""
        return girl.has_trait("loyal") and hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

    def _get_reactor_camera_tier(girl):
        """Return 'low', 'mid', or 'high' based on girl's relationship stats."""
        love = getattr(girl, "Love", 0)
        inbt = getattr(girl, "Inbt", 0)
        lust = getattr(girl, "Lust", 0)
        if love > 60 or inbt > 40 or lust > 50:
            return "high"
        elif love >= 30 or inbt >= 20 or lust >= 25:
            return "mid"
        return "low"

    def _pick_group_video_girl_present(girl, vid, group):
        """When the video girl is a member of this group, pick a direct-address reaction.
        Handles both subject='other' (reactor sees video girl) and subject='self'
        (video girl sees her own video — sexy lines if she has traits/high stats).
        Returns (main_line, followup_line, followup_girl) or (None, None, None).
        followup_girl is the Girl who should SAY the followup (may differ from girl)."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        vid_gid = vid.get("girl_gid", "")
        group_gids = group.get("members", [])
        vid_type = vid.get("type", "hj")

        # ── subject="self": video girl reacts to her own video in the group ──
        if subject == "self":
            # Only trigger sexy self-reaction if she has the right traits/stats
            if not hasattr(girl, "has_trait"):
                return None, None, None
            # Find the other girl in the group to address
            other_gids = [gid for gid in group_gids if gid != girl.gid]
            if not other_gids:
                return None, None, None
            other_girl = GIRL_BY_ID.get(other_gids[0])
            if not other_girl or not hasattr(other_girl, "Name"):
                return None, None, None
            other_name = other_girl.Name

            # Determine which trait key to use
            sexy_trait = None
            if girl.has_trait("hate_cum"):
                sexy_trait = "hate_cum"
            elif girl.has_trait("camera_lover"):
                sexy_trait = "camera_lover"
            elif girl.has_trait("exhibitionist"):
                sexy_trait = "exhibitionist"
            else:
                # High Inbt (>= 300) or high Lust (>= 90) = she's comfortable being sexual openly
                inbt = getattr(girl, "Inbt", 0)
                lust = getattr(girl, "Lust", 0)
                if inbt >= 300 or lust >= 90:
                    sexy_trait = "high_inbt"

            if not sexy_trait:
                return None, None, None

            # Discover the trait that drove the reaction
            if sexy_trait not in ("high_inbt",):
                _group_video_discover(girl, sexy_trait)

            # Pick sexy self-reaction line
            tg = _video_type_group(vid_type)
            main_line = None
            for tkey in [vid_type, tg, "any"]:
                key = (sexy_trait, tkey)
                if key in GROUP_VIDEO_SELF_SEXY:
                    main_line = _tl(_group_unique_choice(GROUP_VIDEO_SELF_SEXY[key])).replace(
                        "{other}", other_name).replace("{player}", Player.Name if hasattr(Player, "Name") else "him"
                    )
                    break

            # No follow-up here — the reactor's camera-trait response will fire
            # during HER own group_video_reaction call (subject="other").
            # Adding a follow-up here would be captured as the VIDEO girl's message
            # by the phone messaging queue system.
            return main_line, None, None

        # ── subject="other": reactor sees video girl in the group ──
        if vid_gid not in group_gids:
            return None, None, None

        vid_girl = GIRL_BY_ID.get(vid_gid)
        if not vid_girl or not hasattr(vid_girl, "Name"):
            return None, None, None

        name = vid_girl.Name
        consensual = vid.get("consensual", True)
        other_has_bf = _vid_bf_still_relevant(vid)

        # ── Main line ──
        main_line = None

        # Non-consensual: warn the video girl
        if not consensual:
            pool = GROUP_VIDEO_GIRL_PRESENT_NONCONSENSUAL.get(vid_type)
            if not pool:
                pool = GROUP_VIDEO_GIRL_PRESENT_NONCONSENSUAL.get("sex", [_("{name}... did you know he filmed that?! He sent it to me!")])
            main_line = _tl(_group_unique_choice(pool)).replace("{name}", name)
        # Video girl has BF: call it out
        elif other_has_bf:
            pool = GROUP_VIDEO_GIRL_PRESENT_BF.get(vid_type)
            if not pool:
                pool = GROUP_VIDEO_GIRL_PRESENT_BF.get("sex", [_("{name}... you're with %(pl)s and he just showed me this?!")])
            # translate FIRST, then the name: a line with the name already in it has no pair
            main_line = _format_partner_line(vid_girl, _group_unique_choice(pool)).replace("{name}", name)
        # Normal case
        else:
            # Creampie special
            if vid_type == "creampie":
                pool = GROUP_VIDEO_GIRL_PRESENT_BF.get("creampie_no_bf")
                if pool:
                    main_line = _tl(_group_unique_choice(pool)).replace("{name}", name)
            if not main_line:
                pool = GROUP_VIDEO_GIRL_PRESENT.get(vid_type)
                if not pool:
                    pool = GROUP_VIDEO_GIRL_PRESENT.get("sex", [_("{name}?! He just sent this to both of us!")])
                main_line = _tl(_group_unique_choice(pool)).replace("{name}", name)

        # ── Trait follow-up (reactor's trait-colored response) ──
        followup = None
        if hasattr(girl, "has_trait"):
            tg = _video_type_group(vid_type)

            # Check camera_lover / exhibitionist FIRST with stat tiers
            for cam_trait in ["camera_lover", "exhibitionist"]:
                if not girl.has_trait(cam_trait):
                    continue
                tier = _get_reactor_camera_tier(girl)
                key = (cam_trait, tier)
                if key in GROUP_VIDEO_REACTOR_CAMERA:
                    _group_video_discover(girl, cam_trait)
                    followup = _tl(_group_unique_choice(GROUP_VIDEO_REACTOR_CAMERA[key])).replace(
                        "{name}", name).replace("{player}", Player.Name if hasattr(Player, "Name") else "him"
                    )
                    break

            # If no camera/exhib follow-up, fall back to normal trait order
            if not followup:
                trait_order = [
                    "camera_hater", "cum_slut", "hate_cum",
                    "cheater", "loyal", "voyeur",
                    "public_shy", "public_fetish", "hardcore_sex", "cute_sex", "virgin",
                    "lesbian",
                ]
                _vid_condom = vid.get("condom", False)
                for trait in trait_order:
                    if not girl.has_trait(trait) or trait_is_discovering(girl, trait):   # no veteran voice while she discovers it
                        continue
                    if trait == "cheater" and not _cheater_applies(girl):
                        continue
                    if trait == "loyal" and not _loyal_applies(girl):
                        continue
                    if trait == "hate_cum" and _vid_condom:
                        continue
                    for tkey in [vid_type, tg, "any"]:
                        key = (trait, tkey)
                        if key in GROUP_VIDEO_GIRL_PRESENT_TRAIT:
                            _group_video_discover(girl, trait)
                            followup = _tl(_group_unique_choice(GROUP_VIDEO_GIRL_PRESENT_TRAIT[key])).replace("{name}", name)
                            break
                    # camera_hater: use self_vid key
                    if not followup and trait == "camera_hater":
                        key = (trait, "self_vid")
                        if key in GROUP_VIDEO_GIRL_PRESENT_TRAIT:
                            _group_video_discover(girl, trait)
                            followup = _tl(_group_unique_choice(GROUP_VIDEO_GIRL_PRESENT_TRAIT[key])).replace("{name}", name)
                    if followup:
                        break

        return main_line, followup, girl

    def _get_group_video_line(group_dict, original_dict, key):
        """Try group-specific dict first, fall back to original."""
        lines = group_dict.get(key)
        if lines:
            return _group_unique_choice(lines)
        lines = original_dict.get(key)
        if lines:
            return _group_unique_choice(lines)
        return None
    # ==========================================================
    GROUP_VIDEO_DATING_TYPE_LINES = {
        ("other", "hj"): [
            _("A handjob from another girl, shared with the group, while we're DATING?!"),
            _("The whole group just saw another girl's hand on my boyfriend!"),
            _("Everyone in this chat watched some girl jerk off MY boyfriend!"),
            _("A handjob video in the GROUP?! While you're with ME?!"),
        ],
        ("other", "bj"): [
            _("Another girl sucking off my boyfriend, shared with the ENTIRE GROUP?!"),
            _("The group just watched some girl go down on YOU?! While we're TOGETHER?!"),
            _("A blowjob from another girl in the group chat?! Everyone just saw!"),
            _("The whole group knows another girl uses her mouth on my boyfriend!"),
        ],
        ("other", "penetration"): [
            _("You're sleeping with someone else AND sharing with the group?! While we DATE?!"),
            _("A sex tape with another girl, in the GROUP?! My boyfriend, everyone!"),
            _("The group just watched you have sex with someone else! We're DATING!"),
            _("Everyone in this chat just saw my boyfriend cheat with a sex tape!"),
        ],
        ("other", "cowgirl"): [
            _("Another girl riding my boyfriend, shared with the GROUP?!"),
            _("The whole chat watched some girl on top of YOU?! We're DATING!"),
            _("A cowgirl video with another girl in the group?! Everyone saw!"),
            _("She's riding MY boyfriend in the group chat?! Unbelievable!"),
        ],
        ("other", "creampie"): [
            _("You finished inside another girl AND shared with the GROUP?! While dating ME?!"),
            _("The whole chat saw you creampie someone else?! I'm your GIRLFRIEND!"),
            _("A creampie for another girl in the group?! EVERYONE just watched!"),
            _("You came inside her AND the group saw?! While we're TOGETHER?!"),
        ],
        ("other", "tj"): [
            _("Another girl's tits on my boyfriend, shared with the GROUP?!"),
            _("The whole chat saw a titjob from someone else while you date ME?!"),
            _("A titjob video with another girl in the group?! Everyone knows!"),
        ],
        ("self", "hj"): [
            _("You shared our handjob video with the GROUP?! That was private!"),
            _("The whole group watched me give my boyfriend a handjob. Great."),
            _("Our handjob video in the group chat?! Everyone just saw my hand on you!"),
        ],
        ("self", "bj"): [
            _("You shared me going down on you with the GROUP?! That was OUR moment!"),
            _("The whole chat watched me blow my boyfriend. I'm mortified."),
            _("My mouth on my boyfriend... in the group chat for everyone to see!"),
        ],
        ("self", "penetration"): [
            _("Our sex tape in the GROUP?! Everyone just watched us!"),
            _("The whole group saw me have sex with my boyfriend. Was that necessary?!"),
            _("A video of us having sex, shared with the group. I'm dying."),
        ],
        ("self", "cowgirl"): [
            _("Me riding my boyfriend, shared with the GROUP?! That was intimate!"),
            _("The whole chat just watched me on top of my boyfriend. I'm dying!"),
            _("A cowgirl video with my boyfriend in the group?! Everyone saw me bounce!"),
        ],
        ("self", "creampie"): [
            _("My boyfriend finishing inside me, shared with the GROUP?! Oh my GOD!"),
            _("The whole chat saw a creampie of me and my boyfriend. I'm traumatized."),
            _("Everyone in this group just watched my boyfriend cum inside me!"),
        ],
        ("self", "tj"): [
            _("My tits around my boyfriend, shared with the GROUP?! That was PRIVATE!"),
            _("The whole group just saw my titjob. My boyfriend has no shame."),
            _("A titjob video with my boyfriend in the group chat?! Everyone saw my chest!"),
        ],
    }

    # ==========================================================
    # CHEATING EXPOSURE ESCALATION — Severity Tiers & Constants
    # When a video of a girl with a partner is shared in a group,
    # consequences scale with act severity. Tier 1 = harmless solo,
    # Tier 4 = undeniable intercourse proof.
    # ==========================================================

    _GROUP_VIDEO_SEVERITY_TIER = {
        "masturbate": 1,
        "hj": 2,
        "tj": 2,
        "bj": 3,
        "cowgirl": 3,
        "reverse_cowgirl": 3,
        "reverse_cowgirl_anal": 4,
        "penetration": 4,
        "creampie": 4,
        "anal": 4,
        "doggy": 4,
    }

    # Per-tier stat penalties when girl has a BF/GF.
    # "self" = her video shared, "other" = she watches another girl's video.
    _GROUP_BF_CHEATING_PENALTIES = {
        "self": {
            1: {"Love": -3,  "Obed": 2,  "Inbt": 3,  "bf_loyalty": -15,  "provoke": 1},
            2: {"Love": -8,  "Obed": 4,  "Inbt": 5,  "bf_loyalty": -40,  "provoke": 2},
            3: {"Love": -12, "Obed": 6,  "Inbt": 8,  "bf_loyalty": -80,  "provoke": 3},
            4: {"Love": -20, "Obed": 10, "Inbt": 12, "bf_loyalty": -150, "provoke": 4},
        },
        "other": {
            1: {"Love": -1, "Obed": 1, "Inbt": 1, "bf_loyalty": -5,  "provoke": 1},
            2: {"Love": -3, "Obed": 2, "Inbt": 2, "bf_loyalty": -10, "provoke": 1},
            3: {"Love": -5, "Obed": 3, "Inbt": 3, "bf_loyalty": -20, "provoke": 2},
            4: {"Love": -7, "Obed": 4, "Inbt": 5, "bf_loyalty": -30, "provoke": 2},
        },
    }

    # Blackmail leverage gained from group video exposure.
    # Only for girls with NPC partners (BF/GF).
    _GROUP_SHARE_LEVERAGE = {
        1: 0,
        2: 1,
        3: 1,
        4: 2,
    }

    # Panic/cheater lines when girl with BF/GF sees HER OWN video in group.
    # Uses %(pl)s, %(pp)s, %(po)s, %(poss)s, %(Pp)s — resolved by _format_partner_line.
    GROUP_VIDEO_CHEATING_SELF_PANIC = {
        "masturbate": {
            "panic": [
                _("At least it's just me alone... but if %(pl)s ever finds this chat..."),
                _("A solo video isn't proof of cheating... but the group knowing I do this is humiliating..."),
            ],
            "cheater": [
                _("The group has my private video. %(Pp)s would flip if %(pp)s saw this chat~"),
                _("Nothing wrong with touching myself... but the group having it gives you leverage~"),
            ],
        },
        "hj": {
            "panic": [
                _("My hand on you... in front of everyone... if %(pl)s ever sees this chat I'm done..."),
                _("The group has proof I touched you. %(pl)s can NEVER find this conversation..."),
                _("Everyone just saw me cheat with my hands. If %(pl)s finds out through one of them..."),
            ],
            "cheater": [
                _("A handjob in the group chat while I'm with %(pl)s? The scandal is delicious~"),
                _("The group knows my hand was on you. %(pl)s has no idea. I love the danger~"),
            ],
        },
        "tj": {
            "panic": [
                _("My chest around you, shared with the group... if %(pl)s sees this chat..."),
                _("Everyone has proof my tits were on you. %(pl)s would leave me instantly..."),
                _("A titjob in the group chat... the more people who know, the higher the risk %(pl)s finds out..."),
            ],
            "cheater": [
                _("My tits wrapped around you, seen by everyone... and %(pl)s is clueless~ Love it."),
                _("The group has a titjob video of me. %(pl)s doesn't know a thing~"),
            ],
        },
        "bj": {
            "panic": [
                _("My mouth on you, in the GROUP... if %(pl)s ever finds out through any of these girls..."),
                _("The group has proof I went down on you behind %(poss)s back. Every girl here is a potential witness..."),
                _("A blowjob in the group chat... that's undeniable proof. If %(pl)s asks any of them..."),
            ],
            "cheater": [
                _("Everyone saw my mouth on you while I'm with %(pl)s. The risk is intoxicating~"),
                _("A blowjob behind %(poss)s back, shared with the group... I'm a terrible person and I love it~"),
            ],
        },
        "cowgirl": {
            "panic": [
                _("Me riding you, in the GROUP CHAT... everyone has proof I cheated on %(pl)s..."),
                _("The group watched me on top of you. Every single one of them could tell %(pl)s..."),
                _("I was riding another person and the whole group SAW. %(pl)s can never know about this chat..."),
            ],
            "cheater": [
                _("Me riding you behind %(poss)s back, shared with everyone? Best group chat ever~"),
                _("The group watched me cheat on %(pl)s from the best angle. No regrets~"),
            ],
        },
        "penetration": {
            "panic": [
                _("A sex tape of me cheating, in the GROUP... my life with %(pl)s is over if this leaks..."),
                _("Everyone has PROOF I slept with you behind %(poss)s back. I'm going to be sick..."),
                _("Full sex, in the group chat... undeniable. If even ONE of these girls tells %(pl)s..."),
                _("The group has a video of me being unfaithful. Every girl here can destroy my relationship..."),
            ],
            "cheater": [
                _("A sex tape cheating on %(pl)s, shared with the whole group? Maximum scandal~"),
                _("Everyone knows I'm sleeping with you behind %(poss)s back. And I couldn't care less~"),
            ],
        },
        "creampie": {
            "panic": [
                _("You finished inside me AND shared it with the GROUP?! If %(pl)s sees this... it's not just cheating, it's..."),
                _("A creampie of me cheating, in the group chat... the most damning proof possible. %(pl)s can NEVER see this..."),
                _("Everyone has proof you came inside me behind %(poss)s back. My relationship is hanging by a thread..."),
                _("The group watched you fill me up while I'm with %(pl)s... if this leaks I lose EVERYTHING..."),
            ],
            "cheater": [
                _("A creampie behind %(poss)s back, in the group chat? Maximum betrayal. I'm getting wet again~"),
                _("You came inside me and showed the group. %(pl)s is the only one who doesn't know. Delicious~"),
            ],
        },
        "anal": {
            "panic": [
                _("Anal, in the GROUP... if %(pl)s finds out I did THAT behind %(poss)s back..."),
                _("The group has proof I took it in the ass while with %(pl)s. My life is over if this leaks..."),
                _("Everyone saw me do the most extreme thing possible behind %(poss)s back... I'm shaking..."),
            ],
            "cheater": [
                _("Anal behind %(poss)s back AND the group saw? %(pl)s would never try that with me~"),
                _("The group knows I take it in the ass for you, not for %(pl)s. Scandalous~"),
            ],
        },
    }

    # ==========================================================
    # Cheating panic when partner IS in the group watching
    # ==========================================================
    # Same moment, but her partner has NTR active + boundary discovered: he knows, nothing is exposed.
    # Keyed by _ntr_video_ctx(npc) so "you asked" is only said to a partner who asks for videos.
    GROUP_VIDEO_NTR_KNOWN_BF_WATCHING = {
        "requested": {
            "panic": [
                _("Well, %(pn)s, you asked to see it. There it is."),
                _("%(pn)s wanted videos, so... enjoy, I guess. This is so embarrassing."),
            ],
            "cheater": [
                _("There's your video, %(pn)s~ Watch it as many times as you like."),
            ],
        },
        "known": {
            "panic": [
                _("Well, %(pn)s, now you've seen it. This is so embarrassing."),
            ],
            "cheater": [
                _("%(pn)s, I hope you're paying attention. This is the good part~"),
            ],
        },
        "hostile": {
            "panic": [
                _("%(pn)s... you don't have to watch this. But I know you will."),
            ],
            "cheater": [
                _("Go on, %(pn)s. Watch it. You always do~"),
            ],
        },
    }
    # Stats when her own video is watched by her NTR-known partner in the group (replaces the exposure penalties)
    _GROUP_BF_NTR_KNOWN_STATS = {"Inbt": 3, "Lust": 2}

    GROUP_VIDEO_CHEATING_BF_WATCHING = {
        "panic": [
            _("[Player.Name]! Are you forgetting something? %(pl)s IS IN THIS GROUP! Fuck..."),
            _("%(pl)s is in this chat. %(Pp)s watched the whole thing. I am done."),
            _("There is nothing I can say. %(pl)s watched it with everyone else."),
        ],
        "cheater": [
            _("%(pl)s just saw everything in real time. Right here in the group~ How thrilling."),
            _("%(pl)s, I know you are reading this right now. Enjoy the show?~"),
        ],
    }

    # ==========================================================
    # GROUP VIDEO STATS — enhanced stat application for group context
    # ==========================================================
    def _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid):
        """Apply stat changes for group video reactions.
        Group context amplifies reactions:
        - More Inbt (exposure to multiple girls)
        - Love loss when she dislikes sharing (especially 'other' + group)
        - Lust gain for positive/horny reactions
        - Obed changes based on compliance
        """
        # Track video sent for corruption (same as solo)
        girl.CorruptionVideosSentCount = getattr(girl, "CorruptionVideosSentCount", 0) + 1
        _vts = getattr(girl, "CorruptionVideoTypesSent", None)
        if _vts is None:
            _vts = set()
        _vts.add(vid_type)
        girl.CorruptionVideoTypesSent = _vts
        girl.check_corruption("camera")

        is_dating = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        is_cheater = hasattr(girl, "has_trait") and girl.has_trait("cheater")
        _group_size = len(group.get("members", []))

        # ── Non-consensual self: heavy penalties ──
        if subject == "self" and not consensual:
            Change_Status(girl, "Inbt", 6)
            Change_Status(girl, "Love", -10)
            Change_Status(girl, "Obed", 2)
            return

        # ── Base by subject ──
        if subject == "self":
            if consensual:
                Change_Status(girl, "Inbt", 5)       # more than solo (3)
                Change_Status(girl, "Lust", 2)
                Change_Status(girl, "Love", -2)       # mild discomfort, group exposure
            else:
                Change_Status(girl, "Inbt", 6)
                Change_Status(girl, "Love", -10)
        else:
            # Other girl's video sent to group — jealousy amplified
            Change_Status(girl, "Inbt", 3)
            Change_Status(girl, "Love", -5)            # more than solo (-3)
            Change_Status(girl, "Lust", 1)

        # ── Trait modifiers ──
        if hasattr(girl, "has_trait"):
            # Positive traits — gain lust/inbt
            if girl.has_trait("camera_lover"):
                Change_Status(girl, "Inbt", 3)
                Change_Status(girl, "Lust", 2)
            if girl.has_trait("exhibitionist"):
                Change_Status(girl, "Lust", 3)
                Change_Status(girl, "Inbt", 2)
            if girl.has_trait("voyeur") and subject == "other":
                Change_Status(girl, "Lust", 3)
            if girl.has_trait("public_fetish"):
                Change_Status(girl, "Lust", 2)
                Change_Status(girl, "Inbt", 1)
            if girl.has_trait("cum_slut"):
                Change_Status(girl, "Lust", 2)
                if vid_type == "creampie":
                    Change_Status(girl, "Lust", 3)
                    Change_Status(girl, "Inbt", 3)

            # Negative traits — lose love, resist
            if girl.has_trait("camera_hater") and subject == "self":
                Change_Status(girl, "Love", -8)
            if girl.has_trait("public_shy"):
                Change_Status(girl, "Love", -3)
            if girl.has_trait("hate_cum"):
                Change_Status(girl, "Lust", -2)
                if vid_type == "creampie":
                    Change_Status(girl, "Love", -5)
            if girl.has_trait("loyal"):
                Change_Status(girl, "Love", -3)
                if subject == "other":
                    Change_Status(girl, "Love", -3)

            # Cheater — enjoys the scandal
            if girl.has_trait("cheater"):
                Change_Status(girl, "Inbt", 3)
                Change_Status(girl, "Lust", 2)

            # Hardcore — mild arousal from explicit content
            if girl.has_trait("hardcore_sex") and vid_type in ("cowgirl", "reverse_cowgirl", "creampie"):
                Change_Status(girl, "Lust", 2)

            # Cute sex — discomfort with group exposure
            if girl.has_trait("cute_sex"):
                Change_Status(girl, "Love", -2)

        # ── BF/GF overlay (tier-scaled cheating exposure) ──
        # Not an exposure when the partner watching her own video has NTR active + known: he is in on it
        _ntr_known_here = (subject == "self" and has_bf and _ntr_active_discovered(girl)
                           and getattr(girl, "npc_partner_id", None) in group.get("members", []))
        if _ntr_known_here:
            for _stat, _val in _GROUP_BF_NTR_KNOWN_STATS.items():
                Change_Status(girl, _stat, _val)
            print("[GROUP_VIDEO_STATS] %s: ntr_known overlay %s (no exposure penalty, no leverage)" % (girl.gid, _GROUP_BF_NTR_KNOWN_STATS))
        elif has_bf:
            _tier = _GROUP_VIDEO_SEVERITY_TIER.get(vid_type, 2)
            if is_cheater:
                Change_Status(girl, "Inbt", 2 + _tier)
                Change_Status(girl, "Lust", 1 + _tier)
                provoke(girl, max(1, _tier - 1))
            else:
                _penalties = _GROUP_BF_CHEATING_PENALTIES.get(subject, {}).get(_tier, {})
                for _stat in ("Love", "Obed", "Inbt"):
                    _val = _penalties.get(_stat, 0)
                    if _val:
                        Change_Status(girl, _stat, _val)
                _loy = _penalties.get("bf_loyalty", 0)
                if _loy and hasattr(girl, "change_bf_loyalty"):
                    girl.change_bf_loyalty(_loy)
                provoke(girl, _penalties.get("provoke", 1))
            _lev = _GROUP_SHARE_LEVERAGE.get(_tier, 0)
            if _lev > 0 and subject == "self" and hasattr(girl, "gain_blackmail_leverage"):
                girl.gain_blackmail_leverage(_lev)
                debug_log("[GROUP_VIDEO] %s gained %d blackmail leverage from tier %d exposure" % (girl.gid, _lev, _tier))

        # ── Dating (GF) overlay ──
        if is_dating and subject == "other":
            Change_Status(girl, "Love", -20)        # heavier than solo (-15)
            Change_Status(girl, "Obed", -12)

        # ── Group size bonus — more girls = more exposure ──
        if _group_size >= 3:
            Change_Status(girl, "Inbt", 2)
            if subject == "self":
                Change_Status(girl, "Love", -2)

        # ── Obedience: she watched and stayed — slight compliance ──
        if not is_dating or subject == "self":
            Change_Status(girl, "Obed", 1)

        # ── Virginity knowledge propagation in group context ──
        # girl_learns_virgin only records if target currently has the virgin trait,
        # so this safely no-ops for girls who already lost their virginity.
        _members = group.get("members", [])
        for _m_gid in _members:
            _m = GIRL_BY_ID.get(_m_gid)
            if _m and _m.gid != girl.gid:
                girl_learns_virgin(_m, girl)

    # ==========================================================
    # GROUP: Discover helper — fire trait notification when a
    # trait-specific line is picked so the player learns the trait.
    # ==========================================================
    def _group_video_discover(girl, trait):
        """Call girl.discover() for the given trait if applicable."""
        if not hasattr(girl, "discover"):
            return
        if trait == "virgin":
            girl.discover("discovered_virgin")
        else:
            girl.discover("discovered_trait_%s" % trait)

    # ==========================================================
    # GROUP: Pick combo line (2-trait combos)
    # ==========================================================
    def _pick_group_video_combo_line(girl, subject, vid_type, vid=None):
        """Pick a 2-trait combo line from GROUP_VIDEO_COMBO_LINES."""
        if not hasattr(girl, "has_trait"):
            return None
        tg = _video_type_group(vid_type)
        _vid_condom = vid.get("condom", False) if vid else False
        all_traits = [
            "camera_lover", "camera_hater", "cum_slut", "hate_cum",
            "hardcore_sex", "cute_sex", "public_fetish", "public_shy",
            "exhibitionist", "voyeur", "cheater", "loyal",
            "anal_lover", "anal_hater",
        ]
        # an eager trait she is still discovering has no veteran combo voice (same rule as _pick_video_combo_line)
        girl_traits = [t for t in all_traits if girl.has_trait(t) and not trait_is_discovering(girl, t) and (t != "cheater" or _cheater_applies(girl)) and (t != "loyal" or _loyal_applies(girl)) and (t != "hate_cum" or not _vid_condom)]
        if len(girl_traits) < 2:
            return None
        for i in range(len(girl_traits)):
            for j in range(i + 1, len(girl_traits)):
                combo = frozenset([girl_traits[i], girl_traits[j]])
                for tkey in [tg, "any"]:
                    key = (combo, subject, tkey)
                    if key in GROUP_VIDEO_COMBO_LINES:
                        _group_video_discover(girl, girl_traits[i])
                        _group_video_discover(girl, girl_traits[j])
                        return _group_unique_choice(GROUP_VIDEO_COMBO_LINES[key])
        return None

    # ==========================================================
    # GROUP: Pick trait line (single trait)
    # ==========================================================
    def _pick_group_video_trait_line(girl, subject, vid_type, vid=None):
        """Pick a single-trait line from GROUP_VIDEO_TRAIT_LINES."""
        tg = _video_type_group(vid_type)
        # an anal video tries its own "anal" pools before the "penetration" group (they were never reached)
        _tkeys = (["anal"] if vid_type in _ANAL_SCENE_TYPES else []) + [tg, "any"]
        _vid_condom = vid.get("condom", False) if vid else False
        if hasattr(girl, "has_trait") and girl.has_trait("lesbian") and girl.has_trait("virgin"):
            for tkey in _tkeys:
                key = ("lesbian_virgin", subject, tkey)
                if key in GROUP_VIDEO_TRAIT_LINES:
                    _group_video_discover(girl, "lesbian")
                    _group_video_discover(girl, "virgin")
                    return _group_unique_choice(GROUP_VIDEO_TRAIT_LINES[key])
        # submissive before hardcore: a line about being used is hers (docs/plan_femdom.md D3); a (trait, subject,
        # type) she has no pool for falls through to the next trait
        trait_order = [
            "camera_lover", "camera_hater",
            "cum_slut", "hate_cum",
            "submissive", "hardcore_sex", "cute_sex",
            "public_fetish", "public_shy",
            "voyeur", "exhibitionist",
            "cheater", "loyal",
            "anal_lover", "anal_hater",
            "virgin",
            "lesbian",
        ]
        _girl_has_sex_history = bool(getattr(girl, "intimacy_flags", set()) & {"hj", "bj", "tj", "sex", "anal"})
        _girl_is_lesbian = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        _implies_history = {"hardcore_sex", "cum_slut", "exhibitionist"}
        _needs_nohist = not _girl_has_sex_history or _girl_is_lesbian
        for trait in trait_order:
            if not (hasattr(girl, "has_trait") and girl.has_trait(trait)):
                continue
            if trait == "cheater" and not _cheater_applies(girl):
                continue
            if trait == "loyal" and not _loyal_applies(girl):
                continue
            if trait == "hate_cum" and _vid_condom:
                continue
            # No history or lesbian: try "other_nohist" variants for traits that imply wanting the player
            if subject == "other" and trait in _implies_history and _needs_nohist:
                if _girl_is_lesbian:
                    continue
                for tkey in _tkeys:
                    nh_key = (trait, "other_nohist", tkey)
                    if nh_key in GROUP_VIDEO_TRAIT_LINES:
                        _group_video_discover(girl, trait)
                        return _group_unique_choice(GROUP_VIDEO_TRAIT_LINES[nh_key])
                continue
            # still discovering an eager trait: its discovery lines or nothing (trait_line_keys)
            for tname in trait_line_keys(girl, trait):
                for tkey in _tkeys:
                    key = (tname, subject, tkey)
                    if key in GROUP_VIDEO_TRAIT_LINES:
                        _group_video_discover(girl, trait)
                        return _group_unique_choice(GROUP_VIDEO_TRAIT_LINES[key])
        return None

    # ==========================================================
    # GROUP: Pick blended line (context + trait + type)
    # ==========================================================
    def _pick_group_video_blended_line(girl, subject, vid_type, vid=None):
        """Try group-specific blended line combining context + trait + type."""
        if not hasattr(girl, "has_trait"):
            return None
        tg = _video_type_group(vid_type)
        is_dating = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        has_bf = _is_bf_context(girl)
        _vid_of_gf = vid and _video_is_of_player_gf(vid)
        _player_has_gf = player_has_girlfriend(ALL_GIRLS) and not is_dating and not _vid_of_gf and not is_player_harem_exempt(girl)

        if is_dating:
            ctx = "dating"
        elif _player_has_gf and has_bf:
            ctx = "both"
        elif _player_has_gf:
            ctx = "player_gf"
        elif has_bf:
            ctx = "bf"
        else:
            return None

        _vid_condom = vid.get("condom", False) if vid else False
        trait_order = [
            "camera_lover", "camera_hater", "cum_slut", "hate_cum",
            "hardcore_sex", "cute_sex", "exhibitionist", "public_shy",
            "public_fetish", "cheater", "loyal", "voyeur", "virgin",
            "lesbian",
        ]
        for trait in trait_order:
            if not girl.has_trait(trait):
                continue
            if trait == "hate_cum" and _vid_condom:
                continue
            # still discovering an eager trait: its discovery lines or nothing (trait_line_keys)
            for tname in trait_line_keys(girl, trait):
                for tkey in [vid_type, tg, "any"]:
                    key = (ctx, tname, subject, tkey)
                    if key in GROUP_VIDEO_BLENDED_LINES:
                        _group_video_discover(girl, trait)
                        line = _group_unique_choice(GROUP_VIDEO_BLENDED_LINES[key])
                        if ctx in ("player_gf", "both"):
                            gf_name = _get_player_gf_name()
                            line = _tl(line).replace("{0}", gf_name)
                        return line
        return None

    # ==========================================================
    # GROUP: Pick full reaction (other girl has BF)
    # ==========================================================
    def _pick_group_full_video_reaction(girl, vid, group):
        """Combined line for 'other' videos where the girl in video has a BF.
        Uses GROUP_ versions with tone override."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        if subject != "other":
            return None
        other_has_bf = _vid_bf_still_relevant(vid)
        if not other_has_bf:
            return None

        name = _get_vid_girl_name(vid)
        loc = vid.get("location", "room")
        is_pub = _is_public_location(loc)
        loc_tag = "public" if is_pub else "private"
        vid_type = vid.get("type", "hj")
        if vid_type == "reverse_cowgirl":
            vid_type = "cowgirl"
        tg = _video_type_group(vid_type)

        tone = _get_cheat_tone(girl)
        if tone != "casual":
            _pool = GROUP_VIDEO_FULL_REACTION_PANIC if tone == "panic" else GROUP_VIDEO_FULL_REACTION_HORNY
            for tkey in [vid_type, tg, "any"]:
                if tkey in _pool:
                    return _tl(_group_unique_choice(_pool[tkey])).replace("{name}", name)

        # Casual: trait-aware from GROUP_VIDEO_FULL_REACTION
        _vid_condom = vid.get("condom", False)
        trait_order = [
            "cum_slut", "hate_cum", "camera_lover", "camera_hater",
            "cheater", "loyal", "hardcore_sex", "cute_sex",
            "public_fetish", "public_shy", "voyeur", "exhibitionist",
            "lesbian",
        ]
        if hasattr(girl, "has_trait"):
            for trait in trait_order:
                if not girl.has_trait(trait):
                    continue
                if trait == "cheater" and not _cheater_applies(girl):
                    continue
                if trait == "loyal" and not _loyal_applies(girl):
                    continue
                if trait == "hate_cum" and _vid_condom:
                    continue
                for tkey in [vid_type, tg, "any"]:
                    key = (loc_tag, tkey, trait)
                    if key in GROUP_VIDEO_FULL_REACTION:
                        _group_video_discover(girl, trait)
                        return _tl(_group_unique_choice(GROUP_VIDEO_FULL_REACTION[key])).replace("{name}", name)

        for tkey in [vid_type, tg, "any"]:
            key = (loc_tag, tkey, "_default")
            if key in GROUP_VIDEO_FULL_REACTION:
                return _tl(_group_unique_choice(GROUP_VIDEO_FULL_REACTION[key])).replace("{name}", name)
        return None

    # ==========================================================
    # GROUP: Pick BF line
    # ==========================================================
    def _pick_group_video_bf_line(girl, subject, vid_type, partner_in_group=False):
        """Pick a BF/GF-aware line from GROUP_VIDEO_BF/GF_TYPE_LINES + GROUP_VIDEO_BF_SELF/OTHER_LINES.
        When partner_in_group is True, uses BF_WATCHING pools (he already saw it)."""
        if not partner_in_group:
            _type_dict = GROUP_VIDEO_GF_TYPE_LINES if (hasattr(girl, "get_flag") and girl.get_flag("partner_is_female")) else GROUP_VIDEO_BF_TYPE_LINES
            tg = _video_type_group(vid_type)
            for tkey in [vid_type, tg]:
                key = (subject, tkey)
                if key in _type_dict:
                    return _group_unique_choice(_type_dict[key])

        _bf_mood = _get_bf_mood(girl) if hasattr(girl, "has_trait") else "normal"
        if partner_in_group:
            if subject == "self":
                pool = GROUP_VIDEO_BF_WATCHING_SELF_LINES
            else:
                pool = GROUP_VIDEO_BF_WATCHING_OTHER_LINES
        else:
            if subject == "self":
                pool = GROUP_VIDEO_BF_SELF_LINES
            else:
                pool = GROUP_VIDEO_BF_OTHER_LINES
        lines = pool.get(_bf_mood) or pool.get("normal")
        if lines:
            return _group_unique_choice(lines)
        return None

    def _get_bf_mood(girl):
        """Determine BF mood tier for video reactions."""
        if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
            return "cheater"
        bf_love = getattr(girl, "BFLove", 50)
        if bf_love >= 80:
            return "in_love"
        elif bf_love >= 50:
            return "normal"
        elif bf_love >= 25:
            return "strained"
        return "miserable"

    # ==========================================================
    # GROUP: Pick dating line (she IS the player's GF)
    # ==========================================================
    def _pick_group_video_dating_line(girl, subject, vid_type, vid=None):
        """Pick a dating-context line from GROUP_VIDEO_DATING_PLAYER_LINES and GROUP_VIDEO_DATING_TYPE_LINES."""
        if not hasattr(girl, "is_dating_player") or not girl.is_dating_player():
            return None

        tg = _video_type_group(vid_type)

        # Type-specific dating line first
        for tkey in [vid_type, tg]:
            key = (subject, tkey)
            if key in GROUP_VIDEO_DATING_TYPE_LINES:
                return _group_unique_choice(GROUP_VIDEO_DATING_TYPE_LINES[key])

        # Then trait-based from GROUP_VIDEO_DATING_PLAYER_LINES
        sub_dict = GROUP_VIDEO_DATING_PLAYER_LINES.get(subject, {})
        if hasattr(girl, "has_trait"):
            trait_order = [
                "camera_lover", "camera_hater", "cum_slut", "hate_cum",
                "hardcore_sex", "cute_sex", "exhibitionist", "public_shy",
                "public_fetish", "cheater", "loyal", "voyeur", "virgin",
                "lesbian",
            ]
            _vid_condom = vid.get("condom", False) if vid else False
            for trait in trait_order:
                if not girl.has_trait(trait) or (trait == "hate_cum" and _vid_condom):
                    continue
                # still discovering an eager trait: its discovery lines or nothing (trait_line_keys)
                for tname in trait_line_keys(girl, trait):
                    if tname in sub_dict:
                        _group_video_discover(girl, trait)
                        return _group_unique_choice(sub_dict[tname])

        # Emotional fallback
        if subject == "other":
            for emo_key in ["_furious", "_heartbroken", "_default"]:
                if emo_key in sub_dict:
                    return _group_unique_choice(sub_dict[emo_key])
        if "_default" in sub_dict:
            return _group_unique_choice(sub_dict["_default"])
        return None

    # ==========================================================
    # GROUP: Pick player-GF line (player has a GF, girl is NOT the GF)
    # ==========================================================
    def _pick_group_video_player_gf_line(girl, subject, vid_type, vid=None):
        """Pick a line about the player having a GF, from GROUP_VIDEO_PLAYER_GF_TYPE_LINES / GROUP_VIDEO_PLAYER_GF_LINES."""
        is_dating = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        if is_dating:
            return None
        _vid_of_gf = vid and _video_is_of_player_gf(vid)
        if not player_has_girlfriend(ALL_GIRLS) or _vid_of_gf or is_player_harem_exempt(girl):
            return None

        gf_name = _get_player_gf_name()
        tg = _video_type_group(vid_type)

        # Type-specific first
        for tkey in [vid_type, tg]:
            key = (subject, tkey)
            if key in GROUP_VIDEO_PLAYER_GF_TYPE_LINES:
                line = _group_unique_choice(GROUP_VIDEO_PLAYER_GF_TYPE_LINES[key])
                return _tl(line).replace("{0}", gf_name)

        # Then tier-based
        _tier = _get_gf_tier(girl)
        key = (subject, _tier)
        if key in GROUP_VIDEO_PLAYER_GF_LINES:
            line = _group_unique_choice(GROUP_VIDEO_PLAYER_GF_LINES[key])
            return _tl(line).replace("{0}", gf_name)
        return None

    def _get_gf_tier(girl):
        """Determine the girl's attitude tier toward the player's GF."""
        if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
            return "cheater"
        love = getattr(girl, "Love", 0)
        if love >= 80:
            return "close"
        elif love >= 40:
            return "friendly"
        elif love >= 10:
            return "distant"
        return "hostile"

    # ==========================================================
    # GROUP: Pick location follow-up
    # ==========================================================
    def _pick_group_video_location_line(girl, vid):
        """Pick a location follow-up from GROUP_VIDEO_LOCATION_LINES."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        # Non-consensual self: skip location commentary
        if subject == "self" and not vid.get("consensual", True):
            return None

        loc = vid.get("location", "room")
        is_pub = _is_public_location(loc)
        loc_tag = "public" if is_pub else "private"
        vid_type = vid.get("type", "hj")
        tg = _video_type_group(vid_type)

        # Trait-specific
        if hasattr(girl, "has_trait"):
            trait_order = [
                "public_fetish", "public_shy", "exhibitionist",
                "camera_lover", "camera_hater", "voyeur",
                "lesbian",
            ]
            for trait in trait_order:
                if not girl.has_trait(trait):
                    continue
                for tkey in [tg, "any"]:
                    key = (subject, loc_tag, trait, tkey)
                    if key in GROUP_VIDEO_LOCATION_LINES:
                        return _group_unique_choice(GROUP_VIDEO_LOCATION_LINES[key])

        # Default
        for tkey in [tg, "any"]:
            key = (subject, loc_tag, "_default", tkey)
            if key in GROUP_VIDEO_LOCATION_LINES:
                return _group_unique_choice(GROUP_VIDEO_LOCATION_LINES[key])
        return None

    # ==========================================================
    # GROUP: Pick BF viewer follow-up (she has BF, sees other girl)
    # ==========================================================
    def _pick_group_video_bf_viewer_followup(girl, vid, group):
        """Follow-up when viewer has BF and sees another girl's video in group.
        Uses GROUP_ versions of same-act jealousy and both-committed lines.
        References the other girl by name."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        if subject != "other":
            return None
        if not _is_bf_context(girl):
            return None

        vid_type = vid.get("type", "hj")
        tg = _video_type_group(vid_type)
        name = _get_vid_girl_name(vid)
        other_has_bf = _vid_bf_still_relevant(vid)
        tone = _get_cheat_tone(girl)

        # Did she do the same act with player?
        # by video type: a position reads its counter, "laying_anal" reads anal, "creampie" its own count
        _did_same = girl_type_count(girl, vid_type) > 0

        # Both committed + same act (most specific)
        if _did_same and other_has_bf:
            if tone == "panic":
                for tkey in [vid_type, tg, "any"]:
                    if tkey in GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_PANIC:
                        return _group_unique_choice(GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_PANIC[tkey])
            elif tone == "horny":
                for tkey in [vid_type, tg, "any"]:
                    if tkey in GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_HORNY:
                        return _group_unique_choice(GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED_HORNY[tkey])
            else:
                for tkey in [vid_type, tg, "any"]:
                    if tkey in GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED:
                        line = _group_unique_choice(GROUP_VIDEO_BF_JEALOUSY_BOTH_COMMITTED[tkey])
                        if "{name}" in line:
                            line = _tl(line).replace("{name}", name)
                        return line

        # Same act jealousy (no both-committed)
        if _did_same:
            for tkey in [vid_type, tg, "any"]:
                if tkey in GROUP_VIDEO_BF_JEALOUSY_SAME_ACT:
                    line = _group_unique_choice(GROUP_VIDEO_BF_JEALOUSY_SAME_ACT[tkey])
                    if "{name}" in line:
                        line = _tl(line).replace("{name}", name)
                    return line

        # Both committed (no same act)
        if other_has_bf:
            if tone == "panic":
                return _tl(_group_unique_choice(GROUP_VIDEO_BOTH_COMMITTED_PANIC))
            elif tone == "horny":
                return _tl(_group_unique_choice(GROUP_VIDEO_BOTH_COMMITTED_HORNY))
            else:
                return _tl(_group_unique_choice(GROUP_VIDEO_BOTH_COMMITTED_LINES))

        return None

    # ==========================================================
    # GROUP: Pick self-aware follow-up
    # ==========================================================
    def _pick_group_video_self_aware_followup(girl, vid):
        """Self-aware follow-up from GROUP_VIDEO_SELF_AWARE_LINES."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        if subject != "other":
            return None
        if not hasattr(girl, "has_trait"):
            return None

        _own_vids = [v for v in getattr(store.Player, "recorded_videos", []) if v.get("girl_gid") == girl.gid]
        _has_videos = len(_own_vids) > 0
        _own_vid_types = set(v.get("type", "") for v in _own_vids)
        _has_sex_vids = bool(_own_vid_types & {"cowgirl", "reverse_cowgirl", "sex"})
        _cream_count = int(getattr(girl, "CreampieCounts", 0))
        _has_creampies = _cream_count >= 1
        _has_bf = _is_bf_context(girl)

        trait_order = [
            "camera_hater", "camera_lover", "hate_cum", "cum_slut",
            "cheater", "loyal", "hardcore_sex", "cute_sex",
            "exhibitionist", "public_shy", "voyeur",
            "lesbian",
        ]
        matched_trait = None
        for trait in trait_order:
            if girl.has_trait(trait):
                matched_trait = trait
                break
        if not matched_trait:
            matched_trait = "_default"

        # Determine situation
        if matched_trait in ("hate_cum", "cum_slut"):
            sit = "has_creampies" if _has_creampies else "no_creampies"
        elif matched_trait in ("cheater", "loyal"):
            sit = "has_bf" if _has_bf else "no_bf"
        elif matched_trait in ("hardcore_sex", "cute_sex"):
            sit = "has_sex_vids" if _has_sex_vids else "no_sex_vids"
        elif matched_trait == "voyeur":
            sit = "any"
        else:
            sit = "has_videos" if _has_videos else "no_videos"

        for try_key in [(matched_trait, sit), (matched_trait, "any"), ("_default", sit), ("_default", "has_videos" if _has_videos else "no_videos")]:
            if try_key in GROUP_VIDEO_SELF_AWARE_LINES:
                # discover only when HER trait pool answers (a missing key falls to _default: no evidence)
                if matched_trait != "_default" and try_key[0] == matched_trait:
                    _group_video_discover(girl, matched_trait)
                return _group_unique_choice(GROUP_VIDEO_SELF_AWARE_LINES[try_key])
        return None

    # ==========================================================
    # GROUP: GF cheating gate (she IS the GF, sees other girl in group)
    # ==========================================================
    def _group_video_gf_cheating_breakup(girl, vid_type, group, vid=None):
        """GF sees video of another girl in group — shock + possible breakup."""
        tg = _video_type_group(vid_type)
        # Shock line (type-specific)
        shock = None
        for tkey in [vid_type, tg]:
            if tkey in GROUP_VIDEO_GF_CHEATING_SHOCK:
                shock = _group_unique_choice(GROUP_VIDEO_GF_CHEATING_SHOCK[tkey])
                break
        if not shock:
            shock = _tl(_group_unique_choice(GROUP_VIDEO_GF_CHEATING_SHOCK_DEFAULT))
        if vid:
            shock = _group_full_sub(shock, girl, vid, group)
        else:
            shock = _group_name_sub(shock, girl, group)
        Say_Line(girl, shock)

        # Breakup
        breakup_line = _tl(_group_unique_choice(GROUP_VIDEO_GF_CHEATING_BREAKUP))
        if vid:
            breakup_line = _group_full_sub(breakup_line, girl, vid, group)
        else:
            breakup_line = _group_name_sub(breakup_line, girl, group)
        Say_Line(girl, breakup_line)

        # Stat penalties
        Change_Status(girl, "Love", -400)
        Change_Status(girl, "Obed", 50)
        Change_Status(girl, "Lust", -10)
        # Trigger breakup — girl becomes ex
        if hasattr(girl, "break_up_with_player"):
            girl.break_up_with_player(reason="saw_cheating_video", mood="angry")
            girl.set_temp_status("angry", days=7, reason="saw_cheating_video")

    # ==========================================================
    # GROUP: Other girl's BF lines
    # ==========================================================
    def _pick_group_video_other_girl_bf_lines(girl, vid, group):
        """When subject is 'other' and the girl in the video has a BF.
        Uses GROUP_VIDEO_OTHER_GIRL_BF_LINES."""
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        if subject != "other":
            return None
        other_has_bf = _vid_bf_still_relevant(vid)
        if not other_has_bf:
            return None
        if not hasattr(girl, "has_trait"):
            return None

        vid_type = vid.get("type", "hj")
        tg = _video_type_group(vid_type)

        _vid_condom = vid.get("condom", False)
        trait_order = [
            "camera_hater", "camera_lover", "hate_cum", "cum_slut",
            "cheater", "loyal", "hardcore_sex", "cute_sex",
            "exhibitionist", "public_shy", "voyeur", "virgin",
            "lesbian",
        ]
        for trait in trait_order:
            if not girl.has_trait(trait) or trait_is_discovering(girl, trait):   # no veteran voice while she discovers it
                continue
            if trait == "cheater" and not _cheater_applies(girl):
                continue
            if trait == "loyal" and not _loyal_applies(girl):
                continue
            if trait == "hate_cum" and _vid_condom:
                continue
            for tkey in [vid_type, tg, "any"]:
                key = (trait, tkey)
                if key in GROUP_VIDEO_OTHER_GIRL_BF_LINES:
                    _group_video_discover(girl, trait)
                    return _group_unique_choice(GROUP_VIDEO_OTHER_GIRL_BF_LINES[key])

        # Fallback
        for tkey in [vid_type, tg, "any"]:
            key = ("_default", tkey)
            if key in GROUP_VIDEO_OTHER_GIRL_BF_LINES:
                return _group_unique_choice(GROUP_VIDEO_OTHER_GIRL_BF_LINES[key])
        return None

    # ==========================================================
    # GROUP: Name substitution — reference other girls in the group
    # ==========================================================
    def _group_name_sub(line, girl, group):
        """Personalize group references based on actual members.
        For 2-person groups: replace generic 'the group/everyone/the whole chat'
        with the specific other girl's name so it reads naturally.
        For 3+ groups: keep generic language (it actually makes sense).
        Translated first: a name put in before the lookup made it miss."""
        line = _tl(line)
        # Collect other members' names
        other_names = []
        for gid in group.get("members", []):
            if gid == girl.gid:
                continue
            g = GIRL_BY_ID.get(gid)
            if g and hasattr(g, "Name"):
                other_names.append(g.Name)

        # Handle {other_girl} placeholder
        if "{other_girl}" in line:
            if other_names:
                line = line.replace("{other_girl}", _group_unique_choice(other_names))
            else:
                line = line.replace("{other_girl}", _tl(_("the others")))

        # For 2-person groups, replace generic group references with the other girl's name
        if len(other_names) == 1:
            _oname = other_names[0]
            # Ordered replacements — longest/most specific first to avoid partial matches
            _replacements = [
                # CAPS variations (preserve emphasis)
                ("EVERYONE in this chat", _oname),
                ("EVERYONE in this group", _oname),
                ("EVERYONE", _oname.upper()),
                ("the ENTIRE GROUP", _oname),
                ("the WHOLE GROUP", _oname),
                ("the WHOLE CHAT", _oname),
                ("the GROUP CHAT", _oname),
                ("the GROUP", _oname),
                # "Every girl in this chat/group"
                ("Every girl in this chat", _oname),
                ("Every girl in this group", _oname),
                ("every girl in this chat", _oname),
                ("every girl in this group", _oname),
                ("every girl here", _oname),
                # "Everyone in this chat/group"
                ("Everyone in this chat", _oname),
                ("Everyone in this group", _oname),
                ("Everyone in the chat", _oname),
                ("everyone in this chat", _oname),
                ("everyone in this group", _oname),
                ("everyone in the chat", _oname),
                # "Everyone" standalone
                ("Everyone just", _oname + " just"),
                ("Everyone can", _oname + " can"),
                ("Everyone knows", _oname + " knows"),
                ("Everyone watching", _oname + " watching"),
                ("Everyone saw", _oname + " saw"),
                ("Everyone seeing", _oname + " seeing"),
                ("everyone just", _oname + " just"),
                ("everyone can", _oname + " can"),
                ("everyone knows", _oname + " knows"),
                ("everyone watching", _oname + " watching"),
                ("everyone saw", _oname + " saw"),
                ("everyone seeing", _oname + " seeing"),
                ("everyone", _oname),
                # "The whole group/chat" variations
                ("The whole group chat", _oname),
                ("the whole group chat", _oname),
                ("The whole group", _oname),
                ("the whole group", _oname),
                ("The whole chat", _oname),
                ("the whole chat", _oname),
                ("The entire group", _oname),
                ("the entire group", _oname),
                ("The entire chat", _oname),
                ("the entire chat", _oname),
                # "The group" — careful with context
                ("The group just", _oname + " just"),
                ("The group has", _oname + " has"),
                ("The group can", _oname + " can"),
                ("The group is", _oname + " is"),
                ("The group saw", _oname + " saw"),
                ("The group knows", _oname + " knows"),
                ("The group watching", _oname + " watching"),
                ("the group just", _oname + " just"),
                ("the group has", _oname + " has"),
                ("the group can", _oname + " can"),
                ("the group is", _oname + " is"),
                ("the group saw", _oname + " saw"),
                ("the group knows", _oname + " knows"),
                ("the group watching", _oname + " watching"),
                # "shared/sent/shown with/to the group"
                ("shared with the group", "sent to " + _oname),
                ("Shared with the group", "Sent to " + _oname),
                ("sent to the group", "sent to " + _oname),
                ("shown to the group", "shown to " + _oname),
                ("shared with everyone", "sent to " + _oname),
                ("shown to everyone", "shown to " + _oname),
                ("sent to everyone", "sent to " + _oname),
                ("sent to EVERYONE", "sent to " + _oname.upper()),
                ("sent to ALL of us", "sent to " + _oname),
                ("shared with EVERYONE", "sent to " + _oname.upper()),
                # "in the group/chat"
                ("in the group chat", "to " + _oname),
                ("in the GROUP CHAT", "to " + _oname),
                ("in the GROUP", "to " + _oname),
                ("in the group", "to " + _oname),
                ("in the chat", "to " + _oname),
                ("in this chat", "to " + _oname),
                ("in this group", "to " + _oname),
                ("in OUR group", "to " + _oname),
                ("in our group", "to " + _oname),
                # "for the group/chat"
                ("for the whole group", "for " + _oname + " to see"),
                ("for the whole chat", "for " + _oname + " to see"),
                ("for the group", "for " + _oname + " to see"),
                ("for the chat", "for " + _oname + " to see"),
                ("for everyone", "for " + _oname + " to see"),
                # "with the group"
                ("with the group", "with " + _oname),
                ("with the chat", "with " + _oname),
                ("with everyone", "with " + _oname),
                # "All of us" / "all of us"
                ("ALL of us", _oname),
                ("All of us", _oname),
                ("all of us", _oname),
                # "the girls" / "other girls"
                ("the girls", _oname),
                ("The girls", _oname),
                # "the chat" standalone
                ("The chat just", _oname + " just"),
                ("The chat has", _oname + " has"),
                ("the chat just", _oname + " just"),
                ("the chat has", _oname + " has"),
                ("the chat", _oname),
            ]
            for old, new in _replacements:
                if old in line:
                    line = line.replace(old, new, 1)

        return line

    def _group_vid_girl_sub(line, vid):
        """Replace generic 'another girl/some girl/someone else/her' references
        with the actual video girl's name when subject is 'other'."""
        vid_gid = vid.get("girl_gid", "")
        vid_girl = GIRL_BY_ID.get(vid_gid)
        if not vid_girl or not hasattr(vid_girl, "Name"):
            return line
        vname = vid_girl.Name

        _replacements = [
            ("another girl's", vname + "'s"),
            ("Another girl's", vname + "'s"),
            ("another girl", vname),
            ("Another girl", vname),
            ("some girl's", vname + "'s"),
            ("Some girl's", vname + "'s"),
            ("some girl", vname),
            ("Some girl", vname),
            ("someone else's", vname + "'s"),
            ("Someone else's", vname + "'s"),
            ("someone else", vname),
            ("Someone else", vname),
            ("other girls", vname),
            ("Other girls", vname),
            ("other girl", vname),
            ("Other girl", vname),
        ]
        for old, new in _replacements:
            if old in line:
                line = line.replace(old, new, 1)
        return line

    def _group_name_sub_first_person(line):
        """For 2-person groups where the video girl IS the other member.
        The speaker IS the only real audience, so 'the group/everyone' → 'me/I'."""
        _replacements = [
            # CAPS
            ("EVERYONE in this chat", "I"),
            ("EVERYONE in this group", "I"),
            ("EVERYONE", "ME"),
            ("the ENTIRE GROUP", "ME"),
            ("the WHOLE GROUP", "ME"),
            ("the WHOLE CHAT", "ME"),
            ("the GROUP CHAT", "ME"),
            ("the GROUP", "ME"),
            # Every girl
            ("Every girl in this chat", "I"),
            ("Every girl in this group", "I"),
            ("every girl in this chat", "I"),
            ("every girl in this group", "I"),
            ("every girl here", "I"),
            # Everyone in this chat/group (verb-aware before generic)
            (_("Everyone in this chat just"), _("I just")),
            (_("Everyone in this group just"), _("I just")),
            (_("Everyone in this chat now knows"), _("I now know")),
            (_("Everyone in this chat now has"), _("I now have")),
            (_("Everyone in this chat can see"), _("I can see")),
            (_("Everyone in this chat can"), _("I can")),
            (_("Everyone in this chat knows"), _("I know")),
            (_("Everyone in this chat saw"), _("I saw")),
            (_("Everyone in this chat has"), _("I have")),
            (_("Everyone in this chat is watching"), _("I'm watching")),
            (_("Everyone in this chat is"), _("I'm")),
            ("Everyone in this chat", "I"),
            ("Everyone in this group", "I"),
            ("Everyone in the chat", "I"),
            (_("everyone in this chat just"), _("I just")),
            (_("everyone in this group just"), _("I just")),
            (_("everyone in this chat now knows"), _("I now know")),
            (_("everyone in this chat now has"), _("I now have")),
            (_("everyone in this chat can see"), _("I can see")),
            (_("everyone in this chat can"), _("I can")),
            (_("everyone in this chat knows"), _("I know")),
            (_("everyone in this chat saw"), _("I saw")),
            (_("everyone in this chat has"), _("I have")),
            (_("everyone in this chat is watching"), _("I'm watching")),
            (_("everyone in this chat is"), _("I'm")),
            ("everyone in this chat", "I"),
            ("everyone in this group", "I"),
            ("everyone in the chat", "I"),
            # Everyone + verb
            (_("Everyone just"), _("I just")),
            (_("Everyone can"), _("I can")),
            (_("Everyone knows"), _("I know")),
            (_("Everyone watching"), _("I'm watching")),
            (_("Everyone saw"), _("I saw")),
            (_("Everyone seeing"), _("I'm seeing")),
            (_("everyone just"), _("I just")),
            (_("everyone can"), _("I can")),
            (_("everyone knows"), _("I know")),
            (_("everyone watching"), _("I'm watching")),
            (_("everyone saw"), _("I saw")),
            (_("everyone seeing"), _("I'm seeing")),
            ("everyone", "I"),
            # The whole/entire group/chat
            ("The whole group chat", "I"),
            ("the whole group chat", "I"),
            (_("The whole group just"), _("I just")),
            (_("The whole group has"), _("I have")),
            (_("The whole group can"), _("I can")),
            ("The whole group", "I"),
            (_("the whole group just"), _("I just")),
            (_("the whole group has"), _("I have")),
            ("the whole group", "I"),
            (_("The whole chat just"), _("I just")),
            ("The whole chat", "I"),
            (_("the whole chat just"), _("I just")),
            ("the whole chat", "I"),
            ("The entire group", "I"),
            ("the entire group", "I"),
            ("The entire chat", "I"),
            ("the entire chat", "I"),
            # The group + verb
            (_("The group just"), _("I just")),
            (_("The group has"), _("I have")),
            (_("The group can"), _("I can")),
            ("The group is", "I'm"),
            (_("The group saw"), _("I saw")),
            (_("The group knows"), _("I know")),
            (_("The group watching"), _("I'm watching")),
            (_("the group just"), _("I just")),
            (_("the group has"), _("I have")),
            (_("the group can"), _("I can")),
            ("the group is", "I'm"),
            (_("the group saw"), _("I saw")),
            (_("the group knows"), _("I know")),
            (_("the group watching"), _("I'm watching")),
            # shared/sent/shown with/to
            (_("shared with the group"), _("showed me")),
            (_("Shared with the group"), _("Showed me")),
            (_("sent to the group"), _("sent to me")),
            (_("shown to the group"), _("showed me")),
            (_("shared with everyone"), _("showed me")),
            (_("Shared with everyone"), _("Showed me")),
            (_("shown to everyone"), _("showed me")),
            (_("sent to everyone"), _("sent to me")),
            (_("sent to EVERYONE"), _("sent to ME")),
            (_("sent to ALL of us"), _("sent to me")),
            (_("shared with EVERYONE"), _("showed ME")),
            # in the group/chat
            (_("in the group chat"), _("to me")),
            (_("in the GROUP CHAT"), _("to ME")),
            (_("in the GROUP"), _("to ME")),
            (_("in the group"), _("to me")),
            (_("in the chat"), _("to me")),
            (_("in this chat"), _("to me")),
            (_("in this group"), _("to me")),
            (_("in OUR group"), _("to me")),
            (_("in our group"), _("to me")),
            # for the group/chat
            (_("for the whole group"), _("for me to see")),
            (_("for the whole chat"), _("for me to see")),
            (_("for the group"), _("for me to see")),
            (_("for the chat"), _("for me to see")),
            (_("for everyone"), _("for me to see")),
            # with the group/chat
            (_("with the group"), _("to me")),
            (_("with the chat"), _("to me")),
            (_("with everyone"), _("to me")),
            # All of us
            ("ALL of us", "me"),
            ("All of us", "me"),
            ("all of us", "us"),
            # the girls
            ("the girls", "me"),
            ("The girls", "Me"),
            # the chat standalone
            (_("The chat just"), _("I just")),
            (_("The chat has"), _("I have")),
            (_("the chat just"), _("I just")),
            (_("the chat has"), _("I have")),
            ("the chat", "me"),
        ]
        for old, new in _replacements:
            if old in line:
                line = line.replace(old, new, 1)
        return line

    def _group_full_sub(line, girl, vid, group):
        """Apply group name + video girl name substitutions with smart context.
        Handles the special case where the video girl IS the other group member
        in a 2-person group: uses first-person for group refs to avoid
        'Rogue just saw Rogue' nonsense.
        The line is translated FIRST (the English surgery below then finds nothing in another language, and a name put
        in before the lookup made it miss), and the partner keys a translation wrote are filled with HER partner."""
        line = _tl(line)
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        vid_gid = vid.get("girl_gid", "")
        other_gids = [gid for gid in group.get("members", []) if gid != girl.gid]

        if subject == "other" and len(other_gids) == 1 and vid_gid == other_gids[0]:
            line = _group_name_sub_first_person(line)
            line = _group_vid_girl_sub(line, vid)
        else:
            line = _group_name_sub(line, girl, group)
            if subject == "other":
                line = _group_vid_girl_sub(line, vid)
        _npc_ref = None
        try:
            if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                _npc_ref = get_npc_partner_for(girl)
        except Exception:
            pass
        _pname = getattr(_npc_ref, "name", None) if _npc_ref else None
        if _pname:
            _bf = _tr("boyfriend")
            _gf = _tr("girlfriend")
            _poss_map = [
                ("my boyfriend", _pname), ("My boyfriend", _pname),
                ("my BF", _pname), ("My BF", _pname),
                ("my girlfriend", _pname), ("My girlfriend", _pname),
                ("my GF", _pname), ("My GF", _pname),
            ]
            if _bf != "boyfriend":
                _poss_map.extend([
                    ("meu " + _bf, _pname), ("Meu " + _bf, _pname),
                    ("minha " + _gf, _pname), ("Minha " + _gf, _pname),
                    ("mi " + _bf, _pname), ("Mi " + _bf, _pname),
                    ("mi " + _gf, _pname), ("Mi " + _gf, _pname),
                ])
            for _old, _new in _poss_map:
                line = line.replace(_old, _new)
        elif hasattr(girl, "get_flag") and girl.get_flag("partner_is_female"):
            _plbl = girl.partner_label() if hasattr(girl, "partner_label") else _tr("girlfriend")
            line = line.replace("a boyfriend", "a " + _plbl)
            line = line.replace(_("a BF"), _("a GF"))
            line = line.replace("my boyfriend", "my " + _plbl)
            line = line.replace(_("my BF"), _("my GF"))
            line = line.replace(_("have a BF"), _("have a GF"))
            line = line.replace("I have a boyfriend", "I have a " + _plbl)
        if "%(" in line:
            line = fmt_safe(line, partner_fmt(girl))
        return line

    # ==========================================================
    # MAIN FUNCTION: group_video_reaction
    # ==========================================================
    def group_video_reaction(girl, vid, group):
        """Full group-aware reaction when the player sends a sex video to a group chat.
        Same priority chain as video_reaction() but uses GROUP_ constants.
        Max 2 lines total.
        Priority:
        1) GF cheating gate (breakup)
        2) Full combined reaction (other + has_bf)
        3) Blended (context + trait + type)
        4) Layered fallback (context + trait + base)
        +1 optional follow-up (bf viewer / location / self-aware)
        """
        if girl_is_away(girl):
            # at her parents' giving birth: she is not reading the group. No lines, no stats, no breakup, and
            # the video is NOT recorded as seen (she reacts if he sends it again when she is back).
            print("[GROUP_VIDEO] %s is away: no reaction" % girl.gid)
            return
        subject = "self" if vid.get("girl_gid") == girl.gid else "other"
        has_bf = _is_bf_context(girl)
        vid_type = vid.get("type", "hj")
        if vid_type == "reverse_cowgirl":
            vid_type = "cowgirl"
        consensual = vid.get("consensual", True)
        is_dating = hasattr(girl, "is_dating_player") and girl.is_dating_player()

        _partner_in_group = False
        if has_bf and hasattr(girl, "npc_partner_id") and girl.npc_partner_id:
            _partner_in_group = girl.npc_partner_id in group.get("members", [])

        # ── Record video seen + cheating knowledge ──
        _record_video_seen(girl, vid)
        _record_video_witness_history(girl, vid)

        # ── Knowledge from video: viewer learns about vid_girl ──
        # Face hidden: can't identify who it is, so no knowledge gained
        if subject == "other" and not vid.get("face_hidden", True):
            _vg = GIRL_BY_ID.get(vid.get("girl_gid", ""))
            if _vg:
                # Virginity knowledge
                girl_learns_virgin(girl, _vg)
                # Act knowledge (she now knows vid_girl did this with the player)
                girl_learns_act(girl, _vg, vid_type, with_player=True)
                # BF knowledge (if video was marked as committed/cheating)
                if vid.get("committed", False):
                    girl_learns_has_bf(girl, _vg)
                    girl_learns_cheating(girl, _vg)

        _is_face_hidden = vid.get("face_hidden", True)

        # ── Priority 0: GF cheating gate ──
        # Skip breakup if the vid_girl was the player's GF when the video
        # was filmed — that's not cheating, it's an ex-GF video (handled later).
        # Also skip if face is hidden — she can't identify who's in the video.
        _vid_was_ex = _vid_snap(vid, "was_dating", False)
        if is_dating and subject == "other" and not _vid_was_ex and not _is_face_hidden:
            _other_gid = vid.get("girl_gid", "")
            _harem = getattr(girl, "harem_accepted", set()) or set()
            _is_poly = hasattr(girl, "has_trait") and girl.has_trait("polyamorous")
            _is_harem_ok = _other_gid in _harem
            if not _is_poly and not _is_harem_ok:
                _group_video_gf_cheating_breakup(girl, vid_type, group, vid=vid)
                return

        # ── Hostility check (per-girl): if viewer hates the vid_girl ──
        if subject == "other" and not _is_face_hidden:
            _vid_g_h = GIRL_BY_ID.get(vid.get("girl_gid", ""))
            if _vid_g_h:
                _like_val = int(girl.Girl_like.get(_vid_g_h.gid, 500)) if hasattr(girl, "Girl_like") else 500
                if _like_val < 250:
                    _hvn = _vid_g_h.Name
                    _hostile_solo = [
                        _tl(_("Ugh, WHY the fuck would I want to see %s like that?! Disgusting.")) % _hvn,
                        _tl(_("Oh GREAT, %s on camera. Just what nobody asked for.")) % _hvn,
                        _tl(_("Is that supposed to impress me? %s looks pathetic.")) % _hvn,
                        _tl(_("Wow. %s really has no shame, does she? Not surprised.")) % _hvn,
                        _tl(_("I could have gone my WHOLE life without seeing %s do that. Thanks for nothing.")) % _hvn,
                        _tl(_("Hah, that's %s's best? %s, you can do better than THAT.")) % (_hvn, Player.Name if hasattr(Player, "Name") else "Dude"),
                    ]
                    Say_Line(girl, _tl(_group_unique_choice(_hostile_solo)))
                    _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                    Change_Status(girl, "Obed", -2)
                    return

        # ── Non-consensual self: shock + stats + return ──
        if subject == "self" and not consensual:
            shock = _tl(_group_unique_choice(GROUP_VIDEO_NONCONSENSUAL_LINES))
            shock = _group_full_sub(shock, girl, vid, group)
            Say_Line(girl, shock)
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── Face hidden: self in GROUP — she pretends it's not her ──
        # She KNOWS it's her video, but revealing that in a group defeats the
        # purpose of hiding her face. She reacts like a bystander instead.
        if subject == "self" and _is_face_hidden and consensual:
            _fh_grp_self = [
                _("Wow, who IS that? Bold of you to share this here."),
                _("Haha, I can't even tell who that is. Pretty wild video though."),
                _("Okay... that's a lot for a group chat. Who is she?"),
                _("She hid her face, smart move. Whoever she is."),
            ]
            Say_Line(girl, _tl(_group_unique_choice(_fh_grp_self)))
            _fh_grp_trait = None
            _has_t_fh = hasattr(girl, "has_trait") and girl.has_trait
            if _has_t_fh:
                if _has_t_fh("lesbian") and vid_type != "masturbate":
                    _fh_grp_trait = _group_unique_choice([
                        _("That looks... intense. Not my thing, but whatever."),
                        _("With a guy? Interesting choice for her. Anyway."),
                    ])
                elif _has_t_fh("camera_lover"):
                    _fh_grp_trait = _group_unique_choice([
                        _("The angles are decent but without a face reveal, what's the point?"),
                        _("Honestly? The framing is good but no face makes it forgettable."),
                    ])
                elif _has_t_fh("camera_hater"):
                    _fh_grp_trait = _group_unique_choice([
                        _("Can we move on? I don't need to see some random girl like that."),
                        _("Why would anyone share this? Next topic."),
                    ])
                elif _has_t_fh("exhibitionist"):
                    _fh_grp_trait = _group_unique_choice([
                        _("I bet she enjoyed every second of it~ Too bad we can't see who she is."),
                        _("Whoever that is, she clearly knows how to put on a show~"),
                    ])
                elif _has_t_fh("public_shy"):
                    _fh_grp_trait = _group_unique_choice([
                        _("...that's someone's private moment. In a group chat. Cool."),
                        _("I really don't want to talk about this."),
                    ])
                elif _has_t_fh("cheater") and has_bf:
                    _fh_grp_trait = _group_unique_choice([
                        _("Whoever she is, at least she was smart about hiding her face."),
                        _("A hidden face video in a group... classic. Smart girl."),
                    ])
                elif _has_t_fh("loyal"):
                    _fh_grp_trait = _group_unique_choice([
                        _("I feel kind of bad for her, honestly. Even with the face hidden."),
                        _("That poor girl. I hope nobody figures out who she is."),
                    ])
                elif _has_t_fh("cute_sex"):
                    _fh_grp_trait = _group_unique_choice([
                        _("Oh my... that's, um... I can't even tell who that is. Wow."),
                        _("This is so embarrassing... for whoever she is."),
                    ])
                elif _has_t_fh("voyeur"):
                    _fh_grp_trait = _group_unique_choice([
                        _("Interesting video... can't tell who it is though."),
                    ])
            if _fh_grp_trait:
                Say_Line(girl, _fh_grp_trait)
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── Abandoned-partner self (group): pre-partner video in group chat ──
        if subject == "self" and getattr(girl, "_hc_was_abandoned", False) and _is_bf_context(girl) and not vid.get("committed", False):
            _ab_att = _abandoned_video_attitude(girl)
            _ab_vt = vid_type if vid_type != "doggy" else "cowgirl"
            _ab_pool = GROUP_VIDEO_ABANDONED_SELF_LINES.get((_ab_att, _ab_vt), GROUP_VIDEO_ABANDONED_SELF_LINES.get((_ab_att, "hj")))
            _ab_line = _format_partner_line(girl, _tl(_group_unique_choice(_ab_pool)))
            if _ab_att == "protective":
                set_scene_expression(girl, "angry")
                Change_Status(girl, "Love", -12)
                Change_Status(girl, "Obed", -5)
                provoke(girl, 2)
            elif _ab_att == "indifferent":
                set_scene_expression(girl, "looking_left")
                Change_Status(girl, "Inbt", 3)
                Change_Status(girl, "Love", -2)
            else:
                set_scene_expression(girl, "sly", blush=2)
                Change_Status(girl, "Inbt", 5)
                Change_Status(girl, "Lust", 3)
                Change_Status(girl, "Love", 1)
            Say_Line(girl, _ab_line)
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── Cuckold / Threesome video in group ──
        _is_cuckold_vid = vid.get("cuckold", False)
        _is_threesome_vid = vid.get("threesome", False)
        if _is_cuckold_vid or _is_threesome_vid:
            _recorder_gid = vid.get("recorder_gid", "")
            _has_t = hasattr(girl, "has_trait") and girl.has_trait
            _grp_members = group.get("members", [])

            _is_subject = (subject == "self")
            _is_recorder = (not _is_subject and _recorder_gid == girl.gid)

            if _is_cuckold_vid and _is_subject:
                # She's in the video, her BF was watching, shared in group (amplified shame)
                if _has_t and _has_t("camera_hater"):
                    _pool = GROUP_CUCKOLD_SELF_CAMERA_HATER
                    set_scene_expression(girl, "angry")
                    Change_Status(girl, "Love", -20)
                    Change_Status(girl, "Inbt", 12)
                    provoke(girl, 3)
                elif _has_t and _has_t("camera_lover"):
                    _pool = GROUP_CUCKOLD_SELF_CAMERA_LOVER
                    Change_Status(girl, "Lust", 4)
                    Change_Status(girl, "Inbt", 5)
                elif _has_t and (_has_t("cheater") or (hasattr(girl, "CheatAttitude") and girl.CheatAttitude >= 7)):
                    _pool = GROUP_CUCKOLD_SELF_CHEATER
                    set_scene_expression(girl, "sly", blush=2)
                    Change_Status(girl, "Lust", 6)
                    Change_Status(girl, "Obed", 4)
                elif _has_t and (_has_t("loyal") or (hasattr(girl, "CheatAttitude") and girl.CheatAttitude <= 3)):
                    _pool = GROUP_CUCKOLD_SELF_LOYAL
                    set_scene_expression(girl, "scared")
                    Change_Status(girl, "Love", -15)
                    Change_Status(girl, "Inbt", 10)
                else:
                    _pool = GROUP_CUCKOLD_SELF_DEFAULT
                    Change_Status(girl, "Love", -8)
                    Change_Status(girl, "Inbt", 7)
                Say_Line(girl, _group_full_sub(_tl(_group_unique_choice(_pool)), girl, vid, group))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

            elif _is_threesome_vid and _is_subject:
                # She's in the video, another girl recorded, shared in group
                if _has_t and (_has_t("camera_hater") or _has_t("public_shy")):
                    _pool = GROUP_THREESOME_SELF_SHY
                    set_scene_expression(girl, "embarrassed")
                    Change_Status(girl, "Inbt", 8)
                    Change_Status(girl, "Love", -5)
                elif _has_t and _has_t("exhibitionist"):
                    _pool = GROUP_THREESOME_SELF_EXHIBITIONIST
                    set_scene_expression(girl, "sly", blush=2)
                    Change_Status(girl, "Lust", 5)
                    Change_Status(girl, "Obed", 3)
                else:
                    _pool = GROUP_THREESOME_SELF_DEFAULT
                    Change_Status(girl, "Inbt", 5)
                    Change_Status(girl, "Love", -3)
                # Extra line if recorder is also in the group
                Say_Line(girl, _group_full_sub(_tl(_group_unique_choice(_pool)), girl, vid, group))
                if _recorder_gid in _grp_members:
                    _rec_girl = GIRL_BY_ID.get(_recorder_gid)
                    if _rec_girl:
                        _extra = _tl(_("And %s is RIGHT HERE reading this?!")) % _rec_girl.Name
                        Say_Line(girl, _tl(_extra))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

            elif _is_threesome_vid and _is_recorder:
                # She held the camera, everyone in group now knows
                if _has_t and _has_t("camera_lover"):
                    _pool = GROUP_THREESOME_RECORDER_CAMERA_LOVER
                    Change_Status(girl, "Lust", 4)
                    Change_Status(girl, "Obed", 2)
                elif _has_t and _has_t("camera_hater"):
                    _pool = GROUP_THREESOME_RECORDER_CAMERA_HATER
                    Change_Status(girl, "Love", -8)
                    Change_Status(girl, "Inbt", 6)
                else:
                    _pool = GROUP_THREESOME_RECORDER_DEFAULT
                    Change_Status(girl, "Love", -3)
                    Change_Status(girl, "Inbt", 3)
                Say_Line(girl, _group_full_sub(_tl(_group_unique_choice(_pool)), girl, vid, group))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

            else:
                # Uninvolved girl sees cuckold/threesome in group
                if _is_cuckold_vid:
                    _pool = GROUP_UNINVOLVED_CUCKOLD
                else:
                    _pool = GROUP_UNINVOLVED_THREESOME
                Change_Status(girl, "Inbt", 3)
                Say_Line(girl, _group_full_sub(_tl(_group_unique_choice(_pool)), girl, vid, group))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

        # ── SPECIAL: Virginity loss video (group) ──
        if vid.get("special") == "virginity" and not (subject == "other" and _is_face_hidden):
            _vid_girl_g = GIRL_BY_ID.get(vid.get("girl_gid", ""))
            _vid_name_g = _vid_girl_g.Name if _vid_girl_g else "her"
            _grp_m = group.get("members", [])
            _vid_in_group = vid.get("girl_gid") in _grp_m

            _has_t = hasattr(girl, "has_trait") and girl.has_trait
            _is_les_v = _has_t and _has_t("lesbian")
            if subject == "self":
                if _is_les_v:
                    _vl = _("Everyone in this chat just watched a lesbian lose her virginity to a MAN. My life is over.")
                elif _has_t("camera_lover"):
                    _vl = _("Everyone in this chat just watched me lose my virginity. You're welcome.")
                elif _has_t("camera_hater"):
                    _vl = _("You sent my FIRST TIME to the GROUP CHAT?! I'm going to kill you! EVERYONE can see this!")
                elif _has_t("cute_sex"):
                    _vl = _("Oh my god... everyone just saw me lose my virginity... I want to disappear...")
                elif _has_t("hardcore_sex"):
                    _vl = _("Yeah, that's me losing my virginity. And I'd do it again in front of all of you.")
                elif has_bf:
                    _plbl = girl.partner_label() if hasattr(girl, "partner_label") else "boyfriend"
                    _vl = _tl(_("My first time... sent to a group chat... while I have a %s. I'm so dead.")) % _plbl
                else:
                    _vl = _("You... you sent the video of my first time to EVERYONE?! This is so embarrassing!")
            else:
                _viewer_virgin = _has_t and _has_t("virgin")
                _vidg_les_vl = _vid_girl_g and hasattr(_vid_girl_g, "has_trait") and _vid_girl_g.has_trait("lesbian")
                if _viewer_virgin and _is_les_v:
                    _vl = _tl(_("%s lost her virginity to a GUY?! I'm a lesbian virgin and even I would never...")) % _vid_name_g
                elif _viewer_virgin:
                    _vl = _tl(_("%s lost her virginity?! On VIDEO?! I'm... I haven't even... oh my god.")) % _vid_name_g
                elif _vidg_les_vl:
                    _vl = _tl(_("%s the LESBIAN lost her virginity to a MAN?! And it's in our group chat?! WHAT?!")) % _vid_name_g
                elif _has_t("hardcore_sex"):
                    _vl = _tl(_("%s's first time? In a group chat? You're breaking her in and showing everyone. Respect.")) % _vid_name_g
                elif _has_t("cute_sex"):
                    _vl = _tl(_("That was %s's first time?! Why would you share something so personal with everyone?!")) % _vid_name_g
                elif _has_t("cum_slut"):
                    _vl = _tl(_("%s was a virgin?! And now everyone in this chat knows what she looks like getting fucked for the first time~")) % _vid_name_g
                elif _has_t("cheater") and has_bf:
                    _vl = _tl(_("%s lost her virginity to you... and you're sharing it with all of us. My boyfriend would never be this bold~")) % _vid_name_g
                elif _vid_in_group:
                    _vl = _tl(_("%s... your first time is in the group chat now. Are you okay with this?!")) % _vid_name_g
                else:
                    _vl = _tl(_("Wait... %s was a VIRGIN?! And you filmed it AND sent it to the group?! That's insane!")) % _vid_name_g

            Say_Line(girl, _vl)
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── Angry creampie reaction (group): she didn't want it ──
        if subject == "self" and vid_type == "creampie" and vid.get("reaction") == "angry":
            _has_t = hasattr(girl, "has_trait") and girl.has_trait
            _is_hate_cum = _has_t and girl.has_trait("hate_cum")
            _is_cam_lover = _has_t and girl.has_trait("camera_lover")

            # Find other girls in the group for name reference
            _grp_members = group.get("members", [])
            _other_gids = [gid for gid in _grp_members if gid != girl.gid]
            _other_name = None
            if _other_gids:
                _og = GIRL_BY_ID.get(_tl(_group_unique_choice(_other_gids)))
                if _og and hasattr(_og, "Name"):
                    _other_name = _og.Name

            if _is_hate_cum and _is_cam_lover:
                _angry_cream = [
                    _("The recording is amazing and the cum in my pussy looks so cinematic... BUT I TOLD YOU TO PULL OUT! A good film will not save your life next time."),
                    _("The footage is incredible but I said NO cum inside! Great camera work does not mean you get to ignore me!"),
                ]
            elif _is_hate_cum:
                _angry_cream = [
                    _("I told you to pull out! Seriously, DO NOT cum inside me again! It is dangerous!"),
                    _("Are you out of your mind?! I said pull out! And you sent this to the group?! Never again!"),
                ]
            elif _is_cam_lover:
                _angry_cream = [
                    _("Great footage, terrible decision. I said no cum inside. The fact that it looks good on film does not change that! And now the whole group saw it!"),
                    _("The recording is hot but I TOLD you to pull out! Now everyone in the group knows you came inside me!"),
                ]
            elif has_bf and _partner_in_group:
                _angry_cream = [
                    _("You came inside me AND sent it to the group?! My boyfriend is RIGHT HERE! He just SAW that!"),
                    _("I told you to pull out... and now my boyfriend just watched a creampie video of me. In real time."),
                ]
            elif has_bf:
                _angry_cream = [
                    _("Ugh! I told you not to cum inside! The sex was so good, but you should have pulled out... and now you shared this?! If my {hint}boyfriend{/hint} finds out..."),

                    _("You came inside me AND sent it to the group?! I have a {hint}boyfriend{/hint}! What is wrong with you?!"),

                ]
            else:
                _angry_cream = [
                    _("Ugh! I told you not to cum inside! The sex was so good, but you should have pulled out..."),
                    _("I said pull out! And now you sent this to the group?! Everyone can see you came inside me!"),
                ]

            # Add group-aware variant with other girl's name
            if _other_name:
                _angry_cream.append(
                    _tl(_("UGH! I told you to pull out! Now %s will think I am letting you cum inside me!")) % _other_name
                )

            Say_Line(girl, _tl(_group_unique_choice(_angry_cream)))
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── ATM video reaction (group): video has "atm" flag ──
        if vid.get("atm", False) and not (subject == "other" and _is_face_hidden):
            _atm_pool = video_atm_pool(girl, subject, True)
            if _atm_pool:
                _atm_line = _tl(_group_unique_choice(_atm_pool))
                _atm_line = _group_full_sub(_atm_line, girl, vid, group)
                Say_Line(girl, _atm_line)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

        # ── Anal creampie video reaction (group): creampie from anal scene ──
        if vid_type == "creampie" and vid.get("anal_creampie", False) and not (subject == "other" and _is_face_hidden):
            _ac_pool = video_group_table_pool(GROUP_VIDEO_ANAL_CREAMPIE_LINES, subject, True)
            if _ac_pool:
                _ac_line = _tl(_group_unique_choice(_ac_pool))
                _ac_line = _group_full_sub(_ac_line, girl, vid, group)
                Say_Line(girl, _ac_line)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

        # ── Virgin-watches-virgin shock (group): BOTH girls are virgins ──
        # Higher priority than normal virgin shock. The viewer is also a virgin
        # and is shocked/conflicted seeing another virgin doing sexual acts.
        # Blocked when face_hidden — can't identify who it is
        _gv_covered = getattr(store, "_gv_virgin_shock_covered", set())
        if subject == "other" and girl.gid not in _gv_covered and not _is_face_hidden:
            _vid_girl = GIRL_BY_ID.get(vid.get("girl_gid", ""))
            _viewer_is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
            _viewer_is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
            _vidg_is_les = _vid_girl and hasattr(_vid_girl, "has_trait") and _vid_girl.has_trait("lesbian")

            # Lesbian viewer watching virgin's video: skip hetero-curious convos
            if _vid_girl and _viewer_is_virgin and _viewer_is_les and _vid_girl.gid not in _gv_covered and check_virgin_shock(girl, _vid_girl):
                _vn = _vid_girl.Name
                _vid_in_group = _vid_girl.gid in group.get("members", [])
                _pn = Player.Name if hasattr(Player, "Name") else "him"

                if vid_type in ("cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "creampie", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
                    if _vid_in_group and _vidg_is_les:
                        _convos = [
                            [
                                (girl, _("{vn}... you did THAT?! With a MAN?! We're both gay!")),
                                (_vid_girl, _("I know! I KNOW! Don't remind me! It just... happened!")),
                                (girl, _("How does sex with a man 'just happen' to a LESBIAN?!")),
                                (_vid_girl, _("Stop! I'm already dying inside! {pn}, WHY did you share this?!")),
                            ],
                        ]
                    elif _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn}... you actually slept with him? Straight girls really do just go for it, huh.")),
                                (_vid_girl, _("Don't say it like that! It wasn't some casual decision!")),
                                (girl, _("I'm not judging! It's just... a man? Inside you? I could never.")),
                                (_vid_girl, _("Well nobody asked you to! And {pn}, DELETE THIS!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} went all the way with a guy... I'd never let a man touch me like that.")),
                            ],
                        ]
                elif vid_type in ("bj", "tj", "hj"):
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn}... you're doing THAT with {pn}? Voluntarily?")),
                                (_vid_girl, _("Yes! It's not that weird! Not everyone shares your preferences!")),
                                (girl, _("I know! I just... a man's body? I don't get the appeal.")),
                                (_vid_girl, _("You don't HAVE to get it! Just stop staring at the video!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("She's doing that with a guy... I don't understand straight girls at all.")),
                            ],
                        ]
                else:
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn} touching herself... okay, THAT I understand.")),
                                (_vid_girl, _("Can you NOT comment on this?! It's private!")),
                            ],
                        ]
                    else:
                        _convos = [[(girl, _("{vn} doing that... at least there's no guy involved."))]]

                _picked = _group_unique_choice(_convos)
                for _speaker, _raw in _picked:
                    _translated = _tl(_raw).replace("{vn}", _vn).replace("{pn}", _pn)
                    Say_Line(_speaker, _translated)
                Change_Status(girl, "Obed", 6)
                Change_Status(girl, "Inbt", 8)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                _covered = getattr(store, "_gv_virgin_shock_covered", set())
                _covered.add(girl.gid)
                if _vid_in_group:
                    _covered.add(_vid_girl.gid)
                store._gv_virgin_shock_covered = _covered
                return

            if _vid_girl and _viewer_is_virgin and _vid_girl.gid not in _gv_covered and check_virgin_shock(girl, _vid_girl):
                _vn = _vid_girl.Name
                _vid_in_group = _vid_girl.gid in group.get("members", [])
                _pn = Player.Name if hasattr(Player, "Name") else "him"

                if vid_type in ("cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "creampie", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
                    _obed_gain = 15
                    _inbt_gain = 20
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn}... you actually DID it?! We BOTH said we were waiting!")),
                                (_vid_girl, _("I know! I know! It just... he was so... I couldn't say no...")),
                                (girl, _("I can't believe you went all the way before me... I feel so... behind now.")),
                                (_vid_girl, _("Don't say it like that! And don't watch it anymore! {pn}, WHY?!")),
                            ],
                            [
                                (girl, _("You LOST it?! {vn}, we made a PACT! We said we'd both wait!")),
                                (_vid_girl, _("I'M SORRY! I didn't plan it! One thing led to another and...")),
                                (girl, _("And now it's in the group chat and I'm the only virgin left. GREAT.")),
                                (_vid_girl, _("You're making me feel so guilty... it just felt so good I couldn't stop...")),
                            ],
                            [
                                (girl, _("Wait... that's... {vn} is having sex. ACTUAL sex. And I'm watching this as a virgin.")),
                                (_vid_girl, _("Please stop... I can explain...")),
                                (girl, _("Is it... is it really that good? You look like... never mind. I can't believe this.")),
                                (_vid_girl, _("It IS... I mean... this is NOT the time for this conversation! {pn}, delete this NOW!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} lost her virginity before me... and now everyone can see it.")),
                                (girl, _("We said we'd both wait... and she just... I don't know how to feel about this.")),
                            ],
                            [
                                (girl, _("She actually did it... the girl who swore she was waiting just like me.")),
                                (girl, _("And now I'm sitting here watching it wondering what it feels like... this is messed up.")),
                            ],
                        ]
                elif vid_type in ("bj", "tj", "hj"):
                    _obed_gain = 10
                    _inbt_gain = 12
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn}?! You're doing... THAT?! We're both supposed to be innocent!")),
                                (_vid_girl, _("I AM innocent! This doesn't count! It's not... you know... actual sex!")),
                                (girl, _("Not count?! I've never even done THAT and you're acting like it's nothing!")),
                                (_vid_girl, _("It IS nothing! I mean... it's something but... ugh, stop judging me!")),
                            ],
                            [
                                (girl, _("I can't believe I'm watching {vn} do this... I haven't even held a guy's hand and she's...")),
                                (_vid_girl, _("It's not as big of a deal as you think! I'm still a virgin!")),
                                (girl, _("You keep saying that but... is it really that easy to just... do stuff?")),
                                (_vid_girl, _("Can we PLEASE not have this conversation in the GROUP CHAT?! {pn}, I'm going to kill you!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} is doing THAT... and I've never even tried...")),
                                (girl, _("She said she was just as innocent as me. Apparently not.")),
                            ],
                        ]
                else:
                    _obed_gain = 6
                    _inbt_gain = 8
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn}... is that... are you... I would NEVER do something like that!")),
                                (_vid_girl, _("Relax, it's completely normal! Every girl does it!")),
                                (girl, _("I DON'T! I've never... okay, HOW does that even work? Not that I want to know!")),
                                (_vid_girl, _("You literally just asked! And {pn}, I'm going to kill you for this!")),
                            ],
                            [
                                (girl, _("{vn}?! You touch yourself?! I could NEVER. I'm too innocent for that.")),
                                (_vid_girl, _("Sure you are. That's what everyone says until they try it.")),
                                (girl, _("I haven't tried it! I wouldn't even know where to... I mean... does it really feel that good?")),
                                (_vid_girl, _("Are you seriously asking me this in the GROUP CHAT?! {pn}, this is YOUR fault!")),
                            ],
                            [
                                (girl, _("Wait... {vn} does THAT?! But we're both... I would never... that's so private...")),
                                (_vid_girl, _("It IS private! That's why this video shouldn't be here! And yes, it's NORMAL!")),
                                (girl, _("Is it...? I've always wondered but... no. I definitely haven't wondered about it. Ever.")),
                                (_vid_girl, _("You're the worst liar ever. {pn}, congratulations, you've corrupted us both!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} does that...? I would never, obviously. But she seems to really... no. Not thinking about this.")),
                            ],
                            [
                                (girl, _("{vn} touches herself...? She's supposed to be as innocent as me... unless... no. I definitely don't do that. Ever.")),
                            ],
                        ]

                _picked = _group_unique_choice(_convos)
                for _speaker, _raw in _picked:
                    _translated = _tl(_raw).replace("{vn}", _vn).replace("{pn}", _pn)
                    Say_Line(_speaker, _translated)
                Change_Status(girl, "Obed", _obed_gain)
                Change_Status(girl, "Inbt", _inbt_gain)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                _covered = getattr(store, "_gv_virgin_shock_covered", set())
                _covered.add(girl.gid)
                if _vid_in_group:
                    _covered.add(_vid_girl.gid)
                store._gv_virgin_shock_covered = _covered
                return

        # ── Virgin shock (group): viewer thought the girl was a virgin ──
        # This is the per-girl fallback. Produces alternating messages when
        # the vid_girl is also in the group, otherwise a single shocked line.
        # Only fires ONCE per video send (checked via _gv_virgin_shock_covered).
        if subject == "other" and girl.gid not in _gv_covered and not _is_face_hidden:
            _vid_girl = GIRL_BY_ID.get(vid.get("girl_gid", ""))
            if _vid_girl and _vid_girl.gid not in _gv_covered and check_virgin_shock(girl, _vid_girl):
                _vn = _vid_girl.Name
                _vid_in_group = _vid_girl.gid in group.get("members", [])
                _pn = Player.Name if hasattr(Player, "Name") else "him"
                _vdg_les = hasattr(_vid_girl, "has_trait") and _vid_girl.has_trait("lesbian")

                # Lesbian vid_girl: shock is about her being with a man, not just losing virginity
                if _vdg_les and vid_type in ("cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "creampie", "bj", "tj", "hj", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
                    _obed_gain = 12
                    _inbt_gain = 15
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("Wait... {vn}?! With a GUY?! She told me she was a lesbian AND a virgin!")),
                                (_vid_girl, _("I AM a lesbian! This doesn't... it doesn't change who I am!")),
                                (girl, _("Girl, you're literally on video doing THAT with {pn}! Explain!")),
                                (_vid_girl, _("There's nothing to explain! It happened! I didn't plan it! {pn}, why would you send this?!")),
                            ],
                            [
                                (girl, _("Hold on... {vn} the LESBIAN VIRGIN is doing... THAT?! With a MAN?!")),
                                (_vid_girl, _("Stop saying it like that! You're making it sound worse than it is!")),
                                (girl, _("How can I make it sound WORSE? You literally said you'd never touch a man!")),
                                (_vid_girl, _("WELL THINGS CHANGE OKAY?! No they don't! This was a mistake! Delete it!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} is doing THAT with a guy?! The LESBIAN?! The girl who said she'd never...?!")),
                                (girl, _("I'm genuinely shocked. She was a virgin AND gay and now... this is in our group chat.")),
                            ],
                        ]
                    _picked = _group_unique_choice(_convos)
                    for _speaker, _raw in _picked:
                        _translated = _tl(_raw).replace("{vn}", _vn).replace("{pn}", _pn)
                        Say_Line(_speaker, _translated)
                    Change_Status(girl, "Obed", _obed_gain)
                    Change_Status(girl, "Inbt", _inbt_gain)
                    _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                    _covered = getattr(store, "_gv_virgin_shock_covered", set())
                    _covered.add(girl.gid)
                    if _vid_in_group:
                        _covered.add(_vid_girl.gid)
                    store._gv_virgin_shock_covered = _covered
                    return

                if vid_type in ("cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "creampie", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
                    _obed_gain = 12
                    _inbt_gain = 15
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("WAIT. {vn}?! You're having SEX?! You told me you were a VIRGIN!")),
                                (_vid_girl, _("I... it just HAPPENED okay?! I wasn't planning on it!")),
                                (girl, _("Girl, you are literally getting RAILED on camera! That doesn't 'just happen'!")),
                                (_vid_girl, _("Stop watching it!! Oh my god... {pn}, why would you send this here?!")),
                            ],
                            [
                                (girl, _("Is that... {vn}?! On top of him?! The VIRGIN {vn}?!")),
                                (_vid_girl, _("Please... please stop looking at it... I can explain...")),
                                (girl, _("Explain WHAT?! You said you'd never done it and now you're riding him like that?!")),
                                (_vid_girl, _("It was my first time! I lost control! {pn}, I'm going to KILL you for sending this!")),
                            ],
                            [
                                (girl, _("Oh my GOD. {vn}... you lost your virginity?! And it's on VIDEO?!")),
                                (_vid_girl, _("Don't say it out loud!! It was supposed to be private!")),
                                (girl, _("Private?! It's in our GROUP CHAT! So all that 'saving myself' talk was just...")),
                                (_vid_girl, _("It WAS real! I just... he made me feel things and I couldn't stop... ugh, I hate you both!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("WAIT. {vn} is having SEX?! She told me she was a VIRGIN!")),
                                (girl, _("The 'innocent' girl is getting railed... I can NOT believe what I'm seeing right now.")),
                            ],
                        ]
                elif vid_type in ("bj", "tj", "hj"):
                    _obed_gain = 8
                    _inbt_gain = 10
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("Hold on... {vn}?! The VIRGIN?! Doing THAT?!")),
                                (_vid_girl, _("It's not what you think! That doesn't count as... you know...")),
                                (girl, _("Doesn't COUNT?! Girl, his dick is in your mouth! What exactly is your definition?!")),
                                (_vid_girl, _("I'm still a virgin! That's just... different! Stop looking at me like that!")),
                            ],
                            [
                                (girl, _("Wait... the girl who said 'I've never done anything' is doing THIS to {pn}?!")),
                                (_vid_girl, _("I said I was a virgin, not that I've never... ugh, this is so embarrassing!")),
                                (girl, _("So you draw the line at penetration but everything else is fair game? Interesting~")),
                                (_vid_girl, _("STOP analyzing it! It was just one time! {pn}, you're DEAD for sending this!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("Wait... {vn} is doing THAT?! She told me she was a virgin!")),
                                (girl, _("The 'pure innocent' act is officially over. The group chat doesn't lie.")),
                            ],
                        ]
                else:
                    _obed_gain = 5
                    _inbt_gain = 6
                    if _vid_in_group:
                        _convos = [
                            [
                                (girl, _("{vn} touching herself on camera?! The VIRGIN?!")),
                                (_vid_girl, _("That's PRIVATE! Why would you send that here?! I'm still a virgin, that was just... personal!")),
                                (girl, _("Okay technically yes, but the 'innocent' image? Gone. Everyone here saw that.")),
                                (_vid_girl, _("It doesn't mean anything! I was just... curious! {pn}, I trusted you!")),
                            ],
                        ]
                    else:
                        _convos = [
                            [
                                (girl, _("{vn} touching herself?! The virgin?! Well, she's not as innocent as she told us.")),
                            ],
                        ]

                _picked = _group_unique_choice(_convos)
                for _speaker, _raw in _picked:
                    _translated = _tl(_raw).replace("{vn}", _vn).replace("{pn}", _pn)
                    Say_Line(_speaker, _translated)
                Change_Status(girl, "Obed", _obed_gain)
                Change_Status(girl, "Inbt", _inbt_gain)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                # Mark both girls as covered — only 1 virgin shock convo per send
                _covered = getattr(store, "_gv_virgin_shock_covered", set())
                _covered.add(girl.gid)
                if _vid_in_group:
                    _covered.add(_vid_girl.gid)
                store._gv_virgin_shock_covered = _covered
                return

        # ── Priority 0.5: Video girl is IN the group chat — direct address ──
        if not (subject == "other" and _is_face_hidden):
            _gp_main, _gp_followup, _gp_followup_girl = _pick_group_video_girl_present(girl, vid, group)
            if _gp_main:
                Say_Line(girl, _gp_main)
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                if _gp_followup and _gp_followup_girl:
                    Say_Line(_gp_followup_girl, _gp_followup)
                return

        # ── Ex-girlfriend snapshot: vid was filmed when vid_girl dated the player ──
        _vid_was_dating = _vid_snap(vid, "was_dating", False)
        if _vid_was_dating:
            _vid_gid_ex = vid.get("girl_gid", "")
            _vid_g_ex = GIRL_BY_ID.get(_vid_gid_ex)
            _ex_still_dating = _vid_g_ex and hasattr(_vid_g_ex, "is_dating_player") and _vid_g_ex.is_dating_player() if _vid_g_ex else False

            if not _ex_still_dating:
                _pn = Player.Name if hasattr(Player, "Name") else "him"
                _vid_in_grp = _vid_gid_ex in group.get("members", [])

                if subject == "self":
                    # Girl sees her OWN ex-video in the group
                    if _vid_in_grp:
                        _ex_self_group = [
                            _tl(_("This is from when %s and I were still together... and now everyone here is seeing it.")) % _pn,
                            _("We were dating when this happened. We're NOT together anymore. Why is this in the group chat?!"),
                            _tl(_("Oh great. A video from when I was his girlfriend. In the GROUP. Thanks for nothing, %s.")) % _pn,
                        ]
                    else:
                        _ex_self_group = [
                            _("That video is old. We were together back then. We're not anymore. Drop it."),
                            _("This was from when we were dating... why are you sending this around?"),
                        ]
                    Say_Line(girl, _tl(_group_unique_choice(_ex_self_group)))
                    Change_Status(girl, "Love", -5)
                    Change_Status(girl, "Obed", 5)
                    _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                    return

                elif subject == "other" and _vid_g_ex and not _is_face_hidden:
                    _vn = _vid_g_ex.Name
                    if is_dating:
                        # Current GF sees ex-GF video in group
                        _ex_gf_grp = [
                            _tl(_("He kept a video of his ex %s?! And sent it to the GROUP?! What is he trying to prove?!")) % _vn,
                            _tl(_("Wait... %s was his girlfriend when this was filmed? And he's sharing it with ALL of us?!")) % _vn,
                            _tl(_("So %s dated %s, they broke up, and now he's sending her video here? That's SO messed up.")) % (_vn, _pn),
                        ]
                        Say_Line(girl, _tl(_group_unique_choice(_ex_gf_grp)))
                        # If vid_girl is in group, she reacts
                        if _vid_in_grp:
                            _ex_caught_grp = [
                                _("Can you NOT?! That was private! We were together and now you're humiliating me in front of everyone!"),
                                _("Are you serious right now?! Sending THAT here?! We broke up and this is what you do?!"),
                                _("I trusted you with that video when we were dating! And now the whole group sees it?!"),
                            ]
                            Say_Line(_vid_g_ex, _tl(_group_unique_choice(_ex_caught_grp)))
                        Change_Status(girl, "Love", -8)
                        Change_Status(girl, "Obed", -3)
                    else:
                        # Non-GF viewer sees ex-GF video in group
                        _ex_other_grp = [
                            _tl(_("Wait... wasn't %s his girlfriend? And now he's sending her video to the group? Damn.")) % _vn,
                            _tl(_("This is from when %s and %s were together? He really has no boundaries.")) % (_vn, _pn),
                            _tl(_("So %s filmed his ex %s... and now we're all watching it. Classy.")) % (_pn, _vn),
                        ]
                        Say_Line(girl, _tl(_group_unique_choice(_ex_other_grp)))
                        if _vid_in_grp:
                            _ex_caught_grp2 = [
                                _("STOP! We were DATING! That was between us! Why is this in the group?!"),
                                _("Oh my god... everyone here is watching a video from when I was his girlfriend... I want to disappear."),
                            ]
                            Say_Line(_vid_g_ex, _tl(_group_unique_choice(_ex_caught_grp2)))
                        Change_Status(girl, "Inbt", 5)
                        Change_Status(girl, "Obed", 3)
                    _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                    return

        # ── Ex-viewer: this girl is the player's ex ──
        _is_ex = hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player()
        if _is_ex and subject == "other" and not _is_face_hidden:
            _ex_key = ("other",)
            _ex_lines = GROUP_VIDEO_EX_VIEWER_LINES.get(_ex_key)
            if _ex_lines:
                Say_Line(girl, _tl(_group_unique_choice(_ex_lines)))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return
        elif _is_ex and subject == "self":
            _ex_key = ("self",)
            _ex_lines = GROUP_VIDEO_EX_VIEWER_LINES.get(_ex_key)
            if _ex_lines:
                Say_Line(girl, _tl(_group_unique_choice(_ex_lines)))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

        # ── Video is of player's GF: 3rd girl uses neutral lines (no suggestive) ──
        _vid_of_gf = vid and _video_is_of_player_gf(vid)
        if _vid_of_gf and subject == "other" and not is_dating and not _is_face_hidden:
            _neutral_pool = GROUP_VIDEO_OF_GF_NEUTRAL_LINES.get(vid_type) or GROUP_VIDEO_OF_GF_NEUTRAL_LINES.get("_default", [])
            if _neutral_pool:
                Say_Line(girl, _tl(_group_unique_choice(_neutral_pool)))
                _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                return

        # ── Cheating exposure panic: her video in group while she has BF/GF ──
        if subject == "self" and has_bf and not is_dating:
            _tier = _GROUP_VIDEO_SEVERITY_TIER.get(vid_type, 1)
            if _tier >= 2:
                _is_ch = hasattr(girl, "has_trait") and girl.has_trait("cheater")
                _pool_key = "cheater" if _is_ch else "panic"
                if _partner_in_group:
                    _gv_ntr_npc = get_npc_partner_for(girl)
                    _gv_ntr_known = _ntr_active_discovered(girl) and _gv_ntr_npc is not None
                    if _gv_ntr_known:
                        _lines = GROUP_VIDEO_NTR_KNOWN_BF_WATCHING.get(_ntr_video_ctx(_gv_ntr_npc), {}).get(_pool_key, [])
                    else:
                        _lines = GROUP_VIDEO_CHEATING_BF_WATCHING.get(_pool_key, [])
                    print("[GROUP_VIDEO] partner in group: ntr_known=%s pool=%s" % (_gv_ntr_known, _pool_key))
                    if _lines:
                        _panic_line = _format_partner_line(girl, _tl(_group_unique_choice(_lines)))
                        Say_Line(girl, _panic_line)
                        _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                        debug_log("[GROUP_VIDEO] Cheating BF-watching panic for %s, vid=%s" % (girl.gid, vid_type))
                        return
                else:
                    _panic_pool = GROUP_VIDEO_CHEATING_SELF_PANIC.get(vid_type)
                    if _panic_pool:
                        _lines = _panic_pool.get(_pool_key, [])
                        if _lines:
                            _panic_line = _format_partner_line(girl, _tl(_group_unique_choice(_lines)))
                            Say_Line(girl, _panic_line)
                            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
                            _loc_line = _pick_group_video_location_line(girl, vid)
                            if _loc_line:
                                _loc_line = _group_full_sub(_loc_line, girl, vid, group)
                                Say_Line(girl, _loc_line)
                            debug_log("[GROUP_VIDEO] Cheating exposure panic fired for %s, vid=%s, tier=%d" % (girl.gid, vid_type, _tier))
                            return

        # ── Face hidden "other" in group: can't identify, comment on anonymity ──
        if subject == "other" and _is_face_hidden:
            _fh_grp_other_trait = None
            _has_t_fho = hasattr(girl, "has_trait") and girl.has_trait
            if _has_t_fho:
                if _has_t_fho("camera_lover"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("No face in the shot? Terrible camera work. You completely wasted the best part of the video."),
                        _("A face-hidden video in the group chat? No personality, no expressions. Boring."),
                        _("Who films someone and doesn't get their face? The angle is all wrong. Amateur work."),
                    ])
                elif _has_t_fho("camera_hater"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("At least she was smart about it. Hidden face in a group chat is the only right move."),
                        _("Good for her, hiding her face. At least someone understands how dangerous cameras are."),
                        _("She hid her face. Smart. If only more people did that before letting someone film them."),
                    ])
                elif _has_t_fho("exhibitionist"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("Hidden face? In the group? What a waste. If you're going to be on video, OWN it."),
                        _("She's hiding her face from the group? That's so boring. Show yourself."),
                        _("Anonymous video shared with everyone? Coward move. If that were me I'd want the group to KNOW."),
                    ])
                elif _has_t_fho("public_shy"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("She hid her face... that's the smartest decision anyone in this group has ever made."),
                        _("Good. Her face is hidden. If that were me I'd want exactly the same thing. Or better, no video at all."),
                        _("At least she protected herself. A video in a group chat with her face showing? Nightmare."),
                    ])
                elif _has_t_fho("voyeur"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("Face hidden makes it more mysterious... I'm watching this differently, studying the body language."),
                        _("I can't identify her, but I can still watch. The anonymity makes it feel like a different kind of experience."),
                        _("Without the face, the group is focused on the act itself. Which is... honestly more interesting to watch."),
                    ])
                elif _has_t_fho("hardcore_sex"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("Face hidden doesn't matter. You can still see how hard she was taking it. That's what counts."),
                        _("Who cares about the face? The group can see the intensity just fine without it."),
                    ])
                elif _has_t_fho("cute_sex"):
                    _fh_grp_other_trait = _group_unique_choice([
                        _("She felt like she had to hide her face from the group... that's sad. I hope she's okay."),
                        _("Poor girl, hiding her face in a group video... she must have been so nervous about being recognized."),
                    ])
                elif _has_t_fho("lesbian") and vid_type != "masturbate":
                    _fh_grp_other_trait = _group_unique_choice([
                        _("Face hidden... maybe she has the same reasons I would for not wanting proof with a man."),
                        _("Smart to hide her face. If she's anything like me, she doesn't want evidence of this."),
                    ])
            if _fh_grp_other_trait:
                _fh_grp_other_trait = _group_full_sub(_fh_grp_other_trait, girl, vid, group)
                Say_Line(girl, _fh_grp_other_trait)
            else:
                _fh_grp_other = [
                    _("Her face is hidden... who is that? Could be anyone."),
                    _("Can't see her face. Is this supposed to be someone we know?"),
                    _("She's hiding her face. Smart, I guess, but now I'm curious who it is."),
                    _("Anonymous video? Her face is completely hidden. Interesting."),
                ]
                Say_Line(girl, _tl(_group_unique_choice(_fh_grp_other)))
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            return

        # ── Priority 1: Full combined reaction (other + other_girl has BF) ──
        full_line = _pick_group_full_video_reaction(girl, vid, group)
        if full_line:
            full_line = _group_full_sub(full_line, girl, vid, group)
            Say_Line(girl, full_line)
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            # Follow-up: BF viewer > self-aware
            _bf_followup = _pick_group_video_bf_viewer_followup(girl, vid, group)
            if _bf_followup:
                _bf_followup = _group_full_sub(_bf_followup, girl, vid, group)
                Say_Line(girl, _bf_followup)
            else:
                _trait_followup = _pick_group_video_trait_line(girl, subject, vid_type, vid=vid)
                if _trait_followup:
                    _trait_followup = _group_full_sub(_trait_followup, girl, vid, group)
                    Say_Line(girl, _trait_followup)
            return

        # ── Priority 2: Blended line (context + trait + type) ──
        line = _pick_group_video_blended_line(girl, subject, vid_type, vid=vid)
        if line:
            line = _group_full_sub(line, girl, vid, group)
            Say_Line(girl, line)
            if is_dating and subject == "other":
                pass  # stats handled in _apply_group_video_stats
            _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)
            # Follow-up: BF viewer > location
            _bf_followup = _pick_group_video_bf_viewer_followup(girl, vid, group)
            if _bf_followup:
                _bf_followup = _group_full_sub(_bf_followup, girl, vid, group)
                Say_Line(girl, _bf_followup)
            else:
                _loc_line = _pick_group_video_location_line(girl, vid)
                if _loc_line:
                    _loc_line = _group_full_sub(_loc_line, girl, vid, group)
                    Say_Line(girl, _loc_line)
            return

        # ── Priority 3: Layered fallback ──
        # Step 1: Context line (dating / player-GF / BF)
        ctx_line = None
        if is_dating:
            ctx_line = _pick_group_video_dating_line(girl, subject, vid_type, vid=vid)
        if not ctx_line:
            ctx_line = _pick_group_video_player_gf_line(girl, subject, vid_type, vid=vid)
        if not ctx_line and has_bf:
            ctx_line = _pick_group_video_bf_line(girl, subject, vid_type, partner_in_group=_partner_in_group)

        # Step 2: Trait line (combo > single > base subject)
        trait_line = _pick_group_video_combo_line(girl, subject, vid_type, vid=vid)
        if not trait_line:
            trait_line = _pick_group_video_trait_line(girl, subject, vid_type, vid=vid)

        # Step 3: Say what we got — max 2 lines
        if ctx_line and trait_line:
            trait_line = _group_full_sub(trait_line, girl, vid, group)
            ctx_line = _format_partner_line(girl, _group_full_sub(ctx_line, girl, vid, group))
            Say_Line(girl, trait_line)
            Say_Line(girl, ctx_line)
        elif trait_line:
            trait_line = _group_full_sub(trait_line, girl, vid, group)
            Say_Line(girl, trait_line)
        elif ctx_line:
            ctx_line = _format_partner_line(girl, _group_full_sub(ctx_line, girl, vid, group))
            Say_Line(girl, ctx_line)
        else:
            # Pure fallback: base subject line (group versions)
            _base_line = None
            if subject == "self":
                _vcount = girl_type_count(girl, vid_type)
                if _vcount == 0 and vid_type in GROUP_VIDEO_SELF_FIRST_LINES:
                    _base_line = _group_unique_choice(GROUP_VIDEO_SELF_FIRST_LINES[vid_type])
                elif _vcount >= 5 and vid_type in GROUP_VIDEO_SELF_VETERAN_LINES:
                    _base_line = _group_unique_choice(GROUP_VIDEO_SELF_VETERAN_LINES[vid_type])
                else:
                    pool = GROUP_VIDEO_SELF_LINES
                    _base_line = _group_unique_choice(pool.get(vid_type, [_("I... I don't even know what to say.")]))
            else:
                pool = GROUP_VIDEO_OTHER_LINES
                _base_line = _group_unique_choice(pool.get(vid_type, [_("I... I don't even know what to say.")]))
            if _base_line:
                _base_line = _group_full_sub(_base_line, girl, vid, group)
                Say_Line(girl, _base_line)

        _apply_group_video_stats(girl, subject, vid_type, has_bf, consensual, group, vid)

        # One follow-up max: BF viewer > other girl BF > self-aware > location
        _bf_followup = _pick_group_video_bf_viewer_followup(girl, vid, group)
        if _bf_followup:
            _bf_followup = _group_full_sub(_bf_followup, girl, vid, group)
            Say_Line(girl, _bf_followup)
        elif subject == "other":
            _ogbf = _pick_group_video_other_girl_bf_lines(girl, vid, group)
            if _ogbf:
                _ogbf = _group_full_sub(_ogbf, girl, vid, group)
                Say_Line(girl, _ogbf)
            else:
                _aware = _pick_group_video_self_aware_followup(girl, vid)
                if _aware:
                    _aware = _group_full_sub(_aware, girl, vid, group)
                    Say_Line(girl, _aware)
        elif subject == "self":
            _loc_line = _pick_group_video_location_line(girl, vid)
            if _loc_line:
                _loc_line = _group_full_sub(_loc_line, girl, vid, group)
                Say_Line(girl, _loc_line)

        _condom_line = _pick_video_condom_followup(girl, vid, subject)
        if _condom_line:
            Say_Line(girl, _condom_line)

    # ==========================================================
    # SCRIPTED GROUP VIDEO CONVERSATIONS
    # One-time multi-message exchanges between girls with specific
    # trait combos. Each fires only once per playthrough.
    # Returns list of (gid, text) tuples or None.
    # ==========================================================

    def _gv_claims_birth_control(girl):
        """She can say she relies on birth control: the "on_pill" claim of the fertility truth filter
        (pregnancy.rpy, what SHE believes: a placebo counts), with pregnancy in the game, and never once
        she knows she is pregnant."""
        return (store._pregnancy_mode != "off"
                and not (getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False))
                and _FERT_CLAIMS["on_pill"][0](girl))

    def _try_scripted_group_video(vid, group):
        """Check if a scripted multi-message conversation should fire.
        Returns list of (gid, text) tuples or None.
        Each scenario fires only once per run."""
        vid_type = vid.get("type", "hj")
        vid_gid = vid.get("girl_gid", "")
        if vid.get("face_hidden", True):
            return None
        members = group.get("members", [])
        if len(members) != 2:
            return None

        girl_a = GIRL_BY_ID.get(members[0])
        girl_b = GIRL_BY_ID.get(members[1])
        if not girl_a or not girl_b:
            return None
        if not hasattr(girl_a, "has_trait") or not hasattr(girl_b, "has_trait"):
            return None
        if girl_is_away(girl_a) or girl_is_away(girl_b):
            return None   # a two-girl scripted conversation needs both: fall back to per-girl reactions

        pname = Player.Name if hasattr(Player, "Name") else "him"
        seen = store._scripted_group_convos_seen
        consensual = vid.get("consensual", True)
        vid_girl = GIRL_BY_ID.get(vid_gid)

        # ── Helper: check virgin or was-virgin ──
        def _is_virgin_or_was(g):
            return (hasattr(g, "has_trait") and g.has_trait("virgin")) or getattr(g, "virginity_taken_by_player", False)

        # ── Helper: find trait pair ──
        _pair_traits = [None, None]   # [trait_pos, trait_neg] from latest _pair call
        def _pair(trait_pos, trait_neg):
            _pair_traits[0] = trait_pos
            _pair_traits[1] = trait_neg
            if girl_a.has_trait(trait_pos) and girl_b.has_trait(trait_neg):
                return girl_a, girl_b
            if girl_b.has_trait(trait_pos) and girl_a.has_trait(trait_neg):
                return girl_b, girl_a
            return None, None

        def _fire(key, msgs, girl_self, girl_other, traits_self=None, traits_other=None):
            if key in seen:
                return None
            seen.add(key)
            subj_self = "self" if vid_gid == girl_self.gid else "other"
            subj_other = "self" if vid_gid == girl_other.gid else "other"
            _apply_group_video_stats(girl_self, subj_self, vid_type, _is_bf_context(girl_self), consensual, group, vid)
            _apply_group_video_stats(girl_other, subj_other, vid_type, _is_bf_context(girl_other), consensual, group, vid)
            # Discover traits revealed by the conversation
            # Use explicit traits if provided, otherwise auto-detect from _pair
            _ts = traits_self
            _to = traits_other
            if not _ts and not _to and _pair_traits[0] and _pair_traits[1]:
                # Map _pair traits to girl_self/girl_other
                _tp, _tn = _pair_traits
                if hasattr(girl_self, "has_trait"):
                    if girl_self.has_trait(_tp):
                        _ts = _tp
                    elif girl_self.has_trait(_tn):
                        _ts = _tn
                if hasattr(girl_other, "has_trait"):
                    if girl_other.has_trait(_tp):
                        _to = _tp
                    elif girl_other.has_trait(_tn):
                        _to = _tn
            if _ts:
                for _dt in (_ts if isinstance(_ts, (list, tuple)) else [_ts]):
                    _group_video_discover(girl_self, _dt)
            if _to:
                for _dt in (_to if isinstance(_to, (list, tuple)) else [_to]):
                    _group_video_discover(girl_other, _dt)
            # Virginity knowledge propagation (only works for current virgins)
            girl_learns_virgin(girl_other, girl_self)
            girl_learns_virgin(girl_self, girl_other)
            # Clear virgin shock belief if vid shows a (was-)virgin having sex
            if vid_girl and _is_virgin_or_was(vid_girl):
                check_virgin_shock(girl_self, vid_girl)
                check_virgin_shock(girl_other, vid_girl)
            # THE translation point of the scripted convos: a line is still its English source here (a name or a partner
            # key goes in only through _tl(_(template)) % name or _format_partner_line, which translate before they fill,
            # and a line already translated passes this _tl unchanged). A partner key a translation wrote gets the
            # speaker's partner, as in Say_Line. Per line, never the whole list
            return [(_cg, ru_keys_safety(_tl(_ct), GIRL_BY_ID.get(_cg))) for _cg, _ct in msgs]

        # ── BOTH HATE EACH OTHER (Girl_like < 250 both ways, consensual video): their one-shot scripted fight, one per
        # pair and video subject. The hostility check below calls it first (it used to answer every hostile pair before
        # this could play); once seen, the generic hostile pools answer ──
        def _enemies_convo():
            if vid_gid == girl_a.gid:
                return _fire(
                    "enemies_a_self_" + girl_a.gid + "_" + girl_b.gid,
                    [
                        (girl_b.gid, _tl(_("Oh look, it's %s doing what she does best. Being easy.")) % girl_a.Name),
                        (girl_a.gid, _tl(_("Excuse me?! At least %s actually WANTS to be with me!")) % pname),
                        (girl_b.gid, _("Wants you? He sends your videos around like party favors! Real special!")),
                        (girl_a.gid, _("At least I HAVE videos! When's the last time anyone wanted to film YOU?")),
                        (girl_b.gid, _("Because I have STANDARDS! Something you clearly know nothing about!")),
                        (girl_a.gid, _("Standards? Or just no options? Be honest with yourself for once!")),
                        (girl_b.gid, _tl(_("%s, I don't know why you bother with her. You could do SO much better.")) % pname),
                        (girl_a.gid, _("He already HAS the best! Don't be bitter just because it's not you!")),
                    ],
                    girl_b, girl_a,
                )

            if vid_gid == girl_b.gid:
                return _fire(
                    "enemies_b_self_" + girl_b.gid + "_" + girl_a.gid,
                    [
                        (girl_a.gid, _tl(_("Lmao %s on video? This should be embarrassing.")) % girl_b.Name),
                        (girl_b.gid, _("Embarrassing for YOU maybe, watching someone who actually knows what she's doing!")),
                        (girl_a.gid, _("Knows what she's doing? Girl, I've seen better performances from a mannequin!")),
                        (girl_b.gid, _tl(_("Says the girl %s didn't film! Wonder why~")) % pname),
                        (girl_a.gid, _("He FILMED me plenty! He just doesn't need to share mine because I'm not desperate for attention!")),
                        (girl_b.gid, _("Sure. Whatever helps you sleep at night, sweetheart!")),
                        (girl_a.gid, _tl(_("%s, why is she even in this group? Nobody wants her here!")) % pname),
                        (girl_b.gid, _tl(_("Nobody wants ME here?! %s, kick HER out! I was here first!")) % pname),
                    ],
                    girl_a, girl_b,
                )

            # a third girl's video: the enemies briefly agree before going back to fighting
            vid_girl_name = vid_girl.Name if vid_girl else "that girl"
            return _fire(
                "enemies_other_" + girl_a.gid + "_" + girl_b.gid,
                [
                    (girl_a.gid, _tl(_("Great, a video of %s. %s really has no taste.")) % (vid_girl_name, pname)),
                    (girl_b.gid, _("For ONCE I agree with you. He picks the worst girls.")),
                    (girl_a.gid, _("...Did we just agree on something? I feel sick.")),
                    (girl_b.gid, _("Don't get used to it. You're still the worst person in this chat.")),
                    (girl_a.gid, _("Second worst. You're still here.")),
                    (girl_b.gid, _tl(_("%s, the one thing she and I agree on is that you have terrible judgment.")) % pname),
                ],
                girl_a, girl_b,
            )

        # ── PRIORITY 0: Hostility check — girls who hate each other ──
        _like_ab = int(girl_a.Girl_like.get(girl_b.gid, 500)) if hasattr(girl_a, "Girl_like") else 500
        _like_ba = int(girl_b.Girl_like.get(girl_a.gid, 500)) if hasattr(girl_b, "Girl_like") else 500
        _mutual_like = min(_like_ab, _like_ba)

        if _mutual_like < 250:
            # Only ONE of them dislikes the other: no two-girl fight (the one who likes her would trade insults too). The
            # per-girl reactions answer: the one who hates her with her own hostile line (_hostile_solo)
            if max(_like_ab, _like_ba) >= 250:
                print("[GROUP_VIDEO] one-sided dislike %s->%s %d / %s->%s %d: per-girl reactions" % (
                    girl_a.gid, girl_b.gid, _like_ab, girl_b.gid, girl_a.gid, _like_ba))
                return None
            # They hate each other — hostile / mocking reactions. A consensual video: their scripted fight plays first,
            # once
            if consensual:
                _fight = _enemies_convo()
                if _fight:
                    print("[GROUP_VIDEO] enemies scripted fight: %s / %s, video of %s" % (girl_a.gid, girl_b.gid, vid_gid))
                    return _fight
            if vid_gid not in (girl_a.gid, girl_b.gid):
                # a third girl's video: every hostile script is about one of the two; the per-girl reactions answer
                print("[GROUP_VIDEO] hostile pair %s / %s, third girl's video (%s): no hostile script" % (
                    girl_a.gid, girl_b.gid, vid_gid))
                return None
            _viewer = girl_b if vid_gid == girl_a.gid else girl_a
            _vid_g = girl_a if vid_gid == girl_a.gid else girl_b
            _vn = _vid_g.Name

            # Her video reached the girl she hates: the viewer mocks first, or she protests first (half each)
            if renpy.random.random() < 0.5:
                _vid_in_grp = _vid_g.gid in members

                if vid_type in ("cowgirl", "reverse_cowgirl", "creampie", "sex", "anal"):
                    _hostile_convos = [
                        [
                            (_viewer.gid, _tl(_("Hah! Take notes, %s. THAT'S how a girl rides properly~")) % _vn if vid_type == "cowgirl" else
                             _tl(_("Wow %s, is that really the best you can do? I've seen better from a pillow.")) % _vn),
                            (_vid_g.gid, _("Excuse me?! Nobody asked for YOUR opinion!")),
                            (_viewer.gid, _tl(_("Nobody had to, it's right there on screen! %s, you could do SO much better~")) % pname),
                            (_vid_g.gid, _tl(_("I swear to GOD, %s, if you don't shut her up I'm blocking EVERYONE.")) % pname),
                        ],
                        [
                            (_viewer.gid, _tl(_("Ugh, WHY would you send me this?! I did NOT need to see %s like that!")) % _vn),
                            (_vid_g.gid, _("Then DON'T LOOK! Nobody forced you to watch!")),
                            (_viewer.gid, _("Hard not to when it's in MY group chat! Keep your business to yourself!")),
                            (_vid_g.gid, _("YOU'RE in a group with ME! That's YOUR problem, not mine!")),
                        ],
                        [
                            (_viewer.gid, _tl(_("Oh please... %s acting like she's some kind of goddess. Girl, he's just being polite.")) % _vn),
                            (_vid_g.gid, _("Polite?! He literally couldn't keep his hands off me!")),
                            (_viewer.gid, _("Sure babe. Whatever helps you sleep at night~")),
                            (_vid_g.gid, _("At least I'M sleeping with someone! When's the last time YOU got any?!")),
                        ],
                    ]
                elif vid_type in ("bj", "tj", "hj"):
                    _hostile_convos = [
                        [
                            (_viewer.gid, _tl(_("Is THAT what %s calls a blowjob? I'm embarrassed FOR her.")) % _vn if vid_type == "bj" else
                             _tl(_("Wow %s, could you look any more bored doing that?")) % _vn),
                            (_vid_g.gid, _("Oh shut UP! Like you could do better!")),
                            (_viewer.gid, _("Sweetie, I could do it blindfolded and he'd enjoy it more~")),
                            (_vid_g.gid, _tl(_("You are INSUFFERABLE. %s, WHY is she in this group?!")) % pname),
                        ],
                        [
                            (_viewer.gid, _tl(_("Why the FUCK would I want to see %s doing that?! My eyes are BURNING.")) % _vn),
                            (_vid_g.gid, _("Then scroll past it! Nobody asked you to stare!")),
                            (_viewer.gid, _("I TRIED but the cringe was too powerful! Couldn't look away!")),
                            (_vid_g.gid, _("I HATE you. Genuinely. With my entire soul.")),
                        ],
                    ]
                else:
                    # Masturbation
                    _hostile_convos = [
                        [
                            (_viewer.gid, _tl(_("%s touching herself? Wow, she really can't find anyone else huh~")) % _vn),
                            (_vid_g.gid, _("It's called SELF CARE! Something you clearly know nothing about!")),
                            (_viewer.gid, _("I know enough not to let someone FILM it! But you do you, girl~")),
                            (_vid_g.gid, _("I am going to MURDER both of you.")),
                        ],
                    ]

                # a convo is a list of (gid, text): translate each line, never the whole list (str(list) crashes the replay)
                _picked = [(_cg, _tl(_ct)) for _cg, _ct in _group_unique_choice(_hostile_convos)]
                # Apply stats — hostility means less obedience, more inhibition loss
                _apply_group_video_stats(_viewer, "other", vid_type, _is_bf_context(_viewer), consensual, group, vid)
                _apply_group_video_stats(_vid_g, "self", vid_type, _is_bf_context(_vid_g), consensual, group, vid)
                # Mutual dislike grows
                Change_Status(_viewer, "Obed", -2)
                Change_Status(_vid_g, "Obed", -2)
                return _picked

            else:
                # She protests first: her own video went to the girl she hates
                _hostile_self_convos = [
                    [
                        (_vid_g.gid, _("Are you KIDDING me?! You sent my video to HER?! Of ALL people?!")),
                        (_viewer.gid, _("Oh calm down, it's not like there's much to see anyway~")),
                        (_vid_g.gid, _tl(_("I will END you. %s, remove her from this group RIGHT NOW.")) % pname),
                        (_viewer.gid, _("Aww, she's embarrassed~ How cute~")),
                    ],
                    [
                        (_vid_g.gid, _tl(_("NO. No no no. WHY is SHE seeing this?! %s, what is WRONG with you?!")) % pname),
                        (_viewer.gid, _("Relax, I've already seen worse. Like your personality, for example.")),
                        (_vid_g.gid, _("I hope you choke. Both of you. I'm done.")),
                        (_viewer.gid, _("Drama queen as always~ The video was mid anyway.")),
                    ],
                ]
                _picked = [(_cg, _tl(_ct)) for _cg, _ct in _group_unique_choice(_hostile_self_convos)]
                _apply_group_video_stats(_vid_g, "self", vid_type, _is_bf_context(_vid_g), consensual, group, vid)
                _apply_group_video_stats(_viewer, "other", vid_type, _is_bf_context(_viewer), consensual, group, vid)
                Change_Status(_vid_g, "Love", -5)
                Change_Status(_vid_g, "Obed", -3)
                return _picked

        # ==========================================================
        # CUM_SLUT vs HATE_CUM — creampie
        # ==========================================================
        slut, hater = _pair("cum_slut", "hate_cum")

        # The eager-trait scripts (cum_slut / hardcore_sex) speak in a veteran's voice and fire once: they wait until
        # she is past discovering the trait (trait_is_veteran); before that her own reactions answer
        if slut and hater and vid_type == "creampie" and trait_is_veteran(slut, "cum_slut"):
            if consensual:
                # ── Scenario 1a: creampie of the cum_slut (she knew about the recording) ──
                if vid_gid == slut.gid:
                    return _fire(
                        "cumslut_creampie_self_" + slut.gid + "_" + hater.gid,
                        [
                            (slut.gid, _("Omg... look at how much he filled me up... it's dripping out~")),
                            (hater.gid, _("Are you two CRAZY?! Why would you send me this?! AND YOU SHOULD USE PROTECTION!")),
                            (slut.gid, _("No way girl, you need to live a little! Being filled up is literally the best sensation in the world~")),
                            (hater.gid, _("What if you get pregnant?! This is dangerous, do you even think about that?!")),
                            (slut.gid, _tl(_("Some risks are worth it... and now I'm getting hot watching this again... %s, are you free later~?")) % pname),
                        ],
                        slut, hater,
                    )

                # ── Scenario 2a: creampie of the cum_hater (she knew about the recording) ──
                if vid_gid == hater.gid:
                    return _fire(
                        "cumhater_creampie_self_" + hater.gid + "_" + slut.gid,
                        [
                            (hater.gid, _tl(_("%s!! WHAT THE HELL?! WHY ARE YOU SENDING THIS HERE?! I'M GONNA DIE!")) % pname),
                            (slut.gid, _tl(_("Hoooooly shit! %s, you told me once you didn't even do it without protection! So you changed your mind~?")) % hater.Name),
                            (hater.gid, _("I can't believe this... IT WAS JUST THAT ONE TIME! I was almost there and couldn't pull out...")),
                            (slut.gid, _("Are you gonna tell me the sensation wasn't amazing? ADMIT IT!")),
                            (hater.gid, _("It was disgusting.")),
                            (slut.gid, _("Admit it!")),
                            (hater.gid, _("Okay fine! It was good, but too dangerous! Are you happy now?!")),
                            (slut.gid, _tl(_("Hahaha I knew it! %s, thank you! You saved my whole day!")) % pname),
                        ],
                        hater, slut,
                    )
            else:
                # ── Scenario 1b: secret creampie recording of the cum_slut ──
                if vid_gid == slut.gid:
                    return _fire(
                        "cumslut_creampie_secret_" + slut.gid + "_" + hater.gid,
                        [
                            (slut.gid, _("Wait... you FILMED that?! Without telling me?! I mean... I look good but that's NOT the point!")),
                            (hater.gid, _tl(_("He secretly recorded a CREAMPIE?! %s, that's seriously messed up!")) % slut.Name),
                            (slut.gid, _("I know I should be furious but... look at that shot... okay NO. I'm mad! Probably. Let me watch it one more time.")),
                            (hater.gid, _("You're WATCHING IT AGAIN?! He came inside you WITHOUT protection AND filmed it secretly!")),
                            (slut.gid, _tl(_("Fine, it's wrong! But you can't deny the content is... ugh, %s, you're in SO much trouble.")) % pname),
                        ],
                        slut, hater,
                    )

                # ── Scenario 2b: secret creampie recording of the cum_hater ──
                if vid_gid == hater.gid:
                    return _fire(
                        "cumhater_creampie_secret_" + hater.gid + "_" + slut.gid,
                        [
                            (hater.gid, _tl(_("%s!! You SECRETLY RECORDED THAT?! And now it's in the GROUP?! I'M GOING TO KILL YOU!")) % pname),
                            (slut.gid, _tl(_("Oh no... %s, he recorded you without asking?! That's really not cool.")) % hater.Name),
                            (hater.gid, _("NOT COOL?! It's a CRIME! There's CUM inside me on that video and I NEVER agreed to any of it!")),
                            (slut.gid, _tl(_("Okay yeah, even I think that's too far. %s, secret recordings? Really?")) % pname),
                            (hater.gid, _("I already hated the cum, I hated the video, and now I hate YOU! Delete EVERYTHING!")),
                            (slut.gid, _tl(_("%s, you need to fix this. Like, right now. She's right to be furious.")) % pname),
                        ],
                        hater, slut,
                    )

        # ==========================================================
        # CAMERA_LOVER vs CAMERA_HATER — any video type (consensual)
        # ==========================================================
        cam_lover, cam_hater = _pair("camera_lover", "camera_hater")

        if cam_lover and cam_hater and consensual:
            vid_girl_name = vid_girl.Name if vid_girl else "her"

            # ── Scenario 3: video is OF the camera_lover ──
            if vid_gid == cam_lover.gid:
                return _fire(
                    "camlover_vid_self_" + cam_lover.gid + "_" + cam_hater.gid,
                    [
                        (cam_lover.gid, _("Look at that! The lighting, the angle... I look SO good in this~")),
                        (cam_hater.gid, _("You're actually HAPPY about being filmed?! That's insane to me!")),
                        (cam_lover.gid, _("Happy? Girl, I ASKED him to record it! Why wouldn't I want this on camera?")),
                        (cam_hater.gid, _("Because it's PRIVATE?! What if someone sees this?! I would literally die!")),
                        (cam_lover.gid, _tl(_("That's the fun part~ Besides, %s knows exactly how to get my good angles~")) % pname),
                        (cam_hater.gid, _tl(_("I will never understand you. NEVER. %s, please don't ever point a camera at me!")) % pname),
                        (cam_lover.gid, _("Your loss babe~ More screen time for me!")),
                    ],
                    cam_lover, cam_hater,
                )

            # ── Scenario 4: video is OF the camera_hater ──
            if vid_gid == cam_hater.gid:
                return _fire(
                    "camhater_vid_self_" + cam_hater.gid + "_" + cam_lover.gid,
                    [
                        (cam_hater.gid, _tl(_("%s!! I can't believe you actually SENT that! I told you that was a ONE TIME thing!")) % pname),
                        (cam_lover.gid, _tl(_("Hold on... %s?! YOU let him film you?! I never thought I'd see the day!")) % cam_hater.Name),
                        (cam_hater.gid, _("He was being really sweet and I got caught up in the moment okay?! I REGRET EVERYTHING!")),
                        (cam_lover.gid, _("Girl you look amazing though! Like genuinely, why do you hate cameras so much?!")),
                        (cam_hater.gid, _("Because of this! Because someone records it and then shares it!")),
                        (cam_lover.gid, _("Ok fair... but you can't deny you look good! Just admit it!")),
                        (cam_hater.gid, _tl(_("I am NOT admitting anything! %s, this was supposed to stay between US!")) % pname),
                        (cam_lover.gid, _tl(_("Lmao girl you're never living this down~ %s I owe you one, this is gold!")) % pname),
                    ],
                    cam_hater, cam_lover,
                )

            # ── Scenario 5: video is of a THIRD girl (neither lover nor hater) ──
            if vid_gid != cam_lover.gid and vid_gid != cam_hater.gid:
                return _fire(
                    "cam_other_vid_" + cam_lover.gid + "_" + cam_hater.gid,
                    [
                        (cam_lover.gid, _tl(_("Ooh! %s on camera? Let me see that!")) % vid_girl_name),
                        (cam_hater.gid, _("Why are you excited about this?! That poor girl got filmed!")),
                        (cam_lover.gid, _tl(_("She looks great though! %s really knows how to work a camera~")) % pname),
                        (cam_hater.gid, _("That is SO not the point! Doesn't anyone care about privacy anymore?!")),
                        (cam_lover.gid, _("Privacy is overrated. If I looked like that on video I'd post it everywhere~")),
                        (cam_hater.gid, _("You are UNHINGED. I'm done with this conversation!")),
                    ],
                    cam_lover, cam_hater,
                )

        # ==========================================================
        # EXHIBITIONIST vs PUBLIC_SHY — any video type (consensual)
        # ==========================================================
        exhib, shy = _pair("exhibitionist", "public_shy")

        if exhib and shy and consensual:

            # ── Scenario 6: video is OF the exhibitionist ──
            if vid_gid == exhib.gid:
                return _fire(
                    "exhib_vid_self_" + exhib.gid + "_" + shy.gid,
                    [
                        (exhib.gid, _("Yes! He finally sent it! I've been waiting for people to see this~")),
                        (shy.gid, _("You WANTED him to share this?! Are you out of your mind?!")),
                        (exhib.gid, _("Obviously! What's the point of looking this good if nobody sees it?")),
                        (shy.gid, _("The POINT is that it's intimate!! What if this gets out?!")),
                        (exhib.gid, _("Then more people get to appreciate the view~ Honestly, I wouldn't mind~")),
                        (shy.gid, _("I literally cannot process how your brain works. I would move to another country!")),
                        (exhib.gid, _("And I would start a fan page~ We are not the same, babe!")),
                    ],
                    exhib, shy,
                )

            # ── Scenario 7: video is OF the shy girl ──
            if vid_gid == shy.gid:
                return _fire(
                    "shy_vid_self_" + shy.gid + "_" + exhib.gid,
                    [
                        (shy.gid, _tl(_("No no no NO NO!! %s WHY?! Why would you send this HERE?!")) % pname),
                        (exhib.gid, _tl(_("Oh my god... %s?! Is that YOU?! Girl!!")) % shy.Name),
                        (shy.gid, _("Please stop looking at it!! I'm shaking right now, this can't be happening!")),
                        (exhib.gid, _("Relax! It's just me here! And honestly? You look incredible!")),
                        (shy.gid, _("I DON'T CARE! This was supposed to be PRIVATE! I feel so exposed!")),
                        (exhib.gid, _("Being exposed is the best part though! Embrace it, you look hot!")),
                        (shy.gid, _tl(_("That is not helpful! %s, I swear if you ever do this again...!")) % pname),
                        (exhib.gid, _tl(_("Girl, breathe. But also... %s, you owe her BIG time. And me a copy~")) % pname),
                    ],
                    shy, exhib,
                )

        # ==========================================================
        # HARDCORE_SEX vs CUTE_SEX — penetration vids (consensual)
        # ==========================================================
        hardcore, cute = _pair("hardcore_sex", "cute_sex")

        if hardcore and cute and consensual and vid_type in ("cowgirl", "reverse_cowgirl", "sex", "creampie", "anal") and trait_is_veteran(hardcore, "hardcore_sex"):

            # ── Scenario 8: video is OF the hardcore girl ──
            if vid_gid == hardcore.gid:
                return _fire(
                    "hardcore_vid_self_" + hardcore.gid + "_" + cute.gid,
                    [
                        (hardcore.gid, _("Look at that! That's how it's supposed to be done! No holding back~")),
                        (cute.gid, _("Oh my god... that looks so... intense. Doesn't that HURT?!")),
                        (hardcore.gid, _("Hurt? Girl, that's the best part! Pain and pleasure go together~")),
                        (cute.gid, _("I could NEVER. I like it slow and gentle... that looks scary!")),
                        (hardcore.gid, _tl(_("Scary? That's barely getting started! %s knows I can handle way more~")) % pname),
                        (cute.gid, _("I don't understand how you enjoy that! I want cuddles, not... THAT!")),
                        (hardcore.gid, _("Babe, try it once and you'll never go back to your vanilla stuff~")),
                        (cute.gid, _("My 'vanilla stuff' is ROMANTIC! Not everything has to be so aggressive!")),
                    ],
                    hardcore, cute,
                )

            # ── Scenario 9: video is OF the cute girl ──
            if vid_gid == cute.gid:
                _hc_has_history = bool(getattr(hardcore, "intimacy_flags", set()) & {"hj", "bj", "tj", "sex", "anal"})
                if _hc_has_history:
                    return _fire(
                        "cute_vid_self_" + cute.gid + "_" + hardcore.gid,
                        [
                            (cute.gid, _("Oh gosh... he sent it... it was such a sweet moment though...")),
                            (hardcore.gid, _("That's IT? He's barely touching you! Where's the energy?!")),
                            (cute.gid, _("It's not about energy! It was tender and intimate and perfect!")),
                            (hardcore.gid, _tl(_("It looks like he's afraid of breaking you! %s, go HARDER next time!")) % pname),
                            (cute.gid, _("DON'T listen to her! It was exactly how I like it!")),
                            (hardcore.gid, _("Girl, I'm telling you, if he put even HALF the intensity he gives me...")),
                            (cute.gid, _("I don't WANT intensity! I want him to hold my hand and look me in the eyes!")),
                            (hardcore.gid, _("...He can choke me AND look me in the eyes. Best of both worlds~")),
                        ],
                        cute, hardcore,
                    )
                else:
                    _hc_is_les = hardcore.has_trait("lesbian")
                    _hc_has_partner = hasattr(hardcore, "has_npc_partner") and hardcore.has_npc_partner()
                    if _hc_is_les:
                        _hc_pl = hardcore.partner_label() if _hc_has_partner and hasattr(hardcore, "partner_label") else "girlfriend"
                        return _fire(
                            "cute_vid_self_nohist_les_" + cute.gid + "_" + hardcore.gid,
                            [
                                (cute.gid, _("Oh gosh... he sent it... it was such a sweet moment though...")),
                                (hardcore.gid, _("That's what sex with a man looks like? Seriously? That's so... tame.")),
                                (cute.gid, _("It's not tame! It was tender and intimate and perfect!")),
                                (hardcore.gid, _("I don't get why you'd want a guy when you could have... never mind.")),
                                (cute.gid, _("Because I LIKE him! Not everything is about what YOU prefer!")),
                                (hardcore.gid, _("I'm just saying, it looks boring. But hey, your body, your choice.")),
                                (cute.gid, _("It was NOT boring! It was exactly how I wanted it!")),
                                (hardcore.gid, _("...Fine. But don't expect me to understand the appeal.")),
                            ],
                            cute, hardcore,
                        )
                    elif _hc_has_partner:
                        _hc_pl = hardcore.partner_label() if hasattr(hardcore, "partner_label") else "partner"
                        return _fire(
                            "cute_vid_self_nohist_bf_" + cute.gid + "_" + hardcore.gid,
                            [
                                (cute.gid, _("Oh gosh... he sent it... it was such a sweet moment though...")),
                                (hardcore.gid, _("That's IT? That's what you call sex? Where's the energy?!")),
                                (cute.gid, _("It's not about energy! It was tender and intimate and perfect!")),
                                (hardcore.gid, _("He looks like he's afraid of breaking you! So boring!")),
                                (cute.gid, _("It's NOT boring! It was exactly how I like it!")),
                                (hardcore.gid, _tl(_("My %s is more intense than that... and HE's not even that good.")) % _hc_pl),
                                (cute.gid, _("I don't WANT intense! I want gentle and loving!")),
                                (hardcore.gid, _("...To each their own, I guess. But that video was a snoozefest.")),
                            ],
                            cute, hardcore,
                        )
                    else:
                        return _fire(
                            "cute_vid_self_nohist_" + cute.gid + "_" + hardcore.gid,
                            [
                                (cute.gid, _("Oh gosh... he sent it... it was such a sweet moment though...")),
                                (hardcore.gid, _("That's IT? That's what you call sex? Where's the energy?!")),
                                (cute.gid, _("It's not about energy! It was tender and intimate and perfect!")),
                                (hardcore.gid, _("He looks like he's afraid of breaking you! That's so boring!")),
                                (cute.gid, _("It's NOT boring! It was exactly how I like it!")),
                                (hardcore.gid, _("If that was ME in that video, it would look VERY different.")),
                                (cute.gid, _("I don't WANT it different! I want him to hold my hand and look me in the eyes!")),
                                (hardcore.gid, _("...Whatever. But if he ever comes to me, I'll show him what real intensity looks like.")),
                            ],
                            cute, hardcore,
                        )

        # ==========================================================
        # CHEATER vs LOYAL — video where the vid girl has a BF (consensual)
        # ==========================================================
        cheater, loyal = _pair("cheater", "loyal")
        _vid_has_bf = _vid_bf_still_relevant(vid)

        if cheater and loyal and consensual and _vid_has_bf:

            # ── Scenario 10: video girl has a boyfriend/girlfriend ──
            # Works whether vid girl is one of them or a third person
            if vid_gid == cheater.gid:
                _fpl = lambda s: _format_partner_line(cheater, s)
                return _fire(
                    "cheater_bf_self_" + cheater.gid + "_" + loyal.gid,
                    [
                        (cheater.gid, _fpl(_("Oops~ Well, what %(pp)s doesn't know won't hurt %(po)s, right?"))),
                        (loyal.gid, _fpl(_("OOPS?! You're with %(pl)s and you're saying OOPS?!"))),
                        (cheater.gid, _("Relax, it's not that serious! A girl has needs~")),
                        (loyal.gid, _fpl(_("NEEDS?! Then break up with %(po)s first! This is so wrong!"))),
                        (cheater.gid, _fpl(_("Why would I break up with %(po)s? %(Pp)s gives me stability. {player} gives me... other things~")).replace("{player}", pname)),
                        (loyal.gid, _("That is the most disgusting logic I have ever heard in my LIFE!")),
                        (cheater.gid, _("You're just mad because you follow the rules and I have more fun~")),
                        (loyal.gid, _("I have MORALS! Something clearly missing from your vocabulary!")),
                    ],
                    cheater, loyal,
                )

            if vid_gid == loyal.gid:
                _fpl = lambda s: _format_partner_line(loyal, s)
                return _fire(
                    "loyal_bf_self_" + loyal.gid + "_" + cheater.gid,
                    [
                        (loyal.gid, _tl(_("%s... I can't believe this is out there. I feel terrible...")) % pname),
                        (cheater.gid, _("Oh please! You did it, own it! Was it good at least~?")),
                        (loyal.gid, _fpl(_("That's not the POINT! I'm with %(pl)s and this is eating me alive!"))),
                        (cheater.gid, _("Girl, if it's eating you alive then clearly you enjoyed it~")),
                        (loyal.gid, _("STOP! I made a mistake! A huge, terrible mistake!")),
                        (cheater.gid, _("A mistake you'd make again based on that video~ Don't lie to me!")),
                        (loyal.gid, _tl(_("I am NOT having this conversation! %s, why would you send this?!")) % pname),
                        (cheater.gid, _("Because it was hot! Relax, your secret is safe with me~ ...probably~")),
                    ],
                    loyal, cheater,
                )

            # Third girl has BF/GF
            if vid_gid != cheater.gid and vid_gid != loyal.gid:
                vid_girl_name = vid_girl.Name if vid_girl else "that girl"
                _fpl = lambda s: _format_partner_line(vid_girl, s) if vid_girl else s
                return _fire(
                    "cheat_loyal_other_" + cheater.gid + "_" + loyal.gid,
                    [
                        (loyal.gid, _fpl(_("Wait... isn't {name} with %(pl)s?! {player}, WHAT ARE YOU DOING?!")).replace("{name}", vid_girl_name).replace("{player}", pname)),
                        (cheater.gid, _tl(_("Oh wow~ Naughty naughty %s... I love it!")) % vid_girl_name),
                        (loyal.gid, _fpl(_("You LOVE it?! A girl is cheating on %(pl)s and you LOVE it?!"))),
                        (cheater.gid, _("I mean... the heart wants what it wants! Can you blame her?")),
                        (loyal.gid, _tl(_("YES! I can absolutely blame her! And YOU, %s!")) % pname),
                        (cheater.gid, _("Calm down, it's their business! I just appreciate the content~")),
                    ],
                    loyal, cheater,
                )

        # ==========================================================
        # VOYEUR + VIRGIN — any explicit video (consensual)
        # ==========================================================
        voyeur, virgin = _pair("voyeur", "virgin")

        if voyeur and virgin and consensual:
            _virgin_is_les = hasattr(virgin, "has_trait") and virgin.has_trait("lesbian")

            # ── Scenario 11: voyeur's own vid, virgin hasn't done penetration ──
            if vid_gid == voyeur.gid:
                if _virgin_is_les:
                    return _fire(
                        "voyeur_vid_self_les_" + voyeur.gid + "_" + virgin.gid,
                        [
                            (voyeur.gid, _("Oh wow... seeing myself like this is... different. But I can't stop watching~")),
                            (virgin.gid, _("You're watching yourself with a guy on repeat? I could never...")),
                            (voyeur.gid, _("It's fascinating from this angle! I never noticed how I move~")),
                            (virgin.gid, _("Fascinating? It's a man. How is that fascinating?")),
                            (voyeur.gid, _("Come on, aren't you even a little curious what it's like?")),
                            (virgin.gid, _("Curious about sex with a man? Absolutely not. I'm a lesbian.")),
                            (voyeur.gid, _("Not even a tiny bit? It's just a video~")),
                            (virgin.gid, _("Not even a tiny bit. You enjoy your videos, I'll enjoy mine.")),
                        ],
                        voyeur, virgin,
                    )
                return _fire(
                    "voyeur_vid_self_" + voyeur.gid + "_" + virgin.gid,
                    [
                        (voyeur.gid, _("Oh wow... seeing myself like this is... different. But I can't stop watching~")),
                        (virgin.gid, _("You can't stop watching YOURSELF?! That's... a lot!")),
                        (voyeur.gid, _("It's fascinating from this angle! I never noticed how I move~")),
                        (virgin.gid, _("I really don't need that level of detail right now!")),
                        (voyeur.gid, _("Come on, aren't you even a little curious what it's like?")),
                        (virgin.gid, _("Curious and comfortable are two VERY different things!")),
                        (voyeur.gid, _("You're so tense~ It's just a video! You've done stuff with him too!")),
                        (virgin.gid, _("Not THAT stuff! And I don't want a preview through YOUR video!")),
                    ],
                    voyeur, virgin,
                )

            # Virgin IS the girl in the video
            if vid_gid == virgin.gid:
                if _virgin_is_les:
                    return _fire(
                        "voyeur_virgin_self_les_" + voyeur.gid + "_" + virgin.gid,
                        [
                            (virgin.gid, _("You're all watching me with a GUY?! This is humiliating...")),
                            (voyeur.gid, _("Actually, you look incredible! The way you move, even nervous, it's fascinating~")),
                            (virgin.gid, _("Fascinating?! It's a man! I didn't even want to do it! Well... not really!")),
                            (voyeur.gid, _("Your body says otherwise! That's the most genuine reaction I've ever seen~")),
                            (virgin.gid, _("Stop analyzing me! This is the worst day of my life!")),
                            (voyeur.gid, _("Drama! You'll thank me when you realize how good you looked~")),
                            (virgin.gid, _("I will NEVER thank you for this. Ever.")),
                            (voyeur.gid, _("Sure~ Save that energy for the rematch~")),
                        ],
                        virgin, voyeur,
                    )
                return _fire(
                    "voyeur_virgin_self_" + voyeur.gid + "_" + virgin.gid,
                    [
                        (virgin.gid, _tl(_("Oh my god... that's ME! %s, why would you send this?!")) % pname),
                        (voyeur.gid, _("Wait, that's you?! Let me see... wow, you actually look amazing!")),
                        (virgin.gid, _("STOP looking at it! This is so embarrassing!")),
                        (voyeur.gid, _("Embarrassing? Girl, you look way better than you think! The angles, the expressions...")),
                        (virgin.gid, _("I don't want commentary on my performance! Delete this!")),
                        (voyeur.gid, _("Performance? I'm complimenting you! You're a natural~")),
                        (virgin.gid, _("A natural at what?! I barely knew what I was doing!")),
                        (voyeur.gid, _("And THAT'S what makes it so good! The genuine reactions are everything~")),
                    ],
                    virgin, voyeur,
                )

            # Third girl in vid (neither voyeur nor virgin)
            vid_girl_name = vid_girl.Name if vid_girl else "her"
            if _virgin_is_les:
                return _fire(
                    "voyeur_virgin_other_les_" + voyeur.gid + "_" + virgin.gid,
                    [
                        (voyeur.gid, _tl(_("Ooh... %s looks amazing. I could watch this all day~")) % vid_girl_name),
                        (virgin.gid, _("You actually enjoy watching this? It's a girl with a guy...")),
                        (voyeur.gid, _("Look at the way she moves! The rhythm, the expressions... fascinating!")),
                        (virgin.gid, _("I mean, she looks good, but the guy part ruins it for me.")),
                        (voyeur.gid, _("Focus on HER then! The technique is impressive regardless~")),
                        (virgin.gid, _("I'd rather see her without the guy involved, honestly.")),
                        (voyeur.gid, _("Picky picky~ A good performance is a good performance!")),
                        (virgin.gid, _("It's not about performance! I'm just... not into that. At all.")),
                    ],
                    voyeur, virgin,
                )
            return _fire(
                "voyeur_virgin_other_" + voyeur.gid + "_" + virgin.gid,
                [
                    (voyeur.gid, _tl(_("Ooh... %s looks amazing. I could watch this all day~")) % vid_girl_name),
                    (virgin.gid, _("All day?! How can you just sit there and casually analyze this?!")),
                    (voyeur.gid, _("Look at the way she moves! The rhythm, the expressions... fascinating!")),
                    (virgin.gid, _("Fascinating is NOT the word I'd use! This is way too much!")),
                    (voyeur.gid, _("See that thing with her hips? That's technique! You should pay attention~")),
                    (virgin.gid, _("I don't need pointers from a video! I'm fine at my own pace!")),
                    (voyeur.gid, _("Your pace? Girl, eventually you'll want to go further and this is research~")),
                    (virgin.gid, _("It's NOT research! Stop treating this like a nature documentary!")),
                ],
                voyeur, virgin,
            )

        # ==========================================================
        # CUM_SLUT + VIRGIN — creampie video (consensual)
        # ==========================================================
        cslut_v, virgin_v = _pair("cum_slut", "virgin")

        if cslut_v and virgin_v and consensual and vid_type == "creampie" and trait_is_veteran(cslut_v, "cum_slut"):
            _virgin_v_les = hasattr(virgin_v, "has_trait") and virgin_v.has_trait("lesbian")

            if vid_gid == cslut_v.gid:
                if _virgin_v_les:
                    return _fire(
                        "cumslut_virgin_les_self_" + cslut_v.gid + "_" + virgin_v.gid,
                        [
                            (cslut_v.gid, _("Mmm~ Look at all that... he really filled me up good!")),
                            (virgin_v.gid, _("He came INSIDE you?! That's... why would you want a man to do that?!")),
                            (cslut_v.gid, _("Because it feels INCREDIBLE! The warmth spreading through you...")),
                            (virgin_v.gid, _("Okay, I definitely did NOT need that image. I'm a lesbian. Hard pass.")),
                            (cslut_v.gid, _("Lesbian or not, the sensation is universal! You'd be surprised~")),
                            (virgin_v.gid, _("I would NOT be surprised because I will NEVER find out!")),
                            (cslut_v.gid, _tl(_("Never say never~ %s has a way of changing minds!")) % pname),
                            (virgin_v.gid, _("My mind is NOT changing! I like women! This conversation is over!")),
                        ],
                        cslut_v, virgin_v,
                    )
                # "birth control" is a claim about HER (_gv_claims_birth_control): otherwise she brushes it off
                _cs_bc = _gv_claims_birth_control(cslut_v)
                _cs_msgs = _fire(
                    "cumslut_virgin_self_" + cslut_v.gid + "_" + virgin_v.gid,
                    [
                        (cslut_v.gid, _("Mmm~ Look at all that... he really filled me up good!")),
                        (virgin_v.gid, _("He... WHAT?! Inside?! Isn't that how you get... you know...!!")),
                        (cslut_v.gid, _tl(_("Pregnant? Girl, there's this thing called birth control! And also... it feels INCREDIBLE!")) if _cs_bc
                         else _tl(_("Pregnant? Girl, don't be such a buzzkill! It feels INCREDIBLE!"))),
                        (virgin_v.gid, _("I don't want to know how it feels!! This is way too much information!")),
                        (cslut_v.gid, _("You'll understand one day! That warm feeling when he finishes inside... nothing compares~")),
                        (virgin_v.gid, _("Please stop describing it! I'm going to have a heart attack!")),
                        (cslut_v.gid, _("Fine fine~ But when it's your turn, remember I told you so!")),
                        (virgin_v.gid, _tl(_("There will be no turn! %s what have you done to her?!")) % pname),
                    ],
                    cslut_v, virgin_v,
                )
                if _cs_msgs:
                    print("[GROUP_VIDEO] cumslut_virgin_self %s: birth control line=%s (on_pill=%s placebo=%s pregnant=%s known=%s mode=%s)" % (
                        cslut_v.gid, _cs_bc, getattr(cslut_v, "_on_pill", False), getattr(cslut_v, "_on_placebo", False),
                        getattr(cslut_v, "_pregnant", False), getattr(cslut_v, "_pregnancy_known", False), store._pregnancy_mode))
                return _cs_msgs

            # NOTE: virgin_v can't BE in a creampie vid — she loses
            # the virgin trait upon penetration, so no self-vid scenario here.

        # ==========================================================
        # EXHIBITIONIST + VOYEUR — video of one of them (consensual)
        # ==========================================================
        exhib_v, voyeur_v = _pair("exhibitionist", "voyeur")

        if exhib_v and voyeur_v and consensual:

            if vid_gid == exhib_v.gid:
                return _fire(
                    "exhib_voyeur_self_" + exhib_v.gid + "_" + voyeur_v.gid,
                    [
                        (exhib_v.gid, _("I hope you're watching closely~ This is premium content!")),
                        (voyeur_v.gid, _("Oh trust me, I haven't blinked once since this started...")),
                        (exhib_v.gid, _("Good~ I love knowing you're paying attention to every detail!")),
                        (voyeur_v.gid, _("The way the light hits your skin at 0:23... perfection.")),
                        (exhib_v.gid, _("See?! Someone who APPRECIATES it! Finally!")),
                        (voyeur_v.gid, _("I could watch this on repeat. Actually, I already am~")),
                        (exhib_v.gid, _tl(_("%s, you should record us together next time~ She watches, I perform~")) % pname),
                        (voyeur_v.gid, _("...I would not say no to that. Just putting it out there.")),
                    ],
                    exhib_v, voyeur_v,
                )

            if vid_gid == voyeur_v.gid:
                return _fire(
                    "voyeur_exhib_self_" + voyeur_v.gid + "_" + exhib_v.gid,
                    [
                        (voyeur_v.gid, _("Oh god... usually I'm the one watching, not being watched...")),
                        (exhib_v.gid, _("NOW you know how it feels! And girl, you look GOOD!")),
                        (voyeur_v.gid, _("This is so weird being on the other side... I feel exposed!")),
                        (exhib_v.gid, _("Exposed is AMAZING! Embrace it! You finally get what I feel!")),
                        (voyeur_v.gid, _("I don't know... I prefer being behind the screen, not on it...")),
                        (exhib_v.gid, _("Too bad! You're on it now and you're gorgeous! Own it!")),
                        (voyeur_v.gid, _("I guess it's... kind of interesting seeing myself from this angle...")),
                        (exhib_v.gid, _tl(_("SEE?! That's the first step! %s, film her more! She's converting!")) % pname),
                    ],
                    voyeur_v, exhib_v,
                )

        # ==========================================================
        # PUBLIC_FETISH vs PUBLIC_SHY — any video type (consensual)
        # ==========================================================
        pub_fet, pub_shy = _pair("public_fetish", "public_shy")

        if pub_fet and pub_shy and consensual:

            # ── Scenario: video is OF the public_fetish girl ──
            if vid_gid == pub_fet.gid:
                return _fire(
                    "pubfet_vid_self_" + pub_fet.gid + "_" + pub_shy.gid,
                    [
                        (pub_fet.gid, _("The fact that this is out there... in a group chat... god that's exciting~")),
                        (pub_shy.gid, _("Exciting?! This is a group chat! Anyone could screenshot this!")),
                        (pub_fet.gid, _("I know right? The risk is what makes it so good~")),
                        (pub_shy.gid, _("The risk?! That's not a good thing! What is wrong with you?!")),
                        (pub_fet.gid, _("You know what would be even better? If he posted it somewhere public~")),
                        (pub_shy.gid, _("Are you insane?! I'm hyperventilating just thinking about that!")),
                        (pub_fet.gid, _("Girl, you need to loosen up~ The thrill of being caught is half the fun!")),
                        (pub_shy.gid, _("The thrill of being CAUGHT?! I would literally cease to exist!")),
                    ],
                    pub_fet, pub_shy,
                )

            # ── Scenario: video is OF the public_shy girl ──
            if vid_gid == pub_shy.gid:
                return _fire(
                    "pubshy_vid_self_" + pub_shy.gid + "_" + pub_fet.gid,
                    [
                        (pub_shy.gid, _("No... no please no... this is in a GROUP CHAT?! People can SEE this?!")),
                        (pub_fet.gid, _("They sure can! And honestly? That's kind of hot~")),
                        (pub_shy.gid, _("Hot?! I'm having a panic attack right now! This is my worst fear!")),
                        (pub_fet.gid, _("Your worst fear is my biggest fantasy! Funny how that works~")),
                        (pub_shy.gid, _("It's not funny! What if someone saves it?! What if it spreads?!")),
                        (pub_fet.gid, _("Then more people get to see you! And you look great, by the way!")),
                        (pub_shy.gid, _tl(_("I don't want more people to see me! %s, delete this!")) % pname),
                        (pub_fet.gid, _tl(_("Don't delete it! %s, next time record us somewhere public~ Imagine a park, or a mall...")) % pname),
                        (pub_shy.gid, _("I am BLOCKING both of you. GOODBYE!")),
                    ],
                    pub_shy, pub_fet,
                )

        # ==========================================================
        # EXHIBITIONIST + CAMERA_LOVER — both enjoy it (consensual)
        # Two girls who love attention, competing for the spotlight.
        # ==========================================================
        exhib_c, cam_c = _pair("exhibitionist", "camera_lover")

        if exhib_c and cam_c and consensual:

            # ── Scenario: video is OF the exhibitionist ──
            if vid_gid == exhib_c.gid:
                return _fire(
                    "exhib_camlover_self_" + exhib_c.gid + "_" + cam_c.gid,
                    [
                        (exhib_c.gid, _("Everyone look! I don't care who sees this, I look AMAZING~")),
                        (cam_c.gid, _("Ok I'll admit, you look good... but the camera angle is all wrong!")),
                        (exhib_c.gid, _("Wrong?! I look incredible! The exposure is what matters!")),
                        (cam_c.gid, _tl(_("The exposure means nothing if the framing is bad! %s should've gone lower!")) % pname),
                        (exhib_c.gid, _("You're jealous because you're not the one being watched right now~")),
                        (cam_c.gid, _("Jealous? Please! When it's MY turn, the cinematography will be on another level!")),
                        (exhib_c.gid, _("Cinematography?! Girl, it's a sex video, not a movie!")),
                        (cam_c.gid, _tl(_("Every video of ME is a movie! %s, remember that for next time!")) % pname),
                    ],
                    exhib_c, cam_c,
                )

            # ── Scenario: video is OF the camera_lover ──
            if vid_gid == cam_c.gid:
                return _fire(
                    "camlover_exhib_self_" + cam_c.gid + "_" + exhib_c.gid,
                    [
                        (cam_c.gid, _tl(_("Look at those angles! %s really outdid himself with the camera work~")) % pname),
                        (exhib_c.gid, _("Angles shmangles! What matters is that everyone can SEE you!")),
                        (cam_c.gid, _("It matters HOW they see me! Lighting, composition, framing!")),
                        (exhib_c.gid, _("Girl, I would show this in Times Square and not care about the lighting!")),
                        (cam_c.gid, _("And THAT is why your videos never look as good as mine~")),
                        (exhib_c.gid, _("Excuse me?! My videos are amazing because I'M in them!")),
                        (cam_c.gid, _("And mine are amazing because they're actually well MADE!")),
                        (exhib_c.gid, _tl(_("%s, settle this! Who looks better on camera?!")) % pname),
                        (cam_c.gid, _("Don't answer that! Just film me better next time!")),
                    ],
                    cam_c, exhib_c,
                )

        # ==========================================================
        # VIRGIN SYSTEM — knowledge-gated reactions
        # Set pair traits for auto-discover in _fire
        _pair_traits[0] = "virgin"
        _pair_traits[1] = None
        # Three scenarios:
        # 1. Other girl KNOWS she's virgin AND she IS still virgin
        #    -> teasing about hj/bj/tj, shock about penetration
        # 2. Other girl THINKS she's virgin but she ALREADY LOST IT
        #    -> "wait, aren't you a virgin?!" and she tries to deflect
        # 3. Other girl does NOT know -> no virgin-specific reactions
        # ==========================================================
        _supposed_virgin = None   # girl the other THINKS is virgin
        _questioner = None        # the one asking

        # Check if girl_a thinks girl_b is virgin (or vice versa)
        _a_thinks_b_virgin = girl_thinks_virgin(girl_a, girl_b)
        _b_thinks_a_virgin = girl_thinks_virgin(girl_b, girl_a)

        # ==========================================================
        # FLOW 1b: BOTH think the other is virgin (both virgins)
        # ==========================================================
        if _a_thinks_b_virgin and _b_thinks_a_virgin and consensual:
            _vid_girl_pair = girl_a if vid_gid == girl_a.gid else girl_b
            _watcher_pair = girl_b if vid_gid == girl_a.gid else girl_a
            _vn_pair = _vid_girl_pair.Name
            _pn_pair = Player.Name if hasattr(Player, "Name") else "him"
            _vg_les = hasattr(_vid_girl_pair, "has_trait") and _vid_girl_pair.has_trait("lesbian")
            _wa_les = hasattr(_watcher_pair, "has_trait") and _watcher_pair.has_trait("lesbian")

            if _vg_les or _wa_les:
                if vid_type in ("cowgirl", "reverse_cowgirl", "creampie"):
                    if _vg_les and _wa_les:
                        return _fire(
                            "both_lesvirgin_sex_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... you slept with a MAN?! We're both GAY!")) % _vn_pair),
                                (_vid_girl_pair.gid, _("I KNOW! I don't know how it happened! He just... I couldn't stop it...")),
                                (_watcher_pair.gid, _("You couldn't stop it?! Girl, we're LESBIANS! How do you end up riding a GUY?!")),
                                (_vid_girl_pair.gid, _("Stop yelling! It's complicated! My body reacted even if my brain didn't want it!")),
                                (_watcher_pair.gid, _("I'm never letting a man near me like that. NEVER.")),
                                (_vid_girl_pair.gid, _tl(_("Good for you! Now can %s please DELETE this?!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                    elif _wa_les:
                        return _fire(
                            "leswatch_virgin_sex_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... you actually went all the way with him?")) % _vn_pair),
                                (_vid_girl_pair.gid, _("Yes! And I wasn't planning on it! Don't judge me!")),
                                (_watcher_pair.gid, _("I'm not judging... it's just... I'd never let a man do that to me.")),
                                (_vid_girl_pair.gid, _("Well we're not the same! Some of us like guys!")),
                                (_watcher_pair.gid, _("Fair enough. But the whole group seeing your first time? Rough.")),
                                (_vid_girl_pair.gid, _tl(_("%s, WHY would you share this?!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                    else:
                        return _fire(
                            "virgin_leswatch_sex_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... you actually... with a MAN?! But you're...")) % _vn_pair),
                                (_vid_girl_pair.gid, _("Don't say it! I KNOW what I am! It just... happened!")),
                                (_watcher_pair.gid, _("I thought we were both waiting... but your reason was different from mine...")),
                                (_vid_girl_pair.gid, _("My reason WAS different! I don't even like guys! This was... I don't know what this was!")),
                                (_watcher_pair.gid, _("Are you okay...? That looked intense...")),
                                (_vid_girl_pair.gid, _tl(_("I'm NOT okay! And %s needs to DELETE THIS RIGHT NOW!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                elif vid_type in ("bj", "tj", "hj"):
                    if _vg_les and _wa_les:
                        return _fire(
                            "both_lesvirgin_oral_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... you're doing THAT with a guy?! We're both supposed to be gay!")) % _vn_pair),
                                (_vid_girl_pair.gid, _("I AM gay! This doesn't change that! It was just... one time!")),
                                (_watcher_pair.gid, _("One time with a MAN'S body! How do you even...?!")),
                                (_vid_girl_pair.gid, _tl(_("Don't ask! And don't watch! %s, I'm going to destroy you for this!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                    elif _wa_les:
                        return _fire(
                            "leswatch_virgin_oral_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("So... you did THAT with %s? You straight girls are brave.")) % _pn_pair),
                                (_vid_girl_pair.gid, _("It's not about being brave! It just happened! And I'm still a virgin!")),
                                (_watcher_pair.gid, _("Relax, I'm not judging. I just could never imagine doing that with a guy.")),
                                (_vid_girl_pair.gid, _tl(_("Well nobody asked you to imagine it! %s, delete this!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                    else:
                        return _fire(
                            "virgin_leswatch_oral_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... with a GUY?! But you said you were...")) % _vn_pair),
                                (_vid_girl_pair.gid, _("I AM! This doesn't mean anything! I was just... it was complicated!")),
                                (_watcher_pair.gid, _("It's okay... I'm just surprised. I never thought you'd do anything with a man.")),
                                (_vid_girl_pair.gid, _tl(_("Me neither! And the group doesn't need to see it! %s, you're dead!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                elif vid_type == "masturbate":
                    if _vg_les and _wa_les:
                        return _fire(
                            "both_lesvirgin_mast_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                            [
                                (_watcher_pair.gid, _tl(_("%s... well, at least there's no guy in this one.")) % _vn_pair),
                                (_vid_girl_pair.gid, _("Obviously! I'm a lesbian! But the group didn't need to SEE this!")),
                                (_watcher_pair.gid, _("I do it too... but I'd die if anyone saw mine...")),
                                (_vid_girl_pair.gid, _tl(_("And now you know how I feel! %s, DELETE THIS!")) % _pn_pair),
                            ],
                            _vid_girl_pair, _watcher_pair,
                        )
                    # Masturbate with only one lesbian — no guy involved, normal convo is fine
                else:
                    # Sex/oral with lesbian: don't fall through to hetero convos
                    return

            if vid_type in ("cowgirl", "reverse_cowgirl", "creampie"):
                return _fire(
                    "both_virgin_sex_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                    [
                        (_watcher_pair.gid, _tl(_("%s... you actually DID it?! We BOTH said we were waiting!")) % _vn_pair),
                        (_vid_girl_pair.gid, _("I know! I KNOW! It just happened! He was so... and I couldn't...")),
                        (_watcher_pair.gid, _("I can't believe you went first... I feel like I'm falling behind...")),
                        (_vid_girl_pair.gid, _("You're NOT falling behind! It's not a race! And stop watching!")),
                        (_watcher_pair.gid, _("Was it... was it worth it? Does it hurt as much as they say?")),
                        (_vid_girl_pair.gid, _tl(_("I am NOT having this conversation in a group chat! %s, you ruined EVERYTHING!")) % _pn_pair),
                        (_watcher_pair.gid, _("...That's not a no.")),
                        (_vid_girl_pair.gid, _("STOP!")),
                    ],
                    _vid_girl_pair, _watcher_pair,
                )
            elif vid_type == "bj":
                return _fire(
                    "both_virgin_bj_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                    [
                        (_watcher_pair.gid, _tl(_("%s?! You put it in your MOUTH?! I could never... how do you even...")) % _vn_pair),
                        (_vid_girl_pair.gid, _("It's not that big of a deal! I'm still a virgin! Oral doesn't count!")),
                        (_watcher_pair.gid, _("How does THAT not count?! His... thing was in your MOUTH!")),
                        (_vid_girl_pair.gid, _("Stop saying it like that! You're making it sound worse than it was!")),
                        (_watcher_pair.gid, _("Were you scared? I'd be terrified... I've never even seen one up close...")),
                        (_vid_girl_pair.gid, _tl(_("Can we PLEASE talk about this literally ANYWHERE except here?! %s, you're dead!")) % _pn_pair),
                    ],
                    _vid_girl_pair, _watcher_pair,
                )
            elif vid_type == "tj":
                return _fire(
                    "both_virgin_tj_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                    [
                        (_watcher_pair.gid, _tl(_("%s... your boobs are... around his... I don't even know what to say.")) % _vn_pair),
                        (_vid_girl_pair.gid, _("Then DON'T say anything! And stop staring at the video!")),
                        (_watcher_pair.gid, _("I'm not staring! I just... did it feel weird? Having it between your...")),
                        (_vid_girl_pair.gid, _("I am NOT answering that! We are BOTH virgins and this is a GROUP CHAT!")),
                        (_watcher_pair.gid, _("I know but... you've done more than me now and I have questions...")),
                        (_vid_girl_pair.gid, _tl(_("Ask me in private! NOT HERE! %s, I'm never trusting you with ANYTHING again!")) % _pn_pair),
                    ],
                    _vid_girl_pair, _watcher_pair,
                )
            elif vid_type == "hj":
                return _fire(
                    "both_virgin_hj_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                    [
                        (_watcher_pair.gid, _tl(_("You touched it?! With your HAND?! %s, we said we weren't doing anything!")) % _vn_pair),
                        (_vid_girl_pair.gid, _("It's just a handjob! That barely counts as anything!")),
                        (_watcher_pair.gid, _("It counts to ME! I've never even... what does it feel like?!")),
                        (_vid_girl_pair.gid, _("Why are you asking me that HERE?! And it's... warm? I don't know! Stop!")),
                        (_watcher_pair.gid, _("Warm?! That's all you're giving me? You owe me details. In private.")),
                        (_vid_girl_pair.gid, _tl(_("FINE! In private! Now can everyone please FORGET this video exists?! %s!!")) % _pn_pair),
                    ],
                    _vid_girl_pair, _watcher_pair,
                )
            elif vid_type == "masturbate":
                return _fire(
                    "both_virgin_mast_" + _vid_girl_pair.gid + "_" + _watcher_pair.gid,
                    [
                        (_watcher_pair.gid, _tl(_("%s... you do that too?! I thought I was the only one...")) % _vn_pair),
                        (_vid_girl_pair.gid, _("Everyone does it! And you weren't supposed to see that!")),
                        (_watcher_pair.gid, _("I know but... it's kind of relieving to know I'm not weird for...")),
                        (_vid_girl_pair.gid, _tl(_("You're NOT weird! But can we not bond over this in a GROUP CHAT?! %s!!!")) % _pn_pair),
                    ],
                    _vid_girl_pair, _watcher_pair,
                )

            # Both virgins: never fall through to FLOW 2 (which assumes one is experienced)
            return

        # Case: one thinks the other is virgin (not both)
        if _b_thinks_a_virgin and not _a_thinks_b_virgin:
            _supposed_virgin, _questioner = girl_a, girl_b
        elif _a_thinks_b_virgin and not _b_thinks_a_virgin:
            _supposed_virgin, _questioner = girl_b, girl_a

        # Determine actual status
        _still_virgin = _supposed_virgin and _is_virgin_or_was(_supposed_virgin) and hasattr(_supposed_virgin, "has_trait") and _supposed_virgin.has_trait("virgin")
        _was_virgin = _supposed_virgin and _is_virgin_or_was(_supposed_virgin) and not (_supposed_virgin.has_trait("virgin") if hasattr(_supposed_virgin, "has_trait") else True)

        # ==========================================================
        # FLOW 2: Girl IS still virgin + other KNOWS
        # hj/bj/tj -> teasing about "that's all you did?"
        # ==========================================================
        _sv_is_les = _supposed_virgin and hasattr(_supposed_virgin, "has_trait") and _supposed_virgin.has_trait("lesbian")
        _q_is_les = _questioner and hasattr(_questioner, "has_trait") and _questioner.has_trait("lesbian")

        if _still_virgin and _questioner and consensual and vid_type in ("hj", "bj", "tj") and _sv_is_les:

            if vid_gid == _supposed_virgin.gid:
                return _fire(
                    "lesvirgin_self_" + vid_type + "_" + _supposed_virgin.gid + "_" + _questioner.gid,
                    [
                        (_questioner.gid, _tl(_("Wait... you did THAT with %s? But you're a lesbian...?")) % pname),
                        (_supposed_virgin.gid, _("I AM a lesbian! It doesn't mean anything! I was pressured into it!")),
                        (_questioner.gid, _("Pressured? Girl, are you okay? That looks pretty intense...")),
                        (_supposed_virgin.gid, _("I'm FINE! I just... it happened. And it doesn't change who I am.")),
                        (_questioner.gid, _("Nobody said it does! But... doing that with a guy when you're gay...")),
                        (_supposed_virgin.gid, _tl(_("Can we NOT analyze my sexuality in the group chat?! %s, delete this!")) % pname),
                    ],
                    _supposed_virgin, _questioner,
                )

            if vid_gid == _questioner.gid:
                if _q_is_les:
                    return _fire(
                        "lesvirgin_otherles_" + vid_type + "_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_supposed_virgin.gid, _("You did that with a GUY?! I thought you were a lesbian like me!")),
                            (_questioner.gid, _("I am! What's wrong with it?")),
                            (_supposed_virgin.gid, _("Nothing! It's just... watching a girl with a man is weird for me.")),
                            (_questioner.gid, _("Then don't watch! And you're one to talk, virgin~")),
                            (_supposed_virgin.gid, _("I'm a virgin because I like WOMEN, not because I'm waiting!")),
                            (_questioner.gid, _("Fair point! Different reasons, same status~")),
                        ],
                        _supposed_virgin, _questioner,
                    )
                return _fire(
                    "lesvirgin_other_" + vid_type + "_" + _supposed_virgin.gid + "_" + _questioner.gid,
                    [
                        (_supposed_virgin.gid, _("I mean... good for you? It's just not something I'd ever do with a guy.")),
                        (_questioner.gid, _("Right, because you're... yeah. But you've never done anything at all?")),
                        (_supposed_virgin.gid, _("Not with a MAN. That's the key detail here.")),
                        (_questioner.gid, _("So you have done stuff with girls? Spill!")),
                        (_supposed_virgin.gid, _("I am NOT spilling anything in a group chat! Mind your business!")),
                        (_questioner.gid, _("Fine fine! But I have questions later~")),
                    ],
                    _supposed_virgin, _questioner,
                )

        if _still_virgin and _questioner and consensual and vid_type in ("hj", "bj", "tj"):

            # ── Virgin's OWN hj/bj/tj ──
            if vid_gid == _supposed_virgin.gid:

                if vid_type == "hj":
                    return _fire(
                        "virgin_self_hj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("Okay sooo... a handjob huh? That's all you did~?")),
                            (_supposed_virgin.gid, _("YES! That's all! Why are you saying it like that?!")),
                            (_questioner.gid, _("I'm just saying... you're alone with him, hand on his dick, and you stopped THERE?")),
                            (_supposed_virgin.gid, _("I wasn't READY for more! There's nothing wrong with that!")),
                            (_questioner.gid, _("No judgment! But like... wasn't it hard to stop? Be honest~")),
                            (_supposed_virgin.gid, _("...It was fine. I was totally in control. Completely.")),
                            (_questioner.gid, _tl(_("That pause says otherwise~ %s, she's going to crack eventually!")) % pname),
                            (_supposed_virgin.gid, _("I am NOT cracking! It was just a handjob and that's FINAL!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "bj":
                    return _fire(
                        "virgin_self_bj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("So you put his whole dick in your mouth but you won't go further? Girl...")),
                            (_supposed_virgin.gid, _("It's COMPLETELY different! A blowjob is not... you know... the real thing!")),
                            (_questioner.gid, _("You're on your knees with him in your mouth! That's pretty intimate!")),
                            (_supposed_virgin.gid, _("Intimate and SEX are two different things! I'm not ready for that yet!")),
                            (_questioner.gid, _tl(_("Yet! She said YET! %s did you hear that?!")) % pname),
                            (_supposed_virgin.gid, _("STOP reading into everything I say! I meant... ugh, you know what I meant!")),
                            (_questioner.gid, _("I know exactly what you meant~ You're getting there, slowly but surely~")),
                            (_supposed_virgin.gid, _("I'm getting NOWHERE! It was just a blowjob! END OF STORY!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "tj":
                    return _fire(
                        "virgin_self_tj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("A titjob! So your chest is fair game but everything else is off limits? Interesting~")),
                            (_supposed_virgin.gid, _("It's not 'off limits'! I'm just... taking things at my own pace!")),
                            (_questioner.gid, _("Your pace went from zero to tits-around-his-dick pretty fast though!")),
                            (_supposed_virgin.gid, _("That's different! It's not like we actually had sex!")),
                            (_questioner.gid, _("Girl, you're one step away! One tiny little step!")),
                            (_supposed_virgin.gid, _("A step I am NOT taking yet! I'll know when I'm ready!")),
                            (_questioner.gid, _("Based on this video you look VERY ready to me~")),
                            (_supposed_virgin.gid, _("Looking ready and BEING ready are NOT the same thing! Drop it!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

            # ── Other girl's hj/bj/tj — virgin sees it, other girl turns it around ──
            if vid_gid == _questioner.gid:

                # Check if the supposed virgin did these acts with player vs boyfriend
                _sv_flags = getattr(_supposed_virgin, "intimacy_flags", set()) or set()
                _sv_has_bf = hasattr(_supposed_virgin, "has_npc_partner") and _supposed_virgin.has_npc_partner()
                _sv_did_hj_player = "hj" in _sv_flags
                _sv_did_bj_player = "bj" in _sv_flags
                _sv_did_tj_player = "tj" in _sv_flags
                _sv_did_hj_bf = _sv_has_bf and hasattr(_supposed_virgin, "bf_has_done") and _supposed_virgin.bf_has_done("hj")
                _sv_did_bj_bf = _sv_has_bf and hasattr(_supposed_virgin, "bf_has_done") and _supposed_virgin.bf_has_done("bj")
                _sv_did_tj_bf = _sv_has_bf and hasattr(_supposed_virgin, "bf_has_done") and _supposed_virgin.bf_has_done("tj")

                if vid_type == "hj":
                    if _sv_did_hj_player:
                        _hj_msgs = [
                            (_supposed_virgin.gid, _tl(_("Okay well... at least it's just a handjob. I've {hint}done that{/hint} with %s too, no big deal.")) % pname),
                            (_questioner.gid, _tl(_("Oh you HAVE? So you and %s are getting closer huh~?")) % pname),
                            (_supposed_virgin.gid, _("Not THAT close! Hands are as far as it goes!")),
                            (_questioner.gid, _("For now~ That's what I said too! Then one thing led to another...")),
                            (_supposed_virgin.gid, _("Well I have more self-control than that!")),
                            (_questioner.gid, _tl(_("Self-control? Girl, have you SEEN %s? That only lasts so long!")) % pname),
                            (_supposed_virgin.gid, _("It will last as long as I WANT it to! I decide when I'm ready!")),
                            (_questioner.gid, _("Okay okay, I respect that! But I'm calling it now... before summer~")),
                        ]
                    elif _sv_did_hj_bf:
                        _supposed_virgin.discover("discovered_bf_done_hj")
                        _discover_partner(_supposed_virgin)
                        _hj_msgs = [
                            (_supposed_virgin.gid, _("It's just a handjob... I've {hint}done that with my boyfriend{/hint}, it's not a big deal.")),
                            (_questioner.gid, _tl(_("With your BOYFRIEND? But not with %s? That's interesting...")) % pname),
                            (_supposed_virgin.gid, _("What's interesting about it?! He's my {hint}boyfriend{/hint}, of course I've done stuff with him!")),
                            (_questioner.gid, _("I just thought you were 'saving everything'... turns out there are levels to this~")),
                            (_supposed_virgin.gid, _("There ARE levels! And the top level stays with my {hint}boyfriend{/hint}!")),
                            (_questioner.gid, _tl(_("For now~ You say that now but %s has a way of changing minds...")) % pname),
                            (_supposed_virgin.gid, _("My mind is NOT changing! I know my limits!")),
                            (_questioner.gid, _("Limits that already include {hint}handjobs with your boyfriend{/hint}. Just saying~")),
                        ]
                    else:
                        _hj_msgs = [
                            (_supposed_virgin.gid, _("I mean... it's just a handjob. That's not THAT wild...")),
                            (_questioner.gid, _("Says the virgin~ Easy to judge when you haven't tried it!")),
                            (_supposed_virgin.gid, _("I'm not judging! I just said it's not that shocking!")),
                            (_questioner.gid, _("Uh huh. You should try it sometime. You might like it~")),
                            (_supposed_virgin.gid, _("I'll try things when I'm READY! Stop pressuring me!")),
                            (_questioner.gid, _("Not pressuring! Just planting seeds~")),
                        ]
                    return _fire(
                        "virgin_other_hj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        _hj_msgs, _supposed_virgin, _questioner,
                    )

                if vid_type == "bj":
                    if _sv_did_bj_player:
                        _bj_msgs = [
                            (_supposed_virgin.gid, _tl(_("I mean... I've {hint}given %s blowjobs{/hint} too so this isn't THAT shocking...")) % pname),
                            (_questioner.gid, _("You have?! But you won't go all the way? That's the most confusing logic!")),
                            (_supposed_virgin.gid, _("It's not confusing! Oral is oral, sex is sex! Big difference!")),
                            (_questioner.gid, _("His dick was literally in your mouth! What's one more step?!")),
                            (_supposed_virgin.gid, _("One more step?! It's a huge step! You don't just... casually do that!")),
                            (_questioner.gid, _("Girl I promise you it's not as scary as you think!")),
                            (_supposed_virgin.gid, _("Easy for you to say! You've already done it!")),
                            (_questioner.gid, _("Exactly! And I survived! You will too, when you're ready~")),
                        ]
                    elif _sv_did_bj_bf:
                        _supposed_virgin.discover("discovered_bf_done_bj")
                        _discover_partner(_supposed_virgin)
                        _bj_msgs = [
                            (_supposed_virgin.gid, _("I've {hint}done that with my boyfriend{/hint} before... oral isn't THAT big of a deal.")),
                            (_questioner.gid, _("With your {hint}boyfriend{/hint}?! But you're still a {hint}virgin{/hint}? Girl, where do you draw the line?!")),
                            (_supposed_virgin.gid, _("The line is clear! Mouth stuff is one thing, actual sex is completely different!")),
                            (_questioner.gid, _("You've had his dick in your mouth but won't let him inside?! Make it make sense!")),
                            (_supposed_virgin.gid, _("It DOES make sense! I'm saving THAT for when I'm truly ready!")),
                            (_questioner.gid, _tl(_("Ready? You're already on your knees for your {hint}boyfriend{/hint}! %s must be so confused~")) % pname),
                            (_supposed_virgin.gid, _("He's NOT confused! He respects my boundaries! Unlike SOME people!")),
                            (_questioner.gid, _("Okay okay! But the mental gymnastics here are Olympic-level, just saying~")),
                        ]
                    else:
                        _bj_msgs = [
                            (_supposed_virgin.gid, _("A blowjob... okay that's a bit more than I expected from you.")),
                            (_questioner.gid, _("Says the girl who won't even try! Maybe you should take notes~")),
                            (_supposed_virgin.gid, _("I don't need notes! I'll figure it out when the time comes!")),
                            (_questioner.gid, _("IF the time comes~ At this rate I'll be a grandma first!")),
                            (_supposed_virgin.gid, _("Oh shut up! Not everyone moves at your speed!")),
                            (_questioner.gid, _("Fair enough! But the offer to give pointers stands~")),
                        ]
                    return _fire(
                        "virgin_other_bj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        _bj_msgs, _supposed_virgin, _questioner,
                    )

                if vid_type == "tj":
                    if _sv_did_tj_player:
                        _tj_msgs = [
                            (_supposed_virgin.gid, _tl(_("A titjob... I've {hint}done that{/hint} with %s too. It's not THAT crazy.")) % pname),
                            (_questioner.gid, _("So you'll wrap your tits around him but won't let him inside? Make it make sense!")),
                            (_supposed_virgin.gid, _("It makes PERFECT sense! There's a line and I'm not crossing it yet!")),
                            (_questioner.gid, _("Where even IS the line at this point? You've done everything BUT!")),
                            (_supposed_virgin.gid, _("The line is penetration! And it stays there until I say otherwise!")),
                            (_questioner.gid, _("Okay fair enough! But you're running out of 'everything but'~")),
                            (_supposed_virgin.gid, _("I am NOT! There's plenty of stuff that isn't... the full thing!")),
                            (_questioner.gid, _("Sure babe~ Just remember there's nothing wrong with wanting more!")),
                        ]
                    elif _sv_did_tj_bf:
                        _supposed_virgin.discover("discovered_bf_done_tj")
                        _discover_partner(_supposed_virgin)
                        _tj_msgs = [
                            (_supposed_virgin.gid, _("A titjob... I've {hint}done that with my boyfriend{/hint}. It's really not a big deal.")),
                            (_questioner.gid, _tl(_("With your {hint}boyfriend{/hint}? So your boobs are fair game for him but not %s?")) % pname),
                            (_supposed_virgin.gid, _("He's my BOYFRIEND! Of course he gets more than... anyone else!")),
                            (_questioner.gid, _("More but not ALL? The suspense must be killing the poor guy~")),
                            (_supposed_virgin.gid, _("He RESPECTS that I'm not ready! Unlike some people in this chat!")),
                            (_questioner.gid, _("I respect it too! I'm just amazed at the willpower. Tits out but no entry~")),
                            (_supposed_virgin.gid, _("When I'm ready, I'm ready! End of discussion!")),
                            (_questioner.gid, _("Fine fine! But your boyfriend is either the most patient or most frustrated man alive~")),
                        ]
                    else:
                        _tj_msgs = [
                            (_supposed_virgin.gid, _("A titjob... okay, that's a lot more than I've done...")),
                            (_questioner.gid, _("You sound curious~ Want me to tell you how it feels?")),
                            (_supposed_virgin.gid, _("NO! I mean... not in the group chat! I was just... observing!")),
                            (_questioner.gid, _("Observing with very wide eyes~ It's okay to be curious, you know!")),
                            (_supposed_virgin.gid, _("I'm not curious! I'm just... surprised! That's all!")),
                            (_questioner.gid, _("Sure~ 'Surprised' and still watching the video on repeat~")),
                        ]
                    return _fire(
                        "virgin_other_tj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        _tj_msgs, _supposed_virgin, _questioner,
                    )

        # ==========================================================
        # FLOW 3: Girl THINKS other is virgin but she ALREADY LOST IT
        # hj/bj/tj -> "wait aren't you a virgin?" + awkward deflection
        # ==========================================================
        if _was_virgin and _questioner and consensual and vid_type in ("hj", "bj", "tj"):

            if vid_gid == _supposed_virgin.gid:

                if vid_type == "hj":
                    return _fire(
                        "exvirgin_self_hj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("A handjob huh? Well, at least it's just hands... I mean, you're still... you know.")),
                            (_supposed_virgin.gid, _("Still what?")),
                            (_questioner.gid, _("You know... a virgin? You haven't gone all the way, right?")),
                            (_supposed_virgin.gid, _("I... well... that's... none of your business!")),
                            (_questioner.gid, _("Wait. Why are you being weird about it? OH MY GOD. Did you?!")),
                            (_supposed_virgin.gid, _("I didn't say that! I just said it's none of your business!")),
                            (_questioner.gid, _("Your face is SO red right now! You totally did! When?! How?! DETAILS!")),
                            (_supposed_virgin.gid, _("There are NO details! Nothing happened! Can we just watch the video?!")),
                            (_questioner.gid, _("The video of you jerking him off? Sure. While you pretend you haven't done MORE~")),
                            (_supposed_virgin.gid, _("I am NOT having this conversation!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "bj":
                    return _fire(
                        "exvirgin_self_bj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("You're giving blowjobs now? Last I heard you were still... taking it slow.")),
                            (_supposed_virgin.gid, _("I AM taking it slow! A blowjob isn't... it's not the same as...")),
                            (_questioner.gid, _("As what? Sex? Wait... why did you hesitate just now?")),
                            (_supposed_virgin.gid, _("I didn't hesitate! I was just... choosing my words!")),
                            (_questioner.gid, _("Choosing your words?! Oh no. OH NO. You lost it, didn't you?!")),
                            (_supposed_virgin.gid, _("WHAT?! No! Why would you even... that's ridiculous!")),
                            (_questioner.gid, _("You're a terrible liar! Your ears are red! They ALWAYS get red when you lie!")),
                            (_supposed_virgin.gid, _("My ears are NOT... okay it's warm in here! That's all!")),
                            (_questioner.gid, _tl(_("%s, look at her face. She is LYING. I know it. She KNOWS I know it.")) % pname),
                            (_supposed_virgin.gid, _("Nobody knows anything because there is nothing to know! Next video!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "tj":
                    return _fire(
                        "exvirgin_self_tj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("A titjob! At least that's... safe territory for you, right? Since you're still...")),
                            (_supposed_virgin.gid, _("Since I'm still what? Just say it.")),
                            (_questioner.gid, _("You know! Since you haven't done the real thing yet!")),
                            (_supposed_virgin.gid, _("...Right. Yeah. I haven't. Obviously.")),
                            (_questioner.gid, _("That was the LEAST convincing 'obviously' I have ever heard.")),
                            (_supposed_virgin.gid, _("What do you want me to say?! It was a titjob! That's it!")),
                            (_questioner.gid, _tl(_("I want you to say the truth! Did something else happen with %s?!")) % pname),
                            (_supposed_virgin.gid, _("Nothing! Happened! I used my boobs! End of story! Can we move on?!")),
                            (_questioner.gid, _("Fine! But I'm watching you! One slip and I'll get the truth out of you!")),
                            (_supposed_virgin.gid, _("There IS no truth to get! You're imagining things!")),
                        ],
                        _supposed_virgin, _questioner,
                    )

            # ── Questioner's hj/bj/tj — ex-virgin watches, questioner pokes ──
            if vid_gid == _questioner.gid:

                if vid_type == "hj":
                    return _fire(
                        "exvirgin_other_hj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_supposed_virgin.gid, _("A handjob... yeah, I've {hint}done that too{/hint}. It's no big deal.")),
                            (_questioner.gid, _("No big deal, huh? So hands are fine... what about everything else~?")),
                            (_supposed_virgin.gid, _("What do you mean 'everything else'? Hands are... hands.")),
                            (_questioner.gid, _("You're being very careful with your words lately. Something you want to share?")),
                            (_supposed_virgin.gid, _("Nope. Nothing. Zero. My life is very boring, thank you.")),
                            (_questioner.gid, _("Uh huh. Your 'boring' life sure involves a lot of blushing.")),
                            (_supposed_virgin.gid, _("It's HOT in here! That's literally all it is!")),
                            (_questioner.gid, _("Sure, babe. I believe you. Totally~")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "bj":
                    return _fire(
                        "exvirgin_other_bj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_supposed_virgin.gid, _("I've {hint}done that too{/hint}, so... I'm not going to judge.")),
                            (_questioner.gid, _("You're not going to judge? How mature of you. So what ELSE have you done?")),
                            (_supposed_virgin.gid, _("What else? Nothing else! Blowjobs and hands, that's my limit!")),
                            (_questioner.gid, _("Your 'limit'? Interesting word choice. Sounds temporary~")),
                            (_supposed_virgin.gid, _("It's not temporary! It's... permanent! Very permanent!")),
                            (_questioner.gid, _("Nobody who is SURE says 'very permanent.' You sound like you're convincing yourself.")),
                            (_supposed_virgin.gid, _("I am convincing YOU! Because you won't drop it!")),
                            (_questioner.gid, _("Okay okay! Lips are sealed! ...Unlike yours apparently~")),
                            (_supposed_virgin.gid, _("I SWEAR TO GOD...")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "tj":
                    return _fire(
                        "exvirgin_other_tj_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_supposed_virgin.gid, _("Titjobs are fine, I've {hint}done those{/hint}. It's not like it's actual sex.")),
                            (_questioner.gid, _("You really love drawing that line, don't you? 'It's not ACTUAL sex.'")),
                            (_supposed_virgin.gid, _("Because it's NOT! There's a clear difference!")),
                            (_questioner.gid, _("A difference you seem VERY invested in maintaining. Makes me wonder why~")),
                            (_supposed_virgin.gid, _("Because people keep ASKING! Not because I'm hiding anything!")),
                            (_questioner.gid, _("I didn't say you were hiding anything. But now that YOU brought it up...")),
                            (_supposed_virgin.gid, _("I didn't bring anything up! You twisted my words!")),
                            (_questioner.gid, _("Relax! I'm just teasing! ...mostly~")),
                        ],
                        _supposed_virgin, _questioner,
                    )

        # ==========================================================
        # FLOW 2: Girl IS still virgin + other KNOWS
        # Penetration vids of THE VIRGIN (consensual)
        # The other girl thought she was a virgin. Now she sees her
        # getting fucked on video. Total disbelief.
        # Also covers FLOW 3 (thought virgin, sees penetration = shock)
        # ==========================================================
        if (_still_virgin or _was_virgin) and _questioner and consensual and vid_type in ("cowgirl", "reverse_cowgirl", "creampie") and _sv_is_les:

            if vid_gid == _supposed_virgin.gid:
                _vp_result = _fire(
                    "lesvirgin_self_pen_" + _supposed_virgin.gid + "_" + _questioner.gid,
                    [
                        (_questioner.gid, _("WAIT. Is that YOU?! With a GUY?! But you're a LESBIAN!")),
                        (_supposed_virgin.gid, _("I KNOW what I am! This doesn't change anything!")),
                        (_questioner.gid, _("You told everyone you'd never be with a man! And now you're on video doing exactly that?!")),
                        (_supposed_virgin.gid, _("I was... it's complicated! I didn't plan this! None of this was supposed to happen!")),
                        (_questioner.gid, _("Girl... are you okay? Did he pressure you into this?")),
                        (_supposed_virgin.gid, _tl(_("Just... don't. Please. I can't talk about this right now. %s, DELETE IT.")) % pname),
                    ],
                    _supposed_virgin, _questioner,
                )
                if _vp_result is not None:
                    Change_Status(_questioner, "Obed", 12)
                    Change_Status(_questioner, "Inbt", 15)
                    Change_Status(_supposed_virgin, "Obed", 8)
                    Change_Status(_supposed_virgin, "Inbt", 10)
                    if hasattr(_questioner, "knows_virgin") and _supposed_virgin.gid in _questioner.knows_virgin:
                        del _questioner.knows_virgin[_supposed_virgin.gid]
                    return _vp_result

        if (_still_virgin or _was_virgin) and _questioner and consensual and vid_type in ("cowgirl", "reverse_cowgirl", "creampie"):

            if vid_gid == _supposed_virgin.gid:

                _vp_result = None

                if vid_type == "cowgirl":
                    _vp_result = _fire(
                        "virgin_self_cowgirl_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("WAIT. Hold on. HOLD ON. Is that YOU?! On TOP of him?! RIDING him?!")),
                            (_supposed_virgin.gid, _("Oh god... oh no... you weren't supposed to see this...")),
                            (_questioner.gid, _("You told me you were a VIRGIN! And now you're bouncing on his dick like a pro?!")),
                            (_supposed_virgin.gid, _("I WAS a virgin! This was... it was my first time! It just happened!")),
                            (_questioner.gid, _("Your FIRST TIME and you went cowgirl?! Most people don't even do that until like their fifth time!")),
                            (_supposed_virgin.gid, _("I don't know!! I just... got on top and it felt... I didn't think about it!")),
                            (_questioner.gid, _("Didn't think about it?! Girl, you're GRINDING. You clearly thought about it plenty~")),
                            (_supposed_virgin.gid, _("STOP analyzing the video! Oh my god, I can never look at you again...")),
                            (_questioner.gid, _tl(_("%s, I'm impressed. You turned the virgin into a cowgirl on day one. Respect.")) % pname),
                            (_supposed_virgin.gid, _("I HATE both of you right now.")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type in ("reverse_cowgirl", "doggy"):
                    # RCG/doggy share cowgirl virgin dialogue for now
                    _vp_result = _fire(
                        "virgin_self_rcg_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("WAIT. Hold on. HOLD ON. Is that YOU?! On TOP of him?! RIDING him?!")),
                            (_supposed_virgin.gid, _("Oh god... oh no... you weren't supposed to see this...")),
                            (_questioner.gid, _("You told me you were a VIRGIN! And now you're bouncing on his dick like a pro?!")),
                            (_supposed_virgin.gid, _("I WAS a virgin! This was... it was my first time! It just happened!")),
                            (_questioner.gid, _("Your FIRST TIME and you went cowgirl?! Most people don't even do that until like their fifth time!")),
                            (_supposed_virgin.gid, _("I don't know!! I just... got on top and it felt... I didn't think about it!")),
                            (_questioner.gid, _("Didn't think about it?! Girl, you're GRINDING. You clearly thought about it plenty~")),
                            (_supposed_virgin.gid, _("STOP analyzing the video! Oh my god, I can never look at you again...")),
                            (_questioner.gid, _tl(_("%s, I'm impressed. You turned the virgin into a cowgirl on day one. Respect.")) % pname),
                            (_supposed_virgin.gid, _("I HATE both of you right now.")),
                        ],
                        _supposed_virgin, _questioner,
                    )

                if vid_type == "creampie":
                    # "I'm on the pill" is a claim about HER (_gv_claims_birth_control): otherwise she has no comeback
                    _vs_pill = _gv_claims_birth_control(_supposed_virgin)
                    _vp_result = _fire(
                        "virgin_self_creampie_" + _supposed_virgin.gid + "_" + _questioner.gid,
                        [
                            (_questioner.gid, _("GIRL. WHAT. THE. FUCK. Is that you getting CREAMPIED?!")),
                            (_supposed_virgin.gid, _("I... I can explain...")),
                            (_questioner.gid, _("You were a VIRGIN last week! And now he came INSIDE you?! WITHOUT protection?!")),
                            (_supposed_virgin.gid, _("It wasn't planned! We were doing it and he was about to finish and I... I said don't pull out...")),
                            (_questioner.gid, _("YOU said it?! The VIRGIN told him to cum inside her?! On her FIRST TIME?!")),
                            (_supposed_virgin.gid, _("I don't know what came over me! It felt so good and I just... said it without thinking!")),
                            (_questioner.gid, _("Without THINKING?! Do you know what happens when you don't think?! BABIES HAPPEN!")),
                            (_supposed_virgin.gid, _tl(_("I'm on the pill! I'm not stupid! I just... wanted to feel it... all of it...")) if _vs_pill
                             else _tl(_("I know! I KNOW! Don't remind me! It just... happened!"))),
                            (_questioner.gid, _("From 'I'm saving myself' to 'cum inside me' in one session. I'm actually in awe.")),
                            (_supposed_virgin.gid, _("I DID NOT SAY THAT! Oh my god, I want to crawl into a hole and never come out!")),
                            (_questioner.gid, _tl(_("%s... what did you DO to this girl? She was innocent like three days ago!")) % pname),
                        ],
                        _supposed_virgin, _questioner,
                    )
                    if _vp_result is not None:
                        print("[GROUP_VIDEO] virgin_self_creampie %s: pill line=%s (on_pill=%s placebo=%s pregnant=%s known=%s mode=%s)" % (
                            _supposed_virgin.gid, _vs_pill, getattr(_supposed_virgin, "_on_pill", False),
                            getattr(_supposed_virgin, "_on_placebo", False), getattr(_supposed_virgin, "_pregnant", False),
                            getattr(_supposed_virgin, "_pregnancy_known", False), store._pregnancy_mode))

                # Apply bonus stats + clear virgin belief
                if _vp_result is not None:
                    Change_Status(_questioner, "Obed", 12)
                    Change_Status(_questioner, "Inbt", 15)
                    Change_Status(_supposed_virgin, "Obed", 8)
                    Change_Status(_supposed_virgin, "Inbt", 10)
                    # She now knows the truth
                    if hasattr(_questioner, "knows_virgin") and _supposed_virgin.gid in _questioner.knows_virgin:
                        del _questioner.knows_virgin[_supposed_virgin.gid]
                    return _vp_result

        # ── Actual virgin sees penetration vid of the other girl ──
        # This does NOT require prior knowledge - the scene IS the discovery
        # Works with knowledge-gated _supposed_virgin OR direct trait check
        _real_virgin = None
        _real_other = None
        if hasattr(girl_a, "has_trait") and girl_a.has_trait("virgin"):
            _real_virgin, _real_other = girl_a, girl_b
        elif hasattr(girl_b, "has_trait") and girl_b.has_trait("virgin"):
            _real_virgin, _real_other = girl_b, girl_a

        if _real_virgin and _real_other and consensual:
            _rv_is_les = hasattr(_real_virgin, "has_trait") and _real_virgin.has_trait("lesbian")
            if vid_gid == _real_other.gid and vid_type in ("cowgirl", "reverse_cowgirl", "sex", "creampie", "anal"):
                girl_learns_virgin(_real_other, _real_virgin)
                if _rv_is_les:
                    return _fire(
                        "lesvirgin_pen_other_" + _real_virgin.gid + "_" + _real_other.gid,
                        [
                            (_real_virgin.gid, _("Wow... you really let him do all that?")),
                            (_real_other.gid, _("What? It felt good! Haven't you ever...?")),
                            (_real_virgin.gid, _("With a GUY? No. I'm... not into that.")),
                            (_real_other.gid, _("Oh! I didn't realize. So you've never...?")),
                            (_real_virgin.gid, _("Not with a man. And I don't plan to. She looks like she's enjoying it though...")),
                            (_real_other.gid, _("She?! You mean ME?! And yes, I was! Don't look so judgmental!")),
                            (_real_virgin.gid, _("I'm not judging! It's just... a completely foreign world to me.")),
                        ],
                        _real_virgin, _real_other,
                    )
                return _fire(
                    "virgin_pen_other_" + _real_virgin.gid + "_" + _real_other.gid,
                    [
                        (_real_virgin.gid, _("Oh... so that's what it really looks like...")),
                        (_real_other.gid, _("Don't tell me you've never watched something like this before?")),
                        (_real_virgin.gid, _("Not with someone I KNOW! It's different when it's real!")),
                        (_real_other.gid, _("So... you haven't done it yet? Like, for real?")),
                        (_real_virgin.gid, _("...No. I haven't. Happy now?")),
                        (_real_other.gid, _("No judgment! Seriously! Does it... make you nervous watching it?")),
                        (_real_virgin.gid, _("A little... it looks like a lot. Does it hurt?")),
                        (_real_other.gid, _("Only at first! After that it's... well... you'll find out when you're ready~")),
                        (_real_virgin.gid, _("IF! Not when! ...but thanks for being honest about it.")),
                    ],
                    _real_virgin, _real_other,
                )

        # ==========================================================
        # RELATIONSHIP SCENARIOS — based on dating status & history
        # Clear pair traits (no trait discovery for relationship-based convos)
        _pair_traits[0] = None
        _pair_traits[1] = None
        # ==========================================================
        _a_dating = hasattr(girl_a, "is_dating_player") and girl_a.is_dating_player()
        _b_dating = hasattr(girl_b, "is_dating_player") and girl_b.is_dating_player()
        _a_acts = getattr(girl_a, "Sex_acts", {})
        _b_acts = getattr(girl_b, "Sex_acts", {})
        _a_did_stuff = any(v > 0 for k, v in _a_acts.items() if k != "kiss")
        _b_did_stuff = any(v > 0 for k, v in _b_acts.items() if k != "kiss")

        # Girl_like: 0-1000. < 250 = hostile, 750+ = close/best friends
        _a_likes_b = int(girl_a.Girl_like.get(girl_b.gid, 500)) if hasattr(girl_a, "Girl_like") else 500
        _b_likes_a = int(girl_b.Girl_like.get(girl_a.gid, 500)) if hasattr(girl_b, "Girl_like") else 500

        # ==========================================================
        # BOTH DATING — one did stuff, the other didn't (consensual)
        # The experienced one is possessive/smug, the innocent one
        # is jealous/insecure about not having gone as far.
        # ==========================================================
        if _a_dating and _b_dating and consensual:

            experienced = None
            innocent = None
            if _a_did_stuff and not _b_did_stuff:
                experienced, innocent = girl_a, girl_b
            elif _b_did_stuff and not _a_did_stuff:
                experienced, innocent = girl_b, girl_a

            if experienced and innocent:

                # ── Video is of the experienced girl ──
                if vid_gid == experienced.gid:
                    return _fire(
                        "dating_exp_self_" + experienced.gid + "_" + innocent.gid,
                        [
                            (experienced.gid, _tl(_("Yeah, that's me~ %s and I have been... busy~")) % pname),
                            (innocent.gid, _("You've done THAT with him?! We're both dating him and he's... doing THIS with you?!")),
                            (experienced.gid, _("What can I say? Things just happened naturally! He couldn't resist~")),
                            (innocent.gid, _("We haven't even... I mean he hasn't tried anything like that with ME!")),
                            (experienced.gid, _("Maybe you need to be more... forward? He responds really well to initiative~")),
                            (innocent.gid, _("Forward?! I shouldn't HAVE to be! Does he even like me as much as you?!")),
                            (experienced.gid, _("Of course he does! It's not a competition... but if it was, I'd be winning~")),
                            (innocent.gid, _tl(_("%s!! We need to talk. Seriously. Why haven't you... why am I always the last one?!")) % pname),
                        ],
                        experienced, innocent,
                    )

                # ── Video is of the innocent girl (hj/bj/tj only since she hasn't done more) ──
                if vid_gid == innocent.gid:
                    return _fire(
                        "dating_inn_self_" + innocent.gid + "_" + experienced.gid,
                        [
                            (innocent.gid, _tl(_("%s! You sent this?! That was supposed to be our private moment!")) % pname),
                            (experienced.gid, _("Aww, that's cute! I remember when I was at that stage too~")),
                            (innocent.gid, _("At that STAGE? What's that supposed to mean?!")),
                            (experienced.gid, _tl(_("Nothing! Just that... %s and I have moved a bit further, that's all~")) % pname),
                            (innocent.gid, _("Further?! How much further?! What have you two done?!")),
                            (experienced.gid, _("Wouldn't you like to know~ Let's just say that video is... tame compared to ours~")),
                            (innocent.gid, _tl(_("I can't believe this. Am I the only one who hasn't... %s, do you even care about me?!")) % pname),
                            (experienced.gid, _("Relax girl! Everyone goes at their own pace! Yours is just... slower~")),
                        ],
                        innocent, experienced,
                    )

            # ==========================================================
            # BOTH DATING — both have done stuff with player (consensual)
            # Rivalry, jealousy, comparing experiences.
            # ==========================================================
            if _a_did_stuff and _b_did_stuff:

                # Video is of girl A
                if vid_gid == girl_a.gid:
                    return _fire(
                        "dating_both_a_" + girl_a.gid + "_" + girl_b.gid,
                        [
                            (girl_b.gid, _("So... I'm looking at MY boyfriend with another girl. In a GROUP CHAT. Cool!")),
                            (girl_a.gid, _("YOUR boyfriend? Last time I checked, he's MY boyfriend too!")),
                            (girl_b.gid, _("And he sent a video of YOU to both of us?! What is he thinking?!")),
                            (girl_a.gid, _("Maybe he's thinking I look better than you in this video~")),
                            (girl_b.gid, _("Excuse me?! I could send a video right now that would make yours look amateur!")),
                            (girl_a.gid, _tl(_("Then do it! I dare you! %s can judge who's better!")) % pname),
                            (girl_b.gid, _tl(_("%s!! You have TWO girlfriends watching this right now! Explain yourself!")) % pname),
                            (girl_a.gid, _tl(_("Yeah %s! Explain! ...but also, tell her I'm better~")) % pname),
                        ],
                        girl_b, girl_a,
                    )

                # Video is of girl B
                if vid_gid == girl_b.gid:
                    return _fire(
                        "dating_both_b_" + girl_b.gid + "_" + girl_a.gid,
                        [
                            (girl_a.gid, _("Oh great. My boyfriend sent a video of his OTHER girlfriend. Wonderful.")),
                            (girl_b.gid, _("Don't be jealous~ He clearly couldn't wait to show me off!")),
                            (girl_a.gid, _("Show you off?! He does the same things with ME! You're not special!")),
                            (girl_b.gid, _("Not special? Then why did he film ME and send it~?")),
                            (girl_a.gid, _tl(_("Because he filmed me LAST WEEK! %s, tell her!")) % pname),
                            (girl_b.gid, _("Girl, he told me I was the best he ever had!")),
                            (girl_a.gid, _tl(_("He told me the SAME THING! %s you are in SO much trouble!")) % pname),
                            (girl_b.gid, _tl(_("Okay at least we agree on one thing! %s is a LIAR!")) % pname),
                        ],
                        girl_a, girl_b,
                    )

                # Video is of a third girl — both GFs react
                if vid_gid != girl_a.gid and vid_gid != girl_b.gid:
                    vid_girl_name = vid_girl.Name if vid_girl else "her"
                    return _fire(
                        "dating_both_other_" + girl_a.gid + "_" + girl_b.gid,
                        [
                            (girl_a.gid, _tl(_("...Are you KIDDING me?! A THIRD girl?! %s!!")) % pname),
                            (girl_b.gid, _tl(_("Wait... that's not me and that's not you... WHO IS %s?!")) % vid_girl_name),
                            (girl_a.gid, _("He has TWO girlfriends and he's STILL out there with other girls?!")),
                            (girl_b.gid, _("I can't believe we BOTH weren't enough! The audacity!")),
                            (girl_a.gid, _tl(_("For once we agree on something. %s is unbelievable!")) % pname),
                            (girl_b.gid, _("You know what? Maybe WE should team up against him!")),
                            (girl_a.gid, _tl(_("I never thought I'd say this, but... I'm in. %s, you're DONE!")) % pname),
                            (girl_b.gid, _("United front! He can't play us BOTH and get away with it!")),
                        ],
                        girl_a, girl_b,
                    )

        # ==========================================================
        # BEST FRIENDS — Girl_like >= 750 both ways (consensual)
        # Supportive, teasing, gossipy, girl-talk energy.
        # ==========================================================
        if _a_likes_b >= 750 and _b_likes_a >= 750 and consensual:

            if vid_gid == girl_a.gid:
                return _fire(
                    "besties_a_self_" + girl_a.gid + "_" + girl_b.gid,
                    [
                        (girl_b.gid, _("GIRL!! Is that you?! Oh my god oh my god!!")),
                        (girl_a.gid, _("I KNOW right?! I can't believe he sent it here but also... I look good?")),
                        (girl_b.gid, _tl(_("You look AMAZING! The way you move?! %s is so lucky!")) % pname),
                        (girl_a.gid, _("Stooop you're making me blush! But like... was it too much?")),
                        (girl_b.gid, _("Too much?! Girl this is art! I'm saving this as motivation!")),
                        (girl_a.gid, _("Motivation?! For what exactly?!")),
                        (girl_b.gid, _("For when it's MY turn! I need to match this energy!")),
                        (girl_a.gid, _tl(_("LMAO okay bestie! %s you better treat her just as good!")) % pname),
                    ],
                    girl_b, girl_a,
                )

            if vid_gid == girl_b.gid:
                return _fire(
                    "besties_b_self_" + girl_b.gid + "_" + girl_a.gid,
                    [
                        (girl_a.gid, _("Bestie!! That's you!! Oh my god I'm screaming!")),
                        (girl_b.gid, _("Shut up! I know! I can't believe he actually sent it!")),
                        (girl_a.gid, _("You look so HOT! Like seriously, I'm jealous!")),
                        (girl_b.gid, _("Jealous?! YOU?! Girl please, you'd look ten times better!")),
                        (girl_a.gid, _("Stop lying! That hip thing you did at the end? TEACH ME!")),
                        (girl_b.gid, _("Omg okay when we hang out I'll show you the technique! It's all in the...")),
                        (girl_a.gid, _tl(_("WAIT not in the group chat! %s is reading this!")) % pname),
                        (girl_b.gid, _("Let him read! Maybe he'll appreciate us both even more~")),
                    ],
                    girl_a, girl_b,
                )

            # Third girl video — besties gossip together
            if vid_gid != girl_a.gid and vid_gid != girl_b.gid:
                vid_girl_name = vid_girl.Name if vid_girl else "her"
                return _fire(
                    "besties_other_" + girl_a.gid + "_" + girl_b.gid,
                    [
                        (girl_a.gid, _tl(_("Omg bestie are you seeing this?! %s and %s!!")) % (pname, vid_girl_name)),
                        (girl_b.gid, _("I'M SEEING IT! I'm literally watching it right now!")),
                        (girl_a.gid, _("What do you think? Rate it honestly! I give it a 7!")),
                        (girl_b.gid, _("A 7?! That's generous! I'd say a 6. We could do better!")),
                        (girl_a.gid, _("Right?! Like... the energy is off? She's not matching his rhythm!")),
                        (girl_b.gid, _("Exactly! Girl, if that was me I would've...")),
                        (girl_a.gid, _("Don't say it don't say it!")),
                        (girl_b.gid, _tl(_("Too late! %s, my bestie and I have notes for you!")) % pname),
                    ],
                    girl_a, girl_b,
                )

        # ==========================================================
        # EX-GIRLFRIEND — video was filmed when vid_girl dated the player
        # but she no longer dates him. Both girls are in the group.
        # ==========================================================
        _vid_was_dating = _vid_snap(vid, "was_dating", False)
        if _vid_was_dating and vid_girl:
            _ex_still_dating = hasattr(vid_girl, "is_dating_player") and vid_girl.is_dating_player()
            if not _ex_still_dating:
                # vid_girl is now the player's EX
                _ex_girl = vid_girl
                _other_ex = girl_b if _ex_girl.gid == girl_a.gid else girl_a

                if vid_gid == _ex_girl.gid:
                    # ── Ex-GF's video sent to the group — other girl reacts ──

                    if _other_ex and hasattr(_other_ex, "is_dating_player") and _other_ex.is_dating_player():
                        # Current GF sees ex-GF's video in group with ex present
                        _ex_r = _fire(
                            "ex_gf_current_gf_" + _ex_girl.gid + "_" + _other_ex.gid,
                            [
                                (_other_ex.gid, _("Wait... this is from when YOU were his girlfriend? And he's sharing it HERE?!")),
                                (_ex_girl.gid, _("I didn't ask for this! We broke up! That video was supposed to be PRIVATE!")),
                                (_other_ex.gid, _tl(_("Private?! It's in our group chat now! %s, what is WRONG with you?!")) % pname),
                                (_ex_girl.gid, _("See?! This is exactly the kind of thing he does! You'll learn the hard way!")),
                                (_other_ex.gid, _("Don't project YOUR relationship issues onto mine!")),
                                (_ex_girl.gid, _("Issues?! He literally just sent YOUR current boyfriend's sex tape with his EX to a group chat!")),
                                (_other_ex.gid, _tl(_("...Okay that IS pretty fucked up. %s, you better have a REALLY good explanation.")) % pname),
                            ],
                            _ex_girl, _other_ex,
                        )
                        if _ex_r:
                            Change_Status(_other_ex, "Love", -8)
                            Change_Status(_ex_girl, "Love", -10)
                            Change_Status(_ex_girl, "Obed", 5)
                            return _ex_r
                    else:
                        # Non-GF sees ex-GF video, ex is present
                        _ex_r = _fire(
                            "ex_gf_other_" + _ex_girl.gid + "_" + _other_ex.gid,
                            [
                                (_other_ex.gid, _("Hold on... weren't you two together when this was filmed?")),
                                (_ex_girl.gid, _("Yes. We were dating. And now he's sending it around like it's nothing.")),
                                (_other_ex.gid, _("That's really messed up... are you okay?")),
                                (_ex_girl.gid, _("I'm FINE. It's just... I trusted him with that. And now everyone is seeing it.")),
                                (_other_ex.gid, _tl(_("%s, that's pretty low. Even for you. She was your girlfriend.")) % pname),
                                (_ex_girl.gid, _("Whatever. It's done now. Just... don't rewatch it, okay?")),
                                (_other_ex.gid, _tl(_("Girl, I'm deleting this from my memory. But seriously, %s, not cool.")) % pname),
                            ],
                            _ex_girl, _other_ex,
                        )
                        if _ex_r:
                            Change_Status(_ex_girl, "Love", -8)
                            Change_Status(_ex_girl, "Obed", 5)
                            Change_Status(_other_ex, "Obed", 3)
                            Change_Status(_other_ex, "Inbt", 5)
                            return _ex_r

        # ==========================================================
        # HIS EX WATCHES — a video of the OTHER girl, filmed after he broke up with this one (the girl he moved on to)
        # ==========================================================
        if vid_girl and vid_gid in (girl_a.gid, girl_b.gid):
            _ex_girl = girl_b if vid_gid == girl_a.gid else girl_a
            _other_ex = vid_girl
            _vid_day = _vid_snap(vid, "day", None)
            _ex_breakup_day = (getattr(_ex_girl, "ex_player_history", None) or {}).get("breakup_day")
            if (_ex_girl.is_ex_of_player() and _vid_day is not None and _ex_breakup_day is not None
                    and _vid_day >= _ex_breakup_day):
                print("[GROUP_VIDEO] ex %s watches %s (filmed day %s, breakup day %s)" % (
                    _ex_girl.gid, _other_ex.gid, _vid_day, _ex_breakup_day))
                _ex_r = _fire(
                    "ex_watches_new_" + _ex_girl.gid + "_" + _other_ex.gid,
                    [
                        (_ex_girl.gid, _("Oh... so this is what he does with other girls now. Cool. Cool cool cool.")),
                        (_other_ex.gid, _("Sorry... this must be weird for you to see...")),
                        (_ex_girl.gid, _("Weird? Watching my ex's new... whatever she is... on video? Nah, I'm GREAT.")),
                        (_other_ex.gid, _("I didn't know he was going to send it to this group! I would've said no!")),
                        (_ex_girl.gid, _tl(_("Sure you would have. %s clearly hasn't changed one bit.")) % pname),
                        (_other_ex.gid, _("Look, I'm not trying to make this awkward...")),
                        (_ex_girl.gid, _("Too late! It's PEAK awkward! But honestly? You're welcome to him. I know what he's like.")),
                    ],
                    _ex_girl, _other_ex,
                )
                if _ex_r:
                    Change_Status(_ex_girl, "Love", -5)
                    Change_Status(_other_ex, "Obed", 3)
                    Change_Status(_other_ex, "Inbt", 5)
                    return _ex_r

        # ==========================================================
        # LESBIAN DISCOVERY — video of lesbian girl doing sexual acts
        # ==========================================================
        _les_girl = None
        _other_les = None
        if girl_a.has_trait("lesbian") and not girl_b.has_trait("lesbian"):
            _les_girl = girl_a
            _other_les = girl_b
        elif girl_b.has_trait("lesbian") and not girl_a.has_trait("lesbian"):
            _les_girl = girl_b
            _other_les = girl_a

        if _les_girl and _other_les and consensual:
            _ln = _les_girl.Name
            _on = _other_les.Name

            if vid_gid == _les_girl.gid and vid_type in ("hj", "bj", "tj", "cowgirl", "reverse_cowgirl", "creampie", "anal"):
                _proof = lesbian_openness(_les_girl)

                if _proof < 26:
                    _les_r = _fire(
                        "lesbian_discovery_denial_" + _les_girl.gid + "_" + _other_les.gid,
                        [
                            (_other_les.gid, _tl(_("Wait... %s?! Aren't you... I thought you only liked girls?!")) % _ln),
                            (_les_girl.gid, _("I DO only like girls! This is NOT what it looks like!")),
                            (_other_les.gid, _tl(_("It looks like you're with %s! How is that not what it looks like?!")) % pname),
                            (_les_girl.gid, _("It was a mistake! I was confused! It meant NOTHING!")),
                            (_other_les.gid, _("A mistake? Girl, you look pretty into it in this video...")),
                            (_les_girl.gid, _tl(_("%s, I swear to god if you don't delete this RIGHT NOW...")) % pname),
                            (_other_les.gid, _("Oh my god... this is wild. I never would have guessed.")),
                            (_les_girl.gid, _("There's NOTHING to guess! I'm a lesbian! End of story! DELETE IT!")),
                        ],
                        _les_girl, _other_les,
                        traits_self="lesbian",
                    )
                elif _proof < 51:
                    _les_r = _fire(
                        "lesbian_discovery_confused_" + _les_girl.gid + "_" + _other_les.gid,
                        [
                            (_other_les.gid, _tl(_("Hold on... %s? With a GUY? But you always said you were...")) % _ln),
                            (_les_girl.gid, _("I know what I said! I don't... I don't know what's happening to me.")),
                            (_other_les.gid, _tl(_("So you DO like guys? Or just %s? I'm so confused!")) % pname),
                            (_les_girl.gid, _("I don't LIKE guys! He's just... different. I can't explain it.")),
                            (_other_les.gid, _("Different how? Because that video doesn't look like someone who 'doesn't like guys'...")),
                            (_les_girl.gid, _("Can we please not do this right now? I'm still trying to figure it out myself.")),
                            (_other_les.gid, _("Okay okay... but when you figure it out, you owe me the full story!")),
                        ],
                        _les_girl, _other_les,
                        traits_self="lesbian",
                    )
                elif _proof < 76:
                    _les_r = _fire(
                        "lesbian_discovery_conflict_" + _les_girl.gid + "_" + _other_les.gid,
                        [
                            (_other_les.gid, _tl(_("%s... is that you? With %s? I thought you were strictly into women!")) % (_ln, pname)),
                            (_les_girl.gid, _("I AM into women. He's just... he's the exception. The only one.")),
                            (_other_les.gid, _("The exception?! Girl, that's not how being a lesbian works!")),
                            (_les_girl.gid, _("Don't lecture me about my own sexuality! I've been dealing with this!")),
                            (_other_les.gid, _("I'm not lecturing! I just... never expected to see you doing THAT.")),
                            (_les_girl.gid, _("Yeah well... neither did I. Life is full of surprises.")),
                            (_other_les.gid, _("...Do you want to talk about it?")),
                            (_les_girl.gid, _tl(_("No. Maybe. Not in a group chat. %s, you owe me SO many apologies.")) % pname),
                        ],
                        _les_girl, _other_les,
                        traits_self="lesbian",
                    )
                else:
                    _les_r = _fire(
                        "lesbian_discovery_accepted_" + _les_girl.gid + "_" + _other_les.gid,
                        [
                            (_other_les.gid, _tl(_("%s?! Wait... you and %s?! But you're a lesbian!")) % (_ln, pname)),
                            (_les_girl.gid, _("Still am. He's just... the one exception. Don't make it weird.")),
                            (_other_les.gid, _("How is this NOT weird?! You literally only dated women!")),
                            (_les_girl.gid, _tl(_("And I still prefer women. But %s does something to me that I can't explain.")) % pname),
                            (_other_les.gid, _("That's actually kind of sweet... in a really unexpected way.")),
                            (_les_girl.gid, _("If you tell ANYONE, I will make your life miserable. We clear?")),
                            (_other_les.gid, _("Crystal clear! But... I have SO many questions for later!")),
                            (_les_girl.gid, _("Later. Much later. And only if you bring wine.")),
                        ],
                        _les_girl, _other_les,
                        traits_self="lesbian",
                    )

                if _les_r:
                    girl_learns_lesbian(_other_les, _les_girl)
                    _les_girl.gain_blackmail_leverage(1)
                    Change_Status(_les_girl, "Obed", 10)
                    Change_Status(_other_les, "Inbt", 8)
                    return _les_r

            if vid_gid == _other_les.gid and vid_type in ("cowgirl", "reverse_cowgirl", "creampie", "anal"):
                _les_v = _fire(
                    "lesbian_viewer_other_" + _les_girl.gid + "_" + _other_les.gid,
                    [
                        (_les_girl.gid, _tl(_("You're really showing me a video of %s with a man? Why would I want to see this?")) % _on),
                        (_other_les.gid, _("What's wrong with it? I look good!")),
                        (_les_girl.gid, _("I just don't need to see a guy doing... that. It's not my thing.")),
                        (_other_les.gid, _tl(_("Not your thing? Really? Because I heard you've been spending time with %s too~")) % pname),
                        (_les_girl.gid, _("That's COMPLETELY different! Don't compare us!")),
                        (_other_les.gid, _("Different how? Same guy, same... activities~")),
                        (_les_girl.gid, _tl(_("I am NOT having this conversation. %s, stop stirring things up!")) % pname),
                    ],
                    _les_girl, _other_les,
                    traits_self="lesbian",
                )
                if _les_v:
                    return _les_v

        # ==========================================================
        # CHEATING EXPOSURE ESCALATION — tier-aware scripted scenarios
        # Higher severity videos trigger heavier relationship consequences.
        # ==========================================================
        _a_bf = _is_bf_context(girl_a)
        _b_bf = _is_bf_context(girl_b)
        _vid_tier = _GROUP_VIDEO_SEVERITY_TIER.get(vid_type, 1)

        # The specific stories first (CE-5 a lesbian with a GF caught with a man, CE-6 the loyal girl's fall): the generic
        # partner scenarios below would answer them first, and their secret-recording variants only on a 2nd video
        # ── Scenario CE-5: Lesbian with GF, her tier 3+ video with a man ──
        if vid_girl and vid_gid in (girl_a.gid, girl_b.gid) and _vid_tier >= 3:
            _les = girl_a if vid_gid == girl_a.gid else girl_b
            _other = girl_b if vid_gid == girl_a.gid else girl_a
            if _les.has_trait("lesbian") and _is_bf_context(_les):
                _fpl_l = lambda s: _format_partner_line(_les, s)
                if consensual:
                    _ce5 = _fire(
                        "ce_lesbian_bf_exposure_" + _les.gid + "_" + _other.gid,
                        [
                            (_les.gid, _("Oh no... no no no. Everyone in this group just saw me with a MAN.")),
                            (_other.gid, _("Wait... aren't you... a lesbian? And you have a girlfriend?")),
                            (_les.gid, _fpl_l(_("I AM a lesbian. %(pl)s can NEVER know about this. About ANY of this."))),
                            (_other.gid, _tl(_("But you just... with %s... that's... how?")) % pname),
                            (_les.gid, _fpl_l(_("It's complicated. %(Pp)s is everything to me. But {player} is... I can't explain it.")).replace("{player}", pname)),
                            (_other.gid, _("Your secret is safe with me. But this is in a GROUP CHAT now...")),
                            (_les.gid, _("I know. One screenshot and my entire identity crumbles. My relationship, my life...")),
                            (_other.gid, _tl(_("%s... you have no idea the power you hold right now. Be careful with it.")) % pname),
                        ],
                        _les, _other,
                        traits_self="lesbian",
                    )
                else:
                    _ce5 = _fire(
                        "ce_lesbian_bf_exposure_secret_" + _les.gid + "_" + _other.gid,
                        [
                            (_les.gid, _("He FILMED me?! With a MAN?! Without my PERMISSION?! And the whole group just SAW?!")),
                            (_other.gid, _("Wait... you're a lesbian and he secretly recorded you with him?!")),
                            (_les.gid, _fpl_l(_("I AM a lesbian! %(pl)s can never see this! I never agreed to any recording!"))),
                            (_other.gid, _tl(_("This is really bad. %s, secretly filming a lesbian cheating? That's blackmail material.")) % pname),
                            (_les.gid, _("That's exactly what it is. He has proof I slept with a man AND I never consented to the video.")),
                            (_other.gid, _("You're being held hostage by a recording you never agreed to. That's terrifying.")),
                            (_les.gid, _fpl_l(_("My identity, my relationship with %(pl)s, my reputation... all in his hands. And I never said yes to the camera."))),
                            (_other.gid, _tl(_("%s... what you're doing to her goes beyond just sharing a video.")) % pname),
                        ],
                        _les, _other,
                        traits_self="lesbian",
                    )
                if _ce5:
                    _les.gain_blackmail_leverage(2)
                    _les.change_bf_loyalty(-80)
                    Change_Status(_les, "Inbt", 12)
                    if not consensual:
                        Change_Status(_les, "Love", -10)
                    return _ce5

        # ── Scenario CE-6: Vid girl has BF, loyal trait, tier 4 — fall from grace ──
        if vid_girl and vid_gid in (girl_a.gid, girl_b.gid) and _vid_tier >= 4:
            _fallen = girl_a if vid_gid == girl_a.gid else girl_b
            _observer = girl_b if vid_gid == girl_a.gid else girl_a
            if _fallen.has_trait("loyal") and _is_bf_context(_fallen):
                _fpl_f = lambda s: _format_partner_line(_fallen, s)
                if consensual:
                    _ce6 = _fire(
                        "ce_loyal_fall_" + _fallen.gid + "_" + _observer.gid,
                        [
                            (_fallen.gid, _tl(_("%s... what have you done to me? I was the GOOD girl. I had principles.")) % pname),
                            (_observer.gid, _tl(_("%s... I've never seen you like this.")) % _fallen.Name),
                            (_fallen.gid, _fpl_f(_("I'm with %(pl)s. I had values. And now there's a sex video of me in a group chat."))),
                            (_observer.gid, _("You don't have to explain yourself to me...")),
                            (_fallen.gid, _("That's the worst part. I should be devastated. But rewatching it... I felt something.")),
                            (_observer.gid, _("...Felt what?")),
                            (_fallen.gid, _fpl_f(_("Alive. For the first time. And that terrifies me more than %(pl)s finding out."))),
                            (_observer.gid, _("...I don't know what to say. But your secret is safe with me.")),
                        ],
                        _fallen, _observer,
                        traits_self="loyal",
                    )
                else:
                    _ce6 = _fire(
                        "ce_loyal_fall_secret_" + _fallen.gid + "_" + _observer.gid,
                        [
                            (_fallen.gid, _("You... you FILMED me? Without asking? I trusted you... I broke every rule I had for you...")),
                            (_observer.gid, _tl(_("%s... oh my god. Are you okay?")) % _fallen.Name),
                            (_fallen.gid, _fpl_f(_("I'm with %(pl)s. I had a life. And now there's a secret recording of me in a group chat."))),
                            (_observer.gid, _tl(_("%s, she didn't even know you were recording. That's really low.")) % pname),
                            (_fallen.gid, _("I already hated myself for cheating. Now I have to hate you too for filming it.")),
                            (_observer.gid, _tl(_("This is messed up. %s, whatever you need, I'm here.")) % _fallen.Name),
                            (_fallen.gid, _fpl_f(_("The girl I used to be would never have been in this video. And she definitely wouldn't have been filmed without knowing."))),
                            (_observer.gid, _tl(_("%s... you owe her an explanation. At minimum.")) % pname),
                        ],
                        _fallen, _observer,
                        traits_self="loyal",
                    )
                if _ce6:
                    _fallen.gain_blackmail_leverage(2)
                    _fallen.change_bf_loyalty(-100)
                    Change_Status(_fallen, "Obed", 8)
                    Change_Status(_fallen, "Inbt", 10)
                    if not consensual:
                        Change_Status(_fallen, "Love", -10)
                    return _ce6

        # ── Scenario CE-1: Both have BF/GF, tier 3+ video, vid is of one of them ──
        if _a_bf and _b_bf and _vid_tier >= 3 and vid_girl and vid_gid in (girl_a.gid, girl_b.gid):
            _exposed = girl_a if vid_gid == girl_a.gid else girl_b
            _witness = girl_b if vid_gid == girl_a.gid else girl_a
            _fpl_e = lambda s: _format_partner_line(_exposed, s)
            _fpl_w = lambda s: _format_partner_line(_witness, s)
            if consensual:
                _ce1 = _fire(
                    "ce_both_bf_panic_" + _exposed.gid + "_" + _witness.gid,
                    [
                        (_witness.gid, _fpl_e(_("Wait... isn't she with %(pn)s?! And this is in OUR group chat?!"))),
                        (_exposed.gid, _fpl_e(_("Oh god... you can see everything... %(pn)s can NEVER find this chat..."))),
                        (_witness.gid, _fpl_w(_("Do you realize I'm with %(pn)s too?! If %(pp)s finds out I'M in a group with THIS..."))),
                        (_exposed.gid, _tl(_("We're both screwed. %s, what are you DOING to us?!")) % pname),
                        (_witness.gid, _("If ANYONE in this chat talks... both our relationships are OVER.")),
                        (_exposed.gid, _("We need to trust each other. Nobody says a word. Deal?")),
                        (_witness.gid, _tl(_("Deal. But %s... you owe us BOTH. Big time.")) % pname),
                    ],
                    _exposed, _witness,
                )
            else:
                _ce1 = _fire(
                    "ce_both_bf_panic_secret_" + _exposed.gid + "_" + _witness.gid,
                    [
                        (_witness.gid, _fpl_e(_("Wait... did she know she was being recorded?! And this is in OUR group?!"))),
                        (_exposed.gid, _("He FILMED me?! Without ASKING?! And now it's in a GROUP CHAT?!")),
                        (_witness.gid, _fpl_w(_("This is insane! I'm with %(pn)s too! If %(pp)s finds out I'm in a group with secretly recorded videos..."))),
                        (_exposed.gid, _fpl_e(_("%(pn)s can never know. And I never agreed to being filmed. ")) + _tl(_("%s, this is a new low.")) % pname),
                        (_witness.gid, _("If ANYONE in this chat talks... we're ALL in trouble.")),
                        (_exposed.gid, _("Secret recording or not, this video can't leave this chat. Deal?")),
                        (_witness.gid, _tl(_("Deal. But %s... what you did is seriously wrong.")) % pname),
                    ],
                    _exposed, _witness,
                )
            if _ce1:
                _lev = _GROUP_SHARE_LEVERAGE.get(_vid_tier, 0)
                if _lev > 0:
                    _exposed.gain_blackmail_leverage(_lev)
                _exposed.change_bf_loyalty(-50)
                _witness.change_bf_loyalty(-20)
                if not consensual:
                    Change_Status(_exposed, "Love", -8)
                return _ce1

        # ── Scenario CE-2: Both have cheater trait, tier 3+ video ──
        if girl_a.has_trait("cheater") and girl_b.has_trait("cheater") and _vid_tier >= 3 and vid_girl and vid_gid in (girl_a.gid, girl_b.gid):
            _exposed = girl_a if vid_gid == girl_a.gid else girl_b
            _buddy = girl_b if vid_gid == girl_a.gid else girl_a
            _fpl_e = lambda s: _format_partner_line(_exposed, s) if _is_bf_context(_exposed) else s
            _fpl_b = lambda s: _format_partner_line(_buddy, s) if _is_bf_context(_buddy) else s
            if consensual:
                _ce2 = _fire(
                    "ce_cheater_solidarity_" + _exposed.gid + "_" + _buddy.gid,
                    [
                        (_exposed.gid, _("Well well... the whole group knows now. And honestly? I don't care~")),
                        (_buddy.gid, _("THAT'S the spirit! Why hide what feels good?")),
                        (_exposed.gid, _tl(_("%s really outdid himself this time. Look at that angle~")) % pname),
                        (_buddy.gid, _("I'm jealous! When's MY video going to the group chat?")),
                        (_exposed.gid, _("Girl, we're terrible. And I love every second of it~")),
                        (_buddy.gid, _("Terrible? We're just honest about what we want! Cheers to that~")),
                        (_exposed.gid, _tl(_("%s, you've created a monster. Two monsters. Keep filming~")) % pname),
                    ],
                    _exposed, _buddy,
                    traits_self="cheater", traits_other="cheater",
                )
            else:
                _ce2 = _fire(
                    "ce_cheater_solidarity_secret_" + _exposed.gid + "_" + _buddy.gid,
                    [
                        (_exposed.gid, _("He secretly recorded me?! That's... wait. That's actually kind of hot.")),
                        (_buddy.gid, _("Girl, you were SECRETLY FILMED and you think it's hot?!")),
                        (_exposed.gid, _("I mean... the angle is good and I look amazing. Could be worse~")),
                        (_buddy.gid, _("...Okay fair, you DO look good. But the principle! He didn't ask!")),
                        (_exposed.gid, _tl(_("Since when do cheaters care about principles? %s, you owe me one. But don't stop~")) % pname),
                        (_buddy.gid, _tl(_("You two are unhinged. I love it. But %s, ask first next time?")) % pname),
                    ],
                    _exposed, _buddy,
                    traits_self="cheater", traits_other="cheater",
                )
            if _ce2:
                Change_Status(_exposed, "Lust", 5)
                Change_Status(_buddy, "Lust", 5)
                return _ce2

        # ── Scenario CE-3: Vid girl has BF, other girl has no BF — friend concerned ──
        if vid_girl and vid_gid in (girl_a.gid, girl_b.gid) and _vid_tier >= 3:
            _exposed = girl_a if vid_gid == girl_a.gid else girl_b
            _friend = girl_b if vid_gid == girl_a.gid else girl_a
            if _is_bf_context(_exposed) and not _is_bf_context(_friend) and not _friend.has_trait("cheater"):
                _fpl_e = lambda s: _format_partner_line(_exposed, s)
                if consensual:
                    _ce3 = _fire(
                        "ce_friend_concerned_" + _exposed.gid + "_" + _friend.gid,
                        [
                            (_friend.gid, _fpl_e(_("Hold on... you're with %(pl)s. {player}, does {name}'s %(pl)s know about this?")).replace("{player}", pname).replace("{name}", _exposed.Name)),
                            (_exposed.gid, _fpl_e(_("NO! And %(pp)s CAN'T! Please don't tell anyone!"))),
                            (_friend.gid, _("I'm not going to tell anyone. But this is in a GROUP CHAT now. That's risky.")),
                            (_exposed.gid, _("I know... I know. It just happened and now there's proof everywhere...")),
                            (_friend.gid, _("Are you okay though? Like... actually okay?")),
                            (_exposed.gid, _fpl_e(_("I don't know. Part of me feels guilty. Part of me... doesn't want to stop."))),
                            (_friend.gid, _tl(_("That's between you and your conscience. But %s sharing this in a group? That's messed up.")) % pname),
                        ],
                        _exposed, _friend,
                    )
                else:
                    _ce3 = _fire(
                        "ce_friend_concerned_secret_" + _exposed.gid + "_" + _friend.gid,
                        [
                            (_friend.gid, _tl(_("Wait... %s, did you know you were being recorded?")) % _exposed.Name),
                            (_exposed.gid, _("WHAT?! He FILMED me?! I had no idea! And now it's in a GROUP CHAT?!")),
                            (_friend.gid, _fpl_e(_("Oh my god... you're with %(pl)s AND he secretly recorded you? {player}, that's really messed up.")).replace("{player}", pname)),
                            (_exposed.gid, _fpl_e(_("I already felt guilty enough about cheating... and now there's a video I never agreed to..."))),
                            (_friend.gid, _("Are you okay? Like... do you need me to do anything?")),
                            (_exposed.gid, _fpl_e(_("I need this video to disappear. If %(pl)s ever sees this... I never consented to being filmed."))),
                            (_friend.gid, _tl(_("%s... filming someone secretly AND sharing it? That's not cool. At all.")) % pname),
                        ],
                        _exposed, _friend,
                    )
                if _ce3:
                    _lev = _GROUP_SHARE_LEVERAGE.get(_vid_tier, 0)
                    if _lev > 0:
                        _exposed.gain_blackmail_leverage(_lev)
                    _exposed.change_bf_loyalty(-30)
                    if not consensual:
                        Change_Status(_exposed, "Love", -8)
                    return _ce3

        # ── Scenario CE-4: Non-consensual tier 3+ video of girl with BF ──
        if vid_girl and vid_gid in (girl_a.gid, girl_b.gid) and _vid_tier >= 3 and not consensual:
            _victim = girl_a if vid_gid == girl_a.gid else girl_b
            _ally = girl_b if vid_gid == girl_a.gid else girl_a
            if _is_bf_context(_victim):
                _fpl_v = lambda s: _format_partner_line(_victim, s)
                _ce4 = _fire(
                    "ce_nonconsensual_bf_" + _victim.gid + "_" + _ally.gid,
                    [
                        (_victim.gid, _("I didn't consent to being filmed! AND you're sharing it in a GROUP?!")),
                        (_ally.gid, _tl(_("%s, this is REALLY messed up. She didn't agree to this.")) % pname),
                        (_victim.gid, _fpl_v(_("If %(pl)s EVER sees this... I didn't just cheat, I got exposed without my permission..."))),
                        (_ally.gid, _("This is beyond wrong. You're using her own body against her.")),
                        (_victim.gid, _("I feel so powerless... the group has proof and I never agreed to any of it...")),
                        (_ally.gid, _tl(_("%s, you need to delete this from everywhere. I mean it.")) % pname),
                        (_victim.gid, _fpl_v(_("My relationship, my reputation... you have all the power now. Are you happy?"))),
                    ],
                    _victim, _ally,
                )
                if _ce4:
                    Change_Status(_victim, "Love", -15)
                    Change_Status(_victim, "Inbt", 10)
                    _victim.gain_blackmail_leverage(2)
                    _victim.change_bf_loyalty(-60)
                    return _ce4

        return None
