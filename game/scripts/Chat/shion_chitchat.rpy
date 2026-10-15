# ============================================================
# shion_chitchat.rpy... Shion's small talk (docs/plan_shion.md Fase 2 item 3, docs/personality_in_game.md)
# ============================================================
#
# Her persona topics: entries of _PERSONA_TOPICS (Chat/ChitChat.rpy: faces, love, pairs) + a one-line
# chitchat_shion_<topic> function each (the chosen topic sits in a store variable, so a save pickles it BY NAME) +
# register_chitchat("shion", ...). Filled at init 1: the table and register_chitchat are made at init 0.
# Her voice follows her stage on the turn (femdom_stage, Actions/femdom_turn.rpy):
#   - stages 0-2 (femdom_stage < 3): BEFORE she turns. Caring on the surface, a blade underneath. He is her "favorite
#     investment", she calls him "boy", her money is hers, his father is a punctual little salaryman.
#   - stage 2 also gets "shion_cracking": she is giving in to him and hates it.
#   - stage 3 (femdom_stage >= 3): AFTER, she is his behind his father's back. Proud, possessive, cruel tongue intact,
#     few orders; she calls him "my boy". She still checks his grades, but now she lies to his father for him.
#     Her jokes about his father in bed ("shion_father_after") need them to have had sex (girl_had_sex).
# A line states a fact only where it is true:
#   - his girlfriend only while he dates a girl who is not her (shion_gf_topic_ok). No name: the topic system has no
#     slot for one, so she says "that girl" / "her" (true with one girlfriend or more)
#   - his failure ("can't even pass his tests", the messenger, his father's temper; after the turn: the grade she hid
#     from his father) only while his LAST exam grade is bad (shion_failure_topic_ok, SHION_BAD_GRADES)
#   - nothing says where his father is right now, and nothing needs him in the room: the topics also play by phone
#     and at the mall
# Her "get to know her" answers (_CC_ASK_STYLE) and her "what are you up to?" answers (_WHATS_UP_OWN) live in
# Chat/ChitChat.rpy, next to the other girls'. The student topics of ChitChat.rpy (student=True) never reach her.
# ============================================================

