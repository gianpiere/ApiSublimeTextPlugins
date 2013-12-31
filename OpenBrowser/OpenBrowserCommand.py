''' 
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	Developer 	: Gianpiere Julio Ramos Bernuy
	Contact		: gianpiere@live.com
	Description : funcion que permite ejecutar en el navegador los routes de codeigniter que selecciones, ademas de
				  buscar las funciones en las clases seleccionadas.

	KeyBindings-user 	:
	{ "keys": ["ctrl+shift+b"], "command": "open_browser","args": {"block":true,"url_basepath":"http://urlbase/"}}

	Settings File 		:
	OpenBrowserStartFiles.sublime-settings
	
	keymap que activa el API. 
-------------------------------------------------------------------------------------------------------------------
''' 
import sublime, sublime_plugin
import webbrowser
import urllib
import re, os, os.path

class OpenBrowserCommand(sublime_plugin.TextCommand):
	
	def run(self,edit,block,url_basepath,author):
		window = sublime.active_window()
		proj_folders = window.folders()
		EXT = '.php'
		view = self.view
		self.settings = sublime.load_settings("OpenBrowserStartFiles.sublime-settings")
		settings_pkg = self.settings.get("Parametros")

		''' ::: SETTINGS LOAD ::: '''
		user_name 	= settings_pkg[0]["Nombre"]
		css_package = settings_pkg[1]["css"]
		js_package 	= settings_pkg[2]["js"]
		url_base 	= settings_pkg[3]["urlbase"]
		controller 	= proj_folders[0]+'/'+settings_pkg[3]["controller"]

		''' ::: THIS LOAD NAME FILE ::: '''
		FileName = self.view.file_name().split('\\')
		
		for region in self.view.sel():
			Text = self.view.substr(region)
			lineRegion = self.view.line(region)
			lineText = self.view.substr(lineRegion)

		view = self.view

		''' ::: TEXT SELECTED ::: '''
		selection_region = view.sel()[0]
		word_region = view.word(selection_region)
		word = view.substr(word_region).strip()
		word = re.sub('[\(\)\{\}\s]', '', word)

		ClassFunctionDiv = word.split('/')

		''' ::: Cargar Clase y seleccionar Funcion dentro de ROUTES.PHP ::: '''
		if str(type(ClassFunctionDiv)) == "<class 'list'>" and len(ClassFunctionDiv) > 1:
			FileClass = controller+'/'+ClassFunctionDiv[0]+EXT
			if FileName[-1] == 'routes.php':
				if os.path.exists(controller) and os.path.exists(FileClass):
					window.open_file(FileClass, sublime.ENCODED_POSITION)
					
					FindText = '@'+ClassFunctionDiv[1]
					self.view.window().run_command("show_overlay", {"overlay": "goto","text":FindText})
					return 0
		elif len(ClassFunctionDiv) == 1:
			if FileName[-1] == 'routes.php':
				if url_basepath == '':
					url_basepath = 'http://localhost/'

				url = url_basepath+Text
				webbrowser.open_new(url)
				return 0
			

		#################################################################################################################
		
			#print(os.path.exists(controller))
			#sublime.message_dialog(sublime.get_clipboard())

		
		for region in self.view.sel():
			t = self.view.substr(region)
			if not region.empty():
				result = self.view.file_name().split('\\')
				
				if str(type(result)) == "<class 'list'>":
					if result[-1] == 'routes.php':
						text = self.view.substr(region)
						url = url_basepath+text
						webbrowser.open_new(url)
					else:
						text = self.view.substr(region)
						subresult = text.split('.')
						if str(type(subresult)) == "<class 'list'>":
							if subresult[-1] == 'css':
								print(result[0])
								window.open_file(result[0]+'\\'+css_package+text, sublime.ENCODED_POSITION)
							elif subresult[-1] == 'js':
								window.open_file(result[0]+'\\'+js_package+text, sublime.ENCODED_POSITION)
							elif subresult[-1] != '':
								self.view.window().run_command("show_overlay", {"overlay": "goto", "text": text})
								#self.view.window().run_command("show_panel",{"panel": "find_in_files","text":'asdasds '+text})
							else:
								print('No File Correct')
						else:
							print('No ha Seleccionado un Archivo Valido [CSS, JS]')
			else:
				url = url_basepath
				webbrowser.open_new(url)


	

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '::' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' 
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '::' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' 