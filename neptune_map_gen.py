import configparser
import json
import os
import math
import random
from datetime import datetime

import numpy as np
import plotly.graph_objects as go
from names_generator import generate_name

# Load configuration from file
config = configparser.ConfigParser()
config.read("config.ini")

# Extract parameters from configuration
total_points = config.getint("galaxy", "total_points")
num_arms = config.getint("galaxy", "num_arms")
pitch_angle = np.radians(config.getfloat("galaxy", "pitch_angle_degrees"))
min_distance = config.getfloat("galaxy", "min_distance")
radius_limit = config.getfloat("galaxy", "radius_limit")
galaxy_type = config.get("galaxy", "galaxy_type")
wormholes = json.loads(config.get("wormholes", "pairs"))
num_player = config.getint("player_positioning", "num_players")
max_dist_to_neighbor = config.getfloat("player_positioning", "max_dist_to_neighbor")
ini_r = config.getint("player_initial_resource", "r")
ini_g = config.getint("player_initial_resource", "g")
ini_e = config.getint("player_initial_resource", "e")
ini_i = config.getint("player_initial_resource", "i")
ini_s = config.getint("player_initial_resource", "s")
ini_st = config.getint("player_initial_resource", "st")


def add_players_to_coordinates(coordinates):
    player_indices = np.random.choice(len(coordinates), num_player, replace=False)
    optimized_dist_min = radius_limit / (2 * math.sqrt(num_player))
    optimized_dist_max = radius_limit / (2 * math.sqrt(math.log(num_player)))

    if max_dist_to_neighbor < optimized_dist_min:
        print("max_dist_to_neighbor is too small, players will be too close to each other")

    if max_dist_to_neighbor > optimized_dist_max:
        print("max_dist_to_neighbor is too large, players will be too far from each other")

    optimized_dist = max_dist_to_neighbor
    if max_dist_to_neighbor < optimized_dist_min or max_dist_to_neighbor > optimized_dist_max:
        print("max_dist_to_neighbor is not in the optimal range, using the average value")
        optimized_dist = (optimized_dist_min + optimized_dist_max) / 2

    for i in range(1, num_player):
        while True:
            distances = np.linalg.norm(
                np.array([coordinates[player_indices[i]]["x"], coordinates[player_indices[i]]["y"]])
                - np.array([[coordinates[j]["x"], coordinates[j]["y"]] for j in player_indices[:i]]),
                axis=1,
            )
            if np.all(distances > optimized_dist):
                break
            player_indices[i] = np.random.choice(len(coordinates))

    for i, idx in enumerate(player_indices):
        coordinates[idx].update({"puid": i + 1, "r": ini_r, "g": ini_g, "e": ini_e, "i": ini_i, "s": ini_s, "st": ini_st})

    return coordinates


def generate_spiral_galaxy(total_points, num_arms, pitch_angle, min_distance, radius_limit):
    coordinates = []

    while len(coordinates) < total_points:
        # Randomly generate a radius and angle
        radius = np.random.uniform(0, radius_limit)
        angle = np.random.uniform(0, 2 * np.pi)

        # Compute the angular offset based on the pitch angle and radius
        arm_offset = radius / np.tan(pitch_angle)
        arm_angle = angle + arm_offset

        # Assign the star to a specific arm
        arm_choice = np.random.randint(0, num_arms)
        arm_rotation = 2 * np.pi * arm_choice / num_arms
        arm_angle += arm_rotation

        # Convert polar coordinates to Cartesian coordinates
        x = radius * np.cos(arm_angle)
        y = radius * np.sin(arm_angle)

        # Check if the new point is at least min_distance from all existing points
        if all(np.linalg.norm([x - cx, y - cy]) >= min_distance for cx, cy in coordinates):
            coordinates.append((x, y))

    return np.array(coordinates)


def generate_elliptical_galaxy(total_points, min_distance, radius_limit):
    coordinates = []

    while len(coordinates) < total_points:
        # Randomly generate a radius and angle
        radius = np.random.uniform(0, radius_limit)
        angle = np.random.uniform(0, 2 * np.pi)

        # Convert polar coordinates to Cartesian coordinates
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        # Check if the new point is at least min_distance from all existing points
        if all(np.linalg.norm([x - cx, y - cy]) >= min_distance for cx, cy in coordinates):
            coordinates.append((x, y))

    return np.array(coordinates)


