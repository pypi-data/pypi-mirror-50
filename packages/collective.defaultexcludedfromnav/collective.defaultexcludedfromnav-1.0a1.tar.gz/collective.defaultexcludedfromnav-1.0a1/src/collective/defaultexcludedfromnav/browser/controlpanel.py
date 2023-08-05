# -*- coding: utf-8 -*-

from collective.defaultexcludedfromnav import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class IDefaultExcludedFromNavSettingsSchema(Interface):

    portal_types = schema.List(
        title=_(u"Portal types"),
        value_type=schema.Choice(
            title=_(u"Portal type"), source="plone.app.vocabularies.PortalTypes"
        ),
        required=False,
    )


class DefaultExcludedFromNavSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IDefaultExcludedFromNavSettingsSchema
    label = _(u"Configuration for collective.defaultexcludedfromnav product")
    description = _(u"")

    def updateFields(self):
        super(DefaultExcludedFromNavSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(DefaultExcludedFromNavSettingsEditForm, self).updateWidgets()


class DefaultExcludedFromNavControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DefaultExcludedFromNavSettingsEditForm
