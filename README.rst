====================
 Serverless Transit
====================

Users subscribe to transit authority, line, maybe station. We collect
information about status from twitter and transit authorities. When we
have enough confidences there is a real incident, we send the
subscribers an SNS alert.

Data Model
==========

Subscriber
----------

DynamoDB PK + SK: define transit and line they are interested in, with
SK holding start/end time of interest; attibutes includes phone number for SNS

pk: subscriber:wmata:orange
sk: 07:00:00-09:00:00
subscriber_phone: 703-555-1212
transit_authority: wmata
transit_line: orange
transit_station: ballston  # for future use if we can get this specific

One of the judges suggested using separate entries for start and
stoop, so we can do limited queries, but then need to do the set
intersection in the code. Or we could put the start time in the SK and
put the stop time on an attribute with a LSI.


Report
------

DynamoDB PK + SK: define transit and line with timestamp
Attributes define the contents of the report, with "status" being our analysis.

pk: report:wmata:orange
sk: 07:00:15

transit_line: orange
transit_authority: wmata
transit_station: ballston
report_source: twitter:@unsuckdcmetro
report_text: I've never seen the Ballston Metro this hectic. Silver line is shut down except between Ballston and Wiehle Reston. Orange running every 15 min. They are queuing people up to head into D.C. from Ballston. #dcmetro #commute @DCMetroandBus @dcmetrohero
status: delay

Incident
--------

If we get a Report from the transit authority, or enough Twitter
reports of the same line within a small amount of time (e.g., 30
minutes), we create an Incident. This will trigger a lambda to send an
SNS to Subscribers of that line (if within time of interest).

PK + SK indicates incident and time we conclude we have confirmed it. Attributes summarize the information, perhaps confirming that a transit authority has announced it or the number of Twitter reports we've seen, and timestamps of our first and last Reports.

pk: incident:wmata:silver
sk: 2019-10-07T16:21:27

transit_line: orange
transit_authority: wmata
transit_station: ballston
status: delay
incident_first: 2019-10-07T16:20:00
incident_latest: 2019-10-07T16:22:22
incident_details: Reported by 5 tweets, announced by WMATA

