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

import os, os.path

from gi.repository import Gtk, Gio

from .ui import ui
from . import settings
from . import gsettings

class Themesettings ():
    def __init__(self, container):
        '''Handler Initialisations.
        Obtain all references here.'''
        self.builder = Gtk.Builder()
        self.glade = (os.path.join(settings.UI_DIR, 
                                    'theme.ui'))
        self.container = container
        self.builder.add_from_file(self.glade)
        self.ui = ui(self.builder)
        self.page = self.ui['nb_themesettings']
        self.page.unparent()
        
        self.gtkthemestore=Gtk.ListStore(str,str)
        self.windowthemestore=self.gtkthemestore
        self.ui['tree_gtk_theme'].set_model(self.gtkthemestore)
        self.ui['tree_window_theme'].set_model(self.windowthemestore)
# Get all themes
        systhdir='/usr/share/themes'
        systemthemes=[(theme.capitalize(),os.path.join(systhdir,theme)) for theme in os.listdir(systhdir) if os.path.isdir(os.path.join(systhdir,theme))]
        try:
            uthdir=os.path.expanduser('~/.themes')
            userthemes=[(theme.capitalize(),os.path.join(uthdir,theme)) for theme in os.listdir(uthdir) if os.path.isdir(os.path.join(uthdir,theme))]
        except OSError as e:
            userthemes=[]
        allthemes=systemthemes+userthemes
        allthemes.sort()
        required=['gtk-2.0','gtk-3.0','metacity-1']
        self.gtkthemes={}
        self.windowthemes={}
        for theme in allthemes:
            if all([os.path.isdir(os.path.join(theme[1],req)) for req in required]):
                iter=self.gtkthemestore.append(theme)
                themename=os.path.split(theme[1])[1]
                self.gtkthemes[themename]={"iter":iter,"path":theme[1]}
                self.windowthemes[themename]={"iter":iter,"path":theme[1]}

        self.iconthemestore=Gtk.ListStore(str,str)
        self.cursorthemestore=Gtk.ListStore(str,str)
        self.ui['tree_icon_theme'].set_model(self.iconthemestore)
        self.ui['tree_cursor_theme'].set_model(self.cursorthemestore)
        
        sysithdir='/usr/share/icons'
        systemiconthemes= [(theme.capitalize(),os.path.join(sysithdir,theme)) for theme in os.listdir(sysithdir) if os.path.isdir(os.path.join(sysithdir,theme))]
        to_be_hidden=[('Loginicons','/usr/share/icons/LoginIcons'),('Unity-webapps-applications','/usr/share/icons/unity-webapps-applications')]
        for item in to_be_hidden:
            try:
                systemiconthemes.remove(item)
            except ValueError as e:
                pass
        try:
            uithdir=os.path.expanduser('~/.icons')
            usericonthemes=[(theme.capitalize(),os.path.join(uithdir,theme)) for theme in os.listdir(uithdir) if os.path.isdir(os.path.join(uithdir,theme))]
        except OSError as e:
            usericonthemes=[]
        allithemes=systemiconthemes+usericonthemes
        allithemes.sort()
        self.iconthemes={}
        self.cursorthemes={}
        for theme in allithemes:
            iter=self.iconthemestore.append(theme)
            themename=os.path.split(theme[1])[1]
            self.iconthemes[themename]={"iter":iter,"path":theme[1]}
            if os.path.isdir(os.path.join(theme[1],'cursors')):
                iter=self.cursorthemestore.append(theme)
                self.cursorthemes[themename]={"iter":iter,"path":theme[1]}

        self.matchthemes=True
        self.refresh()
        self.refresh_window_controls()
        self.refresh_window_controls_combobox()
        self.refresh_window_controls_checkbox()
        self.builder.connect_signals(self)

