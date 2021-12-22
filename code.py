"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
import displayio
import terminalio
import json
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# CONFIGURABLES ------------------------
MACROS_DIRECTORY = '/macros/'
SOUND_DIRECTORY = 'sounds/'
DEFAULT_BRIGHTNESS = 1
NUMBER_OF_KEYS = 12

macropad = MacroPad()
macropad.pixels.brightness = DEFAULT_BRIGHTNESS

KEY_MAP = {
    0: "key1",
    1: "key2",
    2: "key3",
    3: "key4",
    4: "key5",
    5: "key6",
    6: "key7",
    7: "key8",
    8: "key9",
    9: "key10",
    10: "key11",
    11: "key12",
}

def tryGetDictionaryKey(key, dictionary, fallbackValue=None):
    try:
        return (True, dictionary[key])
    except:
        return (False, fallbackValue)

class KeyDefinition:
    def __tryGetKeyCode(_, command):
        try:
            return (True, int(getattr(Keycode(), command)))
        except:
            return (False, None)
    def __tryGetConsumerControlCode(_, command):
        try:
            return (True, int(getattr(ConsumerControlCode(), command)))
        except:
            return (False, None)
    def __initCommand(self, command):
        if isinstance(command, list):
            consumerControls = []
            for consumerControl in command:
                (isConsumerControlCode, consumerControlValue) = self.__tryGetConsumerControlCode(consumerControl)
                if isConsumerControlCode:
                    consumerControls.append(consumerControlValue)
            return consumerControls

        (isKeyCode, keyCodeValue) = self.__tryGetKeyCode(command)
        if isKeyCode:
            return keyCodeValue
        else:
            return command
    def __init__(self, name, color: str, commands, sound, tone) -> None:
        self.name = name
        self.color = int(color.replace("#", "0x"), 0)
        self.commands = list(map(self.__initCommand, commands))
        self.sound =  (SOUND_DIRECTORY + sound) if sound != "" else ""
        self.tone = tone

class MacroDefinition:
    def __validate(_, dictionary) -> bool:
        hasProps = ("name" in dictionary) and ("macros" in dictionary)
        if hasProps:
            for keyIdentifier in dictionary['macros']:
                if keyIdentifier in KEY_MAP.values():
                    continue
                else:
                    return False
            return True
        else:
            return False
    def __getName(_, dictionary) -> str:
        return dictionary['name']
    def __getKeyCommands(_, dictionary) -> None:
        keyCommands = []
        (_, macros) = tryGetDictionaryKey('macros', dictionary)
        for keyId in range(NUMBER_OF_KEYS):
            (isPresent, macro) = tryGetDictionaryKey(KEY_MAP[keyId], macros)
            
            if not isPresent:
                keyCommands.append(KeyDefinition("","#000000", [], "", -1))
                continue
            (_, name) = tryGetDictionaryKey('name', macro, "")
            (_, color) = tryGetDictionaryKey('color', macro, "#000000")
            (_, command) = tryGetDictionaryKey('command', macro, [])
            (_, sound) = tryGetDictionaryKey('sound', macro, "")
            (_, tone) = tryGetDictionaryKey('tone', macro, -1)
            keyCommands.append(KeyDefinition(
                name,
                color,
                list(command),
                sound,
                tone
            ))
        return keyCommands
    def __init__(self, filePath):
        definition = str(open(filePath).read())
        dictionary = None
        try:
            dictionary = json.loads(definition)
        except:
            dictionary = {}
        self.isValid = self.__validate(dictionary)
        if self.isValid:
            self.name = self.__getName(dictionary)
            self.keyCommands = self.__getKeyCommands(dictionary)
    def getKeyDefinition(self, keyId) -> KeyDefinition:
        return self.keyCommands[keyId]


def retrieveMacros() -> list:
    definitions = []
    files = os.listdir(MACROS_DIRECTORY)
    for file in files:
        macroDefinition = MacroDefinition(MACROS_DIRECTORY + file)
        if macroDefinition.isValid:
            definitions.append(macroDefinition)
    return definitions

def setupDisplayLayout():
    group = displayio.Group()
    for key_index in range(12):
        x = key_index % 3
        y = key_index // 3
        group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                anchored_position=((macropad.display.width - 1) * x / 2,
                                                    macropad.display.height - 1 -
                                                    (3 - y) * 12),
                                anchor_point=(x / 2, 1.0)))
    group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
    group.append(label.Label(terminalio.FONT, text='Hi', color=0x000000,
                            anchored_position=(macropad.display.width//2, -2),
                            anchor_point=(0.5, 0.0)))
    return group

def displayMacro(macro: MacroDefinition, displayGroup):
    displayGroup[13].text = macro.name
    for keyId in range(NUMBER_OF_KEYS):
        keyDefinition = macro.getKeyDefinition(keyId)
        macropad.pixels[keyId] = keyDefinition.color
        displayGroup[keyId].text = keyDefinition.name



displayGroup = setupDisplayLayout()
macros = retrieveMacros()
currentMacroIndex = 0
currentMacro = macros[currentMacroIndex]
previousMacroIndex = -1
currentBrightness = DEFAULT_BRIGHTNESS
macropad.pixels.brightness = (currentBrightness % 10) / 10
macropad.display.show(displayGroup)

while True:

    currentMacroIndex = macropad.encoder % len(macros)
    if currentMacroIndex >= len(macros):
        currentMacroIndex = 0

    currentMacro = macros[currentMacroIndex]
    if currentMacroIndex != previousMacroIndex:
        displayMacro(currentMacro, displayGroup)
        previousMacroIndex = currentMacroIndex

    event = macropad.keys.events.get()
    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        currentBrightness += 1
        macropad.pixels.brightness = (currentBrightness % 10) / 10

    if not event or event.key_number > NUMBER_OF_KEYS:
        continue
    keyId = event.key_number

    keyCommands = currentMacro.getKeyDefinition(keyId).commands
    keySound = currentMacro.getKeyDefinition(keyId).sound
    keyTone = currentMacro.getKeyDefinition(keyId).tone
    if event.pressed:
        if keySound != "":
            macropad.play_file(keySound)
        if keyTone != -1:
            macropad.play_tone(keyTone, 0.1)
        for command in keyCommands:
            if isinstance(command, int):
                if command >= 0:
                    macropad.keyboard.press(command)
                else:
                    macropad.keyboard.release(-command)
            elif isinstance(command, str):
                macropad.keyboard_layout.write(command)
            elif isinstance(command, list):
                for consumerControl in command:
                    if isinstance(consumerControl, int):
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(consumerControl)

    else:
        for command in keyCommands:
            if isinstance(command, int) and command >= 0:
                macropad.keyboard.release(command)
        macropad.consumer_control.release()



    macropad.display.show(displayGroup)
