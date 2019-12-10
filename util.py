'''A module storing common utility funcions'''
from flask import Flask, render_template, request, session, url_for, redirect
from config import db

#database functions
def fetchall(sql,keys):
    """sql search: fetch all result
    
    Arguments:
        sql {string} -- the prepared query
        keys {tuple} -- a tuple of corresponding search keys
    
    Returns:
        list -- list of dic storing query result
    """
    with db:
        cur = db.cursor()
        cur.execute(sql,keys)
        result = cur.fetchall()
    return result

def fetchone(sql,keys):
    """sql search: fetch one result
    
    Arguments:
        sql {string} -- the prepared query
        keys {tuple} -- a tuple of corresponding search keys
    
    Returns:
        list -- list of dic storing query result
    """
    with db:
        cur = db.cursor()
        cur.execute(sql,keys)
        result = cur.fetchone()
    return result

def modify(sql,keys):

        with db:
            cur = db.cursor()
            cur.execute(sql,keys)
        db.commit()

#utility function
def doorman(lock):
    username = session.get('username')
    usertype = session.get('usertype')

    if not username or not usertype :
        return False
    if usertype != lock:
        return False
    sql = 'select * from '+ usertype + ' where email = %s'
    key = (username)
    data = fetchone(sql,key)
    if not data:
        return False
    else:
        return True