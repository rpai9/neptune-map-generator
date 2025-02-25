# Neptune Map Generator
This project generates a map of a galaxy with stars and wormholes based on configurable parameters. The galaxy can be of different types: spiral, elliptical, or irregular.

## Project Structure

- [`config.ini`](config.ini): Configuration file containing parameters for galaxy generation.
- [`neptune_map_gen.py`](neptune_map_gen.py): Main script that generates the galaxy map.
- [`requirements.txt`](requirements.txt): List of dependencies required for the project.
- `map_dump/`: Directory where the generated maps and JSON files are saved.

## Configuration

The [`config.ini`](config.ini) file contains the following parameters:

```ini
[galaxy]
total_points = 1000          ; Total number of stars to generate in the galaxy.
num_arms = 4                 ; Number of spiral arms in the galaxy (only applicable for spiral galaxies).
pitch_angle_degrees = 15.0   ; Pitch angle of the spiral arms in degrees (only applicable for spiral galaxies).
min_distance = 0.1           ; Minimum distance between any two stars to avoid overlap.
radius_limit = 100.0         ; Maximum radius of the galaxy.
galaxy_type = spiral         ; Type of the galaxy. Can be 'spiral', 'elliptical', or 'irregular'.

[wormholes]
pairs = [[1, 10], [2, 3], [4, 8], [6, 7]]  ; List of wormhole pairs, where each pair connects two stars by their indices.
```

## Installation

Clone the repository.
Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run the neptune_map_gen.py script to generate the galaxy map:

```bash
python neptune_map_gen.py
```

The script will generate the galaxy based on the parameters specified in the config.ini file and save the output in the map_dump directory.

## Output
The script generates the following output:

A JSON file containing the stars and wormholes.
An interactive HTML file with the galaxy map.

Example output files:

- `map_dump/1633036800/neptune_map.json`
- `map_dump/1633036800/galaxy_map.html`

## Example JSON Output

```json
{
  "stars": [
    {
      "uid": 1,
      "name": "competent_mayer",
      "x": -68.744,
      "y": 42.394,
      "r": 49,
      "g": 0,
      "e": 0,
      "i": 0,
      "s": 0,
      "st": 0
    },
    ...
  ],
  "wormholes": [[1, 10], [2, 3], [4, 8], [6, 7]]
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](license.md) file for details.
