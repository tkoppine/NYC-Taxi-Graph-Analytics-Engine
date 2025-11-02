"""
NYC Taxi Graph Analytics Engine

A high-performance graph analytics engine for processing and analyzing 
New York City taxi trip data using Neo4j graph database.
Includes data loading, graph algorithms, and deployment configurations.
"""

__version__ = "1.0.0"
__author__ = "Teja Naidu"

from .data_loader import DataLoader
from .interface import Interface

__all__ = ["DataLoader", "Interface"]