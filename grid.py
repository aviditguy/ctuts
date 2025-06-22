from manim import *


class Grid(VGroup):
    def __init__(
        self,
        width=7,
        height=6,
        data=None,
        fs=24,
        hbuff=0,
        vbuff=0,
        color=BLACK,
        opacity=1,
        stroke=WHITE,
        **kwargs,
    ):
        super().__init__(**kwargs)

        data = data or [[" "]]

        self.rows = len(data)
        self.cols = len(data[0])
        self.fs = fs
        self.grid = VGroup()

        for drow in data:
            grid_row = VGroup()
            for cell in drow:
                rect = Rectangle(
                    width=width / self.cols,
                    height=height / self.rows,
                    color=color,
                    fill_opacity=opacity,
                    stroke_color=stroke,
                )
                label = Text(str(cell), font_size=fs, z_index=1).move_to(
                    rect.get_center()
                )
                grid_row.add(VGroup(rect, label))
            grid_row.arrange(RIGHT, buff=hbuff)
            self.grid.add(grid_row)
        self.grid.arrange(DOWN, buff=vbuff)

        self.add(self.grid)

    def get_cell(self, row, col):
        return self.grid[row][col]

    def get_cell_rect(self, row, col):
        return self.get_cell(row, col)[0]

    def get_cell_label(self, row, col):
        return self.get_cell(row, col)[1]

    def get_row(self, row):
        return VGroup(self.get_cell(row, col) for col in range(self.cols))

    def get_col(self, col):
        return VGroup(self.get_cell(row, col) for row in range(self.rows))

    def update_cell(
        self,
        scene,
        *cells,
        labels=None,
        fill=" ",
        animate=True,
        sequential=True,
        delay=0.2,
    ):
        labels = labels or []
        labels += [fill] * (len(cells) - len(labels))

        animations = []
        cellgroup = []

        for (row, col), label in zip(cells, labels):
            cell = self.get_cell(row, col)
            old_label = self.get_cell_label(row, col)
            new_label = Text(str(label), font_size=self.fs, z_index=1).move_to(
                self.get_cell_rect(row, col).get_center()
            )

            cellgroup.append((cell, old_label, new_label))
            if animate:
                animations.append(AnimationGroup(FadeOut(old_label), FadeIn(new_label)))

        if animate:
            if sequential:
                for anim in animations:
                    scene.play(anim, run_time=delay)
            else:
                scene.play(*animations, run_time=delay)

        for cell, old_label, new_label in cellgroup:
            cell.remove(old_label)
            cell.add(new_label)

            scene.remove(old_label)
            scene.add(new_label)

    def highlight_cell(
        self,
        scene,
        *cells,
        colors=None,
        fill=ORANGE,
        animate=False,
        sequential=False,
        delay=0.2,
    ):
        if colors is None:
            colors = [fill] * len(cells)
        elif isinstance(colors, list):
            colors += [fill] * (len(cells) - len(colors))
        else:
            colors = [colors] * len(cells)

        animations = []
        for (row, col), color in zip(cells, colors):
            rect = self.get_cell_rect(row, col)
            if animate:
                animations.append(rect.animate.set_fill(color))
            else:
                rect.set_fill(color)

        if animate:
            if sequential:
                for anim in animations:
                    scene.play(anim, run_time=delay)
            else:
                scene.play(*animations, run_time=delay)
