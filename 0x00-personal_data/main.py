#!/usr/bin/env python3
"""
Main file
"""
import logging

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
get = cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()