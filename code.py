
import os
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from macrodefinition import MacroDefinition, NUMBER_OF_KEYS, MACROS_DIRECTORY
import commands

# CONFIGURABLES ------------------------


DEFAULT_BRIGHTNESS = 1

commands.setReadTimeout(0)
macropad = MacroPad()
macropad.pixels.brightness = DEFAULT_BRIGHTNESS                    


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

def handleCommands():
        command = commands.readCommand()
        if command != None:
            code = commands.getCode(command)
            payload = commands.getPayload(command)

            commands.handlePingCommand(code)
            commands.handleGetCurrentMacroName(code, currentMacro.name)
            commands.handleGetMacroDefinition(code, payload, macros)

            selectedMacroIndex = commands.handleSetCurrentMacroByName(code, payload, macros)
            if selectedMacroIndex != -1:
                global currentMacroIndex
                currentMacroIndex = selectedMacroIndex
            commands.handleCreateMacroDefinition(code, payload, macros)
            commands.handleUpdateMacroDefinition(code, payload, macros)
            commands.handleDeleteMacroDefinition(code, payload, macros)
            commands.handlerListMacroDefinitionNames(code, macros)
            


while True:
    
    currentMacroIndex = macropad.encoder % len(macros)
    if currentMacroIndex >= len(macros):
        currentMacroIndex = 0
    
    handleCommands()
    displayMacro(currentMacro, displayGroup)
    currentMacro = macros[currentMacroIndex]


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

