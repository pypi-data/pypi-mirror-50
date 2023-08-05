# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.defaultexcludedfromnav.testing import (
    COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_INTEGRATION_TESTING,
)  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


no_get_installer = False


try:
    from Products.CMFPlone.utils import get_installer
except Exception:
    no_get_installer = True


class TestSetup(unittest.TestCase):
    """Test that collective.defaultexcludedfromnav is properly installed."""

    layer = COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.defaultexcludedfromnav is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.defaultexcludedfromnav")
        )

    def test_browserlayer(self):
        """Test that ICollectiveDefaultexcludedfromnavLayer is registered."""
        from collective.defaultexcludedfromnav.interfaces import (
            ICollectiveDefaultexcludedfromnavLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(ICollectiveDefaultexcludedfromnavLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_DEFAULTEXCLUDEDFROMNAV_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.defaultexcludedfromnav")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.defaultexcludedfromnav is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.defaultexcludedfromnav")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveDefaultexcludedfromnavLayer is removed."""
        from collective.defaultexcludedfromnav.interfaces import (
            ICollectiveDefaultexcludedfromnavLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveDefaultexcludedfromnavLayer, utils.registered_layers()
        )
