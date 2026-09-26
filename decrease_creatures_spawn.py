import json
from pathlib import Path

SOURCE_DIR = Path(r"d:\Games\Minecraft\26.3\data\minecraft\worldgen\biome")
DEST_DIR = Path(r"d:\Games\Minecraft\MyDataPacks_Java\ScarceWorld\ScarceWorld\data\minecraft\worldgen\biome")

MULTIPLIER = 0.25

# Vanilla 26.3 default when the biome does not specify the attribute.
DEFAULT_PROBABILITY = 0.1

ATTRIBUTE = "minecraft:gameplay/creature_world_gen_spawn_probability"


def process_file(source_path, dest_path):
    with source_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Find the creature spawn category.
    try:
        spawns_by_category = (
            data["attributes"]
            ["minecraft:gameplay/natural_mob_spawns"]
            ["argument"]
            ["spawns_by_category"]
        )
    except KeyError:
        print(f"{source_path.name}: skipped (no spawn categories)")
        return

    # Skip biomes that have no "creature" category.
    if "creature" not in spawns_by_category:
        print(f"{source_path.name}: skipped (no creature category)")
        return

    attributes = data["attributes"]

    was_missing = ATTRIBUTE not in attributes
    old_value = attributes.get(ATTRIBUTE, DEFAULT_PROBABILITY)
    new_value = old_value * MULTIPLIER

    attributes[ATTRIBUTE] = new_value

    with dest_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    if was_missing:
        print(f"{source_path.name}: {old_value} -> {new_value} (field added)")
    else:
        print(f"{source_path.name}: {old_value} -> {new_value}")


def main():
    for source_path in SOURCE_DIR.glob("*.json"):
        dest_path = DEST_DIR / source_path.name
        process_file(source_path, dest_path)


if __name__ == "__main__":
    main()
