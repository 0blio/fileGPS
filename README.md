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
When you upload a file on a web-server using a file upload functionality, usually the file get renamed in various ways in order to prevent direct access to the file, RCE and file overwrite.

fileGPS is a tool that uses various techniques to find the new filename, after the server-side script renamed and saved it.

Some of the techniques used by fileGPS are:

* Various hash of the filename
* Various timestamps tricks
* Filename + PHP time() up to 5 minutes before the start of the script
* So many more

![demo](https://i.ibb.co/SwDkS7r/file-GPSscreen.png)

### Features
* Easy to use
* Multithreaded
* HTTP(s) Proxy support
* User agent randomization
* Over 100.000 filenames combinations

### Requirements
* Python
* Python requests library

### Documentation and examples
Please, refer to the LINK_ALLA_WIKI.

Video tutorial: LINK_AL_VIDEO

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

