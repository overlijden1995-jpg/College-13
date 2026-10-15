# ============================================================
# shion_flirt_lines.rpy... Shion's own voice for the flirts (docs/plan_shion.md, Fase 2 item 5 + Fase 3)
# ============================================================
#
# rod_lines["shion"]: the per-girl block of dialogue_bank.rpy (models: rod_lines["tenny"] / rod_lines["ntw"]).
# rod_flirt_line(girl, action, mode) tries her "<key>.<modifier>", her role's (rod_lines["role:stepmom"]) and the Global
# "<key>.<modifier>", then her "<key>", her role's, the Global "<key>". Her stage on the turn is the FIRST modifier
# (femdom_stage_mod, femdom_turn.rpy), so her own "<key>.femdom_s3" beats every other pool.
#
# Her voice by stage on the turn (femdom_turn.rpy: break points -> stage 0..3):
#   - Stages 0 and 1 (femdom_stage_mod is None): the base pools. Cold, commanding, backhanded, amused by his audacity
#     at best. A yes from her is permission, never shyness. Nothing in the base pools has her already his.
#   - Stage 2 (modifier "femdom_s2"): she is cracking. There is no ".femdom_s2" pool here yet, so her base pools speak,
#     except for his hands on her: they leave the commanding modes (femdom_flirt_mode, FEMDOM_TURN_NO_HOLD_STAGE) for
#     the usual six, and the pools "HIS HANDS ON HER FROM HER STAGE 2" are her stage 2 voice (grudging permission, a
#     sharp no). Her ".player_cheating" pools still speak at stage 2.
#   - Stage 3 (modifier "femdom_s3"): she is his, behind his father's back. ".femdom_s3" pools for the safe touches and
#     the stolen kiss, the compliments she loves (confidence, gorgeous, outfit_style, smart), the lewd compliments and
#     his hands on her (not the sunscreen, see below). Every other flirt (joke, massage, the other compliments) falls
#     back to her base voice. Pride and tongue intact; possessive, sensual, taunting about his father. Her no is about
#     the risk (his father, being seen), never about him not deserving her; no girlfriend talk (it beats
#     ".player_cheating"); never "your father is away" (a flirt can't know it).
#
# What can happen to her (read the code before adding a key):
#   - Safe flirts and the 16 safe compliments: all six modes (hard_no, soft_no, shy_yes, normal_yes, enthusiastic_yes,
#     obedient_yes). The compliment list is never filtered by girl or place (face to face AND by phone), so she also
#     hears "class", "grades", "gym" and "swimmer": she answers as the woman who has no classes and checks HIS grades.
#     Compliment and joke lines must work as a text message too.
#   - Joke: only normal_yes / soft_no (do_safe_flirt fakes the result). Shoulder massage: only soft_no / hard_no (the
#     sex-menu massage speaks through here only when she refuses).
#   - His hands on her (FEMDOM_FLIRT_PENALTY: slap / pinch / grab / touch / ask for her panties / the sunscreen): she
#     is canon femdom, so at stages 0 and 1 ONLY commanding_no / commanding_yes. For a hand flirt the narration catches
#     his wrist before her no (FEMDOM_FLIRT_HOLD); ask_panties has no wrist. From stage 2 the usual six modes
#     (obedient_yes too: not in the Global block for these, but get_flirt_reaction_mode_lewd returns it), her hard no
#     slaps him again (flirt_lewd_slaps) and a touch flirt's hard no raises her middle finger first (arm 2).
#   - The sunscreen needs her at the pool (phone invite). flirt_lewd_react reads its rod_lines pools only in the
#     commanding modes: from stage 2 its inline lines in Flirty.rpy (_SunscreenLoop) speak, so it has no normal-mode or
#     ".femdom_s3" pool here.
#   - Lewd compliments (tits / ass) are words: the usual six modes at every stage, and a hard no slaps him.
#   - ".player_cheating": he has a girlfriend who is not her. She distrusts "that girl" and pushes him to end it. The
#     slap_ass / grab_tits pools are on commanding_yes (stages 0 and 1); from stage 2 the role's normal_yes ones speak.
#   - Stolen kiss: her yes and her no both go through rod_flirt_line (her no is followed by a slap).
# She has no NPC partner (the father is not an NPCPartner): no both_cheating, no %(pl)s placeholders.
# No confession keys: she is married and never confesses (chitchat_girl_confesses skips "married", D6). No
# "pregnancy_ask_about_kids_high": that tier needs her to be dating him.
# ============================================================

