def validate_request(request):
    if not isinstance(request, dict):
        raise TypeError("Invalid request: request must be a dictionary.")
    required = ("request_id", "client_name", "status", "vehicles")
    for f in required:
        if f not in request:
            raise ValueError(f"Missing required field: {f}")
    if not isinstance(request.get("request_id"), str) or len(request["request_id"].strip()) == 0:
        raise ValueError("Invalid request_id: must be a non-empty string.")
    if not isinstance(request.get("client_name"), str) or len(request["client_name"].strip()) == 0:
        raise ValueError("Invalid client_name: must be a non-empty string.")
    allowed = {"pending", "approved", "rejected", "completed"}
    status = request.get("status")
    if not isinstance(status, str) or status.strip().lower() not in allowed:
        raise ValueError("Invalid status: must be one of pending, approved, rejected, completed.")
    vehicles = request.get("vehicles")
    if not isinstance(vehicles, list) or len(vehicles) == 0:
        raise ValueError("Invalid vehicles: must be a non-empty list.")

def validate_vehicle(vehicle):
    if not isinstance(vehicle, dict):
        raise TypeError("Invalid vehicle: vehicle must be a dictionary.")
    required = ("vehicle_id", "model", "year", "base_cost", "discount", "services")
    for f in required:
        if f not in vehicle:
            raise ValueError(f"Missing required field: {f}")
    if not isinstance(vehicle.get("vehicle_id"), str) or len(vehicle["vehicle_id"].strip()) == 0:
        raise ValueError("Invalid vehicle_id: must be a non-empty string.")
    if not isinstance(vehicle.get("model"), str) or len(vehicle["model"].strip()) == 0:
        raise ValueError("Invalid model: must be a non-empty string.")
    year = vehicle.get("year")
    if isinstance(year, bool) or not isinstance(year, int):
        raise TypeError("Invalid year: must be an integer.")
    if year < 1990 or year > 2026:
        raise ValueError("Invalid year: must be between 1990 and 2026.")
    base_cost = vehicle.get("base_cost")
    if isinstance(base_cost, bool) or not isinstance(base_cost, (int, float)):
        raise TypeError("Invalid base_cost: must be a number.")
    if base_cost <= 0:
        raise ValueError("Invalid base_cost: must be greater than 0.")
    discount = vehicle.get("discount")
    if isinstance(discount, bool) or not isinstance(discount, (int, float)):
        raise TypeError("Invalid discount: must be a number.")
    if discount < 0 or discount > 100:
        raise ValueError("Invalid discount: must be between 0 and 100.")
    services = vehicle.get("services")
    if not isinstance(services, list) or len(services) == 0:
        raise ValueError("Invalid services: must be a non-empty list.")
    for s in services:
        if not isinstance(s, str) or len(s.strip()) == 0:
            raise ValueError("Invalid services: all services must be non-empty strings.")

def normalize_vehicle(vehicle):
    vehicle["vehicle_id"] = vehicle["vehicle_id"].strip()
    vehicle["model"] = vehicle["model"].strip()
    return vehicle

def remove_duplicate_services(vehicle):
    seen = set()
    unique = []
    for s in vehicle.get("services", []):
        cleaned = s.strip().lower()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique.append(cleaned)
    vehicle["services"] = unique
    return vehicle

def calculate_vehicle_cost(vehicle):
    base = vehicle.get("base_cost")
    disc = vehicle.get("discount")
    final_cost = base * (1 - disc / 100)
    vehicle["final_cost"] = round(float(final_cost), 2)
    vehicle["discount_amount"] = round(float(base - final_cost), 2)
    return vehicle

def process_vehicle(vehicle):
    try:
        validate_vehicle(vehicle)
        working = {}
        for k, v in vehicle.items():
            working[k] = v[:] if k == "services" else v
        working = normalize_vehicle(working)
        working = remove_duplicate_services(working)
        working = calculate_vehicle_cost(working)
        working["processing_result"] = "success"
        return working
    except (TypeError, ValueError) as e:
        return {
            "vehicle_id": vehicle.get("vehicle_id", "UNKNOWN") if isinstance(vehicle, dict) else "UNKNOWN",
            "processing_result": "failed",
            "error": str(e)
        }

