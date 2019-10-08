#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------
#   Import Libraries
#---------------------------
import sys
import os
import json
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Whisper response to a command"
Website = "none"
Description = "Response with a whisper to a command when the user has a certain permission level (Twitch only!!!)"
Creator = "Korben85"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Settings overwritten! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command:
		if Parent.HasPermission(data.User, ScriptSettings.Permission): # Has Permissions
			SendAllGood(data)
		else: # Not Enough Permissions Response
			SendNotEnoughPerms(data)
	return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
	return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

#---------------------------
#   SendAllGood
#---------------------------
def SendAllGood(data):
	if data.IsFromTwitch():
		#Send whisper message to User (SendStreamMessage | SendTwitchMessage)
		Parent.SendTwitchMessage("/w $username " + ScriptSettings.ResponseMessage.format(data.User, ScriptSettings.Command, ScriptSettings.Permission)) #"/w $username " + -> whisper to user
		Parent.SendTwitchMessage(ScriptSettings.ResponseMessageToChat.format(data.User, ScriptSettings.Command, ScriptSettings.Permission))
	return

#---------------------------
#   SendNotEnoughPerms
#---------------------------
def SendNotEnoughPerms(data):
	if data.IsFromTwitch():
		Parent.SendTwitchMessage(ScriptSettings.ResponseNotEnoughPermissions.format(
		data.User, ScriptSettings.Command, ScriptSettings.Permission))
	else:
		Parent.SendStreamMessage(ScriptSettings.ResponseMessageToNonTwitch.format(data.User, ScriptSettings.Command, ScriptSettings.Permission))
	return
