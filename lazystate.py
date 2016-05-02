#! /usr/bin/python
#
# -*- coding: utf-8; -*-
#
# maintained by Charlie O'Leary @ https://github.com/charlieoleary/lazystate
#
# lazyState is aimed at being a *VERY* simple method for tracking states of
# various outcomes, particularly in the case of Sensu.  This can be easily
# integrated into a Sensu check to track failures and return appropriate error
# codes based on the number of times a check has failed without relying on
# the Sensu Plugin.
#
# To use, simply import the script as a module and execute the following after
# your checks have confirmed success or failure:
#
# from lazyState import lazyState
# Success: lazyState(checkName).updateState()
# Failure: lazyState(checkName, True).updateState()
#
# By default, state files are stored in /tmp/states/<ls_service>.lazystate,
# will trigger a warning after 3 failures and a critical after 5.  To override
# these values, simply provide the following arguments:
#
# lazyState(checkName, True, 1, 3, "/etc/sensu/states", ".statefile")
#
# The above example will cause a check to return a warning after 1 failure, a
# critical after 3 failures, and will store checks in /etc/sensu/states with the
# extension .statefile.
#

import json
import time
import os

class lazyState(object):

  def __init__(self, ls_service, ls_fail=False, ls_warn=3, ls_crit=5, ls_store="/tmp/states", ls_store_extension=".lazystate"):

    # base variables and default format
    self.ls_store = ls_store
    self.ls_store_extension = ls_store_extension
    self.ls_service = ls_service
    self.ls_warn = ls_warn
    self.ls_crit = ls_crit
    self.ls_fail = ls_fail
    self.format = {"outcome": 0, "last_check": 0, "fails": 0}

    # create state directory if it doesn't exist
    if not os.path.exists(self.ls_store):
      os.makedirs(self.ls_store)

    # attempt to read the state file
    if os.path.exists(self.ls_store + "/" + self.ls_service + self.ls_store_extension):
      self.ls_file = open(self.ls_store + "/" + self.ls_service + self.ls_store_extension, "r+")
      # validate and parse the json within the state file
      try:
        self.ls_stats = json.loads(self.ls_file.read())
      # if json is invalid, recreate the file with the base state
      except ValueError:
        print "failed"
        self.ls_stats = self.format
        self.ls_file.write(json.dumps(self.ls_stats))
    # if state file does not exist, create it with the base state
    else:
      self.ls_stats = self.format
      self.ls_file = open(self.ls_store + "/" + self.ls_service + self.ls_store_extension, "w+")
      self.ls_file.write(json.dumps(self.ls_stats))

  # handle the state change
  def updateState(self):

    # if the state is failing, update the state count
    if (self.ls_fail is True):
      self.ls_stats["fails"] += 1
      self.ls_stats["last_check"] = int(time.time())

      # set the appropriate exit code based on the number of failures within the state file
      if self.ls_stats["fails"] >= self.ls_crit:
        exit_code = 2
      elif self.ls_stats["fails"] >= self.ls_warn:
        exit_code = 1
      else:
        exit_code = 0

      # write the state file and return the exit code
      self.ls_stats["outcome"] = exit_code
      self.ls_file = open(self.ls_store + "/" + self.ls_service + self.ls_store_extension, "w+")
      self.ls_file.write(json.dumps(self.ls_stats))
      return exit_code

    # if the state is not failing, update the state file
    else:
      self.ls_stats["fails"] = 0
      self.ls_stats["last_check"] = int(time.time())
      self.ls_stats["outcome"] = 0

      self.ls_file = open(self.ls_store + "/" + self.ls_service + self.ls_store_extension, "w+")
      self.ls_file.write(json.dumps(self.ls_stats))

      return 0
