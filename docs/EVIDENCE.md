# Evidence — Stage 1 (Clean Code & Architecture)

This document provides concrete evidence for the Stage 1 requirements.
All references include file paths and specific responsibilities to enable fast review.

---

## 1. Clean Architecture & Layered Design

**Evidence**
- Domain logic is fully isolated from the API layer.
- Dependency direction is strictly `api → domain`.

**Files**
- `app/domain/gilded_rose.py`
- `app/api/handlers.py`

**Notes**
- The domain module has no imports from `api`, frameworks, or IO.
- The API layer only performs data mapping and delegates behavior to the domain.

---

## 2. Refactored Domain Logic (Clean Code)

**Evidence**
- Deeply nested conditionals were replaced with small, intention-revealing functions.
- Each function represents a single business rule.

**Files & Examples**
- `update_normal_item` — normal item degradation  
  (`app/domain/gilded_rose.py`)
- `update_aged_brie` — increasing quality rule
- `update_backstage` — tiered quality increase rules
- `handle_expired_item` — centralized expired-item behavior

**Notes**
- Each rule is independently readable and testable.
- No dispatch table was introduced to preserve explicit control flow and clarity.

---

## 3. Explicit Invariants

**Evidence**
- Invariant behavior for special items is enforced explicitly.

**Files**
- `app/domain/gilded_rose.py`

**Examples**
- Sulfuras items short-circuit update logic and never change:
  ```python
  if item.name == SULFURAS:
      continue


## 4. Coverage Report 

=========================================================== tests coverage 
__________________________________________ coverage: platform linux, python 3.13.7-final-0 ___________________________________________


Name                                                Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------------------------
app/__init__.py                                         0      0      0      0   100%
app/api/__init__.py                                     0      0      0      0   100%
app/api/handler.py                                      9      2      0      0    78%
app/domain/gilded_rose.py                              55      2     24      2    95%
kata/gilded_rose/after/__init__.py                      0      0      0      0   100%
kata/gilded_rose/after/gilded_rose.py                  55      2     24      2    95%
kata/gilded_rose/before/gilded_rose.py                 36     17     34      7    40%
kata/gilded_rose/before/tests/__init__.py               0      0      0      0   100%
kata/gilded_rose/before/tests/conftest.py               0      0      0      0   100%
kata/gilded_rose/before/tests/test_gilded_rose.py      10      1      2      1    83%
tests/unit/test_api_handler.py                         42      0      0      0   100%
tests/unit/test_gilded_rose.py                         37      0      0      0   100%
-------------------------------------------------------------------------------------
TOTAL                                                 244     24     84     12    84%

========================================================= 21 passed in 0.05s 