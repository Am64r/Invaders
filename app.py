"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # Attribute _pauseScreen: the pause message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # Attribute _background: the background of the game
    # Invariant: _background is a GImage object, or None if there is no image to
    # display.
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = Wave()
        self._lastkeys = 0
        self._text = GLabel(text="Press 'S' to Play", font_size = 72,
        x = 400, y = 350, font_name = 'Arcade.ttf', fillcolor=None, linecolor='white')
        self._pauseScreen = GLabel(text="Press 'C' to Continue", font_size = 72,
        x = 400, y = 350, font_name = 'Arcade.ttf', fillcolor=None, linecolor="white")
        self._background = GImage(x=GAME_WIDTH//2,y=GAME_HEIGHT//2,
        width=GAME_WIDTH, height=GAME_HEIGHT,source='background.png')
        self._GO = GLabel(text="GAME OVER", font_size = 72,
        x = 400, y = 350, font_name = 'Arcade.ttf', fillcolor=None, linecolor='white')
        self._endW = GLabel(text="YOU DEFEATED THE ALIENS", font_size = 40,
        x = 400, y = 300, font_name = 'Arcade.ttf', fillcolor=None, linecolor='white')
        self._endL = GLabel(text="THE ALIENS HAVE INVADED", font_size = 40,
        x = 400, y = 300, font_name = 'Arcade.ttf', fillcolor=None, linecolor='white')
        self._continue = GLabel(text="Press 'c' to continue...", font_size = 40,
        x = 400, y = 300, font_name = 'Arcade.ttf', fillcolor=None, linecolor='white')
        #self._test = GRectangle(x=40.5,y=518.0,width=10,height=10,fillcolor='red')
        #self._test2 = True



    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        self.determine_game_state()



        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        #elif self_state == STATE_ACTIVE and self._wave.getShip() is none
        elif self._state == STATE_ACTIVE:
            self._wave.update(self.input, dt)
            # Check if the ship is destroyed and lives are remaining
            # if self._wave.getAliens() is None:
            #     print('c')
            #     self._state = STATE_COMPLETE
            if self._wave.getShip() is None and self._wave.getLives() != 0:
                    #print('dog')
                self._state = STATE_PAUSED
                #print('x')
            elif (self._wave.getShip() is None
                and self._wave.getLives() == 0) or self._allDead():
                self._state = STATE_COMPLETE
                #print('helllll')
            # elif (self._wave.bottomPOS() <= DEFENSE_LINE):
            #     self._state = STATE_COMPLETE
            #     self._wave.setLives(0)

        elif self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE
            self._wave.resetShip()
            #print('m')


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """

        self._background.draw(self.view)
        #self._test.draw(self.view)
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
        elif self._state == STATE_PAUSED:
            self._wave.draw(self.view)
            self._continue.draw(self.view)
        elif self._state == STATE_COMPLETE:
            self._GO.draw(self.view)
            if self._wave.getLives() == 0:
                self._endL.draw(self.view)
            else:
                self._endW.draw(self.view)
        else:
            if self._wave is not None:
                self._wave.draw(self.view)


    # HELPER METHODS FOR THE STATES GO HERE
    def _allDead(self):
        for row in self._wave.getAliens():
            for alien in row:
                if alien is not None:
                    return False
        return True
    def key_is_pressed(self):
        """
        Checks if a key is pressd and starts the game.
        """
        return self.input.is_key_pressed('s')

    def key_is_cpressed(self):
        """
        Checks if a key is pressd and starts the game.
        """
        return self.input.is_key_pressed('c')


    def determine_game_state(self):
        """
        Determines the current state and assigns it to
        self.state

        This method checks for a key press, and if there is
        one, changes the state to the next value.  A key
        press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as
        we hold down the key. The user must release the
        key and press it again to change the state.
        """
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count

        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0


        if change:

            if self._state == STATE_INACTIVE and self.key_is_pressed():
                self._state = STATE_NEWWAVE
            #elif self._state = STATE_ACTIVE
            # elif self._state == STATE_ACTIVE and self.key_is_cpressed():
            #     self._state = STATE_PAUSED
            elif self._state == STATE_PAUSED and self.key_is_cpressed():
                self._state = STATE_CONTINUE

                #self._state = STATE_ACTIVE



        # Update last_keys
        self.lastkeys = curr_keys
