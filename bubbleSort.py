from manim import *
from helper.array import Array


class BubbleSort(Scene):
    def construct(self):
        data = [12, 25, 11, 9, 17]
        n = len(data)

        arr = Array(data=data, index_dir_up=False)
        ilabel = Text("i", font_size=16).next_to(arr.get_bit(0), DOWN, buff=0.2)
        jlabel = Text("j", font_size=16).next_to(arr.get_bit(0), UP, buff=0.2)
        j1label = Text("j+1", font_size=16).next_to(arr.get_bit(1), UP, buff=0.2)

        self.add(arr, ilabel, jlabel, j1label)
        self.wait(1)

        for i in range(n - 1):

            for j in range(n - 1 - i):
                self.play(
                    jlabel.animate.next_to(arr.get_bit(j), UP, buff=0.2),
                    j1label.animate.next_to(arr.get_bit(j + 1), UP, buff=0.2),
                )
                arr.highlight_bit(
                    self, j, j + 1, colors=[RED_E, BLUE_E], sequential=False
                )

                if data[j + 1] < data[j]:
                    arr.swap_bit(self, j, j + 1)
                    data[j], data[j + 1] = data[j + 1], data[j]

                self.wait(0.5)
                arr.highlight_bit(self, j, j + 1, fill=BLACK, animate=False)

            arr.highlight_bit(self, n - i - 1, fill=GREEN_E)

            if i < n - 2:
                self.play(ilabel.animate.next_to(arr.get_bit(i + 1), DOWN, buff=0.2))

        arr.highlight_bit(self, 0, fill=GREEN_E)
        self.wait(2)
