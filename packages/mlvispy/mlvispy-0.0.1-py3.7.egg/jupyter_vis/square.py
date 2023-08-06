from __future__ import print_function
from jupyter_react import Component

class Square(Component):
    module = 'Square'

    def __init__(self, **kwargs):
        super(Square, self).__init__(target_name='react.jupyter_vis', **kwargs)
        self.on_msg(self._handle_msg)

    def _handle_msg(self, msg):
        print(msg)
