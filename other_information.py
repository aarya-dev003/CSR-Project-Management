# # import streamlit as st

# # def other_information_tab(other_data=None):
# #     st.header("Other Information")
# #     other_data = other_data or [None] * 13
# #     fpr_cpf = st.text_input("FPR CPF", value=other_data[1] or "", max_chars=12)
# #     project_ref = st.selectbox("Project Reference", ["MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister", "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"], 
# #                                index=["MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister", "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"].index(other_data[2] or "None"))
# #     ref_name = st.text_input("Reference Name", value=other_data[3] or "", max_chars=50)
# #     designation = st.text_input("Designation", value=other_data[4] or "", max_chars=50)
    
# #     beneficiaries = 1
# #     # Use integers consistently for beneficiary fields
# #     # beneficiaries = st.number_input("Beneficiaries", value=int(other_data[5] or 0), min_value=0, step=1)
# #     direct_beneficiaries = st.number_input("Direct Beneficiaries", min_value=0, value=int(other_data[6] or 0), step=1)
    
# #     # Calculate min_value for indirect_beneficiaries
# #     min_indirect = int(direct_beneficiaries * 4 if direct_beneficiaries > 0 else 0)
# #     # Ensure the default value is at least the min_value
# #     default_indirect = int(other_data[7] or 0)
# #     if default_indirect < min_indirect:
# #         default_indirect = min_indirect
# #     indirect_beneficiaries = st.number_input("Indirect Beneficiaries", min_value=min_indirect, value=default_indirect, step=1)
    
# #     # Use integers consistently for percentage fields
# #     obc_percent = st.number_input("OBC %", min_value=0, max_value=100, value=int(other_data[8] or 0), step=1)
# #     scst_percent = st.number_input("SC/ST %", min_value=0, max_value=100 - obc_percent, value=int(other_data[9] or 0), step=1)
# #     divyang_percent = st.number_input("Divyang %", min_value=0, max_value=100, value=int(other_data[10] or 0), step=1)
# #     women_percent = st.number_input("Women %", min_value=0, max_value=100, value=int(other_data[11] or 0), step=1)
# #     ews_percent = st.number_input("EWS %", min_value=0, max_value=100, value=int(other_data[12] or 0), step=1)

# #     return {
# #         "fpr_cpf": fpr_cpf,
# #         "project_ref": project_ref,
# #         "ref_name": ref_name,
# #         "designation": designation,
# #         "beneficiaries": beneficiaries,
# #         "direct_beneficiaries": direct_beneficiaries,
# #         "indirect_beneficiaries": indirect_beneficiaries,
# #         "obc_percent": obc_percent,
# #         "scst_percent": scst_percent,
# #         "divyang_percent": divyang_percent,
# #         "women_percent": women_percent,
# #         "ews_percent": ews_percent
# #     }


# import streamlit as st

# def other_information_tab(other_data=None):
#     st.header("Other Information")
    
#     # Initialize default dictionary
#     defaults = {
#         "fpr_cpf": "",
#         "project_ref": "None",
#         "ref_name": "",
#         "designation": "",
#         "beneficiaries": 1,
#         "direct_beneficiaries": 0,
#         "indirect_beneficiaries": 0,
#         "obc_percent": 0,
#         "scst_percent": 0,
#         "divyang_percent": 0,
#         "women_percent": 0,
#         "ews_percent": 0
#     }
#     other_data = other_data or {}
#     for key, value in defaults.items():
#         other_data.setdefault(key, value)

#     # FPR/CPF
#     fpr_cpf = st.text_input("FPR/CPF", value=other_data["fpr_cpf"], max_chars=12)

#     # Project Reference
#     project_ref_options = [
#         "MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister",
#         "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"
#     ]
#     project_ref = st.selectbox(
#         "Project Reference *",
#         project_ref_options,
#         index=project_ref_options.index(other_data["project_ref"])
#     )

#     # Reference Name and Designation
#     ref_name = st.text_input("Reference Name *", value=other_data["ref_name"], max_chars=50)
#     designation = st.text_input("Designation *", value=other_data["designation"], max_chars=50)

#     # Beneficiaries
#     try:
#         beneficiaries = int(other_data["beneficiaries"] or 1)
#     except (ValueError, TypeError):
#         beneficiaries = 1
#     beneficiaries = st.number_input(
#         "Total Beneficiaries *",
#         min_value=1,
#         value=beneficiaries,
#         step=1
#     )

