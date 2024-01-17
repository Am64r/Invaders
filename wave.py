"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _firerate: the max number of steps taken between a
    # missle from the aliens
    # Invariant: _firerate is a int between 1 and BOLT_RATE
    #
    # Attribute _direction: the direction of the aliens are moving either
    #positve or negative
    # Invariant: _direction is a int of either -1,1
    #
    # Attribute _moveDown: trigger for when the aliens advance down
    # Invariant: _moveDown is a bool either true or false
    #
    # Attribute _alienFireTime: counting the time between when the alien last
    #fires
    # Invariant: _alienFireTime is a float >= 0s
    #
    # Attribute _nextFireTime: Determines how long to wait before firing based
    #on _alienFireTime
    # Invariant: _nextFireTime is a int between 1 and BOLT_RATE
    #
    # Attribute _alienHitEdge: trigger for when the aliens hit end of gamescreen
    # Invariant: _alienHitEdge is a bool either true or false
    #
    # Attribute _pew: sound for shot being fired
    # Invariant: _pew is Sound Object
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAliens(self):
        return self._aliens


    def getLives(self):
        """
        Returns the number of the player's lives left.
        """
        return self._lives


    def setLives(self, lives):
        assert isinstance(lives,int)
        assert lives >= 0
        self._lives = lives

    def getShip(self):
        """
        Returns the ship.
        """
        return self._ship
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    def __init__(self):
        self._ship = Ship()
        self._2dlistAlien()
        self._bolts = []
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth = 0.5, linecolor = 'gray')
        self._lives = SHIP_LIVES
        self._time = 0
        self._direction = 1
        self._moveDown = False
        self._firerate = 1
        self._alienFireTime = 0
        self._nextFireTime = random.randint(1, BOLT_RATE)
        self._alienHitEdge = False
        self._pew = Sound('pew1.wav')

    # Helper methods for initializer
    def _2dlistAlien(self):
        """
        Creates a block (a 2D list) of Alien objects.
        """
        # STARTING X COORDINATE
        startX = ALIEN_H_SEP + ALIEN_WIDTH/2
        # HEIGHT OF THE OF ALIENS
        height = ALIEN_ROWS * ALIEN_HEIGHT + (ALIEN_ROWS-1)*ALIEN_H_SEP
        # STARTING Y COORDINATE
        startY = GAME_HEIGHT - height - ALIEN_CEILING

        self._aliens = []

        for row in range(ALIEN_ROWS):
            # Create a list for this row
            alien_row = []

            # Determine the image for the row
            if row < 2:  # First 2 rows
                alien_image = ALIEN_IMAGES[0]
            elif row < 4:  # 3rd and 4th rows
                alien_image = ALIEN_IMAGES[1]
            else:  # Last row
                alien_image = ALIEN_IMAGES[2]

            for col in range(ALIENS_IN_ROW):
                alien_x = startX + col * (ALIEN_WIDTH + ALIEN_H_SEP)
                alien_y = startY + row * (ALIEN_HEIGHT + ALIEN_V_SEP)

                # Create an Alien object and add it to the row
                alien = Alien(x=alien_x, y=alien_y, image=alien_image)
                alien_row.append(alien)

            self._aliens.append(alien_row)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates the wave by one animation frame.

        Parameter input: The user input, used to control the ship.
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since the last update
        Precondition: dt is a number (int or float)
        """
        self._attemptAlienFire(dt)

        if self._ship is not None:
            self._moveShip(input)
        if self._aliens is not None:

            self._time += dt

            if self._time > ALIEN_SPEED:
                self._walkAliens()

                self._time = 0

        if input.is_key_pressed('spacebar'):
            self._pew.play()
            self._fireShip()
        # Update existing bolts
        self._updateBolts()

        if self._bottomPOS() is not None and self._bottomPOS() <= DEFENSE_LINE:
            self._lives = 0
            self._ship = None

    # Helper METHODS for UPDATE
    def _bottomPOS(self):
        for row_index in range(len(self._aliens)):
            alien = self._aliens[row_index][0]
            if alien is not None:
                return alien.getY() - (ALIEN_HEIGHT//2)


    def resetShip(self):
        """
        Resets the ship's position to the center.
        This should only be called when the game is paused.
        """
        if self._lives > 0:
            # Reset the ship's position to the center
            self._ship = Ship()


    def _attemptAlienFire(self, dt):
        self._alienFireTime += dt

        if self._alienFireTime >= self._nextFireTime:
            col = self._pickAlienCol()
            aln = self._findBottomAlien(col)
            if aln is not None:
                bolt = Bolt(x=aln.x, y=aln.y - (ALIEN_HEIGHT // 2), velocity=-BOLT_SPEED)
                self._bolts.append(bolt)

            self._alienFireTime = 0
            self._nextFireTime = random.randint(1, BOLT_RATE)


    def _findBottomAlien(self, column):
        # if self._aliens is None:
        #     return None
        if not self._aliens or column < 0 or column >= len(self._aliens[0]):
            return None

        for row_index in range(len(self._aliens)):
            alien = self._aliens[row_index][column]
            if alien is not None:
                return alien

        return None


    def _pickAlienCol(self):
        valid_columns = self.get_valid_columns()
        return random.choice(valid_columns) if valid_columns else None


    def is_valid_column(self, col_index):
        for row in self._aliens:
            if row[col_index] is not None:
                return True
        return False


    def get_valid_columns(self):
        num_columns = len(self._aliens[0])
        return [col for col in range(num_columns) if self.is_valid_column(col)]


    def _fireShip(self):
        if self._ship is not None and len(self._bolts) < MAX_BOLTS:
            bolt = Bolt(x=self._ship.x, y=self._ship.y + SHIP_HEIGHT/2, velocity=BOLT_SPEED)
            self._bolts.append(bolt)


    def _updateBolts(self):
        for bolt in self._bolts[:]:  # Iterate over a copy of the list
            bolt.y += bolt.getVelocity()

            # Check for collisions with the ship
            if self._ship and self._ship.collides(bolt):
                self._ship = None
                self._bolts.remove(bolt)
                self._lives -= 1
                continue

            # Check for collisions with aliens
            for row in self._aliens:
                for alien in row:
                    if alien and alien.collides(bolt):
                        # Set alien to None and remove the bolt
                        row[row.index(alien)] = None
                        self._bolts.remove(bolt)
                        break  # Exit the loop as the bolt is removed

            # Remove bolt if it's off-screen
            if bolt.y > GAME_HEIGHT or bolt.y < 0:
                self._bolts.remove(bolt)


    def _isPlayerBolt(self, bolt):
            assert isinstance(bolt, Bolt)
            if bolt._velocity > 0:
                return True


    def _walkAliens(self):
        """
        Moves the aliens horizontally, and when they reach the edge, marks them to move down in the next update.
        """
        if self._moveDown:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setY(alien.getY() - ALIEN_V_WALK)
            self._direction *= -1
            self._moveDown = False
            return

        edge_reached = False

        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.setX(alien.getX() + ALIEN_H_WALK * self._direction)

        if self._aliens:
            top_row = self._aliens[-1]
            #print(top_row)
            for alien in top_row:
                if alien is not None:
                    if self._direction > 0 and (GAME_WIDTH - (alien.getX() + ALIEN_WIDTH // 2)) < ALIEN_H_SEP:
                        edge_reached = True
                    elif self._direction < 0 and (alien.getX() - ALIEN_WIDTH // 2) < ALIEN_H_SEP:
                        edge_reached = True

        if edge_reached:
            self._moveDown = True



    def _moveShip(self, input):
        """
        Moves the ship based on player input.

        Parameter input: The user input, used to control the ship.
        Precondition: input is an instance of GInput
        """
        if input.is_key_down('left'):
            self._ship.x = max(0, self._ship.x - SHIP_MOVEMENT)
        elif input.is_key_down('right'):
            self._ship.x = min(GAME_WIDTH, self._ship.x + SHIP_MOVEMENT)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        This method draws all the models: aliens, ship, defensive line,
        and bolts.

        Parameter view: the game view, used in drawing
        Precondition: view is instance of GView; it is inherited from GameApp
        """
        #DRAW A BLOCK OF ALIENS
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                alien = self._aliens[row][col]
                if alien!=None:
                    alien.draw(view)
        #DRAW THE DEFENSIVE LINE
        self._dline.draw(view)
        #DRAW THE SHIP
        if self._ship is not None:
            self._ship.draw(view)
        #DRAW THE BOLTS
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
