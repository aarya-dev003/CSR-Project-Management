import streamlit as st

def financial_details_tab(financial_data=None, gst_amount=0):
    st.header("Financial Details")
    financial_data = financial_data or [None] * 7
    # bdp_name = st.text_input("BDP Name", value=financial_data[1] or "", max_chars=14)
    bdp_names = ["BDP001", "BDP002", "BDP003", "BDP004", "BDP005", "BDP006"]
    default_bdp_name = financial_data[1] or ""
    bdp_name_idx = bdp_names.index(default_bdp_name) if default_bdp_name in bdp_names else 0
    bdp_name = st.selectbox("BDP Name", bdp_names, index=bdp_name_idx)
    
    # company_code = st.text_input("Company Code", value=financial_data[2] or "", max_chars=4)
    company_codes = ["DLI", "MUM", "KOL", "CHN", "AHM", "VDR"]
    default_company_code = financial_data[0] or ""
    company_code_idx = company_codes.index(default_company_code) if default_company_code in company_codes else 0
    company_code = st.selectbox("Company Code *", company_codes, index=company_code_idx)
    
    amount_applied = st.number_input("Amount Applied *", min_value=0.0, value=float(financial_data[2] or 0), step=1.0)
    amount_approved = st.number_input("Amount Approved *", min_value=0.0, value=float(financial_data[3] or 0), step=1.0)
    total_cost = st.number_input("Total Project Cost *", min_value=0.0, value=float(amount_approved + gst_amount), disabled=True)
    first_pay_date = st.date_input("First Payment Date *", value=None if financial_data[5] is None else financial_data[5])

    # Immediate feedback for validation rules
    if amount_applied <= amount_approved and amount_applied or amount_approved != 0.0:
        st.warning("Amount Applied must be greater than Amount Approved.")


    first_pay_date = st.date_input("First Payment Date", value=financial_data[6] or None)

    return {
        "bdp_name": bdp_name,
        "company_code": company_code,
        "amount_applied": amount_applied,
        "amount_approved": amount_approved,
        "total_cost": total_cost,
        "first_pay_date": first_pay_date
    }