def credit_amount(prev_amount, incoming_amount):
    return prev_amount + incoming_amount


def debit_amount(prev_amount, incoming_amount):
    return prev_amount - incoming_amount


OPERATION_MAPPING = {"credit": credit_amount, "debit": debit_amount}


def calculate_amount(prev_amount, incoming_amount, operation):
    return OPERATION_MAPPING[operation](prev_amount, incoming_amount)


def convert_decimal_to_float(amount):
    return float(str(amount))


def validate_min_balance(amount, min_balance):
    return amount >= min_balance


def validate_amount(amount):
    return amount >= 0


def check_for_missing_params(required_params, req_body):
    missing_params_list = []
    for param in required_params:
        if param not in req_body:
            missing_params_list.append(param)
    return missing_params_list

