#!/usr/bin/python3
"""console testing module"""
from io import StringIO
import sys
import unittest
from unittest.mock import patch
import os
from models.engine.file_storage import FileStorage
from datetime import datetime
from models.base_model import BaseModel
from console import HBNBCommand
import MySQLdb

fs = FileStorage()
args = {
    'user': os.environ.get('HBNB_MYSQL_USER'),
    'passwd': os.environ.get('HBNB_MYSQL_PWD'),
    'db': os.environ.get('HBNB_MYSQL_DB'),
    'host': os.environ.get('HBNB_MYSQL_HOST')
}


class TestConsole(unittest.TestCase):
    """A unittesting class for console"""

    @unittest.skipIf(os.environ.get('HBNB_TYPE_STORAGE') == 'db', "Not db")
    def test_create(self):
        if os.path.exists(fs._FileStorage__file_path):
            os.remove(fs._FileStorage__file_path)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            state_id = f.getvalue()[:-1]
        with open(fs._FileStorage__file_path, 'r') as fd:
            self.assertIn(state_id, fd.read())

    @unittest.skipIf(os.environ.get('HBNB_TYPE_STORAGE') != 'db', "DB only")
    def test_create2(self):
        """Tests create state"""
        self.db_connection = MySQLdb.connect(**args)
        self.cursor = self.db_connection.cursor()
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

if __name__ == "__main__":
    unittest.main()
