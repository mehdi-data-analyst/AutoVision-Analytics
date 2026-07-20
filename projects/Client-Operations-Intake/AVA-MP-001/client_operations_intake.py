# Client information validation.
def validate_client(client_name, original_cost, discount):
    if not isinstance(client_name, str):
        return 'The client name should be a string.'
    if client_name == '':
        return 'The client name should have a name.'
    if not isinstance(original_cost, (int, float)):
        return 'The service cost should be a integer number or a float number.'
    if original_cost <= 0:
        return 'The service cost should be greater than 0.'
    if not isinstance(discount, (int, float)):
        return 'The discount should be a number.'
    if discount < 0 or discount > 100:
        return 'The discount should be between 0 and 100.'

    return "Validation passed."

# No any validation.
def calculate_service_cost(original_cost, discount):
    final_cost = original_cost - (original_cost * discount / 100)
    return final_cost

# Doing validation.
def process_request(client_name, original_cost, discount):
    validation_message = validate_client(client_name, original_cost, discount)
    if validation_message != "Validation passed.":
        return validation_message

    final_cost = calculate_service_cost(original_cost, discount)

    report = (
        "====================================\n"
        "AutoVision Analytics\n"
        "Client Request Summary\n"
        "====================================\n"
        f"Client : {client_name}\n"
        f"Original Cost : {original_cost} SEK\n"
        f"Discount : {discount} %\n"
        f"Final Cost : {final_cost} SEK\n"
        "Status : Approved"
    )

    return report