from dataclasses import dataclass


@dataclass
class EditUIState:
    """
    Keeps information about state of edit view UI
    """
    draw_grid: bool = True
    show_background: bool = True
    shape_loaded: bool = False
    edit: bool = True
    dragging: bool = False
    dragged_point_index: int | None = None