def process_fleet_request(request):
    try:
        validate_request(request)
        working = {}
        for k, v in request.items():
            if k == "vehicles":
                working[k] = [dict(veh) if isinstance(veh, dict) else veh for veh in v]
            else:
                working[k] = v
        working["request_id"] = working["request_id"].strip()
        working["client_name"] = working["client_name"].strip()
        working["status"] = working["status"].strip().lower()

        successful_vehicles = []
        failed_vehicles = []
        for veh in working.get("vehicles", []):
            result = process_vehicle(veh)
            if result.get("processing_result") == "success":
                successful_vehicles.append(result)
            else:
                result["request_id"] = working["request_id"]
                result["client_name"] = working["client_name"]
                failed_vehicles.append(result)

        if len(successful_vehicles) == 0 and len(failed_vehicles) > 0:
            return None, failed_vehicles, {
                "request_id": working["request_id"],
                "client_name": working["client_name"],
                "processing_result": "failed",
                "error": f"All {len(failed_vehicles)} vehicles failed validation.",
                "failed_vehicles": failed_vehicles
            }

        total_base = sum(v.get("base_cost", 0) for v in successful_vehicles)
        total_final = sum(v.get("final_cost", 0) for v in successful_vehicles)
        total_disc = sum(v.get("discount_amount", 0) for v in successful_vehicles)

        enriched_request = {
            "request_id": working["request_id"],
            "client_name": working["client_name"],
            "status": working["status"],
            "vehicles": successful_vehicles,
            "vehicle_count": len(successful_vehicles),
            "request_original_cost": round(total_base, 2),
            "request_final_cost": round(total_final, 2),
            "request_discount_amount": round(total_disc, 2),
            "processing_result": "success"
        }
        return enriched_request, failed_vehicles, None

    except (TypeError, ValueError) as e:
        return None, [], {
            "request_id": request.get("request_id", "UNKNOWN") if isinstance(request, dict) else "UNKNOWN",
            "client_name": request.get("client_name", "UNKNOWN") if isinstance(request, dict) else "UNKNOWN",
            "processing_result": "failed",
            "error": str(e)
        }

def process_all_fleet_requests(requests):
    if not isinstance(requests, list):
        raise TypeError("Invalid input: requests must be a list.")

    total_raw_vehicles = 0
    for req in requests:
        if isinstance(req, dict) and isinstance(req.get("vehicles"), list):
            total_raw_vehicles += len(req.get("vehicles"))

    successful_requests = []
    failed_requests = []
    failed_vehicles = []

    for req in requests:
        success_req, fail_vehs, fail_req = process_fleet_request(req)
        if success_req: successful_requests.append(success_req)
        if fail_req: failed_requests.append(fail_req)
        if fail_vehs: failed_vehicles.extend(fail_vehs)

    return successful_requests, failed_requests, failed_vehicles, total_raw_vehicles

