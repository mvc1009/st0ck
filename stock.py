#!/usr/bin/python3

try:
	import sqlite3
	import sys, os
	import gi
	gi.require_version("Gtk", "3.0")
	from gi.repository import Gtk
except:
	print("[!] Error at importing")


class stockWindow(Gtk.Window):
	def __init__(self, cursor):
		self.cursor = cursor

		# Initialize Window
		Gtk.Window.__init__(self, title="Stock Furgoneta", default_width=600, default_height=400)
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

		# Vertical Pane
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(self.vbox)

		# SearchBar
		self.search = Gtk.SearchEntry(valign=Gtk.Align.CENTER)
		self.search.connect("activate", self.searchFunc)
		self.vbox.pack_start(self.search, False, True, 10)

		# Scrolled Label 
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.vbox.pack_start(self.scrolledwindow, True, True, 10)

		self.results = Gtk.Label(label="Sin resultados")
		self.results.set_justify(Gtk.Justification.LEFT)
		self.results.set_selectable(True)
		self.scrolledwindow.add(self.results)

		# Horizontal pane
		self.hbox = Gtk.Box(spacing=10)
		self.vbox.pack_start(self.hbox, False, True, 10)

		# Del Button
		self.delButton = Gtk.Button(label="Elminar", valign=Gtk.Align.CENTER)
		self.delButton.connect("clicked", self.delFunc)
		self.hbox.pack_start(self.delButton, True, True, 10)

		# Add Button
		self.addButton = Gtk.Button(label="Añadir", valign=Gtk.Align.CENTER)
		self.addButton.connect("clicked", self.addFunc)
		self.hbox.pack_start(self.addButton, True, True, 10)

		# ShowALl Button
		self.showallButton = Gtk.Button(label="Mostrar Todo", valign=Gtk.Align.CENTER)
		self.showallButton.connect("clicked", self.searchAllFunc)
		self.hbox.pack_start(self.showallButton, True, True, 10)

	def addFunc(self, widget):
		addWin = addWindow(self.cursor)
		addWin.show_all()
	
	def delFunc(self, widget):
		delWin = delWindow(self.cursor)
		delWin.show_all()

	def searchFunc(self, widget):
		s = self.search.get_text()
		self.search.set_text("")
		result = search(self.cursor, s)
		#self.results.set_text(str(result))
		self.showResults(widget, result)

	def searchAllFunc(self, widget):
		result = searchAll(self.cursor)
		#self.results.set_text(str(result))
		self.showResults(widget, result)

	def showResults(self, widget, result):
		if len(result) <= 0:
			self.results.set_markup("Sin Resultados")

		else:
			printable = "<big><b>ID \t Cantidad</b></big> \n"
			for i in result:
				printable += str(i['id']) + ' \t ' + str(i['amount']) + '\n'

			self.results.set_markup(printable)

class addWindow(Gtk.Window):
	def __init__(self, cursor):

		self.cursor = cursor

		# Initialize Window
		Gtk.Window.__init__(self, title="Añadir", resizable=False)
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(100, 200)

		# Vertical Pane
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.add(self.vbox)

		# Entry
		self.entry = Gtk.Entry()
		self.vbox.pack_start(self.entry, True, True, 0)

		# SpinButton
		adjustment = Gtk.Adjustment(value=0, lower=0, upper=1000000, step_increment=1, page_increment=5, page_size=0)
		self.spinbutton = Gtk.SpinButton(adjustment=adjustment)
		self.vbox.pack_start(self.spinbutton, True, True, 0)

		# Button
		self.addButton = Gtk.Button(label="Añadir")
		self.addButton.connect("clicked", self.doFunc)
		self.vbox.pack_start(self.addButton, True, True, 0)

		# Label
		self.result = Gtk.Label()
		self.result.set_justify(Gtk.Justification.LEFT)
		self.vbox.pack_start(self.result, True, True, 0)


	def doFunc(self, widget):
		product = self.entry.get_text()
		count = self.spinbutton.get_value_as_int()
		result = add(self.cursor, product, count)
		self.result.set_text(result)
		self.entry.set_text("")
		self.spinbutton.set_value(0)

