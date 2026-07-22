def validate_request_record(request):
    if not isinstance(request, dict):
        return "Invalid request: request must be a dictionary."

    required_fields = {"request_id", "client_name", "original_cost", "discount", "status", "services"}
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
    if isinstance(original_cost, bool) or not isinstance(original_cost, (int, float)) or original_cost <= 0:
        return "Invalid original_cost: must be a number greater than 0."
    if isinstance(discount, bool) or not isinstance(discount, (int, float)) or discount < 0 or discount > 100:
        return "Invalid discount: must be between 0 and 100."

    allowed_statuses = {"pending", "approved", "rejected"}
    if not isinstance(status, str) or status.strip().lower() not in allowed_statuses:
        return "Invalid status."

    if not isinstance(services, list) or len(services) == 0:
        return "Invalid services: must be a non-empty list."
    for s in services:
        if not isinstance(s, str) or len(s.strip()) == 0:
            return "Invalid services: all services must be non-empty strings."

    return True

def clean_request_record(request):
    services = request.get("services", [])
    seen = set()
    unique = []
    for s in services:
        cleaned = s.strip().lower()
        if cleaned not in seen:
            seen.add(cleaned)
            unique.append(cleaned)
    request["services"] = unique
    return request

def normalize_request_record(request):
    if "status" in request and isinstance(request["status"], str):
        request["status"] = request["status"].strip().lower()
    if "client_name" in request and isinstance(request["client_name"], str):
        request["client_name"] = request["client_name"].strip()
    if "request_id" in request and isinstance(request["request_id"], str):
        request["request_id"] = request["request_id"].strip()
    return request

def enrich_request_record(request):
    original_cost = request.get("original_cost")
    discount = request.get("discount")
    final_cost = original_cost * (1 - discount / 100)
    request["final_cost"] = round(final_cost, 2)
    request["discount_amount"] = round(original_cost - final_cost, 2)
    return request

def process_all_records(requests):
    if not isinstance(requests, list):
        return "Invalid input: requests must be a list."

    valid_records = []
    invalid_records = []

    for req in requests:
        validation = validate_request_record(req)
        if validation is not True:
            invalid_records.append({
                "request_id": req.get("request_id", "UNKNOWN") if isinstance(req, dict) else "UNKNOWN",
                "processing_result": "failed",
                "error": validation
            })
            continue

        working = {}
        for k, v in req.items():
            working[k] = v[:] if k == "services" else v

        working = clean_request_record(working)
        working = normalize_request_record(working)
        working = enrich_request_record(working)
        working["processing_result"] = "success"
        valid_records.append(working)

    return valid_records, invalid_records

def generate_management_report(valid_records, invalid_records, total_requests):
    approved = rejected = pending = 0
    total_original = 0
    total_discount = 0
    total_final = 0
    unique_services_set = set()
    service_counter = {}

    for rec in valid_records:
        status = rec.get("status")
        if status == "approved":
            approved += 1
        elif status == "rejected":
            rejected += 1
        elif status == "pending":
            pending += 1

        total_original += rec.get("original_cost", 0)
        total_final += rec.get("final_cost", 0)
        total_discount += rec.get("discount_amount", 0)

        for service in rec.get("services", []):
            unique_services_set.add(service)
            service_counter[service] = service_counter.get(service, 0) + 1

    num_unique_services = len(unique_services_set)

    most_requested = "N/A"
    most_requested_list = []
    if service_counter:
        max_count = max(service_counter.values())
        most_requested_list = [s for s, c in service_counter.items() if c == max_count]
        most_requested = ", ".join(sorted(most_requested_list))

    report = f"""AutoVision Analytics
Operations Summary

Total Requests: {total_requests}
Valid Requests: {len(valid_records)}
Invalid Requests: {len(invalid_records)}
Approved Requests: {approved}
Rejected Requests: {rejected}
Pending Requests: {pending}
Total Original Cost: {total_original}
Total Final Cost: {total_final}
Total Discount Given: {round(total_discount, 2)}
Number of Unique Services: {num_unique_services}
Unique Services: {', '.join(sorted(unique_services_set)) if unique_services_set else 'None'}
Most Requested Service: {most_requested}
"""

    kpis = {
        "total_requests": total_requests,
        "valid_requests": len(valid_records),
        "invalid_requests": len(invalid_records),
        "approved": approved,
        "rejected": rejected,
        "pending": pending,
        "total_original": total_original,
        "total_final": total_final,
        "total_discount": round(total_discount, 2),
        "unique_services_count": num_unique_services,
        "most_requested_service": most_requested,
        "most_requested_service_list": most_requested_list
    }

    return report, kpis, valid_records

requests = [
    {"request_id": "REQ-001", "client_name": "Volvo", "original_cost": 12000, "discount": 10, "status": " APPROVED ", "services": ["Inspection", "repair", " inspection "]},
    {"request_id": "REQ-002", "client_name": "Cytiva", "original_cost": 7000, "discount": 10, "status": "pending", "services": ["inspection", "repair", "inspection", "software update"]},
    {"request_id": "REQ-003", "client_name": "Ericsson", "original_cost": 15000, "discount": 15, "status": "Rejected", "services": ["repair", "repair"]},
    {"request_id": "REQ-004", "client_name": "", "original_cost": 9000, "discount": 10, "status": "pending", "services": ["inspection"]},
    {"request_id": "REQ-005", "client_name": "BMW", "original_cost": 8500, "discount": 5, "status": "approved", "services": ["software update", "inspection"]},
]

valid, invalid = process_all_records(requests)
report, kpis, enriched = generate_management_report(valid, invalid, len(requests))

print(report)
print(kpis)