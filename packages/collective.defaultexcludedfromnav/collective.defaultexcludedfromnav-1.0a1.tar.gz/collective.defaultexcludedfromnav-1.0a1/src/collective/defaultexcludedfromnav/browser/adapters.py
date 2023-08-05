# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.interface import implementer
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigationDefault
from zope.globalrequest import getRequest


@implementer(IExcludeFromNavigationDefault)
def default_exclude(context):
    registry = getUtility(IRegistry)
    portal_types = registry.get(
        "collective.defaultexcludedfromnav.browser.controlpanel.IDefaultExcludedFromNavSettingsSchema.portal_types"
    )

    request = getRequest()
    portal_type = request.steps[-1].replace("++add++", "")
    if portal_types:
        if portal_type in portal_types:
            return True

    return False
