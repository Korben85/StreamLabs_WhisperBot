import os
import codecs
import json

class MySettings(object):
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.Command = "!ts"
			self.ReponseMessage = "{0}, hier sind die TS-Daten: Server:255.255.255.255 PW:sicheresPW\r\nViel Spaß!"
			self.ReponseMessageToChat = "Hey {0}, dir wurden die Teamspeak-Daten zugeflüstert ;)"
			self.Permission = "Subscriber"
			self.ReponseNotEnoughPermissions = "Sorry {0}, der Befehl \"{1}\" ist nur für {2}!"
			self.ReponseMessageToNonTwitch = "{0}, der Befehl \"{1}\" ist nur im Twitch-Chat verfügbar."

	def Reload(self, jsondata):
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, settingsfile):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")
		return