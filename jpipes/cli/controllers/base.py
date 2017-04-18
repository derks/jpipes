
import sys
from time import sleep
from cement.ext.ext_argparse import ArgparseController, expose as ex


class BaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = 'Jenkins Pipeline Automation'
        default_func = '_default'

    @ex(hide=True)
    def _default(self):
        self.app.log.warning('Sub-Command required!')
        self.app.args.print_help()


class PipelineController(ArgparseController):
    class Meta:
        label = None
        help = 'pipeline sub-controller'

    def __init__(self, *args, **kw):
        super(PipelineController, self).__init__(*args, **kw)
