# myWallet

myWallet is a simple wallet transaction system that lets users create a new Wallet, check their balance and credit/debit money from their wallet. 
It also keeps track of all the user transaction details.


## Requirements
* Flask 1.1.2
* Python 3.6.9
* mysql Ver 14.14 Distrib 5.7.33


## Installation

* Clone or download this repository into your working directory.
* Create a virtual environment and activate it.
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```
* Upgrade to the latest version of pip.
```bash
python -m pip install --upgrade pip
```
* Install Flask and other dependencies using requirements.txt .
```bash
pip install -r requirements.txt
```
* Run the myWallet_queries.sql file
* Create a .env file and configure MIN_BAL(minimum balance) and other environment variables mentioned in settings.py
* Import myWallet.postman_collection.json into Postman for API reference (with examples).

## Usage
* Navigate to the directory of your project folder and run the following command to start a development server.

```bash
FLASK_APP=app.py FLASK_ENV=development flask run
```
* Call the different APIs using Postman or the CURL command.
* All transactions are logged in transaction_details table.