#     # Direct Beneficiaries
#     try:
#         direct_beneficiaries = int(other_data["direct_beneficiaries"] or 0)
#     except (ValueError, TypeError):
#         direct_beneficiaries = 0
#     direct_beneficiaries = st.number_input(
#         "Direct Beneficiaries",
#         min_value=0,
#         value=direct_beneficiaries,
#         step=1
#     )

#     # Indirect Beneficiaries
#     min_indirect = direct_beneficiaries * 4 if direct_beneficiaries > 0 else 0
#     try:
#         indirect_beneficiaries = int(other_data["indirect_beneficiaries"] or 0)
#     except (ValueError, TypeError):
#         indirect_beneficiaries = min_indirect
#     indirect_beneficiaries = st.number_input(
#         "Indirect Beneficiaries",
#         min_value=min_indirect,
#         value=max(indirect_beneficiaries, min_indirect),
#         step=1
#     )

#     # Percentage Fields with Sum Constraint
#     try:
#         obc_percent = int(other_data["obc_percent"] or 0)
#     except (ValueError, TypeError):
#         obc_percent = 0
#     obc_percent = st.number_input(
#         "OBC %",
#         min_value=0,
#         max_value=100,
#         value=obc_percent,
#         step=1
#     )

#     try:
#         scst_percent = int(other_data["scst_percent"] or 0)
#     except (ValueError, TypeError):
#         scst_percent = 0
#     scst_percent = st.number_input(
#         "SC/ST %",
#         min_value=0,
#         max_value=100 - obc_percent,
#         value=scst_percent,
#         step=1
#     )

#     try:
#         divyang_percent = int(other_data["divyang_percent"] or 0)
#     except (ValueError, TypeError):
#         divyang_percent = 0
#     divyang_percent = st.number_input(
#         "Divyang %",
#         min_value=0,
#         max_value=100 - obc_percent - scst_percent,
#         value=divyang_percent,
#         step=1
#     )

#     try:
#         women_percent = int(other_data["women_percent"] or 0)
#     except (ValueError, TypeError):
#         women_percent = 0
#     women_percent = st.number_input(
#         "Women %",
#         min_value=0,
#         max_value=100 - obc_percent - scst_percent - divyang_percent,
#         value=women_percent,
#         step=1
#     )

#     try:
#         ews_percent = int(other_data["ews_percent"] or 0)
#     except (ValueError, TypeError):
#         ews_percent = 0
#     ews_percent = st.number_input(
#         "EWS %",
#         min_value=0,
#         max_value=100 - obc_percent - scst_percent - divyang_percent - women_percent,
#         value=ews_percent,
#         step=1
#     )

#     # Warn if percentages sum to more than 100
#     total_percent = obc_percent + scst_percent + divyang_percent + women_percent + ews_percent
#     if total_percent > 100:
#         st.warning("Total percentage exceeds 100%. Please adjust the values.")

#     return {
#         "fpr_cpf": fpr_cpf,
#         "project_ref": project_ref,
#         "ref_name": ref_name,
#         "designation": designation,
#         "beneficiaries": beneficiaries,
#         "direct_beneficiaries": direct_beneficiaries,
#         "indirect_beneficiaries": indirect_beneficiaries,
#         "obc_percent": obc_percent,
#         "scst_percent": scst_percent,
#         "divyang_percent": divyang_percent,
#         "women_percent": women_percent,
#         "ews_percent": ews_percent
#     }


import streamlit as st
import re

