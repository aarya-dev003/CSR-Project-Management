import streamlit as st

def location_beneficiary_tab(location_data=None):
    st.header("Location/Beneficiary Details")
    location_data = location_data or [None] * 8
    operational_area = st.radio("Operational Area", ["Yes", "No"], index=["Yes", "No"].index(location_data[1] or "Yes"))
    plan_campaign = st.selectbox("Plan/Campaign Name", ["SWACHHTA ACTION PLAN", "ANNUAL COMPONENT PLAN", "SPECIAL COMPONENT PLAN", "HAR GHAR TIRANGA", "OTHER"], 
                                 index=["SWACHHTA ACTION PLAN", "ANNUAL COMPONENT PLAN", "SPECIAL COMPONENT PLAN", "HAR GHAR TIRANGA", "OTHER"].index(location_data[2] or "SWACHHTA ACTION PLAN"))
    plan_campaign_other = st.text_input("Other Plan/Campaign Description", value=location_data[3] or "") if plan_campaign == "OTHER" else None
    activity = st.text_area("Activity under the Project", value=location_data[4] or "")
    all_india = st.radio("All India Implementation", ["Yes", "No"], index=["Yes", "No"].index(location_data[5] or "Yes"))
    districts_impacted = st.number_input("Number of Districts Impacted", min_value=1, max_value=10, value=int(location_data[6] or 1))
    pin_codes = location_data[7] or [""] * districts_impacted
    pin_codes = [st.text_input(f"PIN Code {i}", value=pin_codes[i-1] if i-1 < len(pin_codes) else "") for i in range(1, min(districts_impacted, 11) + 1)]

    return {
        "operational_area": operational_area,
        "plan_campaign": plan_campaign,
        "plan_campaign_other": plan_campaign_other,
        "activity": activity,
        "all_india": all_india,
        "districts_impacted": districts_impacted,
        "pin_codes": pin_codes
    }