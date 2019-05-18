from paver.easy import *
from paver.setuputils import setup
import platform
from multiprocessing.dummy import Pool as ThreadPool

setup(
    name = "behave-browserstack",
    version = "0.1.0",
    author = "BrowserStack",
    author_email = "support@browserstack.com",
    description = ("Behave Integration with BrowserStack"),
    license = "MIT",
    keywords = "example selenium browserstack",
    url = "https://github.com/browserstack/behave-browserstack",
    packages=['features']
)


def run_behave_test(config, feature, task_id=0):
    if platform.system() == "Windows":
        sh('cmd /C "set CONFIG_FILE=config/%s.json && set TASK_ID=%s && behave features/%s.feature --junit --junit-directory reports/%s"' % (config, task_id, feature, task_id))
    else:
        sh('CONFIG_FILE=config/%s.json TASK_ID=%s behave features/%s.feature --junit --junit-directory reports/%s' % (config, task_id, feature, task_id))


@task
@consume_nargs(1)
def run(args):
    """Run single, local and parallel test using different config."""
    if args[0] in ('single', 'local'):
        run_behave_test(args[0], args[0])
    else:
        pool = ThreadPool(4)
        jobs = pool.starmap(run_behave_test, [(args[0], "single", "0"), (args[0], "single", "1"), (args[0], "single", "2"), (args[0], "single", "3")])
        #use jobs for something later maybe?


@task
def test():
    """Run all tests"""
    sh("paver run single")
    sh("paver run local")
    sh("paver run parallel")




