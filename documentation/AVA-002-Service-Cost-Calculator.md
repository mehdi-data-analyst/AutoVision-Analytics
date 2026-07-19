# AVA-002 — Service Cost Calculator

## Project Information

**Task ID:** AVA-002

**Department:** Finance

**Role:** Junior Data Analyst

**Status:** Completed

---

## Business Problem

The finance department needs a reliable way to calculate the final service cost after applying a customer discount.

---

## Objective

Develop a Python function that calculates the final service cost using the original cost and the discount percentage.

---

## Business Rules

- The original service cost must be provided.
- A discount is applied as a percentage.
- The final service cost cannot be calculated without a valid original cost.

---

## Solution

A dedicated Python function was created to calculate the final service cost.

The calculation follows this formula:

Final Cost = Original Cost − (Original Cost × Discount / 100)

---

## Python Concepts Used

- Functions
- Variables
- Arithmetic Operators
- Return Statement

---

## Lessons Learned

This task showed how business calculations can be separated from validation logic.

Keeping the calculation inside its own function makes the code easier to reuse, maintain, and test.

---

## Future Improvements

- Support multiple currencies.
- Add tax calculation.
- Support promotional discounts.

---

## Next Task

AVA-003 — Client Request Validator
