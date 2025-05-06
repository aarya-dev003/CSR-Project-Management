import streamlit as st

def agency_details_tab(agency_data=None):
    st.header("Agency Details")
    agency_data = agency_data or [None] * 12
    vendor_no = st.text_input("Vendor No.", value=agency_data[1] or "", max_chars=10)
    csr1_reg_no = st.text_input("CSR-1 Registration No.", value=agency_data[2] or "", max_chars=25)
    agency_type = st.selectbox("Agency Type", ["Registered Society", "Section 8 Company", "Trust"], index=["Registered Society", "Section 8 Company", "Trust"].index(agency_data[3] or "Registered Society"))
    pan_no = st.text_input("PAN No.", value=agency_data[4] or "", max_chars=10)
    gstn_no = st.text_input("GSTN No.", value=agency_data[5] or "", max_chars=18)
    reg_active = st.radio("Registration Active", ["Yes", "No"], index=["Yes", "No"].index(agency_data[6] or "Yes"))
    accounts_audited = st.radio("Accounts Audited", ["Yes", "No"], index=["Yes", "No"].index(agency_data[7] or "Yes"))
    bye_laws = st.radio("Bye Laws Cover Proposed Activity", ["Yes", "No"], index=["Yes", "No"].index(agency_data[8] or "Yes"))
    admin_cost = st.number_input("Administrative Cost", value=float(agency_data[9] or 0))
    gst_amount = st.number_input("GST Amount", value=float(agency_data[10] or 0))
    total_cost = st.number_input("Total Cost", value=float(admin_cost + gst_amount), disabled=True)

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