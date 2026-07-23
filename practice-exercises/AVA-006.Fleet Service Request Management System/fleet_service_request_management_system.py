def validate_request_record(request):
    if not isinstance(request, dict):
        raise TypeError("Invalid request: request must be a dictionary.")

    required_fields = {"request_id", "client_name", "original_cost", "discount", "status", "services"}
    for field in required_fields:
        if field not in request:
            raise ValueError(f"Missing required field: {field}")

    request_id = request.get("request_id")
    client_name = request.get("client_name")
    original_cost = request.get("original_cost")
    discount = request.get("discount")
    status = request.get("status")
    services = request.get("services")

    if not isinstance(request_id, str) or len(request_id.strip()) == 0:
        raise ValueError("Invalid request_id: must be a non-empty string.")
    if not isinstance(client_name, str) or len(client_name.strip()) == 0:
        raise ValueError("Invalid client_name: must be a non-empty string.")

    if isinstance(original_cost, bool) or not isinstance(original_cost, (int, float)):
        raise TypeError("Invalid original_cost: must be a number.")
    if original_cost <= 0:
        raise ValueError("Invalid original_cost: must be greater than 0.")

    if isinstance(discount, bool) or not isinstance(discount, (int, float)):
        raise TypeError("Invalid discount: must be a number.")
    if discount < 0 or discount > 100:
        raise ValueError("Invalid discount: must be between 0 and 100.")

    allowed_statuses = {"pending", "approved", "rejected", "completed"}
    if not isinstance(status, str) or status.strip().lower() not in allowed_statuses:
        raise ValueError(f"Invalid status: must be one of Pending, Approved, Rejected, Completed.")

    if not isinstance(services, list) or len(services) == 0:
        raise ValueError("Invalid services: must be a non-empty list.")
    for s in services:
        if not isinstance(s, str) or len(s.strip()) == 0:
            raise ValueError("Invalid services: all services must be non-empty strings.")

    return "Validation passed."

def normalize_request_record(request):
    if "request_id" in request and isinstance(request["request_id"], str):
        request["request_id"] = request["request_id"].strip()
    if "client_name" in request and isinstance(request["client_name"], str):
        request["client_name"] = request["client_name"].strip()
    if "status" in request and isinstance(request["status"], str):
        request["status"] = request["status"].strip().lower()

    if "services" in request and isinstance(request["services"], list):
        normalized_services = []
        for s in request["services"]:
            if isinstance(s, str):
                normalized_services.append(s.strip())
        request["services"] = normalized_services

    return request

def calculate_final_cost(request):
    original_cost = request.get("original_cost")
    discount = request.get("discount")
    final_cost = original_cost * (1 - discount / 100)
    return round(float(final_cost), 2)

def generate_request_summary(request):
    final_cost = request.get("final_cost")
    if final_cost is None:
        final_cost = calculate_final_cost(request)

    services = request.get("services", [])
    services_list = [f"- {s}" for s in services]
    services_str = "\n".join(services_list)

    display_status = request.get('status', '').strip().title()

    summary = f"""====================================
AutoVision Analytics
SERVICE REQUEST SUMMARY

Request ID : {request.get('request_id')}
Client : {request.get('client_name')}
Status : {display_status}

Services :
{services_str}

Original Cost : {request.get('original_cost')} SEK
Discount : {request.get('discount')} %
Final Cost : {final_cost} SEK
===================================="""
    return summary

def process_request(request):
    try:
        validate_request_record(request)

        working = {}
        for k, v in request.items():
            working[k] = v[:] if k == "services" else v

        working = normalize_request_record(working)

        final_cost = calculate_final_cost(working)
        working["final_cost"] = final_cost

        return generate_request_summary(working)

    except (TypeError, ValueError) as e:
        return f"Error: {str(e)}"

print("--- Test 1: status ---")
req_from_mp003 = {
    "request_id": "REQ-1001",
    "client_name": "Volvo Sweden",
    "original_cost": 4200,
    "discount": 15,
    "status": "pending", 
    "services": ["Oil Change", "Brake Inspection"]
}
print(process_request(req_from_mp003))

print("\n--- Test 2: ---")
req_with_spaces = {
    "request_id": " REQ-1002 ",
    "client_name": " Volvo Sweden ",
    "original_cost": 4200,
    "discount": 15,
    "status": " APPROVED ",
    "services": [" Oil Change ", "Brake Inspection"]
}
print(process_request(req_with_spaces))

print("\n--- Test 3: Invalid Status ---")
print(process_request({**req_from_mp003, "status": "In Progress"}))