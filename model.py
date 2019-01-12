import sqlite3

# returns a row from a query
def query_db(query, args=(), one=False):
    """Query the database, and returns a list of rows."""
    cur = get_db().execute(query, args)
    r_v = cur.fetchall()
    cur.close()
    return (r_v[0] if r_v else None) if one else r_v


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary."""
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    """Open a new database connection."""
    conn = sqlite3.connect(insta485.app.config['DATABASE_FILENAME'])
    # Foreign keys have to be enabled per-connection.  This is an sqlite3
    # backwards compatibility thing.
    conn.execute("PRAGMA foreign_keys = ON")

    # if not hasattr(flask.g, 'sqlite_db'):
    #     flask.g.sqlite_db = sqlite3.connect(
    #         insta485.app.config['DATABASE_FILENAME'])
    #     flask.g.sqlite_db.row_factory = dict_factory
    return conn


# @insta485.app.teardown_appcontext
# def close_db(error):
#     # pylint: disable=unused-argument
#     """Close the database at the end of a request."""
#     if hasattr(flask.g, 'sqlite_db'):
#         flask.g.sqlite_db.commit()
#         flask.g.sqlite_db.close()
