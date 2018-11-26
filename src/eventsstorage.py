""" 2018 by Albert Ratajczak
    EventsStorage - class with storage (database) for Event instances
"""
from sqlite3 import connect
from event import Event
from datetime_functions import date_with_dots
from datetime import datetime


class EventsStorage:
    def __init__(self, db_file):
        self.connection = connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS races (
                               name TEXT,
                               date TEXT,
                               place TEXT,
                               distance TEXT,
                               url TEXT UNIQUE
                               )'''
                            )

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def store(self, events):
        """
        :param events: list of class Event instances
        """
        print('Inserting events into database')
        insert = []
        for e in events:
            insert.append(e.to_tuple())
        self.cursor.executemany('''INSERT OR REPLACE INTO races
                                   VALUES (?, ?, ?, ?, ?)''', insert)
        self.connection.commit()

    def read(self, event_date=None):
        print('Selecting events from database')
        if event_date is None:
            self.cursor.execute('''SELECT name, date, place, distance, url
                                   FROM races''')
        else:
            self.cursor.execute('''SELECT name, date, place, distance, url
                                   FROM races WHERE date=?''', (event_date, ))
        table = self.cursor.fetchall()
        events = []
        for row in table:
            events.append(Event(row[0], datetime.strptime(row[1], '%Y-%m-%d'),
                                row[2], row[3], row[4]))
        return events

    def remove(self, event):
        print('Removing event from database: ' + event.name)
        self.cursor.execute('DELETE FROM races WHERE url=?', (event.url, ))
        self.connection.commit()


if __name__ == '__main__':
    pass
