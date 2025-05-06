"""
Data Utilities for FIFA Visual Analysis

This module provides utility functions for loading and processing data.
"""

import pandas as pd
import numpy as np
import os
import colorsys

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the cleaned data folder

# Define a colorblind-friendly palette with reduced variety for better clarity
# Using a smaller set of high-contrast, distinctive colors
TEAM_COLORS = {
    'Argentina': '#66c2a5',      # Teal
    'Australia': '#fc8d62',      # Salmon
    'Belgium': '#8da0cb',        # Blue-purple
    'Brazil': '#e78ac3',         # Pink
    'Cameroon': '#a6d854',       # Light green
    'Canada': '#ffd92f',         # Yellow
    'Costa Rica': '#e5c494',     # Tan
    'Croatia': '#b3b3b3',        # Gray
    'Denmark': '#4d4d4d',        # Dark gray
    'Ecuador': '#80b1d3',        # Light blue
    'England': '#bebada',        # Light purple
    'France': '#fb8072',         # Light red/coral
    'Germany': '#1f78b4',        # Dark blue
    'Ghana': '#33a02c',          # Green
    'Iran': '#ff7f00',           # Orange
    'Japan': '#6a3d9a',          # Purple
    'Korea Republic': '#b15928',  # Brown
    'Mexico': '#ffff99',         # Light yellow
    'Morocco': '#cab2d6',        # Light lavender
    'Netherlands': '#fdbf6f',    # Light orange
    'Poland': '#d9d9d9',         # Very light gray
    'Portugal': '#e31a1c',       # Red
    'Qatar': '#a6cee3',          # Very light blue
    'Saudi Arabia': '#b2df8a',   # Light lime
    'Senegal': '#1f78b4',        # Medium blue
    'Serbia': '#fb9a99',         # Light pink
    'Spain': '#e31a1c',          # Red
    'Switzerland': '#fdbf6f',    # Light orange
    'Tunisia': '#ff7f00',        # Orange
    'United States': '#6a3d9a',  # Purple
    'Uruguay': '#33a02c',        # Green
    'Wales': '#cab2d6'           # Light lavender
}

# Pattern mapping for additional visual differentiation 
# Each team gets a unique dash pattern to supplement color
TEAM_PATTERNS = {
    'Argentina': 'solid',
    'Australia': 'dash',
    'Belgium': 'dot',
    'Brazil': 'dashdot',
    'Cameroon': 'longdash',
    'Canada': 'longdashdot',
    'Costa Rica': 'solid',
    'Croatia': 'dash',
    'Denmark': 'dot',
    'Ecuador': 'dashdot',
    'England': 'longdash',
    'France': 'longdashdot',
    'Germany': 'solid',
    'Ghana': 'dash',
    'Iran': 'dot',
    'Japan': 'dashdot',
    'Korea Republic': 'longdash',
    'Mexico': 'longdashdot',
    'Morocco': 'solid',
    'Netherlands': 'dash',
    'Poland': 'dot',
    'Portugal': 'dashdot',
    'Qatar': 'longdash',
    'Saudi Arabia': 'longdashdot',
    'Senegal': 'solid',
    'Serbia': 'dash',
    'Spain': 'dot',
    'Switzerland': 'dashdot',
    'Tunisia': 'longdash',
    'United States': 'longdashdot',
    'Uruguay': 'solid',
    'Wales': 'dash'
}

# Simplified symbol mapping for scatter plots
# Using a smaller set of solid shapes (no hollow shapes or triangles)
TEAM_SYMBOLS = {
    'Argentina': 'circle',
    'Australia': 'square',
    'Belgium': 'diamond',
    'Brazil': 'cross',
    'Cameroon': 'x',
    'Canada': 'star',
    'Costa Rica': 'circle',
    'Croatia': 'square',
    'Denmark': 'diamond',
    'Ecuador': 'cross',
    'England': 'x',
    'France': 'star',
    'Germany': 'circle',
    'Ghana': 'square',
    'Iran': 'diamond', 
    'Japan': 'cross',
    'Korea Republic': 'x',
    'Mexico': 'star',
    'Morocco': 'circle',
    'Netherlands': 'square',
    'Poland': 'diamond',
    'Portugal': 'cross',
    'Qatar': 'x',
    'Saudi Arabia': 'star',
    'Senegal': 'circle',
    'Serbia': 'square',
    'Spain': 'diamond',
    'Switzerland': 'cross',
    'Tunisia': 'x',
    'United States': 'star',
    'Uruguay': 'circle',
    'Wales': 'square'
}

