
import re
from cement.core import handler
from jpipes.cli.controllers.base import BaseController
from jpipes.cli.controllers.pipeline import PipelineController
from jpipes.core.jenkins import JenkinsAPI

def extend_jenkins_api(app):
    jenkins = JenkinsAPI(
                app.config.get('jenkins', 'url'), 
                auth=(
                    app.config.get('jenkins', 'username'), 
                    app.config.get('jenkins', 'password')
                ),
                debug=app.debug,
            )
    app.extend('api', jenkins)

def load_pipeline_controllers(app):
    pipelines = []

    # get all jobs that start with `prefix`
    prefix = app.config.get('jenkins', 'prefix')
    res = app.api.get('/api/json').json()
    for job in res['jobs']:
        if job['name'].startswith(prefix):
            pipelines.append(job['name'])

    for job in pipelines:
        pipe = {}
        pipe['label'] = re.sub(prefix, '', job)
        pipe['job'] = job
        pipe['arguments'] = []
        pipe['param_keys'] = []
        
        # get params for parameterized builds
        job_res = app.api.get('/job/%s/api/json' % pipe['job']).json()
        pipe['params'] = []
        param_class = 'hudson.model.ParametersDefinitionProperty'
        param_defs = []
        for _property in job_res['property']:
            if _property['_class'] == param_class:
                param_defs = _property['parameterDefinitions']
                break
        for param_def in param_defs:
            param = {}
            if param_def['_class'] == 'hudson.model.StringParameterDefinition':
                param['key'] = param_def['name']
                param['default'] = param_def['defaultParameterValue']['value']
                param['help'] = param_def['description'].lower().rstrip('.')
            else:
                raise exc.JPipesError(
                    "Unsupported Paramater Type: %s" % param_def['_class']
                )

            pipe['params'].append(param)

        for param in pipe['params']:
            if isinstance(param, dict):
                key = param['key']
                
                # defaults
                param_dict = {
                    'name' : key,
                    'help' : '%s parameter' % key,
                    'default' : None,
                    'required' : False,
                    'help' : 'pipeline parameter',
                }

                # override with what's passed
                param_dict.update(param)

            elif isinstance(param, str):
                # defaults
                param_dict = {
                    'key' : param,
                    'help' : '%s parameter' % param,
                    'default' : None,
                    'required' : False,
                    'help' : 'pipeline parameter',
                }

            param = param_dict

            if param['default'] in [None, ""]:
                param['required'] = True
            else:
                param['help'] = "%s [default: %s]" % (
                            param['help'].lower().rstrip('.'),
                            param['default'].lower()
                            )

            argument = ( [ '--%s' % param['key'].lower() ], 
                         { 'help' : param['help'],
                           'dest' : param['key'],
                           'default' : param['default'],
                           'required' : param['required'] } )

            pipe['arguments'].append(argument)
            pipe['param_keys'].append(param['key'])

        # add a -d/--detach option
        argument = ( [  '-d', '--detach' ], 
                     {  'help' : 'detach from the process after job starts',
                        'dest' : 'detach',
                        'action' : 'store_true' } )
        pipe['arguments'].append(argument)
        class PipelineControllerInstance(PipelineController):
            class Meta:
                label = pipe['label']
                job = pipe['job']
                arguments = pipe['arguments']
                param_keys = pipe['param_keys']


        PipelineControllerInstance.__name__ = "%sPipelineController" % \
                                                pipe['label'].capitalize()
        app.handler.register(PipelineControllerInstance)

def load(app):
    app.handler.register(BaseController)
    app.hook.register('pre_run', extend_jenkins_api, weight=0)
    app.hook.register('pre_run', load_pipeline_controllers, weight=1)
