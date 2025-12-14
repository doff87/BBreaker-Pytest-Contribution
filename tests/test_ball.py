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

# Helper classes and functions for brick collision tests
class FakeBrick:
    def __init__(self, rect):
        self.rect = rect

def brick_at_point(point):
    return FakeBrick(pygame.Rect(point[0], point[1], 1, 1)) # Make a 1x1 rect at the point

# One-brick collision cases
# Arrange
@pytest.mark.parametrize(
    "rect_origin, vx, vy, hit_point, expect_vx_positive, expect_vy_positive",
    [
        ((100, 100, 10, 10), 5, 5, "midright", False, True),   # midright - vx flips
        ((120, 120, 10, 10), 5, 5, "midbottom", True, False),  # midbottom - vy flips
        ((140, 140, 10, 10), 5, -5, "midtop", True, True),     # midtop - vy flips
        ((160, 160, 10, 10), -5, -5, "midleft", True, False),  # midleft - vx flips
    ],
)
def test_one_brick_collisions(rect_origin, vx, vy, hit_point, expect_vx_positive, expect_vy_positive):
    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()

    ball = Ball(surface)
    ball.rect = pygame.Rect(*rect_origin)
    ball.vx, ball.vy = vx, vy

    pt = getattr(ball.rect, hit_point)
    bricks = [brick_at_point(pt)]

    # Act
    ball.handle_brick_collisions(bricks)

    # Assert
    if expect_vx_positive:
        assert ball.vx > 0
    else:
        assert ball.vx < 0

    if expect_vy_positive:
        assert ball.vy > 0
    else:
        assert ball.vy < 0


# Two-brick collision variant
# Arrange
@pytest.mark.parametrize(
    "vx, vy, case, expect_vx_positive, expect_vy_positive",
    [
        (5, -5, "same_center_x", False, False),   # vx flips
        (-5, -5, "same_center_x", True, False),   # vx flips
        (5, -5, "same_center_y", True, True),     # vy flips
        (5, 5, "same_center_y", True, False),     # vy flips
        (5, 5, "different_centers", False, False),   # Both axes flip
        (-5, -5, "different_centers", True, True),   # Both axes flip
    ],
)

def test_two_brick_collision_variants(vx, vy, case, expect_vx_positive, expect_vy_positive):
    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()

    ball = Ball(surface)
    ball.vx, ball.vy = vx, vy

    if case == "same_center_x":
        b1 = FakeBrick(pygame.Rect(90, 90, 20, 20))
        b2 = FakeBrick(pygame.Rect(90, 200, 20, 20))
    elif case == "same_center_y":
        b1 = FakeBrick(pygame.Rect(90, 90, 20, 20))
        b2 = FakeBrick(pygame.Rect(200, 90, 20, 20))
    else:
        b1 = FakeBrick(pygame.Rect(10, 10, 20, 20))
        b2 = FakeBrick(pygame.Rect(200, 200, 20, 20))

    # Act
    ball.handle_brick_collisions([b1, b2])

    # Assert
    if expect_vx_positive:
        assert ball.vx > 0
    else:
        assert ball.vx < 0

    if expect_vy_positive:
        assert ball.vy > 0
    else:
        assert ball.vy < 0


# Three-brick collision case
# Arrange
@pytest.mark.parametrize(
    "vx, vy, expect_vx_positive, expect_vy_positive",
    [
        # In all situations of 3-brick collisions, all velocity components should flip
        (-5, 5, True, False),    # Left and down - both axes flip
        (5, -5, False, True),    # Right and up - both axes flip
        (5, 5, False, False),    # Right and down – both axes flip
        (-5, -5, True, True),    # Left and up – both axes flip
    ],
)

def test_three_brick_collision_flips_both_axes(vx, vy, expect_vx_positive, expect_vy_positive):
    # These tests failing reflects the structure for three-brick collision handling in Ball.py is misconstructed.
    # As written, the method handler utilizes two if statements, not an if-elif-else structure,
    # so that when three bricks are hit, the single-brick handler is also invoked after the three-brick handler,
    # given a three-brick block collision. The logic of the handlers is such that the single-brick handler
    # requires ball.rect to be set, whereas the handler does not require that parameter. In normal play,
    # that isn't an issue, but in the testing suite it causes an AttributeError.
    # To fix this issue, ball.handle_brick_collisions should be restructured to use if-elif-else.

    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()

    ball = Ball(surface)
    ball.vx, ball.vy = vx, vy

    bricks = [
        FakeBrick(pygame.Rect(10, 10, 20, 20)),
        FakeBrick(pygame.Rect(50, 50, 20, 20)),
        FakeBrick(pygame.Rect(90, 90, 20, 20)),
    ]

    # Act
    ball.handle_brick_collisions(bricks)

    # Assert
    if expect_vx_positive:
        assert ball.vx > 0
    else:
        assert ball.vx < 0

    if expect_vy_positive:
        assert ball.vy > 0
    else:
        assert ball.vy < 0