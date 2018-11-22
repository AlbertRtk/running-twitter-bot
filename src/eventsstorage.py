from sqlite3 import connect
from event import Event


class EventsStorage:
    def __init__(self, db_file):
        self.connection = connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS races (
                               name TEXT UNIQUE,
                               date TEXT,
                               place TEXT,
                               distance TEXT,
                               url TEXT
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

    def read(self):
        print('Selecting events from database')
        self.cursor.execute('''SELECT name, date, place, distance, url
                               FROM races''')
        table = self.cursor.fetchall()
        events = []
        for row in table:
            events.append(Event(row[0], row[1], row[2], row[3], row[4]))
        return events

    def remove(self, name):
        print('Removing event from database: ' + name)
        self.cursor.execute('DELETE FROM races WHERE name=?', (name, ))
        self.connection.commit()


if __name__ == '__main__':
    pass
