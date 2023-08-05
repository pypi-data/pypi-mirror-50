# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.defaultexcludedfromnav


class CollectiveDefaultexcludedfromnavLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.defaultexcludedfromnav)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.defaultexcludedfromnav:default")


COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_FIXTURE = CollectiveDefaultexcludedfromnavLayer()


COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_FIXTURE,),
    name="CollectiveDefaultexcludedfromnavLayer:IntegrationTesting",
)


COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_FIXTURE,),
    name="CollectiveDefaultexcludedfromnavLayer:FunctionalTesting",
)


COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveDefaultexcludedfromnavLayer:AcceptanceTesting",
)
