#######################################################################
#
#    Push Service for Enigma-2
#    Coded by betonme (c) 2012 <glaserfrank(at)gmail.com>
#    Support: http://www.i-have-a-dreambox.com/wbb2/thread.php?threadid=167779
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#######################################################################

import os, sys, traceback

# Plugin
from Plugins.Plugin import PluginDescriptor

# Config
from Components.config import config, ConfigSubsection, ConfigNothing, ConfigOnOff, ConfigText, ConfigClock, ConfigSelectionNumber

# Default encoding
#from Components.Language import language

# Plugin internal
from __init__ import _
from PushService import PushService
#from ConfigScreen import ConfigScreen


# Constants
NAME = "PushService"
VERSION = "0.4.4"
SUPPORT = "http://bit.ly/psihad"
DONATE = "http://bit.ly/pspaypal"
ABOUT = "\n  " + NAME + " " + VERSION + "\n\n" \
				+ _("  (C) 2012 by betonme @ IHAD \n\n") \
				+ _("  If You like this plugin and want to support it,\n") \
				+ _("  or if just want to say ''thanks'',\n") \
				+ _("  feel free to donate via PayPal. \n\n") \
				+ _("  Thanks a lot ! \n  PayPal: ") + DONATE + "\n" \
				+ _("  Support: ") + SUPPORT


# Globals
gPushService = None


# Config options
config.pushservice                           = ConfigSubsection()

config.pushservice.about                     = ConfigNothing()

config.pushservice.enable                    = ConfigOnOff(default = True)

config.pushservice.boxname                   = ConfigText(default = "Enigma2", fixed_size = False)
config.pushservice.xmlpath                   = ConfigText(default = "/etc/enigma2/pushservice.xml", fixed_size = False)

config.pushservice.time                      = ConfigClock(default = 0)
config.pushservice.period                    = ConfigSelectionNumber(0, 1000, 1, default = 24)
config.pushservice.runonboot                 = ConfigOnOff(default = True)
config.pushservice.bootdelay                 = ConfigSelectionNumber(5, 1000, 5, default = 10)

config.pushservice.push_errors               = ConfigOnOff(default = False)


#######################################################
# Plugin configuration
def setup(session, **kwargs):
	try:
		### For testing only
		import ConfigScreen
		reload(ConfigScreen)
		###
		session.open(ConfigScreen.ConfigScreen)
	except Exception, e:
		print _("PushService setup exception ") + str(e)
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)


#######################################################
# Autostart
def autostart(reason, **kwargs):
	if reason == 0:  # start
		if config.pushservice.enable.value:
			try:
				global gPushService
				gPushService = PushService()
				gPushService.start()
			except Exception, e:
				print _("PushService autostart exception ") + str(e)
				exc_type, exc_value, exc_traceback = sys.exc_info()
				traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)


#######################################################
# Plugin main function
def Plugins(**kwargs):
	
	descriptors = []
	
	if config.pushservice.enable.value:
		# AutoStart
		descriptors.append( PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, fnc = autostart, needsRestart = False) )
		
	#TODO icon
	descriptors.append( PluginDescriptor(name = NAME, description = NAME + " " +_("configuration"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = setup, needsRestart = False) ) #icon = "/icon.png"

	return descriptors
