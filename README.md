Malawi music machine
====================

> NOTE: WIP

Malawi Music Machine is an experimental project to build an API and tools over
the [malawi-music.com](http://malawi-music.com) website.

## GOALS

* Develop a REST API for sharing information about Artists, Albums and Songs from the malawi-music.com website
* Provide functionality to download songs in "bulk" via the API
* Create a machine-learning model that "recognizes" music downloaded from malawi-music.com
* Build an example music web application that uses the API with React

## Architecture

* [collect](./collect) - tools for collecting data about artists, albums, songs etc.. from the website. 
* [api](./api/README.md)     - JSON REST API
* [webapp](./webapp/README.md)  - React application
* [analyzer](./analyzer/README.md) - Analysis of MP3 Data of the songs