init 1 python:

    rod_lines["shion"] = {

        # ==========================
        # SAFE FLIRT: JOKE (face to face and by phone)
        # ==========================
        "flirt_safe_joke_normal_yes": [
            _("Hm. That was almost clever. Almost."),
            _("I laughed. Don't let it go to your head, [Player.Name]."),
            _("Funny. Imagine if you put that much effort into your grades."),
        ],
        "flirt_safe_joke_soft_no": [
            _("Say it plainly. I don't fuck boys who need me to fill in their sentences for them."),
            _("I've sat through quarterly reports with more wit than that."),
            _("Was that a joke? I'll assume you're tired, and I'll forgive it. Once."),
        ],

        # ==========================
        # SAFE FLIRT: TOUCH CHEEK
        # ==========================
        "flirt_safe_touch_cheek_shy_yes": [
            _("...Hm. Your hand is warm. Don't make me regret noticing."),
            _("Careful. I haven't decided yet whether I like that."),
        ],
        "flirt_safe_touch_cheek_normal_yes": [
            _("Gentle. At least your father taught you some manners."),
            _("You may. Once. I'm keeping count, [Player.Name]."),
        ],
        "flirt_safe_touch_cheek_enthusiastic_yes": [
            _("Bold. I like bold, as long as it remembers its place."),
            _("Mm. Reaching above your pay grade, are we?"),
        ],
        "flirt_safe_touch_cheek_obedient_yes": [
            _("Fine. Because I choose to allow it, not because you asked."),
            _("Go on, then. I'm feeling generous. It won't last."),
        ],
        "flirt_safe_touch_cheek_soft_no": [
            _("Not now. You haven't earned that yet."),
            _("Hand down, [Player.Name]. Try again when you've done something worth rewarding."),
        ],
        "flirt_safe_touch_cheek_hard_no": [
            _("I've had men escorted out of the building for less. Remove your hand."),
            _("Touch my face without asking again and you'll be explaining it to your father."),
        ],
        "flirt_safe_touch_cheek_soft_no.player_cheating": [
            _("Save your hands for that girl of yours. For now."),
            _("Shouldn't you be touching your little girlfriend? Or has she stopped letting you?"),
        ],
        "flirt_safe_touch_cheek_normal_yes.player_cheating": [
            _("Does that girl of yours know where your hands go? No? Good. Leave her. She's beneath you."),
            _("You'd rather touch me than her. Of course you would. So why are you still with her?"),
        ],

        # ==========================
        # SAFE FLIRT: HOLD HANDS
        # ==========================
        "flirt_safe_hold_hands_shy_yes": [
            _("...Fine. For a moment. Don't squeeze."),
            _("Your palm is sweating. It's almost endearing. Almost."),
        ],
        "flirt_safe_hold_hands_normal_yes": [
            _("Holding hands. How very juvenile. Fine, I'll indulge you."),
            _("There. Now stand like you belong next to me."),
        ],
        "flirt_safe_hold_hands_enthusiastic_yes": [
            _("Mm. Firm grip. Finally, something about you I approve of."),
            _("Hold it properly, [Player.Name]. If you're going to take my hand, do it with conviction."),
        ],
        "flirt_safe_hold_hands_obedient_yes": [
            _("You want my hand? Take it. I'm letting you, remember that."),
            _("Fine. Since you insist so politely."),
        ],
        "flirt_safe_hold_hands_soft_no": [
            _("Old enough to go to college, and still you shake. Disappointing, [Player.Name]."),
            _("Not now. I don't hold hands with boys who haven't proven anything."),
        ],
        "flirt_safe_hold_hands_hard_no": [
            _("Let go. I don't hold hands with children."),
            _("Hands off. I don't know what they tolerate on your campus, but I don't."),
        ],

        # ==========================
        # SAFE FLIRT: KISS CHEEK
        # ==========================
        "flirt_safe_kiss_cheek_shy_yes": [
            _("...That was unexpected. Don't do it in front of your father."),
            _("Hm. On the cheek. How careful of you."),
        ],
        "flirt_safe_kiss_cheek_normal_yes": [
            _("On the cheek, like a proper stepson. How disappointingly polite."),
            _("Fine. That's the kind of affection I can tolerate."),
        ],
        "flirt_safe_kiss_cheek_enthusiastic_yes": [
            _("Mm. You missed. Or were you too scared to aim?"),
            _("Adorable. Next time, have the nerve to aim somewhere that matters."),
        ],
        "flirt_safe_kiss_cheek_obedient_yes": [
            _("Fine. One. Because I allowed it."),
            _("There. Satisfied? Good. Now behave."),
        ],
        "flirt_safe_kiss_cheek_soft_no": [
            _("Not now. I'm not in the mood to be fawned over."),
            _("Keep your lips to yourself until I say otherwise."),
        ],
        "flirt_safe_kiss_cheek_hard_no": [
            _("Do that again and I'll make sure you regret it. Understood?"),
            _("Back up. You don't get that close to me without an invitation."),
        ],

        # ==========================
        # FLIRT: STEAL A KISS (yes: rod_flirt_say in _kiss_accepted; no: rod_pick_line, then a slap)
        # ==========================
        "flirt_safe_steal_kiss_shy_yes": [
            _("...You're either very brave or very stupid. I'm still deciding which."),
            _("Hm. I didn't stop you. Don't make me wonder why."),
        ],
        "flirt_safe_steal_kiss_normal_yes": [
            _("Bold. Next time you wait until I lean in."),
            _("Sloppy. Acceptable, but sloppy. I'll teach you properly. Eventually."),
        ],
        "flirt_safe_steal_kiss_enthusiastic_yes": [
            _("Mm. Finally, some initiative. Don't expect it to work twice."),
            _("Well, well. The boy has ambitions. I might even reward them."),
        ],
        "flirt_safe_steal_kiss_obedient_yes": [
            _("Fine. You took it, I allowed it. Remember which one of those matters."),
            _("There. You've had your kiss. Don't ask what it cost you yet."),
        ],
        "flirt_safe_steal_kiss_soft_no": [
            _("No. You don't take, [Player.Name]. You wait to be given."),
            _("Not like that. Grabbing is for boys. Earn it."),
        ],
        "flirt_safe_steal_kiss_hard_no": [
            _("How dare you. I'm your father's wife, not some girl at a party."),
            _("Try that again and you'll learn exactly how I deal with insubordination."),
        ],
        "flirt_safe_steal_kiss_soft_no.player_cheating": [
            _("And then you'd go back to that girl with my lipstick on you? No. End it first."),
            _("Not while you're still playing house with her. Break it off, then we'll talk."),
        ],
        "flirt_safe_steal_kiss_normal_yes.player_cheating": [
            _("Does that girl kiss you like that? No? Then why are you still with her?"),
            _("Remember that taste. She'll never match it. Get rid of her, [Player.Name]."),
        ],

        # ==========================
        # SAFE FLIRT: HUG
        # ==========================
        "flirt_safe_hug_shy_yes": [
            _("...Fine. Briefly. Don't hold on like a child."),
            _("Hm. You're warmer than I expected. That's not a compliment."),
        ],
        "flirt_safe_hug_normal_yes": [
            _("A hug. How filial of you."),
            _("There. Family affection. Don't make it strange."),
        ],
        "flirt_safe_hug_enthusiastic_yes": [
            _("Mm. Hold me like you mean it, or don't bother."),
            _("Firmer. If you're going to hold something this expensive, act like it."),
        ],
        "flirt_safe_hug_obedient_yes": [
            _("Fine. One hug. I'm the one allowing it."),
            _("If it keeps you quiet, go ahead."),
        ],
        "flirt_safe_hug_soft_no": [
            _("Not now. I'm not in the mood for clinging."),
            _("No. Hugs are for people who've earned my patience."),
        ],
        "flirt_safe_hug_hard_no": [
            _("Arms down. I don't do clingy, and I certainly don't do it with you."),
            _("Step back. Now. I won't say it twice."),
        ],

        # ==========================
        # SAFE FLIRT: SHOULDER MASSAGE (sex menu; only her no speaks from here)
        # ==========================
        "flirt_safe_shoulder_massage_soft_no": [
            _("Your hands on my shoulders? You haven't earned my back yet, let alone the rest."),
            _("Not today. I have a masseuse. She's better than you, and she doesn't have ulterior motives."),
        ],
        "flirt_safe_shoulder_massage_hard_no": [
            _("A massage? From you? I pay professionals for that. Sit down."),
            _("Keep your hands to yourself. I know exactly where they'd wander."),
        ],

        # ==========================
        # COMPLIMENT: SMILE (she distrusts it: GIRL_COMPLIMENT_TASTE)
        # ==========================
        "flirt_safe_compliment_smile_shy_yes": [
            _("...Hm. I wasn't smiling for you."),
            _("Enjoy it. You won't see it often."),
        ],
        "flirt_safe_compliment_smile_normal_yes": [
            _("It's my negotiating smile. It closes deals. Remember that."),
            _("Thank you. Now tell me why you're really flattering me."),
        ],
        "flirt_safe_compliment_smile_enthusiastic_yes": [
            _("It is, isn't it? It's cost other people a great deal of money."),
            _("Mm. Keep earning it and you might see it more often."),
        ],
        "flirt_safe_compliment_smile_obedient_yes": [
            _("Fine. You may compliment my smile. Once."),
            _("Noted, [Player.Name]."),
        ],
        "flirt_safe_compliment_smile_soft_no": [
            _("My smile isn't for you, [Player.Name]."),
            _("Flattery about my smile? Try harder."),
        ],
        "flirt_safe_compliment_smile_hard_no": [
            _("My smile? That's the best you've got? Pathetic."),
            _("I don't smile for boys who talk like greeting cards."),
        ],

        # ==========================
        # COMPLIMENT: LAUGH (she distrusts it)
        # ==========================
        "flirt_safe_compliment_laugh_shy_yes": [
            _("...You weren't supposed to hear that."),
            _("Hm. I laugh when something amuses me. Rarely."),
        ],
        "flirt_safe_compliment_laugh_normal_yes": [
            _("Then make me laugh more often. It's harder than it looks."),
            _("Contagious. Like a bad habit. Fine, I'll take it."),
        ],
        "flirt_safe_compliment_laugh_enthusiastic_yes": [
            _("Only the right people make me laugh. Consider yourself lucky."),
            _("Mm. Keep entertaining me and I'll keep you around."),
        ],
        "flirt_safe_compliment_laugh_obedient_yes": [
            _("If you insist. I'll allow the observation."),
            _("Fine. Thank you, [Player.Name]."),
        ],
        "flirt_safe_compliment_laugh_soft_no": [
            _("Don't get sentimental. It doesn't suit you."),
            _("Contagious? That's something you say about a cold."),
        ],
        "flirt_safe_compliment_laugh_hard_no": [
            _("Is that supposed to charm me? Try again in ten years."),
            _("I don't giggle, boy. You're thinking of someone else."),
        ],

        # ==========================
        # COMPLIMENT: HAIR TODAY
        # ==========================
        "flirt_safe_compliment_hair_today_shy_yes": [
            _("...Today? It always does. But thank you."),
            _("Hm. You noticed. Good."),
        ],
        "flirt_safe_compliment_hair_today_normal_yes": [
            _("Only today? It looks like this every day. I pay someone a great deal to make sure of it."),
            _("Of course it does. I don't leave the house looking anything less."),
        ],
        "flirt_safe_compliment_hair_today_enthusiastic_yes": [
            _("Finally, a man with eyes. Keep them on me."),
            _("Mm. Good. Attention to detail. I value that."),
        ],
        "flirt_safe_compliment_hair_today_obedient_yes": [
            _("Thank you. Noted."),
            _("Fine. I'll take the compliment."),
        ],
        "flirt_safe_compliment_hair_today_soft_no": [
            _("Save the hair compliments for someone who needs them."),
            _("I didn't ask for your opinion on my hair."),
        ],
        "flirt_safe_compliment_hair_today_hard_no": [
            _("My hair is none of your business."),
            _("Flattery about my hair? What do you want, money?"),
        ],

        # ==========================
        # COMPLIMENT: OUTFIT STYLE (she loves it)
        # ==========================
        "flirt_safe_compliment_outfit_style_shy_yes": [
            _("...It does. I'm glad someone noticed."),
            _("Hm. You have better taste than I assumed."),
        ],
        "flirt_safe_compliment_outfit_style_normal_yes": [
            _("It's tailored. You wouldn't know the name, but thank you."),
            _("Everything suits me. But I appreciate that you noticed."),
        ],
        "flirt_safe_compliment_outfit_style_enthusiastic_yes": [
            _("Mm. Look all you want. Touching is another matter."),
            _("Good eye. It costs more than your scholarship, and it's worth every cent."),
        ],
        "flirt_safe_compliment_outfit_style_obedient_yes": [
            _("Thank you. It should."),
            _("Fine. Compliment accepted."),
        ],
        "flirt_safe_compliment_outfit_style_soft_no": [
            _("I didn't dress for you, [Player.Name]."),
            _("Don't comment on my clothes. It's not your place."),
        ],
        "flirt_safe_compliment_outfit_style_hard_no": [
            _("My wardrobe is not a topic for you. Ever."),
            _("Flattering my clothes won't get you anywhere near what's under them."),
        ],

        # ==========================
        # COMPLIMENT: FRAGRANCE
        # ==========================
        "flirt_safe_compliment_fragrance_shy_yes": [
            _("...It's custom. You're not supposed to notice it unless you're close."),
            _("Hm. You noticed. That means you've been paying attention."),
        ],
        "flirt_safe_compliment_fragrance_normal_yes": [
            _("It's custom made. There's only one bottle, and it's mine."),
            _("Of course it suits me. I had it made for me."),
        ],
        "flirt_safe_compliment_fragrance_enthusiastic_yes": [
            _("Mm. Remember it. You'll want to."),
            _("It's rare, like my patience. Enjoy it while you're allowed near it."),
        ],
        "flirt_safe_compliment_fragrance_obedient_yes": [
            _("Thank you. It's rare."),
            _("Fine. It's nice that you noticed."),
        ],
        "flirt_safe_compliment_fragrance_soft_no": [
            _("It isn't for you. Don't flatter yourself."),
            _("You don't get to comment on how I smell, [Player.Name]."),
        ],
        "flirt_safe_compliment_fragrance_hard_no": [
            _("Is that your idea of a line? Rehearse better ones."),
            _("Keep your nose, and your opinions, to yourself."),
        ],

        # ==========================
        # COMPLIMENT: CLASS (she has no classes: the list is not filtered by girl)
        # ==========================
        "flirt_safe_compliment_class_shy_yes": [
            _("...Class? I haven't sat in a classroom in years. But I'll take the thought."),
            _("You're confusing me with someone. Still... thank you, I suppose."),
        ],
        "flirt_safe_compliment_class_normal_yes": [
            _("Class? I don't take classes, [Player.Name]. I give them. But thank you."),
            _("Wrong woman, right idea. Everything I do is excellent work."),
        ],
        "flirt_safe_compliment_class_enthusiastic_yes": [
            _("Class? The only classroom I sit in now is a boardroom. And yes, I'm the best in it."),
            _("Mm. I'll take any praise you have. Even misplaced."),
        ],
        "flirt_safe_compliment_class_obedient_yes": [
            _("Class? ...Fine. I'll accept it anyway."),
            _("I don't have classes. But the effort is noted."),
        ],
        "flirt_safe_compliment_class_soft_no": [
            _("Class? I think you have me confused with one of your study partners."),
            _("I haven't been a student in a very long time. Focus on your own classes."),
        ],
        "flirt_safe_compliment_class_hard_no": [
            _("Mixing me up with some girl from your class? Careful."),
            _("Worry about your own classes, [Player.Name]. I'll be seeing those grades."),
        ],

        # ==========================
        # COMPLIMENT: CLASS GRADES (she is the one who checks HIS)
        # ==========================
        "flirt_safe_compliment_class_grades_shy_yes": [
            _("...My grades? That's sweet. Misguided, but sweet."),
            _("Hm. I haven't had grades in years. Nice try, though."),
        ],
        "flirt_safe_compliment_class_grades_normal_yes": [
            _("My grades? I'm the one who checks yours, remember?"),
            _("Mine were always excellent. Let's talk about yours."),
        ],
        "flirt_safe_compliment_class_grades_enthusiastic_yes": [
            _("Top of every class I ever took. Now match me."),
            _("Of course they were. Mediocrity is something I fire people for."),
        ],
        "flirt_safe_compliment_class_grades_obedient_yes": [
            _("Fine. Thank you. Now show me yours."),
            _("Noted. I expect the same from you."),
        ],
        "flirt_safe_compliment_class_grades_soft_no": [
            _("Deflecting to my grades won't save yours, [Player.Name]."),
            _("Flatter me all you want. I'll still see your grades."),
        ],
        "flirt_safe_compliment_class_grades_hard_no": [
            _("Cute deflection. Bring me an A and then we'll talk about grades."),
            _("You want to talk about grades? Careful, boy. I read yours."),
        ],

        # ==========================
        # COMPLIMENT: SWIMMER (dr_skill)
        # ==========================
        "flirt_safe_compliment_dr_skill_shy_yes": [
            _("...When were you watching me swim? Don't answer that."),
            _("Hm. I didn't know I had an audience."),
        ],
        "flirt_safe_compliment_dr_skill_normal_yes": [
            _("I do everything well. Swimming is no exception."),
            _("Thank you. Discipline shows, in the water and everywhere else."),
        ],
        "flirt_safe_compliment_dr_skill_enthusiastic_yes": [
            _("Mm. Were you watching? Good. I like an audience that pays attention."),
            _("Of course. I don't do anything halfway."),
        ],
        "flirt_safe_compliment_dr_skill_obedient_yes": [
            _("Thank you. I'll accept that."),
            _("Hm. I'll let that stand."),
        ],
        "flirt_safe_compliment_dr_skill_soft_no": [
            _("I don't swim for spectators, [Player.Name]."),
            _("Keep your eyes off me in the water. Understood?"),
        ],
        "flirt_safe_compliment_dr_skill_hard_no": [
            _("Watching me in a swimsuit, were you? Choose your next words carefully."),
            _("Spare me. I know exactly what you were looking at."),
        ],

        # ==========================
        # COMPLIMENT: GYM WEIGHTS
        # ==========================
        "flirt_safe_compliment_gym_weights_shy_yes": [
            _("...I stay in shape. I don't advertise it."),
            _("Hm. I don't recall giving you a show."),
        ],
        "flirt_safe_compliment_gym_weights_normal_yes": [
            _("I stay in shape. Discipline, [Player.Name]. You should try it."),
            _("Strong women run companies. Remember that."),
        ],
        "flirt_safe_compliment_gym_weights_enthusiastic_yes": [
            _("Mm. Impressed? Wait until you see what else I can hold down."),
            _("Good. I like it when you notice how strong I am."),
        ],
        "flirt_safe_compliment_gym_weights_obedient_yes": [
            _("Thank you. I don't need the reminder, but thank you."),
            _("Fine. Consider it acknowledged."),
        ],
        "flirt_safe_compliment_gym_weights_soft_no": [
            _("I don't lift for applause."),
            _("Weights? I have people to carry heavy things for me."),
        ],
        "flirt_safe_compliment_gym_weights_hard_no": [
            _("Watching me work out? Don't make it strange."),
            _("Keep your gym talk for your little friends."),
        ],

        # ==========================
        # COMPLIMENT: BEAUTY TODAY
        # ==========================
        "flirt_safe_compliment_beauty_today_shy_yes": [
            _("...Only today? I'll forgive the wording this once."),
            _("Hm. You're getting better at this."),
        ],
        "flirt_safe_compliment_beauty_today_normal_yes": [
            _("Only today? Choose your words more carefully, [Player.Name]."),
            _("Thank you. I'm aware."),
        ],
        "flirt_safe_compliment_beauty_today_enthusiastic_yes": [
            _("Mm. Extra beautiful. Now that's the language I like."),
            _("Of course I am. And you noticed. Good boy."),
        ],
        "flirt_safe_compliment_beauty_today_obedient_yes": [
            _("Thank you. Accepted."),
            _("Fine. I'll take it."),
        ],
        "flirt_safe_compliment_beauty_today_soft_no": [
            _("Save it. I hear that from better men every day."),
            _("Flattery is cheap. You'll have to do better."),
        ],
        "flirt_safe_compliment_beauty_today_hard_no": [
            _("Keep your eyes to yourself. I'm your father's wife."),
            _("Don't. Whatever you're working up to, don't."),
        ],

        # ==========================
        # COMPLIMENT: GORGEOUS (she loves it)
        # ==========================
        "flirt_safe_compliment_gorgeous_shy_yes": [
            _("...Hm. Bold opener. It worked. Don't gloat."),
            _("...Gorgeous. Well. You're not wrong."),
        ],
        "flirt_safe_compliment_gorgeous_normal_yes": [
            _("Hello, [Player.Name]. And yes. Accurate."),
            _("Gorgeous is accurate. 'Hey there' is beneath you."),
        ],
        "flirt_safe_compliment_gorgeous_enthusiastic_yes": [
            _("Mm. Say it again. Slower."),
            _("That's the right word. Use it often."),
        ],
        "flirt_safe_compliment_gorgeous_obedient_yes": [
            _("Hello. And thank you."),
            _("Fine. I'll answer to that."),
        ],
        "flirt_safe_compliment_gorgeous_soft_no": [
            _("'Hey there'? I'm not a girl at a bar, [Player.Name]."),
            _("Gorgeous, yes. Yours, no."),
        ],
        "flirt_safe_compliment_gorgeous_hard_no": [
            _("That's how you address your father's wife? Try again."),
            _("Don't 'hey there' me, boy. I'm not someone you pick up."),
        ],

        # ==========================
        # COMPLIMENT: CONFIDENCE (she loves it)
        # ==========================
        "flirt_safe_compliment_confidence_shy_yes": [
            _("...Hm. You're not the first to say it. You might be the first to mean it."),
            _("...Good. It took years to build. Don't expect a discount."),
        ],
        "flirt_safe_compliment_confidence_normal_yes": [
            _("Confidence is what you call it when you haven't earned it. I've earned mine."),
            _("Good. Watch closely. You could use some."),
        ],
        "flirt_safe_compliment_confidence_enthusiastic_yes": [
            _("Mm. Then you'll love me when I'm in charge. Which is always."),
            _("Of course you do. Everyone likes power. Few can handle it."),
        ],
        "flirt_safe_compliment_confidence_obedient_yes": [
            _("Thank you. It's well deserved."),
            _("Fine. Noted, [Player.Name]."),
        ],
        "flirt_safe_compliment_confidence_soft_no": [
            _("Flattery about my confidence? Transparent."),
            _("I don't need you to like it. I need you to respect it."),
        ],
        "flirt_safe_compliment_confidence_hard_no": [
            _("You like it? You're not supposed to like it. You're supposed to fear it."),
            _("Don't mistake my confidence for an invitation."),
        ],

        # ==========================
        # COMPLIMENT: SMART
        # ==========================
        "flirt_safe_compliment_smart_shy_yes": [
            _("...Hm. Only one of?"),
            _("...That's a better compliment than most. Thank you."),
        ],
        "flirt_safe_compliment_smart_normal_yes": [
            _("One of? I don't compete for 'one of', [Player.Name]."),
            _("Obviously. Smart enough to see through you, too."),
        ],
        "flirt_safe_compliment_smart_enthusiastic_yes": [
            _("Mm. Smart enough to run a company and you. Remember that."),
            _("Of course. Intelligence is the only thing I find attractive. Develop some."),
        ],
        "flirt_safe_compliment_smart_obedient_yes": [
            _("Thank you. It's true."),
            _("Noted. Accurate, too."),
        ],
        "flirt_safe_compliment_smart_soft_no": [
            _("Flattering my intelligence? I know that trick. I invented it."),
            _("Smart enough to know when I'm being buttered up."),
        ],
        "flirt_safe_compliment_smart_hard_no": [
            _("I'm smart enough to know exactly what you want. The answer is no."),
            _("Don't patronize me, boy."),
        ],

        # ==========================
        # COMPLIMENT: EYES
        # ==========================
        "flirt_safe_compliment_eyes_shy_yes": [
            _("...Hm. Find your way out, then. Slowly."),
            _("...That was a terrible line. And yet."),
        ],
        "flirt_safe_compliment_eyes_normal_yes": [
            _("Lost? Then I'll lead. I always do."),
            _("A cheap line, but you delivered it well."),
        ],
        "flirt_safe_compliment_eyes_enthusiastic_yes": [
            _("Mm. Stay lost. I like you where I can see you."),
            _("Good. Now you know where to look when I'm speaking."),
        ],
        "flirt_safe_compliment_eyes_obedient_yes": [
            _("Fine. Accepted."),
            _("Fine. I'll let you have that line, [Player.Name]."),
        ],
        "flirt_safe_compliment_eyes_soft_no": [
            _("Then find your way out and look somewhere else."),
            _("Cheap line. Try again when you've grown up a little."),
        ],
        "flirt_safe_compliment_eyes_hard_no": [
            _("I've fired men for looking at me the way you are. Remember that next time when you're speaking to me."),
            _("Lost in my eyes? Don't be pathetic."),
        ],

        # ==========================
        # COMPLIMENT: TONED BODY
        # ==========================
        "flirt_safe_compliment_toned_body_shy_yes": [
            _("...You've been paying attention. Interesting."),
            _("Hm. Discipline shows. I'm glad you noticed."),
        ],
        "flirt_safe_compliment_toned_body_normal_yes": [
            _("Discipline, [Player.Name]. You should try it sometime."),
            _("I work for it. Unlike some people."),
        ],
        "flirt_safe_compliment_toned_body_enthusiastic_yes": [
            _("Mm. You like what you see? Good. Keep wanting it."),
            _("Every inch of it earned. Look all you want."),
        ],
        "flirt_safe_compliment_toned_body_obedient_yes": [
            _("It is. Thank you for noticing, I suppose."),
            _("Fine. I'll allow that one."),
        ],
        "flirt_safe_compliment_toned_body_soft_no": [
            _("My body is none of your business."),
            _("Lately? I've always been in shape. Pay better attention."),
        ],
        "flirt_safe_compliment_toned_body_hard_no": [
            _("Stop cataloguing my body. It's disgusting."),
            _("You look at your father's wife like that? Careful."),
        ],

        # ==========================
        # COMPLIMENT: SO INTO YOU (she distrusts it)
        # ==========================
        "flirt_safe_compliment_so_into_you_shy_yes": [
            _("...Of course you are. Don't make it a speech."),
            _("Hm. I suspected. Don't make it my problem."),
        ],
        "flirt_safe_compliment_so_into_you_normal_yes": [
            _("I know. Everyone is, eventually."),
            _("Into me. Of course. Now what do you plan to do about it?"),
        ],
        "flirt_safe_compliment_so_into_you_enthusiastic_yes": [
            _("Good. Stay that way. It makes you easier to manage."),
            _("Mm. I know. It's written all over you, boy."),
        ],
        "flirt_safe_compliment_so_into_you_obedient_yes": [
            _("I heard you the first time, [Player.Name]."),
            _("Fine. I've heard you."),
        ],
        "flirt_safe_compliment_so_into_you_soft_no": [
            _("Into me? Get in line."),
            _("Feelings. How inconvenient for you."),
        ],
        "flirt_safe_compliment_so_into_you_hard_no": [
            _("Say that again and I'll have you sent back to your dorm for good."),
            _("I'm your father's wife. Get over it."),
        ],

        # ==========================
        # LEWD COMPLIMENT: TITS (words, not his hands: the usual modes, a hard no slaps him)
        # ==========================
        "flirt_lewd_compliment_tits_shy_yes": [
            _("...Crude. But accurate."),
            _("Hm. Say it with better words next time."),
        ],
        "flirt_lewd_compliment_tits_normal_yes": [
            _("I know. They're not for you. Yet."),
            _("Crude, but honest. I appreciate honesty."),
        ],
        "flirt_lewd_compliment_tits_enthusiastic_yes": [
            _("Mm. They are. Keep staring, it's the closest you'll get today."),
            _("Of course they are. Look all you want. Touching is a privilege you haven't earned."),
        ],
        "flirt_lewd_compliment_tits_obedient_yes": [
            _("Fine. Thank you, I suppose."),
            _("Noted. Now keep your eyes up."),
        ],
        "flirt_lewd_compliment_tits_soft_no": [
            _("Vulgar. You can do better than that, [Player.Name]."),
            _("Talk to me like that when you've earned the right."),
        ],
        "flirt_lewd_compliment_tits_hard_no": [
            _("Talk about my body like that again and you'll lose more than your allowance."),
            _("Is that how you speak to your father's wife? Disgusting."),
        ],

        # ==========================
        # LEWD COMPLIMENT: ASS
        # ==========================
        "flirt_lewd_compliment_ass_shy_yes": [
            _("...You've been looking. Of course you have."),
            _("Hm. Bold. Keep it to yourself next time."),
        ],
        "flirt_lewd_compliment_ass_normal_yes": [
            _("Pilates and good tailoring. Glad you noticed."),
            _("It does. Now stop staring before I start charging you for it."),
        ],
        "flirt_lewd_compliment_ass_enthusiastic_yes": [
            _("Mm. It does. Follow it and you might learn something."),
            _("Of course it does. It's worth more than you are."),
        ],
        "flirt_lewd_compliment_ass_obedient_yes": [
            _("Fine. Noted."),
            _("If you say so, [Player.Name]."),
        ],
        "flirt_lewd_compliment_ass_soft_no": [
            _("Crude. Try again with a vocabulary."),
            _("Keep your eyes above my waist, [Player.Name]."),
        ],
        "flirt_lewd_compliment_ass_hard_no": [
            _("You're talking about your father's wife. Remember that before you open your mouth."),
            _("Say that again and see what it costs you."),
        ],

        # ==========================
        # HIS HANDS ON HER (FEMDOM_FLIRT_PENALTY): she answers in command, always
        # ==========================

        # ---- SLAP HER ASS ----
        "flirt_lewd_slap_ass_commanding_no": [
            _("You don't spank me, boy. I spank you. Remember the order of things."),
            _("Did I give you permission? No. Then that hand stays still."),
            _("Try that again and I'll break the habit for you."),
        ],
        "flirt_lewd_slap_ass_commanding_yes": [
            _("One. Consider it a bonus. Bonuses are rare, [Player.Name]."),
            _("Mm. I'll allow it. Don't mistake permission for a promotion."),
            _("Harder next time, or don't bother. And only when I ask for it."),
        ],
        "flirt_lewd_slap_ass_commanding_yes.player_cheating": [
            _("Mm. You like that more than anything she lets you do, don't you? Then end it with her."),
            _("I'll allow it. Now tell that girl it's over. I don't share my investments."),
        ],

        # ---- PINCH HER ASS ----
        "flirt_lewd_pinch_ass_commanding_no": [
            _("Pinching? What are you, twelve? Hand down."),
            _("No. You don't touch me because you feel like it. You touch me because I allow it."),
            _("I've broken men for less. Don't test me."),
        ],
        "flirt_lewd_pinch_ass_commanding_yes": [
            _("Cheeky. I'll let it slide, because I felt like it."),
            _("Mm. You get away with that because I allow it. Only because."),
            _("Fine. Once. Next time you ask first, and you ask nicely."),
        ],

        # ---- GRAB HER TITS ----
        "flirt_lewd_grab_tits_commanding_no": [
            _("Ah-ah... no hands until I say. You haven't earned the right to grab me like that... yet."),
            _("Let go. You don't grab, you ask. And then you wait."),
            _("Wrong move, [Player.Name]. My body runs on my schedule, not yours."),
        ],
        "flirt_lewd_grab_tits_commanding_yes": [
            _("Gently. I'll tell you when you've earned a squeeze."),
            _("You may. For now. I can revoke it whenever I like."),
            _("Slowly, boy. You're handling something far above your means."),
        ],
        "flirt_lewd_grab_tits_commanding_yes.player_cheating": [
            _("Bet she doesn't feel like this. So why are you wasting your time with her?"),
            _("Fine. Enjoy it. Then end things with that girl. She's a distraction."),
        ],

        # ---- GRAB HER ASS ----
        "flirt_lewd_grab_ass_commanding_no": [
            _("Grabbing me isn't how this works. I say when. I say where."),
            _("Let go. Nobody puts their hands on me unless I tell them to."),
            _("Hands where I can see them, [Player.Name]. Now."),
        ],
        "flirt_lewd_grab_ass_commanding_yes": [
            _("Fine. But I decide where your hands go next."),
            _("Mm. Keep it there. Don't move until I say."),
            _("I'll allow it. Enjoy it while I'm feeling generous. I rarely am."),
        ],

        # ---- ASK FOR HER PANTIES (words: no wrist to catch) ----
        "flirt_lewd_ask_panties_commanding_no": [
            _("My panties? I decide who gets them, and you haven't qualified."),
            _("Bold request from a boy who hasn't earned a single thing from me."),
            _("No. Try begging. It might go better."),
        ],
        "flirt_lewd_ask_panties_commanding_yes": [
            _("Maybe. If you're good. Very good, for a very long time."),
            _("You'll get them when I decide you've earned them. Not a minute before."),
            _("Ask me again on your knees and we'll see."),
        ],

        # ---- TOUCH HER THIGHS ----
        "flirt_lewd_touch_thighs_commanding_no": [
            _("Uh-uh. That hand stays at your side until I say otherwise."),
            _("Your hand moved without my signature. Request denied."),
            _("No. I decide who touches me, and when. You're not on the list today."),
        ],
        "flirt_lewd_touch_thighs_commanding_yes": [
            _("That high, [Player.Name]. Not an inch higher without my approval."),
            _("You can leave it there. Moving it is my decision."),
            _("Mm. Good. Now keep very still."),
        ],

        # ---- TOUCH HER TITS ----
        "flirt_lewd_touch_tits_commanding_no": [
            _("Hands off. You don't touch me. I let you touch me. Learn the difference."),
            _("Put it down. I'll tell you what you're allowed to touch."),
            _("Did I say you could? Then don't embarrass yourself."),
        ],
        "flirt_lewd_touch_tits_commanding_yes": [
            _("Softly. I'll grade your technique when you're done."),
            _("Go ahead. You're allowed. This once."),
            _("Mm. Keep going until I say stop. And I will say stop."),
        ],

        # ---- TOUCH HER PUSSY ----
        "flirt_lewd_touch_pussy_commanding_no": [
            _("Absolutely not. That is mine to give, never yours to take."),
            _("Hand. Away. You haven't earned anything close to that."),
            _("Nobody touches me there without my say. Nobody."),
        ],
        "flirt_lewd_touch_pussy_commanding_yes": [
            _("Slowly. And you stop the second I tell you to, or you never touch me again."),
            _("You want it that badly? Good. Wanting is where obedience starts."),
            _("Mm. I'll allow it. Remember whose permission this was."),
        ],

        # ---- SUNSCREEN AT THE POOL: he goes lower than her back ----
        "flirt_lewd_sunscreen_thighs_commanding_no": [
            _("My back, [Player.Name]. I gave you one simple instruction."),
            _("Thighs? That wasn't in the instructions. Back. Now."),
            _("Follow instructions, or I find someone who can."),
        ],
        "flirt_lewd_sunscreen_thighs_commanding_yes": [
            _("The thighs too, then. Slowly. I set the limit, not you."),
            _("I didn't ask for that. But I'll allow it. Be thorough."),
            _("Go on. Carefully. I'll know if you get ideas."),
        ],
        "flirt_lewd_sunscreen_ass_commanding_no": [
            _("That isn't my back. Hands up, where I told you."),
            _("You don't decide what gets covered here. I do."),
            _("My ass wasn't in the brief. Back to work."),
        ],
        "flirt_lewd_sunscreen_ass_commanding_yes": [
            _("Be thorough. I review everyone's work, including yours."),
            _("Mm. Thorough work. That's what I expect from my investments."),
            _("Go ahead. Since I'm in a good mood. Don't waste it."),
        ],

        # ==========================
        # HIS HANDS ON HER FROM HER STAGE 2 (femdom_flirt_mode: no commanding modes from FEMDOM_TURN_NO_HOLD_STAGE)
        # The usual six modes; her stage 3 has its own ".femdom_s3" below, so these are her stage 2 voice: she is
        # cracking. His hands are allowed, on her terms: a yes is grudging permission, annoyed at herself; a no is
        # sharp but no longer "no hands until I say". A hard no slaps him again (flirt_lewd_slaps) and a touch
        # flirt's hard no raises her middle finger first (Flirty.rpy, arm 2). obedient_yes is not in the Global
        # block for these flirts, but get_flirt_reaction_mode_lewd returns it (an allow whose primary reason is
        # Obed): without her pool she would say nothing. No sunscreen pools: flirt_lewd_react reads rod_lines only
        # in the commanding modes, so from stage 2 its inline Flirty.rpy lines speak.
        # ==========================

        # ---- SLAP HER ASS ----
        "flirt_lewd_slap_ass_shy_yes": [
            _("...You've gotten very sure of yourself. I haven't decided yet whether I hate it."),
            _("Hm. I should have stopped that. I didn't. We won't discuss why."),
        ],
        "flirt_lewd_slap_ass_normal_yes": [
            _("Fine. I'll let that one stand. Don't turn it into a habit."),
            _("Cheeky. I'll pretend I didn't enjoy that, and so will you."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes": [
            _("Mm... again. Harder. And wipe that smug look off your face."),
            _("There it is. A man's hand, for once, not a boy's."),
        ],
        "flirt_lewd_slap_ass_obedient_yes": [
            _("...Fine. If that's what you want. Don't look so pleased with yourself."),
            _("I'm letting it go. Not because you earned it. I'm simply tired of fighting you on it."),
        ],
        "flirt_lewd_slap_ass_soft_no": [
            _("Not today, [Player.Name]. I'm in no mood for games."),
            _("Easy. You've gotten bolder, but I still pick the moment."),
        ],
        "flirt_lewd_slap_ass_hard_no": [
            _("Don't you dare. You've gotten far too comfortable, boy."),
            _("Cocky little bastard. Try that again and you'll wear my handprint for a week."),
        ],

        # ---- PINCH HER ASS ----
        "flirt_lewd_pinch_ass_shy_yes": [
            _("...Childish. And still I didn't stop you. Interesting."),
            _("Hm. Don't look at me like that. It meant nothing."),
        ],
        "flirt_lewd_pinch_ass_normal_yes": [
            _("Fine. You're lucky I'm in a forgiving mood."),
            _("Petty. But I'll let you have it."),
        ],
        "flirt_lewd_pinch_ass_enthusiastic_yes": [
            _("Mm. If you're going to pinch, at least have the nerve to grab."),
            _("Bold boy. Again, and mean it this time."),
        ],
        "flirt_lewd_pinch_ass_obedient_yes": [
            _("...Fine. I'm not going to fight you over a pinch."),
            _("Go on, then. You'd do it anyway, wouldn't you?"),
        ],
        "flirt_lewd_pinch_ass_soft_no": [
            _("Not now. And grow out of pinching, it's beneath you."),
            _("Not today, boy. I have a headache, and you're not helping."),
        ],
        "flirt_lewd_pinch_ass_hard_no": [
            _("Pinch me again and I'll break that finger."),
            _("Did you forget who you're touching? Allow me to remind you."),
        ],

        # ---- GRAB HER TITS ----
        "flirt_lewd_grab_tits_shy_yes": [
            _("...I'm letting you. Don't ask me why. I haven't worked it out myself."),
            _("...Your hands are steadier than they used to be. I noticed. Unfortunately."),
        ],
        "flirt_lewd_grab_tits_normal_yes": [
            _("Fine. Hold them. Just don't act like you've won something."),
            _("Hm. Firmer than I expected. I'll allow it."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes": [
            _("Mm... yes. Like that. Not a word to anyone, understood?"),
            _("God, your hands... I hate how much I like this."),
        ],
        "flirt_lewd_grab_tits_obedient_yes": [
            _("Fine. Take them. You wanted them badly enough."),
            _("If you insist... go ahead. I'm done arguing with you."),
        ],
        "flirt_lewd_grab_tits_soft_no": [
            _("Not now, [Player.Name]. Hands down. I'm not in the mood."),
            _("Not like that. You touch a woman like me slowly, or not at all."),
        ],
        "flirt_lewd_grab_tits_hard_no": [
            _("You've gotten far too sure of yourself. Let go."),
            _("Grab me like some cheap date again and you'll regret it."),
        ],

        # ---- GRAB HER ASS ----
        "flirt_lewd_grab_ass_shy_yes": [
            _("...You're bolder than you were. I should hate that more than I do."),
            _("Hm. I didn't push you away. Neither of us mentions that."),
        ],
        "flirt_lewd_grab_ass_normal_yes": [
            _("Fine. Keep it there. Briefly."),
            _("Mm. Pilates pays off, I see. Enjoy it for a moment."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes": [
            _("Mm... squeeze. Don't turn timid on me now."),
            _("That's it. Don't you dare let go yet."),
        ],
        "flirt_lewd_grab_ass_obedient_yes": [
            _("...Fine. Since you won't take no for an answer anymore."),
            _("Go ahead. I'm tired of pretending I'll stop you."),
        ],
        "flirt_lewd_grab_ass_soft_no": [
            _("Not here. Hands to yourself for now."),
            _("Not now, boy. You're pushing your luck today."),
        ],
        "flirt_lewd_grab_ass_hard_no": [
            _("Let go. Since when do you handle me like that?"),
            _("Push me like that again and you'll find out how hard I hit."),
        ],

        # ---- ASK FOR HER PANTIES (words) ----
        "flirt_lewd_ask_panties_shy_yes": [
            _("...You'd really keep them. God. Fine. Maybe."),
            _("Hm. I'm not saying yes. I'm not saying no, either."),
        ],
        "flirt_lewd_ask_panties_normal_yes": [
            _("Maybe. If you ask nicely, and somewhere private."),
            _("Perhaps. I'll decide when. You'll know."),
        ],
        "flirt_lewd_ask_panties_enthusiastic_yes": [
            _("Mm. Would you keep them under your pillow? ...Don't answer. You'll get them."),
            _("Bold. Fine. You'll find them somewhere you don't expect."),
        ],
        "flirt_lewd_ask_panties_obedient_yes": [
            _("...Fine. If you want them that badly."),
            _("You'll get them. Don't make me regret it."),
        ],
        "flirt_lewd_ask_panties_soft_no": [
            _("Not today. Don't push your luck, boy."),
            _("Ask me again some other time. Today, no."),
        ],
        "flirt_lewd_ask_panties_hard_no": [
            _("My panties are not a souvenir for a schoolboy."),
            _("Have you lost your mind? Watch your mouth, boy."),
        ],

        # ---- TOUCH HER THIGHS ----
        "flirt_lewd_touch_thighs_shy_yes": [
            _("...Hm. Your hand is warm. I'm choosing not to move it."),
            _("...I should stop you. Give me a moment to remember why."),
        ],
        "flirt_lewd_touch_thighs_normal_yes": [
            _("Fine. That high. We'll discuss higher another time."),
            _("Hm. Your hand can stay. For now."),
        ],
        "flirt_lewd_touch_thighs_enthusiastic_yes": [
            _("Mm... don't stop there. I'm not made of glass."),
            _("Higher. If you're going to be bold, finish the job."),
        ],
        "flirt_lewd_touch_thighs_obedient_yes": [
            _("...Fine. Leave it there. I won't argue."),
            _("Go ahead. Apparently I can't say no to you anymore."),
        ],
        "flirt_lewd_touch_thighs_soft_no": [
            _("Not now. Move it before someone sees."),
            _("Not today, [Player.Name]. Back on your own knee."),
        ],
        "flirt_lewd_touch_thighs_hard_no": [
            _("Move that hand or I'll move it for you."),
            _("You're getting greedy, boy. Back off."),
        ],

        # ---- TOUCH HER TITS ----
        "flirt_lewd_touch_tits_shy_yes": [
            _("...Gently. I said gently. ...I didn't say it. I'm saying it now."),
            _("Hm. I'm not stopping you. Neither of us knows why."),
        ],
        "flirt_lewd_touch_tits_normal_yes": [
            _("Fine. Softly. I'm not a stress ball."),
            _("Hm. Acceptable. Your hands have improved."),
        ],
        "flirt_lewd_touch_tits_enthusiastic_yes": [
            _("Mm... don't stop. And don't you dare smirk."),
            _("God... yes. I hate that you know how to do that."),
        ],
        "flirt_lewd_touch_tits_obedient_yes": [
            _("...Fine. Touch them, if you must."),
            _("Go on. I won't pretend I'll stop you."),
        ],
        "flirt_lewd_touch_tits_soft_no": [
            _("Not right now, [Player.Name]. Hands down."),
            _("Not today. Ask me when I'm in a better mood."),
        ],
        "flirt_lewd_touch_tits_hard_no": [
            _("Don't you dare paw at me like that."),
            _("You've gotten very brave. Too brave. Hands off."),
        ],

        # ---- TOUCH HER PUSSY ----
        "flirt_lewd_touch_pussy_shy_yes": [
            _("...Wait. Slowly... God, what are you doing to me?"),
            _("...I should slap you. Why am I not slapping you?"),
        ],
        "flirt_lewd_touch_pussy_normal_yes": [
            _("Fine. Slowly. And not a word about this later."),
            _("Hm. Careful. You're handling something very expensive."),
        ],
        "flirt_lewd_touch_pussy_enthusiastic_yes": [
            _("Mm... don't stop. Don't you dare stop now."),
            _("There... yes. I hate how good you've gotten at this."),
        ],
        "flirt_lewd_touch_pussy_obedient_yes": [
            _("...Fine. Go on. I'm done pretending I don't want it."),
            _("Go on, then. You win this one."),
        ],
        "flirt_lewd_touch_pussy_soft_no": [
            _("Not here. Not now. Pull your hand back."),
            _("Too far for today, [Player.Name]. Hand away."),
        ],
        "flirt_lewd_touch_pussy_hard_no": [
            _("Absolutely not. Who do you think you are, boy?"),
            _("Get your hand out of there before I break it."),
        ],

        # ==========================
        # AFTER HER TURN: STAGE 3 ("<key>.femdom_s3", femdom_stage_mod): she is his, behind his father's back
        # Her stage comes first of the modifiers in rod_flirt_line: these beat every other pool, ".player_cheating"
        # and the role's trait variants included (so no girlfriend talk here). Her pride and her tongue stay:
        # possessive, sensual, taunting about his father. Her no is about the risk (his father, being seen), never
        # about him not deserving her. Never "your father is away": a flirt can't know it (a question or an "if").
        # ==========================

        # ---- SAFE TOUCHES (all six modes: get_flirt_reaction_mode_safe) ----

        # TOUCH CHEEK
        "flirt_safe_touch_cheek_shy_yes.femdom_s3": [
            _("...Don't look at me like that. I'm still not used to being yours."),
            _("...Your hand fits there now. I don't like how much I like that."),
        ],
        "flirt_safe_touch_cheek_normal_yes.femdom_s3": [
            _("There you are. My boy, with his hand on his father's wife."),
            _("Mm. Go on. This face is yours, behind closed doors."),
        ],
        "flirt_safe_touch_cheek_enthusiastic_yes.femdom_s3": [
            _("Well, well... Did little [Player.Name] finally grow enough spine to come to me behind his father's back?"),
            _("Mm. Touch me like that in front of your father and see what happens. ...No. Don't."),
        ],
        "flirt_safe_touch_cheek_obedient_yes.femdom_s3": [
            _("Whatever you want, [Player.Name]. You know that by now."),
            _("Go ahead. I stopped saying no to you a while ago."),
        ],
        "flirt_safe_touch_cheek_soft_no.femdom_s3": [
            _("Not here. One wrong look and this whole thing burns down."),
            _("Careful. Save it for when no one's around to see."),
        ],
        "flirt_safe_touch_cheek_hard_no.femdom_s3": [
            _("Are you out of your mind? Not where anyone can see us."),
            _("Hand down, now. If the wrong person sees that, we're both finished."),
        ],

        # HOLD HANDS
        "flirt_safe_hold_hands_shy_yes.femdom_s3": [
            _("...Holding hands. Like a couple. God, what have you done to me?"),
            _("...Fine. Just don't be the first to let go."),
        ],
        "flirt_safe_hold_hands_normal_yes.femdom_s3": [
            _("Hold it, then. Just let go the second anyone looks our way."),
            _("Mm. When did your father last hold my hand? I can't remember. You may."),
        ],
        "flirt_safe_hold_hands_enthusiastic_yes.femdom_s3": [
            _("Mm. Hold it like you're claiming me. Because you are."),
            _("Tighter. This hand is yours now. Act like it."),
        ],
        "flirt_safe_hold_hands_obedient_yes.femdom_s3": [
            _("Take it. You don't need to ask anymore."),
            _("Of course. It's yours whenever you want it."),
        ],
        "flirt_safe_hold_hands_soft_no.femdom_s3": [
            _("Not here. A hand in mine is the kind of thing people remember."),
            _("Later. When there's no one around to wonder why."),
        ],
        "flirt_safe_hold_hands_hard_no.femdom_s3": [
            _("Let go. Now. Do you want the whole world to know?"),
            _("Are you trying to get us caught? Hands apart."),
        ],

        # KISS CHEEK
        "flirt_safe_kiss_cheek_shy_yes.femdom_s3": [
            _("...On the cheek. How restrained. I almost miss the boy who'd never dare."),
            _("...Hm. Sweet. Don't let anyone see me smile at it."),
        ],
        "flirt_safe_kiss_cheek_normal_yes.femdom_s3": [
            _("Mm. The cheek. Save the rest for when we're alone."),
            _("Sweet. That's how your father kisses me. You can do much better."),
        ],
        "flirt_safe_kiss_cheek_enthusiastic_yes.femdom_s3": [
            _("The cheek? You can aim lower than that now. You've earned it."),
            _("Mm. You missed my mouth, [Player.Name]. Try again."),
        ],
        "flirt_safe_kiss_cheek_obedient_yes.femdom_s3": [
            _("Of course. Kiss me wherever you like."),
            _("There. Anything else my boy wants?"),
        ],
        "flirt_safe_kiss_cheek_soft_no.femdom_s3": [
            _("Not now. Lipstick marks are evidence, [Player.Name]."),
            _("Wait until we're alone. I'm not getting caught over a kiss on the cheek."),
        ],
        "flirt_safe_kiss_cheek_hard_no.femdom_s3": [
            _("Not here! Do you want to be the one who explains that to your father?"),
            _("Back up. Someone could see, and then we lose everything."),
        ],

        # STEAL A KISS (yes: _kiss_accepted; no: then a slap)
        "flirt_safe_steal_kiss_shy_yes.femdom_s3": [
            _("...You still take my breath away when you do that. I'll deny I ever said it."),
            _("...Again. No. Wait. ...Again."),
        ],
        "flirt_safe_steal_kiss_normal_yes.femdom_s3": [
            _("Your old man would be crying if he saw us... too bad for him."),
            _("Mm. Stolen from your father's wife. It tastes better that way, doesn't it?"),
        ],
        "flirt_safe_steal_kiss_enthusiastic_yes.femdom_s3": [
            _("Mm... that's my boy. Take what's yours."),
            _("There it is. Kiss me like that and I forget I have a husband."),
        ],
        "flirt_safe_steal_kiss_obedient_yes.femdom_s3": [
            _("Take as many as you want. They're all yours."),
            _("Mm. You don't need to steal what already belongs to you."),
        ],
        "flirt_safe_steal_kiss_soft_no.femdom_s3": [
            _("Not here, you idiot. If anyone saw that, it's over."),
            _("Are you trying to get caught? Wait until the door is locked."),
        ],
        "flirt_safe_steal_kiss_hard_no.femdom_s3": [
            _("Have you lost your mind? Anyone could have seen that!"),
            _("Do you want your father to find out like this? Think, boy."),
        ],

        # HUG
        "flirt_safe_hug_shy_yes.femdom_s3": [
            _("...Hold me a moment longer. Don't make it a big deal."),
            _("...You feel like home. That's a dangerous thing to admit to you."),
        ],
        "flirt_safe_hug_normal_yes.femdom_s3": [
            _("Mm. Come here, my boy. You're the only one who holds me properly."),
            _("There. Now I'll smell like you all day. Careful, someone might notice."),
        ],
        "flirt_safe_hug_enthusiastic_yes.femdom_s3": [
            _("Come closer, boy. You've been staring at my tits for months... do you think I don't notice when you adjust yourself under the table?"),
            _("Closer. I want to feel exactly how much you missed me."),
        ],
        "flirt_safe_hug_obedient_yes.femdom_s3": [
            _("Of course. Come here."),
            _("Whatever you need, [Player.Name]. Hold on to me."),
        ],
        "flirt_safe_hug_soft_no.femdom_s3": [
            _("Not here. A hug like ours lasts too long to explain."),
            _("Later. When there's nobody to see how I lean into you."),
        ],
        "flirt_safe_hug_hard_no.femdom_s3": [
            _("Step back. Now. Someone could walk in at any second."),
            _("Not here, are you mad? Arms down before we're seen."),
        ],

        # ---- COMPLIMENTS SHE LOVES (GIRL_COMPLIMENT_TASTE; face to face AND by phone: each line works as a text) ----

        # CONFIDENCE
        "flirt_safe_compliment_confidence_shy_yes.femdom_s3": [
            _("...You're the only one who ever made it slip. Don't tell anyone."),
            _("...Funny. Around you, I'm not so sure of myself anymore."),
        ],
        "flirt_safe_compliment_confidence_normal_yes.femdom_s3": [
            _("Of course. It takes confidence to cheat on your father with his own son."),
            _("Mm. It takes nerve to be yours and still sit at his table."),
        ],
        "flirt_safe_compliment_confidence_enthusiastic_yes.femdom_s3": [
            _("Mm. Wait until I turn all of it on you."),
            _("Good. I run a company and still answer to you. Enjoy that."),
        ],
        "flirt_safe_compliment_confidence_obedient_yes.femdom_s3": [
            _("Thank you, [Player.Name]. Coming from you, it means something."),
            _("Mm. You're the only one I lower it for."),
        ],
        "flirt_safe_compliment_confidence_soft_no.femdom_s3": [
            _("Not now. Compliments like that make me careless, and careless gets us caught."),
            _("Careful. If I start smiling at you like that, people will ask why."),
        ],
        "flirt_safe_compliment_confidence_hard_no.femdom_s3": [
            _("Don't. Not like this, not where it could get back to your father."),
            _("Enough, [Player.Name]. Sweet talk like that leaves a trail."),
        ],

        # GORGEOUS
        "flirt_safe_compliment_gorgeous_shy_yes.femdom_s3": [
            _("...Hey yourself. You still make me feel like that."),
            _("...Gorgeous. From you, it still lands."),
        ],
        "flirt_safe_compliment_gorgeous_normal_yes.femdom_s3": [
            _("Hello, my boy. Gorgeous, and all yours."),
            _("Mm. Hey there, handsome. Don't tell your father I said that."),
        ],
        "flirt_safe_compliment_gorgeous_enthusiastic_yes.femdom_s3": [
            _("Mm. Say it again. I could get used to hearing it from you."),
            _("Gorgeous, and yours. Your father only thinks I'm his."),
        ],
        "flirt_safe_compliment_gorgeous_obedient_yes.femdom_s3": [
            _("Hello, [Player.Name]. Call me whatever you like."),
            _("Mm. Yes. Yours to call that."),
        ],
        "flirt_safe_compliment_gorgeous_soft_no.femdom_s3": [
            _("Careful who's around when you call me that."),
            _("Not now. Treat me like your stepmother until we're alone."),
        ],
        "flirt_safe_compliment_gorgeous_hard_no.femdom_s3": [
            _("Don't you dare call me that where it could get back to him!"),
            _("Are you mad? A stepson doesn't greet his father's wife like that. Not where anyone could notice."),
        ],

        # OUTFIT STYLE
        "flirt_safe_compliment_outfit_style_shy_yes.femdom_s3": [
            _("...I picked it thinking about you. Don't let that go to your head."),
            _("...Hm. You noticed. I wore it for you."),
        ],
        "flirt_safe_compliment_outfit_style_normal_yes.femdom_s3": [
            _("It should. I dress for you now, not for him."),
            _("Mm. Let your father think I wore it for work. It's for you."),
        ],
        "flirt_safe_compliment_outfit_style_enthusiastic_yes.femdom_s3": [
            _("Mm. Then imagine how it looks on your floor."),
            _("Glad you like it. You'll like it even more when it comes off."),
        ],
        "flirt_safe_compliment_outfit_style_obedient_yes.femdom_s3": [
            _("Thank you, [Player.Name]. I'll wear it for you again."),
            _("Mm. Then I'll keep wearing it."),
        ],
        "flirt_safe_compliment_outfit_style_soft_no.femdom_s3": [
            _("Careful. Compliments like that make people wonder who I'm dressing for."),
            _("Not now. Notice me less obviously, [Player.Name]."),
        ],
        "flirt_safe_compliment_outfit_style_hard_no.femdom_s3": [
            _("Enough. That's not how a stepson talks to me, and someone will notice."),
            _("Stop. One comment like that in the wrong company and your father starts asking questions."),
        ],

        # SMART
        "flirt_safe_compliment_smart_shy_yes.femdom_s3": [
            _("...Smart enough to know I shouldn't be yours. And yet here I am."),
            _("...Coming from the one who got the better of me, that means something."),
        ],
        "flirt_safe_compliment_smart_normal_yes.femdom_s3": [
            _("Smart enough to keep us secret. Remember that."),
            _("One of? I'm smart enough to fool your father every single day."),
        ],
        "flirt_safe_compliment_smart_enthusiastic_yes.femdom_s3": [
            _("Mm. Smart enough to choose you over him. Clever girl, wasn't I?"),
            _("Mm. And clever enough to find us time alone whenever I want."),
        ],
        "flirt_safe_compliment_smart_obedient_yes.femdom_s3": [
            _("Thank you, [Player.Name]. You're the only one who ever outsmarted me."),
            _("Mm. Smart enough to know who I belong to now."),
        ],
        "flirt_safe_compliment_smart_soft_no.femdom_s3": [
            _("Not now. Smart means not getting caught, [Player.Name]."),
            _("Flattery in the wrong place leaves fingerprints. Later."),
        ],
        "flirt_safe_compliment_smart_hard_no.femdom_s3": [
            _("Enough. Smart is not getting caught. Act like it."),
            _("Don't. Praise like that gets noticed, and noticed is the end of us."),
        ],

        # ---- LEWD COMPLIMENTS (words; face to face AND by phone; a hard no face to face still slaps) ----

        # TITS
        "flirt_lewd_compliment_tits_shy_yes.femdom_s3": [
            _("...Hm. Coming from you, I'll take it. Only from you."),
            _("...They're yours, you know. Say it like you know it."),
        ],
        "flirt_lewd_compliment_tits_normal_yes.femdom_s3": [
            _("Of course they are. And they're yours, not his."),
            _("Mm. Good. I dress them up for you now, not for him."),
        ],
        "flirt_lewd_compliment_tits_enthusiastic_yes.femdom_s3": [
            _("Mm. Then come and prove it. They've been waiting."),
            _("Keep talking like that and I'll make you show me how much you mean it."),
        ],
        "flirt_lewd_compliment_tits_obedient_yes.femdom_s3": [
            _("Thank you, [Player.Name]. They're yours."),
            _("Mm. Whatever pleases you."),
        ],
        "flirt_lewd_compliment_tits_soft_no.femdom_s3": [
            _("Careful, [Player.Name]. Words like that have a way of reaching the wrong ears."),
            _("Not now. Save that kind of talk for when we're alone."),
        ],
        "flirt_lewd_compliment_tits_hard_no.femdom_s3": [
            _("Watch it! One slip like that and your father hears about us."),
            _("Not one more word like that. Do you have any idea what we'd lose?"),
        ],

        # ASS
        "flirt_lewd_compliment_ass_shy_yes.femdom_s3": [
            _("...You do have a way of noticing. I like that it's you."),
            _("...It's yours to look at. Only yours."),
        ],
        "flirt_lewd_compliment_ass_normal_yes.femdom_s3": [
            _("Of course it does. I keep it that way for you now."),
            _("Mm. Your father never says that. Then again, he never looks."),
        ],
        "flirt_lewd_compliment_ass_enthusiastic_yes.femdom_s3": [
            _("You want to fuck me? Tee-hee... bastard, you think I haven't noticed how you stare at my ass when you think I'm not looking?"),
            _("Mm. Then stop admiring it and do something about it."),
        ],
        "flirt_lewd_compliment_ass_obedient_yes.femdom_s3": [
            _("Thank you. It's yours, after all."),
            _("Mm. If it pleases you, [Player.Name]."),
        ],
        "flirt_lewd_compliment_ass_soft_no.femdom_s3": [
            _("Not now. Talk like that is how secrets get out."),
            _("Careful, boy. Somebody's always listening."),
        ],
        "flirt_lewd_compliment_ass_hard_no.femdom_s3": [
            _("Shut up! If anyone ever heard you say that to me..."),
            _("Enough. You'll get us caught with that mouth."),
        ],

        # ---- HIS HANDS ON HER (the usual six modes; a hard no slaps him, a touch flirt's adds arm 2) ----

        # SLAP HER ASS
        "flirt_lewd_slap_ass_shy_yes.femdom_s3": [
            _("...You know exactly what that does to me now. Bastard."),
            _("...Again. Quietly this time."),
        ],
        "flirt_lewd_slap_ass_normal_yes.femdom_s3": [
            _("Mm. Your mark on me. Your father will never know where it came from."),
            _("Go on, then. That ass answers to you now."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.femdom_s3": [
            _("Harder. I want to feel you the next time I sit down to dinner with him."),
            _("Mm... yes. Spank your father's wife like you own her. You do."),
        ],
        "flirt_lewd_slap_ass_obedient_yes.femdom_s3": [
            _("As you like, [Player.Name]. It's yours to slap."),
            _("Of course. Whenever you want."),
        ],
        "flirt_lewd_slap_ass_soft_no.femdom_s3": [
            _("Not here. That sound carries."),
            _("Later, boy. Somewhere no one can hear how I react."),
        ],
        "flirt_lewd_slap_ass_hard_no.femdom_s3": [
            _("Idiot! Do you want someone to hear that?"),
            _("Not where we can be caught. Ever. Is that clear?"),
        ],

        # PINCH HER ASS
        "flirt_lewd_pinch_ass_shy_yes.femdom_s3": [
            _("...Brat. You're lucky I'm yours."),
            _("...Hm. I'll pay you back for that later. In private."),
        ],
        "flirt_lewd_pinch_ass_normal_yes.femdom_s3": [
            _("Mm. Cheeky. That's my boy."),
            _("Playful today? Fine. Your father never once dared that."),
        ],
        "flirt_lewd_pinch_ass_enthusiastic_yes.femdom_s3": [
            _("Mm. Don't just pinch it. It's yours. Take hold of it."),
            _("Tease. Keep that up and I'll drag you somewhere private."),
        ],
        "flirt_lewd_pinch_ass_obedient_yes.femdom_s3": [
            _("Go on. You don't need my permission anymore."),
            _("As you wish. It's yours anyway."),
        ],
        "flirt_lewd_pinch_ass_soft_no.femdom_s3": [
            _("Not here. Behave until we're alone."),
            _("Careful. Someone might see, and I'm not explaining a pinch."),
        ],
        "flirt_lewd_pinch_ass_hard_no.femdom_s3": [
            _("Stop it. Are you trying to get us caught?"),
            _("Hands off, now. One witness and everything ends."),
        ],

        # GRAB HER TITS
        "flirt_lewd_grab_tits_shy_yes.femdom_s3": [
            _("...They're yours. I still can't believe I'm saying that."),
            _("...Mm. Slowly. I want to remember this."),
        ],
        "flirt_lewd_grab_tits_normal_yes.femdom_s3": [
            _("Mm. He put a ring on me. You put your hands on me. Guess which I prefer."),
            _("There. Exactly where your hands belong."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.femdom_s3": [
            _("Mm... yes. Squeeze. They've been waiting for you all day."),
            _("God, yes. He never touches me like this. Never."),
        ],
        "flirt_lewd_grab_tits_obedient_yes.femdom_s3": [
            _("They're yours, [Player.Name]. Take them."),
            _("Go ahead. Whatever my boy wants."),
        ],
        "flirt_lewd_grab_tits_soft_no.femdom_s3": [
            _("Not here. Someone could walk in on us."),
            _("Wait. Too many eyes around. Later, I promise."),
        ],
        "flirt_lewd_grab_tits_hard_no.femdom_s3": [
            _("Let go! Do you want us caught with your hands on me?"),
            _("Not here, you fool. Think before you grab."),
        ],

        # GRAB HER ASS
        "flirt_lewd_grab_ass_shy_yes.femdom_s3": [
            _("...Mm. Your hands know me too well now."),
            _("...Don't let go yet. Not yet."),
        ],
        "flirt_lewd_grab_ass_normal_yes.femdom_s3": [
            _("Mm. I keep it in shape, you get to grab it. Fair trade."),
            _("Hold on to it. Your father certainly doesn't."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.femdom_s3": [
            _("Mm... squeeze it. It's all yours, and he'll never have it like you do."),
            _("Harder. Let me feel how much you want what's his."),
        ],
        "flirt_lewd_grab_ass_obedient_yes.femdom_s3": [
            _("Of course. Grab whatever you want, it's yours."),
            _("Mm. As you like, [Player.Name]."),
        ],
        "flirt_lewd_grab_ass_soft_no.femdom_s3": [
            _("Not here. Wait until we're behind a locked door."),
            _("Easy. People notice where a boy's hands go."),
        ],
        "flirt_lewd_grab_ass_hard_no.femdom_s3": [
            _("Hands off! Do you want to be caught grabbing your father's wife?"),
            _("Not here. Never here. Understood?"),
        ],

        # ASK FOR HER PANTIES (words)
        "flirt_lewd_ask_panties_shy_yes.femdom_s3": [
            _("...You'd keep them. You'd actually keep them. Fine. They're yours."),
            _("...I'll slip them into your pocket. Don't let anyone find them."),
        ],
        "flirt_lewd_ask_panties_normal_yes.femdom_s3": [
            _("Mm. You'll have them before the day is over. Hide them well."),
            _("Fine. One more thing of mine your father will never know is missing."),
        ],
        "flirt_lewd_ask_panties_enthusiastic_yes.femdom_s3": [
            _("Mm. Want them warm? Then you'll have to come and take them."),
            _("Take them. I'll spend the rest of the day bare and thinking of you."),
        ],
        "flirt_lewd_ask_panties_obedient_yes.femdom_s3": [
            _("Of course. Whatever you want from me."),
            _("They're yours. Everything is, remember?"),
        ],
        "flirt_lewd_ask_panties_soft_no.femdom_s3": [
            _("Not today. If those turn up in your room, how would you explain them?"),
            _("Not now. Every piece of laundry gets counted in my house."),
        ],
        "flirt_lewd_ask_panties_hard_no.femdom_s3": [
            _("Are you insane? Not where anyone can hear you ask that!"),
            _("Lower your voice! Do you want the whole world to know?"),
        ],

        # TOUCH HER THIGHS
        "flirt_lewd_touch_thighs_shy_yes.femdom_s3": [
            _("...Mm. Your hand belongs there. I hate that I think that."),
            _("...Slower. I want to feel every inch."),
        ],
        "flirt_lewd_touch_thighs_normal_yes.femdom_s3": [
            _("Mm. Higher, if you like. You know the way."),
            _("Go on. I like your hand there."),
        ],
        "flirt_lewd_touch_thighs_enthusiastic_yes.femdom_s3": [
            _("Higher. Don't make your father's wife beg."),
            _("Mm... yes. Keep going until I can't think about anything else."),
        ],
        "flirt_lewd_touch_thighs_obedient_yes.femdom_s3": [
            _("Wherever you want, [Player.Name]."),
            _("Go ahead. I'm yours to touch."),
        ],
        "flirt_lewd_touch_thighs_soft_no.femdom_s3": [
            _("Not here. There's only so much I can hide."),
            _("Easy. Not where people can see your hand."),
        ],
        "flirt_lewd_touch_thighs_hard_no.femdom_s3": [
            _("Not here, idiot! Someone's going to see!"),
            _("Hand away. Now. You'll get us both thrown out of this family."),
        ],

        # TOUCH HER TITS
        "flirt_lewd_touch_tits_shy_yes.femdom_s3": [
            _("...Gently. I'm still getting used to belonging to someone."),
            _("...Mm. Your hands are warm. Stay."),
        ],
        "flirt_lewd_touch_tits_normal_yes.femdom_s3": [
            _("Mm. Go on. You know how I like it."),
            _("There. Exactly the way he never does it."),
        ],
        "flirt_lewd_touch_tits_enthusiastic_yes.femdom_s3": [
            _("Mm... more. Make me forget whose ring I'm wearing."),
            _("Yes... like that. Your father never learned how. You did."),
        ],
        "flirt_lewd_touch_tits_obedient_yes.femdom_s3": [
            _("Of course. Touch me however you want."),
            _("They're yours. You don't need to ask."),
        ],
        "flirt_lewd_touch_tits_soft_no.femdom_s3": [
            _("Not here, [Player.Name]. Too many eyes."),
            _("Later. I want you, just not where we could be caught."),
        ],
        "flirt_lewd_touch_tits_hard_no.femdom_s3": [
            _("Stop it. Someone could see us, you idiot!"),
            _("Not here. Do you want to throw everything away for a grope?"),
        ],

        # TOUCH HER PUSSY
        "flirt_lewd_touch_pussy_shy_yes.femdom_s3": [
            _("...Mm. You know it's yours. Be gentle with it."),
            _("...God. Just you. Only ever you now."),
        ],
        "flirt_lewd_touch_pussy_normal_yes.femdom_s3": [
            _("Mm. It belongs to you now. Remember that."),
            _("There. Better than he ever did, and you know it."),
        ],
        "flirt_lewd_touch_pussy_enthusiastic_yes.femdom_s3": [
            _("Mm... don't stop. I'm all yours, boy. Only yours."),
            _("Yes... right there. If your father could see what you do to me..."),
        ],
        "flirt_lewd_touch_pussy_obedient_yes.femdom_s3": [
            _("Whatever you want. Take your time."),
            _("Of course, [Player.Name]. I'm yours."),
        ],
        "flirt_lewd_touch_pussy_soft_no.femdom_s3": [
            _("Not here. I won't be able to stay quiet."),
            _("Wait. Somewhere private, where you can finish what you start."),
        ],
        "flirt_lewd_touch_pussy_hard_no.femdom_s3": [
            _("Not here! Are you trying to ruin us both?"),
            _("Get your hand back, now. If anyone sees, it's over."),
        ],

        # ==========================
        # PREGNANCY CHITCHAT: "do you ever think about having kids?" (chitchat_ask_about_kids, not pregnant)
        # ==========================
        "pregnancy_ask_about_kids": [
            _("I already have one to raise. You. It's exhausting enough."),
            _("Children are a long-term investment with uncertain returns. I'm still evaluating the one I have."),
            _("Someday is a word for people without a calendar. Mine is full."),
        ],
        "pregnancy_ask_about_kids_mid": [
            _("Perhaps. When it suits me. Nothing in my life happens by accident."),
            _("I've thought about it. Then I look at you and remember how much work one of you is."),
        ],
        "pregnancy_ask_about_kids_fetish": [
            _("...More than a woman in my position should. That stays between us."),
            _("I think about it. Often. Don't ever repeat that to anyone."),
        ],
        "pregnancy_ask_about_kids_fear": [
            _("No. Nine months with my body out of my control? Never."),
            _("Absolutely not. I don't hand control of my life to anyone. Not even a child."),
        ],
    }
