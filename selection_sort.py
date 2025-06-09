from manim import *
from helper import Array


def selsortCode():
    return Code(
        code_string="""
data = [64, 25, 12, 22, 11]
for i in range(len(data)-1):
    min_idx = i
    for j in range(i+1, len(data)):
        if data[j] < data[min_idx]:
            min_idx = j
    data[i], data[min_idx] = data[min_idx], data[i]
""",
        language="python",
        add_line_numbers=False,
        background="window",
    )


class SelectionSort(Scene):
    def construct(self):
        # code = selsortCode()
        # self.play(Write(code))
        # self.play(code.animate.scale(0.6).to_edge(UL))

        data = [64, 25, 12, 22, 11]
        n = len(data)
        iidx = 0
        jidx = iidx + 1

        # self.add(NumberPlane().add_coordinates())

        arr = Array(data=data, hbuff=0.05).set_stroke(WHITE, width=1)
        self.play(Write(arr.grid))
        self.wait(1)

        arc_up = ArcBetweenPoints(
            start=arr.get_bit(0).get_center(),
            end=arr.get_bit(4).get_center(),
            angle=-PI,
        )

        arc_down = ArcBetweenPoints(
            start=arr.get_bit(4).get_center(),
            end=arr.get_bit(0).get_center(),
            angle=-PI,
        )

        # self.play(
        #     MoveAlongPath(arr.get_bit_value(0), arc_up),
        #     MoveAlongPath(arr.get_bit_value(4), arc_down),
        # )
        # arr.update_bit(self, 0, 4, labels=["11", "64"], animate=False)
        # self.wait(1)

        # i_label = Text("i", font_size=18).next_to(arr.get_bit(0), UP)
        # i_arrow = Arrow(
        #     start=arr.get_bit(0).get_center(),
        #     end=arr.get_bit(3).get_center(),
        #     buff=0.1,
        #     stroke_width=2,
        #     max_tip_length_to_length_ratio=0.1,
        # ).move_to([-1.5, 0.7, 0], aligned_edge=LEFT)
        # self.play(Write(i_label), Write(i_arrow, run_time=1.5))

        # for i in range(len(data)):
        #     if i < len(data) - 2:
        #         self.play(
        #             i_label.animate.next_to(arr.get_bit(i), UP),
        #             i_arrow.animate.put_start_and_end_on(
        #                 start=[-1.5 + 0.8 * i, 0.7, 0], end=i_arrow.get_end()
        #             ),
        #         )
        #     else:
        #         self.remove(i_arrow)
        #         self.play(i_label.animate.next_to(arr.get_bit(i), UP))

        # j_label = Text("j", font_size=18).next_to(arr.get_bit(1), DOWN)
        # j_arrow = Arrow(
        #     start=arr.get_bit(1).get_center(),
        #     end=arr.get_bit(4).get_center(),
        #     buff=0.1,
        #     stroke_width=2,
        #     max_tip_length_to_length_ratio=0.1,
        # ).move_to([-0.7, -0.7, 0], aligned_edge=LEFT)
        # self.play(Write(j_label), Write(j_arrow, run_time=1.5))

        min_idx = None
        anim = 0
        for i in range(len(data) - 1):
            if min_idx is not None:
                self.play(arr.get_bit(min_idx).animate.set_fill(BLACK))

            min_idx = i

            self.play(arr.get_bit(i).animate.set_fill(RED))

            for j in range(i + 1, len(data)):
                self.play(arr.get_bit(j).animate.set_fill(BLUE))
                if data[j] < data[min_idx]:
                    self.play(
                        arr.get_bit(min_idx).animate.set_fill(BLACK),
                        arr.get_bit(j).animate.set_fill(RED),
                    )
                    min_idx = j
                else:
                    self.play(arr.get_bit(j).animate.set_fill(BLACK))

            # swap the values
            if anim == 0:
                self.play(
                    MoveAlongPath(arr.get_bit_value(i), arc_up),
                    MoveAlongPath(arr.get_bit_value(min_idx), arc_down),
                )
                anim += 1

            arr.update_bit(self, i, min_idx, labels=[data[min_idx], data[i]])
            data[i], data[min_idx] = data[min_idx], data[i]

        self.wait(1)
