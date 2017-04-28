
import re
import sys
from time import sleep
from cement.ext.ext_argparse import ArgparseController, expose as ex
from jpipes.core import exc


class PipelineController(ArgparseController):
    class Meta:
        label = None
        stacked_type = 'nested'
        stacked_on = 'base'
        help = 'pipeline sub-controller'
        default_func = '_default'
        console_log_poll_interval = 1
        job = None
        arguments = []
        param_keys = []

    def __init__(self, *args, **kw):
        super(PipelineController, self).__init__(*args, **kw)

    @ex(hide=True)
    def _default(self):    
        params = {}
        for param in self._meta.param_keys:
            if getattr(self.app.pargs, param) is not None:
                params[param] = getattr(self.app.pargs, param)

        if len(params) > 0:
            build_res = self.app.api.post('/job/%s/buildWithParameters' % \
                                          self._meta.job, params)
        else:
            build_res = self.app.api.post('/job/%s/build' % self._meta.job)

        assert build_res.status_code == 201, \
            "Unexpected Status Code: %s" % build_res.status_code

        self.app.log.info('WAITING FOR JOB TO START: %s/api/json' % \
                          build_res.headers['Location'].rstrip('/'))
        self.app.log.info('THIS PROCESS CAN BE SAFELY EXITED [CTRL-C]')

        while True:
            path = "%s/api/json" % build_res.headers['Location'].rstrip('/')
            q_res = self.app.api.get(path).json()
            # odd but at times can hit a little too early and the data isn't
            # populated in the api
            if 'executable' in q_res.keys() \
                and q_res['executable'] is not None:
                if 'url' in q_res['executable'].keys() \
                    and q_res['executable']['url'] is not None:
                    break
            else:
                sleep(1)

        self.app.log.info("JOB STARTED: %s" % q_res['executable']['url'])
        if not self.app.pargs.detach:
            offset = 0
            while True:
                log_url = "%s/logText/progressiveText?start=%s" % (
                            q_res['executable']['url'],
                            offset
                            )
                log_res = self.app.api.get(log_url)
                
                if len(log_res.text):
                    print(log_res.text)

                if 'X-More-Data' in log_res.headers:
                    offset = log_res.headers['X-Text-Size']
                    sleep(self._meta.console_log_poll_interval)
                else:
                    break

            path = "%s/api/json" % q_res['executable']['url']
            job_res = self.app.api.get(path).json()
            if job_res['result'] == 'SUCCESS': 
                self.app.log.info('JOB COMPLETED SUCCESSFULLY')
            else:
                raise exc.JPipesError("JOB FAILED! %s" % \
                                      q_res['executable']['url'])
