# # import streamlit as st

# # def agency_details_tab(agency_data=None):
# #     st.header("Agency Details")
# #     agency_data = agency_data or [None] * 12
# #     # vendor_no = st.text_input("Vendor No.", value=agency_data[1] or "", max_chars=10)
# #     vendor_no = st.text_input(
# #         "Vendor No.",
# #         value=agency_data.get("vendor_no", "") if isinstance(agency_data, dict) else "",
# #         max_chars=10
# #     )

# #     csr1_reg_no = st.text_input("CSR-1 Registration No.", value=agency_data[2] or "", max_chars=25)
# #     agency_type = st.selectbox("Agency Type", ["Registered Society", "Section 8 Company", "Trust"], index=["Registered Society", "Section 8 Company", "Trust"].index(agency_data[3] or "Registered Society"))
# #     pan_no = st.text_input("PAN No.", value=agency_data[4] or "", max_chars=10)
# #     gstn_no = st.text_input("GSTN No.", value=agency_data[5] or "", max_chars=18)
# #     reg_active = st.radio("Registration Active", ["Yes", "No"], index=["Yes", "No"].index(agency_data[6] or "Yes"))
# #     accounts_audited = st.radio("Accounts Audited", ["Yes", "No"], index=["Yes", "No"].index(agency_data[7] or "Yes"))
# #     bye_laws = st.radio("Bye Laws Cover Proposed Activity", ["Yes", "No"], index=["Yes", "No"].index(agency_data[8] or "Yes"))
# #     admin_cost = st.number_input("Administrative Cost", value=float(agency_data[9] or 0))
# #     gst_amount = st.number_input("GST Amount", value=float(agency_data[10] or 0))
# #     total_cost = st.number_input("Total Cost", value=float(admin_cost + gst_amount), disabled=True)

# #     return {
# #         "vendor_no": vendor_no,
# #         "csr1_reg_no": csr1_reg_no,
# #         "agency_type": agency_type,
# #         "pan_no": pan_no,
# #         "gstn_no": gstn_no,
# #         "reg_active": reg_active,
# #         "accounts_audited": accounts_audited,
# #         "bye_laws": bye_laws,
# #         "admin_cost": admin_cost,
# #         "gst_amount": gst_amount,
# #         "total_cost": total_cost
# #     }



# import streamlit as st

# def agency_details_tab(agency_data=None):
#     st.header("Agency Details")

#     # Fallback to default empty dict
#     if not isinstance(agency_data, dict):
#         agency_data = {}

#     vendor_no = st.text_input(
#         "Vendor No.",
#         value=agency_data.get("vendor_no", ""),
#         max_chars=10
#     )

#     csr1_reg_no = st.text_input(
#         "CSR-1 Registration No.",
#         value=agency_data.get("csr1_reg_no", ""),
#         max_chars=25
#     )

#     agency_type = st.selectbox(
#         "Agency Type",
#         ["Registered Society", "Section 8 Company", "Trust"],
#         index=["Registered Society", "Section 8 Company", "Trust"].index(
#             agency_data.get("agency_type", "Registered Society")
#         )
#     )

#     pan_no = st.text_input(
#         "PAN No.",
#         value=agency_data.get("pan_no", ""),
#         max_chars=10
#     )

#     gstn_no = st.text_input(
#         "GSTN No.",
#         value=agency_data.get("gstn_no", ""),
#         max_chars=18
#     )

#     reg_active = st.radio(
#         "Registration Active",
#         ["Yes", "No"],
#         index=["Yes", "No"].index(agency_data.get("reg_active", "Yes"))
#     )

#     accounts_audited = st.radio(
#         "Accounts Audited",
#         ["Yes", "No"],
#         index=["Yes", "No"].index(agency_data.get("accounts_audited", "Yes"))
#     )

#     bye_laws = st.radio(
#         "Bye Laws Cover Proposed Activity",
#         ["Yes", "No"],
#         index=["Yes", "No"].index(agency_data.get("bye_laws", "Yes"))
#     )

#     admin_cost = st.number_input(
#         "Administrative Cost",
#         value=float(agency_data.get("admin_cost", 0))
#     )

#     gst_amount = st.number_input(
#         "GST Amount",
#         value=float(agency_data.get("gst_amount", 0))
#     )

