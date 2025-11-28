import h3
from typing import List, Set, Tuple
from .singleton import singleton

@singleton
class HexManager:
  def __init__(self):
      self.cells = {}

  def __get_all_cells(self, res : int) -> Set[str]:
      return h3.uncompact_cells(h3.get_res0_cells(), res)

  def __get_all_centers(self, cells : Set[str]) -> List[Tuple[float, float]]:
      centers = []

      for i in cells:
          centers.append(h3.cell_to_latlng(i))

      return centers

  def get_centers(self, resolution: int) -> List[Tuple[float, float]]:
      if (resolution >= 7):
          raise ValueError("Поддерживается разрешение не более 6")

      if (resolution in self.cells):
          return self.cells[resolution]

      self.cells[resolution] = self.__get_all_centers(self.__get_all_cells(resolution))

      return self.cells[resolution]
