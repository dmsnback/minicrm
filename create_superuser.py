import asyncio

from app.core.init_db import create_first_superuser


async def main():
    await create_first_superuser()


if __name__ == "__main__":
    asyncio.run(main())
