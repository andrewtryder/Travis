[![Build Status](https://travis-ci.org/reticulatingspline/Travis.svg?branch=master)](https://travis-ci.org/reticulatingspline/Travis)

# Supybot / Limnoria plugin for working with Travis CI continuous Integration Platform

## Introduction

This is an IRC plugin for interacting with the Travis CI platform through its API.


## Install

You will need a working Limnoria bot on Python 2.7 for this to work.

Go into your Limnoria plugin dir, usually ~/supybot/plugins and run:

```
git clone https://github.com/reticulatingspline/Travis
```

To install additional requirements, run:

```
pip install -r requirements.txt 
```

or if you don't have or don't want to use root, 

```
pip install -r requirements.txt --user
```

Next, load the plugin:

```
/msg bot load Travis
```

Next, you will need to configure your GitHub Auth Token. Go [here]() and under Personal access tokens,
generate a new one with these scopes:

- read:org
- user:email
- repo_deployment
- repo:status
- write:repo_hook

Once, complete, they will issue a token to you on the page. Copy and paste this and configure the bot:

```
/msg bot config plugins.Travis.GitHubToken <token>
```

Next, reload the plugin.

```
/msg bot reload Travis
```

You are now done.

## About

All of my plugins are free and open source. When I first started out, one of the main reasons I was
able to learn was due to other code out there. If you find a bug or would like an improvement, feel
free to give me a message on IRC or fork and submit a pull request. Many hours do go into each plugin,
so, if you're feeling generous, I do accept donations via Amazon or browse my [wish list](http://amzn.com/w/380JKXY7P5IKE).

I'm always looking for work, so if you are in need of a custom feature, plugin or something bigger, contact me via GitHub or IRC.