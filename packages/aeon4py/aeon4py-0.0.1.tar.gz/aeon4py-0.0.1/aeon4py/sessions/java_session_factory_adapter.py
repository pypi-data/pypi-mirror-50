import os
import sys

from aeoncloud import ISessionFactoryAdapter
from aeoncloud.sessions.session_adapter import ISessionAdapter
from py4j.java_gateway import JavaGateway, GatewayParameters, launch_gateway, java_import

from aeon4py.sessions.java_session_adapter import JavaSessionAdapter


class JavaSessionFactoryAdapter(ISessionFactoryAdapter):

    def __init__(self, working_directory=None):
        javaopts = []
        if working_directory is not None:
            javaopts.append('-Duser.dir=' + working_directory)

        base_path = os.path.dirname(os.path.dirname(__file__))
        classpath='.:'\
                  + base_path + '/lib/aeon.platform.python.jar:'\
                  + base_path + '/lib/aeon.selenium.jar:'\
                  + base_path + '/lib/aeon.extensions.reporting.jar:'\
                  + base_path + '/lib/aeon.extensions.log4j2.jar:'\
                  + base_path + '/lib/log4j-slf4j-impl.jar:'\
                  + base_path + '/lib/log4j-core.jar:'\
                  + base_path + '/lib/log4j-api.jar:'
        gateway_port = launch_gateway(
            classpath=classpath,
            die_on_exit=True,
            javaopts=javaopts,
            redirect_stdout=sys.stdout,
            redirect_stderr=sys.stderr)
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True, port=gateway_port))
        self.factory = self.gateway.jvm.com.ultimatesoftware.aeon.platform.AeonPlatform.getSessionFactory()
        java_import(self.gateway.jvm, 'com.ultimatesoftware.aeon.core.testabstraction.product.*')

    def get_session(self, settings=None) -> ISessionAdapter:
        return JavaSessionAdapter(self.factory.getSession(settings))

    def before_start(self, suite_name):
        self.gateway.jvm.AeonTestExecution.beforeStart(suite_name)

    def done(self):
        self.gateway.jvm.Aeon.done()

    def given(self, message: str):
        self.gateway.jvm.AeonTestExecution.given(message)

    def and_given(self, message: str):
        self.gateway.jvm.AeonTestExecution.testStep("AND " + message)

    def when(self, message: str):
        self.gateway.jvm.AeonTestExecution.when(message)

    def and_when(self, message: str):
        self.gateway.jvm.AeonTestExecution.testStep("AND " + message)

    def then(self, message: str):
        self.gateway.jvm.AeonTestExecution.then(message)

    def and_then(self, message: str):
        self.gateway.jvm.AeonTestExecution.testStep("AND " + message)

    def start_test(self, name: str):
        self.gateway.jvm.AeonTestExecution.startTest(name)

    def test_succeeded(self):
        self.gateway.jvm.AeonTestExecution.testSucceeded()

    def test_failed(self, message: str, exception=None):
        self.gateway.jvm.AeonTestExecution.testFailed(message, exception)
