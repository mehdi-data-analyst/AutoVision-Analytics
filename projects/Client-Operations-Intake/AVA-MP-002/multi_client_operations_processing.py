def validate_client(client_name, original_cost, discount):
    if not isinstance(client_name, str) or len(client_name.strip()) == 0:
        return "Client name must be a non-empty string."
    if isinstance(original_cost, bool) or not isinstance(original_cost, (int, float)):
        return "Original cost must be a number."
    if original_cost <= 0:
        return "Original cost must be greater than 0."
    if isinstance(discount, bool) or not isinstance(discount, (int, float)):
        return "Discount must be a number."
    if discount < 0 or discount > 100:
        return "Discount must be between 0 and 100."
    return True

def calculate_service_cost(original_cost, discount):
    final_cost = original_cost * (1 - discount / 100)
    return final_cost

def process_request(client_request):
    if not isinstance(client_request, list):
        return "Invalid request: must be a list."
    if len(client_request)!= 3:
        return "Invalid request: must have exactly 3 values."

    client_name = client_request[0]
    original_cost = client_request[1]
    discount = client_request[2]

    validation = validate_client(client_name, original_cost, discount)
    if validation!= True:
        return validation

    final_cost = calculate_service_cost(original_cost, discount)
    return f"Client: {client_name}, Final Cost: {final_cost}"

def process_multiple_requests(client_requests):
    if not isinstance(client_requests, list):
        return "Invalid input: client_requests must be a list."

    results = []

    for req in client_requests:
        if not isinstance(req, list):
            results.append("Invalid request: each request must be a list.")
            continue
        if len(req)!= 3:
            results.append("Invalid request: must have exactly 3 values [client_name, original_cost, discount].")
        result = process_request(req)
        results.append(result)

    return results

def generate_operations_summary(processed_requests):
    if not isinstance(processed_requests, list):
        return processed_requests

    total_requests = len(processed_requests)
    processed_count = 0
    failed_count = 0
    total_final_cost = 0

    for res in processed_requests:
        if isinstance(res, str) and res.startswith("Client:"):
            processed_count = processed_count + 1
            parts = res.split("Final Cost:")
            if len(parts) == 2:
                cost_str = parts[1].strip()
                total_final_cost = total_final_cost + float(cost_str)
        else:
            failed_count = failed_count + 1
    if failed_count == 0 and total_requests > 0:
        status = "All operations processed successfully."
    elif processed_count == 0 and total_requests > 0:
        status = "All operations failed."
    else:
        status = "Processing completed."

    summary = (
        "AutoVision Analytics\n"
        "Multi-Client Operations Summary\n"
        "\n"
        f"Total Requests: {total_requests}\n"
        f"Processed Requests: {processed_count}\n"
        f"Failed Requests: {failed_count}\n"
        f"Total Final Cost: {total_final_cost}\n"
        f"Status: {status}"
    )

    return summary
client_requests = [
    ["Volvo", 12000, 10],
    ["BMW", 8500, 5],
    ["Audi", 15000, 15],
    ["", 9000, 10],
    ["Porsche", -5000, 8],
    ["Mercedes-Benz", 20000, 120]
]

results = process_multiple_requests(client_requests)
print("--- Individual Results ---")
for r in results:
    print(r)

print("\n--- Operations Summary ---")
print(generate_operations_summary(results))