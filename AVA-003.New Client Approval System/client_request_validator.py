def client_request_validator(client_name, service_cost, discount):

    if not isinstance(client_name, str):
        return 'The client name should be a string.'
    if client_name == '':
        return 'The client name should have a name.'
    
    if not isinstance(service_cost, (int, float)):
        return 'The service cost should be a integer number or a float number.'
    if service_cost <= 0:
        return 'The service cost should be greater than 0.'
    
    if not isinstance(discount, (int, float)):
        return 'The discount should be a number.'
    if discount < 0 or discount > 100:
        return 'The discount should be between 0 and 100.'
    
    final_result = service_cost - (service_cost * discount / 100)

    return final_result 