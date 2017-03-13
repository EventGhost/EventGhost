# flake8: noqa

width, height = Setup(
    minWidth=18,
    minHeight=18,
    xMargin=12,
    yMargin=12,
)

Scale(5, 5, 1, 1, 0, 0, width, height)  # the center area
Scale(0, 0, 3, 3, 0, 0, 3, height - 3)  # left border
Scale(0, 0, 3, 3, 0, 0, width, 3)  # top border
Scale(0, 0, 3, 3, 0, height -3, width, 3)  # bottom border
Scale(0, 0, 3, 3, width - 3, 0, 3, height)  # right border
