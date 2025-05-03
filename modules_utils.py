import json
from requests import get
from csv import reader, writer, DictReader, DictWriter # Import DictReader/Writer
from datetime import datetime
import os # Import os for path checking

class Modules:
    """
    Modules class, this class holds all the non-main functions the program needs for better functionality.
    """

    Format = {
        'GREEN':'\033[92m',
        'YELLOW':'\033[93m',
        'RED':'\033[91m',
        'END':'\033[0m'
    }

    @staticmethod
    def log(index: int, data: str) -> None:
        """
            Logging system. Not necessary, but good and useful.
        """
        log_prefix = f'[{str(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))}]'
        log_message = f'{log_prefix} - {data}'
        # managing different inputs to output them in different colors
        if(index == -1): # neutral input, no color
            print(log_message)
        elif(index == 0): # success input, green
            print(f'{Modules.Format["GREEN"]}{log_message}{Modules.Format["END"]}')
        elif(index == 1): # error input, yellow
            print(f'{Modules.Format["YELLOW"]}{log_message}{Modules.Format["END"]}')
        elif(index == 2): # fatal error input, red
            print(f'{Modules.Format["RED"]}{log_message}{Modules.Format["END"]}')

        try:
            # Ensure logs directory exists
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            with open(os.path.join(log_dir, 'log'), 'a', encoding='utf-8') as log_file:
                log_file.write(f'{log_message}\n')
        except IOError as e:
            print(f'{log_prefix} - [Modules.log] ERROR: Could not write to log file: {e}')


    # --- Configuration Loading Methods --- (Keep existing ones)
    @staticmethod
    def getAccounts() -> list:
        # ... (implementation)
        try:
            with open('rdt/accounts.json','r') as accounts:
                return json.load(accounts)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rdt/accounts.json not found.")
             return []
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rdt/accounts.json.")
             return []

    @staticmethod
    def getProxies() -> dict: # Changed return type to dict based on usage
        # ... (implementation)
        try:
            with open('rsrc/proxies.json','r') as proxies:
                return json.load(proxies)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rsrc/proxies.json not found.")
             return {}
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/proxies.json.")
             return {}

    @staticmethod
    def getPaths() -> dict:
        # ... (implementation)
        try:
            with open('rsrc/paths.json','r') as config:
                return json.load(config)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rsrc/paths.json not found.")
             return {}
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/paths.json.")
             return {}

    @staticmethod
    def getConfig() -> dict:
        # ... (implementation)
        try:
            with open('rsrc/config.json','r') as config:
                return json.load(config)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rsrc/config.json not found.")
             return {}
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/config.json.")
             return {}

    @staticmethod
    def getLocators() -> dict:
        # ... (implementation)
        try:
            with open('rsrc/locators.json','r') as locators:
                return json.load(locators)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rsrc/locators.json not found.")
             return {}
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/locators.json.")
             return {}

    @staticmethod
    def getLinks() -> dict:
        # ... (implementation)
        try:
            with open('rsrc/links.json','r') as links:
                return json.load(links)
        except FileNotFoundError:
             Modules.log(2, "[Modules] ERROR: rsrc/links.json not found.")
             return {}
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/links.json.")
             return {}

    @staticmethod
    def getUserAgents() -> list:
         # ... (implementation)
        try:
            with open('rsrc/user_agents.json','r') as user_agents:
                return json.load(user_agents)
        except FileNotFoundError:
             Modules.log(1, "[Modules] WARNING: rsrc/user_agents.json not found. User agent list will be empty.")
             return []
        except json.JSONDecodeError:
             Modules.log(2, "[Modules] ERROR: Could not decode rsrc/user_agents.json.")
             return []

    # --- CSV Helper Methods --- (Add new ones here)

    @staticmethod
    def load_sent_log(filepath: str) -> set:
        """Loads already sent username/post_url pairs from sent_log.csv into a set for quick lookup."""
        sent_items = set()
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None) # Skip header row if present
                if header and len(header) >= 2:
                     Modules.log(0, f"[Modules] Reading sent log with headers: {header}")
                else: # Assume no header or missing columns
                    csvfile.seek(0) # Rewind if no valid header was read

                for row in reader:
                    if len(row) >= 2: # Ensure row has at least username and url
                        # Create a tuple (username, post_url) for the set
                        sent_items.add((str(row[0]).strip(), str(row[1]).strip()))
                    elif row: # Log if row is not empty but has too few columns
                         Modules.log(1, f"[Modules] Skipping malformed row in {filepath}: {row}")
        except FileNotFoundError:
            Modules.log(1, f"[Modules] Sent log file '{filepath}' not found. Assuming no items sent yet.")
        except Exception as e:
            Modules.log(2, f"[Modules] Error loading sent log from '{filepath}': {e}")
        return sent_items

    @staticmethod
    def append_to_csv(filepath: str, data_row_list: list, fieldnames: list):
        """Appends a row (list) to a CSV file. Creates file/header if it doesn't exist."""
        file_exists = os.path.isfile(filepath)
        try:
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists or os.path.getsize(filepath) == 0:
                    Modules.log(0, f"[Modules] Creating or writing header to {filepath}: {fieldnames}")
                    writer.writerow(fieldnames) # Write header if new file or empty
                writer.writerow(data_row_list)
        except IOError as e:
            Modules.log(2, f"[Modules] Error appending to CSV file '{filepath}': {e}")
        except Exception as e:
             Modules.log(2, f"[Modules] Unexpected error appending to CSV '{filepath}': {e}")

    @staticmethod
    def write_dm_queue(filepath: str, tasks_list_of_dicts: list):
        """Writes a list of dictionaries to the DM queue CSV, overwriting the file."""
        if not tasks_list_of_dicts:
            Modules.log(1, "[Modules] DM queue task list is empty. Not writing file.")
            # Optionally delete the file if it exists?
            # if os.path.exists(filepath): os.remove(filepath)
            return

        fieldnames = tasks_list_of_dicts[0].keys()
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(tasks_list_of_dicts)
            Modules.log(0, f"[Modules] Successfully wrote {len(tasks_list_of_dicts)} tasks to DM queue file '{filepath}'.")
        except IOError as e:
            Modules.log(2, f"[Modules] Error writing DM queue file '{filepath}': {e}")
        except Exception as e:
             Modules.log(2, f"[Modules] Unexpected error writing DM queue '{filepath}': {e}")


    @staticmethod
    def read_dm_queue(filepath: str) -> list:
        """Reads the DM queue CSV using DictReader, returns a list of task dictionaries."""
        tasks = []
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = DictReader(csvfile)
                if not reader.fieldnames:
                     Modules.log(1, f"[Modules] Warning: DM queue file '{filepath}' is empty or missing headers.")
                     return []
                Modules.log(0, f"[Modules] Reading DM queue with headers: {reader.fieldnames}")
                for row in reader:
                    tasks.append(dict(row)) # Convert OrderedDict to dict if necessary
        except FileNotFoundError:
            Modules.log(1, f"[Modules] DM queue file '{filepath}' not found. Returning empty queue.")
        except Exception as e:
            Modules.log(2, f"[Modules] Error reading DM queue from '{filepath}': {e}")
        return tasks


    # --- Other Helper Methods --- (Keep existing ones like manageProxyExtension if still needed)
    @staticmethod
    def manageProxyExtension(index: int, proxy_backend_path: str, proxy: str) -> None:
        """
            this function is responsible for adding and removing proxy from rsrc/extensions/proxy
            this is a really important function that would enable the software to rotate between proxies
        """
        # ... (implementation - ensure paths are correct)
        try:
            if(index == 0): # removing proxy - placeholder logic
                Modules.log(0, f'[Modules] Simulating removal for proxy {proxy}')
                pass
            elif(index == 1): # adding proxy - placeholder logic
                Modules.log(0, f'[Modules] Simulating setup for proxy {proxy}')
                pass
                # ... (Original file read/write logic would go here)
        except Exception as e:
             Modules.log(2, f'[Modules] - Fatal error while trying to setup Proxy extension: {e}')

    # Deprecated methods (Remove if no longer used)
    # @staticmethod
    # def dbToList(database: str, list_usernames: list) -> None: ...
    # @staticmethod
    # def writeToCSV(database: str, data: list) -> None: ...
    # @staticmethod
    # def loadSentUsernames(database: str) -> set: ... # Replaced by load_sent_log

    # @staticmethod
    # def getJS(path) -> str: ... # Keep if used 