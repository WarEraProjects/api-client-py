# Code Snippets

This page contains a collection of quick, copy-pasteable code snippets for common tasks and patterns in the `warera-client`. 

If you are trying to figure out "How do I do X?", you are in the right place!

## Sync/Blocking Usage

If you don't want to use `asyncio`, use the synchronous wrapper! It automatically manages a background event loop for you.

```python
from warera.sync import WareraClient

# Create a client
client = WareraClient(api_key="your-api-key")

# Call methods exactly like the async version, but without 'await'
user = client.user.get_by_id("123")
print(user.name)

# Even get_many works synchronously!
countries = client.country.get_many(["7", "8", "9"])
```

## Using Enums for Filtering

Many endpoints require specific filter strings. To avoid typos, the library provides Python Enums for all valid options!

```python
import warera
from warera import BattleFilter, BattleRankingDataType

async def fetch_battles():
    # Only fetch battles happening in your country
    battles = await warera.battle.get_active(filter_by=BattleFilter.YOUR_COUNTRY)
    
    # Fetch battle rankings, specifically for Damage dealt
    rankings = await warera.battle_ranking.get(
        battle_id="100", 
        data_type=BattleRankingDataType.DAMAGE
    )
```

## Handling Missing/Optional Data

WarEra's API is highly dynamic, and some fields may not exist if a user hasn't unlocked a feature or if a country hasn't set a policy. Always check if a nested object exists before accessing its properties!

```python
import warera

async def check_user_party():
    user = await warera.user.get_by_id("123")
    
    # ALWAYS check if the field exists first
    if user.party:
        print(f"User is in party: {user.party.name}")
    else:
        print("User is completely independent!")
```

## Explicit Batch Control

If you have a complex block of code where you want to manually group multiple unrelated requests into a single network payload, you can use the manual batch context manager:

```python
from warera import WareraClient

async def fetch_dashboard():
    async with WareraClient() as client:
        # Open a manual batch session
        async with client.batch() as batch:
            # Queue up requests (these don't hit the network yet)
            c1_req = batch.add("country.getCountryById", {"countryId": "7"})
            c2_req = batch.add("country.getCountryById", {"countryId": "8"})
            game_req = batch.add("gameConfig.getGameConfig", {})
            
        # The block exits, the single combined network request fires, and we get our data!
        c1 = c1_req.result
        game_config = game_req.result
```

## Persistent Caching

If you are writing a Discord bot or long-running script, you should persist the cache to a local SQLite database so it survives restarts.

```python
import asyncio
from warera import WareraClient
from warera.cache_backends import SQLiteCacheBackend

async def main():
    # Store the cache in a local sqlite file
    cache = SQLiteCacheBackend("my_bot_cache.sqlite")
    
    async with WareraClient(cache_backend=cache) as client:
        # The first time this runs, it hits the network.
        # If you restart the script 10 minutes later, it loads from disk instantly!
        config = await client.game_config.get()

if __name__ == "__main__":
    asyncio.run(main())
```

## Catching Specific API Errors

Sometimes you need to gracefully handle rate limits, missing entities, or bad authentication.

```python
import warera
from warera.exceptions import (
    WareraNotFoundError,
    WareraRateLimitError,
    WareraUnauthorizedError
)

async def safe_fetch():
    try:
        user = await warera.user.get_by_id("99999999999999")
    except WareraNotFoundError:
        print("That user doesn't exist!")
    except WareraRateLimitError:
        print("We hit the rate limit and ran out of automatic retries!")
    except WareraUnauthorizedError:
        print("Our API key is invalid or missing.")
    except Exception as e:
        print(f"A totally different error occurred: {e}")
```
