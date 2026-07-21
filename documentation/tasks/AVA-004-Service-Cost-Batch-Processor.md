# AVA-004 — Service Cost Batch Processor

## Task Information

**Task ID:** AVA-004  
**Department:** Operations  
**Role:** Junior Data Analyst  
**Status:** Completed  

## Business Problem

The AutoVision Analytics Operations team receives multiple service costs that must be validated and combined into one total value.

Calculating these costs manually is repetitive and may lead to mistakes. The team needs a reusable Python function that can process several service costs safely and consistently.

## Objective

Create a Python function that:

- Accepts a list of service costs.
- Validates the input collection.
- Checks every cost individually.
- Rejects invalid values.
- Calculates and returns the total service cost.

## Function

```python
calculate_total_cost(service_costs)