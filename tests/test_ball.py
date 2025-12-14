import pytest
import pygame

from bbreaker.Ball import Ball

# Arrange
@pytest.mark.parametrize(
    "start_pos, end_pos, expect_none",
    [
        ((100, 200), (100, 100), True),   # Upward drag - invalid
        ((100, 100), (-20, 120), True),  # Drag angle too shallow to the left - invalid
        ((100, 100), (220, 120), True),   # Drag angle too shallow to the right - invalid
        ((100, 100), (100, 120), False), # Straight down - valid
        ((100, 100), (-18, 121), False), # Downward left - valid
        ((100, 100), (218, 121), False),  # Downward right - valid
    ]
)

def test_calculate_strike_angle(start_pos, end_pos, expect_none):
    # Act
    angle = Ball.calculate_strike_angle(start_pos, end_pos)

    # Assert
    if expect_none:
        assert angle is None
    else:
        assert angle is not None