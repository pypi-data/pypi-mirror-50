############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python Client Helpers
# Description:   Helpers class providing common helper functions to the iotJumpWay MQTT
#                Python Clients.
# Last Modified: 2019-04-07
#
############################################################################################

import os
import logging
import logging.handlers as handlers

from requests.auth import HTTPBasicAuth


class Helpers():

    def __init__(self, cName):
        """ Initiates the Helpers class """

        self.cName = cName
        self.setLogging()

    def setLogging(self):
        """ Sets up logging for the NLU device. """

        self.logger = logging.getLogger(self.cName)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        allLogHandler = handlers.TimedRotatingFileHandler(
            self.lConfs["Logs"] + 'all.log', when='H', interval=1, backupCount=0)
        allLogHandler.setLevel(logging.INFO)
        allLogHandler.setFormatter(formatter)

        errorLogHandler = handlers.TimedRotatingFileHandler(
            self.lConfs["Logs"] + 'error.log', when='H', interval=1, backupCount=0)
        errorLogHandler.setLevel(logging.ERROR)
        errorLogHandler.setFormatter(formatter)

        warningLogHandler = handlers.TimedRotatingFileHandler(
            self.lConfs["Logs"] + 'warning.log', when='H', interval=1, backupCount=0)
        warningLogHandler.setLevel(logging.WARNING)
        warningLogHandler.setFormatter(formatter)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)

        self.logger.addHandler(allLogHandler)
        self.logger.addHandler(errorLogHandler)
        self.logger.addHandler(warningLogHandler)
        self.logger.addHandler(consoleHandler)

        self.logger.info("Class " + self.cName + " logging setup complete.")
