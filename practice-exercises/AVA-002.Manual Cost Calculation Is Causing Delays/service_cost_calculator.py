def service_cost_calculator(price, discount):

    if not isinstance(price, (int, float)):
        return 'The price should be a number.'
    if not isinstance(discount, (int, float)):
        return 'The discount should be a number.'
    
    if price <= 0:
        return 'The price should be greater than 0.'
    if discount < 0 or discount > 100:
        return 'The discount should be between 0 and 100.'
    
    total_cost = price - (price * discount / 100)

    return total_cost