def get_team_color(team, fallback_colors=None):
    """Get a consistent color for a team, with fallback to a generated color if needed"""
    if team in TEAM_COLORS:
        return TEAM_COLORS[team]
    
    # If we don't have a pre-defined color, generate one
    if fallback_colors and team in fallback_colors:
        return fallback_colors[team]
        
    # Last resort: generate a random color
    h = hash(team) % 360 / 360.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.9, 0.9)
    return f'rgba({int(r*255)},{int(g*255)},{int(b*255)},0.85)'

def get_team_pattern(team):
    """Get a consistent dash pattern for a team"""
    if team in TEAM_PATTERNS:
        return TEAM_PATTERNS[team]
    return 'solid'  # Default

def get_team_symbol(team):
    """Get a consistent symbol for a team"""
    if team in TEAM_SYMBOLS:
        return TEAM_SYMBOLS[team]
    return 'circle'  # Default

def load_team_data():
    """
    Load team data from CSV file
    """
    try:
        file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None
        
def load_player_data():
    """
    Load player data from CSV file
    """
    try:
        file_path = os.path.join(DATA_PATH, "player_data_clean.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading player data: {e}")
        return None
        
def load_match_data():
    """
    Load match data from CSV file
    """
    try:
        file_path = os.path.join(DATA_PATH, "match_data_clean.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading match data: {e}")
        return None
        
def get_attribute_range(df, attribute):
    """
    Get the min and max values for an attribute
    """
    if attribute not in df.columns:
        return 0, 1
        
    min_val = df[attribute].min()
    max_val = df[attribute].max()
    
    # Add a small buffer to the range
    buffer = (max_val - min_val) * 0.05
    
    return min_val - buffer, max_val + buffer
    
def get_pcp_attributes():
    """
    Get the attributes to be used in the PCP
    """
    return [
        'possession', 
        'shots_per90', 
        'goals_per90', 
        'assists_per90', 
        'passes_pct', 
        'passes_pct_short', 
        'passes_pct_medium', 
        'passes_pct_long', 
        'tackles_interceptions', 
        'gk_save_pct'
    ]
    
def get_attribute_labels():
    """
    Get the user-friendly labels for attributes
    """
    return {
        'possession': 'Possession %',
        'shots_per90': 'Shots per 90',
        'goals_per90': 'Goals per 90',
        'assists_per90': 'Assists per 90',
        'passes_pct': 'Pass Completion %',
        'passes_pct_short': 'Short Pass %',
        'passes_pct_medium': 'Medium Pass %',
        'passes_pct_long': 'Long Pass %',
        'tackles_interceptions': 'Tackles + Interceptions',
        'gk_save_pct': 'Save %',
        'xg_per90': 'xG per 90',
        'xg_assist_per90': 'xA per 90',
        'npxg_per90': 'npxG per 90',
        'dribble_tackles_pct': 'Tackle Success %',
        'dribbles_completed_pct': 'Dribble Success %',
        'aerials_won_pct': 'Aerial Duels Won %',
        'gk_pens_save_pct': 'Penalty Save %'
    }
    
def get_team_color_map():
    """
    Get a color map for teams
    """
    return {
        0: 'rgba(220, 20, 60, 0.9)',     # Crimson
        1: 'rgba(0, 0, 255, 0.9)',       # Blue
        2: 'rgba(0, 128, 0, 0.9)',       # Green
        3: 'rgba(255, 140, 0, 0.9)',     # Dark Orange
        4: 'rgba(128, 0, 128, 0.9)',     # Purple
        5: 'rgba(0, 206, 209, 0.9)',     # Turquoise
        6: 'rgba(255, 20, 147, 0.9)',    # Deep Pink
        7: 'rgba(255, 215, 0, 0.9)',     # Gold
        8: 'rgba(139, 69, 19, 0.9)',     # Saddle Brown
        9: 'rgba(70, 130, 180, 0.9)'     # Steel Blue
    }