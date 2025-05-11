# # import streamlit as st

# # def financial_details_tab(financial_data=None, gst_amount=0):
# #     st.header("Financial Details")
# #     financial_data = financial_data or [None] * 7
# #     # bdp_name = st.text_input("BDP Name", value=financial_data[1] or "", max_chars=14)
# #     bdp_names = ["BDP001", "BDP002", "BDP003", "BDP004", "BDP005", "BDP006"]
# #     default_bdp_name = financial_data[1] or ""
# #     bdp_name_idx = bdp_names.index(default_bdp_name) if default_bdp_name in bdp_names else 0
# #     bdp_name = st.selectbox("BDP Name", bdp_names, index=bdp_name_idx)
    
# #     # company_code = st.text_input("Company Code", value=financial_data[2] or "", max_chars=4)
# #     company_codes = ["DLI", "MUM", "KOL", "CHN", "AHM", "VDR"]
# #     default_company_code = financial_data[0] or ""
# #     company_code_idx = company_codes.index(default_company_code) if default_company_code in company_codes else 0
# #     company_code = st.selectbox("Company Code *", company_codes, index=company_code_idx)
    
# #     amount_applied = st.number_input("Amount Applied *", min_value=0.0, value=float(financial_data[2] or 0), step=1.0)
# #     amount_approved = st.number_input("Amount Approved *", min_value=0.0, value=float(financial_data[3] or 0), step=1.0)
# #     total_cost = st.number_input("Total Project Cost *", min_value=0.0, value=float(amount_approved + gst_amount), disabled=True)
# #     first_pay_date = st.date_input("First Payment Date *", value=None if financial_data[5] is None else financial_data[5])

# #     # Immediate feedback for validation rules
# #     if amount_applied <= amount_approved and amount_applied or amount_approved != 0.0:
# #         st.warning("Amount Applied must be greater than Amount Approved.")


 

# #     return {
# #         "bdp_name": bdp_name,
# #         "company_code": company_code,
# #         "amount_applied": amount_applied,
# #         "amount_approved": amount_approved,
# #         "total_cost": total_cost,
# #         "first_pay_date": first_pay_date
# #     }


# import streamlit as st
# import datetime

# def financial_details_tab(financial_data=None, gst_amount=0):
#     st.header("Financial Details")

#     # Ensure financial_data is a dictionary or fallback to list
#     if isinstance(financial_data, dict):
#         # Access by keys if it's a dictionary
#         financial_data = {key: financial_data.get(key, None) for key in ['company_code', 'bdp_name', 'amount_applied', 'amount_approved', 'total_cost', 'first_pay_date']}
#     else:
#         # If it's a list, use the default list structure
#         financial_data = financial_data or [None] * 6

#     bdp_names = ["BDP001", "BDP002", "BDP003", "BDP004", "BDP005", "BDP006"]
#     default_bdp_name = financial_data['bdp_name'] or ""
#     bdp_name_idx = bdp_names.index(default_bdp_name) if default_bdp_name in bdp_names else 0
#     bdp_name = st.selectbox("BDP Name", bdp_names, index=bdp_name_idx)

#     company_codes = ["DLI", "MUM", "KOL", "CHN", "AHM", "VDR"]
#     default_company_code = financial_data['company_code'] or ""
#     company_code_idx = company_codes.index(default_company_code) if default_company_code in company_codes else 0
#     company_code = st.selectbox("Company Code *", company_codes, index=company_code_idx)

#     amount_applied = st.number_input("Amount Applied *", min_value=0.0, value=float(financial_data['amount_applied'] or 0), step=1.0)
#     amount_approved = st.number_input("Amount Approved *", min_value=0.0, value=float(financial_data['amount_approved'] or 0), step=1.0)

#     # Total cost = approved + GST
#     total_cost = st.number_input("Total Project Cost *", min_value=0.0, value=float(amount_approved + gst_amount), disabled=True)

#     default_date = financial_data['first_pay_date'] if isinstance(financial_data['first_pay_date'], datetime.date) else datetime.date.today()
#     first_pay_date = st.date_input("First Payment Date *", value=default_date)

#     # ✅ Validation Rule Fix
#     if amount_applied <= amount_approved and (amount_applied != 0.0 or amount_approved != 0.0):
#         st.warning("⚠️ Amount Applied must be greater than Amount Approved.")

#     return {
#         "bdp_name": bdp_name,
#         "company_code": company_code,
#         "amount_applied": amount_applied,
#         "amount_approved": amount_approved,
#         "total_cost": total_cost,
#         "first_pay_date": first_pay_date
#     }


import streamlit as st
import datetime

def financial_details_tab(financial_data=None, gst_amount=0.0):
    st.header("Financial Details")

    # Initialize default dictionary
    defaults = {
        "bdp_name": "",
        "company_code": "",
        "amount_applied": 0.0,
        "amount_approved": 0.0,
        "total_cost": 0.0,
        "first_pay_date": None
    }
    financial_data = financial_data or {}
    for key, value in defaults.items():
        financial_data.setdefault(key, value)

    # BDP Name
    bdp_names = ["BDP001", "BDP002", "BDP003", "BDP004", "BDP005", "BDP006"]
    bdp_name = st.selectbox(
        "BDP Name",
        bdp_names,
        index=bdp_names.index(financial_data["bdp_name"]) if financial_data["bdp_name"] in bdp_names else 0
    )

    # Company Code
    company_codes = ["DLI", "MUM", "KOL", "CHN", "AHM", "VDR"]
    company_code = st.selectbox(
        "Company Code *",
        company_codes,
        index=company_codes.index(financial_data["company_code"]) if financial_data["company_code"] in company_codes else 0
    )

    # Amount Applied
    try:
        amount_applied = float(financial_data["amount_applied"] or 0)
    except (ValueError, TypeError):
        amount_applied = 0.0
    amount_applied = st.number_input(
        "Amount Applied *",
        min_value=0.0,
        value=amount_applied,
        step=1.0
    )

    # Amount Approved
    try:
        amount_approved = float(financial_data["amount_approved"] or 0)
    except (ValueError, TypeError):
        amount_approved = 0.0
    amount_approved = st.number_input(
        "Amount Approved *",
        min_value=0.0,
        value=amount_approved,
        step=1.0
    )

    # Total Cost
    try:
        total_cost = float(financial_data["total_cost"] or 0)
    except (ValueError, TypeError):
        total_cost = amount_approved + gst_amount
    total_cost = st.number_input(
        "Total Project Cost *",
        min_value=0.0,
        value=amount_approved ,
        disabled=True
    )

    # First Payment Date
    def parse_date(val):
        if val and isinstance(val, (datetime.date, datetime.datetime)):
            return val
        try:
            return datetime.datetime.strptime(str(val), "%Y-%m-%d").date() if val else datetime.date.today()
        except (ValueError, TypeError):
            return datetime.date.today()

    first_pay_date = st.date_input(
        "First Payment Date *",
        value=parse_date(financial_data["first_pay_date"])
    )

    # Validation
    if amount_applied <= amount_approved and (amount_applied != 0.0 or amount_approved != 0.0):
        st.error("Amount Applied must be greater than Amount Approved.")

    return {
        "bdp_name": bdp_name,
        "company_code": company_code,
        "amount_applied": amount_applied,
        "amount_approved": amount_approved,
        "total_cost": total_cost,
        "first_pay_date": first_pay_date
    }