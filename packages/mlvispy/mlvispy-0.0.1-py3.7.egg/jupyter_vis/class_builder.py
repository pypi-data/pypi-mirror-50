import sys
from jupyter_react import Component


current_module = sys.modules[__name__]


def init(self, **kwargs):
    Component.__init__(self, target_name='react.jupyter_vis', **kwargs)
    self.on_msg(self._handle_msg)


def _handle_msg(self, msg):
    print(msg)


components = [
    'AreaChart',
    'StackedCalendar',
    'GraphBuilder',
    'FeatureListView',
    'MultiWayPlot'
]

# Dynamically create module classes
for component in components:
    setattr(current_module, component, type(component,
                                            (Component, ), {
                                                'module': component,
                                                '__init__': init,
                                                '_handle_msg': _handle_msg}))
