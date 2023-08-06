# python-eloqua-wrapper

This outlines the current behavior and use cases of the API via an example.

Currently, the main functionality is centered around creating, updating, or deleting Custom Data Object records in Eloqua.

# Example Outline

Let's say we have a CDO with ID# 12345, and a record with these field values:

Record ID#369789
- business_email: bob@bobbyworld.com 
- first_last_name: bob_wilbert
- zip_code: 32123
- job_title: Nannygoat Herder

We would like to update him in our CDO with the following:
- zip_code: 22667
- job_title: Alligator Wrangler

How do we upload changes via our lovely api wrapper?

## Step 1: What you need to upload data to Eloqua

To push a given record with the basic CdoRecord class, you will need:

- the CDO ID
- the CDO record ID
- A dictionary of the fieldName:value pairs you want to upload/update
- A dictionary of the fieldName:fieldID pairs to map your fieldsNames
    
## Step 2: bare bones initialization

```
from eloqua_api_wrapper.cdo_record import CdoRecord
from eloqua_api_wrapper.eloqua_session import EloquaSession
from os import environ

session = EloquaSession(company=environ["ELOQUA_COMPANY"], 
                        username=environ["ELOQUA_USER"], 
                        password=environ["ELOQUA_PASSWORD"])

cdo_record = CdoRecord(session=session)
```

That's it, you now have a local object!

## Step 3: Updating your record

There is a method called `update_cdo_record`, which can be used as follows:

```
cdo_record.update_cdo_record(
    cdo_id=12345, 
    record_id=369789, 
    cdo_field_to_field_id_map={
        'zip_code': 11221,
        'job_title': 11232}, 
    record_fields_and_values_dict={
        'zip_code': '22667',
        'job_title': 'Alligator Wrangler'})
```
Simply execute this and you will receive the response object if it was successful, else it will raise an exception.

To be more explicit about update behavior:

- If a previous value for that field/column already existed: it gets overwritten.

- If you don't provide a field/column name, it won't alter that column.
