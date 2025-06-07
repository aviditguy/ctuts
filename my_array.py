from manim import *
from grid import Grid


class Array(Grid):
    def __init__(
        self,
        data=None,
        cell_width=0.7,
        cell_height=0.5,
        index=True,
        index_ltr=True,
        index_dir="UP",
        index_color=WHITE,
        fs=22,
        **kwargs,
    ):
        data = data or [""]
        self.index_ltr = index_ltr
        self.array = VGroup()
        self.indices = None

        super().__init__(
            data=[data],
            width=cell_width * len(data),
            fs=fs,
            height=cell_height,
            **kwargs,
        )

        self.array.add(self.grid)

        if index:
            self.indices = VGroup()
            indices = (
                list(range(len(data)))
                if index_ltr
                else list(reversed(range(len(data))))
            )

            dir = DOWN if index_dir is "DOWN" else UP
            for idx, label in enumerate(indices):
                index_label = Text(str(label), color=index_color, font_size=fs * 0.8)
                index_label.next_to(self.get_cell((0, idx)), dir, buff=0.1)
                self.indices.add(index_label)

            self.array.add(self.indices)

        self.add(self.array)

    def get_bit_group(self, index):
        index = index if self.index_ltr else self.cols - 1 - index
        return VGroup(self.array[0][0][index], self.array[1][index])

    def get_bit(self, index):
        return self.get_bit_group(index)[0][0]

    def get_bit_value(self, index):
        return self.get_bit_group(index)[0][1]

    def get_bit_index(self, index):
        return self.get_bit_group(index)[1]

    def update_bit(
        self,
        scene,
        *bits,
        labels=None,
        fill="",
        sequential=True,
        delay=0.2,
        animate=True,
    ):
        cells = [(0, bit) for bit in bits]
        if self.index_ltr == False:
            cells = []
            for bit in bits:
                cells.append((0, self.cols - bit - 1))

        self.update_cell(
            scene,
            *cells,
            labels=labels,
            fill=fill,
            sequential=sequential,
            delay=delay,
            animate=animate,
        )

    def update_n_bit(
        self,
        scene,
        n=1,
        labels=None,
        fill="",
        sequential=True,
        delay=0.2,
        animate=True,
        ltr=True,
    ):
        cells = [
            (0, bit) for bit in (range(n) if ltr else range(self.cols - n, self.cols))
        ]
        self.update_cell(
            scene,
            *cells,
            labels=labels,
            fill=fill,
            sequential=sequential,
            delay=delay,
            animate=animate,
        )

    def highlight_bit(self, scene, *bits, color=ORANGE, sequential=True, delay=0.2):
        cells = [(0, bit) for bit in bits]
        if self.index_ltr == False:
            cells = []
            for bit in bits:
                cells.append((0, self.cols - 1 - bit))
        self.highlight_cell(
            scene, *cells, color=color, sequential=sequential, delay=delay
        )

    def highlight_n_bit(
        self, scene, n=1, color=ORANGE, ltr=True, sequential=True, delay=0.2
    ):
        cells = [
            (0, bit) for bit in (range(n) if ltr else range(self.cols - n, self.cols))
        ]
        self.highlight_cell(
            scene, *cells, color=color, sequential=sequential, delay=delay
        )

    def left_shift(self, scene, n=1, delay=0.2):
        ss = n if self.index_ltr else self.cols - n - 1
        se = self.cols if self.index_ltr else -1
        st = 1 if self.index_ltr else -1
        for idx in range(ss, se, st):
            target = idx - n if self.index_ltr else idx + n

            scene.play(
                self.get_bit_value(idx).animate.move_to(
                    self.get_bit(target).get_center()
                ),
                run_time=delay,
            )
            self.update_bit(scene, target, idx, labels=[self.get_bit_value(idx).text])

    def right_shift(self, scene, n=1, delay=0.2):
        ss = self.cols - n - 1 if self.index_ltr else n
        se = -1 if self.index_ltr else self.cols
        st = -1 if self.index_ltr else 1
        for idx in range(ss, se, st):
            target = idx + n if self.index_ltr else idx - n

            scene.play(
                self.get_bit_value(idx).animate.move_to(
                    self.get_bit(target).get_center()
                ),
                run_time=delay,
            )
            self.update_bit(scene, target, idx, labels=[self.get_bit_value(idx).text])
