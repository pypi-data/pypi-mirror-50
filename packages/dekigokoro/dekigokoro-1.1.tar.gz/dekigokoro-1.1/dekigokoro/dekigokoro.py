import aiohttp
import utils.values as values


class Client:
    r"""
    The base client class for Dekigokoro.

    token: `str`_
        The token used to authorise with the API. This will be added as the
        Authorization header for all requests.
        You can obtain this token by creating a `Dekigokoro`_ account.

    All class methods are `coroutines`_.
    """

    def __init__(self, token: str):
        self._base_url = "https://dekigokoro.io/api/v1"
        self._headers = {"Authorization": token, "Content-Type": "application/json"}

    # Balance
    async def get_balance(self, player: str, *, subkey: str = "") -> int:
        """
        Gets a players balance.

        player: `str`_
            The player whose balance to set.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/currency/{player}/{subkey}",
                headers=self._headers,
                raise_for_status=True,
            )
            bal = await r.json()
            return int(bal["balance"])

    async def set_balance(self, player: str, balance: int, *, subkey: str = "") -> int:
        """
        Sets a players balance.

        player: `str`_
            The player whose balance to set.

        balance: `int`_
            The player's new balance.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The balance value provided was not an integer.
        """
        await values.check_int(balance)
        async with aiohttp.ClientSession() as session:
            await session.put(
                f"{self._base_url}/currency/{player}/{subkey}",
                headers=self._headers,
                json={"balance": str(balance)},
                raise_for_status=True,
            )

    async def add_balance(self, player: str, balance: int, *, subkey: str = "") -> int:
        """
        Adds to a player's balance.

        player: `str`_
            The player whose balance to add to.

        balance: `int`_
            The amount to add to the player's balance.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The balance value provided was not an integer.
        """
        currentbal = await self.get_balance(player, subkey=subkey)
        return await self.set_balance(player, currentbal + balance, subkey=subkey)

    async def subtract_balance(
        self, player: str, balance: int, *, subkey: str = ""
    ) -> int:
        """
        Subtracts from a player's balance.

        player: `str`_
            The player whose balance to subtract from.

        balance: `int`_
            The amount to subtract from the players balance.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The balance value provided was not an integer.
        """
        currentbal = await self.get_balance(player, subkey=subkey)
        return await self.set_balance(player, currentbal - balance, subkey=subkey)

    # Levels
    async def get_levels(self, player: str, subkey: str = "") -> int:
        """
        Gets a player's levels.

        player: `str`_
            The player whose levels to retrieve.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int` -- The level balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/levels/{player}/{subkey}",
                headers=self._headers,
                raise_for_status=True,
            )
            ret = await r.json()
            return int(ret["exp"])

    async def set_levels(self, player: str, exp: int, *, subkey: str = "") -> int:
        """
        Set a player's levels.

        player: `str`_
            The player whose levels to set.

        exp: `int`_
            The amount of levels to set.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new level balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The experience value provided was not an integer.
        """
        await values.check_int(exp)
        async with aiohttp.ClientSession() as session:
            r = await session.put(
                f"{self._base_url}/levels/{player}/{subkey}",
                headers=self._headers,
                json={"exp": str(exp)},
                raise_for_status=True,
            )
            ret = await r.json()

    async def add_levels(self, player: str, exp: int, *, subkey: str = "") -> int:
        """
        Adds to a player's level balance.

        player: `str`_
            The player whose level balance to add to.

        exp: `int`_
            The amount to add to the player's level balance.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The experience value provided was not an integer.
        """
        currentexp = self.get_levels(player, subkey=subkey)
        newbal = self.set_levels(player, exp + currentexp, subkey=subkey)
        return int(newbal)

    async def subtract_levels(self, player: str, exp: int, *, subkey: str = "") -> int:
        """
        Subtracts from a player's level balance.

        player: `str`_
            The player whose level balance to subtract from.

        balance: `int`_
            The amount to add to the player's level balance.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `int`_ -- The new level balance for the player.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The experience value provided was not an integer.
        """
        currentexp = self.get_levels(player, subkey=subkey)
        newbal = self.set_levels(player, currentexp - exp, subkey=subkey)
        return int(newbal)

    # Leaderboards
    async def get_balance_leaderboards(
        self, *, after: int = 0, limit: int = 100, subkey: str = ""
    ) -> list:
        """
        Retrieve a list of the current balance leaderboards.

        after: Optional[`int`_]
            Position to get results after. This value must be positive. Defaults to 0.

        limit: Optional[`int`_]
            Maximum number of leaderboard entries to return. This value must be between 1 and 100. Defaults to 100.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `list`_ [`dict`_] -- A list of leaderboard entries in descending order (highest balance first).

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- One or more of the values provided are outside the boundary.

        Example response:
            .. code-block:: python

                [
                    {
                        "app_id": 1234567890123456,
                        "player_id": 1234,
                        "balance": 1000,
                        "rank": 1
                    },
                    {
                        "app_id": 1234567890123456,
                        "player_id": 513,
                        "balance": 854,
                        "rank": 2
                    },
                    # ...
                ]
        """
        await values.check_vals(after, limit)
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/currency/rankings?after={after}?limit={limit}",
                headers=self._headers,
                raise_for_status=True,
            )
            players = await r.json()
            # Convert the stringly-typed integer values returned by the API to ints, since other methods convert as well.
            for player in players:
                player.update(
                    (k, int(v)) for k, v in player.items() if k != "player_id"
                )
            return players

    async def get_levels_leaderboards(
        self, *, after: int = 0, limit: int = 100, subkey: str = ""
    ) -> list:
        """
        Retrieve a list of the current levels leaderboards.

        after: Optional[`int`_]
            Position to get results after. This value must be positive. Defaults to 0.

        limit: Optional[`int`_]
            Maximum number of leaderboard entries to return. This value must be between 1 and 100. Defaults to 100.

        subkey: Optional[`str`_]
            The `subkey`_ to use.

        Returns:
            `list`_ [`dict`_] -- A list of leaderboard entries in descending order (highest exp first).

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- One or more of the values provided are outside the boundary.

        Example response:
            .. code-block:: python

                [
                    {
                        "app_id": 1234567890123456,
                        "player_id": "1234",
                        "exp": 1000,
                        "rank": 1
                    },
                    {
                        "app_id": 1234567890123456,
                        "player_id": "513",
                        "exp": 854,
                        "rank": 2
                    },
                    # ...
                ]
        """
        await values.check_vals(after, limit)
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/levels/rankings?after={after}?limit={limit}",
                headers=self._headers,
                raise_for_status=True,
            )
            players = await r.json()
            # Convert the stringly-typed integer values returned by the API to ints, since other methods convert as well
            for player in players:
                player.update(
                    (k, int(v)) for k, v in player.items() if k != "player_id"
                )
            return players

    async def get_userdata(self, player: str) -> dict:
        """
        Gets a player's userdata.

        player: `str`_
            The player whose userdata to get.

        Returns:
            `dict`_ -- The player's userdata.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/userdata/{player}",
                headers=self._headers,
                raise_for_status=True,
            )
            data = await r.json()
            return data["data"]

    async def set_userdata(self, player: str, data: dict):
        """
        Sets a player's userdata.

        player: `str`_
            The player whose userdata to set.

        data: `dict`_
            The userdata in the form of a dictionary. Nested data is supported.

        Returns:
            `dict`_ -- The player's new userdata.

        Raises:
            `aiohttp.ClientResponseError`_ -- An HTTP error occured.
            `ValueError`_ -- The data provided was not a dictionary.
        """
        await values.check_dict(data)
        async with aiohttp.ClientSession() as session:
            response = await session.put(
                f"{self._base_url}/userdata/{player}",
                headers=self._headers,
                json=data,
                raise_for_status=True,
            )

    async def set_relationship(self, player: str, target: str, relationship_type: str):
        """
        Sets a player's relationship to another player. Relationships are stringly typed,
        meaning any kind of relationship is possible.

        player: `str`_
            The player whose relationship to set.

        target: `str`_
            The target player.

        Raises:
            `ValueError`_ -- One or more of the values provided are None or empty.
        """
        if relationship_type:
            raise ValueError("Value required.")
        async with aiohttp.ClientSession() as session:
            await session.put(
                f"{self._base_url}/relationships/{player}/{target}",
                headers=self._headers,
                json={
                    "type": relationship_type,
                },
                raise_for_status=True,
            )

    async def get_relationship(self, player: str, target: str) -> str:
        """
        Retrieves a player's relationship to another player.

        player: `str`_
            The player whose relationship to retrieve.

        target: `str`_
            The target player.
        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"{self._base_url}/relationships/{player}/{target}",
                headers=self._headers,
                raise_for_status=True,
            )
            data = await r.json()
            return r["type"]

    async def delete_relationship(self, player: str, target: str):
        """
        Removes a player's relationship to another player.

        player: `str`_
            The player whose relationship to remove.

        target: `str`_
            The target player.
        """
        async with aiohttp.ClientSession() as session:
            await session.delete(
                f"{self._base_url}/relationships/{player}/{target}",
                headers=self._headers,
                raise_for_status=True,
            )