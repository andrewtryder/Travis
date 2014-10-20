###
# Copyright (c) 2014, spline
# All rights reserved.
#
#
###

import os
from supybot.test import *

class TravisTestCase(PluginTestCase):
    plugins = ('Travis',)

    def setUp(self):
        PluginTestCase.setUp(self)
        GitHubToken = os.environ.get('GitHubToken')
        conf.supybot.plugins.Travis.GitHubToken.setValue(GitHubToken)
        
    def testTravis(self):
        self.assertSnarfResponse('reload Travis', 'The operation succeeded.')

    def testTravisUser(self):
        self.assertNotError('travisuser')



# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
