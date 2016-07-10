import sys
import datetime

from peewee import *
from collections import OrderedDict

db = SqliteDatabase('diary.db')


class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db

def initialize():
	"""create the database and the table if they don't exit"""
	db.connect()
	db.create_tables([Entry], safe=True)

def menu_loop():
	"""show menu"""
	choice = None

	while choice != 'q':
		print('Enter q to quit.')
		for key, value in menu.items():
			print ('{}) {}'.format(key, value.__doc__))
			#since value is a funtion like add_entry or view_entry
			#value.__doc__ gives a docstring of the value returned by
			#the function.
		choice = raw_input('Action: ').lower().strip('')

		if choice in menu:
			menu[choice]()

def add_entry():
	"""add a new entry"""
	print("Enter your entry. Press ctrl + z and press return when finished.")
	data = sys.stdin.read().strip()

	if data:
		if raw_input("Save Entry? [Yn] ").lower() != 'n':
			Entry.create(content=data)
			print("Saved successfully!")


def view_entries(search_query=None):
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('n) next entry')
        print('q) return to main menu')
        
        next_action = raw_input('Action: [Nq] ').lower().strip()
        if next_action == 'q':
        	break	
   	print('='*len(timestamp))
def search_entries():
    """Search entries for a string."""
    view_entries(raw_input('Search query: '))

def delete_entry(entry):
	"""delete the selected entry"""

menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries)	
])	

if __name__ == '__main__':
	initialize()
	menu_loop()