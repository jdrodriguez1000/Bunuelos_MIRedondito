import pytest
import pandas as pd
import numpy as np
from src.builder import StatsEngine

def test_get_numeric_stats_basic():
    """Prueba que el StatsEngine calcule correctamente las métricas básicas"""
    # Arrange
    engine = StatsEngine()
    data = pd.DataFrame({
        'val': [10, 20, 30, 40, 50, 1000]
    })
    cols = ['val']
    config = {'outlier_detection': {'multiplier': 1.5}}
    
    # Act
    stats = engine.get_numeric_stats(data, cols, config)
    
    # Assert
    assert 'val' in stats
    assert stats['val']['mean'] == float(data['val'].mean())
    assert stats['val']['median'] == float(data['val'].median())
    assert "outlier_bounds" in stats['val']

def test_get_categorical_stats():
    """Prueba el perfilamiento de columnas categóricas"""
    # Arrange
    engine = StatsEngine()
    data = pd.DataFrame({
        'cat': ['A', 'A', 'B', 'C', 'A', 'B']
    })
    cols = ['cat']
    
    # Act
    stats = engine.get_categorical_stats(data, cols)
    
    # Assert
    assert 'cat' in stats
    assert stats['cat']['unique_values'] == 3
    assert 'distribution' in stats['cat']
    assert stats['cat']['distribution']['A'] == 0.5

def test_get_numeric_stats_empty():
    """Prueba el comportamiento con un DataFrame vacío"""
    engine = StatsEngine()
    data = pd.DataFrame({'val': []})
    stats = engine.get_numeric_stats(data, ['val'], {})
    
    # Pandas devuelve NaN para métricas en series vacías
    assert np.isnan(stats['val']['mean'])
    assert np.isnan(stats['val']['median'])
