# Getting Started

Ready to build your first script with the WarEra Python Client? This guide will walk you through the absolute basics.

## 1. Installation

Install the library using pip:

```bash
pip install warera-client
```

## 2. Setting Your API Key

While you *can* use the library anonymously, you will be heavily rate-limited. It is highly recommended to get an API key from the WarEra settings page.

You can set your API key by passing it to `set_api_key()`:

```python
import warera

warera.set_api_key("YOUR_API_KEY_HERE")
```

Alternatively, you can just set the `WARERA_API_KEY` environment variable in your terminal, and the library will detect it automatically!

## 3. Your First Async Script

Let's write a simple script to fetch a specific country's data and print its name and treasury balance.

```python
import asyncio
import warera

async def main():
    # Fetch country ID '7'
    country = await warera.country.get_by_id("7")
    
    print(f"Welcome to {country.name}!")
    
    # We can access nested fields safely!
    if country.taxes:
        print(f"Income Tax: {country.taxes.income}%")

if __name__ == "__main__":
    asyncio.run(main())
```

## 4. Fetching Multiple Items (Auto-Batching)

One of the best features of this library is how it handles multiple requests. 

If you want to fetch 5 different users, you don't need to manually combine them into a single payload. Just use `.get_many()`:

```python
import asyncio
import warera

async def main():
    # Pass a list of IDs to get_many()
    user_ids = ["1", "2", "3", "4", "5"]
    
    # The library will automatically bundle these into a SINGLE network request!
    users = await warera.user.get_many(user_ids)
    
    for user in users:
        print(f"{user.name} is level {user.leveling.level}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 5. Paginated Endpoints

Many endpoints in WarEra return cursor-paginated data (like lists of articles, battle logs, or users).

The library handles pagination tokens for you automatically via the `auto_items=True` parameter. This turns the response into an asynchronous generator that you can easily loop over!

```python
import asyncio
import warera

async def main():
    print("Fetching all users in country 7...")
    
    # auto_items=True abstracts away the pagination logic!
    async for user in await warera.user.get_by_country("7", auto_items=True):
        print(user.name)

if __name__ == "__main__":
    asyncio.run(main())
```

## 6. Going Huge: The `collect_all()` Engine

If you need to fetch millions of records (like transaction logs or battle rankings), simple pagination is too slow.

The `collect_all()` engine solves this by dividing the timeline into chunks and fetching them all **concurrently**:

```python
import asyncio
import warera

async def main():
    print("Downloading massive transaction history concurrently...")
    
    # This will fire 500 concurrent network requests!
    transactions = await warera.transaction.collect_all(
        oldest_date="2026-01-01T00:00:00Z",
        concurrency=500
    )
    
    print(f"Downloaded {len(transactions)} transactions instantly.")

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

Now that you know the basics, check out the [Code Snippets](Code-Snippets) page for quick copy-paste examples of common tasks, or explore the [API Reference](API-Reference) to see all the endpoints available!
