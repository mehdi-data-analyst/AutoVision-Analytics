def validate_request_record(request):
    if not isinstance(request, dict):
        return "Invalid request: request must be a dictionary."

    required_fields = {
        "request_id",
        "client_name",
        "original_cost",
        "discount",
        "status",
        "services"
    }

    for field in required_fields:
        if field not in request:
            return f"Missing required field: {field}"

    request_id = request.get("request_id")
    client_name = request.get("client_name")
    original_cost = request.get("original_cost")
    discount = request.get("discount")
    status = request.get("status")
    services = request.get("services")

    if not isinstance(request_id, str) or len(request_id.strip()) == 0:
        return "Invalid request_id: must be a non-empty string."
    if not isinstance(client_name, str) or len(client_name.strip()) == 0:
        return "Invalid client_name: must be a non-empty string."
    if isinstance(original_cost, bool) or not isinstance(original_cost, (int, float)):
        return "Invalid original_cost: must be a number."
    if original_cost <= 0:
        return "Invalid original_cost: must be greater than 0."
    if isinstance(discount, bool) or not isinstance(discount, (int, float)):
        return "Invalid discount: must be a number."
    if discount < 0 or discount > 100:
        return "Invalid discount: must be between 0 and 100."

    allowed_statuses = {"pending", "approved", "rejected"}
    if not isinstance(status, str) or status.lower() not in allowed_statuses:
        return "Invalid status."

    if not isinstance(services, list) or len(services) == 0:
        return "Invalid services: must be a non-empty list."
    for s in services:
        if not isinstance(s, str):
            return "Invalid services: all services must be strings."
        if len(s.strip()) == 0:
            return "Invalid services: service must not be empty."

    return True

def remove_duplicate_services(request):
    services = request.get("services", [])
    seen = set()
    unique = []
    for s in services:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    request["services"] = unique
    return request

def update_request_status(request, new_status):
    if not isinstance(new_status, str):
        return "Invalid status."
    new_status_lower = new_status.lower()
    allowed_statuses = {"pending", "approved", "rejected"}
    if new_status_lower not in allowed_statuses:
        return "Invalid status."
    request.update({"status": new_status_lower})
    return request

def generate_request_report(request):
    order = ["request_id", "client_name", "original_cost", "discount", "status", "services"]
    order_index = {key: i for i, key in enumerate(order)}

    sorted_items = sorted(request.items(), key=lambda kv: order_index.get(kv[0], 999))

    report = "AutoVision Analytics\nClient Request Record\n\n"

    for key, value in sorted_items:
        if key not in order:
            continue
        pretty_key = key.replace("_", " ").title()
        if isinstance(value, list):
            value_str = ", ".join(value)
        else:
            value_str = str(value)
        report += f"{pretty_key}: {value_str}\n"

    return report.strip()

def process_request_record(request, new_status):
    validation_result = validate_request_record(request)
    if validation_result is not True:
        return validation_result

    allowed_statuses = {"pending", "approved", "rejected"}
    if not isinstance(new_status, str) or new_status.lower() not in allowed_statuses:
        return "Invalid status."

    working_copy = {}
    for k, v in request.items(): 
        if k == "services":
            working_copy[k] = v[:] 
        else:
            working_copy[k] = v

    working_copy = remove_duplicate_services(working_copy)
    working_copy = update_request_status(working_copy, new_status)

    if isinstance(working_copy, str):
        return working_copy

    return generate_request_report(working_copy)

client_request = {
    "request_id": "REQ-001",
    "client_name": "Cytiva",
    "original_cost": 7000,
    "discount": 10,
    "status": "pending",
    "services": ["inspection", "repair", "inspection", "software update", "repair"]
}

print("--- Test 1: Valid ---")
print(process_request_record(client_request, "approved"))
print("\nOriginal after Test 1 (should still be pending):", client_request["status"])

print("\n--- Test 2: Invalid new_status - should NOT mutate ---")
print(process_request_record(client_request, "completed"))
print("Original after Test 2 - services should still have duplicates:", client_request["services"])

print("\n--- Test 3: Missing field ---")
print(process_request_record({"request_id": "REQ-002"}, "approved"))