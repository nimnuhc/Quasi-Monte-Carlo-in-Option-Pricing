from manim import *
from Functions.qmc import * # this is a self-made package, you can find the package in the same repository
from scipy import integrate
from scipy.stats import qmc

class Halton2D(Scene):
    def construct(self):
        # the location of the ticks depends on the x_range and y_range.
        grid = Axes(
            x_range=[0, 1, 0.05],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.05],
            x_length=6,
            y_length=6,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.1),
                "font_size": 24,
            },
            tips=True,
        )
        grid.shift(0.5 * DOWN)
        # Labels for the x-axis and y-axis.
        title  = MathTex(r"\text{Halton sequence of } (\phi_2(n), \phi_3(n))")
        y_label = grid.get_y_axis_label("y").shift(0.25* LEFT)
        x_label = grid.get_x_axis_label("x").shift(0.27* DOWN)
        grid_labels = VGroup(x_label, y_label) 
        k = 0
        vals = always_redraw(lambda: MathTex(r"N = {}".format(k)).move_to(grid, RIGHT).shift(1.8 * RIGHT))

        self.play(Write(title), run_time = 2)
        self.play(FadeOut(title))
        self.play(Write(grid), run_time = 3)
        self.play(Write(grid_labels), run_time = 2)
        self.play(Write(vals))
        self.wait()
        # self.play(Write(title, graphs))

        for n in range(500):
            k += 1
            dot = Dot(grid.c2p(brifunc(2,n+1), brifunc(3,n+1), 0))
            self.play(Create(dot), run_time = 0.01)

        self.wait(2)
