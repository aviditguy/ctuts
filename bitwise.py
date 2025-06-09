from manim import *
from helper import BitwiseOrTable
from helper import BitwiseAndTable
from helper import Array


class Bitwise(Scene):
    def construct(self):
        n = 100
        one = 1
        k = 5
        shift = 5
        # self.add(NumberPlane().add_coordinates())

        l1 = MathTex(f"n = {n}").move_to([-2, 1, 0])
        self.play(Write(l1))

        a_l1 = (
            Array(data=format(n, "08b"), index_ltr=False)
            .next_to(l1, RIGHT, buff=1)
            .shift(UP * 0.1)
        )
        self.play(Write(a_l1))

        l2 = MathTex(rf"\sim({one} << {shift})").next_to(
            l1, DOWN, buff=0.9, aligned_edge=RIGHT
        )
        self.play(Write(l2))

        v = ~(1 << shift)
        a_l2 = (
            Array(data=format(v & 0xFF, "08b"), index_ltr=False)
            .next_to(l2, RIGHT, buff=1)
            .shift(UP * 0.1)
        )
        self.play(Write(a_l2.grid))

        l3 = MathTex(rf"n\; \& \sim({one} << {shift})").next_to(
            l2, DOWN, buff=0.9, aligned_edge=RIGHT
        )
        self.play(Write(l3))

        a_l3 = Array(data=[""] * 8, index_ltr=False, index_dir_up=False).next_to(
            l3, RIGHT, buff=1, aligned_edge=UP
        )
        self.play(Write(a_l3))

        andTable = BitwiseAndTable().scale(0.9).move_to([-6, 6, 0])
        self.play(andTable.animate.move_to([-6.8, 1.5, 0], aligned_edge=UL))
        self.wait(0.5)

        values = list(format(n & (~(1 << shift) & 0xFF), "08b"))
        a_l3.update_n_bit(self, n=8, labels=values)
        self.wait(0.5)

        a_l3.highlight_bit(self, k, color=GREEN)
        self.wait(1)
