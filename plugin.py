###
# Copyright (c) 2014, spline
# All rights reserved.
#
#
###

# my libs
from travispy import TravisPy
# supybot libs
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Travis')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class Travis(callbacks.Plugin):
    """Add the help for "@plugin help Travis" here
    This should describe *how* to use this plugin."""
    threaded = True
    
    def __init__(self, irc):
        self.__parent = super(Travis, self)
        self.__parent.__init__(irc)
        self.travisAuth = False
        if not self.travisAuth:
            self.checkAuthorization()

    def die(self):
        self.__parent.die()

    def checkAuthorization(self):
        """Check Travis Auth."""
        
        if self.travisAuth:
            pass
        else:
            GitHubToken = self.registryValue('GitHubToken')
            if not GitHubToken:
                self.log.info("ERROR :: You need to set GitHubToken in the config values for Travis.")
                self.travisAuth = False
            else:  # we have key.
                try:  # we're good. authed.
                    t = TravisPy.github_auth(GitHubToken)
                    self.travisAuth = t
                    self.log.info("I have successfully logged into Travis using your credentials.")
                except Exception as e:
                    self.log.info("ERROR :: I could not auth with Travis :: {0}".format(e))
                    self.travisAuth = False
    
    def _travisrepos(self):
        """Handler to display repos."""

        # auth.
        t = self.travisAuth
        user = t.user()  # get user.
        repos = t.repos(member=user.login, active=True)  # get active repos.
        p = "{0}/".format(t.user().login)  # prefix.
        # now determine what to return.
        if len(repos) == 0:  
            return None
        else:  # found repos.
            o = " | ".join([i.slug.replace(p, '') for i in repos])
            return (len(repos), o)
    
    def travisbuild(self, irc, msg, args, optrepo):
        """<repo>
        
        Start a build on a repo.
        Ex: travis
        """

        # make sure we're authenticated.
        if not self.travisAuth:
            irc.reply("ERROR: You must be authenticated with Travis first. Set plugins.Travis.GitHubToken with your key, reload and try again.")
            return
        # now lets try this.
        t = self.travisAuth
        # lets use shorthand with the repository name.
        p = "{0}/".format(t.user().login)
        # make sure its a valid repo.
        try:
            repo = t.repo(p + optrepo)
            if not repo:
                irc.reply("ERROR: {0} is an invalid repo. Call travisrepos to see valid ones.".format(optrepo))
                return
        except Exception as e:
            irc.reply("ERROR: {0} repo caused an error. {1}".format(optrepo, e))
            return
        # valid repo.
        repo = t.repo(p + optrepo)
        
        try:
            build = t.build(repo.last_build_id)
            build.restart()
            irc.reply("Trying to restart build #{0} on {1} ({2} job(s)) for commit {3}".format(build.number, optrepo, len(build.jobs), build.commit.sha))
        except Exception as e:
            irc.reply("ERROR: Could not restart build on {0} :: {1}".format(optrepo, e))
            
    travisbuild = wrap(travisbuild, [('checkCapability', 'admin'), ('somethingWithoutSpaces')])

    def travisrepos(self, irc, msg, args):
        """
        Display valid Travis repositories for the user.
        """
        
        # make sure we're authenticated.
        if not self.travisAuth:
            irc.reply("ERROR: You must be authenticated with Travis first. Set plugins.Travis.GitHubToken with your key, reload and try again.")
            return
        # now lets try this.
        t = self.travisAuth
        user = t.user()  # get user.        
        # get repos.
        r = self._travisrepos()
        # now lets print.
        if not r:  # no repos found.
            irc.reply("ERROR: I could not find any repositories on Travis for you.")
        else:
            irc.reply("{0} repos({1}) on Travis :: {2}".format(user.login, r[0], r[1]))
        
    travisrepos = wrap(travisrepos, [('checkCapability', 'admin')])

    def travisrepoinfo(self, irc, msg, args, optrepo):
        """<repo slug>
        
        Display Travis information about a repo. Use only the slug.
        Ex: travis
        """

        # make sure we're authenticated.
        if not self.travisAuth:
            irc.reply("ERROR: You must be authenticated with Travis first. Set plugins.Travis.GitHubToken with your key, reload and try again.")
            return
        # now lets try this.
        t = self.travisAuth
        # lets use shorthand with the repository name.
        p = "{0}/".format(t.user().login)
        try:
            repo = t.repo(p + optrepo)
            if not repo:
                irc.reply("ERROR: {0} is an invalid repo. Call travisrepos to see valid ones.".format(optrepo))
                return
        except Exception as e:
            irc.reply("ERROR: {0} repo caused an error. {1}".format(optrepo, e))
            return
        # we're here if the repo info is valid.
        slug = repo.slug  # (str) Repository slug.
        desc = repo.description  # (str)  Description on GitHub.
        lbi = repo.last_build_id  # (int)  # Build ID of the last executed build.
        lbn = repo.last_build_number  # (str)  Build number of the last executed build.
        lbs = repo.last_build_state  # (str) Build state of the last executed build.
        lbd = repo.last_build_duration  # (str) Build duration of the last executed build.
        lbstart = repo.last_build_started_at  # (str) Build started at of the last executed build.
        lbfinish = repo.last_build_finished_at  # (str) ? Build finished at of the last executed build.
        #active = repo.active  # (bool) Whether or not the repository is active on Travis CI.
        # output to irc.
        irc.reply("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(optrepo, slug, desc, lbi, lbn, lbs, lbd, lbstart, lbfinish))
                
    travisrepoinfo = wrap(travisrepoinfo, [('checkCapability', 'admin'), ('somethingWithoutSpaces')])

    def travisuser(self, irc, msg, args):
        """
        Display information on Travis User.
        """

        # make sure we're authenticated.
        if not self.travisAuth:
            irc.reply("ERROR: You must be authenticated with Travis first. Set plugins.Travis.GitHubToken with your key, reload and try again.")
            return
        # now lets try this.
        t = self.travisAuth
        user = t.user()
        # attrs about user:
        login = user.login
        name = user.name
        is_syncing = user.is_syncing
        synced_at = user.synced_at
        created_at = user.created_at
        # print.
        irc.reply("Travis User: {0} Name: {1} Created: {2} Syncing? {3} Last sync: {4}".format(login, name, created_at, is_syncing, synced_at))

    travisuser = wrap(travisuser, [('checkCapability', 'admin')])
                
    def travis(self, irc, msg, args, optrepo):
        """<repo>
        
        Run test on repo.
        """
        
        ght = self.registryValue('GitHubToken')
        t = TravisPy.github_auth(ght)
        user = t.user()
        irc.reply("user.login {0}".format(user.login))
        repos = t.repos(member=user.login)
        irc.reply("Member Repos: {0}".format(" | ".join([i.slug for i in repos])))
        repo = t.repo(optrepo)
        build = t.build(repo.last_build_id)
        irc.reply("BUILD: {0}".format(build))
        build.restart()
        irc.reply("BUILD RESTART: {0}".format(build))

    travis = wrap(travis, [('somethingWithoutSpaces')])

Class = Travis


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
