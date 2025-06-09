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
        fs=22,
        hbuff=0,
        vbuff=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        data = data or [[""]]

        self.cols = len(data[0])
        self.rows = len(data)
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

            cell_groups.append((cell_grp, old_val, new_val))
            if animate:
                animations += [AnimationGroup(FadeOut(old_val), FadeIn(new_val))]

        if animate:
            if sequential:
                for anim in animations:
                    scene.play(anim, run_time=delay)
            else:
                scene.play(*animations, run_time=delay)

        for cell_grp, old_val, new_val in cell_groups:
            cell_grp.remove(old_val)
            cell_grp.add(new_val)

            scene.add(new_val)
            scene.remove(old_val)

    def highlight_cell(self, scene, *cells, color=ORANGE, sequential=True, delay=0.2):
        animations = [self.get_cell(cell).animate.set_fill(color) for cell in cells]
        if sequential:
            for anim in animations:
                scene.play(anim, run_time=delay)
        else:
            scene.play(*animations, run_time=delay)


class HexBinDecTable(Grid):
    def __init__(self, **kwargs):
        data = [["Decimal", "Hex", "Binary"]]
        for i in range(16):
            data += [[str(i), format(i, "X"), format(i, "04b")]]
        super().__init__(data=data, **kwargs)


class BitwiseOrTable(Grid):
    def __init__(self, width=3, height=2.2, fs=18, **kwargs):
        data = [["A", "B", "A | B"], [0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        super().__init__(data=data, width=width, height=height, fs=fs, **kwargs)


class BitwiseAndTable(Grid):
    def __init__(self, width=3, height=2.2, fs=18, **kwargs):
        data = [["A", "B", "A & B"], [0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        super().__init__(data=data, width=width, height=height, fs=fs, **kwargs)


class BitwiseXorTable(Grid):
    def __init__(self, width=3, height=2.2, fs=18, **kwargs):
        data = [["A", "B", "A ^ B"], [0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        super().__init__(data=data, width=width, height=height, fs=fs, **kwargs)


class Array(Grid):
    def __init__(
        self,
        data=None,
        cell_width=0.8,
        cell_height=0.7,
        fs=22,
        index_ltr=True,
        index_dir_up=True,
        **kwargs,
    ):
        data = data or [""]
        super().__init__(
            data=[data],
            width=cell_width * len(data),
            height=cell_height,
            fs=fs,
            **kwargs,
        )

        self.index_ltr = index_ltr
        self.indices = VGroup()
        self.array = VGroup()

        indices = range(len(data)) if index_ltr else reversed(range(len(data)))
        index_dir_up = UP if index_dir_up else DOWN

        for idx, index in enumerate(indices):
            idx_label = Text(str(index), font_size=fs * 0.7).next_to(
                self.get_cell((0, idx)), index_dir_up, buff=0.2
            )
            self.indices.add(idx_label)

        self.array.add(self.grid, self.indices)
        self.add(self.array)

    def get_bit_group(self, bit):
        bit = bit if self.index_ltr else (self.cols - bit - 1)
        return VGroup(self.array[0][0][bit], self.array[1][bit])

    def get_bit(self, bit):
        return self.get_bit_group(bit)[0][0]

    def get_bit_value(self, bit):
        return self.get_bit_group(bit)[0][1]

    def get_bit_index(self, bit):
        return self.get_bit_group(bit)[1]

    def update_bit(
        self,
        scene,
        *bits,
        labels=None,
        fill="",
        animate=True,
        sequential=True,
        delay=0.2,
    ):
        cells = [(0, bit if self.index_ltr else self.cols - bit - 1) for bit in bits]
        self.update_cell(
            scene,
            *cells,
            labels=labels,
            fill=fill,
            animate=animate,
            sequential=sequential,
            delay=delay,
        )

    def highlight_bit(self, scene, *bits, color=ORANGE, sequential=True, delay=0.2):
        cells = [(0, bit if self.index_ltr else self.cols - bit - 1) for bit in bits]
        self.highlight_cell(
            scene, *cells, color=color, sequential=sequential, delay=delay
        )

    def highlight_n_bit(
        self, scene, n=None, ltr=True, color=ORANGE, sequential=True, delay=0.2
    ):
        n = n or self.cols - 1
        bits = None
        if self.index_ltr:
            bits = range(n) if ltr else range(self.cols - n, self.cols)
        else:
            bits = (
                range(self.cols - 1, self.cols - n - 1, -1) if ltr else range(0, n, 1)
            )
        self.highlight_bit(
            scene, *bits, color=color, sequential=sequential, delay=delay
        )

    def update_n_bit(
        self,
        scene,
        n=None,
        ltr=True,
        labels=None,
        fill="",
        sequential=True,
        animate=True,
        delay=0.2,
    ):
        n = n or self.cols - 1
        bits = None
        if self.index_ltr:
            bits = range(n) if ltr else range(self.cols - n, self.cols)
        else:
            bits = (
                range(self.cols - 1, self.cols - n - 1, -1) if ltr else range(0, n, 1)
            )
        self.update_bit(
            scene,
            *bits,
            labels=labels,
            fill=fill,
            animate=animate,
            sequential=sequential,
            delay=delay,
        )

    def left_shift(self, scene, n=1, sequential=True, delay=0.2):
        ss = n if self.index_ltr else self.cols - n - 1
        se = self.cols if self.index_ltr else -1
        st = 1 if self.index_ltr else -1
        animations = []
        for i in range(ss, se, st):
            target = i - n if self.index_ltr else i + n
            animations += [
                AnimationGroup(
                    self.get_bit_value(i).animate.move_to(
                        self.get_bit(target).get_center()
                    )
                )
            ]

        if sequential:
            for anim in animations:
                scene.play(anim, run_time=delay)
        else:
            scene.play(*animations, run_time=delay)

        labels = [str(self.get_bit_value(i).text) for i in range(ss, se, st)]
        bits = range(self.cols) if self.index_ltr else range(self.cols - 1, -1, -1)
        print(labels)
        print(list(bits))
        self.update_bit(scene, *bits, labels=labels, animate=False)

    def right_shift(self, scene, n=1, sequential=True, delay=0.2):
        ss = self.cols - n - 1 if self.index_ltr else n
        se = -1 if self.index_ltr else self.cols
        st = -1 if self.index_ltr else 1
        animations = []
        for i in range(ss, se, st):
            target = i + n if self.index_ltr else i - n
            animations += [
                AnimationGroup(
                    self.get_bit_value(i).animate.move_to(
                        self.get_bit(target).get_center()
                    )
                )
            ]

        if sequential:
            for anim in animations:
                scene.play(anim, run_time=delay)
        else:
            scene.play(*animations, run_time=delay)

        labels = [str(self.get_bit_value(i).text) for i in range(ss, se, st)]
        bits = (
            range(self.cols - 1, -1, -1) if self.index_ltr else range(0, self.cols, 1)
        )
        print(labels)
        print(list(bits))
        self.update_bit(scene, *bits, labels=labels, animate=False)


class Demo(Scene):
    def construct(self):
        orTable = BitwiseOrTable(fs=44).scale(0.4).to_edge(UL)
        andTable = BitwiseAndTable(width=2.5, height=2.5).to_edge(UR)
        xorTable = BitwiseXorTable(width=2.5, height=2.5).to_edge(DL)
        tbl = HexBinDecTable()

        self.add(orTable)
        self.add(andTable)
        self.add(xorTable)
        self.wait(2)

        a = Array(data=[1, 2, 3, 4, 5, 6, 7, 8], index_ltr=False)
        self.play(Write(a))
        self.wait(2)

        # a.update_bit(self, *range(8), fill="A", animate=False)
        # self.wait(1)

        a.highlight_n_bit(self, n=3, ltr=False)
        # a.highlight_bit(self, 0, 1, 2)
        a.update_n_bit(self, ltr=False, n=3)
        # a.update_bit(self, 7, 6, 5)
        # a.update_bit(self, 0, 1, 2)
        self.wait(1)
        # a.left_shift(self, n=3, sequential=True)
        a.right_shift(self, n=3, sequential=False)
        self.wait(1)

        self.play(a.get_bit_group(0).animate.to_edge(UL))
        self.play(a.get_bit_group(1).animate.to_edge(UR))
        self.play(a.get_bit_group(2).animate.to_edge(DL))
        self.play(a.get_bit_group(3).animate.to_edge(DR))
        self.play(a.get_bit_group(4).animate.to_edge(UP))
        self.play(a.get_bit_group(5).animate.to_edge(DOWN))
        self.play(a.get_bit_group(6).animate.to_edge(LEFT))
        self.play(a.get_bit_group(7).animate.to_edge(RIGHT))

        self.play(a.get_bit(0).animate.move_to(ORIGIN))
        self.play(a.get_bit_value(0).animate.move_to(ORIGIN))
        self.play(a.get_bit_index(0).animate.move_to(ORIGIN))
        self.wait(1)

        # arr = Grid(width=6, height=0.7, data=[[0, 10, 20, 30, 40, 50, 60, 70]])
        # self.play(Write(arr))
        # self.wait(1)
        #
        # arr.highlight_cell(self, (0, 0), (0, 1), (0, 2))
        # arr.update_cell(self, (0, 0), (0, 1), (0, 2), animate=False)
        # arr.highlight_cell(self, (0, 0), (0, 1), (0, 2), color=BLACK, sequential=False)
        #
        # ss = 3
        # se = 8
        # st = 1
        # animations = []
        # sequential = False
        # for i in range(ss, se, st):
        #     animations += [
        #         AnimationGroup(
        #             arr.get_cell_value((0, i)).animate.move_to(
        #                 arr.get_cell((0, i - ss)).get_center()
        #             )
        #         )
        #     ]
        # self.play(
        #     arr.get_cell_value((0, i)).animate.move_to(
        #         arr.get_cell((0, i - ss)).get_center()
        #     )
        # )
        # arr.update_cell(
        #     self, (0, i - ss), fill=str(arr.get_cell_value((0, i)).text)
        # )
        # arr.update_cell(self, (0, i))
        # if sequential:
        #     for anim in animations:
        #         self.play(anim, run_time=0.2)
        # else:
        #     self.play(*animations, run_time=0.2)

        # labels = []
        # for i in range(ss, se, st):
        #     labels.append(str(arr.get_cell_value((0, i)).text))
        # arr.update_cell(
        #     self,
        #     (0, 0),
        #     (0, 1),
        #     (0, 2),
        #     (0, 3),
        #     (0, 4),
        #     (0, 5),
        #     (0, 6),
        #     (0, 7),
        #     labels=labels,
        # )
        # self.wait(1)
        # arr.update_cell(self, (0, 5), (0, 6), (0, 7), fill="0")
        # self.wait(1)
        #
        # self.play(arr.get_cell_group((0, 0)).animate.to_edge(UL))
        # self.play(arr.get_cell_group((0, 1)).animate.to_edge(UR))
        # self.play(arr.get_cell_group((0, 2)).animate.to_edge(DL))
        # self.play(arr.get_cell_group((0, 3)).animate.to_edge(DR))
        # self.play(arr.get_cell_group((0, 4)).animate.to_edge(UP))
        # self.play(arr.get_cell_group((0, 5)).animate.to_edge(DOWN))
        # self.play(arr.get_cell_group((0, 6)).animate.to_edge(RIGHT))
        # self.play(arr.get_cell_group((0, 7)).animate.to_edge(LEFT))
        #
        # self.wait(2)
