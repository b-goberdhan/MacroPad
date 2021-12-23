# MacroPad

## How to create a macro

1. Create a .json file. example: my-macro.json
2. Copy and paste this template into the file: 
    ```json
    {
        "name": "name-of-macro",
        "macros": {
            "key1": {

            },
            "key2": {

            },
            "key3": {

            },
            "key4": {

            },
            "key5": {

            },
            "key6": {

            },
            "key7": {

            },
            "key8": {

            },
            "key9": {

            },
            "key10": {

            },
            "key11": {

            },
            "key12": {

            }
        }
    }
    ```
3. Now that you have your basic template you just have to define the macro for a given key:
    ```json 
    "key1": {
        "name": "",
        "color": "",
        "command": [],
        "sound": "",
        "tone": -1
    }
    ```
    - `name`: the name for the given key
    - `color`: the illuminated color of the key
    - `command`: the command that is activated when the key is pressed
    - `sound`: a sound file (mp3) that is played when the key is pressed.
    - `tone`: a tone that is played when key is pressed.

## Defining a command

There are 3 types of commands that you can issue:

- `Consumer Control`: These are commands that control things like volume, brightness, pause, play etc.
- `Key code`: These are commands that will trigger various key presses on a keyboard. 
- `Basic Text`: This will allow you to print out a bunch of text on a key press.

These 3 types of commands can be used together for maximum fun.

### Example Consumer Control command

Consumer Control commands must be wrapped within square brackets ([])
```json
    "key1": {
        "name": "my-key",
        "command": [
            ["VOLUME_INCREMENT"], 
            ["BRIGHTNESS_DECREMENT"]
        ]
    }
```
The above command will increase the volume then increase the brightness when `key1` is pressed.


<details>
    <summary>Here is a list of all the Consumer Control Commands</summary>

    RECORD
    FAST_FORWARD
    REWIND
    SCAN_NEXT_TRACK
    SCAN_PREVIOUS_TRACK
    STOP
    EJECT
    PLAY_PAUSE
    MUTE
    VOLUME_DECREMENT
    VOLUME_INCREMENT
    BRIGHTNESS_DECREMENT
    BRIGHTNESS_INCREMENT
</details>


### Example Key Code command
```json
    "key1": {
        "name": "my-key",
        "command": ["CONTROL", "ALT", "DELETE"]
    },
```
The above command will cause windows to prompt you to lock, switch user, sign out, change a password or open task mananger.


