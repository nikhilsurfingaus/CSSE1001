import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
from model import TowerGame
from tower import SimpleTower, MissileTower,PulseTower,AbstractTower,AbstractObstacle,Missile
from enemy import SimpleEnemy,AbstractEnemy
from utilities import Stepper
from view import GameView
from level import AbstractLevel
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange
from high_score_manager import HighScoreManager
from advanced_view import TowerView
from utilities import Countdown, euclidean_distance, rotate_toward, angle_between, polar_to_rectangular, \
    rectangles_intersect
from utilities import rectangles_intersect, get_delta_through_centre
import json
from high_score_manager import HighScoreManager as highscores
import os
import math
import sys
from typing import Union
from core import Unit, Point2D, UnitManager
from enemy import AbstractEnemy
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange
from utilities import Countdown, euclidean_distance, rotate_toward, angle_between, polar_to_rectangular, \
    rectangles_intersect
from typing import Tuple, List

from core import UnitManager, GameData
from modules.ee import EventEmitter
from modules.matrix import get_adjacent_cells

from tower import AbstractTower
from enemy import AbstractEnemy
from path import Path
BACKGROUND_COLOUR = "#4a2f48"

__author__ = ""
__copyright__ = ""

class MadTingEnemy(SimpleEnemy):
    """Basic type of enemy"""
    name = "MadTingEnemy"
    colour = 'grey'  
    points = 5

    def __init__(self, grid_size=(.25, .25), grid_speed=4/60, health=125):
        super().__init__(grid_size, grid_speed, health)

    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        if type_ not in ("projectile","explosive"):     #Checks to see if the damage done is in list
            self.health -= damage
            if self.health < 0:
                self.health = 0