#     total_cost = st.number_input(
#         "Total Cost",
#         value=float(admin_cost + gst_amount),
#         disabled=True
#     )

#     return {
#         "vendor_no": vendor_no,
#         "csr1_reg_no": csr1_reg_no,
#         "agency_type": agency_type,
#         "pan_no": pan_no,
#         "gstn_no": gstn_no,
#         "reg_active": reg_active,
#         "accounts_audited": accounts_audited,
#         "bye_laws": bye_laws,
#         "admin_cost": admin_cost,
#         "gst_amount": gst_amount,
#         "total_cost": total_cost
#     }


import streamlit as st
import re

def agency_details_tab(agency_data=None):
    st.header("Agency Details")

    # Initialize default dictionary
    defaults = {
        "vendor_no": "",
        "csr1_reg_no": "",
        "agency_type": "Registered Society",
        "pan_no": "",
        "gstn_no": "",
        "reg_active": "Yes",
        "accounts_audited": "Yes",
        "bye_laws": "Yes",
        "admin_cost": 0.0,
        "gst_amount": 0.0,
        "total_cost": 0.0
    }
    agency_data = agency_data or {}
    for key, value in defaults.items():
        agency_data.setdefault(key, value)

    # Vendor No
    vendor_no = st.text_input(
        "Vendor No. *",
        value=agency_data["vendor_no"],
        max_chars=10
    )
    if vendor_no and not re.match(r"^[A-Za-z0-9]{1,10}$", vendor_no):
        st.warning("Vendor No. must be alphanumeric and up to 10 characters.")

    # CSR-1 Registration No
    csr1_reg_no = st.text_input(
        "CSR-1 Registration No. *",
        value=agency_data["csr1_reg_no"],
        max_chars=25
    )

    # Agency Type
    agency_type = st.selectbox(
        "Agency Type *",
        ["Registered Society", "Section 8 Company", "Trust"],
        index=["Registered Society", "Section 8 Company", "Trust"].index(agency_data["agency_type"])
    )

    # PAN No
    pan_no = st.text_input(
        "PAN No.",
        value=agency_data["pan_no"],
        max_chars=10
    )
    if pan_no and not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan_no):
        st.warning("PAN No. must follow the format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F).")

    # GSTN No
    gstn_no = st.text_input(
        "GSTN No.",
        value=agency_data["gstn_no"],
        max_chars=15
    )
    if gstn_no and not re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", gstn_no):
        st.warning("GSTN No. must follow the format: 15-character GSTIN (e.g., 22AAAAA0000A1Z5).")

    # Registration Active
    reg_active = st.radio(
        "Registration Active",
        ["Yes", "No"],
        index=["Yes", "No"].index(agency_data["reg_active"])
    )

    # Accounts Audited
    accounts_audited = st.radio(
        "Accounts Audited",
        ["Yes", "No"],
        index=["Yes", "No"].index(agency_data["accounts_audited"])
    )

    # Bye Laws
    bye_laws = st.radio(
        "Bye Laws Cover Proposed Activity",
        ["Yes", "No"],
        index=["Yes", "No"].index(agency_data["bye_laws"])
    )

    # Administrative Cost
    try:
        admin_cost = float(agency_data["admin_cost"] or 0)
    except (ValueError, TypeError):
        admin_cost = 0.0
    admin_cost = st.number_input(
        "Administrative Cost",
        min_value=0.0,
        value=admin_cost,
        step=0.01
    )

    # GST Amount
    try:
        gst_amount = float(agency_data["gst_amount"] or 0)
    except (ValueError, TypeError):
        gst_amount = 0.0
    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0,
        value=gst_amount,
        step=0.01
    )

    # Total Cost
    total_cost = st.number_input(
        "Total Cost",
        min_value=0.0,
        value=float(admin_cost + gst_amount),
        disabled=True
    )

    return {
        "vendor_no": vendor_no,
        "csr1_reg_no": csr1_reg_no,
        "agency_type": agency_type,
        "pan_no": pan_no,
        "gstn_no": gstn_no,
        "reg_active": reg_active,
        "accounts_audited": accounts_audited,
        "bye_laws": bye_laws,
        "admin_cost": admin_cost,
        "gst_amount": gst_amount,
        "total_cost": total_cost
    }