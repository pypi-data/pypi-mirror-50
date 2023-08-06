# gh

[![Build Status](https://travis-ci.org/dvershinin/gh.svg?branch=master)](https://travis-ci.org/dvershinin/gh)
[![PyPI version](https://badge.fury.io/py/gh-api.svg)](https://badge.fury.io/py/gh-api)

Low-level GitHub API request interface. With caching.

It's similiar to the official `hub api`, but:

* only `GET` commands supported
* automatic caching by `ETag` and `Cache-Control` will speed up repeat queries and won't burn your rate limit
* based on Python

## Synopsis

    gh repos/dvershinin/lastversion/license # outputs JSON with license of a given repo

## Install

    pip install --user gh-api