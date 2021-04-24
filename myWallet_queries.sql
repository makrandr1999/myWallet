DROP TABLE IF EXISTS user_wallets;
DROP TABLE IF EXISTS transaction_details;

CREATE TABLE user_wallets (
	id bigint(20) NOT NULL AUTO_INCREMENT,
	mobile_number varchar(15) NOT NULL UNIQUE,
	balance decimal(15,2) NOT NULL,
	is_deleted tinyint(1) NOT NULL DEFAULT '0',
	creation_date dateTime,
	last_update dateTime,
	PRIMARY KEY(id)
);


DELIMITER //
CREATE TRIGGER user_wallets_insert_trigger BEFORE INSERT ON myWallet.user_wallets
FOR EACH ROW 
BEGIN
	SET NEW.creation_date = NOW();
	SET NEW.last_update = NOW();
END//
DELIMITER ;


DELIMITER //
CREATE TRIGGER user_wallets_update_trigger BEFORE UPDATE ON myWallet.user_wallets
FOR EACH ROW 
BEGIN
	SET NEW.last_update = NOW();
END//
DELIMITER ;

CREATE TABLE transaction_details (
	id bigint(20) NOT NULL AUTO_INCREMENT,
	mobile_number varchar(15) NOT NULL,
	prev_balance decimal(15,2) NOT NULL,
	curr_balance decimal(15,2) NOT NULL,
	amount decimal(15,2) NOT NULL,
	transaction_type varchar(15) NOT NULL,
	is_deleted tinyint(1) NOT NULL DEFAULT '0',
	creation_date dateTime,
	PRIMARY KEY(id)
);


DELIMITER //
CREATE TRIGGER transaction_details_insert_trigger BEFORE INSERT ON myWallet.transaction_details
FOR EACH ROW 
BEGIN
	SET NEW.creation_date = NOW();
END//
DELIMITER ;

