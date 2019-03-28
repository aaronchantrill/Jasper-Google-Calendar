Naomi-Google-Calendar
======================

Naomi Google Calendar Module

Written By: Marc Poul Joseph Laventure

##Steps to install Google Calendar

* Install/run the following in your home directory
```
pip3 install httplib2
pip3 install --upgrade google-api-python-client
pip3 install --upgrade python-gflags
```
* run the following commands in order:
```
cd ~/Naomi/plugins/speechhandler
git clone https://github.com/aaronchantrill/Jasper-Google-Calendar.git
```
* Login to [Google developer Console](https://console.developers.google.com/project) and complete the following
* The Client ID in Google needs to be for a native application.
```
Create a project and select it from the dropdown menu
Click on "Enable APIs and Services"
Find and click on "Google Calendar API"
In the sidebar on the left, select Credentials.
Click the "Create Credentials" button
Get Client ID and Client Secret (Save for later)
```
* Open Calendar.py and add Client ID and Client secret to appropriate variables

* Tell Naomi to shut down or open the console where Naomi is running and press CTRL-C to kill the process.
* Restart Naomi from Terminal on the Pi (i.e. don't SSH in)
```
./Naomi.py
```
* This should then open a web browser asking you to accept the authentication request. Accept it.
* Once accepted, Naomi will start up as normal.

##Congrats, Naomi Google Calendar is now installed and ready for use; here are some examples:
```
YOU: Add Calendar event
NAOMI: What would you like to add?
YOU: Movie with jodie Friday at 5 pm
NAOMI: Added event Movie with jodie on June 06 at 5:00 pm
NAOMI: Is this what you wanted?
YOU: Yes
NAOMI: Okay, I added it to your calendar
YOU: Do I have any Calendar events tomorrow
Naomi: Dinner with jodie at 9:00 pm
YOU: Do I have any Calendar Events Today
NAOMI: Dinner with jodie at 6:00 pm
```
##Contributions from the following awesome debuggers/developers :)
```
@dansinclair25
@swcraig
```