#=====================================================================#
#                                Helpers                              #
#=====================================================================#


    def refresh(self):
        # System theme
        gtkthemesel=self.ui['tree_gtk_theme'].get_selection()
        gtktheme=gsettings.gnome('desktop.interface').get_string('gtk-theme')
        gtkthemesel.select_iter(self.gtkthemes[gtktheme]['iter'])

        # Window Theme
        windowthemesel=self.ui['tree_window_theme'].get_selection()
        windowtheme=gsettings.gnome('desktop.wm.preferences').get_string('theme')
        windowthemesel.select_iter(self.windowthemes[windowtheme]['iter'])

        # Icon theme
        iconthemesel=self.ui['tree_icon_theme'].get_selection()
        icontheme=gsettings.gnome('desktop.interface').get_string('icon-theme')
        iconthemesel.select_iter(self.iconthemes[icontheme]['iter'])

        # Cursor theme
        cursorthemesel=self.ui['tree_cursor_theme'].get_selection()
        cursortheme=gsettings.gnome('desktop.interface').get_string('cursor-theme')

# FIXME: LP bug: #1097227
        try:
            cursorthemesel.select_iter(self.cursorthemes[cursortheme]['iter'])
# TODO: except part should make sure the selection is deselected.
        except KeyError:
            cursorthemesel.unselect_all()

        # ===== Fonts ===== #

        # Fonts
        self.ui['font_default'].set_font_name(gsettings.interface.get_string('font-name'))
        self.ui['font_document'].set_font_name(gsettings.interface.get_string('document-font-name'))
        self.ui['font_monospace'].set_font_name(gsettings.interface.get_string('monospace-font-name'))
        self.ui['font_window_title'].set_font_name(gsettings.wm.get_string('titlebar-font'))

        # Antialiasing        
        antialiasing = gsettings.antialiasing.get_string('antialiasing')
        if antialiasing == 'none':
            self.ui['cbox_antialiasing'].set_active(0)
        elif antialiasing == 'grayscale':
            self.ui['cbox_antialiasing'].set_active(1)
        elif antialiasing == 'rgba':
            self.ui['cbox_antialiasing'].set_active(2)

        # Hinting            
        hinting = gsettings.antialiasing.get_string('hinting')
        if hinting == 'none':
            self.ui['cbox_hinting'].set_active(0)
        elif hinting == 'slight':
            self.ui['cbox_hinting'].set_active(1)
        elif hinting == 'medium':
            self.ui['cbox_hinting'].set_active(2)
        elif hinting == 'full':
            self.ui['cbox_hinting'].set_active(3)

        # Scaling        
        self.ui['spin_textscaling'].set_value(gsettings.interface.get_double('text-scaling-factor'))


# Custom refresh functions, due to the reset button for the window controls calls a segmentation fault when
# running the entire self.refresh -snwh


        # ===== Window Controls ===== #

    # Button layout
    def refresh_window_controls(self):

        button_layout = gsettings.wm.get_string('button-layout')
        combobox = ['cbox_custom_layout']
        dependants = ['radio_left',
                    'radio_right']
        if button_layout == 'close,minimize,maximize:':
            self.ui['radio_left'].set_active(True)
            self.ui['radio_default_layout'].set_active(True)
            self.ui['check_show_menu'].set_active(False)
        elif button_layout == ':minimize,maximize,close':
            self.ui['radio_right'].set_active(True)
            self.ui['check_show_menu'].set_active(False)
        else:
            self.ui['radio_custom_layout'].set_active(True)
            self.ui.unsensitize(dependants)
            self.ui.sensitize(combobox)
        del dependants
        del combobox
        del button_layout

    # Custom Combobox
    def refresh_window_controls_combobox(self):

        button_layout_cbox = gsettings.wm.get_string('button-layout')
        if button_layout_cbox == 'close:':
            self.ui['cbox_custom_layout'].set_active(1)
        elif button_layout_cbox == 'close,maximize:':
            self.ui['cbox_custom_layout'].set_active(2)
        elif button_layout_cbox == 'close,minimize:':
            self.ui['cbox_custom_layout'].set_active(3)
        elif button_layout_cbox == 'close:maximize':
            self.ui['cbox_custom_layout'].set_active(4)
        else:
            self.ui['cbox_custom_layout'].set_active(0)
        del button_layout_cbox

    # Show menu
    def refresh_window_controls_checkbox(self):

        button_layout_check = gsettings.wm.get_string('button-layout')
        if button_layout_check.startswith('menu:'):
            self.ui['check_show_menu'].set_active(True)
        elif button_layout_check.endswith(':menu'):
            self.ui['check_show_menu'].set_active(True)
        else:
            self.ui['check_show_menu'].set_active(False)
        del button_layout_check
      
