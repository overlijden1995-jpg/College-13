# ============================================================
# femdom_lines_rogue.rpy... ROGUE's voice for the femdom trait (docs/plan_femdom.md), read by scene_pick_line
# ============================================================
#
# Keys: "femdom_<moment>.rogue". Her gid is the first modifier in scene_pick_line, so these pools win over the
# shared ones in femdom_lines.rpy (same moments, same comments there say when each one plays).
# Her tone: Southern drawl (sugar, darlin', ain't, dropped g's), warm but bossy, a short temper, mild humiliation.
#
# Discovery phase (D7): "femdom_<moment>.rogue.femdom_first" = her very first scene giving orders (she may say it is
# new), "femdom_<moment>.rogue.femdom_new" = her first few scenes (she may say "again", never "first time").
# Every other pool also plays in her discovery phase, so none claims an old habit, except the veteran-only
# moments (femdom_forced, femdom_force_cum, femdom_force_cum_after).
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests
        # ══════════════════════════════════════════════════════════
        "femdom_refused.rogue": [
            _("Excuse me? I wasn't askin', sugar."),
            _("Did you just tell me no? Oh, darlin', don't you sass me."),
            _("Wrong answer, sugar. Ya best make that up to me, and quick."),
        ],
        "femdom_refused.rogue.femdom_first": [
            _("Hey... I told ya what I wanted. Why's it got me this riled up that ya didn't listen?"),
            _("No? Well... huh. I did not like hearin' that one bit, sugar. That's new."),
        ],
        "femdom_refused.rogue.femdom_new": [
            _("Tellin' me no again, darlin'? It bugs me more every time. Reckon I like callin' the shots."),
            _("Ya keep ignorin' me, sugar, and I keep hatin' it. Guess I'm the bossy type after all."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS: what she orders, and how it ends
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order)
        "femdom_defied_won.rogue": [
            _("Well, ain't you somethin'. Fine, sugar, this one's yours. Don't get used to it."),
            _("Hmph. Look at you, takin' charge. ...Alright, darlin'. Just this once."),
            _("Lucky for you that was hot, sugar. Next time I ain't lettin' ya off so easy."),
        ],
        "femdom_defied_lost.rogue": [
            _("Aw, that was cute, sugar. Now we do it my way."),
            _("Nice try, darlin'. Now hush and let me work."),
            _("Hands where I can see 'em, sugar. You'll get your turn."),
        ],
        "femdom_obeyed.rogue": [
            _("Good. Just like that, sugar."),
            _("Mmm, see how easy it is when ya listen, darlin'?"),
            _("That's it. Keep doin' exactly what I tell ya."),
        ],

        # Take over: she gets on top (from doggy / full nelson / laying down)
        "femdom_take_over.rogue": [
            _("Alright, that's enough of that. On your back, sugar, I'm drivin' now."),
            _("Stop. Lie down, darlin'. I wanna ride ya, and I ain't askin'."),
            _("My turn, sugar. Get under me and keep your hands where I can see 'em."),
        ],
        "femdom_take_over.rogue.femdom_first": [
            _("Wait... lie down, sugar. I wanna be on top. Lord, I ain't never said that to anybody."),
            _("On your back, darlin'. No, I ain't askin'... Huh. Where'd that come from? I kinda like it."),
        ],
        "femdom_take_over.rogue.femdom_new": [
            _("On your back again, sugar. I'm gettin' awful fond of bein' up top."),
            _("Lie down, darlin'. Bossin' ya around is startin' to feel real natural."),
        ],
        # Veteran only: she shoved him onto his back anyway
        "femdom_forced.rogue": [
            _("Wasn't a question, sugar."),
            _("That's better. Now stay put, darlin'."),
            _("Ya really thought ya had a say in this? Oh, sugar."),
        ],

        # Challenge
        "femdom_challenge.rogue": [
            _("Is that all ya got, sugar?"),
            _("Come on, darlin', give it to me like ya mean it. That's an order."),
            _("Lord, I've had more excitement shellin' peas. Prove me wrong, sugar."),
        ],
        "femdom_challenge.rogue.femdom_first": [
            _("That all ya got? ...Well, listen to me. I ain't never talked to anybody like this, and I kinda love it."),
            _("Harder, sugar. ...Lord, where'd that come from? I didn't know I had this much boss in me."),
        ],
        "femdom_challenge.rogue.femdom_new": [
            _("Slackin' again, sugar? Good thing I'm startin' to love tellin' ya what to do."),
            _("Harder, darlin'. Every time I say it, I like sayin' it a lil' more."),
        ],
        "femdom_challenge_met.rogue": [
            _("There it is. That's my good boy."),
            _("Now we're talkin', sugar. Keep that up and I might just reward ya."),
            _("See, darlin'? Ya just needed somebody to light a fire under ya."),
        ],

        # Pace
        "femdom_pace_faster.rogue": [
            _("Faster, darlin'. Don't make me tell ya twice."),
            _("Pick it up, sugar. I didn't say ya could take it easy."),
            _("Faster. Now. My patience ain't that long, sugar."),
        ],
        "femdom_pace_slower.rogue": [
            _("Easy there, sugar. I'm drivin' now."),
            _("Slow it down, darlin'. We go at my speed."),
            _("Whoa there, cowboy. Did I say ya could rush? Slow. Down."),
        ],

        # "Don't you dare cum yet" (any scene: handjob, titjob, footjob, blowjob, positions)
        "femdom_no_cum.rogue": [
            _("Don't ya dare cum yet, sugar."),
            _("Ya cum when I say so, darlin'. Not one second sooner."),
            _("Hold it. I ain't done with ya yet."),
        ],
        "femdom_edge_release.rogue": [
            _("Alright, sugar. Now. Cum for me."),
            _("Go on then, darlin'. Ya earned it. Let go."),
            _("That's my good boy. Ya can cum now."),
        ],
        "femdom_edge_kept.rogue": [
            _("Ya waited 'til I said so. That's how I like it, sugar."),
            _("Look at you, holdin' it 'til I let ya. Good boy."),
            _("Now wasn't that worth the wait, darlin'?"),
        ],
        "femdom_edge_broken.rogue": [
            _("I told ya to wait, sugar. One lil' thing, and ya couldn't do it."),
            _("Did I say ya could cum? No, darlin', I did not."),
            _("Lord have mercy. Ya couldn't hold it for one lousy minute?"),
        ],

        # Where he cums (inside: vaginal or anal; mouth: during a blowjob)
        "femdom_demand_inside.rogue": [
            _("When ya cum, sugar, ya cum inside me. That ain't a request."),
            _("Don't even think about pullin' out, darlin'. Inside me."),
            _("You're finishin' inside me. I already made up my mind, sugar."),
        ],
        "femdom_demand_on_me.rogue": [
            _("When you're close, ya pull out and cum on me, sugar. Understood?"),
            _("Not inside, darlin'. On me, where I can see it."),
            _("You're gonna paint me when ya go, not fill me. My rules, sugar."),
        ],
        "femdom_demand_mouth.rogue": [
            _("When ya cum, it goes in my mouth, sugar. Don't ya dare pull away."),
            _("Every drop on my tongue, darlin'. That's an order."),
            _("Ya cum right here in my mouth and nowhere else, ya hear?"),
        ],
        "femdom_demand_kept.rogue": [
            _("Right where I told ya. Good boy."),
            _("See, sugar? Ya can follow simple directions after all."),
            _("Exactly where I wanted it, darlin'. You're learnin'."),
        ],
        "femdom_demand_broken.rogue": [
            _("That ain't where I told ya to cum, sugar."),
            _("One order, darlin'. One. And ya went and ignored it."),
            _("Wrong spot. Oh, you and me are gonna have words about this."),
        ],

        # Me first
        "femdom_me_first.rogue": [
            _("Ya don't cum 'til I do, sugar. Got it?"),
            _("Ladies first, darlin'. Then maybe you."),
            _("I cum first. That's how this is gonna go, sugar."),
        ],
        "femdom_me_first_kept.rogue": [
            _("Me first, just like I said. That's my good boy."),
            _("Now that's a gentleman. Ladies first, just like I told ya, sugar."),
            _("Mmm, ya took care of me first, darlin'. That's the order I like."),
        ],
        "femdom_me_first_broken.rogue": [
            _("Ya finished before me. I said me first, sugar."),
            _("Unbelievable. One simple rule, darlin', and ya couldn't wait for me."),
            _("Where I come from, a gentleman waits his turn. Next time ya don't cum at all 'til I do."),
        ],

        # He came too fast (her profile's "humiliate": mild)
        "femdom_humiliate_fast.rogue": [
            _("Already? Lord, sugar, I barely got started."),
            _("That's it? Well, bless your heart."),
            _("Quick on the draw, ain't ya? We're gonna have to work on that, darlin'."),
        ],

        # He wants to leave her position (cowgirl / reverse cowgirl) for his
        "femdom_pos_refuse.rogue": [
            _("Ya want me under ya? Cute. No, sugar, I'm stayin' right up here."),
            _("Switch? Nuh uh, darlin'. I'm comfy on top, and you're stayin' put."),
            _("I ain't done ridin' ya yet, sugar. Lie back and enjoy the view."),
        ],

        # Forced cum: a veteran on top keeps him inside (veteran only)
        "femdom_force_cum.rogue": [
            _("Don't ya move, sugar. You're cummin' inside me, right now."),
            _("Pull out? Not a chance, darlin'. Every drop stays in me."),
            _("Hush and hold still. Ya know by now I don't let go that easy."),
        ],
        "femdom_force_cum_after.rogue": [
            _("That's where it belongs, sugar. Remember who decided."),
            _("Next time don't even think about pullin' out, darlin'."),
            _("See? I always get what I want, sugar."),
        ],
    })
