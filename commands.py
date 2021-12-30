import usb_cdc
import json
from macrodefinition import MacroDefinition

MAX_SIZE = 4096

COMMAND_PING = ('PING', 0x0)
COMMAND_PONG = ('PONG', 0x1)
COMMAND_GET_CURRENT_MACRO_NAME = ('GET_CURRENT_MACRO_NAME', 0x2)
COMMAND_SET_CURRENT_MACRO_BY_NAME = ('SET_CURRENT_MACRO_BY_NAME', 0x3)
COMMAND_GET_MACRO_DEFINITION = ('GET_MACRO_DEFINITION', 0x4)
COMMAND_CREATE_MACRO_DEFINITION = ('CREATE_MACRO_DEFINITION', 0x5)
COMMAND_UPDATE_MACRO_DEFINITION = ('UPDATE_MACRO_DEFINITION', 0x6)
COMMAND_DELETE_MACRO_DEFINITION = ('DELETE_MACRO_DEFINITION', 0x7)
COMMAND_LIST_MACRO_DEFINITON_NAMES = ('LIST_MACRO_DEFINITON_NAMES', 0x8)



ERROR_NOT_FOUND = ('NOT_FOUND', 0x1)
ERROR_INVALID_PAYLOAD = ('INVALID_PAYLOAD', 0x2)
ERROR_UNKNOWN = ('UNKNOWN', 0x3)
ERROR_ALREADY_EXIST = ('ALREADY_EXIST', 0x4)

SUCCESS_STATUS = 'success'

COMMAND_CODE_NAME_MAP = {
    0x0: COMMAND_PING[0],
    0x1: COMMAND_PONG[0],
    0x2: COMMAND_GET_CURRENT_MACRO_NAME[0],
    0x3: COMMAND_SET_CURRENT_MACRO_BY_NAME[0],
    0x4: COMMAND_GET_MACRO_DEFINITION[0],
    0x5: COMMAND_CREATE_MACRO_DEFINITION[0],
    0x6: COMMAND_UPDATE_MACRO_DEFINITION[0],
    0x7: COMMAND_DELETE_MACRO_DEFINITION[0],
    0x8: COMMAND_LIST_MACRO_DEFINITON_NAMES[0],
}



def _validateCommand(command):
    try:
        _ = COMMAND_CODE_NAME_MAP[command['code']]
        _ = command['payload']
        return True
    except:
        return False

def setReadTimeout(timeout: int = None):
    usb_cdc.data.timeout = timeout

def setWriteTimeout(timeout: int = None):
    usb_cdc.data.write_timeout = timeout

def getCode(command):
    return command['code']

def getPayload(command):
    return command['payload']

def readCommand():
    command = usb_cdc.data.readline(MAX_SIZE)
    if len(command) == 0:
        return None

    parsedCommand = json.loads(command.decode("utf-8"))
    if _validateCommand(parsedCommand):
        return parsedCommand
    return None

def writePayload(code, payload = ''):
    command = {
        'code': code,
        'payload': payload
    }
    commandBytes = str.encode(json.dumps(command))
    bytesWritten = usb_cdc.data.write(commandBytes)
    return bytesWritten != -1

def writeSuccessfulRequestPayload(code, data = {}):
    payload = {
        'status': SUCCESS_STATUS,
        'data': data
    }
    return writePayload(code, payload)

def writeFailedRequestPayload(code, error, detail = ''):
    payload = {
        'error': error[0],
        'errorCode': error[1],
        'detail': detail
    }
    return writePayload(code, payload)

def handlePingCommand(code):
    if code == COMMAND_PING[1]:
        writeSuccessfulRequestPayload(COMMAND_PONG[1])

def handleGetCurrentMacroName(code, currentMacroName):
    if code == COMMAND_GET_CURRENT_MACRO_NAME[1]:
        writeSuccessfulRequestPayload(code, {
            'name': currentMacroName
        })

def handleSetCurrentMacroByName(code, name: str, macros: list):
    selectedMacroIndex = -1
    if code == COMMAND_SET_CURRENT_MACRO_BY_NAME[1]:
        for macro in macros:
            if macro.name == name:
                selectedMacroIndex = macros.index(macro)
                writeSuccessfulRequestPayload(code)
                break
        if selectedMacroIndex == -1:
            writeFailedRequestPayload(code, ERROR_NOT_FOUND)
    return selectedMacroIndex

def handleGetMacroDefinition(code, name, macros):
    if code == COMMAND_GET_MACRO_DEFINITION[1]:
        try:
            foundMacro = next(filter(lambda macro: macro.name == name, macros))
            writeSuccessfulRequestPayload(code, foundMacro.parsedDefinition)
        except StopIteration:
            writeFailedRequestPayload(code, ERROR_NOT_FOUND)

def handleCreateMacroDefinition(code, definition, macros: list):
    if code == COMMAND_CREATE_MACRO_DEFINITION[1]:
        if MacroDefinition.validate(definition):
            try:
                doesNotAlreadyExist = len(list(filter(lambda macro: macro.name == definition['name'], macros))) == 0
                if doesNotAlreadyExist:
                    newMacro = MacroDefinition(definition=definition)
                    writeSuccessfulRequestPayload(code)
                    macros.append(newMacro)
                else:
                    writeFailedRequestPayload(
                        code,
                        ERROR_ALREADY_EXIST,
                        'Macro with provided name already exist'
                    )
            except Exception as e:
                writeFailedRequestPayload(
                    code,
                    ERROR_UNKNOWN,
                    str(e)
                )
        else:
            writeFailedRequestPayload(
                code, 
                ERROR_INVALID_PAYLOAD,
                'Provided macro definition is invalid.'
        )
        
def handleUpdateMacroDefinition(code, payload, macros: list):
    if code == COMMAND_UPDATE_MACRO_DEFINITION[1]:
        try:
            # Check the proposed new definition is valid.
            if MacroDefinition.validate(payload):
                macroName = payload['name']
                #find the macro in question...
                macro = next(filter(lambda macro: macro.name == macroName, macros))
                macro.updateDefinition(payload)
                writeSuccessfulRequestPayload(code)
    
        except KeyError:
            writeFailedRequestPayload(
                code, 
                ERROR_INVALID_PAYLOAD, 
                'name and macros keys are required in payload.'
            )
        except StopIteration:
            writeFailedRequestPayload(
                code,
                ERROR_NOT_FOUND,
                'Provided macro name does not exist.'
            )
        except Exception as e: 
            writeFailedRequestPayload(
                code, 
                ERROR_UNKNOWN,
                str(e)
            )

def handleDeleteMacroDefinition(code, name, macros: list):
    if code == COMMAND_DELETE_MACRO_DEFINITION[1]:
        try:
            print(name)
            foundMacro = next(filter(lambda macro: macro.name == name, macros))
            macroIndex = macros.index(foundMacro)
            macroToDelete = macros.pop(macroIndex)
            macroToDelete.removeFileOnDelete = True
            macroToDelete.terminate()
            del macroToDelete
            writeSuccessfulRequestPayload(code)
        except StopIteration:
            writeFailedRequestPayload(code, ERROR_NOT_FOUND)
        except Exception as e:
            writeFailedRequestPayload(code, ERROR_UNKNOWN, str(e))

def handlerListMacroDefinitionNames(code, macros):
    if code == COMMAND_LIST_MACRO_DEFINITON_NAMES[1]:
        writeSuccessfulRequestPayload(
            code,
            list(map(lambda macro: macro.name, macros))
        )
    