# TODO : Find a clever way or set each one manually.
# Do it the dumb way now. BIIIG refactoring needed later.


#-----BEGIN: Theme settings------

# These check for nonetype and return since for some bizzare reason Gtk.quit destroys 
# the selection object and then calls these callbacks. This is a temporary fix to LP:1096964

    # System Theme
    def on_treeselection_gtk_theme_changed(self,udata=None):
        gtktreesel = self.ui['tree_gtk_theme'].get_selection()
        if gtktreesel is None:
            return
        gtkthemestore,iter = gtktreesel.get_selected()
        if self.matchthemes:
            self.ui['treeselection_window_theme'].select_iter(iter)
        themepath=gtkthemestore.get_value(iter,1)
        theme=os.path.split(themepath)[1]
        gsettings.gnome('desktop.interface').set_string('gtk-theme',theme)

    def on_treeselection_window_theme_changed(self,udata=None):
        windowtreesel = self.ui['tree_window_theme'].get_selection()
        if windowtreesel is None:
            return
        windowthemestore,iter = windowtreesel.get_selected()
        if self.matchthemes:
            self.ui['treeselection_gtk_theme'].select_iter(iter)
        themepath=windowthemestore.get_value(iter,1)
        theme=os.path.split(themepath)[1]
        gsettings.gnome('desktop.wm.preferences').set_string('theme',theme)

    # Icon theme
    def on_tree_icon_theme_cursor_changed(self,udata=None):
        icontreesel = self.ui['tree_icon_theme'].get_selection()
        if icontreesel is None:
            return
        iconthemestore,iter = icontreesel.get_selected()
        themepath=iconthemestore.get_value(iter,1)
        theme=os.path.split(themepath)[1]
        gsettings.gnome('desktop.interface').set_string('icon-theme',theme)

    def on_check_show_incomplete_toggled(self,udata=None):
    # TODO 
        print('To do')

    # Cursor theme
    def on_tree_cursor_theme_cursor_changed(self,udata=None):
        cursortreesel = self.ui['tree_cursor_theme'].get_selection()
        if cursortreesel is None:
            return
        cursorthemestore,iter = cursortreesel.get_selected()
        themepath=cursorthemestore.get_value(iter,1)
        theme=os.path.split(themepath)[1]
        gsettings.gnome('desktop.interface').set_string('cursor-theme',theme)

#----- End: Theme settings------

#----- Begin: Font settings--------

    def on_font_default_font_set(self, widget):
        gsettings.interface.set_string('font-name', self.ui['font_default'].get_font_name())
    
    def on_font_document_font_set(self, widget):
        gsettings.interface.set_string('document-font-name', self.ui['font_document'].get_font_name())
    
    def on_font_monospace_font_set(self, widget):
        gsettings.interface.set_string('monospace-font-name', self.ui['font_monospace'].get_font_name())
        
    def on_font_window_title_font_set(self, widget):
        gsettings.wm.set_string('titlebar-font', self.ui['font_window_title'].get_font_name())
        
    def on_cbox_antialiasing_changed(self, widget):
        mode = self.ui['cbox_antialiasing'].get_active()
        if mode == 0:
            gsettings.antialiasing.set_string('antialiasing', "none")
        elif mode == 1:
            gsettings.antialiasing.set_string('antialiasing', "grayscale")
        elif mode == 2:
            gsettings.antialiasing.set_string('antialiasing', "rgba")

    def on_cbox_hinting_changed(self, widget):
        mode = self.ui['cbox_hinting'].get_active()
        if mode == 0:
            gsettings.antialiasing.set_string('hinting', "none")
        elif mode == 1:
            gsettings.antialiasing.set_string('hinting', "slight")
        elif mode == 2:
            gsettings.antialiasing.set_string('hinting', "medium")
        elif mode == 3:
            gsettings.antialiasing.set_string('hinting', "full")
            
    def on_spin_textscaling_value_changed(self, widget):
        gsettings.interface.set_double('text-scaling-factor', self.ui['spin_textscaling'].get_value())

    def on_b_theme_font_reset_clicked(self, widget):
        gsettings.interface.reset('font-name')
        gsettings.interface.reset('document-font-name')
        gsettings.interface.reset('monospace-font-name')
        gsettings.wm.reset('titlebar-font')
        gsettings.antialiasing.reset('antialiasing')
        gsettings.antialiasing.reset('hinting')
        gsettings.interface.reset('text-scaling-factor')
        self.refresh()

