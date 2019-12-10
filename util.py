'''A module storing common utility funcions'''
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

# def modify(sql,keys)

#utility function