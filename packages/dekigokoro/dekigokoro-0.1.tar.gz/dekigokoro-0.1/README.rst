dekigokoro.py
=========================================

.. Links to non-Python resources

.. _Dekigokoro: https://dekigokoro.io
.. _documentation: https://dekigokoro.io/docs#subkeys
.. _amy: https://amy.gg
.. _subkey: https://dekigokoro.io/docs#subkeys
.. _here: https://dekigokoro.broman.dev/index.html

.. Python classes

.. _str: https://docs.python.org/3/library/stdtypes.html#str
.. _int: https://docs.python.org/3/library/functions.html#int
.. _dict: https://docs.python.org/3/library/stdtypes.html#dict
.. _list: https://docs.python.org/3/library/stdtypes.html#list
.. _coroutines: https://docs.python.org/3/library/asyncio-task.html
.. _ClientResponseError: https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponseError


`Dekigokoro`_ (created by `amy`_) is a simple API designed for managing economy, experience points, leaderboards, and arbitary user data. 

Features:

- Pythonic async/await syntax
- Currency / balances
- Levels / experience
- Leaderboards
- Arbitary user data
- Subkeys (explained below)

Subkeys
-------
From the Dekigokoro `documentation`_:
    Subkeys are conceptually easy, and are best explained with an example.
    Suppose you’re making an RPG-style game.
    Your players might have a balance of gold or other currency, some skills that they’re grinding up, … dekigokoro makes it easy for you to partition these out into sub-groups via subkeys.
    A player could have an overall experience total / level, and they could also have per-skill experience totals, grouped by subkey.
    In this RPG example, a “swords” or “mining” skill would be the subkey.

Documentation
=============
Documentation can be found `here`_.

Getting Started
===============
Install with pip:

``pip install dekigokoro-py``

Quickstart
==========
.. code-block:: python 

    import dekigokoro
    import asyncio 

    client = Client("token")
    async def main():
        await client.add_balance("player", 10)
        await client.set_balance("player2", 50)
    
    l = asyncio.get_event_loop()
    l.run_until_complete(main())
