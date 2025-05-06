import streamlit as st
import datetime

def project_details_tab(project_data=None):
    st.header("Project Details")
    project_data = project_data or [None] * 15
    
    project_name = st.text_input("Project Name *", value=project_data[0] or "", max_chars=100)
    moa_signed_options = ["Yes", "No"]
    default_moa_signed = project_data[1] if project_data[1] in moa_signed_options else "Yes"
    moa_signed = st.selectbox("MoA Signed", moa_signed_options, index=moa_signed_options.index(default_moa_signed))
    
    # Validate moa_date
    moa_date_value = project_data[2]
    if moa_date_value is not None:
        # Check if it's already a date or datetime object
        if isinstance(moa_date_value, (datetime.date, datetime.datetime)):
            moa_date_value = moa_date_value
        else:
            # Try to parse it as an ISO string (e.g., "2025-05-03")
            try:
                moa_date_value = datetime.datetime.fromisoformat(str(moa_date_value)).date()
            except (ValueError, TypeError):
                moa_date_value = None  # Default to None if parsing fails
    
    moa_date = st.date_input("MoA Date", value=moa_date_value) if moa_signed == "Yes" else None
    execution_validity = st.number_input("Execution Validity (Months)", min_value=0, value=int(project_data[3] or 0), step=1)
    disha_file_1 = st.text_input("DISHA File 1 *", value=project_data[4] or "", max_chars=50)
    disha_file_2 = st.text_input("DISHA File 2", value=project_data[5] or "", max_chars=50)
    commencement_date = st.date_input("Commencement Date", value=None if project_data[6] is None else project_data[6])
    end_date = st.date_input("End Date", value=None if project_data[7] is None else project_data[7])
    duration = st.number_input("Duration (Months)", min_value=0, value=int(project_data[8] or 0), step=1)
    mode_of_implementation = st.selectbox("Mode of Implementation", ["Own", "Agency"], index=["Own", "Agency"].index(project_data[9] or "Own"))
    schedule_7 = st.selectbox("Schedule 7 / Internal Order No.", ["I0001", "I0002"], index=["I0001", "I0002"].index(project_data[10] or "I0001") if project_data[10] in ["I0001", "I0002"] else 0)
    milestones = st.text_area("Milestones", value=project_data[11] or "", max_chars=500)
    focused_category = st.selectbox("Focused Category", ["Category A", "Category B"], index=["Category A", "Category B"].index(project_data[12] or "Category A"))
    focused_category_text = st.text_input("Focused Category Text", value=project_data[13] or "", max_chars=100)
    focused_category_desc = st.text_area("Focused Category Description", value=project_data[14] or "", max_chars=500)

    return {
        "project_name": project_name,
        "moa_signed": moa_signed,
        "moa_date": moa_date,
        "execution_validity": execution_validity,
        "disha_file_1": disha_file_1,
        "disha_file_2": disha_file_2,
        "commencement_date": commencement_date,
        "end_date": end_date,
        "duration": duration,
        "mode_of_implementation": mode_of_implementation,
        "schedule_7": schedule_7,
        "milestones": milestones,
        "focused_category": focused_category,
        "focused_category_text": focused_category_text,
        "focused_category_desc": focused_category_desc
    }