<details>
    <summary>Here is a list of all the Key Code Commands</summary>
    

    A
    """``a`` and ``A``"""
    B
    """``b`` and ``B``"""
    C
    """``c`` and ``C``"""
    D
    """``d`` and ``D``"""
    E
    """``e`` and ``E``"""
    F
    """``f`` and ``F``"""
    G
    """``g`` and ``G``"""
    H
    """``h`` and ``H``"""
    I
    """``i`` and ``I``"""
    J
    """``j`` and ``J``"""
    K
    """``k`` and ``K``"""
    L
    """``l`` and ``L``"""
    M
    """``m`` and ``M``"""
    N
    """``n`` and ``N``"""
    O
    """``o`` and ``O``"""
    P
    """``p`` and ``P``"""
    Q
    """``q`` and ``Q``"""
    R
    """``r`` and ``R``"""
    S
    """``s`` and ``S``"""
    T
    """``t`` and ``T``"""
    U
    """``u`` and ``U``"""
    V
    """``v`` and ``V``"""
    W
    """``w`` and ``W``"""
    X
    """``x`` and ``X``"""
    Y
    """``y`` and ``Y``"""
    Z
    """``z`` and ``Z``"""

    ONE
    """``1`` and ``!``"""
    TWO
    """``2`` and ``@``"""
    THREE
    """``3`` and ``#``"""
    FOUR
    """``4`` and ``$``"""
    FIVE
    """``5`` and ``%``"""
    SIX
    """``6`` and ``^``"""
    SEVEN
    """``7`` and ``&``"""
    EIGHT
    """``8`` and ``*``"""
    NINE
    """``9`` and ``(``"""
    ZERO
    """``0`` and ``)``"""
    ENTER
    """Enter (Return)"""
    RETURNR
    """Alias for ``ENTER``"""
    ESCAPE
    """Escape"""
    BACKSPACE
    """Delete backward (Backspace)"""
    TAB
    """Tab and Backtab"""
    SPACEBAR
    """Spacebar"""
    SPACEEBAR
    """Alias for SPACEBAR"""
    MINUS
    """``-` and ``_``"""
    EQUALS
    """` ``+``"""
    LEFT_BRACKET
    """``[`` and ``{``"""
    RIGHT_BRACKET
    """``]`` and ``}``"""
    BACKSLASH
    r"""``\`` and ``|``"""
    POUND
    """``#`` and ``~`` (Non-US keyboard)"""
    SEMICOLON
    """``;`` and ``:``"""
    QUOTE
    """``'`` and ``"``"""
    GRAVE_ACCENT
    r""":literal:`\`` and ``~``"""
    COMMA
    """``,`` and ``<``"""
    PERIOD
    """``.`` and ``>``"""
    FORWARD_SLASH
    """``/`` and ``?``"""

    CAPS_LOCK
    """Caps Lock"""

    F1
    """Function key F1"""
    F2
    """Function key F2"""
    F3
    """Function key F3"""
    F4
    """Function key F4"""
    F5
    """Function key F5"""
    F6
    """Function key F6"""
    F7
    """Function key F7"""
    F8
    """Function key F8"""
    F9
    """Function key F9"""
    F10
    """Function key F10"""
    F11
    """Function key F11"""
    F12
    """Function key F12"""

    PRINT_SCREEN
    """Print Screen (SysRq)"""
    SCROLL_LOCK
    """Scroll Lock"""
    PAUSE
    """Pause (Break)"""

    INSERT
    """Insert"""
    HOME
    """Home (often moves to beginning of line)"""
    PAGE_UP
    """Go back one page"""
    DELETE
    """Delete forward"""
    END
    """End (often moves to end of line)"""
    PAGE_DOWN
    """Go forward one page"""

    RIGHT_ARROW
    """Move the cursor right"""
    LEFT_ARROW
    """Move the cursor left"""
    DOWN_ARROW
    """Move the cursor down"""
    UP_ARROW
    """Move the cursor up"""

    KEYPAD_NUMLOCK
    """Num Lock (Clear on Mac)"""
    KEYPAD_FORWARD_SLASH
    """Keypad ``/``"""
    KEYPAD_ASTERISK
    """Keypad ``*``"""
    KEYPAD_MINUS
    """Keyapd ``-``"""
    KEYPAD_PLUS
    """Keypad ``+``"""
    KEYPAD_ENTER
    """Keypad Enter"""
    KEYPAD_ONE
    """Keypad ``1`` and End"""
    KEYPAD_TWO
    """Keypad ``2`` and Down Arrow"""
    KEYPAD_THREE
    """Keypad ``3`` and PgDn"""
    KEYPAD_FOUR
    """Keypad ``4`` and Left Arrow"""
    KEYPAD_FIVE
    """Keypad ``5``"""
    KEYPAD_SIX
    """Keypad ``6`` and Right Arrow"""
    KEYPAD_SEVEN
    """Keypad ``7`` and Home"""
    KEYPAD_EIGHT
    """Keypad ``8`` and Up Arrow"""
    KEYPAD_NINE
    """Keypad ``9`` and PgUp"""
    KEYPAD_ZERO
    """Keypad ``0`` and Ins"""
    KEYPAD_PERIOD
    """Keypad ``.`` and Del"""
    KEYPAD_BACKSLASH
    """Keypad ``\\`` and ``|`` (Non-US)"""

    APPLICATION
    """Application: also known as the Menu key (Windows)"""
    POWER
    """Power (Mac)"""
    KEYPAD_EQUALS
    """Keypad `ac)"""
    F13
    """Function key F13 (Mac)"""
    F14
    """Function key F14 (Mac)"""
    F15
    """Function key F15 (Mac)"""
    F16
    """Function key F16 (Mac)"""
    F17
    """Function key F17 (Mac)"""
    F18
    """Function key F18 (Mac)"""
    F19
    """Function key F19 (Mac)"""

    F20
    """Function key F20"""
    F21
    """Function key F21"""
    F22
    """Function key F22"""
    F23
    """Function key F23"""
    F24
    """Function key F24"""

    LEFT_CONTROL
    """Control modifier left of the spacebar"""
    CONTROL_CONTROL
    """Alias for LEFT_CONTROL"""
    LEFT_SHIFT
    """Shift modifier left of the spacebar"""
    SHIFT_SHIFT
    """Alias for LEFT_SHIFT"""
    LEFT_ALT
    """Alt modifier left of the spacebar"""
    ALT_ALT
    """Alias for LEFT_ALT; Alt is also known as Option (Mac)"""
    OPTION"""Labeled as Option on some Mac keyboards"""
    LEFT_GUI
    """GUI modifier left of the spacebar"""
    GUI_GUI
    """Alias for LEFT_GUI; GUI is also known as the Windows key, Command (Mac), or Meta"""
    WINDOWS"""Labeled with a Windows logo on Windows keyboards"""
    COMMAND"""Labeled as Command on Mac keyboards, with a clover glyph"""
    RIGHT_CONTROL
    """Control modifier right of the spacebar"""
    RIGHT_SHIFT
    """Shift modifier right of the spacebar"""
    RIGHT_ALT
    """Alt modifier right of the spacebar"""
    RIGHT_GUI
    """GUI modifier right of the spacebar"""
</details>


### Example of basic text input

```json
"key1": {
    "name": "my-key",
    "command": [
        "this is some neat text dawg"
    ]
}
```
This will simply type out `this is some neat text dawg` when `key1` is pressed.

### Example of all three command types being used at once
```json
"key1": {
    "name": "my-key",
    "command": [
        "this is some neat text dawg",
        "F12",
        ["VOLUME_INCREMENT"]
    ]
}
```
This will type some text, hit F12 then increment the volume

## Using a sound file

```json
"key1": {
    "name": "my-key",
    "command": [],
    "sound": "file.mp3"
}
```

This will play a sound file when `key1` is clicked. The file must be stored within the `sound` folder and must be either an `mp3` or `wav` file type.

***Note: You can still specifiy a command, in this example i just left it empty so nothing will be typed.***

## Playing a tone

```json
"key1": {
    "name": "my-key",
    "command": [],
    "tone": 255
}
```

This will play a simple tone when `key1` is clicked. The number for the tone should be greater than 0.