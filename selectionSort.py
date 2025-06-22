from manim import *
from helper.array import Array


class SelectionSort(Scene):
    def construct(self):
        data = [12, 25, 11, 9, 17]
        n = len(data)

        arr = Array(data=data, index_dir_up=False)
        ilabel = Text("i", font_size=16).next_to(arr.get_bit(0), UP, buff=0.2)
        jlabel = Text("j", font_size=16).next_to(arr.get_bit(1), UP, buff=0.2)

        self.add(arr, ilabel, jlabel)
        self.wait(1)

        for i in range(n - 1):
            minidx = i

            arr.highlight_bit(self, minidx, fill=RED_E)

            for j in range(i + 1, n):
                self.play(jlabel.animate.next_to(arr.get_bit_rect(j), UP, buff=0.2))
                arr.highlight_bit(self, j, fill=BLUE_E)

                if data[j] < data[minidx]:
                    self.wait(0.5)
                    arr.highlight_bit(
                        self, minidx, j, colors=[BLACK, RED_E], animate=False
                    )
                    minidx = j
                else:
                    self.wait(0.5)
                    arr.highlight_bit(self, j, fill=BLACK, animate=False)

            if minidx != i:
                arr.swap_bit(self, i, minidx)
                arr.highlight_bit(
                    self, i, minidx, colors=[GREEN_E, BLACK], animate=False
                )

                data[minidx], data[i] = data[i], data[minidx]
            else:
                self.arr.highlight_bit(self, i, fill=GREEN_E)

            if i < n - 2:
                self.play(ilabel.animate.next_to(arr.get_bit_rect(i + 1), UP, buff=0.2))

        self.wait(0.5)
        arr.highlight_bit(self, n - 1, fill=GREEN_E)
        self.wait(2)
