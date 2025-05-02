"""
Data Utilities for FIFA Visual Analysis

This module provides utility functions for loading and processing data.
"""

import pandas as pd
import numpy as np
import os

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the cleaned data folder

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