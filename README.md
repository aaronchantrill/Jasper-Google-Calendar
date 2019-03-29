Naomi-Google-Calendar
======================

Naomi Google Calendar Module

Written By: Marc Poul Joseph Laventure

## Steps to install Google Calendar

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
* Create a project and select it from the dropdown menu.
* Click on "Enable APIs and Services."
* Find and click on "Google Calendar API."
* In the sidebar on the left, select Credentials.
* Click the "Create Credentials" button and select "OAuth client ID."
* Select "other" as application type.
* After creating the credentials, use the "Download JSON" button (looks like a downward pointing arrow) to download your json file. Save it in the ~/naomi directory (the same directory with profile.yml) as credentials.json. 
* Tell Naomi to shut down or open the console where Naomi is running and press CTRL-C to kill the process.
* Restart Naomi from Terminal on the Pi (i.e. don't SSH in)
```
./Naomi.py
```
* This should then open a web browser asking you to accept the authentication request. Accept it.
* Once accepted, Naomi will start up as normal.

## Congrats, Naomi Google Calendar is now installed and ready for use; here are some examples:
```
YOU: Add Calendar event
NAOMI: What would you like to add?
YOU: Movie with Jodie Friday at 5 pm
NAOMI: Added event 'Movie with Jodie on March 29 at 5:00 pm
NAOMI: Is this what you wanted?
YOU: yes
NAOMI: Okay, I added it to your calendar
YOU: Do I have any calendar events tomorrow?
NAOMI: 'Movie with Jodie at 5:00 pm
YOU: Do I have any calendar events today?
NAOMI: Test Event at 7:30 pm
```
Unfortunately, unless you go the full route and set up an OAuth consent screen on a server that you own the domain for (they require you to insert a txt record into the DNS record), 
you will only be able to use your credentials 100 times before getting a consent screen published.

I imagine there is both a way around having to have a desktop environment and GUI web browser on your Naomi server and a way to get around having the consent screen,
but I haven't found them yet. There seem to be infinite options available.

## Contributions from the following awesome debuggers/developers :)
```
@dansinclair25
@swcraig
```
