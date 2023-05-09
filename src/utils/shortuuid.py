# See https://pypi.org/project/shortuuid/ for more information
"""Concise UUID generation."""
import math
import uuid as _uu


class ShortUUID:
    """
    A generator class for PEP-412-compliant short UUIDs.
    """

    ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    def __init__(self) -> None:
        self._alphabet = list(sorted(set(self.ALPHABET)))
        self._alpha_len = len(self._alphabet)
        self._length = int(math.ceil(math.log(2**128, self._alpha_len)))

    async def encode(self, uuid: _uu.UUID) -> str:
        """
        Encode a UUID into a string (LSB first) according to the alphabet.

        If leftmost (MSB) bits are 0, the string might be shorter.
        """
        return await self._int_to_string(uuid.int, self._alphabet, padding=self._length)

    async def decode(self, string: str, legacy: bool = False) -> _uu.UUID:
        """
        Decode a string according to the current alphabet into a UUID.

        Raises ValueError when encountering illegal characters or a too-long string.

        If string too short, fills leftmost (MSB) bits with 0.

        Pass `legacy=True` if your UUID was encoded with a ShortUUID version prior to
        1.0.0.
        """
        if legacy:
            string = string[::-1]
        return _uu.UUID(int=await self._string_to_int(string, self._alphabet))

    async def uuid(self, name: str | None = None) -> str:
        """
        Generate and return a UUID.

        If the name parameter is provided, set the namespace to the provided
        name and generate a UUID.
        """
        # If no name is given, generate a random UUID.
        if name is None:
            u = _uu.uuid4()
        elif name.lower().startswith(("http://", "https://")):
            u = _uu.uuid5(_uu.NAMESPACE_URL, name)
        else:
            u = _uu.uuid5(_uu.NAMESPACE_DNS, name)
        return await self.encode(u)

    @staticmethod
    async def _int_to_string(
        number: int, alphabet: list[str], padding: int | None = None
    ) -> str:
        """
        Convert a number to a string, using the given alphabet.

        The output has the most significant digit first.
        """
        output = ""
        alpha_len = len(alphabet)
        while number:
            number, digit = divmod(number, alpha_len)
            output += alphabet[digit]
        if padding:
            remainder = max(padding - len(output), 0)
            output = output + alphabet[0] * remainder
        return output[::-1]

    @staticmethod
    async def _string_to_int(string: str, alphabet: list[str]) -> int:
        """
        Convert a string to a number, using the given alphabet.

        The input is assumed to have the most significant digit first.
        """
        number = 0
        alpha_len = len(alphabet)
        for char in string:
            number = number * alpha_len + alphabet.index(char)
        return number


# For backwards compatibility
_global_instance = ShortUUID()
encode = _global_instance.encode
decode = _global_instance.decode
uuid = _global_instance.uuid
