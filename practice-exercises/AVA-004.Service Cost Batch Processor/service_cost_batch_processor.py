def calculate_total_cost(service_costs):
    if not isinstance(service_costs, list):
        return 'The service costs should be a list.'
    
    final_costs = 0
    for service_cost in service_costs:
        if isinstance(service_cost, bool) or not isinstance(service_cost, (int, float)):
            return 'The service_cost should be a number.'
        if service_cost <= 0:
            return 'The service cost should be greater then 0.'
        final_costs += service_cost
    return final_costs