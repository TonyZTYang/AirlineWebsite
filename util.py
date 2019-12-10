'''A module storing funcions for database operations'''
from config import db

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

# def modify(sql,keys)