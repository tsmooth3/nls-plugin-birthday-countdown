"""
Birthday board module implementation.
"""
import datetime
import json
import logging
import os

from PIL import Image
from boards.base_board import BoardBase
from data.data import Data
from renderer.matrix import Matrix

from . import __board_name__, __description__, __version__

debug = logging.getLogger("scoreboard")

# ---- Main class --------------------------------------------------------------
class Birthday(BoardBase):
    """
    The **Birthday Board** displays a countdown to a birthday.
    """

    def __init__(self, data: Data, matrix: Matrix, sleepEvent):
        super().__init__(data, matrix, sleepEvent)

        # Board metadata from package
        self.board_name = __board_name__
        self.board_version = __version__
        self.board_description = __description__
        
        # Get configuration values with defaults
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()

        # Resolve paths relative to the plugin directory
        self.board_dir = self._get_board_directory()

        # Access standard application config
        self.font = data.config.layout.font
        self.font.large = data.config.layout.font_large_2
        self.font.medium = data.config.layout.font_medium
        self.font.scroll = data.config.layout.font_xmas
        self.scroll_pos = self.matrix.width

        # custom variables
        self.days_to_next_birthday = 0
        self.age = 0

        # import config from config.json
        with open(f'{self.board_dir}/config.json', 'r') as f:
            self.config = json.load(f)
            self.birthdays = self.config["birthdays"]

    def _get_board_directory(self):
        """Get the absolute path to this board's directory."""
        import inspect
        board_file = inspect.getfile(self.__class__)
        return os.path.dirname(os.path.abspath(board_file))

    # -------- Rendering --------
    def render(self):
        for birthday in self.birthdays:
            self.who = birthday["who"]
            self.birthday = datetime.date.fromisoformat(birthday["birthday"])
            self.bday_image = Image.open(f'{self.board_dir}/{birthday["image"]}').resize((64,64)) 
            debug.info(f"{self.who} {self.birthday} Birthday countdown board launched")
            self.calc_days_to_birthday()
            #for testing purposes
            #self.days_to_birthday = 0

            debug.info(str(self.days_to_birthday) + " days")

            if self.days_to_birthday < 1:
                #today is Birthday
                self.birthday_today()
            else:
                #today is not birthday
                if self.days_to_birthday < birthday["days_before_birthday"]:
                    self.birthday_countdown()

    def calc_days_to_birthday(self):
        #get todays date
        today = datetime.date( datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        this_year_bday = datetime.date ( today.year, self.birthday.month, self.birthday.day)
        next_year_bday = datetime.date ( today.year + 1, self.birthday.month, self.birthday.day)
        if today > this_year_bday:
            thebday = next_year_bday
        else:
            thebday = this_year_bday

        self.age = round((thebday - self.birthday).days / 365.2425)
        #calculate days to bday
        self.days_to_birthday = (thebday - today).days
        self.days_old = (today - this_year_bday).days
        if self.days_to_birthday > 363:
            self.age = self.age - 1
    
    def birthday_today(self) :
        #  it's Party Time!
        duration = 15
        i = 0
        sleep_rate = .1
        debug.info("It's Birthday Time!")
        while not self.sleepEvent.is_set():
            self.matrix.clear()
            self.matrix.draw_image((0,0), self.bday_image)
            self.matrix.draw_text( (67,2), "Happy", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,17), "Birthday", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,32), f"{self.who}!", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,47), f"You're {self.age}", font=self.font.medium, fill=(150,150,150) ) 
            i += sleep_rate
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break

    def birthday_countdown(self) :
        self.matrix.clear()
        debug.info("Counting down to Birthday!")
        #check for three-digit countdown
        if self.days_to_birthday < 10:
            if self.days_to_birthday < 2:
                countdown_text = f"in {self.days_to_birthday} DAY"
            else:
                countdown_text = f"{self.days_to_birthday} DAYS"
        else:
            countdown_text = f"{self.days_to_birthday} DAYS"  

        duration = 7
        i = 0
        sleep_rate = .05

        while not self.sleepEvent.is_set():
            self.matrix.clear()
            self.matrix.draw_image((0,0), self.bday_image)
            self.matrix.draw_text( (67,2), countdown_text, font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,17), f"{self.who}", font=self.font.medium, fill=(150,150,150) ) 
            self.matrix.draw_text( (67,32), f"Turns {self.age}", font=self.font.medium, fill=(150,150,150) ) 
            i += sleep_rate
            self.matrix.render()
            self.sleepEvent.wait(sleep_rate)
            if(i > duration) : break