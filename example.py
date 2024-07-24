"""Example file."""
import asyncio
from dotenv import load_dotenv
import os

from simplefin4py import SimpleFin

# Read info from .env file
load_dotenv()

access_url: str = os.getenv("ACCESS_URL", "")


async def main() -> None:
    """Main function."""
    sf: SimpleFin = SimpleFin(access_url)
    data = await sf.fetch_data()
    # print(data)


    for account in data.accounts:
        print(account.name, account.org.name, account.possible_error)
        print(account.balance_date)
        print(account.last_update_utc)
        print(account.last_update_timestamp)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
