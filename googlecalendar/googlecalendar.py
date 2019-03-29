# -*- coding: utf-8 -*-
import datetime
import httplib2
import logging
import os
import pickle
import re
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from naomi import app_utils
from naomi import paths
from naomi import plugin
from naomi import profile


class GoogleCalendarPlugin(plugin.SpeechHandlerPlugin):

    monthDict = {'January': '01', 
            'February': '02', 
            'March': '03', 
            'April': '04', 
            'May': '05', 
            'June': '06', 
            'July': '07', 
            'August': '08', 
            'September': '09', 
            'October': '10', 
            'November': '11', 
            'December': '12'}


    # The scope URL for read/write access to a user's calendar data
    scope = 'https://www.googleapis.com/auth/calendar.events'
    creds = None
    service = None


    def __init__(self, *args, **kwargs):
        super(GoogleCalendarPlugin, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        # The picklefile is created when the user first authenticates.
        picklefile = os.path.join(paths.CONFIG_PATH,"token.pickle")
        secretsfile = os.path.join(paths.CONFIG_PATH,"credentials.json")
        if os.path.exists(picklefile):
            with open(picklefile, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no valid credentials, let the user log in
        if not (self.creds and self.creds.valid):
            if(self.creds and self.creds.expired and self.creds.refresh_token):
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    secretsfile,
                    self.scope
                )
                self.creds = flow.run_local_server()
            with open(picklefile,'wb')as token:
                pickle.dump(self.creds, token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_phrases(self):
        return [
            self.gettext("CALENDAR"),
            self.gettext("EVENTS"),
            self.gettext("CHECK"),
            self.gettext("ADD"),
            self.gettext("TODAY"),
            self.gettext("TOMORROW")
        ]

    def addEvent(self, mic):
        #service = build('calendar', 'v3', credentials=creds)
        while True:
            try:
                mic.say(self.gettext("What would you like to add?"))
                eventData = mic.active_listen()
                createdEvent = self.service.events().quickAdd(
                    calendarId='primary',
                    text=eventData
                ).execute()
                eventRawStartTime = createdEvent['start']
                
                m = re.search(
                    "".join([
                        '([0-9]{4})-([0-9]{2})-([0-9]{2})',
                        'T([0-9]{2}):([0-9]{2}):([0-9]{2})'
                    ]),
                    str(eventRawStartTime)
                )
                eventDateYear = str(m.group(1))
                eventDateMonth = str(m.group(2))
                eventDateDay = str(m.group(3))
                eventTimeHour = str(m.group(4))
                eventTimeMinute =  str(m.group(5))
                appendingTime = "am"

                if len(eventTimeMinute) == 1:
                    eventTimeMinute = eventTimeMinute + "0"

                eventTimeHour = int(eventTimeHour)

                if ((eventTimeHour - 12) > 0 ):
                        eventTimeHour = eventTimeHour - 12
                        appendingTime = "pm"
            
                dictKeys = [
                    key for key, val in self.monthDict.items()
                    if val==eventDateMonth
                ]
                eventDateMonth = dictKeys[0]
                mic.say(" ".join([
                    self.gettext("Added event"),
                    createdEvent['summary'],
                    self.gettext("on"),
                    str(eventDateMonth),
                    str(eventDateDay),
                    self.gettext("at"),
                    str(eventTimeHour) + ":" + str(eventTimeMinute),
                    appendingTime
                ]))
                
                responded = False
                while responded == False:
                    mic.say("Is this what you wanted?")
                    # convert the userresponse into a string
                    userResponse = mic.active_listen()
                    if type(userResponse) is list:
                        userResponse = " ".join(userResponse)
                    if app_utils.is_positive(userResponse):
                        mic.say("Okay, I added it to your calendar")
                        return
                    if app_utils.is_negative(userResponse):
                        responded = True
                        self.service.events().delete(
                            calendarId='primary',
                            eventId=createdEvent['id']
                        ).execute()

            except KeyError:

                mic.say(self.gettext("Could not add event to your calendar; check if internet issue."))
                responded = False
                while not responded:
                    mic.say(self.gettext("Would you like to attempt again?"))
                    responseRedo = mic.active_listen()

                    if app_utils.is_negative(responseRedo):
                        return
                    if app_utils.is_positive(responseRedo):
                        responded = True

    def getEventsToday(self, mic):

        tz = app_utils.get_timezone(profile.get_profile())
        #service = build('calendar', 'v3', credentials=creds)

        # Get Present Start Time and End Time in RFC3339 Format
        d = datetime.datetime.now(tz=tz)
        utcString = d.isoformat()	
        m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
        utcString = str(m.group(0))
        todayStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
        todayEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString
        page_token = None
        
        while True:

            # Gets events from primary calendar from each page in present day boundaries
            events = self.service.events().list(
                calendarId='primary',
                timeMin=todayStartTime,
                timeMax=todayEndTime,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            #events_result = service.events().list(calendarId='primary', timeMin=now,
            #    maxResults=10, singleEvents=True,
            #    orderBy='startTime').execute()

            if(len(events['items']) == 0):
                mic.say("You have no events scheduled for today")
                return

            for event in events['items']:

                try:
                    eventTitle = event['summary']
                    eventTitle = str(eventTitle)
                    eventRawStartTime = event['start']
                    eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                    temp = eventRawStartTime[1]
                    startHour, startMinute, temp = temp.split(":", 2)
                    startHour = int(startHour)
                    appendingTime = "am"

                    if ((startHour - 12) > 0 ):
                        startHour = startHour - 12
                        appendingTime = "pm"

                    startMinute = str(startMinute)
                    startHour = str(startHour)
                    mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime) # This will be mic.say

                except KeyError as e:
                    mic.say("Check Calendar that you added it correctly")
                
            page_token = events.get('nextPageToken')

            if not page_token:
                return


    def getEventsTomorrow(self, mic):

        # Time Delta function for adding one day 
        
        one_day = datetime.timedelta(days=1)
        tz = app_utils.get_timezone(profile.get_profile())
        #service = build('calendar', 'v3', credentials=creds)
        
        # Gets tomorrows Start and End Time in RFC3339 Format

        d = datetime.datetime.now(tz=tz) + one_day
        utcString = d.isoformat()
        m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
        utcString = m.group(0)
        tomorrowStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
        tomorrowEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString

        page_token = None

        while True:

            # Gets events from primary calendar from each page in tomorrow day boundaries

            events = self.service.events().list(calendarId='primary', pageToken=page_token, timeMin=tomorrowStartTime, timeMax=tomorrowEndTime).execute()
            if(len(events['items']) == 0):
                mic.say("You have no events scheduled Tomorrow")
                return
        
            for event in events['items']:
                
                try:
                    eventTitle = event['summary']
                    eventTitle = str(eventTitle)
                    eventRawStartTime = event['start']
                    eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                    temp = eventRawStartTime[1]
                    startHour, startMinute, temp = temp.split(":", 2)
                    startHour = int(startHour)
                    appendingTime = "am"

                    if ((startHour - 12) > 0 ):
                        startHour = startHour - 12
                        appendingTime = "pm"

                    startMinute = str(startMinute)
                    startHour = str(startHour)
                    mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime) # This will be mic.say

                except KeyError as e:
                    mic.say("Check Calendar that you added it correctly")
                
            page_token = events.get('nextPageToken')
            
            if not page_token:
                return


    def handle(self, text, mic):
            
        if bool(re.search('Add', text, re.IGNORECASE)):
            self.addEvent(mic)

        if bool(re.search('Today', text, re.IGNORECASE)):
            self.getEventsToday(mic)

        if bool(re.search('Tomorrow', text, re.IGNORECASE)):
            self.getEventsTomorrow(mic)


    def is_valid(self, text):
        return any(p.upper() in text.upper() for p in [self.gettext("CALENDAR")])
