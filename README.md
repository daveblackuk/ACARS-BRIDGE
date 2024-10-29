# **ACARS Bridge**

The ACARS bridge enaables aircraft to communicate with Sayintentions.AI's ACARS network even though there is no direct method of communications.

This is achieved by bridging between Hoppie's ACARS network and Sayintentions.AI's ACARS network; a unique 4 character ATSU Callsign is created for the client aircraft to use when sending PDC, Telex and CPDLC messages to the Sayintentions.AI's ACARS network via Hoppie's network.

Users send CPLDC and/or PDC messages to this callsign from their aircraft, when signed onto the Hoppie's ACARS network. The bridge polls the Sayintentions.AI's ACARS network using the aircraft's callsign from your latest SimBrief plan.

![Slide1](https://github.com/user-attachments/assets/011b27c5-ea01-4520-bea2-f0b2b7b8b8fe)

## Configuration

The following information is required

* Your Hoppie Logon ([Register](https://www.hoppie.nl/acars/system/register.html "Register for Hoppie"))
* Your SayIntentions API Key (from the [Pilot Portal](https://portal.sayintentions.ai/portal/account/ "pilot portal"))
* Your SimBrief Pilot ID (from [your account)](https://dispatch.simbrief.com/account "SB ccount")

<img width="433" alt="image" src="https://github.com/user-attachments/assets/4ecbfb8a-8022-457e-befc-d71eef1a440b">

## Operation

The bridge will then listen on both networks and forward messages between them.

<img width="901" alt="image" src="https://github.com/user-attachments/assets/26e2267f-e98a-496d-a443-42faea927bca">

## Maintenance

A configuration file (bridge.ini) is created in the same directory as the programme; this contains the configuration information.


Buy me a Coffee
