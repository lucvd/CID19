from paver.easy import *
from paver.setuputils import setup
import multiprocessing
import platform

setup(
    name = "behave-browserstack",
    version = "0.1.0",
    author = "BrowserStack",
    author_email = "support@browserstack.com",
    description = ("Behave Integration with BrowserStack"),
    license = "MIT",
    keywords = "example selenium browserstack",
    url = "https://github.com/browserstack/lettuce-browserstack",
    packages=['features']
)

def run_behave_test(config, feature, task_id=0):
    if platform.system() == "Windows":
        sh('cmd /C "set CONFIG_FILE=config/%s.json && set TASK_ID=%s && behave features/%s.feature"' % (config, task_id, feature))
    else:
        sh('CONFIG_FILE=config/%s.json TASK_ID=%s behave features/%s.feature' % (config, task_id, feature))

@task
@consume_nargs(1)
def run(args):
    """Run single, local and parallel test using different config."""
    if args[0] in ('single', 'local'):
        run_behave_test(args[0], args[0])
    else:
        '''
        jobs = []
        multiprocessing.set_start_method('spawn')
        for i in range(4):
            p = multiprocessing.Process(target=run_behave_test, args=(args[0], "single", i))
            jobs.append(p)
            p.start()
        '''
        jobs = []
        for i in range(4):
            '''  #p = multiprocessing.Process(target=print, args=("parallel", "single", i))
  cmd = "python " + str(file_name) + " " + str(json_name) + " " + str(counter)
  process.append(subprocess.Popen(cmd, shell=True))
  jobs.append(p)
  p.start()'''
            p = multiprocessing.Process(target=run_behave_test, args=(args[0], "single", i))
            jobs.append(p)
            p.start()

@task
def test():
    """Run all tests"""
    sh("paver run single")
    sh("paver run local")
    sh("paver run parallel")



