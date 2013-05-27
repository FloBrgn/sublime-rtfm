import sublime
import sublime_plugin
import webbrowser
import sys

def rtfmCpp(selection):
        return "http://www.cplusplus.com/search.do?q="+selection

def rtfmJava(selection):
        if(Pref.java_version != "any"):
            selection = "url:\"/javase/6\" "+selection
        return "http://search.oracle.com/search/search?search_p_main_operator=all&group=Documentation&q="+selection+"&docsets=%2F7%2Fdocs%2Fapi"

def rtfmPython(selection):
        return "http://docs.python.org/3/search.html?q="+selection+"&check_keywords=yes&area=default"


class RtfmDoc(sublime_plugin.TextCommand):

    def run(self,edit):

        #Retrieve highlighted selection if only one
        sels = self.view.sel()
        if len(sels)==1:
            selection = self.view.substr(sels[0])
            if selection == "" : return
        elif len(sels) > 1:
            sublime.status_message( "Too many selection" )
            return
        else:
            sublime.status_message( "Nothing selected" )
            return

        #Retrieve language
        language = self.view.settings().get('syntax')

        #no switch in python :'(
        if language == "Packages/C++/C++.tmLanguage" :
            url = rtfmCpp(selection)
        elif language == "Packages/Java/Java.tmLanguage":
            url = rtfmJava(selection)
        elif language == "Packages/Python/Python.tmLanguage":
            url = rtfmPython(selection)
        else :
            sublime.status_message( "Language not supported" )
            return

        #open browser
        webbrowser.open_new_tab(url);

    def is_visible(self):
        return not Pref.hide_open_documentation        



class RtfmGoogle(sublime_plugin.TextCommand):

    def run(self,edit):

        #Retrieve highlighted selection if only one
        sels = self.view.sel()
        if len(sels)==1:
            selection = self.view.substr(sels[0])
            if selection == "" : return
        elif len(sels) > 1:
            sublime.status_message( "Too many selections (One selection is the maximum I can handle)" )
            return
        else:
            sublime.status_message( "Nothing selected" )
            return

        #Construct query
        url = "https://www.google.fr/search?q="+selection

        #open browser
        webbrowser.open_new_tab(url)

    def is_visible(self):
        return not Pref.hide_search_on_google




def plugin_loaded():
    global settings_base
    global Pref

    settings = sublime.load_settings('Sublime RTFM.sublime-settings')
    if int(sublime.version()) >= 2174:
        settings_base = sublime.load_settings('Preferences.sublime-settings')
    else:
        settings_base = sublime.load_settings('Base File.sublime-settings')

    class Pref:
        def load(self):
            Pref.hide_open_documentation            = bool(settings.get('hide_open_documentation', "false"))
            Pref.hide_search_on_google              = bool(settings.get('hide_search_on_google', "false"))

            Pref.java_version                       = settings.get('java_version',"any")


    Pref = Pref()
    Pref.load()

    settings.add_on_change('reload', lambda:Pref.load())
    settings_base.add_on_change('sublime-rtfm-reload', lambda:Pref.load())


# Backwards compatibility with Sublime 2.  sublime.version isn't available at module import time in Sublime 3.
if sys.version_info[0] == 2:
    plugin_loaded()        
