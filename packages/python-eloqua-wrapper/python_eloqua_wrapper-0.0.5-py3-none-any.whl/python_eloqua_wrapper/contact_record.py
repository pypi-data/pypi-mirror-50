from urllib.parse import quote_plus


class Contact:
    """
    Handles eloqua contacts

    Abstracts API operations and handling data about contacts
    """

    pass

    def __init__(self, email, session, eloqua_id=None, data=None):
        self.email = email
        self.session = session
        self.eloqua_id = eloqua_id
        self.data = data

        self.sync_record()

    def to_http_post(self):
        """
        Formats contact data as a POST to the new contact API endpoint in Eloqua

        Abstracts the POST data formatting for Unit testing purposes
        :return: (dict) POST body data
        """
        return {"emailAddress": self.email}

    def sync_from_eloqua(self, response_data):
        """
        Updates contact values based on a created-contact response from Eloqua

        :param response_data: (requests.Response) HTTP response from Eloqua API
        :return: None
        """
        self.data = response_data
        self.eloqua_id = int(self.data["id"])

    def delete_from_eloqua(self):
        """
        Deletes this contact from Eloqua using the Singleton REST API
        :return: None
        """
        response = self.session.delete(
            url="/api/REST/1.0/data/contact/{}".format(self.eloqua_id)
        )
        response.raise_for_status()

    def create_contact(self):
        """
        Create or sync this contact with the Eloqua version
        """
        response = self.session.post(
            url="/api/REST/1.0/data/contact", json=self.to_http_post()
        )
        response.raise_for_status()

        self.sync_from_eloqua(response.json())

    def sync_record(self):
        """
        Sync this record object with the respective Eloqua CDO record via email
        """
        url = "/api/REST/1.0/data/contacts"
        custom_params = "?search=emailAddress='{}'&count=1".format(
            quote_plus(self.email)
        )
        response = self.session.get(url="".join([url, custom_params]))
        response.raise_for_status()

        data = response.json()["elements"]
        if data:
            self.sync_from_eloqua(data[0])
        else:
            self.create_contact()
