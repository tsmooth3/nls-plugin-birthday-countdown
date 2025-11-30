# Birthday Board

A **Birthday Countdown Board** for the [NHL LED Scoreboard](https://github.com/falkyre/nhl-led-scoreboard) that displays countdowns to birthdays and celebrates on the special day.

This board shows:
- Days remaining until a birthday (when within the configured threshold)
- Birthday person's name and age they'll turn
- Special "Happy Birthday" display on the actual birthday
- Custom birthday images for each person

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Display Modes](#display-modes)
- [How It Works](#how-it-works)

---

## Features

- Real-time countdown to birthdays (supports multiple birthdays)
- Displays days remaining until birthday
- Shows the age the person will turn
- Custom birthday image display for each person
- Special birthday day celebration mode with "Happy Birthday" message
- Automatically handles year rollover (counts down to next birthday if current date is after birthday)
- Configurable countdown start threshold per birthday

---

## Installation

1. Use the NHL Led Scoreboard's plugin manager python script to install:

   ```bash
   python plugins.py add https://github.com/tsmooth3/nls-plugin-birthday-countdown.git
   ```

2. Add `birthday_board` to your NHL-LED-Scoreboard's main configuration:

   ```bash
   nano config/config.json
   ```

   For example, to add it to the off day rotation:

   ```json
   "states": {
       "off_day": [
           "season_countdown",
           "birthday_board",
           "team_summary",
           "scoreticker",
           "clock"
       ]
   }
   ```

   **Note:** You must restart the scoreboard for changes to take effect.

---

## Configuration

The Birthday board requires a `config.json` file in the plugin directory. Copy `config.sample.json` to `config.json` and customize it:

```json
{
    "enabled": true,
    "birthdays": [
        {
            "who": "Doug",
            "birthday": "2005-05-03",
            "image": "assets/images/bday0503.jpg",
            "days_before_birthday": 1
        },
        {
            "who": "Judy",
            "birthday": "2000-08-03",
            "image": "assets/images/bday0803.png",
            "days_before_birthday": 102
        }
    ]
}
```

### Configuration Options

- **enabled** (boolean): Enable or disable the birthday board
- **birthdays** (array): List of birthdays to track
  - **who** (string): Name of the person
  - **birthday** (string): Birthday date in ISO format (YYYY-MM-DD)
  - **image** (string): Path to the birthday image file (relative to plugin directory)
  - **days_before_birthday** (integer): Number of days before the birthday to start showing the countdown

### Image Requirements

- Birthday images should be placed in `assets/images/` directory
- Images are automatically resized to 64x64 pixels
- Supported formats: JPG, PNG, and other formats supported by PIL

---

## Display Modes

The board has two main display modes:

### Countdown Mode

When there are 1 or more days until a birthday (within the configured `days_before_birthday` threshold), the board displays:
- Birthday image (64x64 pixels) on the left side
- Days remaining (e.g., "5 DAYS" or "in 1 DAY")
- Person's name
- "Turns [age]" text showing the age they'll turn
- Display duration: 7 seconds

The board cycles through all configured birthdays that are within their countdown threshold.

### Birthday Day Mode

On the actual birthday (when days remaining equals 0), the board displays:
- Birthday image (64x64 pixels) on the left side
- "Happy" text
- "Birthday" text
- "[Name]!" text
- "You're [age]" text showing current age
- Display duration: 15 seconds

---

## How It Works

1. The board reads birthday configurations from `config.json`
2. For each birthday, it calculates the days remaining until the next occurrence
3. It automatically handles year rollover - if the current date is after this year's birthday, it counts down to next year's birthday
4. The board calculates the person's age based on their birth date
5. When `days_to_birthday < days_before_birthday`, the countdown display is shown
6. On the birthday itself (when days remaining equals 0), the board switches to celebration mode
7. The board uses the following fonts from your scoreboard configuration:
   - `font_large_2` for large text (if used)
   - `font_medium` for all text displays
   - `font_xmas` for scrolling text (available but not currently used)

The board requires image assets for each birthday:
- Images should be placed in `assets/images/` directory
- Image paths are specified in the `config.json` file
- Images are automatically resized to 64x64 pixels for display
