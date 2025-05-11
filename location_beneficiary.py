# # import streamlit as st

# # def location_beneficiary_tab(location_data=None):
# #     st.header("Location/Beneficiary Details")
# #     location_data = location_data or [None] * 8
# #     operational_area = st.radio("Operational Area", ["Yes", "No"], index=["Yes", "No"].index(location_data[1] or "Yes"))
# #     plan_campaign = st.selectbox("Plan/Campaign Name", ["SWACHHTA ACTION PLAN", "ANNUAL COMPONENT PLAN", "SPECIAL COMPONENT PLAN", "HAR GHAR TIRANGA", "OTHER"], 
# #                                  index=["SWACHHTA ACTION PLAN", "ANNUAL COMPONENT PLAN", "SPECIAL COMPONENT PLAN", "HAR GHAR TIRANGA", "OTHER"].index(location_data[2] or "SWACHHTA ACTION PLAN"))
# #     plan_campaign_other = st.text_input("Other Plan/Campaign Description", value=location_data[3] or "") if plan_campaign == "OTHER" else None
# #     activity = st.text_area("Activity under the Project", value=location_data[4] or "")
# #     all_india = st.radio("All India Implementation", ["Yes", "No"], index=["Yes", "No"].index(location_data[5] or "Yes"))
# #     districts_impacted = st.number_input("Number of Districts Impacted", min_value=1, max_value=10, value=int(location_data[6] or 1))
# #     pin_codes = location_data[7] or [""] * districts_impacted
# #     pin_codes = [st.text_input(f"PIN Code {i}", value=pin_codes[i-1] if i-1 < len(pin_codes) else "") for i in range(1, min(districts_impacted, 11) + 1)]

# #     return {
# #         "operational_area": operational_area,
# #         "plan_campaign": plan_campaign,
# #         "plan_campaign_other": plan_campaign_other,
# #         "activity": activity,
# #         "all_india": all_india,
# #         "districts_impacted": districts_impacted,
# #         "pin_codes": pin_codes
# #     }

# import streamlit as st

# def location_beneficiary_tab(location_data=None):
#     st.header("Location/Beneficiary Details")
    
#     # Initialize default dictionary
#     defaults = {
#         "operational_area": "Yes",
#         "plan_campaign": "SWACHHTA ACTION PLAN",
#         "plan_campaign_other": "",
#         "activity": "",
#         "all_india": "Yes",
#         "districts_impacted": 1,
#         "pin_codes": []
#     }
#     location_data = location_data or {}
#     for key, value in defaults.items():
#         location_data.setdefault(key, value)

#     # Operational Area
#     operational_area = st.radio(
#         "Operational Area *",
#         ["Yes", "No"],
#         index=["Yes", "No"].index(location_data["operational_area"])
#     )

#     # Plan/Campaign Name
#     plan_campaign_options = [
#         "SWACHHTA ACTION PLAN",
#         "ANNUAL COMPONENT PLAN",
#         "SPECIAL COMPONENT PLAN",
#         "HAR GHAR TIRANGA",
#         "OTHER"
#     ]
#     plan_campaign = st.selectbox(
#         "Plan/Campaign Name *",
#         plan_campaign_options,
#         index=plan_campaign_options.index(location_data["plan_campaign"])
#     )

#     # Plan Campaign Other
#     plan_campaign_other = st.text_input(
#         "Other Plan/Campaign Description",
#         value=location_data["plan_campaign_other"],
#         max_chars=100
#     ) if plan_campaign == "OTHER" else ""

#     # Activity under the Project
#     activity = st.text_area(
#         "Activity under the Project *",
#         value=location_data["activity"],
#         max_chars=500
#     )

#     # All India Implementation
#     all_india = st.radio(
#         "All India Implementation",
#         ["Yes", "No"],
#         index=["Yes", "No"].index(location_data["all_india"])
#     )

#     # Number of Districts Impacted
#     try:
#         districts_impacted = int(location_data["districts_impacted"] or 1)
#     except (ValueError, TypeError):
#         districts_impacted = 1
#     districts_impacted = st.number_input(
#         "Number of Districts Impacted *",
#         min_value=1,
#         max_value=10,
#         value=districts_impacted,
#         step=1
#     )

