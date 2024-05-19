from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import subprocess
import os

class TelegramGroupLister(DiscoverableTransform):
    """
    Transform to list Telegram groups using a pre-existing configuration file.
    Filters groups based on a provided name phrase and returns matched groups.
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        group_filter = request.Value.strip().lower()  # Get the filter phrase from the Maltego request
        config_path = os.path.join(os.path.dirname(__file__), 'telegram.config')  # Path to the config file

        if not os.path.exists(config_path):
            response.addUIMessage("Configuration file not found.", messageType="PartialError")
            return

        # Connect and load groups before listing them
        cls.run_command(f"python3 -m TEx load_groups --config {config_path}", response)

        # List groups and capture the output
        stdout, stderr = cls.run_command(f"python3 -m TEx list_groups --config {config_path}", response, get_output=True)

        if stderr:
            response.addUIMessage("Error listing groups: " + stderr, messageType="PartialError")
        else:
            cls.parse_groups(stdout, group_filter, response)

    @staticmethod
    def run_command(command, response, get_output=False):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if get_output:
            return stdout, stderr
        else:
            if stderr:
                response.addUIMessage(stderr, messageType="PartialError")

    @staticmethod
    def parse_groups(stdout, group_filter, response):
        found = False
        for line in stdout.split('\n'):
            if line.strip() and "ID" not in line:  # To ignore the header line
                parts = line.split()
                group_id = parts[0]
                username = parts[1] if parts[1] != "None" else ""
                title = ' '.join(parts[2:])  # Join the rest which forms the title

                # Applying the filter
                if group_filter in title.lower():
                    found = True
                    entity = response.addEntity('maltego.Phrase', title)
                    entity.addProperty(fieldName="groupID", displayName="Group ID", value=group_id)
                    entity.addProperty(fieldName="username", displayName="Username", value=username)

        if not found:
            response.addUIMessage("No groups found matching the filter.", messageType="Inform")

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([TelegramGroupLister])
