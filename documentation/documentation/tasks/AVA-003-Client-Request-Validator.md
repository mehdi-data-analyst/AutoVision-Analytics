# AVA-003 — Client Request Validator

## Project Information

**Task ID:** AVA-003

**Department:** Operations

**Role:** Junior Data Analyst

**Status:** Completed

---

# Business Problem

The company receives many client requests every day.

Some requests contain missing information or invalid values that can cause errors in later processing.

The operations team needs a validation system that checks all client information before calculating the service cost.

---

# Objective

Develop a Python validation function that verifies client information before processing a service request.

The program must reject invalid requests and return clear error messages.

---

# Validation Rules

- Client name must be a string.
- Client name cannot be empty.
- Original cost must be numeric.
- Original cost must be greater than zero.
- Discount must be numeric.
- Discount cannot be negative.
- Discount cannot exceed the original cost.

---

# Python Concepts Used

- Functions
- Parameters
- if / elif / else
- isinstance()
- Boolean Logic
- Return Statements
- Input Validation

---

# Expected Result

The validation function prevents invalid requests from entering the system and improves data quality before cost calculation.

---

# Lessons Learned

- How to validate user input.
- Defensive programming techniques.
- Writing reusable validation functions.
- Creating clear error messages.
- Improving software reliability.

---

# Project Status

Completed successfully.

This task became the foundation for later AutoVision Analytics modules.
