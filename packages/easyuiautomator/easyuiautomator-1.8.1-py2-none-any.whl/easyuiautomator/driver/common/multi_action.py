# coding=utf-8

"""
Created on 2015年11月5日

@author: thomas.ning
"""


import copy
from easyuiautomator.driver.common.mobilecommand import MobileCommand as Command


class MultiAction(object):
    
    def __init__(self, driver, element=None):
        self._driver = driver
        self._element = element
        self._touch_actions = []

    def add(self, *touch_actions):
        """Add TouchAction objects to the MultiAction, to be performed later.

        :Args:
         - touch_actions - one or more TouchAction objects describing a chain of actions to be performed by one finger
        :Usage:
            a1 = TouchAction(driver)
            a1.press(el1).move_to(el2).release()
            a2 = TouchAction(driver)
            a2.press(el2).move_to(el1).release()

            MultiAction(driver).add(a1, a2)
        """
        for touch_action in touch_actions:
            if self._touch_actions is None:
                self._touch_actions = []
            # deep copy, so that once they are in here, the user can't muck about
            self._touch_actions.append(copy.copy(touch_action))
        return self

    def perform(self):
        """Perform the actions stored in the object.
        :Usage:
            a1 = TouchAction(driver)
            a1.press(el1).move_to(el2).release()
            a2 = TouchAction(driver)
            a2.press(el2).move_to(el1).release()
            MultiAction(driver).add(a1, a2).perform()
        """
        self._driver._execute(Command.MULTI_ACTION, self.json_wire_gestures)
        # clean up and be ready for the next batch
        self._touch_actions = []
        return self

    @property
    def json_wire_gestures(self):
        actions = []
        for action in self._touch_actions:
            actions.append(action.json_wire_gestures)
        if self._element is not None:
            return {'actions': actions, 'elementId': self._element.id}
        else:
            return {'actions': actions} 