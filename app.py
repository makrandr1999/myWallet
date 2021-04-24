from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQLdb
from flask_mysqldb import MySQL
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST, MIN_BAL
from utils import *
from schemas import SCHEMAS
from decimal import Decimal
from logger import log_transaction_details

app = Flask(__name__)
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_HOST"] = MYSQL_HOST

db = MySQL(app)


@app.route("/createWallet", methods=["POST"])
def create_wallet():
    if request.method == "POST":
        req_body = request.json
        missing_params = check_for_missing_params(SCHEMAS["createWallet"], req_body)
        if len(missing_params) > 0:
            return (
                jsonify(
                    {
                        "message": "Missing request body param(s): "
                        + " ".join(missing_params)
                    }
                ),
                400,
            )
        mobile_number = req_body["mobileNumber"]
        amount = req_body["amount"]
        truncated_amount = truncate(amount, 2)

        if not validate_min_balance(truncated_amount, int(MIN_BAL)):
            return (
                jsonify(
                    {"message": "Account must maintain minimum balance: " + MIN_BAL}
                ),
                200,
            )

        try:
            cur = db.connection.cursor()
            cur.execute(
                "INSERT INTO user_wallets(mobile_number, balance) VALUES (%s, %s)",
                (mobile_number, truncated_amount),
            )
            db.connection.commit()
            log_transaction_details(
                db, mobile_number, 0, truncated_amount, truncated_amount, "NEW"
            )
            return jsonify({"message": "Successfully created a wallet"}), 200
        except MySQLdb.Error as ex:
            if ex.args[0] == 1062:
                return (
                    jsonify(
                        {
                            "message": "Wallet already exists for user: "
                            + str(mobile_number)
                        }
                    ),
                    200,
                )
            return jsonify({"message": "Error in creating a wallet"}), 400
        finally:
            cur.close()


@app.route("/getBalance", methods=["POST"])
def get_balance():
    if request.method == "POST":
        req_body = request.json
        missing_params = check_for_missing_params(SCHEMAS["getBalance"], req_body)
        if len(missing_params) > 0:
            return (
                jsonify(
                    {
                        "message": "Missing request body param(s): "
                        + " ".join(missing_params)
                    }
                ),
                400,
            )

        mobile_number = req_body["mobileNumber"]
        try:
            cur = db.connection.cursor()
            cur.execute(
                "SELECT balance FROM user_wallets WHERE mobile_number = %s FOR UPDATE",
                (mobile_number,),
            )
            data = cur.fetchone()
            if not data:
                return (
                    jsonify(
                        {
                            "message": "Wallet does not exist for the given user "
                            + str(mobile_number)
                        }
                    ),
                    200,
                )
            return jsonify({"balance": str(data[0])}), 200
        except MySQLdb.Error as ex:
            print(ex)
            return jsonify({"message": "Error in fetching wallet balance"}), 500
        finally:
            cur.close()


@app.route("/creditMoney", methods=["POST"])
def credit_money():
    if request.method == "POST":
        req_body = request.json
        missing_params = check_for_missing_params(SCHEMAS["creditMoney"], req_body)
        if len(missing_params) > 0:
            return (
                jsonify(
                    {
                        "message": "Missing request body param(s): "
                        + " ".join(missing_params)
                    }
                ),
                400,
            )

        mobile_number = req_body["mobileNumber"]
        amount = req_body["amount"]

        try:
            cur = db.connection.cursor()
            cur.execute(
                "SELECT balance FROM user_wallets WHERE mobile_number = %s FOR UPDATE",
                (mobile_number,),
            )
            curr_amount = cur.fetchone()
            if not curr_amount:
                return (
                    jsonify(
                        {
                            "message": "Wallet does not exist for the given user"
                            + str(mobile_number)
                        }
                    ),
                    200,
                )
            curr_amount_float = convert_decimal_to_float(curr_amount[0])
            new_amount = calculate_amount(curr_amount_float, float(amount), "credit")
            truncated_amount = truncate(new_amount, 2)
            print(truncated_amount)
            try:
                cur.execute(
                    "UPDATE user_wallets SET balance = %s WHERE mobile_number = %s",
                    (truncated_amount, mobile_number),
                )
                db.connection.commit()
                log_transaction_details(
                    db,
                    mobile_number,
                    curr_amount_float,
                    truncated_amount,
                    amount,
                    "CREDIT",
                )
                return jsonify({"newBalance": truncated_amount}), 200
            except MySQLdb.Error as ex:
                print(ex)
                return jsonify({"message": "Error in updating wallet balance"}), 500
        except MySQLdb.Error as ex:
            return jsonify({"message": "Error in fetching wallet balance"}), 500
        finally:
            cur.close()


@app.route("/debitMoney", methods=["POST"])
def debit_money():
    if request.method == "POST":
        req_body = request.json
        missing_params = check_for_missing_params(SCHEMAS["debitMoney"], req_body)
        if len(missing_params) > 0:
            return (
                jsonify(
                    {
                        "message": "Missing request body param(s): "
                        + " ".join(missing_params)
                    }
                ),
                400,
            )

        mobile_number = req_body["mobileNumber"]
        amount = req_body["amount"]

        if not validate_amount(amount):
            return jsonify({"message": "Amount must be a positive value"}), 400

        try:
            cur = db.connection.cursor()
            cur.execute(
                "SELECT balance FROM user_wallets WHERE mobile_number = %s FOR UPDATE",
                (mobile_number,),
            )
            curr_amount = cur.fetchone()
            if not curr_amount:
                return (
                    jsonify({"message": "Wallet does not exist for the given user"}),
                    200,
                )
            curr_amount_float = convert_decimal_to_float(curr_amount[0])
            new_amount = calculate_amount(curr_amount_float, float(amount), "debit")
            truncated_amount = truncate(new_amount, 2)
            if not validate_min_balance(truncated_amount, float(MIN_BAL)):
                return (
                    jsonify(
                        {"message": "Account must maintain minimum balance: " + MIN_BAL}
                    ),
                    200,
                )
            try:
                cur.execute(
                    "UPDATE user_wallets SET balance = %s WHERE mobile_number = %s",
                    (truncated_amount, mobile_number),
                )
                db.connection.commit()
                log_transaction_details(
                    db,
                    mobile_number,
                    curr_amount_float,
                    truncated_amount,
                    amount,
                    "DEBIT",
                )
                return jsonify({"newBalance": truncated_amount}), 200
            except MySQLdb.Error as ex:
                print(ex)
                return jsonify({"message": "Error in updating wallet balance"}), 500
        except MySQLdb.Error as ex:
            print(ex)
            return jsonify({"message": "Error in updating wallet balance"}), 500
        finally:
            cur.close()


if __name__ == "__main__":
    app.run()
