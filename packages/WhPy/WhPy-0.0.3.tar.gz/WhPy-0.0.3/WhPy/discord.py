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

    def message(self, content=None, username=None, avatar_url=None):
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

    def execute(self):
        """
        Executes the Discord Webhook
        Keyword Arguments:
        None
        """
        try:

            if self.content is None:

                raise TypeError("Missing required argument: 'content'")

        except AttributeError:

            raise TypeError("Missing required argument: 'content'")

        # Call Parameters
        url = f"{ discord_endpoint }/{ self.channel_id }/{ self.token }"
        header = {"Content-Type": "application/json"}

        json_data = {}

        json_data["content"] = self.content
        json_data["username"] = self.username
        json_data["avatar_url"] = self.avatar_url

        return requests.post(url, headers=header, json=json_data)
