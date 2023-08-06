from urllib.parse import quote_plus


class CdoRecord:
    """
    Allows bare-bones interaction with CDOs based on IDs; primarily creating, updating, or deleting records.
    Has some helper methods to aid with finding CDO record ID's if you don't know what they are.
    Must be initialized with an EloquaSession class instance.
    A good rule of thumb is that if 'ID' is NOT specified for a parameter, then assume it's referencing a name/string.
    """
    def __init__(self, session):
        self.session = session

    def get_record_id(self, cdo_id, record_unique_field_value, cdo_unique_field='UniqueCode'):
        """
        Allows you to find a record's ID for a given CDO if you know a field that has unique values in it
        (defaults to the 'UniqueCode' reference field of the CDO).
        This will throw an exception if it encounters >1 records with the provided field/value.
        :param cdo_id: a cdo's unique ID number
        :type cdo_id: int
        :param record_unique_field_value: the unique record field value to search for.
        :type record_unique_field_value: str
        :param cdo_unique_field: the name of the field to search for the given record_unique_field_value
        (default is 'UniqueCode').
        :type cdo_unique_field: str
        :return: a record's unique ID number for the given CDO.
        :rtype: string
        """
        url_base = f"/api/REST/2.0/data/customObject/{cdo_id}/instances"
        custom_params = f"?search={cdo_unique_field}='{quote_plus(record_unique_field_value)}'&count=2&depth=complete"
        response = self.session.get(url=''.join([url_base, custom_params]))
        response.raise_for_status()
        data = response.json()['elements']
        if len(data) > 1:
            raise IndexError("Searching for the record by unique name yielded >1 record. Be sure you have:"
                             "\nA: the correct unique value for your record,"
                             "\nB: the correct unique field that the aforementioned unique value belongs to"
                             "\n If both appear valid, then that field is not actually unique, and thus cannot be used!")
        return data[0]['id']

    def get_record_field_ids_and_values(self, cdo_id, record_id, drop_empty=True):
        """
        Gets all the fields and values for a given record id.
        Defaults to dropping empty fields via the parameter 'drop_empty=True'.
        :param cdo_id: a cdo's unique ID number
        :type cdo_id: int
        :param record_id: a record's unique ID number for the given CDO.
        :type record_id: int
        :param drop_empty: Whether to keep empty fields or not
        :type drop_empty: bool
        :return: record field_id:field_value pairs
        :rtype: dict
        """
        response = self.session.get(url=f"/api/REST/2.0/data/customObject/{cdo_id}/instance/{record_id}")
        response.raise_for_status()
        data = response.json()
        if data:
            field_values = data['fieldValues']
            if drop_empty:
                return {field['id']: field['value'] for field in field_values if field['value']}
            return {field['id']: field['value'] for field in field_values}
        else:
            raise ValueError(f"CustomObject ID#{cdo_id} does not seem to exist")

    def map_record_field_ids_to_field_names(self, record_field_values, cdo_field_to_field_id_map):
        """
        Allows you to map the field_id:field_value results of 'get_record_field_ids_and_values' to
        field_name:field_values pairs instead.
        :param record_field_values: field_id:field_value pairs
        :type record_field_values: dict
        :param cdo_field_to_field_id_map: field_name:field_id pairs
        :type cdo_field_to_field_id_map: dict
        :return: record field_name:field_value pairs
        :rtype: dict
        """
        inverted_cdo_field_dict = {value: key for key, value in cdo_field_to_field_id_map.items()}
        return {inverted_cdo_field_dict[field_id]: value for field_id, value in record_field_values.items()}

    def get_record_unique_reference_field_and_value(self, record_field_values, cdo_field_to_field_id_map,
                                                    cdo_reference_field_map, unique_field='UniqueCode'):
        """
        Generally limited use cases and recommended for advanced users only.
        If the provided 'unique_field' field is set (default is'UniqueCode') in the CDO, this will find the field name
        its respective value for the provided record_field_values.
        This generally requires a 'cdo_reference_field_map', obtainable via the CdoInfo object.
        Will throw an exception if the 'unique_field' is not actually unique.
        :param record_field_values: field_id:field_value pairs
        :type record_field_values: dict
        :param cdo_field_to_field_id_map: CDO field_name:field_id pairs
        :type cdo_field_to_field_id_map: dict
        :param cdo_reference_field_map: CDO internal_reference_field_name:field_id pairs
        :type cdo_reference_field_map: dict
        :param unique_field: reference field to check for; defaults to 'UniqueCode'
        :type unique_field: str
        :return:
        """
        if unique_field not in cdo_reference_field_map:
            raise ValueError("The field you are attempting to search on does not appear to be set."
                             "\nThis could be because it's either a) not set, or b) not unique.")
        field_id = cdo_reference_field_map[unique_field]
        return {cdo_field_to_field_id_map[field_id]: record_field_values[field_id]}

    def format_core_record_data_for_pushing(self, cdo_field_to_field_id_map, record_fields_and_values_dict):
        """
        Does the bare-bones data formatting necessary to push via Eloqua's REST API.
        :param cdo_field_to_field_id_map: cdo field_name:field_id pairs
        :type cdo_field_to_field_id_map: dict
        :param record_fields_and_values_dict: record field_name:field_value pairs
        :type record_fields_and_values_dict: dict
        :return: Eloqua API-formatted data
        :rtype: dict
        """
        return {"type": "CustomObjectData",
                "fieldValues":[{
                    'id': cdo_field_to_field_id_map[field],
                    'value': value,
                    'type': 'CustomObjectField'}
                    for field, value in record_fields_and_values_dict.items()]}

    def create_cdo_record(self, cdo_id, cdo_field_to_field_id_map, cdo_unique_field, record_unique_field_value,
                          record_fields_and_values_dict):
        """
        Create a new record in the given CDO. Raises exception if not a 200 HTTP response.
        :param cdo_id: a cdo's unique ID number
        :type cdo_id: int
        :param cdo_field_to_field_id_map: cdo field_name:field_id pairs
        :type cdo_field_to_field_id_map: dict
        :param cdo_unique_field: the name of the field to search for the given record_unique_field_value.
        :type cdo_unique_field: str
        :param record_unique_field_value: the unique record field value to search for.
        :type record_unique_field_value: str
        :param record_fields_and_values_dict: desired record fields via field_name:field_value pairs
        :type record_fields_and_values_dict: dict
        :return: request HTTP response
        :rtype: requests.Response
        """
        response = self.session.post(
            url=f"/api/REST/2.0/data/customObject/{cdo_id}/instance",
            json={**self.format_core_record_data_for_pushing(cdo_field_to_field_id_map, record_fields_and_values_dict),
                  cdo_unique_field: record_unique_field_value})
        response.raise_for_status()
        return response

    def update_cdo_record(self, cdo_id, record_id, cdo_field_to_field_id_map, record_fields_and_values_dict):
        """
        Update a record in the given CDO. Raises exception if not a 200 HTTP response.
        :param cdo_id: a cdo's unique ID number
        :type cdo_id: int
        :param record_id: a record's unique ID number for the given CDO.
        :type record_id: int
        :param cdo_field_to_field_id_map: cdo field_name:field_id pairs
        :type cdo_field_to_field_id_map: dict
        :param record_fields_and_values_dict: desired record fields via field_name:field_value pairs
        :type record_fields_and_values_dict: dict
        :return: request HTTP response
        :rtype: requests.Response
        """
        response = self.session.put(
            url=f"/api/REST/2.0/data/customObject/{cdo_id}/instance/{record_id}",
            json=self.format_core_record_data_for_pushing(cdo_field_to_field_id_map, record_fields_and_values_dict))
        response.raise_for_status()
        return response

    def delete_cdo_record(self, cdo_id, record_id):
        """
        Delete a record in the given CDO. Raises exception if not a 200 HTTP response.
        :param cdo_id: a CDO's unique ID number
        :type cdo_id: int
        :param record_id: a record's unique ID number for the given CDO.
        :type record_id: int
        :return: request HTTP response
        :rtype: requests.Response
        """
        response = self.session.delete(
            url=f"/api/REST/2.0/data/customObject/{cdo_id}/instance/{record_id}")
        response.raise_for_status()
        return response
