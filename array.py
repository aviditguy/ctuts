from manim import *
from .grid import Grid


class Array(Grid):
    def __init__(
        self,
        cell_width=0.8,
        cell_height=0.7,
        data=None,
        fs=24,
        index_ltr=True,
        index_dir_up=False,
        index_from=0,
        index_step=1,
        **kwargs,
    ):
        data = data or [" "]
        super().__init__(
            width=cell_width * len(data),
            height=cell_height,
            data=[data],
            fs=fs,
            **kwargs,
        )

        self.index_ltr = index_ltr
        self.indices = VGroup()
        self.array = VGroup()

        indices = range(index_from, index_from + len(data) * index_step, index_step)
        indices = indices if index_ltr else reversed(indices)
        index_dir_up = UP if index_dir_up else DOWN

        for idx, index in enumerate(indices):
            index_label = Text(str(index), font_size=fs * 0.7).next_to(
                self.get_cell(0, idx), index_dir_up, buff=0.2
            )
            self.indices.add(index_label)

        self.array.add(self.grid, self.indices)
        self.add(self.array)

    def get_bit(self, bit):
        bit = bit if self.index_ltr else (self.cols - 1 - bit)
        return VGroup(self.get_cell(0, bit), self.indices[bit])

    def get_bit_rect(self, bit):
        return self.get_bit(bit)[0][0]

    def get_bit_label(self, bit):
        return self.get_bit(bit)[0][1]

    def update_bit(
        self,
        scene,
        *bits,
        labels=None,
        fill=" ",
        animate=True,
        sequential=True,
        delay=0.2,
    ):
        cells = [(0, bit if self.index_ltr else (self.cols - 1 - bit)) for bit in bits]
        self.update_cell(
            scene,
            *cells,
            labels=labels,
            fill=fill,
            animate=animate,
            sequential=sequential,
            delay=delay,
        )

    def highlight_bit(
        self,
        scene,
        *bits,
        colors=None,
        fill=ORANGE,
        animate=True,
        sequential=True,
        delay=0.2,
    ):
        cells = [(0, bit if self.index_ltr else (self.cols - 1 - bit)) for bit in bits]
        self.highlight_cell(
            scene,
            *cells,
            colors=colors,
            fill=fill,
            animate=animate,
            sequential=sequential,
            delay=delay,
        )

    def swap_bit(self, scene, bit1, bit2, delay=1.5):
        arcUp = ArcBetweenPoints(
            start=self.get_bit_rect(bit1).get_center(),
            end=self.get_bit_rect(bit2).get_center(),
            angle=-PI,
        )
        arcDown = ArcBetweenPoints(
            start=self.get_bit_rect(bit2).get_center(),
            end=self.get_bit_rect(bit1).get_center(),
            angle=-PI,
        )

        l1 = (
            self.get_bit_label(bit1)
            .copy()
            .move_to(self.get_bit_rect(bit1).get_center())
        )
        l2 = (
            self.get_bit_label(bit2)
            .copy()
            .move_to(self.get_bit_rect(bit2).get_center())
        )

        self.add(l1, l2)
        self.update_bit(scene, bit1, bit2, animate=False)

        scene.play(
            MoveAlongPath(l1, arcUp),
            MoveAlongPath(l2, arcDown),
            run_time=delay,
        )

        scene.remove(l1, l2)
        self.update_bit(scene, bit1, bit2, labels=[l2.text, l1.text], animate=False)

    def shift_bit(self, scene, start, end, to, sequential=True, delay=0.2):
        end = end - 1 if start > end else end + 1
        step = -1 if start > end else 1

        srcbits = list(range(start, end, step))
        dstbits = list(range(to, to + len(srcbits) * step, step))
        labels = [self.get_bit_label(bit).text for bit in srcbits]

        animations = []
        for srcbit, dstbit in zip(srcbits, dstbits):
            animations.append(
                self.get_bit_label(srcbit).animate.move_to(
                    self.get_bit_rect(dstbit).get_center()
                )
            )
        if sequential:
            for anim in animations:
                scene.play(anim, run_time=delay)
        else:
            scene.play(*animations, run_time=delay)

        self.update_bit(scene, *srcbits, animate=False)
        self.update_bit(scene, *dstbits, labels=labels, animate=False)

    def swap_and_shift_bit(self, scene, swapfrom, swapto):
        arc_angle = PI if swapfrom > swapto else -PI

        arcup = ArcBetweenPoints(
            start=self.get_bit_rect(swapfrom).get_center(),
            end=self.get_bit_rect(swapto).get_center(),
            angle=arc_angle,
        )

        swapto = swapto - 1 if swapfrom > swapto else swapto + 1
        step = -1 if swapfrom > swapto else 1

        bits = range(swapfrom, swapto, step)
        srcbits = range(swapfrom + step, swapto, step)
        dstbits = range(swapfrom, swapfrom + len(srcbits) * step, step)

        animations = []
        for srcbit, dstbit in zip(srcbits, dstbits):
            animations.append(
                self.get_bit_label(srcbit).animate.move_to(
                    self.get_bit_rect(dstbit).get_center()
                )
            )

        scene.play(MoveAlongPath(self.get_bit_label(swapfrom), arcup), *animations)

        labels = [self.get_bit_label(bit).text for bit in srcbits]
        labels.append(self.get_bit_label(swapfrom).text)
        self.update_bit(scene, *bits, labels=labels, animate=False)
