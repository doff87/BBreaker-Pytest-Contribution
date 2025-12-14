# Contribution

## What I Contributed

I added a comprehensive pytest-based test suite for the `Ball` module, focusing on collision and movement behavior. The test suite covers:

- Strike angle validation based on mouse drag direction and angle
- Ball velocity changes when colliding with the top and side walls
- Ball–brick collision handling for one, two, and three simultaneous brick collisions

While writing these tests, I identified a `if / if / else` logic bug in three-brick collision handling. When three bricks are hit at once, the code correctly invokes the three-brick handler, but then also incorrectly calls the one-brick handler. This causes unintended extra velocity changes.  

This issue is documented and exposed by the tests on the `master` branch and fixed on the `pytest` feature branch by restructuring the conditional logic to use an `if / elif / else` pattern.

These tests add value by validating the most complex and error-prone logic in the game and by addressing a defect in the code itself.

---

## Process

I began by reading through the existing `Ball` class to understand how movement, collisions, and angle calculations were implemented. I then designed tests around observable behaviors rather than internal implementation details.

I used pytest’s parameterization features to cover multiple scenarios efficiently, especially for the collision cases where behavior changes based on geometry or direction. For brick collisions, I created lightweight fake brick objects with only the required `rect` attribute so that collision logic could be tested.

After all tests were written and passing on the `master` branch (except for the known three-brick case), I created a `pytest` feature branch. On that branch, I applied a small fix to the collision handler logic and verified that the full test suite passed.

Tools used:
- Python
- pytest
- pygame (for Rect and collision geometry)
- Git and GitHub

---

## Challenges

The most significant challenge was understanding the brick collision logic, particularly how different numbers of simultaneous brick hits were handled. The code relies on geometric properties of rectangles and branching logic that is not immediately obvious.

Another challenge was that the one-brick collision handler assumes `ball.rect` exists, while the three-brick handler does not. This inconsistency caused an AttributeError during testing, which ultimately helped reveal the underlying `if / if / else` logic error. I addressed this by setting up the test state and by documenting the issue clearly in both the tests and this contribution.

---

## Learning

This contribution helped me better understand how to approach testing an existing codebase rather than code I wrote myself. In particular, I learned how important it is to test behavior at boundaries and edge cases, since that is often where bugs appear.

I also gained experience using feature branches. While my initial development occurred on the fork’s default branch, I moved the bug fix and final documentation to a dedicated `pytest` feature branch to better align with standard Git workflow practices (and assignment instructions).

Finally, I got some firsthand experience on how automated testing can reveal logic errors that can otherwise go unnoticed. In normal play, the `if / if / else` logic error would go unnoticed as draw would be constantly reassigning the required attribute that the testing environment did not create. 

---

## Future Work

There are several areas that could be improved further:

- Adding documentation or docstrings explaining the collision-handling rules more explicitly
- Altering the game controls such that the direction of travel of the ball aligns with the mouse controls rather than the opposite behavior (push towards instead of pull away)
- Expanding the testing suite to assess brick generation, countdown, and deletion

These improvements were intentionally left out of this contribution to keep the scope focused on unit testing and collision behavior.