# Arkvatar-py

API Wrapper to interact with Arkvatar.

## Built with

- [Python](https://www.python.org/)
- [AIOHTTP](https://aiohttp.readthedocs.io/en/stable/)

## Installation

```shell
pip install arkvatar-py
```

## Usage

```python
import asyncio
from arkvatar import Arkvatar


async def main():
    arkvatar = Arkvatar()
    identifier = "azerty@gmail.com"
    request = await arkvatar.store("Email", identifier)
    print(request)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Authors

- Jolan Beer - Highjhacker

## License

Arkvatar-py is under MIT license. See the [LICENSE file](LICENSE.md) for more informations.
