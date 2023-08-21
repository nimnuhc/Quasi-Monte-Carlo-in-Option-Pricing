from manim import *
from Functions.qmc import *
from scipy import integrate
from scipy.stats import qmc

class Halton3DT1(ThreeDScene):
    def func(self, x, y): 
        return np.array([x, y, x**(2*y) - np.exp(2*y + x)])

    def construct(self):
        axes = ThreeDAxes(
            x_range =(0, 1, 0.1), 
            y_range = (0, 1, 0.1), 
            z_range = (-TAU, 0.5, 1), 
            x_length = 6.5, 
            y_length = 6.5, 
            z_length = 8, 
            tips = True
            )
        axes.center()
        axes.scale(0.5)
        x_label = axes.get_x_axis_label("x") 
        y_label = axes.get_y_axis_label('y') 
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        qmc = -99.999
        nums = 000
        f1 = lambda x,y: x**(2*y) - np.exp(2*y + x)
        intgl = integrate.dblquad(f1, 0,1, 0, 1) 
        error = 99.99

        qmcrule = always_redraw(lambda : MathTex("Q_{N,s} =", '{: .5g}'.format(qmc)).to_edge(UP + RIGHT))
        title = MathTex(r" \text{Approximating } f(x,y) = x^{2y} - e^{2y+x} \text{ with } \mathcal{P} = \{\phi_2(n), \phi_3(n)\}_{n \in \mathbb{N}}")
        errort = always_redraw(lambda: MathTex(r"|e(f, \mathcal{P} )| \% = ", "{:.2f}\%".format(error), color = YELLOW).move_to(qmcrule.get_bottom()).shift(0.3 *DOWN))
        N_lab = always_redraw(lambda: MathTex("N = {:03d} ".format(nums)).move_to(errort.get_bottom()).shift(0.3* DOWN + 0.2* RIGHT))


        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.play(Write(axes), run_time =2) 
        self.play(Write(labels))

        f = Surface(
            lambda u, v:
            axes.c2p(*self.func(u,v)),
            u_range = [0.001, 1],
            v_range = [0.001,1],
            resolution=30
        )
        self.add_fixed_in_frame_mobjects(qmcrule)
        self.add_fixed_in_frame_mobjects(N_lab)
        self.add_fixed_in_frame_mobjects(errort)
        self.remove(qmcrule)
        self.remove(N_lab)
        self.remove(errort)
        self.play(Write(qmcrule))
        self.play(Write(errort))
        self.play(Write(N_lab))
        self.play(Create(f),run_time = 3)
        self.wait()
        self.begin_ambient_camera_rotation(rate = 1)
        self.wait(5)

        for n in range(100):
            a = brifunc(2,n+1)
            b = brifunc(3, n+1)
            z_vals = f1(a,b)
            dot = Dot(axes.c2p(a, b, 0), fill_opacity=0.7).scale(0.5)
            dot1 = Dot3D(axes.c2p(a, b, z_vals ), color = RED).scale(0.5)
            l = Line(dot.get_center(), dot1.get_center()) 
            self.play(Create(dot), run_time = 0.2)
            self.wait(0.2)
            self.play(LaggedStart(
                ShowCreationThenFadeOut(l),
                Create(dot1),
                FadeOut(dot),
                lag_ratio=0.25,
                run_time = 0.2
            ))
            nums += 1
            qmc = ((qmc * n ) + z_vals) / (n+1)
            error = np.abs((intgl[0] - qmc) / intgl[0]) * 100


        self.wait()
