## What is the ACARS Bridge?

The ACARS Bridge enables you to send and receive Pre-departure clearance and CPDLC requests with SayIntentions.AI's ATC whilst remaining on Hoppie’s ACARS network. This is typically when direct communication with SayIntentions.AI's ACARS network from your aircraft  isn’t possible.   

<img width="616" alt="image" src="https://github.com/user-attachments/assets/de254b82-ff46-442c-831f-27a5741c491e">


It has been built by Dave Black, to allow more pilots to use the SayIntentions.AI's ACARS network. It is available from [https://vsrsoftware.com/bridge](https://vsrsoftware.com/bridge) 

<img width="585" alt="image" src="https://github.com/user-attachments/assets/78053122-5bd4-4406-b4cc-0320e35ccbe4">


## What aircraft and simulators does it support?

Currently tested with: 

* PMDG’s 777 (MSFS)  
* Fly by Wire’s A32NX. (MSFS)  
* Toliss’ A330-900 in (X-Plane 12\)

It should support any ACARS equipped aircraft compatible with Hoppie’s network.

Since It is agnostic of the simulator, you can use it with any simulator supported by Sayintentions.AI.

## How does it work?

The bridge creates a unique 4-character ATSU callsign, allowing you to request a PDC or CPDLC response from the Sayintentions.AI's. ATC controllers whilst still using Hoppie’s network.

You can send CPDLC and/or PDC messages to this callsign from your aircraft, when signed onto Hoppie's ACARS network. 

The bridge polls Hoppie’s network for messages for this callsign, and polls the Sayintentions.AI's ACARS network for messages to the callsign in your latest SimBrief plan. It then forwards these messages onto their respective networks.

<img width="655" alt="image" src="https://github.com/user-attachments/assets/9b99d926-a672-48ce-bb1f-0a9cb27bac53">


## Do I lose anything by using it?

You gain far more than you lose; a few things to consider? 

* You will be able to both send/receive ACARS/CPDLC messages to/from any station on Hoppie’s network.  
* You can only send/receive messages to/from SayIntentions.AI ATC controllers on their network.   
* If you are using an ACARS connected Virtual Airline, make sure they are connected to Hoppie’s network. They will send messages directly to your callsign. You cannot send messages to a VA that is only connected to SayIntentions.AI.  
* If you start on an ACARS network using the bridge then stay with it throughout the flight . If you plan to use the VATSIM to SayIntentions.AI handoff, then continue to use the bridge for CPDLC.  
* Many aircraft get their weather from a number of sources; this includes real world sources, VATSIM etc. If you use the bridge it is recommended that you use either voice ATIS, the SayIntentions.AI App or alternative tools such as [VSR](https://www.youtube.com/watch?v=Z2nJshEuRvE) to get the ATIS for a SayIntentions.AI airport.

## Configuration

The following information is required when you 1st run the bridge:

* Your Hoppie Logon ([Register](https://www.hoppie.nl/acars/system/register.html))  
* Your SayIntentions API Key (from the [Pilot Portal](https://portal.sayintentions.ai/portal/account/))  
* Your SimBrief Pilot ID (from [your account)](https://dispatch.simbrief.com/account)

<img width="412" alt="image" src="https://github.com/user-attachments/assets/6df14a6f-aef7-45fa-80db-a449e5c8c733">


Use your Hoppie ID to configure the aircraft’s ACARS options, ***not*** your SayIntentions.AI API key. 

## Operation

The bridge will then listen on both networks and forward messages between them. It will inform you of the ATSU callsign to use. 

You enter the 4 character code wherever the client expects a destination station, for instance its the *facility* field on the PMDG 777\. So if you’d use EGLL for a PDC, use the bridge’s code instead.

Remember to turn off the bridge when you complete your flight or plan to use another tool such as [FSM](http://fsm.vsrsoftware.com) or another aircraft with built in ACARS. This is because the ACARS POLL command deletes messages from the server, so whichever system gets their first, gets all the latest messages.

A configuration file (bridge.ini) is created in the same directory as the programme; this contains the configuration information, should you need to change it.  

<img width="417" alt="image" src="https://github.com/user-attachments/assets/fcd9bcd6-afbf-43c4-92c9-e36eb76dfb55">


## Debugging

It is worth remembering that you need to have setup the aircraft to send messages on Hoppie’s ACARS network \- initially check:

[https://www.hoppie.nl/acars/system/log.html](https://www.hoppie.nl/acars/system/log.html)

Search for messages from your callsign to the bridge generated callsign , if they are not reaching here, then the Bridge cannot see them. Check online help tutorials and videos on how to set up the aircraft for Hoppie’s network. 

After that use the SayIntentions.AI ACARS log to search for the messages from your callsign to the bridge generated callsign and vice versa for messages from SayIntentions controllers. 

[https://acars.sayintentions.ai/dump](https://acars.sayintentions.ai/dump)

Check if the messages have been read, if not, check the Bridge is running (possibly restart it).

Check you aren’t running any other ACARS clients that maybe polling either network with your callsign (such as FSM or VSR).

 
