from manim import *
from Functions.qmc import *
from scipy import integrate
from scipy.stats import qmc

class Sobol(Scene):
    def construct(self):
        axes1 = Axes(
            x_range = [0, 1.1, 0.2],
            y_range = [0, 1.1, 0.2],
            x_length = 7,
            y_length = 7,
            tips = True,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.2),
                "font_size": 24,
            }
        ).scale(0.8)

        axes2 = Axes(
            x_range = [0, 1.1, 0.2],
            y_range = [0, 1.1, 0.2],
            x_length = 7,
            y_length = 7,
            tips = True,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.2),
                "font_size": 24,
            }
        ).scale(0.8)

        axes1.to_edge(LEFT, buff = 0.2)
        axes2.move_to(axes1.get_right()).shift(4 * RIGHT)
        
        axes = VGroup(axes1, axes2)

        title1 = MathTex("\\text{Normal}")
        title2 = MathTex("\\text{Scrambled}") 
        title1.move_to(axes1.get_top())
        title2.move_to(axes2.get_top())

        titles = VGroup(title1, title2) 

        num = 0
        count = always_redraw(lambda: MathTex("N = {}".format(num)).to_edge(DOWN))

        self.add(axes)
        self.add(titles)
        self.play(Write(count)) 
        self.wait()

        sampler1 = qmc.Sobol(d=2, scramble = False)
        sample1 = sampler1.random_base2(10)    

        sampler2 = qmc.Sobol(d=3, scramble = True, seed = 11)
        sample2 = sampler2.random_base2(10)

        coord1 = (sample1[0][0], sample1[0][1],0) 
        dot1 = Dot(axes1.c2p(*coord1), 0.5 * DEFAULT_DOT_RADIUS, color = 'RED', fill_opacity=0.7)

        for i in range(1024):
            coord1 = (sample1[i][0], sample1[i][1],0) 
            dot1 = Dot(axes1.c2p(*coord1), 0.5 * DEFAULT_DOT_RADIUS, color = 'GREEN', fill_opacity=0.7)

            coord2 = (sample2[i][0], sample2[i][1], 0)
            dot2 = Dot(axes2.c2p(*coord2), 0.5 * DEFAULT_DOT_RADIUS, color = 'RED', fill_opacity=0.7)

            num += 1
            dots = VGroup(dot1, dot2)
            self.play(Create(dots), run_time = 0.2)
        
        self.wait(2)
