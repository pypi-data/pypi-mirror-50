# Checks that values passed as method parameters match the typehinted value.


async def check_dict(data):
    if not isinstance(data, dict):
        raise ValueError("'data' must be a dictionary.")


async def check_vals(after, limit):
    if after < 0:
        raise ValueError("'after' must be greater than or equal to 0.")
    elif limit < 1 or limit > 100:
        raise ValueError("'limit' must be between 1 and 100.")


async def check_int(val):
    try:
        int(val)
    except ValueError:
        raise ValueError("Value must be an integer.")
