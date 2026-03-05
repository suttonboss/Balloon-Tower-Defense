
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

# Final verification test
from main import Balloon, Tower, Projectile, PATH_POINTS, draw_path, draw_ui, BALLOON_REWARD, TOWER_COST, STARTING_LIVES, STARTING_MONEY

print("Final Verification Test")
print("=" * 50)

# Test all classes exist and work
tests_passed = 0
tests_total = 0

def test(name, condition):
    global tests_passed, tests_total
    tests_total += 1
    if condition:
        tests_passed += 1
        print(f"✓ {name}")
    else:
        print(f"✗ {name}")

# Test Balloon
try:
    b = Balloon(PATH_POINTS)
    test("Balloon can be created", True)
    test("Balloon has correct start position", (b.x, b.y) == PATH_POINTS[0])
    test("Balloon has correct health", b.health == 3)
    b.move()
    test("Balloon can move", b.x != PATH_POINTS[0][0] or b.y != PATH_POINTS[0][1])
    b.take_damage(1)
    test("Balloon can take damage", b.health == 2)
except Exception as e:
    print(f"✗ Balloon tests failed: {e}")

# Test Tower
try:
    t = Tower(400, 300)
    test("Tower can be created", True)
    test("Tower has correct position", (t.x, t.y) == (400, 300))
    test("Tower has correct range", t.range == 150)
    t.update()
    test("Tower can update", True)
except Exception as e:
    print(f"✗ Tower tests failed: {e}")

# Test Projectile
try:
    b = Balloon(PATH_POINTS)
    b.x = 500
    b.y = 500
    p = Projectile(400, 400, b)
    test("Projectile can be created", True)
    test("Projectile starts active", p.active == True)
    p.update()
    test("Projectile can update", True)
except Exception as e:
    print(f"✗ Projectile tests failed: {e}")

# Test PATH_POINTS
test("PATH_POINTS exists", len(PATH_POINTS) > 0)
test("PATH_POINTS has multiple points", len(PATH_POINTS) > 1)

# Test constants
test("BALLOON_REWARD defined", BALLOON_REWARD == 10)
test("TOWER_COST defined", TOWER_COST == 50)
test("STARTING_LIVES defined", STARTING_LIVES == 10)
test("STARTING_MONEY defined", STARTING_MONEY == 100)

# Test functions
test("draw_path function exists", callable(draw_path))
test("draw_ui function exists", callable(draw_ui))

print("=" * 50)
print(f"Tests passed: {tests_passed}/{tests_total}")

if tests_passed == tests_total:
    print("\n✓ All tests passed! Game is ready.")
else:
    print(f"\n✗ {tests_total - tests_passed} test(s) failed.")

pygame.quit()