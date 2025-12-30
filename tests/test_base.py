import math
import pytest
from satellite_system.coordinator import Coordinator
coordinator = Coordinator()

EARTH_RADIUS_M = 6371e3

def analytic_coverage(satel: int, altitude: float, angle: float) -> float:
  """Analytical assessment of Earth's satellite coverage.

  Args:
      satel (int): number of satellites
      altitude (float): orbit altitude, meters
      fov_deg (float): full field of view, degrees

  Returns:
      float: Earth coverage
  """
  R = EARTH_RADIUS_M

  theta = math.radians(angle)

  cos_psi = (R / (R + altitude)) * math.sin(theta)

  psi = math.asin(cos_psi)

  area_one = 2 * math.pi * R**2 * (1 - math.cos(psi - theta))
  earth_area = 4 * math.pi * R**2

  return (satel * area_one) / earth_area

def coverage(height, orb_inclin, longitude_asc, count_orb, count_sat, angle, res):
  """
  Comparison of project code coverage and test results
  """
  group_number = coordinator.add_group(f"{height} {orb_inclin} {longitude_asc} {count_orb} {count_sat} 3 0 2024-01-15 14:30:45.123456 {angle}".split())

  coverage_code = coordinator.calculate_coverage(f"{group_number} {res} 2024-01-15 14:30:45.123456".split())

  coverage_analytic = analytic_coverage(count_sat, height * 1000, angle)

  error = (abs(coverage_code - coverage_analytic) / coverage_code) * 100

  print(f"Coverage (code): {coverage_code * 100:.3g}%")
  print(f"Coverage (test): {coverage_analytic * 100:.3g}%")
  print(f"Error: {error}%")

  assert error <= 100

def test_coverage_1():
  coverage(500, 45, 45, 4, 16, 20, 4)

def test_coverage_2():
  coverage(300, 20, 12, 1, 1, 20, 3)

def test_coverage_3():
  coverage(700, 70, 3, 2, 8, 20, 4)

def test_coverage_4():
  coverage(1000, 54, 124, 3, 6, 20, 4)

def test_coverage_5():
  coverage(600, 25, 350, 4, 16, 20, 4)
