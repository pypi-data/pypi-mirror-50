
class CdoInfo:

    def __init__(self,
                 session,
                 cdo=None):
        """
        A class for querying Eloqua for CDO metadata (such as field names and field ID's).
        :param session: An Eloqua Session Object.
        :type session: EloquaSession
        :param cdo: The name or ID of the desired CDO you wish to use.
        :type cdo: string
        """
        self.id = None
        self.name = None
        self.field_id_map = None
        self.reference_fields = None
        self.session = session

        if cdo:
            try:
                self.id = int(cdo)
                self.get_data_by_id()
            except ValueError:
                self.name = cdo
                self.get_data_by_name()

    def set_reference_fields(self, data):
        """
        :param data: eloqua HTTP request.Response json object
        :return: valid reference name:id pairs
        :rtype: dict
        """
        refs = {
            'uniqueCode': data.get('uniqueCodeFieldId'),
            'name': data.get('displayNameFieldId')}
        return {k: v for k, v in refs.items() if v}

    def set_local_data(self, data):
        """
        Sets all the local attributes on this object based on HTTP response from Eloqua regarding CDO metadata.
        :param data: eloqua HTTP request.Response json object
        """
        self.id = data['id']
        self.name = data.get('name')
        self.field_id_map = {field["name"]: field["id"] for field in data['fields']}
        self.reference_fields = self.set_reference_fields(data)

    def get_data_by_id(self):
        """
        Makes an HTTP request to Eloqua regarding CDO metadata via the CDO ID.
        Later sets the various response values to attributes on this class.
        """
        response = self.session.get(url=f"/api/REST/2.0/assets/customObjects/{self.id}?depth=complete")
        response.raise_for_status()
        data = response.json()
        if data:
            self.set_local_data(data)
        else:
            raise ValueError(f"CustomObject ID#{self.id} does not seem to exist")

    def get_data_by_name(self):
        """
        Makes an HTTP request to Eloqua regarding CDO metadata via the name of the CDO.
        Later sets the various response values to attributes on this class."""
        url = "/api/REST/2.0/assets/customObjects"
        custom_params = f"?search=name='{self.name}'&count=1&depth=complete"
        response = self.session.get(url="".join([url, custom_params]))
        response.raise_for_status()
        data = response.json()["elements"][0]
        self.set_local_data(data)

    def get_cdo_fields(self, cdo_id):
        """
        Separate method for retrieving CDO fields when not initializing the class with a cdo name/id.
        :param cdo_id: unique ID of the desired CDO
        :return: cdo field_name:id pairs
        :rtype: dict
        """
        self.id = cdo_id
        self.set_local_data()
        return self.field_id_map

