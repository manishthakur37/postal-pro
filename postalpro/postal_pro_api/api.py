

import frappe
import requests





import frappe
import requests

@frappe.whitelist()
def get_circle_name_by_pincode(pincode):
    """
    Fetch circle name, taluk, and district name based on the provided postal code.
    
    Args:
        pincode (str): The postal code to look up.

    Returns:
        dict: A dictionary containing taluk, district name, and circle name.

    Raises:
        frappe.ValidationError: If no data is found or API request fails.
    """
    # Fetch settings for Postal Pro
    postal_pro_settings = frappe.get_cached_doc("Postal Pro Setting")
    api_url = postal_pro_settings.url
    api_key = postal_pro_settings.postal_pro_api_key

    # Set up parameters for the API request
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": "1",
        "filters[pincode]": pincode
    }

    try:
        # Make the API request
        response = requests.get(api_url, params=params)

        # Check for a successful response
        if response.status_code == 200:
            data = response.json()

            # Check if records are available
            if data.get("records"):
                record = data["records"][0]
                return {
                    "taluk": record.get("taluk", "Not available"),
                    "districtname": record.get("districtname", "Not available"),
                    "circlename": record.get("circlename", "Not available"),
                }
            else:
                frappe.throw("No data found for the provided postal code.")
        else:
            frappe.throw(f"API request failed with status code {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        frappe.throw(f"An error occurred while making the API request: {str(e)}")
    except Exception as ex:
        frappe.throw(f"An unexpected error occurred: {str(ex)}")