#     # PIN Codes
#     pin_codes = location_data["pin_codes"] or [""] * 10
#     pin_codes_inputs = [
#         st.text_input(
#             f"PIN Code {i}",
#             value=pin_codes[i-1] if i-1 < len(pin_codes) else "",
#             max_chars=6
#         ) for i in range(1, min(districts_impacted, 11) + 1)
#     ]
#     # Filter out empty PIN codes
#     pin_codes = [pin for pin in pin_codes_inputs if pin.strip()]

#     return {
#         "operational_area": operational_area,
#         "plan_campaign": plan_campaign,
#         "plan_campaign_other": plan_campaign_other,
#         "activity": activity,
#         "all_india": all_india,
#         "districts_impacted": districts_impacted,
#         "pin_codes": pin_codes
#     }


import streamlit as st
import re

def location_beneficiary_tab(location_data=None):
    st.header("Location/Beneficiary Details")
    
    # Initialize default dictionary
    defaults = {
        "operational_area": "Yes",
        "plan_campaign": "SWACHHTA ACTION PLAN",
        "plan_campaign_other": "",
        "activity": "",
        "all_india": "Yes",
        "districts_impacted": 1,
        "pin_codes": []
    }
    location_data = location_data or {}
    for key, value in defaults.items():
        location_data.setdefault(key, value)

    # Operational Area
    operational_area = st.radio(
        "Operational Area *",
        ["Yes", "No"],
        index=["Yes", "No"].index(location_data["operational_area"])
    )

    # Plan/Campaign Name
    plan_campaign_options = [
        "SWACHHTA ACTION PLAN",
        "ANNUAL COMPONENT PLAN",
        "SPECIAL COMPONENT PLAN",
        "HAR GHAR TIRANGA",
        "OTHER"
    ]
    plan_campaign = st.selectbox(
        "Plan/Campaign Name *",
        plan_campaign_options,
        index=plan_campaign_options.index(location_data["plan_campaign"])
    )

    # Plan Campaign Other
    plan_campaign_other = st.text_input(
        "Other Plan/Campaign Description",
        value=location_data["plan_campaign_other"],
        max_chars=100
    ) if plan_campaign == "OTHER" else ""

    # Activity under the Project
    activity = st.text_area(
        "Activity under the Project *",
        value=location_data["activity"],
        max_chars=500
    )
    if not activity.strip():
        st.warning("Activity under the Project is mandatory.")

    # All India Implementation
    all_india = st.radio(
        "All India Implementation",
        ["Yes", "No"],
        index=["Yes", "No"].index(location_data["all_india"])
    )

    # Number of Districts Impacted
    try:
        districts_impacted = int(location_data["districts_impacted"] or 1)
    except (ValueError, TypeError):
        districts_impacted = 1
    districts_impacted = st.number_input(
        "Number of Districts Impacted *",
        min_value=1,
        max_value=10,
        value=districts_impacted,
        step=1
    )

    # PIN Codes
    pin_codes = location_data["pin_codes"] or [""] * 10
    pin_codes_inputs = [
        st.text_input(
            f"PIN Code {i}",
            value=pin_codes[i-1] if i-1 < len(pin_codes) else "",
            max_chars=6
        ) for i in range(1, min(districts_impacted, 11) + 1)
    ]
    # Validate PIN codes
    for i, pin in enumerate(pin_codes_inputs, 1):
        if pin and not re.match(r"^[0-9]{6}$", pin):
            st.warning(f"PIN Code {i} must be a 6-digit number.")
    # Filter out empty PIN codes
    pin_codes = [pin for pin in pin_codes_inputs if pin.strip()]

    return {
        "operational_area": operational_area,
        "plan_campaign": plan_campaign,
        "plan_campaign_other": plan_campaign_other,
        "activity": activity,
        "all_india": all_india,
        "districts_impacted": districts_impacted,
        "pin_codes": pin_codes
    }