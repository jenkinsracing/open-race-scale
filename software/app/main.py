from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


FLAVOR = 1  # 1 is local GUI, 0 is client GUI

if not FLAVOR:
    from app.btandroid import *


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

    def __init__(self, scale_data, pos, **kwargs):
        super(WeightDisplay, self).__init__(**kwargs)
        self.cols = 2

        self._sd = scale_data
        self.fl_id = Label(text=self._sd.id)
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

    def get_data(self):
        # TODO read weight from bluetooth interface
        self.fl_wgt.text = str(self._sd.weight)
        self.fl_pct.text = str(self._sd.percent)


def update_disps(dt):
    global sc
    global disps

    if FLAVOR:
        sc.update()

    for disp in disps:
        disp.get_data()


class MyApp(App):

    def build(self):

        if not FLAVOR:
            self.recv_stream, self.send_stream = get_socket_stream('orctest')

        m = ScaleMain()
        m.add_widget(Label(text='Open Race Scale', font_size=50))

        global disps
        global sc
        disps = [WeightDisplay(sc.scale_data['FL'], 0), WeightDisplay(sc.scale_data['FR'], 1), WeightDisplay(sc.scale_data['RL'], 0), WeightDisplay(sc.scale_data['RR'], 1), WeightDisplay(sc.scale_data['TOTAL'], 1)]

        w = ScaleDisplay(disps)

        event = Clock.schedule_interval(update_disps, 1)

        m.add_widget(w)
        return m

    def send(self, cmd):
        self.send_stream.write('{}\n'.format(cmd))
        self.send_stream.flush()


if __name__ == '__main__':
    """
    If the GUI is run locally as the main then the GUI will create a scale controller instead of just obtaining the data
    via BT interface
    """
    sim = True  # change to True if not running on a RPi3

    if FLAVOR:
        from core.corerp3 import ScaleControl
        sc = ScaleControl(simulate=sim)

    disps = None

    MyApp().run()
