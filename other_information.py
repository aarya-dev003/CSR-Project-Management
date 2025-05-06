import streamlit as st

def other_information_tab(other_data=None):
    st.header("Other Information")
    other_data = other_data or [None] * 13
    fpr_cpf = st.text_input("FPR CPF", value=other_data[1] or "", max_chars=12)
    project_ref = st.selectbox("Project Reference", ["MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister", "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"], 
                               index=["MP (RS)", "MP (LS)", "MLA", "Internal", "Union Minister", "Chief Minister", "MoPNG", "Other Ministry", "Mayor", "Any Other", "None"].index(other_data[2] or "None"))
    ref_name = st.text_input("Reference Name", value=other_data[3] or "", max_chars=50)
    designation = st.text_input("Designation", value=other_data[4] or "", max_chars=50)
    
    beneficiaries = 1
    # Use integers consistently for beneficiary fields
    # beneficiaries = st.number_input("Beneficiaries", value=int(other_data[5] or 0), min_value=0, step=1)
    direct_beneficiaries = st.number_input("Direct Beneficiaries", min_value=0, value=int(other_data[6] or 0), step=1)
    
    # Calculate min_value for indirect_beneficiaries
    min_indirect = int(direct_beneficiaries * 4 if direct_beneficiaries > 0 else 0)
    # Ensure the default value is at least the min_value
    default_indirect = int(other_data[7] or 0)
    if default_indirect < min_indirect:
        default_indirect = min_indirect
    indirect_beneficiaries = st.number_input("Indirect Beneficiaries", min_value=min_indirect, value=default_indirect, step=1)
    
    # Use integers consistently for percentage fields
    obc_percent = st.number_input("OBC %", min_value=0, max_value=100, value=int(other_data[8] or 0), step=1)
    scst_percent = st.number_input("SC/ST %", min_value=0, max_value=100 - obc_percent, value=int(other_data[9] or 0), step=1)
    divyang_percent = st.number_input("Divyang %", min_value=0, max_value=100, value=int(other_data[10] or 0), step=1)
    women_percent = st.number_input("Women %", min_value=0, max_value=100, value=int(other_data[11] or 0), step=1)
    ews_percent = st.number_input("EWS %", min_value=0, max_value=100, value=int(other_data[12] or 0), step=1)

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