#----- End: Font settings--------

#----- Begin: Window control settings--------

    def on_radio_default_layout_toggled(self, button, udata = None):
        mode = self.ui['radio_default_layout'].get_active()
        combobox = ['cbox_custom_layout',]
        dependants = ['radio_left',
                    'radio_right',
                    'l_alignment']
        if mode == True:
            gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')
            self.ui.sensitize(dependants)
            self.ui.unsensitize(combobox)
            self.ui['check_show_menu'].set_active(False)
        else:
            self.ui.unsensitize(dependants)
            self.ui.sensitize(combobox)

    def on_radio_left_toggled(self, button, udata = None):
        mode = self.ui['radio_left'].get_active()
        if mode == True:
            gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')
        else:
            gsettings.wm.set_string('button-layout', ':minimize,maximize,close')

    def on_radio_right_toggled(self, button, udata = None):
        mode = self.ui['radio_right'].get_active()
        if mode == True:
            gsettings.wm.set_string('button-layout', ':minimize,maximize,close')
        else:
            gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')

    def on_radio_custom_layout_toggled(self, button, udata = None):
        combobox = ['cbox_custom_layout']
        dependants = ['radio_left',
                    'radio_right',
                    'l_alignment']
        if self.ui['radio_custom_layout'].get_active() == True:
            self.ui.sensitize(combobox)
            self.ui.unsensitize(dependants)
        else:
            self.ui.unsensitize(combobox)
            self.ui.sensitize(dependants)

    def on_cbox_cbox_custom_layout_changed(self, widget, udata = None):
        cbox_mode = self.ui['cbox_custom_layout'].get_active()
        checkbox = ['check_show_menu']
        if cbox_mode == 0:
            pass
        elif cbox_mode == 1:
            gsettings.wm.set_string('button-layout', 'close:')
            self.ui.sensitize(checkbox)
            self.ui['check_show_menu'].set_active(False)
        elif cbox_mode == 2:
            gsettings.wm.set_string('button-layout', 'close,maximize:')
            self.ui.sensitize(checkbox)
            self.ui['check_show_menu'].set_active(False)
        elif cbox_mode == 3:
            gsettings.wm.set_string('button-layout', 'close,minimize:')
            self.ui.sensitize(checkbox)
            self.ui['check_show_menu'].set_active(False)
        elif cbox_mode == 4:
            gsettings.wm.set_string('button-layout', 'close:maximize')
            self.ui.unsensitize(checkbox)
            self.ui['check_show_menu'].set_active(False)
        else:
            gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')
            self.ui.unsensitize(checkbox)
            self.ui['check_show_menu'].set_active(False)
        del cbox_mode

    def on_check_show_menu_toggled(self, button, udata = None):
        button_layout_check = gsettings.wm.get_string('button-layout')
        if button_layout_check.endswith(':'):
            value = button_layout_check + 'menu'
            gsettings.wm.set_string('button-layout', value)
            del value
            self.ui['radio_custom_layout'].set_active(True)
            self.refresh_window_controls_combobox()
        elif button_layout_check.startswith(':'):
            value = 'menu' + button_layout_check
            gsettings.wm.set_string('button-layout', value)
            self.ui['radio_custom_layout'].set_active(True)
            self.refresh_window_controls_combobox()
            del value
        else:
            gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')
            self.ui['radio_default_layout'].set_active(True)
        del button_layout_check

    def on_b_theme_window_controls_reset_clicked(self, widget):
        gsettings.wm.set_string('button-layout', 'close,minimize,maximize:')
        self.refresh_window_controls()
        self.refresh_window_controls_combobox()
        self.refresh_window_controls_checkbox()

#----- End: Window control settings--------
        
if __name__ == '__main__':
# Fire up the Engines
    Themesettings()
# FIXME : Guaranteed to fail. Arguments mismatch.
