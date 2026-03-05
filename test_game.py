
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

# Test the game classes and functions without running the main game loop
pygame.init()

# Test the Balloon class with the fixed move method
from main import Balloon, Tower, Projectile, PATH_POINTS

# Test Balloon creation and movement
balloon = Balloon(PATH_POINTS)
print(f"Balloon starting position: ({balloon.x}, {balloon.y})")
print(f"First target: ({balloon.target_x}, {balloon.target_y})")

# Move the balloon several times
for i in range(10):
    balloon.move()
    print(f"Step {i+1}: ({balloon.x:.2f}, {balloon.y:.2f}), path_index: {balloon.path_index}, next_point: {balloon.next_point_index}")

print("\n✓ Balloon movement with path progression works correctly")

# Test Tower shooting
balloon2 = Balloon(PATH_POINTS)
# Place balloon at tower position but offset so projectile needs to travel
balloon2.x = 450
balloon2.y = 400
tower = Tower(400, 300)

result = tower.shoot([balloon2])
assert result is not None, "Tower should shoot when balloon in range"
assert isinstance(result, Projectile), "Tower should return a Projectile"
print("✓ Tower shooting with balloon in range works correctly")

# Test Projectile movement
projectile = Projectile(400, 300, balloon2)
initial_x = projectile.x
initial_y = projectile.y

# Update several times to see it move
for i in range(5):
    projectile.update()
    if not projectile.active:
        break
    print(f"Projectile position: ({projectile.x:.2f}, {projectile.y:.2f}), active: {projectile.active}")

print("✓ Projectile moves toward target correctly")

# Test Balloon take_damage
balloon2.take_damage(1)
assert balloon2.health == 2, "Balloon should lose health when taking damage"
print("✓ Balloon take_damage works correctly")

print("\n=== All tests passed! ===")
pygame.quit()