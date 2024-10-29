import requests
import re
import logging
import random
import time
import configparser
from hash_userid import *
import threading
from colors import *

config = configparser.ConfigParser()
# Read the INI file


# Configuration attributes
try: 
    config.read('bridge.ini')
    hoppie_logon = config.get('Settings', 'hoppie_logon',fallback="")
    hoppie_url = config.get('Settings', 'hoppie_url', fallback='www.hoppie.nl')
    sai_logon = config.get('Settings', 'sayintentions_api_key',fallback="")
    sai_url = config.get('Settings', 'sayintentions_url', fallback='acars.sayintentions.ai')
    simbrief_id = config.get('Settings', 'simbrief_id',fallback="")
except:
    logging.error("Error reading configuration")
    exit()



if not hoppie_logon or not sai_logon or not simbrief_id:
    logging.error("Missing configuration")
    exit()

atsu_callsign = generate_random_4_letter_string(sai_logon)
callsigns_dict = {}

# Set up logging
logging.basicConfig(
    #filename='acars_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)




def get_simbrief_plan(simbrief_id):
    logging.info(f"Fetch plan: {simbrief_id}")
    url = f"https://www.simbrief.com/api/xml.fetcher.php?json=1&userid={simbrief_id}" 
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()  # Corrected method call
        logging.info(f"Received SB Plan:")
        return json_data 
    except requests.exceptions.RequestException as e:
        logging.error(f"Error polling URL: {e}")
        return False






def poll_backend(source_url, source_logon, source_callsign, target_url, target_logon):
    # Step 1: Poll the URL
    poll_url = f"http://{source_url}/acars/system/connect.html?logon={source_logon}&to=SERVER&type=poll&from={source_callsign}&packet=Nought"
    #logging.info(f"Polling URL: {poll_url}")

    try:
        response = requests.get(poll_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_text = response.text
        #logging.info(f"Received response: {response_text}")
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
            #logging.info(f"Parsed message: {message}")
        #if len(messages):
        #    logging.info(f"Number of messages for {source_callsign}: {len(messages)} on {source_url}")
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
            #logging.info(f"Sent GET request to: {get_request_url}")
            #logging.info(f"Response: {sai_response.status_code} - {sai_response.text}")
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

             sleep_time = int(random.uniform(60, 75))
             #logging.info(f"Hoppie Poll Sleeping for {sleep_time:.2f} seconds")
             time.sleep(sleep_time)
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


            sleep_time = int(random.uniform(10, 15))
            #logging.info(f"SI Poll Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
    except Exception as e:
        logging.error(f"Error polling SI: {e}")


if __name__ == '__main__':
    try:
        atsu_string = f"{bold}{red}{atsu_callsign}{reset}"
        print(f"\n{bold}Use the following ATSU Callsign for all PDC & CPDLC requests: {atsu_string}\n")  
 
        logging.info(f"ATSU Callsign: { atsu_string}")
        sb_plan = get_simbrief_plan(simbrief_id)
        sb_callsign = sb_plan["atc"]["callsign"]
        callsign_string = f"{bold}{green}{sb_callsign}{reset}"
   
        logging.info(f"Aircraft Callsign: {callsign_string} ")
        poll_hoppie_thread = threading.Thread(target=poll_hoppie)  
        poll_si_thread = threading.Thread(target=poll_si)   

        poll_hoppie_thread.start()
        poll_si_thread.start()
    except Exception as e:
        logging.error(f"Error starting: {e}")

    
   

