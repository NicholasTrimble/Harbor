import datetime

# Define the exact core schema keys we expect to find inside each weather alert feature
REQUIRED_KEYS = ["id", "areaDesc", "event", "severity", "urgency"]

def validate_and_transform(raw_json_data):
    """
    Takes raw JSON dictionary from the NOAA API, checks for missing schema structures,
    and returns a clean, standard list of internal dictionaries ready to insert.
    """
    cleaned_records = []
    schema_errors = {"missing_fields": [], "malformed_records": 0}

    # Defensive check: Make sure the response contains the top-level "features" array
    if "features" not in raw_json_data:
        schema_errors["missing_fields"].append("features_root_array")
        return [], schema_errors

    # Process each weather alert item
    for item in raw_json_data["features"]:
        properties = item.get("properties", {})
        
        # SCHEMA DRIFT DETECTION
        # Check if any of our required fields have gone missing or changed names
        missing_in_this_item = [key for key in REQUIRED_KEYS if key not in properties]
        
        if missing_in_this_item:
            schema_errors["missing_fields"].extend(missing_in_this_item)
            schema_errors["malformed_records"] += 1
            continue  # Skip this specific broken record, keep moving

        # DATA TRANSFORMATION
        # Remap the messy third-party structure into a clean internal data block
        transformed_record = {
            "external_id": properties["id"],
            "region": properties["areaDesc"],
            "event_type": properties["event"],
            "severity": properties["severity"],
            "urgency": properties["urgency"],
            "ingested_at": datetime.datetime.now(datetime.timezone.utc)
        }
        cleaned_records.append(transformed_record)

    # Clean up duplicate tracking fields in errors list
    schema_errors["missing_fields"] = list(set(schema_errors["missing_fields"]))
    
    return cleaned_records, schema_errors