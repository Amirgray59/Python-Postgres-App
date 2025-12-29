This document explains how clean-code principles were applied
during the Gilded Rose refactor, with direct references to the code.

---

## 1. Meaningful Names

Functions are named after business rules, not implementation details.

Examples:
- `update_aged_brie`
- `update_backstage`
- `handle_expired_item`

The behavior of each function is clear without reading its body.

---

## 2. Small, Focused Functions

Each function has a single responsibility and is intentionally small.

Examples:
- `increase_quality`
- `decrease_sell_in`
- `update_normal_item`

Most functions are only a few lines long and easy to test in isolation.

---

## 3. Reduced Conditional Complexity

The original nested conditionals were replaced with:
- Guard clauses
- Explicit rule functions
- Centralized expiration handling

Example:

```python
if item.name == SULFURAS:
    continue
```