def other_information_tab(other_data=None):
    st.header("Other Information")
    
    # Initialize default dictionary
    defaults = {
        "fpr_cpf": "",
        "project_ref": "None",
        "ref_name": "",
        "designation": "",
        "beneficiaries": 1,
        "direct_beneficiaries": 0,
        "indirect_beneficiaries": 0,
        "obc_percent": 0,
        "scst_percent": 0,
        "divyang_percent": 0,
        "women_percent": 0,
        "ews_percent": 0
    }
    other_data = other_data or {}
    for key, value in defaults.items():
        other_data.setdefault(key, value)

    # FPR/CPF
    fpr_cpf = st.text_input(
        "FPR/CPF",
        value=other_data["fpr_cpf"],
        max_chars=12
    )
    if fpr_cpf and not re.match(r"^[A-Za-z0-9]{1,12}$", fpr_cpf):
        st.warning("FPR/CPF must be alphanumeric and up to 12 characters.")

    # Project Reference
    project_ref_options = [
        "MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister",
        "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"
    ]
    project_ref = st.selectbox(
        "Project Reference *",
        project_ref_options,
        index=project_ref_options.index(other_data["project_ref"])
    )

    # Reference Name and Designation
    ref_name = st.text_input(
        "Reference Name *",
        value=other_data["ref_name"],
        max_chars=50
    )
    designation = st.text_input(
        "Designation *",
        value=other_data["designation"],
        max_chars=50
    )

    # Beneficiaries
    try:
        beneficiaries = int(other_data["beneficiaries"] or 1)
    except (ValueError, TypeError):
        beneficiaries = 1
    beneficiaries = st.number_input(
        "Total Beneficiaries *",
        min_value=1,
        value=beneficiaries,
        step=1
    )

    # Direct Beneficiaries
    try:
        direct_beneficiaries = int(other_data["direct_beneficiaries"] or 0)
    except (ValueError, TypeError):
        direct_beneficiaries = 0
    direct_beneficiaries = st.number_input(
        "Direct Beneficiaries",
        min_value=0,
        value=direct_beneficiaries,
        step=1
    )

    # Indirect Beneficiaries
    min_indirect = direct_beneficiaries * 4 if direct_beneficiaries > 0 else 0
    try:
        indirect_beneficiaries = int(other_data["indirect_beneficiaries"] or 0)
    except (ValueError, TypeError):
        indirect_beneficiaries = min_indirect
    indirect_beneficiaries = st.number_input(
        "Indirect Beneficiaries",
        min_value=min_indirect,
        value=max(indirect_beneficiaries, min_indirect),
        step=1
    )

    # Percentage Fields with Sum Constraint
    try:
        obc_percent = int(other_data["obc_percent"] or 0)
    except (ValueError, TypeError):
        obc_percent = 0
    obc_percent = st.number_input(
        "OBC %",
        min_value=0,
        max_value=100,
        value=obc_percent,
        step=1
    )

    try:
        scst_percent = int(other_data["scst_percent"] or 0)
    except (ValueError, TypeError):
        scst_percent = 0
    scst_percent = st.number_input(
        "SC/ST %",
        min_value=0,
        max_value=100 - obc_percent,
        value=scst_percent,
        step=1
    )

    try:
        divyang_percent = int(other_data["divyang_percent"] or 0)
    except (ValueError, TypeError):
        divyang_percent = 0
    divyang_percent = st.number_input(
        "Divyang %",
        min_value=0,
        max_value=100 - obc_percent - scst_percent,
        value=divyang_percent,
        step=1
    )

    try:
        women_percent = int(other_data["women_percent"] or 0)
    except (ValueError, TypeError):
        women_percent = 0
    women_percent = st.number_input(
        "Women %",
        min_value=0,
        max_value=100 - obc_percent - scst_percent - divyang_percent,
        value=women_percent,
        step=1
    )

    try:
        ews_percent = int(other_data["ews_percent"] or 0)
    except (ValueError, TypeError):
        ews_percent = 0
    ews_percent = st.number_input(
        "EWS %",
        min_value=0,
        max_value=100 - obc_percent - scst_percent - divyang_percent - women_percent,
        value=ews_percent,
        step=1
    )

    # Warn if percentages sum to more than 100
    total_percent = obc_percent + scst_percent + divyang_percent + women_percent + ews_percent
    if total_percent > 100:
        st.warning("Total percentage exceeds 100%. Please adjust the values.")

    return {
        "fpr_cpf": fpr_cpf,
        "project_ref": project_ref,
        "ref_name": ref_name,
        "designation": designation,
        "beneficiaries": beneficiaries,
        "direct_beneficiaries": direct_beneficiaries,
        "indirect_beneficiaries": indirect_beneficiaries,
        "obc_percent": obc_percent,
        "scst_percent": scst_percent,
        "divyang_percent": divyang_percent,
        "women_percent": women_percent,
        "ews_percent": ews_percent
    }