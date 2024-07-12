# InventorFlowv0.0.1

This is a stock management module for an inventory system.

## Installation

- Install python 3
```python
pip install -r requirements.txt
```
- You are all set.
- The file `helper_functions.py` has helper functions for formatting the dates from the db and the one from the UI. It also has a decorator for Authentication and Authentication session management.
- In `db.yaml`, configure your `database credentials` and `secret_key` to use in the app
- Use `secret_key_generator.py` to generate a secret key that you will copy to `db.yaml`. It has three options to choose from, choose according to you desire.