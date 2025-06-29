









init python:
    config.rollback_enabled = False
    menu_trans_time = 1

    splash_message = _("This game is an unofficial fan work, unaffiliated with Team Salvato.")

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)


image menu_logo:
    "mod_assets/jnlogo.png"
    subpixel True
    xcenter 240
    ycenter 120
    zoom 0.60
    menu_logo_move



image menu_bg:
    topleft
    "mod_assets/backgrounds/menu/backdrop.png"
    menu_bg_move

image game_menu_bg:
    topleft
    "mod_assets/backgrounds/menu/backdrop.png"
    menu_bg_loop

image menu_fade:
    "white"
    menu_fadeout

image menu_art_n:
    subpixel True
    "gui/menu_art_n.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

image menu_nav:
    "mod_assets/backgrounds/menu/background.png"
    menu_nav_move

image menu_particles:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/menu_particle.png", explodeTime=0, numParticles=20, particleTime=2.0, particleXSpeed=6, particleYSpeed=4).sm
    particle_fadeout

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset 0 yoffset -160
        repeat

transform menu_bg_loop:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset 0 yoffset -160
        repeat

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

image intro:
    truecenter
    "white"
    0.5
    "bg/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image tos_a = "mod_assets/backgrounds/menu/tos_a.png"
image tos_b = "mod_assets/backgrounds/menu/tos_b.png"

label splashscreen:
    $ set_language_fonts()


    if persistent.language == None:
        call screen choose_language
    
    # elif persistent.language == "spanish":
    #     python:
    #         renpy.change_language('spanish')
    
    # elif persistent.language == "english":
    #     python:
    #         renpy.change_language(None)

    default persistent.has_launched_before = False
    $ persistent.tried_skip = False
    if not persistent.has_launched_before:
        scene white
        $ quick_menu = False
        pause 0.5
        scene tos_a
        with Dissolve(1.0)
        pause 1.0
        "[config.name] is a Doki Doki Literature Club fan mod that is not affiliated with Team Salvato."
        "It is designed to be played only after the official game has been completed, and contains spoilers for the official game."
        "Game files for Doki Doki Literature Club are required to play this mod and can be downloaded for free at: http://ddlc.moe"
        $ narrator(
            _("By playing [config.name] you agree that you have completed Doki Doki Literature Club and accept any spoilers contained within."),
            interact=False
        )
        $ renpy.display_menu(items=[ (_("I agree."), True)], screen="choice_centred")
        scene tos_b
        with Dissolve(1)
        pause 1.0

        scene black
        with Dissolve(1)





        $ persistent.has_launched_before = True




    if not persistent.jn_first_visited_date:
        $ persistent.jn_first_visited_date = datetime.datetime.now()

    jump autoload

label after_load:
    $ config.allow_skipping = False
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False
    $ style.say_dialogue = style.normal
    return

label autoload:
    python:

        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen

        if "_old_history" in globals():
            _history = _old_history
            del _old_history

        renpy.block_rollback()


        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None


    $ store._game_menu_screen  = "preferences"


    $ config.keymap["debug_voicing"] = list()
    $ config.keymap["choose_renderer"] = list()


    $ renpy.pop_call()


    if not jn_introduction.JNIntroductionStates(persistent.jn_introduction_state) == jn_introduction.JNIntroductionStates.complete:
        jump introduction_progress_check
    else:

        jump ch30_autoload

label before_main_menu:
    if persistent.playername != "":
        $ renpy.jump_out_of_context("start")


    $ store._game_menu_screen  = "preferences"

    return

label quit:
    $ renpy.save_persistent()
    python:

        if not Natsuki.getForceQuitAttempt(): # Assuming Natsuki and jn_apologies are defined
            Natsuki.removeApology(jn_apologies.ApologyTypes.sudden_leave)
            
            if Natsuki.getQuitApology() == jn_apologies.ApologyTypes.sudden_leave:
                Natsuki.clearQuitApology()

        # Initialize the flag if it doesn't exist.
        if not hasattr(store, '_splash_rpy_handling_quit'):
            store._splash_rpy_handling_quit = False

        if not store._splash_rpy_handling_quit:
            # This is the first time through this logic block for the current quit operation.
            store._splash_rpy_handling_quit = True # Mark that we are now handling the quit
            
            # Perform save operation once
            jn_utils.saveGame()


            renpy.save_persistent()


            # Attempt to quit. This is THE quit call from this label's logic
            # If renpy.quit() internally re-runs this label in a new context
            # the flag _splash_rpy_handling_quit will be True
            # and this block will be skipped in the re-entrant call
            renpy.quit()
            
            # renpy.quit() should not return
            # Script execution should end or be transferred to Ren'Py's quit sequence
        else:
            # _splash_rpy_handling_quit is True
            # This means this label is being re-entered as part of a renpy.quit() process
            # that was initiated in the block above
            # We should not re-attempt saving or quitting from this re-entrant call
            # Let the original renpy.quit() call complete its process
            pass
        
        # The unconditional renpy.quit() that was here is now removed