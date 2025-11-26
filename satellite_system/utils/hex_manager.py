import h3

def singleton(cls):
    _instances = None

    def return_obj(*args, **kwargs):
      nonlocal _instances
      if _instances is None:
        _instances = cls(*args, **kwargs)
      else:
        _instances.__init__(*args, **kwargs)
      return _instances

    return return_obj

@singleton
class HexManager:
  cells = {}

  def __get_all_cells(self, res : int) -> set[str]:
    return h3.uncompact_cells(h3.get_res0_cells(), res)

  def __get_all_centers(self, cells : set[str]) -> list[tuple[float, float]]:
    centers = []

    for i in cells:
      centers.append(h3.cell_to_latlng(i))

    return centers

  def get_centers(self, resolution: int) -> list[tuple[float, float]]:
    if (resolution in self.cells):
      return cells[resolution]

    self.cells[resolution] = self.__get_all_centers(self.__get_all_cells(resolution))

    return self.cells[resolution]