def generate_fleet_management_report(successful_requests, failed_requests, failed_vehicles, total_raw_vehicles):
    total_requests = len(successful_requests) + len(failed_requests)
    total_vehicles_success = sum(r.get("vehicle_count", 0) for r in successful_requests)
    total_vehicles_failed = len(failed_vehicles)
    total_vehicles_processed = total_vehicles_success + total_vehicles_failed

    approved = rejected = pending = completed = 0
    total_base = total_final = total_discount = 0
    unique_services = set()
    service_counter = {}
    highest_vehicle = None
    highest_cost = -1
    client_revenue = {}

    for req in successful_requests:
        status = req.get("status")
        if status == "approved": approved += 1
        elif status == "rejected": rejected += 1
        elif status == "pending": pending += 1
        elif status == "completed": completed += 1

        total_base += req.get("request_original_cost", 0)
        total_final += req.get("request_final_cost", 0)
        total_discount += req.get("request_discount_amount", 0)

        client = req.get("client_name")
        client_revenue[client] = client_revenue.get(client, 0) + req.get("request_final_cost", 0)

        for veh in req.get("vehicles", []):
            for svc in veh.get("services", []):
                unique_services.add(svc)
                service_counter[svc] = service_counter.get(svc, 0) + 1
            if veh.get("final_cost", 0) > highest_cost:
                highest_cost = veh.get("final_cost", 0)
                highest_vehicle = veh

    most_requested = "N/A"
    if service_counter:
        max_c = max(service_counter.values())
        most_list = [s for s, c in service_counter.items() if c == max_c]
        most_requested = ", ".join(sorted(most_list))

    highest_client = "N/A"
    highest_client_rev = 0
    if client_revenue:
        highest_client = max(client_revenue, key=lambda k: client_revenue[k])
        highest_client_rev = client_revenue[highest_client]

    highest_vehicle_id_display = highest_vehicle.get('vehicle_id') if highest_vehicle else "N/A"
    highest_cost_display = f"{highest_cost} SEK" if highest_vehicle else "N/A"
    highest_client_display = highest_client if highest_client!= "N/A" else "N/A"
    highest_client_rev_display = f"{highest_client_rev} SEK" if highest_client!= "N/A" else "N/A"

    report = f"""AutoVision Analytics
Fleet Service Operations Summary

Total Requests: {total_requests}
Successful Requests: {len(successful_requests)}
Failed Requests: {len(failed_requests)}

Total Raw Vehicles Received: {total_raw_vehicles}
Total Vehicles Processed (After Request Validation): {total_vehicles_processed}
Successful Vehicles: {total_vehicles_success}
Failed Vehicles: {total_vehicles_failed}

Approved Requests: {approved}
Rejected Requests: {rejected}
Pending Requests: {pending}
Completed Requests: {completed}

Total Base Cost: {total_base} SEK
Total Final Cost: {total_final} SEK
Total Discount Given: {round(total_discount, 2)} SEK

Unique Services: {len(unique_services)}
Services List: {', '.join(sorted(unique_services)) if unique_services else 'None'}
Most Requested Service: {most_requested}

Highest Cost Vehicle: {highest_vehicle_id_display}
Highest Vehicle Final Cost: {highest_cost_display}

Highest Revenue Client: {highest_client_display}
Client Revenue: {highest_client_rev_display}
"""
    return report

empty_requests = [
    {"request_id": "", "client_name": "BMW", "status": "pending", "vehicles": [{"vehicle_id": "VH-001", "model": "X5", "year": 2020, "base_cost": 1000, "discount": 10, "services": ["test"]}] }
]

s, f_req, f_veh, raw = process_all_fleet_requests(empty_requests)
print(generate_fleet_management_report(s, f_req, f_veh, raw))

fleet_requests = [
    {"request_id": "REQ-2001", "client_name": "Volvo Sweden", "status": "pending", "vehicles": [
        {"vehicle_id": "VH-001", "model": "Volvo XC60", "year": 2022, "base_cost": 4500, "discount": 10, "services": [" Inspection ", "oil change", "inspection"]},
        {"vehicle_id": "VH-002", "model": "Volvo EX30", "year": 2024, "base_cost": 6200, "discount": 5, "services": ["software update", "battery inspection"]}
    ]},
    {"request_id": "REQ-2002", "client_name": "Cytiva", "status": "APPROVED", "vehicles": [
        {"vehicle_id": "VH-003", "model": "Volvo XC90", "year": 2020, "base_cost": -5000, "discount": 10, "services": ["inspection"]},
        {"vehicle_id": "VH-004", "model": "Volvo S60", "year": 2021, "base_cost": 7800, "discount": 15, "services": ["Oil Change"]}
    ]},
    {"request_id": "", "client_name": "BMW", "status": "pending", "vehicles": [{"vehicle_id": "VH-010", "model": "BMW X5", "year": 2022, "base_cost": 5000, "discount": 0, "services": ["inspection"]}, {"vehicle_id": "VH-011", "model": "BMW X3", "year": 2023, "base_cost": 6000, "discount": 10, "services": ["repair"]}]}
]

s, f_req, f_veh, raw = process_all_fleet_requests(fleet_requests)
print(generate_fleet_management_report(s, f_req, f_veh, raw))