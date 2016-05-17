width, height = Setup(
    minWidth=20,
    minHeight=26,
    xMargin=8,
    yMargin=8,
    transparentColour=(255, 0, 0)
)

Copy(0, 0, 8, 13, 0, 0)  # top left corner
Copy(9, 0, 7, 13, width - 7, 0)  # top right corner
Copy(0, 18, 8, 8, 0, height - 8)  # bottom left corner
Copy(9, 18, 7, 8, width - 7, height - 8)  # bottom right corner
Scale(0, 13, 8, 5, 0, 13, 8, height - 21)  # left border
Scale(8, 0, 1, 13, 8, 0, width - 15, 13)  # top border
Scale(8, 18, 1, 8, 8, height - 8, width - 15, 8)  # bottom border
Scale(9, 13, 7, 5, width - 7, 13, 7, height - 21)  # right border
Scale(8, 13, 1, 5, 8, 13, width - 14, height - 21)  # the center area
