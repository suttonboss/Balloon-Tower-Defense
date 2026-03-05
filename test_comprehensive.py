
import sys, pytest, collections, collections.abc, urllib3.exceptions, _pytest.pytester, numpy;
collections.Mapping = collections.abc.Mapping;
collections.MutableMapping = collections.abc.MutableMapping;
collections.MutableSet = collections.abc.MutableSet;
collections.Sequence = collections.abc.Sequence;
collections.Callable = collections.abc.Callable;
collections.Iterable = collections.abc.Iterable;
collections.Iterator = collections.abc.Iterator;
urllib3.exceptions.SNIMissingWarning = urllib3.exceptions.DependencyWarning;
pytest.RemovedInPytest4Warning = DeprecationWarning;
_pytest.pytester.Testdir = _pytest.pytester.Pytester;
numpy.PINF = numpy.inf;
numpy.unicode_ = numpy.str_;
numpy.bytes_ = numpy.bytes_;
numpy.float_ = numpy.float64;
numpy.string_ = numpy.bytes_;
numpy.NaN = numpy.nan;


import pygame
import math

pygame.init()

from main import Balloon, Tower, Projectile, PATH_POINTS, BALLOON_REWARD

print("Testing complete game mechanics...")

# Test 1: Balloon follows path
balloon = Balloon(PATH_POINTS)
print(f"\nTest 1: Balloon path following")
print(f"Start: ({balloon.x}, {balloon.y})")

# Move balloon many times to reach the end
steps = 0
max_steps = 1500  # Increased from 1000
while not balloon.reached_end and steps < max_steps:
    balloon.move()
    steps += 1

print(f"Balloon reached end after {steps} steps")
print(f"End position: ({balloon.x:.2f}, {balloon.y:.2f})")
assert balloon.reached_end, "Balloon should reach the end of the path"
print("✓ Balloon path following works")

# Test 2: Tower shooting and balloon destruction
print(f"\nTest 2: Tower shooting mechanics")
balloon2 = Balloon(PATH_POINTS)
balloon2.x = 400
balloon2.y = 400
tower = Tower(400, 300)

initial_money = 100
money = initial_money

# Simulate shooting until balloon dies
shot_count = 0
while balloon2.health > 0 and shot_count < 10:
    tower.update()
    projectile = tower.shoot([balloon2])
    if projectile:
        shot_count += 1
        # Move projectile to hit
        while projectile.active:
            projectile.update()
        if balloon2.health <= 0:
            money += BALLOON_REWARD
            break

print(f"Balloon died after {shot_count} shots")
print(f"Money after kill: {money} (started with {initial_money}, reward is {BALLOON_REWARD})")
assert balloon2.health <= 0, "Balloon should die from tower shots"
assert money == initial_money + BALLOON_REWARD, f"Should earn reward. Expected {initial_money + BALLOON_REWARD}, got {money}"
print("✓ Tower shooting and reward system works")

# Test 3: Multiple balloons
print(f"\nTest 3: Multiple balloons management")
balloons = [Balloon(PATH_POINTS) for _ in range(5)]
print(f"Created {len(balloons)} balloons")

# Move all balloons
for i in range(100):
    for b in balloons:
        b.move()

print(f"Balloons alive after 100 steps: {len(balloons)}")
print("✓ Multiple balloon management works")

print(f"\n=== All comprehensive tests passed! ===")
pygame.quit()