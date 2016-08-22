#Poke Scraping

These are two scripts I use to get coordinates of rare Pokemon. When used in
conjunction with [PokemonGo-Bot](https://github.com/PokemonGoF/PokemonGo-Bot)
and [PokemonGo-Map](https://github.com/PokemonGoMap/PokemonGo-Map) it is
possible to quickly snipe Pokemon from all over the world.

The basic use case is as follows:

1. The scraper (`skiplagged.py` or `pokeradar.py`) detects Pokemon and sends
   the coordinates of the Pokemon with a HTTP request to the PokemonGo-Map instance
2. The PokeMonGo-Map instance starts scanning that area and detects the Pokemon.
   It then notifies the bot (see this [config](https://github.com/PokemonGoF/PokemonGo-Bot/blob/master/configs/config.json.map.example#L142))
3. The bot then teleports to that position which results in an 'encounter'. It
   then moves back to it's original position where it can now actually
   catch the Pokemon. This is known as sniping.


## Usage

```
pip install requests termcolor
python skiplagged.py
```