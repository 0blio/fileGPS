<h1 align="center">
  <br>
  <a href="https://github.com/0blio/fileGPS"><img src="https://i.ibb.co/fGcyM2Y/fileGPS.png" alt="fileGPS" border="0" width="180"></a>
  <br>
  fileGPS
  <br>
</h1>

<h4 align="center">HTTP filename upload guesser</h4>

<p align="center">
  <a href="https://github.com/0blio/gileGPS/releases">
    <img src="https://img.shields.io/badge/Release-v0.2-blue.svg">
  </a>
  <img src="https://img.shields.io/badge/Licence-GPL3-brightgreen.svg">
  <img src="https://img.shields.io/badge/God-Not%20found-red.svg">
</p>

### Introduction
When you upload a shell on a web-server using a file upload functionality, usually the file get renamed in various ways in order to prevent direct access to the file, RCE and file overwrite.

fileGPS is a tool that uses various techniques to find the new filename, after the server-side script renamed and saved it.

Some of the techniques used by fileGPS are:

* Various hash of the filename
* Various timestamps tricks
* Filename + PHP time() up to 5 minutes before the start of the script
* So many more

![screen](https://i.ibb.co/jrtCm0Y/file-GPSscreen.png | width=100)

### Features
* Easy to use
* Multithreaded
* HTTP(s) Proxy support
* User agent randomization
* Over 100.000 filenames combinations

### Requirements
* Python
* Python requests library

### How to write a module
Writing a module is fairly simple and allows you to implement your custom ways of generating filename combinations.

Below is a template for your modules:
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Module name: test
  Coded by: Your name / nickname
  Version: X.X
  
  Description:
    This module destroy the world.
"""
output = []

# Do some computations here

output = ["filename1.php", "filename2.asp", "filename3.jar"]
```

The variables `url` and `filename` are automatically imported from the core script, so you can call them in your module.

Once you finished to write your module, you have to save it in `Modules/`, and it will be automatically imported once the main script is started.

You can use the module [shame](https://github.com/0blio/fileGPS/blob/master/Modules/shame.py) as a template for your modules.


### Contribute to the project
Do you want to help? Here's some ways you can do it:

* Suggest a feature
* Write a module
* Report a bug

### Contacts
Email: michele.cisternino@protonmail.com

### Special thanks
Special thanks to Panfilo Salutari for sharing with me ideas about the project.

Thanks to Claudio Sala for the logo.

### Save an hacker from starvation by making a donation
[![Foo](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.me/0blio)

