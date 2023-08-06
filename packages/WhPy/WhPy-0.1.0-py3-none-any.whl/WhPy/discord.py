import requests


class Webhook:
    """
    Establishes communication with Discord Webhooks
    """
    global discord_endpoint
    discord_endpoint = "https://discordapp.com/api/webhooks"

    def __init__(self, url=None, channel_id=None, token=None):
        """
        Initializes discord class
        Keyword Arguments:
        url -- string -- Discord Webhook URL
        channel_id -- string -- Discord Channel ID
        token -- string -- Discord Webhook Token
        """
        # Sets embeds to use with embeds() call
        self.embeds = []

        # Ensures variables are not None
        if not url and not all([channel_id, token]):

            raise TypeError(
                "Missing required arguments: 'url' or 'channel_id' & 'token'"
            )

        # Use channel_id and token over URL
        if all([channel_id, token]):

            url = None

            self.channel_id = str(channel_id)
            self.token = str(token)

        # Use URL if populated
        if url is not None:

            self.channel_id = url.split("/")[5]
            self.token = url.split("/")[6]

        # Validates Webhook Authorization
        response = requests.get(
            f"{ discord_endpoint }/{ self.channel_id }/{ self.token }"
        )

        if response.status_code != 200:

            message = response.json()["message"]

            raise ValueError(f"Webhook authorization error: { message }")

    def message(self, content=None, username=None, avatar_url=None, tts=False):
        """
        Generates Message JSON
        Keyword Arguments:
        content -- string -- Text to be sent as the message
        username -- string -- The username associated with Discord message
        avatar_url -- string -- URL for the avatar displayed with the message
        """
        self.content = None if content is None else str(content)
        self.username = None if username is None else str(username)
        self.avatar_url = None if avatar_url is None else str(avatar_url)
        self.tts = True if tts is True else False

    def embed(self, title=None, description=None, url=None, color=None):
        """
        Adds a Discord Embed object to the message
        Keyword Arguments:
        title -- string -- Text to be sent as embed title
        description -- string -- text to be sent and embed description
        url -- string -- URL the embed redirects too
        color -- hex -- Hex code of color to be used for embed
        """
        json = {}

        json["title"] = None if title is None else str(title)
        json["description"] = None if description is None else str(description)
        json["url"] = None if url is None else str(url)
        json["color"] = None if color is None else int(color, 16)

        self.embeds.append(json)

    def execute(self, wait=False):
        """
        Executes the Discord Webhook
        Keyword Arguments:
        wait -- boolean -- True returns json verifying message
        """
        # Call Parameters
        url = f"{ discord_endpoint }/{ self.channel_id }/{ self.token }"
        header = {"Content-Type": "application/json"}

        json_data = {}

        # Checks to see if message() has been called
        try:

            json_data["content"] = self.content
            json_data["username"] = self.username
            json_data["avatar_url"] = self.avatar_url
            json_data["tts"] = self.tts

        except AttributeError:

            self.message()

        # If self.content and self.embeds not set
        if all((self.content is None, len(self.embeds) == 0)):

            raise TypeError(
                "Missing required arguments: 'content' or 'embeds'"
            )

        if len(self.embeds) > 0:

            json_data["embeds"] = self.embeds

        url = f"{ url }?wait=true" if wait is True else url

        return requests.post(url, headers=header, json=json_data)

    def clear(self):
        """
        Keeps the Webhook initialized but clears all variables
        Keyword Arguments:
        None
        """
        # Resets self.embends
        self.embeds = []

        # Sets message to None
        self.message()
