from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
import json

import os


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
NUMBER_OF_KEYS = 12
SOUND_DIRECTORY = 'sounds/'
MACROS_DIRECTORY = '/macros/'
ROOT_DIRECTORY = '/'

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
    def validate(definition) -> bool:
        hasProps = ("name" in definition) and ("macros" in definition)
        if hasProps:
            for keyIdentifier in definition['macros']:
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
    def __setupMacroDefinition(self, definition, filePath, skipParse = False):
        parsedDefinition = None
        if not skipParse:
            try:
                parsedDefinition = json.loads(definition)
            except:
                parsedDefinition = {}
        else:
            parsedDefinition = definition
        self.isValid = MacroDefinition.validate(parsedDefinition)
        if self.isValid:
            self.name = self.__getName(parsedDefinition)
            self.keyCommands = self.__getKeyCommands(parsedDefinition)
            self.rawDefinition = parsedDefinition
            self.filePath = filePath
            self.removeFileOnDelete = False
    def __init__(self, filePath = None, definition = None):
        definitionToUse = {}
        skipParse = False
        if filePath != None:  
            file = open(filePath)
            definitionToUse = str(file.read())
            file.close()
        elif definition != None and MacroDefinition.validate(definition):
            filePath = MACROS_DIRECTORY + definition['name'] + '.json'
            file = open(filePath, "x")
            json.dump(definition, file)
            file.close()
            definitionToUse = definition
            skipParse = True

        self.__setupMacroDefinition(definitionToUse, filePath, skipParse)

    def getKeyDefinition(self, keyId) -> KeyDefinition:
        return self.keyCommands[keyId]
    def updateDefinition(self, newDefinition):
        file = open(self.filePath, "w")
        json.dump(newDefinition, file)
        file.close()
        self.__init__(self.filePath)
    def terminate(self):
        if self.removeFileOnDelete and (
            self.filePath != MACROS_DIRECTORY or
            self.filePath != ROOT_DIRECTORY
            ):
            os.remove(self.filePath)



