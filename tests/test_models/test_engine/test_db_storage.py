#!/usr/bin/python3
""" Module for testing db storage"""
from console import HBNBCommand
import unittest
from models.state import State
from models.city import City
from models import storage
from os import environ
import MySQLdb
from unittest.mock import patch
from io import StringIO

args = {
    'user': environ.get('HBNB_MYSQL_USER'),
    'passwd': environ.get('HBNB_MYSQL_PWD'),
    'db': environ.get('HBNB_MYSQL_DB'),
    'host': environ.get('HBNB_MYSQL_HOST')
}


@unittest.skipIf(environ.get('HBNB_TYPE_STORAGE') != 'db', "Db only")
class test_db_Storage(unittest.TestCase):
    """Test class for dbstorage"""

    def setUp(self):
        """ Set up test environment """
        self.db_connection = MySQLdb.connect(**args)
        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            self.cursor.close()
            self.db_connection.close()
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 4)

    def test_new(self):
        """ New object is correctly added to db """
        new = State(name="Oklahoma")
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()

    def test_all(self):
        """ __objects is properly returned """
        self.assertIsInstance(storage.all(), dict)

    def test_city_db(self):
        """ Tests creation of city  """
        var = 'SELECT name FROM cities WHERE name = "San Francisco"'
        self.cursor.execute('SELECT count(*) FROM cities')
        length = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        create_state = 'create State name="California" id="1"'
        create_city = 'create City name="San_Francisco" state_id="1"'
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(create_state)
            HBNBCommand().onecmd(create_city)
        self.db_connection = MySQLdb.connect(**args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('SELECT count(*) FROM cities')
        length2 = self.cursor.fetchone()[0]
        self.assertEqual(length2, length + 1)
        self.cursor.execute(var)
        name = self.cursor.fetchone()
        self.assertIn("San Francisco", name)

    def test_create(self):
        """Tests create state"""
        self.cursor.execute('SELECT count(*) FROM states')
        length = self.cursor.fetchone()[0]
        self.cursor.close()
        self.db_connection.close()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Oklahoma"')
        self.db_connection = MySQLdb.connect(**args)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('SELECT count(*) FROM states')
        length2 = self.cursor.fetchone()[0]
        self.assertEqual(length2, length + 1)
