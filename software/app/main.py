from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class ScaleMain(BoxLayout):

    def __init__(self, **kwargs):
        super(ScaleMain, self).__init__(orientation='vertical', **kwargs)


class ScaleDisplay(GridLayout):

    def __init__(self, disps, **kwargs):
        super(ScaleDisplay, self).__init__(**kwargs)
        self.cols = 2

        for disp in disps:
            self.add_widget(disp)


class WeightDisplay(GridLayout):

    def __init__(self, ident, pos, **kwargs):
        super(WeightDisplay, self).__init__(**kwargs)
        self.cols = 2

        self._wgt = 0
        self._pct = 0
        self.fl_id = Label(text=ident)
        self.fl_wgt = Label(text='0')
        self.fl_pct = Label(text='0%')

        if pos:
            self.add_widget(self.fl_id)
            self.b = BoxLayout(orientation='vertical')
            self.add_widget(self.b)
            self.b.add_widget(self.fl_wgt)
            self.b.add_widget(self.fl_pct)
        else:
            self.b = BoxLayout(orientation='vertical')
            self.add_widget(self.b)
            self.b.add_widget(self.fl_wgt)
            self.b.add_widget(self.fl_pct)

            self.add_widget(self.fl_id)

    def read_wgt(self):
        # TODO read weight from bluetooth interface
        self._wgt += 1
        self.fl_wgt.text = str(self._wgt)
        self.fl_pct.text = '99%'


def read_wgts(dt):
    global disps
    for disp in disps:
        disp.read_wgt()


class MyApp(App):

    def build(self):
        m = ScaleMain()
        m.add_widget(Label(text='Open Race Scale', font_size=50))

        global disps
        disps = [WeightDisplay('FL', 0), WeightDisplay('FR', 1), WeightDisplay('RL', 0), WeightDisplay('RR', 1)]

        w = ScaleDisplay(disps)

        event = Clock.schedule_interval(read_wgts, 1)

        m.add_widget(w)
        return m


if __name__ == '__main__':
    disps = None
    MyApp().run()
