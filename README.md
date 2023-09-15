# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
	This Repo is created to run VV E2E API script.
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
	You just need to pass ship and shore url in pytest run command in order to run this job
* Configuration
	VV Dev:
		--shore https://dev.virginvoyages.com/svc/ --ship https://application-dev.ship.virginvoyages.com/svc/
	VV Int:
		--shore https://int.gcpshore.virginvoyages.com --ship https://application-integration.ship.virginvoyages.com/svc/
	VV Cert:
		--shore https://qa.virginvoyages.com/svc/ --ship https://k8s-qaship.virginvoyages.com/
	VV Stage:
		--shore=https://stage.virginvoyages.com/svc/

* Dependencies
	There is no dependency as of now in order to run this.
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###
	If you get stuck anywhere Please reach out to sarvesh.singh@decurtis.com

* Repo owner or admin
    Decurtis
* Other community or team contact

### Install Docker for UI Debugging ###
* brew install docker
* brew install docker-completion
* brew install docker-compose
* brew install docker-compose-completion

### Docker Compose Commands ###
* docker-compose --file docker-compose.yaml up -d hub chrome
* docker-compose --file docker-compose.yaml down
* docker-compose --file docker-compose.yaml restart hub chrome