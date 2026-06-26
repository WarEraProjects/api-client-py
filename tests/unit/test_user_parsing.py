import json

from warera.models.user import User, UserLite


def test_user_parsing_from_sample():
    sample_json = """
    {
      "result": {
        "data": {
          "dates": {
            "lastConnectionAt": "2024-01-01T00:00:00.000Z",
            "lastHiresAt": ["2024-01-01T00:00:00.000Z"],
            "lastWorkAt": "2024-01-01T00:00:00.000Z"
          },
          "leveling": {
            "level": 10,
            "totalXp": 1000
          },
          "_id": "mock_user_id",
          "username": "mock_user",
          "country": "mock_country_id",
          "isActive": true,
          "skills": {
            "energy": {
              "level": 1,
              "total": 100
            },
            "attack": {
              "level": 1,
              "total": 100
            }
          },
          "militaryRank": 1,
          "createdAt": "2024-01-01T00:00:00.000Z",
          "stats": {
            "damagesCount": 100
          },
          "rankings": {
            "userDamages": {
              "value": 100,
              "rank": 1,
              "tier": "bronze"
            }
          },
          "avatarUrl": "https://example.com/avatar.jpg",
          "mu": "mock_mu_id"
        }
      }
    }
    """
    data = json.loads(sample_json)["result"]["data"]
    user = User.model_validate(data)

    assert user.id == "mock_user_id"
    assert user.username == "mock_user"
    assert user.country == "mock_country_id"
    assert user.is_active is True
    assert user.leveling.level == 10
    assert user.skills.energy.level == 1
    assert user.stats.damages_count == 100
    assert user.rankings.user_damages.tier == "bronze"
    assert user.mu == "mock_mu_id"
    assert user.avatar_url == "https://example.com/avatar.jpg"

    # Also ensure UserLite parses correctly and ignores extra fields
    user_lite = UserLite.model_validate(data)
    assert user_lite.id == "mock_user_id"
    assert user_lite.leveling.level == 10
    assert user_lite.stats.damages_count == 100


def test_user_parses_dict_shaped_skin_keys_and_tours():
    """
    Regression test: the live API returns `equippedSkinKeys` as a string→string
    map and `finishedTours` as a string→bool map. v0.1.x typed these as
    list[str], forcing downstream consumers to monkey-patch the raw response.
    """
    data = {
        "_id": "mock_user_id",
        "username": "mock_user",
        "equippedSkinKeys": {
            "pants": "valentinePants2",
            "rifle": "1kSubRifle",
            "tank": "hamsterTank",
            "helmet": "birthday1YearBetaHelmet",
        },
        "finishedTours": {
            "battle": True,
            "military": True,
            "economic": True,
            "onboarding": True,
        },
    }
    user = User.model_validate(data)
    assert user.equipped_skin_keys["rifle"] == "1kSubRifle"
    assert user.finished_tours["onboarding"] is True

    # Empty maps and absent fields must also parse.
    assert (
        User.model_validate({"_id": "u2", "equippedSkinKeys": {}, "finishedTours": {}}).id == "u2"
    )
    assert User.model_validate({"_id": "u3"}).finished_tours is None
