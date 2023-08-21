from manim import *
from Functions.qmc import *
from scipy import integrate
from scipy.stats import qmc

class Halton2DPi(Scene):
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
        ).scale(0.6)

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
        ).scale(0.6)

        axes3 = Axes(
            x_range = [0, 1.1, 0.2],
            y_range = [0, 1.1, 0.2],
            x_length = 7,
            y_length = 7,
            tips = True,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.2),
                "font_size": 24,
            }
        ).scale(0.6)
    

        axes1.to_edge(UP+LEFT, buff = 0.1)
        axes2.move_to(axes1.get_right()).shift(2.5*RIGHT)
        axes3.move_to(axes2.get_right()).shift(2.5*RIGHT)

        x_label1 = axes1.get_x_axis_label("x")
        x_label1.scale(0.7)
        y_label1 = axes1.get_y_axis_label(MathTex("y = \\sqrt{1-x^2}"))
        y_label1.scale(0.7).shift(0.3 * UP + 0.1 * LEFT)
        labels = VGroup(x_label1, y_label1)

        seq1 = MathTex(r"\mathcal{P}_1 = (\phi_2(n))")
        seq2 = MathTex(r"\mathcal{P}_2 = (\phi_3(n))")
        seq3 = MathTex(r"\mathcal{P}_3 = (\phi_5(n))")

        seq1.move_to(axes1.get_x_axis()).scale(0.7).shift(0.5*DOWN)
        seq2.move_to(axes2.get_x_axis()).scale(0.7).shift(0.5*DOWN)
        seq3.move_to(axes3.get_x_axis()).scale(0.7).shift(0.5*DOWN)

        seq = VGroup(seq1, seq2, seq3)

        function = lambda t : np.sqrt(1-t**2)

        graph1 = axes1.plot(function, x_range = [0, 1, 0.001], color = BLUE)
        graph2 = axes2.plot(function, x_range = [0, 1, 0.001], color = BLUE)
        graph3 = axes3.plot(function, x_range = [0, 1, 0.001], color = BLUE) 

        graphs = VGroup(graph1, graph2, graph3)


        qns1 = 0
        approx1 = always_redraw(lambda : MathTex(r"\pi_1 \approx {:3f}".format(qns1), color = YELLOW).move_to(seq1.get_bottom()).scale(0.7).shift(0.3*DOWN))
        error1 = 0
        error1t = always_redraw(lambda: MathTex(r"|e(f, \mathcal{P}_1 )| \% = ", "{:.2f}\%".format(error1), color = YELLOW).move_to(approx1.get_bottom()).shift(0.3 *DOWN).scale(0.7))

        qns2 = 0 
        approx2 = always_redraw(lambda : MathTex(r"\pi_2 \approx {:3f}".format(qns2), color = YELLOW).move_to(seq2.get_bottom()).scale(0.7).shift(0.3*DOWN))
        error2 = 0
        error2t = always_redraw(lambda: MathTex(r"|e(f, \mathcal{P}_2)| \% = ", "{:.2f}\%".format(error2), color = YELLOW).move_to(approx2.get_bottom()).shift(0.3 *DOWN).scale(0.7))

        qns3 = 0
        approx3 = always_redraw(lambda : MathTex(r"\pi_3 \approx {:3f}".format(qns3), color = YELLOW).move_to(seq3.get_bottom()).scale(0.7).shift(0.3*DOWN))
        error3 = 0
        error3t = always_redraw(lambda: MathTex(r"|e(f, \mathcal{P}_3)| \% = ", "{:.2f}\%".format(error3), color = YELLOW).move_to(approx3.get_bottom()).shift(0.3*DOWN).scale(0.7))


        errorts = VGroup(error1t, error2t, error3t)
        num = 0 
        count = always_redraw(lambda : MathTex(r"N = {}".format(num)).to_edge(DOWN))

        approx = VGroup(approx1, approx2, approx3)

        axes = VGroup(axes1, axes2, axes3)
        #self.add(axes)
        #self.add(labels)
        #self.add(seq)
        #self.add(graphs)
        #self.add(count)
        #self.add(approx)
        #self.add(errorts)
        self.play(Write(axes))
        self.play(Write(labels))
        self.play(Create(graphs), run_time = 2) 
        self.play(Write(seq))
        self.play(Write(approx))
        self.play(Write(errorts))
        self.play(Write(count))

        self.wait()


        bsum1, bsum2, bsum3 = 0, 0, 0 
        denom = 1 
        for n in range(101):
            a1 = brifunc(2, n+1)
            b1 = function(a1)
            bsum1 += b1
            coordx1 = (a1, 0 , 0)
            coordy1 = (a1, b1, 0)
            dotx1 = Dot(axes1.c2p(*coordx1), 0.5 * DEFAULT_DOT_RADIUS) 
            doty1 = Dot(axes1.c2p(*coordy1), 0.5 * DEFAULT_DOT_RADIUS, color = RED)
            l1 = Line(dotx1.get_center(), doty1.get_center())

            a2 = brifunc(3,n+1)
            b2 = function(a2)
            bsum2 += b2 
            coordx2 = (a2, 0,0)
            coordy2 = (a2, b2, 0)
            dotx2 = Dot(axes2.c2p(*coordx2), 0.5* DEFAULT_DOT_RADIUS)
            doty2 = Dot(axes2.c2p(*coordy2), 0.5*DEFAULT_DOT_RADIUS, color = RED)
            l2 = Line(dotx2.get_center(), doty2.get_center()) 


            a3 = brifunc(5,n+1)
            b3 = function(a3)
            bsum3 += b3 
            coordx3 = (a3, 0,0)
            coordy3 = (a3, b3, 0)
            dotx3 = Dot(axes3.c2p(*coordx3), 0.5* DEFAULT_DOT_RADIUS)
            doty3 = Dot(axes3.c2p(*coordy3), 0.5*DEFAULT_DOT_RADIUS, color = RED)
            l3 = Line(dotx3.get_center(), doty3.get_center()) 

            dotx = VGroup(dotx1, dotx2, dotx3) 
            doty = VGroup(doty1, doty2, doty3)
            l = VGroup(l1, l2, l3) 


            self.play(Create(dotx), run_time = 0.1)
            self.play(LaggedStart(
                ShowCreationThenFadeOut(l),
                Create(doty),
                lag_ratio=0.25,
                run_time = 0.2
            ))
            qns1 = 4 * (bsum1) / (denom + n)
            qns2 = 4 * (bsum2) / (denom + n)
            qns3 = 4 * (bsum3) / (denom + n)
            error1 = np.abs(np.pi - qns1) /  np.pi * 100
            error2 = np.abs(np.pi - qns2) /np.pi * 100
            error3 = np.abs(np.pi - qns3)/ np.pi * 100
            num += 1
        
        self.wait(2)
