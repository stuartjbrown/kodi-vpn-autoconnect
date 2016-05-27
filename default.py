# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import os
import xbmcgui

__addon__ = xbmcaddon.Addon(sys.argv[0])

addon = []
vpn = []
execfile = []
sets = []
cur_vpn = ''
cur_i = 0
defaultopenvpn = ''
defaultfile = ''

def reload_settings():
	global cur_vpn
	global defaultopenvpn
	global defaultfile
	del addon[:]
	del vpn[:]
	del execfile[:]
	del sets[:]
	
	for a in range(10):
		settings_addon = __addon__.getSetting("addon" + str(a+1)).lower()
		settings_vpn = __addon__.getSetting("addonovpn" + str(a+1))
		settings_file = __addon__.getSetting("file" + str(a+1))

		if settings_addon != '':
			addon.append(settings_addon)
			vpn.append(settings_vpn)
			execfile.append(settings_file)
	sets.append(__addon__.getSetting("file_disconnect"))	#disconnectfile = sets[0]
	sets.append(__addon__.getSetting("show_name"))			#show_name of path as notification = sets[1]

	defaultopenvpn = __addon__.getSetting("defaultopenvpn")
	defaultfile = __addon__.getSetting("defaultfile")
	if defaultopenvpn != '':
		xbmc.executebuiltin('XBMC.RunScript(script.openvpn, ' + defaultopenvpn + ')')
		cur_vpn = defaultopenvpn
	if defaultfile != '':
		os.system(defaultfile)
		cur_vpn = defaultfile
	
class XBMCMonitor( xbmc.Monitor ):
    def __init__( self, *args ):
        pass

    def onSettingsChanged( self ):
		reload_settings()
		
monitor = XBMCMonitor()
reload_settings()

while (not xbmc.abortRequested):
	addonpath = xbmc.getInfoLabel('Container.FolderPath').lower()
	if sets[1] == 'true':
		xbmc.executebuiltin('Notification(FolderPath, ' + xbmc.getInfoLabel('Container.FolderPath') + ', 2)')
		#xbmc.executebuiltin('Notification(FolderPath, ' + xbmc.getInfoLabel() + ', 2)')
	i = 0
	in_addon = False
	for l_addon in addon:
		if l_addon in addonpath:
			in_addon = True
			if not xbmc.Player().isPlayingVideo():
				if cur_vpn != execfile[i]:
					if execfile[i] != '':
						if cur_vpn == defaultfile:
							os.system(sets[0])
							xbmc.sleep(2000)
						xbmc.executebuiltin('Notification(VPN, Switching VPN, 2)')
						os.system(execfile[i])
						cur_vpn = execfile[i]
						cur_i = i
						xbmc.sleep(4000)
						break
				if cur_vpn != vpn[i]:		
					if vpn[i] != '':
						if cur_vpn == defaultopenvpn:
							xbmc.executebuiltin('XBMC.RunScript(script.openvpn, disconnect)')
							xbmc.sleep(2000)
						xbmc.executebuiltin('XBMC.RunScript(script.openvpn, ' + vpn[i] + ')')
						cur_vpn = vpn[i]
						cur_i = i
						xbmc.sleep(4000)
						break
		i += 1
	
	if (not in_addon) and (not xbmc.Player().isPlayingVideo()) :
		if not cur_vpn in ['', defaultfile, defaultopenvpn]:
			if sets[0] != '':
				xbmc.executebuiltin('Notification(VPN, Disconnect, 2)')
				os.system(sets[0])
				xbmc.sleep(2000)
				if defaultfile != '':
					os.system(defaultfile)
					cur_vpn = defaultfile
				else:	
					cur_vpn = ''
			if vpn[cur_i] != '':
				xbmc.executebuiltin('XBMC.RunScript(script.openvpn, disconnect)')
				xbmc.sleep(2000)
				if defaultopenvpn != '':
					xbmc.executebuiltin('XBMC.RunScript(script.openvpn, ' + defaultopenvpn + ')')
					cur_vpn = defaultopenvpn
				else:	
					cur_vpn = ''
					
	xbmc.sleep(1000)
