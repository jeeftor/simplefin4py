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
    sf: SimpleFin = SimpleFin(access_url, proxy="http://192.168.1.25:3128")
    data = await sf.fetch_data()
    print(data)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
