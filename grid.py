from manim import *


class Grid(VGroup):
    def __init__(
        self,
        width=6,
        height=7,
        data=None,
        color=BLACK,
        opacity=1,
        stroke=WHITE,
        hbuff=0,
        vbuff=0,
        fs=22,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.data = data or [[""]]
        self.rows = len(data)
        self.cols = len(data[0])
        self.cell_width = width / self.cols
        self.cell_height = height / self.rows
        self.color = color
        self.opacity = opacity
        self.stroke = stroke
        self.fs = fs
        self.hbuff = hbuff
        self.vbuff = vbuff
        self.grid = VGroup()

        for drow in data:
            grid_row = VGroup()
            for cell in drow:
                rect = Rectangle(
                    width=self.cell_width,
                    height=self.cell_height,
                    color=color,
                    fill_opacity=opacity,
                    stroke_color=stroke,
                )
                label = Text(str(cell), font_size=fs).move_to(rect.get_center())
                grid_row.add(VGroup(rect, label))
            grid_row.arrange(RIGHT, buff=hbuff)
            self.grid.add(grid_row)
        self.grid.arrange(DOWN, buff=vbuff)
        self.add(self.grid)

    def get_cell_group(self, cell=(0, 0)):
        return self.grid[cell[0]][cell[1]]

    def get_cell(self, cell=(0, 0)):
        return self.get_cell_group(cell)[0]

    def get_cell_value(self, cell=(0, 0)):
        return self.get_cell_group(cell)[1]

    def update_cell(
        self,
        scene,
        *cells,
        labels=None,
        fill="",
        sequential=True,
        delay=0.2,
        animate=True,
    ):
        labels = labels or []
        labels += [fill] * (len(cells) - len(labels))

        animations = []
        cell_groups = []

        for idx, cell in enumerate(cells):
            cell_grp = self.get_cell_group(cell)
            old_val = self.get_cell_value(cell)
            new_val = Text(str(labels[idx]), font_size=self.fs).move_to(
                self.get_cell(cell).get_center()
            )

            if animate:
                cell_groups.append((cell_grp, old_val, new_val))
                animations += [AnimationGroup(FadeOut(old_val), FadeIn(new_val))]
            else:
                cell_grp.remove(old_val)
                cell_grp.add(new_val)

        if animate:
            if sequential:
                for anim in animations:
                    scene.play(anim, run_time=delay)
            else:
                scene.play(*animations, run_time=delay)

            for cell_grp, old_val, new_val in cell_groups:
                cell_grp.remove(old_val)
                cell_grp.add(new_val)
        else:
            scene.add(self)

    def highlight_cell(self, scene, *cells, color=ORANGE, sequential=True, delay=0.2):
        animations = [self.get_cell(cell).animate.set_fill(color) for cell in cells]
        if sequential:
            for anim in animations:
                scene.play(anim, run_time=delay)
        else:
            scene.play(*animations, run_time=delay)


class Demo(Scene):
    def construct(self):
        grid = Grid(
            data=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        )
        self.play(Write(grid))
        self.wait(1)

        grid.highlight_cell(self, (0, 0), (0, 3), (3, 3), (3, 0))
        grid.highlight_cell(
            self, (1, 1), (1, 2), (2, 1), (2, 2), color=GREEN, sequential=False
        )

        grid.update_cell(self, (0, 0), (1, 0), delay=0.5, sequential=False)
        self.wait(1)

        self.play(
            grid.get_cell_value((2, 0)).animate.move_to(
                grid.get_cell((0, 0)).get_center()
            )
        )
        self.play(
            grid.get_cell_value((3, 0)).animate.move_to(
                grid.get_cell((1, 0)).get_center()
            )
        )

        grid.update_cell(self, (0, 0), fill=grid.get_cell_value((2, 0)).text)
        grid.update_cell(self, (2, 0), animate=False)

        grid.update_cell(self, (1, 0), fill=grid.get_cell_value((3, 0)).text)
        grid.update_cell(self, (3, 0), animate=False)

        self.play(grid.get_cell_group((0, 0)).animate.to_edge(UL))

        self.wait(1)


class BitwiseOrTable(Grid):
    def __init__(self, **kwargs):
        data = [["A", "B", "A | B"], [0, 0, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
        super().__init__(data=data, **kwargs)
