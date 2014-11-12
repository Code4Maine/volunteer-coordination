
VolunteerHub
============

[![Build Status](https://travis-ci.org/Code4Maine/volunteer-coordination.svg?branch=master)](https://travis-ci.org/Code4Maine/volunteer-coordination) [![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/Code4Maine/volunteer-coordination?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Stories in Ready](https://badge.waffle.io/code4maine/volunteer-coordination.png?label=ready&title=Ready)](https://waffle.io/code4maine/volunteer-coordination)

*Use the "Ready" badge above to scope out open issues and see you can help. And
be sure to join us in the Gitter chat room too.*

Volunteer Hub is a volunteer coordination system that allows organizations to 
create projects and opportunities that people can then browse and select to 
volunteer for the organizations.

Organizations create a profile and can add large projects as well as individual 
volunteering opportunities. Users can then search through available tasks and 
can select and assign themselves to tasks that they are qualified for.

If an organization has a task that requires training or acceptance of the 
volunteer's application, the volunteer can easily make a request to the 
opportunity and an employee of the organization can approve or deny their request.

The website and Android application work together to access the same database.

Group Members
-------------------
- Zack Schiller
- Nate Welch
- Colin Powell
- Leslie Mercier
- Chris Violette
- Dan Pratt
- Christian Roberts

Getting started
---------------

To get the project running locally, first you have to install:

  * Vagrant
  * Virtualbox
  * Ansible

A google search should provide instructions for those on your operating system.
The trickest to find might be ansible, which may have be installed as a python
module using easy_install or pip.

Once you've got those, simply type:

    $ vagrant up

In the project's home directory. The ansible provisioner goes about it's
business bootstrapping an Ubuntu 14.04 LTS virtual machine for the project.

You may then edit code directly on your computer in the project home directory.
But to see changes reflected on the virtual machine you will have to:

    $ vagrant ssh
    $ sudo restart volunteerhub_Dev

You could also "reprovision" the virutalbox like so:

    $ vagrant provision

Because ansible is indempodent, nothing will be changed but what needs to be
changed and the application will be restarted.

