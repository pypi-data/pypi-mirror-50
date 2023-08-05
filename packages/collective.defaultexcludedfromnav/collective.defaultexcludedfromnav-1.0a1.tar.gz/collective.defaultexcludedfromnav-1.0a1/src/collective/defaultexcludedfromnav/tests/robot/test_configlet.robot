*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup   Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***

Image exluded by default SiteRoot
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@defaultexcludedfromnav_settings
    Page should contain  Configuration for collective.defaultexcludedfromnav product
    Select From List By Value   css:select#form-widgets-portal_types-from  Image
    Click button  →
    Click button  Save
    Go to  ${PLONE_URL}/++add++Image#autotoc-item-autotoc-4
    Checkbox Should Be Selected  css:input#form-widgets-IExcludeFromNavigation-exclude_from_nav-0

Image not exluded by default SiteRoot
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/++add++Image#autotoc-item-autotoc-4
    Checkbox Should Not Be Selected  css:input#form-widgets-IExcludeFromNavigation-exclude_from_nav-0

Image exluded by default Dexterity
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@defaultexcludedfromnav_settings
    Page should contain  Configuration for collective.defaultexcludedfromnav product
    Select From List By Value   css:select#form-widgets-portal_types-from  Image
    Click button  →
    Click button  Save
    Go to  ${PLONE_URL}/++add++Folder
    Input Text  form-widgets-IDublinCore-title  Folder
    Click button  Save
    pause
    Go to  ${PLONE_URL}/folder/++add++Image#autotoc-item-autotoc-4
    Checkbox Should Be Selected  css:input#form-widgets-IExcludeFromNavigation-exclude_from_nav-0

Image not exluded by default Dexterity
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/++add++Folder
    Input Text  form-widgets-IDublinCore-title  Folder
    Click button  Save
    Go to  ${PLONE_URL}/folder/++add++Image#autotoc-item-autotoc-4
    Checkbox Should Not Be Selected  css:input#form-widgets-IExcludeFromNavigation-exclude_from_nav-0
