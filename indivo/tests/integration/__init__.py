from app.main import Application
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS, TEST_ADMINAPPS, TEST_UIAPPS
from test_modules.data import *

class IntegrationTests(InternalTests):

    def setUp(self):
        super(IntegrationTests, self).setUp()
        self.enableAccessControl()

        # Add the integration test apps
        self.createUserApp(TEST_USERAPPS, 1)
        self.createMachineApp(TEST_UIAPPS, 0)
        self.createMachineApp(TEST_ADMINAPPS, 0)

        # Add the integration test accounts
        self.createAccount(TEST_ACCOUNTS, 0)
        self.createAccount(TEST_ACCOUNTS, 1)

    def tearDown(self):
        super(IntegrationTests, self).tearDown()
        
    def test_integrations(self):
        app = Application()
        app.start()

