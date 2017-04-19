
import os
from cement.core.foundation import CementApp
from cement.core.exc import FrameworkError, CaughtSignal
from cement.utils import fs, misc
from jpipes.core import exc

defaults = misc.init_defaults('jpipes', 'jenkins')
defaults['jenkins']['url'] = 'https://jenkins.example.com'
defaults['jenkins']['username'] = None
defaults['jenkins']['password'] = None
defaults['jenkins']['prefix'] = 'pipeline-'

class JPipesApp(CementApp):
    class Meta:
        label = 'jpipes'
        bootstrap = 'jpipes.cli.bootstrap'
        config_defaults = defaults
        extensions = ['yaml', 'colorlog']
        config_handler = 'yaml'
        log_handler = 'colorlog'
        config_files = [
            os.path.join('/', 'etc', label, 'jpipes.yml'),
            os.path.join(fs.HOME_DIR, '.jpipes.yml'),
            os.path.join(fs.HOME_DIR, '.jpipes', 'config'),
            os.path.join('jenkins', 'jpipes.yml')
        ]
        enable_framework_logging = False
        exit_on_close = True

class JPipesTestApp(JPipesApp):
    """A test app that is better suited for testing."""
    class Meta:
        argv = []
        config_files = []
        
def main():
    app = JPipesApp()
    try:
        with app:
            app.run()
    except CaughtSignal as e:
        app.log.warning(e)
        app.exit_code = 0
    except exc.JPipesError as e:
        app.log.fatal(e)
        app.exit_code = 1
    except FrameworkError as e:
        app.log.fatal(e)
        app.exit_code = 1
    finally:
        app.close()
    
if __name__ == '__main__':
    main()