init 1 python:

    # docs/plan_shion.md D3: a D or an F is a bad grade
    SHION_BAD_GRADES = ("D", "F")

    _PERSONA_TOPICS.update({
        # ---- her first step only ("cold", femdom_stage 0): orders, no interest in him at all
        "shion_orders": {"faces": ("annoyed", "serious"), "love": 1, "pairs": [
            (_("Why are you still standing there?"), _("Find something useful to do. Preferably somewhere else.")),
            (_("Did you wipe your feet?"), _("Don't make me ask twice. I hate repeating myself.")),
            (_("Lower your voice. This isn't your dorm."), _("And take your hands out of your pockets when I'm talking to you.")),
            (_("Don't touch the wine. That bottle costs more than your tuition."), _("I'm serious. I count them.")),
            (_("What do you want? Make it quick."), _("My time costs money. Yours doesn't.")),
            (_("Sit up straight. You're not at a frat party."), _("Honestly. Your father raised you in a barn.")),
        ]},
        # ---- her company: the board, the people she fires, her standards
        "shion_company": {"faces": ("smug", "smirk"), "love": 1, "pairs": [
            (_("I fired a vice president last week."), _("He cried in my office. On my carpet. I billed his department for the cleaning.")),
            (_("The board thinks they run my company."), _("I let them think so. It keeps them quiet in meetings.")),
            (_("People say I'm hard to work for."), _("Good. Easy bosses make lazy people, and I don't pay for lazy.")),
            (_("My assistant brings my coffee at exactly the right temperature."), _("The one before her didn't. Nobody remembers her name anymore.")),
            (_("I don't keep people around who make excuses, [Player.Name]."), _("Remember that the next time you're about to give me one.")),
        ]},
        # ---- his father: the punctual little salaryman, and how she handles him
        "shion_father": {"faces": ("smirk", "smug"), "love": 1, "pairs": [
            (_("Your father always kept a strict schedule."), _("Mmm... punctual little salaryman.")),
            (_("Your father calls me 'honey' when he's drunk."), _("I make him sleep on the floor when he does.")),
            (_("Your father irons his own shirts. Every night, the same crease."), _("I married a very reliable man. Reliable is not the same as interesting.")),
            (_("Do you know what your father does when I raise my voice?"), _("He agrees with me. It's the smartest thing about him.")),
            (_("Your father thinks every problem can be fixed with a talk over dinner."), _("Sweet man. That's why he has me for everything else.")),
        ]},
        # ---- his grades and his scholarship: her rules, her favorite investment, every exam she will see
        "shion_grades": {"faces": ("serious", "smirk"), "love": 1, "pairs": [
            (_("I hope you've kept up with your studies."), _("That scholarship is the only reason you're in that college. Lose it, and don't expect my money to catch you.")),
            (_("Tell me... how is my favorite investment doing?"), _("Careful how you answer. Your next exam will tell me the truth anyway.")),
            (_("An A is what I expect."), _("A B, I forgive. Anything lower, and we'll have a conversation you won't enjoy.")),
            (_("Every two weeks, an exam. Every exam, I see the grade."), _("I don't like surprises, [Player.Name]. Don't give me any.")),
            (_("Your professors can be as boring as they like."), _("I've sat through board meetings worse than any lecture. You'll sit through yours.")),
        ]},
        # ---- money: hers, not his father's
        "shion_money": {"faces": ("smug", "serious"), "love": 1, "pairs": [
            (_("Let's be clear about one thing, boy."), _("My money is mine. Your father's salary pays for his hobbies. Mine pays for everything else.")),
            (_("Your father thinks we share a bank account."), _("We share a kitchen. That's where the sharing ends.")),
            (_("I earned every cent I have. Nobody handed me anything."), _("So don't expect me to hand anything to you. You'll earn it, like everyone else.")),
            (_("Every piece of furniture we own is mine."), _("Your father brought one armchair. I let him keep it. In the corner.")),
            (_("People say money can't buy happiness."), _("People who say that never had any. It buys quiet, obedience and very good wine.")),
        ]},
        # ---- his girlfriend (only while he has one, shion_gf_topic_ok): she distrusts "that girl" and wants it over
        "shion_girlfriend": {"faces": ("annoyed", "smirk"), "love": 1, "pairs": [
            (_("So. Tell me, how is my favorite little disappointment spending his evenings these days?"), _("With that girl, I assume. Your father tells me everything.")),
            (_("That girl you're seeing... I don't trust her."), _("You have nothing, so whatever she's after must be mine.")),
            (_("You're wasting your time with that girl."), _("Break up with her before she costs you your scholarship. I won't pay for your heartbreak.")),
            (_("A distraction with a pretty face is still a distraction, [Player.Name]."), _("End it. Your grades will thank me, and so will you.")),
            (_("I've seen a hundred girls like her."), _("Sweet smile, empty head, and one eye on my money. Be smarter than that.")),
        ]},
        # ---- his failure (only while his last grade is bad, shion_failure_topic_ok): the messenger of his father
        "shion_failure": {"faces": ("serious", "smug"), "love": 1, "pairs": [
            (_("Your father asked me to talk some sense into you, boy."), _("Lucky you, I'm feeling generous today.")),
            (_("Do you think I enjoy being the messenger? Hmm?"), _("Cleaning up after a spoiled little whelp who can't even pass his tests?")),
            (_("Your father wanted to shout at you himself."), _("I told him I'd enjoy it more.")),
            (_("I saw your last grade."), _("I've fired interns for less. Unfortunately, I can't fire family.")),
            (_("Keep this up and your scholarship is gone."), _("And when it is, don't come knocking on my door. My money doesn't pay for failures.")),
        ]},

        # ════ STAGE 2: she is giving in to him, and she hates it ════
        "shion_cracking": {"faces": ("annoyed", "embarrassed"), "love": 1, "pairs": [
            (_("I caught myself thinking about you in a board meeting."), _("In the middle of a sentence. Do you know how humiliating that is? Don't answer that.")),
            (_("Your father asked me why I keep checking my phone."), _("I told him it was work. I never needed to lie to him before you came along. I hate it.")),
            (_("Don't think this means you've won, [Player.Name]."), _("I'm still your stepmother. I'm just... having a difficult quarter.")),
            (_("I used to sleep perfectly."), _("Now I lie awake next to your father, thinking about his son. Fix that. No. Don't. I don't know.")),
            (_("I don't lose, [Player.Name]. I never lose."), _("So explain to me why it feels like I'm losing to you.")),
        ]},

        # ════ STAGE 3: AFTER the turn. She is his behind his father's back ════
        # ---- his father (only once they've had sex, girl_had_sex: the bed jokes need it)
        "shion_father_after": {"faces": ("smirk", "smug"), "love": 1, "pairs": [
            (_("Your old man would be crying if he saw us..."), _("...too bad for him.")),
            (_("Your father always finished too fast. Two minutes, maybe three."), _("Pathetic. You at least last long enough to be entertaining.")),
            (_("The only thing your father could stretch was my patience."), _("You, on the other hand... Hmm. I'll let you finish that sentence yourself.")),
            (_("Your father asked me why I've been in such a good mood lately."), _("I told him it was the quarterly numbers. He nodded. He always nods.")),
            (_("Your father still kisses me goodnight like he's signing a receipt."), _("Quick, polite, forgettable. Like everything else he does in bed.")),
        ]},
        # ---- being his, behind his father's back
        "shion_secret": {"faces": ("sexy", "smirk"), "love": 1, "pairs": [
            (_("In front of your father, I'm still the wicked stepmother."), _("Behind his back... well. You know exactly what I am behind his back.")),
            (_("Your father thinks I've finally warmed up to you."), _("If he only knew how warm. Poor, sweet, oblivious man.")),
            (_("I built a company on secrets, [Player.Name]."), _("You're the only one I'd lose sleep over. So keep it quiet, my boy.")),
            (_("Do you know what I think about during your father's little dinner speeches?"), _("You. And what I'd let you do to me if he left the room for five minutes.")),
            (_("Nobody owns me, [Player.Name]. Not the board, not your father."), _("You're the exception. Don't let it go to your head... too much.")),
        ]},
        # ---- his grades: still hers to check, but now she lies to his father for him
        "shion_grades_after": {"faces": ("serious", "smirk"), "love": 1, "pairs": [
            (_("Don't think being mine gets you out of studying."), _("I still see every grade. The difference is, now I decide what your father hears.")),
            (_("Your father asked me how you're doing in school."), _("I told him you're working very hard. I didn't mention who you're working so hard on.")),
            (_("I still expect an A, my boy."), _("But if you ever bring me a C, your father will hear it was the professor's fault. I'll make sure of it.")),
            (_("Your father thinks you study every night until midnight."), _("I told him so myself. I lie beautifully for you, don't I? Don't make a liar out of me with your next grade.")),
            (_("Your father wanted to call your college about your schedule."), _("I talked him out of it. You're welcome. Now go study before I regret it.")),
        ]},
        # ---- her pride: the CEO who chose him
        "shion_pride": {"faces": ("smug", "sexy"), "love": 1, "pairs": [
            (_("Do you know how many men have tried to get where you are?"), _("Senators. Investors. A prince, once. And you just walked in and took it. Insufferable.")),
            (_("I don't regret anything, [Player.Name]. Ever."), _("Not my company, not my marriage, and not you. Especially not you.")),
            (_("I made an entire board of directors apologize to me last week."), _("I still run everything I touch. You're the only thing that runs me. Don't you dare repeat that.")),
            (_("People at the office say I've been different lately."), _("Different. As if I'd tell them it's my husband's son who put me in a good mood.")),
            (_("I could have any man I want, you know."), _("I chose the one who wouldn't stop talking back. Clearly I have a weakness for punishment.")),
        ]},
        # ---- his girlfriend (only while he has one, shion_gf_topic_ok): she is his, and she doesn't share
        "shion_girlfriend_after": {"faces": ("annoyed", "smirk"), "love": 1, "pairs": [
            (_("That girl of yours still thinks she's the only one."), _("Sweet. Let her keep thinking it. I don't share, but I do enjoy winning.")),
            (_("Does she know what you do when you're not with her?"), _("No? Good. Let her have your dinners and your excuses. I have everything else.")),
            (_("I've been very patient about that girl, [Player.Name]."), _("Patience isn't one of my virtues. Think about how long you want to test it.")),
            (_("You still haven't ended it with her."), _("I'm not angry. I'm keeping score. And I always win in the end.")),
        ]},
        # ════ AFTER THE BREAK (she lost the femdom past her final step; trait submissive) ════
        # ---- the CEO who waits for his word now
        "shion_owned": {"faces": ("shy", "embarrassed"), "love": 1, "pairs": [
            (_("I ran a board meeting today. Flawless, as always."), _("Then you texted, and I answered before the CFO. Priorities.")),
            (_("I used to give every order in this house."), _("Now I wait for yours. I'm still learning to say that out loud.")),
            (_("Your father thinks I've mellowed."), _("Let him. Only you know what actually happened to me.")),
        ]},
        # ---- her money on him (the sugar side; shown while the arrangement is on)
        "shion_sugar": {"faces": ("smug", "happy"), "love": 1, "pairs": [
            (_("I checked your account this morning."), _("It was too low. I fixed it. Don't argue.")),
            (_("Money is the one language I've always spoken fluently."), _("So let me spend it on you. It says what I can't.")),
            (_("I once bought a company because it annoyed me."), _("Spoiling you is a better investment. The returns are immediate.")),
        ]},
        # ---- the act she keeps up in front of his father
        "shion_facade": {"faces": ("smirk", "normal"), "love": 1, "pairs": [
            (_("At dinner I'll be the strict stepmother again."), _("Frown back at me. Your father notices everything except the truth.")),
            (_("I scolded you in front of him yesterday. Theater."), _("...You played along beautifully, by the way.")),
            (_("He tells his friends I keep you in line."), _("He's not wrong. He just has the direction backwards.")),
        ]},

        # ---- his failure (only while his last grade is bad, shion_failure_topic_ok): she hid it from his father
        "shion_failure_after": {"faces": ("serious", "smirk"), "love": 1, "pairs": [
            (_("About that last grade of yours..."), _("Your father never saw it. I made sure of that. You owe me, and I always collect.")),
            (_("Your father asked me about your exam."), _("I told him you passed with flying colors. Don't make me tell that lie twice.")),
            (_("Me, lying to my own husband for a boy who can't pass a test."), _("Look what you've done to me, [Player.Name]. Now study.")),
            (_("One bad grade, I can hide."), _("Three, and not even I can save your scholarship. Study. For both our sakes.")),
        ]},
    })

    def shion_gf_topic_ok(girl, loc, t_index):
        """The girlfriend topic: he dates a girl, and she is not that girl."""
        _gfs = get_player_girlfriends([_g for _g in ALL_GIRLS if _g is not girl])
        if _gfs:
            print("[SHION] chitchat: he dates %s, her girlfriend topic is available" % ", ".join(_g.gid for _g in _gfs))
        return bool(_gfs)

    def shion_failure_topic_ok(girl, loc, t_index):
        """The failure topic: his last exam grade is a bad one (SHION_BAD_GRADES). No exam yet = nothing to scold."""
        _hist = getattr(store.Player, "grade_history", None) or []
        if _hist and _hist[-1] in SHION_BAD_GRADES:
            print("[SHION] chitchat: his last grade is %s, her failure topic is available" % _hist[-1])
            return True
        return False

    # Her STORY step (story_step, Events/story_steps.rpy; losing the femdom trait never moves it): the topics above
    # the "STAGE 2" mark are her voice before it (steps 0-2); "shion_cracking" is step 2 only; the "_after" topics
    # and "shion_secret" / "shion_pride" are step 3. The step test comes first: the fact checks log when they pass.

    def chitchat_shion_orders(girl, loc, t_index):
        _persona_topic(girl, "shion_orders")

    def chitchat_shion_company(girl, loc, t_index):
        _persona_topic(girl, "shion_company")

    register_chitchat("shion", chitchat_shion_orders,
        condition=lambda g, loc, t: story_step(g) == 0, weight=4)

    register_chitchat("shion", chitchat_shion_company,
        condition=lambda g, loc, t: story_step(g) < 3, weight=2)

    def chitchat_shion_father(girl, loc, t_index):
        _persona_topic(girl, "shion_father")

    register_chitchat("shion", chitchat_shion_father,
        condition=lambda g, loc, t: story_step(g) < 3, weight=2)

    def chitchat_shion_grades(girl, loc, t_index):
        _persona_topic(girl, "shion_grades")

    register_chitchat("shion", chitchat_shion_grades,
        condition=lambda g, loc, t: story_step(g) < 3, weight=2)

    def chitchat_shion_money(girl, loc, t_index):
        _persona_topic(girl, "shion_money")

    register_chitchat("shion", chitchat_shion_money,
        condition=lambda g, loc, t: story_step(g) < 3, weight=1)

    def chitchat_shion_girlfriend(girl, loc, t_index):
        _persona_topic(girl, "shion_girlfriend")

    register_chitchat("shion", chitchat_shion_girlfriend,
        condition=lambda g, loc, t: story_step(g) < 3 and shion_gf_topic_ok(g, loc, t), weight=3)

    def chitchat_shion_failure(girl, loc, t_index):
        _persona_topic(girl, "shion_failure")

    register_chitchat("shion", chitchat_shion_failure,
        condition=lambda g, loc, t: story_step(g) < 3 and shion_failure_topic_ok(g, loc, t), weight=3)

    # ---- stage 2
    def chitchat_shion_cracking(girl, loc, t_index):
        _persona_topic(girl, "shion_cracking")

    register_chitchat("shion", chitchat_shion_cracking,
        condition=lambda g, loc, t: story_step(g) == 2, weight=3)

    # ---- stage 3: after the turn
    def chitchat_shion_father_after(girl, loc, t_index):
        _persona_topic(girl, "shion_father_after")

    register_chitchat("shion", chitchat_shion_father_after,
        condition=lambda g, loc, t: story_step(g) >= 3 and girl_had_sex(g), weight=2)

    def chitchat_shion_secret(girl, loc, t_index):
        _persona_topic(girl, "shion_secret")

    register_chitchat("shion", chitchat_shion_secret,
        condition=lambda g, loc, t: story_step(g) >= 3, weight=2)

    def chitchat_shion_grades_after(girl, loc, t_index):
        _persona_topic(girl, "shion_grades_after")

    register_chitchat("shion", chitchat_shion_grades_after,
        condition=lambda g, loc, t: story_step(g) >= 3, weight=2)

    def chitchat_shion_pride(girl, loc, t_index):
        _persona_topic(girl, "shion_pride")

    # the proud-owner voice steps aside once she is the one being kept (submissive)
    register_chitchat("shion", chitchat_shion_pride,
        condition=lambda g, loc, t: story_step(g) >= 3 and not g.has_trait("submissive"), weight=1)

    # ---- after the break (submissive): her new voices
    def chitchat_shion_owned(girl, loc, t_index):
        _persona_topic(girl, "shion_owned")

    register_chitchat("shion", chitchat_shion_owned,
        condition=lambda g, loc, t: story_step(g) >= 3 and g.has_trait("submissive"), weight=3)

    def chitchat_shion_sugar(girl, loc, t_index):
        _persona_topic(girl, "shion_sugar")

    register_chitchat("shion", chitchat_shion_sugar,
        condition=lambda g, loc, t: story_step(g) >= 3 and sugar_active(g), weight=2)

    def chitchat_shion_facade(girl, loc, t_index):
        _persona_topic(girl, "shion_facade")

    register_chitchat("shion", chitchat_shion_facade,
        condition=lambda g, loc, t: story_step(g) >= 3 and g.has_trait("submissive"), weight=2)

    def chitchat_shion_girlfriend_after(girl, loc, t_index):
        _persona_topic(girl, "shion_girlfriend_after")

    # possessive "I always win" tone: not for the broken, submissive her
    register_chitchat("shion", chitchat_shion_girlfriend_after,
        condition=lambda g, loc, t: story_step(g) >= 3 and not g.has_trait("submissive") and shion_gf_topic_ok(g, loc, t), weight=3)

    def chitchat_shion_failure_after(girl, loc, t_index):
        _persona_topic(girl, "shion_failure_after")

    register_chitchat("shion", chitchat_shion_failure_after,
        condition=lambda g, loc, t: story_step(g) >= 3 and shion_failure_topic_ok(g, loc, t), weight=3)
