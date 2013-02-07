#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Team:
#   J Phani Mahesh <phanimahesh@gmail.com> 
#   Barneedhar (jokerdino) <barneedhar@ubuntu.com> 
#   Amith KK <amithkumaran@gmail.com>
#   Georgi Karavasilev <motorslav@gmail.com>
#   Sam Tran <samvtran@gmail.com>
#   Sam Hewitt <hewittsamuel@gmail.com>
#
# Description:
#   A One-stop configuration tool for Unity.
#
# Legal Stuff:
#
# This file is a part of Unity Tweak Tool
#
# Unity Tweak Tool is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# Unity Tweak Tool is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/gpl-3.0.txt>


from UnityTweakTool.section.skeletonpage import Section,Tab
from UnityTweakTool.elements.switch import Switch
from UnityTweakTool.elements.checkbox import CheckBox

System=Section(ui='desktop.ui',id='nb_desktop_settings')

switch_desktop_icons= Switch({
    'id'        : 'switch_desktop_icons',
    'builder'   : System.builder,
    'schema'    : 'org.gnome.desktop.background',
    'path'      : None,
    'key'       : 'show-desktop-icons',
    'type'      : 'boolean',
    'map'       : {True:True,False:False},
    'dependants': ['l_desktop_icons_display',
                    'check_desktop_home',
                    'check_desktop_networkserver',
                    'check_desktop_trash',
                    'check_desktop_devices']
})

check_desktop_home= CheckBox({
    'id'        : 'check_desktop_home',
    'builder'   : System.builder,
    'schema'    : 'org.gnome.nautilus.desktop',
    'path'      : None,
    'key'       : 'home-icon-visible',
    'type'      : 'boolean',
    'map'       : {True:True,False:False},
    'dependants': []
})

check_desktop_networkserver= CheckBox({
    'id'        : 'check_desktop_networkserver',
    'builder'   : System.builder,
    'schema'    : 'org.gnome.nautilus.desktop',
    'path'      : None,
    'key'       : 'network-icon-visible',
    'type'      : 'boolean',
    'map'       : {True:True,False:False},
    'dependants': []
})

check_desktop_trash= CheckBox({
    'id'        : 'check_desktop_trash',
    'builder'   : System.builder,
    'schema'    : 'org.gnome.nautilus.desktop',
    'path'      : None,
    'key'       : 'trash-icon-visible',
    'type'      : 'boolean',
    'map'       : {True:True,False:False},
    'dependants': []
})

check_desktop_devices= CheckBox({
    'id'        : 'check_desktop_devices',
    'builder'   : System.builder,
    'schema'    : 'org.gnome.nautilus.desktop',
    'path'      : None,
    'key'       : 'volumes-visible',
    'type'      : 'boolean',
    'map'       : {True:True,False:False},
    'dependants': []
})

DesktopIcons=Tab([  switch_desktop_icons,
                    check_desktop_home,
                    check_desktop_networkserver,
                    check_desktop_trash,
                    check_desktop_devices])

# Pass in the id of restore defaults button to enable it.
DesktopIcons.enable_restore('b_desktop_settings_icons_reset')

# Each page must be added using add_page
System.add_page(DesktopIcons)
# After all pages are added, the section needs to be registered to start listening for events
System.register()