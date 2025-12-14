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

# Arrange
@pytest.mark.parametrize(
    "x, y, vx, vy, expect_vy_positive",
    [                           
        (400, 300, -5, -5, False), # No wall contact - vy unchanged 
        (5, 200, -5, -5, False), # Left wall contact - vy unchanged
        (400, 4, -5, -5, True), # Top wall contact - vy flips
    ]
)

def test_ball_bounces_off_top_wall(x, y, vx, vy, expect_vy_positive):
    # Arrange
    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()

    ball = Ball(surface)
    ball.x = x
    ball.y = y
    ball.vx = vx
    ball.vy = vy

    ball.game_on = True

    # Act
    ball.update(surface)

    # Assert
    if expect_vy_positive:
        assert ball.vy > 0
    else:
        assert ball.vy < 0

# Arrange
@pytest.mark.parametrize(
    "x, y, vx, vy, expect_vx_positive",
    [                           
        (400, 200, -5, -5, False), # No wall contact - vx unchanged
        (4, 200, -5, -5, True), # Left wall contact - vx flips
        (796, 200, 5, -5, False), # Right wall contact - vx flips
    ]
)

def test_ball_bounces_off_side_wall(x, y, vx, vy, expect_vx_positive):
    # Arrange
    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()

    ball = Ball(surface)
    ball.x = x
    ball.y = y
    ball.vx = vx
    ball.vy = vy
    ball.game_on = True

    # Act
    ball.update(surface)

    # Assert
    if expect_vx_positive:
        assert ball.vx > 0
    else:
        assert ball.vx < 0
