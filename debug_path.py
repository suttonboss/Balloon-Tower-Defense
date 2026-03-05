
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
pygame.init()
from main import Balloon, PATH_POINTS

balloon = Balloon(PATH_POINTS)
print(f"Path has {len(PATH_POINTS)} points")
print(f"Path points: {PATH_POINTS}")
print(f"\nBalloon start: ({balloon.x}, {balloon.y})")
print(f"Initial path_index: {balloon.path_index}, next_point_index: {balloon.next_point_index}")

# Track progress
for i in range(20):
    balloon.move()
    if balloon.reached_end:
        print(f"Reached end at step {i}")
        break
    if balloon.path_index != balloon.next_point_index - 1:
        print(f"Step {i}: path_index={balloon.path_index}, next_point_index={balloon.next_point_index}")
        print(f"  Position: ({balloon.x:.2f}, {balloon.y:.2f})")

print(f"\nAfter 20 steps:")
print(f"Position: ({balloon.x:.2f}, {balloon.y:.2f})")
print(f"path_index: {balloon.path_index}, next_point_index: {balloon.next_point_index}")
print(f"Reached end: {balloon.reached_end}")

# Let it run longer and check
steps = 20
while not balloon.reached_end and steps < 2000:
    balloon.move()
    steps += 1
    if steps % 200 == 0:
        print(f"Step {steps}: ({balloon.x:.2f}, {balloon.y:.2f}), path_index={balloon.path_index}")

print(f"\nFinal: steps={steps}, reached_end={balloon.reached_end}")
pygame.quit()