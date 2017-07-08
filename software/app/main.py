from kivy.app import App
from kivy.logger import Logger
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

        self.tx = Label(text='Open Race Scale', font_size=50)
        self.add_widget(self.tx)
        self.tx.size_hint_max_x = 80
        self.tx.size_hint_y = .9
        #self.tx.pos_hint = .1


class HeaderDisplay(BoxLayout):

    def __init__(self, **kwargs):
        super(HeaderDisplay, self).__init__(orientation='horizontal', **kwargs)

        self.add_widget(WeightDisplayVertical(sc.scale_data['FLFR']))
        self.add_widget(WeightDisplayVertical(sc.scale_data['FRRL']))


class FooterDisplay(BoxLayout):

    def __init__(self, **kwargs):
        super(FooterDisplay, self).__init__(orientation='horizontal', **kwargs)

        self.add_widget(WeightDisplayVertical(sc.scale_data['RLRR']))
        self.add_widget(WeightDisplayVertical(sc.scale_data['FLRR']))


class TotalDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(TotalDisplay, self).__init__(orientation='horizontal', **kwargs)

        self.add_widget(WeightDisplayVertical(sc.scale_data['TOTAL']))


class CornerDisplay(GridLayout):

    def __init__(self, **kwargs):
        super(CornerDisplay, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(WeightDisplayHorizontal(sc.scale_data['FL'], 0))
        self.add_widget(WeightDisplayHorizontal(sc.scale_data['FR'], 1))
        self.add_widget(WeightDisplayHorizontal(sc.scale_data['RL'], 0))
        self.add_widget(WeightDisplayHorizontal(sc.scale_data['RR'], 1))


class WeightDisplayHorizontal(GridLayout):

    def __init__(self, scale_data, pos, **kwargs):
        super(WeightDisplayHorizontal, self).__init__(**kwargs)
        self.cols = 2

        self._sd = scale_data
        self._sd.widget = self  # keep track of the widget for this scale data
        self.text = self._get_text_from_id(self._sd.id)
        self.fl_id = Label(text=self.text)
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
        self.fl_wgt.text = '{:.1f}'.format(self._sd.weight) + ' Lbs'
        self.fl_pct.text = '{:.1f}%'.format(self._sd.percent)

    def _get_text_from_id(self, identifier):
        return sc.labels[identifier]


class WeightDisplayVertical(GridLayout):
    def __init__(self, scale_data, **kwargs):
        super(WeightDisplayVertical, self).__init__(**kwargs)
        self.rows = 3

        self._sd = scale_data
        self._sd.widget = self  # keep track of the widget for this scale data
        self.text = self._get_text_from_id(self._sd.id)
        self.fl_id = Label(text=self.text)
        self.fl_wgt = Label(text='0')
        self.fl_pct = Label(text='0%')

        self.add_widget(self.fl_id)
        self.add_widget(self.fl_wgt)
        self.add_widget(self.fl_pct)

    def get_data(self):
        # TODO read weight from bluetooth interface
        self.fl_wgt.text = '{:.1f}'.format(self._sd.weight) + ' Lbs'
        self.fl_pct.text = '{:.1f}%'.format(self._sd.percent)

    def _get_text_from_id(self, identifier):
        return sc.labels[identifier]


def update_disps(dt):
    global sc

    if FLAVOR:
        sc.update()

    # update all display widgets
    for k, v in sc.scale_data.items():
        if v.widget is not None:
            v.widget.get_data()


class OSRApp(App):
    # icon = TODO make app icon
    title = 'Open Race Scale V0.1 Build 5'

    def build(self):

        title = 'Basic Application'

        if not FLAVOR:
            self.recv_stream, self.send_stream = get_socket_stream('orctest')

        r = ScaleMain()

        global sc

        h = HeaderDisplay()
        c = CornerDisplay()
        f = FooterDisplay()
        t = TotalDisplay()

        event = Clock.schedule_interval(update_disps, 1)

        r.add_widget(h)
        r.add_widget(c)
        r.add_widget(f)
        r.add_widget(t)
        return r

    def on_start(self):
        Logger.info('App: Started')

    def on_stop(self):
        Logger.info('App: Stopped')

    def on_pause(self):
        Logger.info('App: Paused')
        return True

    def on_resume(self):
        Logger.info('App: Resumed')
        pass

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

    OSRApp().run()