class delWindow(Gtk.Window):
	def __init__(self, cursor):

		self.cursor = cursor

		# Initialize
		Gtk.Window.__init__(self, title="Eliminar")
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(100, 200)

		# Vertical Pane
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.add(self.vbox)

		# Entry
		self.entry = Gtk.Entry()
		self.vbox.pack_start(self.entry, True, True, 0)

		# SpinButton
		adjustment = Gtk.Adjustment(value=0, lower=0, upper=1000000, step_increment=1, page_increment=5, page_size=0)
		self.spinbutton = Gtk.SpinButton(adjustment=adjustment)
		self.vbox.pack_start(self.spinbutton, True, True, 0)

		# Button
		self.addButton = Gtk.Button(label="Eliminar")
		self.addButton.connect("clicked", self.doFunc)
		self.vbox.pack_start(self.addButton, True, True, 0)

		# Label
		self.result = Gtk.Label()
		self.result.set_justify(Gtk.Justification.LEFT)
		self.vbox.pack_start(self.result, True, True, 0)



	def doFunc(self, widget):
		product = self.entry.get_text()
		count = self.spinbutton.get_value_as_int()
		result = delete(self.cursor, product, count)
		self.result.set_text(result)
		self.entry.set_text("")
		self.spinbutton.set_value(0)

def searchAll(cursor):

	sql_command = "SELECT * FROM stock;"
	cursor.execute(sql_command)
	result = cursor.fetchall()
	return parse(result)

def search(cursor, id):
	sql_command = "SELECT * FROM stock WHERE id LIKE '%" + id + "%';"
	cursor.execute(sql_command)
	result = cursor.fetchall()
	if len(result) <= 0:
		print("[!] Not found")
	return parse(result)

def parse(result):
	l = list()
	for i in result:
		d = {'id': str(i[0]), 'amount' : str(i[1])}
		l.append(d)
	l.sort(key=sortFunc)
	return l

def sortFunc(e):
	return e['id']

def delete(cursor, id, count):

	sql_command = "SELECT * FROM stock WHERE id=" + id +";"
	cursor.execute(sql_command)
	result = cursor.fetchall()

	if len(result) > 0:

		if result[0][1] - count <= 0:
			sql_command = "DELETE FROM stock WHERE id=" + id +";"
			cursor.execute(sql_command)
			return "[+] Deleted " + str(id) + " from databse"
		else:
			sql_command = "UPDATE stock SET count=" + str(result[0][1] - count) +" WHERE id=" + id + ";"
			cursor.execute(sql_command)
			return "[+] Deleted " + str(count) + " to " + str(id)
	else:
		return "[!] No results found, entry a valid ID!"


def add(cursor, id, count):

	sql_command = "SELECT * FROM stock WHERE id=" + id +";"
	cursor.execute(sql_command)
	result = cursor.fetchall()

	if len(result) > 0:
		sql_command= "UPDATE stock SET count=" + str(result[0][1] + count) +" WHERE id=" + id + ";"
		cursor.execute(sql_command)
		return "[+] Added " + str(count) + " to " + str(id)

	else:
		sql_command = "INSERT INTO stock (id, count, name) VALUES ('" + str(id) + "', " + str(count) + ", NULL);"
		cursor.execute(sql_command)
		return "[+] ID not found, added to database"

def start():

	print("[+] Setting up the Database")

	# Connecting to furgoDB
	#connection = sqlite3.connect("/Users/oscar/Desktop/MI PC/MATACHANA/ DOTACIÓN FURGO/furgo.db")
	connection = sqlite3.connect("furgo.db")
	return connection

def close(connection):
	connection.close()
	print("\n\n[!] Thanks for using, exiting!")

def main():

	# Setting up the connection with the db
	connection = start()
	cursor = connection.cursor()

	# GUI
	stock = stockWindow(cursor)
	stock.connect("destroy", Gtk.main_quit)
	stock.show_all()
	Gtk.main()

	# Saving changes to the db
	connection.commit()

	# Closing the connection with the db
	close(connection)

if __name__ == "__main__":
	main()