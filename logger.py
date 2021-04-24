from flask_mysqldb import MySQLdb


def log_transaction_details(
    db, mobile_number, prev_balance, curr_balance, amount, transaction_type
):
    try:
        cur = db.connection.cursor()
        cur.execute(
            "INSERT INTO transaction_details(mobile_number, prev_balance, curr_balance, amount, transaction_type) VALUES (%s, %s, %s, %s, %s)",
            (mobile_number, prev_balance, curr_balance, amount, transaction_type),
        )
        db.connection.commit()
        return
    except MySQLdb.Error as ex:
        return
    finally:
        cur.close()