class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 20

    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave_n (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order 
        """
        enemies = []

        if wave == 1:
            # A hardcoded singleton list of (step, enemy) pairs

            enemies = [(10, SimpleEnemy())]
        elif wave == 2:
            # A hardcoded list of multiple (step, enemy) pairs

            enemies = [(10, SimpleEnemy()), (15, SimpleEnemy()), (30, SimpleEnemy()),
                       (40, MadTingEnemy())]
        elif 3 <= wave < 10:
            # List of (step, enemy) pairs spread across an interval of time (steps)

            steps = int(40 * (wave ** .5))  # The number of steps to spread the enemies across
            count = wave * 2  # The number of enemies to spread across the (time) steps

            for step in self.generate_intervals(steps, count):
                enemies.append((step, SimpleEnemy()))
                enemies.append((step+40, MadTingEnemy()))
                enemies.append((step+60, AdvancedEnemy()))              #Adding in the Advanced and custome
                                                                        #enemies to the waves

        elif wave == 10:
            # Generate sub waves
            sub_waves = [
                # (steps, number of enemies, enemy constructor, args, kwargs)
                (50, 10, SimpleEnemy, (), {}),  # 10 enemies over 50 steps
                (100, None, None, None, None),  # then nothing for 100 steps
                (50, 10, SimpleEnemy, (), {}),(50, 10, MadTingEnemy, (), {}),  
                (100, None, None, None, None),  
                (50, 10, MadTingEnemy, (), {}),(50, 10, AdvancedEnemy, (), {}),  
                (100, None, None, None, None),  
                (50, 10, AdvancedEnemy, (), {})  
            ]

            enemies = self.generate_sub_waves(sub_waves)

        else:  # 11 <= wave <= 20
            # Now it's going to get hectic

            sub_waves = [
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    SimpleEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    MadTingEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),(
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    AdvancedEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                )
                # diffrent enemies after the 11th wave
            ]
            enemies = self.generate_sub_waves(sub_waves)
            
        return enemies


class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None
    _paused = None
    _towers = {}

    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """

        self._master = master
        super().__init__(master, delay=delay)       #Inheriting  from the superclass

        self._game = game = TowerGame()
        self._highscores = highscores()         #Setting equatives in the init
        self.setup_menu()

        # create a game view and draw grid borders
        self._view = view = GameView(master, size=game.grid.cells,
                                     cell_size=game.grid.cell_size,
                                     bg='antique white')
        view.pack(side=tk.LEFT, expand=True)
        
        # Task 1.3 (Status Bar): instantiate status bar
        self._StatusBar = StatusBar(master,bg = "#4b3b4a")
        self._StatusBar.pack(side = tk.RIGHT,expand = True,fill = tk.BOTH)

        self.frame2 = tk.Frame(master,width = 400,bg = "#4b3b4a")   #Creating a frame to pack buttons
        self.frame2.pack(side = tk.BOTTOM,anchor = tk.S,
                         expand = True,fill = tk.BOTH)
        self.create_buttons()


        #Instantiating ShopTowerView
        towers = [SimpleTower,MissileTower,PulseTower,EnergyTower,AdvancedTower] #Towers avaliable
        print(towers)
        shop = tk.Frame(master,bg = "#4b3b4a")
        shop.pack(side = tk.TOP,expand = True,fill = tk.BOTH)

        # Create views for each tower & store to update if availability changes
        self._tower_views = []  #List of towers used
        for tower_class in towers:
            tower = tower_class(self._game.grid.cell_size // 2)
            tower_view = ShopTowerView(shop, tower,  # creating the ShopTowerView Object
                         click_command=lambda class_=tower_class: self.select_tower(class_))
            self._tower_views.append((tower, tower_view))


        
            
        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # Task 1.2 (Tower Placement): bind mouse events to canvas here
        view.bind('<Button-1>', self. _left_click)
        view.bind('<Motion>',self._move)
        view.bind('<Leave>',self._mouse_leave)
        view.bind('<Button-3>',self._sell_tower)

        # Level
        self._level = MyLevel()

        self.select_tower(SimpleTower)

        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()

            
    def setup_menu(self):
        """Sets up the application menu including the New Game, Exit and high
        scores.

        Parameters:
            master (tk.Tk): Area to place the Menubar into

        """
        # Task 1.4: construct file menu here
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)    
        filemenu = tk.Menu(menubar)
        
        #Creating the menu elements and their event commands
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self._new_game)
        filemenu.add_command(label="Exit", command=self._exit)
        filemenu.add_command(label="HighScores", command=self.high_score)
        
    def high_score(self):
        """Retrieves the top 10 highscores from a file and displays the position, name
        and score of a player.

                Parameters:
                    master (tk.Tk): To display the messagebox on screen
                    
        """
        hscore = self._highscores.get_entries(game = 'beta')
        highten = "Place\tName\t\tScore\n"          #The format of the highscore
        
        for num,element in enumerate(hscore):       #string concatnation
            highten += str(num+1) + ".\t" + str(element["name"]) +"\t" + str(element["score"]) + "\n"
            
        messagebox.showinfo("HighScores",highten)       #messagebox to display the highscore

    def create_buttons(self):
        """Creates the two buttons "Play/Pauses" and "Next Wave" button, and packs the two 
        buttons into a frame when called.
        
                Parameters:
                    master (tk.Tk): To manipulate the positioning of the GUI elements on the
                    frame.
        """
        self.pause_tog = 1              #A binary value to hold state of buttons

        #create and pack buttons
        self._next_wave = tk.Button(self.frame2,text = "Next Wave"
                                    ,command = self.wave_button,
                                    state = tk.NORMAL,bg = "white")
        
        self._next_wave.pack(side = tk.LEFT, anchor = tk.S,
                             pady = 0,padx = 0,expand = True)
        
        self._play = tk.Button(self.frame2,text = "Play",command = self.flip_pause,
                                state = tk.NORMAL,bg = "white")
        
        self._play.pack(side = tk.LEFT,anchor = tk.S,ipadx = 18,expand = True)
        
    def flip_pause(self):
        """This method checks the state of the play/pause button and flips the state to the opposite
        state after the state of the button has been selected as well as changing the state of the
        buttons text.

            Parameters:
                    pause_tog (Int):A single binary value that the pause/play button holds.
                    _play(Button): The play/pause button.
                    _next_wave(Button): The next wave button

        """
        #Check the state of the puase and flip if necessary
        print(self.pause_tog)
        if self.pause_tog  == 0:
            self.pause_tog = 1
            self._toggle_paused()           #calling the pause function
            self._play.config(text = "Play")        #change the name back when flipped
        else:
            self.pause_tog = 0
            self._play.config(text = "Pause")
            self._toggle_paused()
            
    def wave_button(self):
        """Starts the next wave when the button is pressed an checks in to see if the state
        of the button is unchanged

                Parameters:
                    _next_wave(Button): Button to intiate the next wave
                    next_wave(Function): Call to a method that intiates the next wave.

        """
        pressed = False
        self.next_wave()        #calling the next wave
        
        if self._next_wave["state"] is tk.NORMAL:
            print("working")                            #a check in the console to check button state
        print(self._next_wave["state"])
        
        

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        # Task 1.5 (Play Controls): Reconfigure the pause button here

        if paused:
            self.pause()            #Calling functions that pause or play the game
        else:
            self.start()
            
        print(self._paused,paused )
        self._paused = paused

    def _setup_game(self):
        """Sets up the game intially and whenever the game is restarted

                Parameters:
                    set_wave(Method): Method that changes the wave count on the label
                    set_score(Method): Method that changes the score value on the label
                    set_gold(Method): Method that changes the coin count on the label
                    set_lives_remaining(Method): Method that changes the life count on the label


        """
        #Intial variable values
        self._wave = 0
        self._score = 0
        self._coins = 500
        self._lives = 20

        self._won = False

        # Task 1.3 (Status Bar): Update status here
        self._StatusBar.set_wave(self._wave)
        self._StatusBar.set_score(self._score)
        self._StatusBar.set_gold(self._coins)
        self._StatusBar.set_lives_remaining(self._lives)

        # Task 1.5 (Play Controls): Re-enable the play controls here (if they were ever disabledself._game.reset()
        self._next_wave["state"] = tk.NORMAL
        self._play["state"] = tk.NORMAL
        self._game.reset()
        # Auto-start the first wave
        self.next_wave()
        self._toggle_paused(paused=True)
        self.pause_tog = 1 
    # Task 1.4 (File Menu): Complete menu item handlers here (including docstrings!)
    def _new_game(self):
        """Sets up a new game, by clearing the canvas and reseting all the variable values, the towers 
        and waves are also reset for the user to begin playing again

                    Parameters:
                        _view(GameView): The grided model as a cavas for the game.
                        _play(Button): The Pause button is changed to play

        """
        #values that need to be reset for the new game
        self._setup_game()
        self.refresh_view()
        self._view.delete("tower")
        self._view.delete("enemy")
        self._view.delete("wave")
        self._play.config(text = "Play")

        
    def _exit(self):
        """A method to exit the game when the user is finished playing, displays a messagebox
        warning the user of their decision to leave, as well as the outcome of the game which
        integrates their score and their won/loss game status

                Parameters:
                        _won(Boolean): The true or false state of whether the game is one.
                        _play(Button): The Pause button is changed to play
                        master (tk.Tk): To allow the display of the messagebox
                        _score(Int):The score ahcieved by the user at the end of their game.


        """
        result = messagebox.askquestion("QUIT GAME", "Are You Sure?", icon='warning') #prompt to the user
        if result == 'yes':
            print("Game Quit Procedure")
            if self._won is True:
                messagebox.showinfo("Win","Score is " + str(self._score))       #display the end result in msgbox
                exit()
            else:
                messagebox.showinfo("Lose","Score is " + str(self._score))
                exit()
        else:
            pass
    

    def refresh_view(self):
        """Refreshes the game view

            Parametres:
                _step_number(Int): The intergeric value of the step count
                _game.enemies(AbstractEnemy): The list of enemies in the game
                _tower_views(List): A list of tuples containing the tower object and
                ShopTowerView object.
                _coins(Int): The value of the amount of coins the user has.


        """
        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)
        self._view.draw_towers(self._game.towers)
        self._view.draw_obstacles(self._game.obstacles)

        #Checking each tower is it is able to be purchaed or not from the shop
        for tower, tower_view in self._tower_views:
            if tower.get_value() <= self._coins:
                tower_view.set_available(True)
            else:
                tower_view.set_available(False)

    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

        Returns:
            (bool) True if the game is still running
        """
        self._game.step()
        self.refresh_view()

        return not self._won

    # Task 1.2 (Tower Placement): Complete event handlers here (including docstrings!)
    # Event handlers: _move, _mouse_leave, _left_click
    
    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        if self._current_tower.get_value() > self._coins:       #comparsion of coins
            return

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position

        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]

        # Task 1.2 (Tower placement): Draw the tower preview here
        self._view.draw_preview(self._current_tower,legal)
        self._view.draw_path(path)
        
    def _mouse_leave(self, event):
        """An event to delete the preview of the path, range and the shadow of the
        tower when the mouse leaves the canvas

                    Parametres:
                        event (tk.Event): Tkinter mouse leave event
                        master (tk.Tk): To delete the display of the shadow,path and
                        range
                        event (tk.Event): Tkinter mouse event

        """
        # Task 1.2 (Tower placement): Delete the preview
        # Hint: Relevant canvas items are tagged with: 'path', 'range', 'shadow'
        #       See tk.Canvas.delete (delete all with tag)
        
        self._view.delete("path")
        self._view.delete("range")      #deletes all relevant tags
        self._view.delete("shadow")
        
    def _sell_tower(self,event):
        """An event to delete the selling of a tower when the mouse right clicks a tower.

                    Parametres:
                        event (tk.Event): Tkinter mouse right click event
                        master (tk.Tk): To delete the display of the tower on the canvas
                        _towers(dictionary): The dictionary of towers and cell positions
                        _coins(Int): Value of the coins held by the user
                        event (tk.Event): Tkinter mouse event

                        
        """
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)
        
        if cell_position in self._towers:
            tower_type = self._towers.get(cell_position)
            print(tower_type)
            self._game.remove(cell_position)                    #Checks if a tower is their ans refunds 80%
            self._coins = int(self._coins + 0.8*tower_type.get_value())                         #for a sale
        else:
            print("No Tower Nikhil")        #consoles output to aid developer
            
    def _left_click(self, event):
        """A click event that deals with the user left clicking to place a tower on the grid,
        accounts for the legalities of placing a tower on the grid.

                    Parametres:
                        _current_tower(Tower): A tower object used by the GameView
                        _coins(Int): Value of the coins held by the user
                        _towers(dictionary): The dictionary of towers and cell positions
                        refresh_view(Method): Called to update the display of the towers
                        event (tk.Event): Tkinter mouse event
        """
        # retrieve position to place tower
        if self._current_tower is None:
            return

        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)
        if self._current_tower.get_value() <= self._coins:          #check to see if enough coins
            if self._game.place(cell_position, tower_type=self._current_tower.__class__):
                # Task 1.2 (Tower Placement): Attempt to place the tower being previewed
                self._game.attempt_placement(cell_position)
                self._towers[cell_position] = self._current_tower
                self.refresh_view()
                self._coins = self._coins - self._current_tower.get_value()

    def next_wave(self):
        """Sends the next wave of enemies against the player

                    Parametres:
                        _wave(Int): The number of the current wave.
                        _level(Int): The number of the current level.
                        _next_wave(Button): Changes the state of the button to
                        deactivated.


        """
        if self._wave == self._level.get_max_wave():
            return

        self._wave += 1             #increment the wave

        # Task 1.3 (Status Bar): Update the current wave display here
        self._StatusBar.set_wave(self._wave)

        # Task 1.5 (Play Controls): Disable the add wave button here (if this is the last wave)
        if self._wave == 20:
            self._next_wave["state"] = tk.DISABLED      #disabling button

        # Generate wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)      #set the current toeer

    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
            _coins(Int): Value of the coins held by the user
            set_gold(Method): Method that changes the score value on the label

        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)

        # Task 1.3 (Status Bar): Update coins & score displays here
        self._StatusBar.set_score(self._score)
        self._StatusBar.set_gold(self._coins)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
            _lives(Int): The number of lives the user has
        """
        #updating the lives on the label
        self._lives -= len(enemies)
        if self._lives < 0:
            self._lives = 0

        # Task 1.3 (Status Bar): Update lives display here
        self._StatusBar.set_lives_remaining(self._lives)

        # Handle game over
        if self._lives == 0:
            self._handle_game_over(won=False)
            

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)

                Parametres:
                    _level(Int): Number of the level curretly on

        """
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)
            return True

        # Task 1.5 (Play Controls): remove this line

    def _handle_game_over(self, won=False):
        """Handles game over, and adds score to the highscores, if the score
        qualifies for the highscore criteria.
        
        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
            _play(Button): The play/pause button.
            _next_wave(Button): The next wave button
            master (tk.Tk): To display the highscores messagebox and askstring.
            _score(Int):The score ahcieved by the user at the end of their game.


        """
        self._won = won
        self.stop()
        self._next_wave["state"] = tk.DISABLED
        self._play["state"] = tk.DISABLED           #update the button states
        # Task 1.4 (Dialogs): show game over dialog here
        if self._won is True:
            messagebox.showinfo("WIN","Score is " + str(self._score))   #display score
            if self._highscores.does_score_qualify(self._score) is True:
                name = askstring("New HighScore", "Your Name is")       #prompt for name
                if len(name) < 19:
                    space = 19 - len(name)          #fit name within the coloumn
                    name = name + str(space*" ")
                elif name == None:
                    name = "No Name"            #error trapping method
                self._highscores.add_entry(name = name,score = self._score, game = 'beta')
                self._highscores.save()     #save the file
                hscore = self._highscores.get_entries(game = 'beta')
                highten = "Place\tName\t                Score\n"    #create the row
                for num,element in enumerate(hscore):
                    highten += str(num+1) + ".\t" + str(element["name"]) +"\t" + str(element["score"]) + "\n" #add the row
                #print("HighScores",highten)
                messagebox.showinfo("HighScores",highten)   #display the highscore
        else:
            messagebox.showinfo("LOSE","Score is " + str(self._score)) #display score
            if self._highscores.does_score_qualify(self._score) is True: #check is score qualified
                name = askstring("New HighScore", "Your Name is") #prompt for name
                if len(name) < 19:
                    space = 19 - len(name)          #fit name within the coloumn
                    name = name + str(space*" ")
                elif name == None:
                    name = "No Name"            #error trapping method
                self._highscores.add_entry(name = name,score = self._score, game = 'beta')
                self._highscores.save()             #save the file
                hscore = self._highscores.get_entries(game = 'beta')
                highten = "Place\tName\t                Score\n"    #create the row
                for num,element in enumerate(hscore):
                    highten += str(num+1) + ".\t" + str(element["name"]) +"\t" + str(element["score"]) + "\n" #add the row
                #print("HighScores",highten)
                messagebox.showinfo("HighScores",highten)   #display the highscore
 

            

class StatusBar(tk.Frame):
    """A simple class that allows the combination of widgets including the score,
    wave, lives and coins to have a GUI on the program

            Parametres:
                master (tk.Tk): To create and pack the labels and frame onto the game view.
    """
    def __init__(self,master,**kwargs):
        """The intialisation of the varibles to be used throughout the statusbar class

                Parametres:
                    master (tk.Tk): To create and pack the labels and frame onto the game view.
                    **kwargs(funct): Pass a variable number of arguments                    


        """
        #intialise the variables
        super().__init__(master,**kwargs)
        #create a main frame
        self.frame1 = tk.Frame(master,bg = 'white',height = 300)
        self.frame1.pack(expand = True,fill = tk.BOTH,side = tk.TOP)

        #create the labels to display information
        self._wave = tk.Label(self.frame1,text = "wave",
                              font=("Helvetica", 10),bg = 'white')
        self._wave.pack(side = tk.TOP)
        
        self._score = tk.Label(self.frame1,text = "score",bg = 'white')
        self._score.pack(side = tk.TOP)
        
        coins = tk.PhotoImage(file="coins.png")     #adding the image to the statusbar
        w = tk.Label(self.frame1,image=coins,bg = 'white')
        w.image = coins 
        w.pack(side = tk.LEFT,anchor = tk.N,pady = 0,padx = 0,
               expand = True,fill = tk.X)
        
        self._gold = tk.Label(self.frame1,text = "gold",bg = 'white')
        self._gold.pack(side = tk.LEFT,anchor = tk.N,pady = 10)
        
        hearts = tk.PhotoImage(file="heart.gif")
        x = tk.Label(self.frame1,image=hearts,bg = 'white')
        x.image = hearts 
        x.pack(side = tk.LEFT,anchor = tk.N,pady = 0,expand = True,fill = tk.X)
        
        self._lives_remaining = tk.Label(self.frame1,text = "Lives Remaining",bg = 'white')
        self._lives_remaining.pack(side = tk.LEFT, anchor = tk.N,pady = 10)
        
    def set_wave(self,wave):
        """Changes the text of the wave label to match the current wave

                    Parametres:
                        wave(Int):The wave number currently completing
                        _wave(Label): A label that holds the value of the wave number

        """
        self._wave.config(text = "Wave: "+str(wave)+"/20")  #update the wave
        
    def set_score(self,score):
        """Changes the text of the score label to match the current score

                    Parametres:
                        score(Int):The score number currently held by the player
                        _score(Label): A label that holds the value of the score value

        """
        self._score.config(text = "Score "+str(score))  #update the score
        
    def set_gold(self,gold):
        """Changes the text of the coin label to match the current coin value.

                    Parametres:
                        gold(Int):The coins number currently held by the player.
                        _gold(Label): A label that holds the value of the coin number

        """
        self._gold.config(text = str(gold)+" Coins")        #update the coins value
        
    def set_lives_remaining(self,lives_remaining):
        """Changes the text of the lives_remaining label to match the current lives number.

                    Parametres:
                        lives_remaining(Int):The lives remaining number currently held.
                        _lives_remaining(Label): A label that holds the value of the lives number

        """
        self._lives_remaining.config(text = str(lives_remaining) +" Lives") #update the lives value of the player

class EnergyTower(SimpleTower):
    """A simple class that creates the energy tower object which can kill the custom enemy

                Parametres:
                    SimpleTower(AbstractTower): Inherits from abstract tower, to create a tower object
                    that shoots and deals damage to enemies.
    """
    #intialise the varaibles
    name = 'Energy Tower'
    
    range = CircularRange(2)
    cool_down_steps = 5
    base_cost = 150
    level_cost = 50


    colour = 'orange'

    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=5, level: int = 1):
        super().__init__(cell_size, grid_size, rotation, base_damage, level)
        """Calls the superclass parametres for use in the energytower class

                    Parametres:
                        cell_size(Float):The size the tower holds on the grid
                        grid_size(Float):The grid size the tower holds on the canvas
                        rotation(Float): The amount the tower can rotate
                        base_damage(Int): The towers damage dealt
                        level(Int): The level value of the towers cost


        """
    def step(self, data):
        """Rotates toward 'target' and attacks if possible

                Parametres:
                    data(Enemy): Holds the enemy object iformation used for the energy tower class.

        """
        self.cool_down.step()

        target = self.get_unit_in_range(data.enemies)   #set the target for the tower

        "only attack MadTingEnemy enemies"
        if target is None:      #selective targeting the custom enemy
            return
     
        angle = angle_between(self.position, target.position)
        partial_angle = rotate_toward(self.rotation, angle, self.rotation_threshold)
        self.rotation = partial_angle
        
        if partial_angle == angle:
            target.damage(self.get_damage(), 'energy')  #the type of damage produced
            
class ShopTowerView(tk.Frame):
    """A simple object used to hold towers and their values allowing the user
    to interact and buy and sell towers from the shop

            Parametres:
                master (tk.Tk): To create and pack the labels and frame onto the game view.
            
    """
    def __init__(self,frame,tower,click_command,*args,**kwargs):
        """The intialisation of the variables used throughout the shop for purchasing and
        selling towers.

                Parametres:
                    frame(tk.Tk): Used to bind all the widegets to in the shop.
                    click_command(Method): A method used to create the ShopTowerView
                    objects when called.
                    *args(Funct):Pass a variable number of arguments to a function
                    **kwargs(Funct):Pass a variable number of arguments to a function
        """
        #intialse the variables
        self._frame = frame
        self._click_command = click_command
        self._tower = tower
        #create a canvas to pack the towers to
        w = tk.Canvas(self._frame,width = 30,height = 30,bg = '#4b3b4a',
                      highlightbackground  = "#4b3b4a", highlightthickness = 1)
        w.pack(expand = True, side = tk.TOP, fill = tk.X, anchor = tk.W)
        
        tower.position = (tower.cell_size // 2, tower.cell_size // 2)  # Position in centre
        tower.rotation = 3 * math.pi / 2  # Point up
        TowerView.draw(w, self._tower)
        #create the labels to display information about the tower.
        self.label = tk.Label(w,
                              text = self._tower.name,bg = "#4b3b4a",fg="white",
                              font=("Helvetica", 10,"bold"))
        self.label.pack(expand = True, fill = tk.Y,side = tk.TOP,anchor = tk.E)
        
        self.label2 = tk.Label(w,text = str(self._tower.get_value())+" Coins",bg= "#4b3b4a",
                               fg="white",font=("Helvetica", 10,"bold"))
        self.label2.pack(expand = True, padx = 15,fill = tk.Y,side = tk.TOP,anchor = tk.E)

       
        w.bind('<Button-1>', self.select_tower) #event button
        
    def pack(self):
        """A method that packs the label when the label is passed through

                Parametres:
                    label(Label): The label passed through that needs to be packed
                    onto the frame.

        """
        self.label.pack(expand = True, anchor = tk.N) #method to pack the label 
        
    def select_tower(self, event):
        """A click command that event that occurs when the tower is selected from the shop

                Parametres:
                    event (tk.Event): Tkinter mouse event for a click that calls a function

        """
        self._click_command()       #call the lambda function
        
    def set_available(self, available = True):
        """Changes and updates the foreground of the coin label to display whether the
        tower is affordable or not.

                Parametres:
                    availiable(Boolean): A true or false value that holds wether the tower
                    is affordable is or not.
                    label2(Label): The label which holds the coin value

        """
        if available is True:
            self.label2.config(fg="green")      #change the colour of the label
        else:
            self.label2.config(fg="red")

class AdvancedEnemy(SimpleEnemy):
    """Advanced type of the simple enemy that has high speeds, low health and deals damage
    to the Ice Tower

            Parametres:
                SimpleEnemy(AbstractEnemy):Inherits from the simple enemy class, to create an
                advanced enemy.

    """
    name = "Advanced Enemy"
    colour = 'yellow'  

    points = 5

    def __init__(self, grid_size=(.1, .1), grid_speed=9/60, health=10):
        super().__init__(grid_size, grid_speed, health)
        """An inheritance from the superclass that inherits characteristics of the abstract enemy

                Parametres:
                    grid_size(Float): The size the enemey takes on the grid
                    grid_speed(Float): The speed of the enemy on the grid
                    health(Int): The health the enemy has.

        """

    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        self.health -= damage
        if self.health < 0:         #subtract the damage done
            self.health = 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas
    
class Advance(AbstractObstacle):
    """An adavanced projectile fired from an Advanced Tower"""
    name = "Advance"
    colour = 'blue'  # colour

    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, position, cell_size, target: AbstractEnemy, size=.8,
                 rotation: Union[int, float] = 0, grid_speed=.1, damage=25):
        super().__init__(position, (size, 0), cell_size, grid_speed=grid_speed, rotation=rotation, damage=damage)
        """Inherits from the superclass to intiaslise variables

                Parametres:
                    position(Int): The grid position of the bullet
                    size(Float): The cell size of the bullet
                    grid_speed(Float): The speed of the bullet
                    rotation(Float): How much the bullet can rotate
                    damage(Int): The amount of damage the bullet deals.
        """
        self.target = target

    def step(self, units):
        """Performs a time step for this missile
        
        Moves towards target and damages if collision occurs
        If target is dead, this missile expires
        
        Parameters:
            units.enemies (UnitManager): The unit manager to select targets from
            
        Return:
            (persist, new_obstacles) pair, where:
                - persist (bool): True if the obstacle should persist in the game (else will be removed)
                - new_obstacles (list[AbstractObstacle]): A list of new obstacles to add to the game, or None
        """
        if self.target.is_dead():
            return False, None

        # move toward the target
        radius = euclidean_distance(self.position, self.target.position)

        if radius <= self.speed:
            self.target.damage(self.damage, 'fire')
            return False, None

        # Rotate toward target and move
        angle = angle_between(self.position, self.target.position)
        self.rotation = rotate_toward(self.rotation, angle, self.rotation_threshold)

        dx, dy = polar_to_rectangular(self.speed, self.rotation)
        x, y = self.position
        self.position = x + dx, y + dy

        return True, None

class AdvancedTower(MissileTower):
    """A tower that fires Ice bullets that track a all enemies

            Parametres:
                MissileTower(AbsractTower): Inherits the characteristics of the Missile
                Tower.
    """
    #initalise the towers characteritics
    name = 'Ice Tower'
    colour = 'deep sky blue'

    cool_down_steps = 10

    base_cost = 200
    level_cost = 60

    range = CircularRange(1.6)

    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, cell_size: int, grid_size=(0.9, 0.9), rotation=math.pi * .25, base_damage=100, level: int = 1):
        super().__init__(cell_size, grid_size=grid_size, rotation=rotation, base_damage=base_damage, level=level)
        """Inherits from the superclass variables.

                Parametres:
                    cell_size(Int): The cell size of the tower
                    size(Float): The cell size of the tower
                    base_damage(int): The health of the tower
                    rotation(Float): How much the tower can rotate
                    level(Int): The level that influcences the cost

        """
        self._target: AbstractEnemy = None        
            
            
    def _get_target(self, units) -> Union[AbstractEnemy, None]:
        """Returns previous target, else selects new one if previous is invalid
        
        Invalid target is one of:
            - dead
            - out-of-range
        
        Return:
            AbstractEnemy: Returns previous target, unless it is non-existent or invalid (see above),
                           Otherwise, selects & returns new target if a valid one can be found,
                           Otherwise, returns None
        """
        if self._target is None \
                or self._target.is_dead() \
                or not self.is_position_in_range(self._target.position):
            self._target = self.get_unit_in_range(units)

        return self._target

    def step(self, units):
        """Rotates toward 'target' and fires missile if possible

                Parametres:
                    units(AbstractEnemy): Holds values about the enemies

        """
        self.cool_down.step()

        target = self._get_target(units.enemies)
        if target is None:
            return None
        elif target.name ==  "Advanced Enemy":      #deal damage from the advanced enemy
            self.base_damage -= 10
            print(self.base_damage)

       
        if self.base_damage <= 0:
            Advance.damage = 0      #The Ice Tower no longer produces any Damage, contiues to create freeze enemies
            self.colour = "grey"
            
            
        target.grid_speed = 1/60
        target.colour = "light sky blue"        #change the speed and colour of near enemies ie freeze
            

        
            

        # Rotate toward target
        angle = angle_between(self.position, target.position)
        partial_angle = rotate_toward(self.rotation, angle, self.rotation_threshold)

        self.rotation = partial_angle

        if angle != partial_angle or not self.cool_down.is_done():
            return None

        self.cool_down.start()

        # Spawn missile on tower
        advance = Advance(self.position, self.cell_size, target, rotation=self.rotation,
                          damage=self.get_damage(), grid_speed=.4)

        # Move missile to outer edge of tower
        radius = self.grid_size[0] / 2
        delta = polar_to_rectangular(self.cell_size * radius, partial_angle)
        advance.move_by(delta)

        return [advance]
            


def main() :
    """The main function that combines all the elements from the classes, and creates an exe
    appliction GUI program

            Parametres:
                TowerGameApp(Class): The main class for combining all the objects
    """
    root = tk.Tk()
    app = TowerGameApp(root)        #create the display for the game
    root.title("Towers")
    root.mainloop()



if __name__ == "__main__" :
    main()
    