def generate_irregular_galaxy(total_points, min_distance, radius_limit):
    coordinates = []

    while len(coordinates) < total_points:
        # Randomly generate x and y coordinates
        x = np.random.uniform(-radius_limit, radius_limit)
        y = np.random.uniform(-radius_limit, radius_limit)

        # Check if the new point is at least min_distance from all existing points
        if all(np.linalg.norm([x - cx, y - cy]) >= min_distance for cx, cy in coordinates):
            coordinates.append((x, y))

    return np.array(coordinates)


if __name__ == "__main__":
    # Generate the galaxy based on the type specified in the config
    if galaxy_type == "spiral":
        coordinates = generate_spiral_galaxy(total_points, num_arms, pitch_angle, min_distance, radius_limit)
    elif galaxy_type == "elliptical":
        coordinates = generate_elliptical_galaxy(total_points, min_distance, radius_limit)
    elif galaxy_type == "irregular":
        coordinates = generate_irregular_galaxy(total_points, min_distance, radius_limit)
    else:
        raise ValueError("Unknown galaxy type")

    stars = []
    star_names = []
    for i, coord in enumerate(coordinates, start=1):
        star_name = generate_name(seed=i)
        star_name = "-".join([j.capitalize() for j in star_name.split("_")])
        star = {
            "uid": i,
            "name": star_name,
            "x": round(coord[0], 3),
            "y": round(coord[1], 3),
            "r": random.randint(1, 50),
            "g": random.randint(0, 1),
            "e": random.randint(0, 0),
            "i": random.randint(0, 0),
            "s": random.randint(0, 0),
            "st": random.randint(0, 0),
        }
        stars.append(star)
        star_names.append(star_name)

    # Add players to the coordinates
    stars = add_players_to_coordinates(stars)

    result = {"stars": stars, "wormholes": wormholes}

    # Convert to JSON
    json_output = json.dumps(result, indent=4)

    epoch = int(datetime.now().timestamp())
    # Create output directory if it doesn't exist
    output_dir = f"./map_dump/{epoch}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write JSON output to file
    with open(f"{output_dir}/neptune_map.json", "w") as f:
        f.write(json_output)

    # Ensure coordinates is a 2D array
    coordinates = np.array([[star["x"], star["y"]] for star in stars])
    if coordinates.ndim != 2 or coordinates.shape[1] != 2:
        raise ValueError("Coordinates array is not in the correct shape")

    # Plot the galaxy using Plotly
    fig = go.Figure()

    # Add stars to the plot with tooltips
    for star in stars:
        color = "white" if "puid" not in star else f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"
        fig.add_trace(
            go.Scatter(
                x=[star["x"]],
                y=[star["y"]],
                mode="markers",
                marker=dict(color=color, size=5, symbol="star"),
                text=f"Index: {star['uid']} , Name: {star['name']} , Resources: {star['r']} , G: {star['g']} , E: {star['e']} , I: {star['i']} , S: {star['s']} ,ST: {star['st']}",
                hoverinfo="text",
                name="Stars" if "puid" not in star else f"Player {star['puid']}",
            )
        )

    # Add wormholes to the plot
    for pair in wormholes:
        star1 = coordinates[pair[0] - 1]
        star2 = coordinates[pair[1] - 1]
        fig.add_trace(
            go.Scatter(
                x=[star1[0], star2[0]],
                y=[star1[1], star2[1]],
                mode="lines+markers",
                marker=dict(color="red", size=5),
                line=dict(color="red"),
                name="Wormholes",
            )
        )

    fig.update_layout(
        title={"text": f"Galaxy Map - {galaxy_type.capitalize()} Galaxy: EPOCH - {epoch}", "x": 0.5, "xanchor": "center"},  # Center the title
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        plot_bgcolor="#202735",  # Hex color for black background
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False),  # Remove x-axis grid and zero lines
        yaxis=dict(showgrid=False, zeroline=False),  # Remove y-axis grid and zero lines
    )

    # Update traces to show only player stars and wormholes in the legend
    for trace in fig.data:
        if "Player" in trace.name:
            trace.update(marker=dict(size=10, color=f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"), showlegend=True)
        elif trace.name == "Wormholes":
            trace.update(showlegend=True)
        else:
            trace.update(showlegend=False)

    # Save the plot as an HTML file
    fig.write_html(f"{output_dir}/galaxy_map.html")

    # Read the HTML template
    with open("editable_map.html") as template_file:
        editable_html_template = template_file.read()

    # Replace the placeholder with the actual data
    editable_html_content = editable_html_template.replace("{{ initial_data }}", json.dumps(result, indent=4))

    # Write the editable HTML content to a file
    with open(f"{output_dir}/editable_galaxy_map.html", "w") as f:
        f.write(editable_html_content)

    print("Map generated successfully! Check the map_dump folder for the output.")
