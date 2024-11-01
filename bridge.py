import requests
import re
import logging

# Set up logging
logging.basicConfig(
    #filename='acars_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)



import random
import time
import configparser
from hash_userid import *
import threading
from colors import *
import os, sys

version = "0.2024.11.1"
hoppie_logon = ""
hoppie_url = ""
sai_logon = ""
sai_url = ""
simbrief_id = ""

config = configparser.ConfigParser()


def get_config():
  try:
    global hoppie_logon, hoppie_url, sai_logon, sai_url, simbrief_id   
    if not os.path.exists('bridge.ini'):
        config.add_section('Settings')
        with open('bridge.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read('bridge.ini')
        hoppie_logon = config.get('Settings', 'hoppie_logon',fallback="")
        hoppie_url = config.get('Settings', 'hoppie_url', fallback='www.hoppie.nl')
        sai_logon = config.get('Settings', 'sayintentions_api_key',fallback="")
        sai_url = config.get('Settings', 'sayintentions_url', fallback='acars.sayintentions.ai')
        simbrief_id = config.get('Settings', 'simbrief_id',fallback="")
        return True
  except Exception as e:
    logging.error(f"Error reading configuration: {e}")


def set_configuration():

    print(f"Please enter the following configuration settings:\n")
    # Get user input for configuration
    hoppie_logon_input = input(f"Enter Hoppie Logon [{hoppie_logon}]: ").strip() or hoppie_logon
    simbrief_id_input = input(f"Enter SimBrief ID [{simbrief_id}]: ").strip() or simbrief_id
    sai_logon_input = input(f"Enter SayIntentions API Key [{sai_logon}]: ").strip() or sai_logon

    if not hoppie_logon_input or not simbrief_id_input or not sai_logon_input:
        logging.error(f" {red} Configuration values cannot be empty. Exiting.")
        sys.exit(1)

    # Save the configuration to the INI file
    config.set('Settings', 'hoppie_logon', hoppie_logon_input)
    config.set('Settings', 'simbrief_id', simbrief_id_input)
    config.set('Settings', 'sayintentions_api_key', sai_logon_input)
    with open('bridge.ini', 'w') as configfile:
            config.write(configfile)



  
def get_simbrief_plan(simbrief_id):
    logging.info(f"Fetch plan: {simbrief_id}")
    url = f"https://www.simbrief.com/api/xml.fetcher.php?json=1&userid={simbrief_id}" 
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()  # Corrected method call
        logging.info(f'Received SB Callsign: {json_data["atc"]["callsign"]}')
        return json_data 
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting SB Plan {e}")
        return {}


def poll_backend(source_url, source_logon, source_callsign, target_url, target_logon):
    # Step 1: Poll the URL
    poll_url = f"http://{source_url}/acars/system/connect.html?logon={source_logon}&to=SERVER&type=poll&from={source_callsign}&packet=Nought"
    #logging.info(f"Polling URL: {poll_url}")

    try:
        response = requests.get(poll_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_text = response.text
        response_text = response_text.replace('\r', '').replace('\n', '')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error polling URL: {e}")
        return
    try:
        # Step 2: Parse the response using regex
        pattern = r"\{(?P<from>[A-Z0-9]+) (?P<type>\w+) \{(?P<packet>.*?)\}\}"
        matches = re.finditer(pattern, response_text)

        # List to store parsed messages
        messages = []

        # Parse each match and store it in the list
        for match in matches:
            message = {
                "from": match.group("from"),
                "type": match.group("type"),
                "packet": match.group("packet").strip()
            }

            logging.info(f'Polling {source_url} From: {match.group("from")} To: {source_callsign} Message: {match.group("packet")} ')

            messages.append(message)
    except Exception as e:
        logging.error(f"Error parsing response: {e}")
       

  
    # Step 3: Create and send the GET request for each message
    for message in messages:
        try:
            get_request_url = (
                f"http://{target_url}/acars/system/connect.html?"
                f"logon={target_logon}&"
                f"from={message['from']}&"
                f"to={source_callsign}&"
                f"type={message['type']}&"
                f"packet={message['packet']}"
        )
        except Exception as e:
            logging.error(f"Error creating GET request: {e}")
            continue
  
        try:
            sai_response = requests.get(get_request_url)
            sai_response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending GET request: {e}")
            continue
        return len(messages)


def poll_hoppie():    
    try:
         logging.info(f"Polling Hoppie ACARS {hoppie_url} for ATSU:  {atsu_string}")

         while True:
             poll_backend(
                 hoppie_url,
                 hoppie_logon,
                 atsu_callsign,
                 sai_url,
                 sai_logon
             )

             hoppie_sleep_time = int(random.uniform(22, 30))
             time.sleep(hoppie_sleep_time)
    except Exception as e:
        logging.error(f"Error polling Hoppie: {e}")

def poll_si():    
    try:
        logging.info(f"Polling SI ACARS {sai_url} for Callsign: {callsign_string}")
        while True:
            poll_backend(
                    sai_url,
                    sai_logon,
                    sb_callsign,
                    hoppie_url,
                    hoppie_logon,
            )


            si_sleep_time = int(random.uniform(5, 15))
            time.sleep(si_sleep_time)
    except Exception as e:
        logging.error(f"Error polling SI: {e}")


if __name__ == '__main__':
    try:
        clear_screen()
        banner =(f"{bold}Hoppie/SayIntentions.AI ACARS Bridge {reset}v{version}{reset}\n")
        print(banner)


        # Get the configuration settings
        get_config()
        while not hoppie_logon or not sai_logon or not simbrief_id:
           set_configuration()
           get_config()

        clear_screen()
        print(banner)


        # Generate the ATSU Callsign
        atsu_callsign = generate_random_4_letter_string(sai_logon)
        atsu_string = f"{bold}{red}{atsu_callsign}{reset}"
        print(f"\n{bold}Use the following ATSU Callsign for all PDC & CPDLC requests: {atsu_string}\n")  
 
        logging.info(f"ATSU Callsign: { atsu_string}")

        # Get the SimBrief plan
        sb_plan = get_simbrief_plan(simbrief_id)
        sb_callsign = sb_plan["atc"]["callsign"]
        callsign_string = f"{bold}{green}{sb_callsign}{reset}"
   
        logging.info(f"Aircraft Callsign: {callsign_string} ")

        # Start the polling threads
        poll_hoppie_thread = threading.Thread(target=poll_hoppie)  
        poll_si_thread = threading.Thread(target=poll_si)   

        poll_hoppie_thread.start()
        poll_si_thread.start()
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

   