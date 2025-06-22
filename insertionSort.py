from manim import *
from helper.array import Array


class InsertionSort(Scene):
    def construct(self):
        data = [64, 34, 25, 12, 11, 50]
        n = len(data)

        arr = Array(data=data)
        ilabel = Text("i", font_size=20).next_to(arr.get_bit_rect(1), UP, buff=0.3)
        self.add(arr, ilabel)
        self.wait(1)

        arr.highlight_bit(self, 0, fill=GREEN_D)
        self.wait(0.5)

        for i in range(1, n):
            j = i - 1
            while j >= 0 and data[j] > data[i]:
                j -= 1

            if j + 1 != i:
                arr.highlight_bit(self, *range(i - 1, j, -1), fill=RED_E)
                self.wait(0.5)
                arr.swap_and_shift_bit(self, i, j + 1)
                arr.highlight_bit(self, *range(i - 1, j, -1), fill=BLACK, animate=False)
                data.insert(j + 1, data.pop(i))

            arr.highlight_bit(self, *range(0, i + 1), fill=GREEN_D, sequential=False)
            if i < n - 1:
                self.play(ilabel.animate.next_to(arr.get_bit_rect(i + 1), UP, buff=0.3))
