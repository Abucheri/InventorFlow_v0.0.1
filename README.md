# InventorFlowv0.0.1

This is a stock management module for an inventory system.

## Installation

- Install python 3
```python
pip install -r requirements.txt
```
- You are all set.
- the file `helper_functions.py` has helper functions for formating the dat from the db and the one from the UI. It also has a decorator for Athentication and Authantication session management.
- In `db.yaml`, configure your `database credentials` and `secret_key` to use in the app
- Use `secret_key_generator.py` to generate a secret key that you will copy to `db.yaml`. It has three options to choose from, choose according to you desire.