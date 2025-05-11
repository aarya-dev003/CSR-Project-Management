# import streamlit as st
# import datetime
# from datetime import datetime, date



# def project_details_tab(project_data=None):
#     st.header("Project Details")
#     # Initialize default dictionary based on schema
#     defaults = {
#         "project_name": "",
#         "disha_file_1": "",
#         "disha_file_2": "",
#         "disha_file_3": "",
#         "moa_signed": "Yes",
#         "moa_date": None,
#         "moa_validity": 0,
#         "execution_validity": 0,
#         "screening_committee": "No",
#         "schedule_7": "I0001",
#         "commencement_date": None,
#         "end_date": None,
#         "duration": "0",
#         "mode_implementation": "Own",
#         "execution_end_date": None,
#         "milestones": 0,
#         "focused_category": "Category A"
#     }
#     project_data = project_data or {}
#     for key, value in defaults.items():
#         project_data.setdefault(key, value)

#     # Project Name
#     project_name = st.text_input("Project Name *", value=project_data["project_name"], max_chars=100)

#     # MoA Signed
#     moa_signed = st.selectbox("MoA Signed", ["Yes", "No"], index=["Yes", "No"].index(project_data["moa_signed"]))

#     # MoA Date
#     moa_date_value = project_data["moa_date"]
#     if moa_date_value and isinstance(moa_date_value, (datetime.date, datetime.datetime)):
#         moa_date_value = moa_date_value
#     elif moa_date_value:
#         try:
#             moa_date_value = datetime.datetime.fromisoformat(str(moa_date_value)).date()
#         except (ValueError, TypeError):
#             moa_date_value = None
#     moa_date = st.date_input("MoA Date * (if signed)", value=moa_date_value, disabled=moa_signed == "No") if moa_signed == "Yes" else None

#     # MoA Validity
#     try:
#         moa_validity = int(project_data["moa_validity"] or 0)
#     except (ValueError, TypeError):
#         moa_validity = 0
#     moa_validity = st.number_input("MoA Validity (Months)", min_value=0, value=moa_validity, step=1)

#     # Execution Validity
#     try:
#         execution_validity = int(project_data["execution_validity"] or 0)
#     except (ValueError, TypeError):
#         execution_validity = 0
#     execution_validity = st.number_input("Execution Validity (Months)", min_value=0, value=execution_validity, step=1)

#     # DISHA Files
#     disha_file_1 = st.text_input("DISHA File 1 *", value=project_data["disha_file_1"], max_chars=250)
#     disha_file_2 = st.text_input("DISHA File 2", value=project_data["disha_file_2"], max_chars=250)
#     disha_file_3 = st.text_input("DISHA File 3", value=project_data["disha_file_3"], max_chars=250)

#     # Screening Committee
#     screening_committee = st.selectbox("Screening Committee", ["Yes", "No"], index=["Yes", "No"].index(project_data["screening_committee"]))

#     # Schedule 7
#     schedule_7_options = ["I0001", "I0002"]
#     schedule_7 = st.selectbox(
#         "Schedule 7 / Internal Order No.",
#         schedule_7_options,
#         index=schedule_7_options.index(project_data["schedule_7"]) if project_data["schedule_7"] in schedule_7_options else 0
#     )

#     # Dates
#     commencement_date = st.date_input("Commencement Date", value=project_data["commencement_date"])
#     # end_date = st.date_input("End Date", value=project_data["end_date"])
#     # end_date = st.date_input("End Date", value=project_data.get("end_date", datetime.today().date()))

#     end_date = project_data.get("end_date", date.today())
#     if isinstance(end_date, str):
#         end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#     end_date = st.date_input("End Date", value=end_date)
#     execution_end_date = st.date_input("Execution End Date", value=project_data["execution_end_date"])

#     # Duration (stored as VARCHAR(10), but input as integer)
#     try:
#         duration = str(int(project_data["duration"] or 0))
#     except (ValueError, TypeError):
#         duration = "0"
#     duration_value = int(duration) if duration.isdigit() else 0
#     duration = str(st.number_input("Duration (Months)", min_value=0, value=duration_value, step=1))

#     # Mode of Implementation
#     mode_of_implementation = st.selectbox(
#         "Mode of Implementation",
#         ["Own", "Agency"],
#         index=["Own", "Agency"].index(project_data["mode_implementation"])
#     )

#     # Milestones
#     try:
#         milestones = int(project_data["milestones"] or 0)
#     except (ValueError, TypeError):
#         milestones = 0
#     milestones = st.number_input("Milestones", min_value=0, value=milestones, step=1)

#     # Focused Category
#     focused_category_options = ["Category A", "Category B"]
#     focused_category_value = project_data["focused_category"]
#     if focused_category_value not in focused_category_options:
#         focused_category_value = focused_category_options[0]  # Default to Category A
#     focused_category = st.selectbox(
#         "Focused Category",
#         focused_category_options,
#         index=focused_category_options.index(focused_category_value)
#     )

#     return {
#         "project_name": project_name,
#         "disha_file_1": disha_file_1,
#         "disha_file_2": disha_file_2,
#         "disha_file_3": disha_file_3,
#         "moa_signed": moa_signed,
#         "moa_date": moa_date,
#         "moa_validity": moa_validity,
#         "execution_validity": execution_validity,
#         "screening_committee": screening_committee,
#         "schedule_7": schedule_7,
#         "commencement_date": commencement_date,
#         "end_date": end_date,
#         "duration": duration,
#         "mode_implementation": mode_of_implementation,
#         "execution_end_date": execution_end_date,
#         "milestones": milestones,
#         "focused_category": focused_category
#     }


import streamlit as st
import datetime

def project_details_tab(project_data=None):
    st.header("Project Details")
    
    # Initialize default dictionary
    defaults = {
        "project_name": "",
        "disha_file_1": "",
        "disha_file_2": "",
        "disha_file_3": "",
        "moa_signed": "Yes",
        "moa_date": None,
        "moa_validity": 0,
        "execution_validity": 0,
        "screening_committee": "No",
        "schedule_7": "I0001",
        "commencement_date": None,
        "end_date": None,
        "duration": "0",
        "mode_implementation": "Own",
        "execution_end_date": None,
        "milestones": 0,
        "focused_category": "Category A"
    }
    project_data = project_data or {}
    for key, value in defaults.items():
        project_data.setdefault(key, value)

    # Project Name
    project_name = st.text_input(
        "Project Name *",
        value=project_data["project_name"],
        max_chars=100
    )
    if not project_name.strip():
        st.warning("Project Name is mandatory.")

    # MoA Signed
    moa_signed = st.selectbox(
        "MoA Signed",
        ["Yes", "No"],
        index=["Yes", "No"].index(project_data["moa_signed"])
    )

    # MoA Date
    def parse_date(val):
        if val and isinstance(val, (datetime.date, datetime.datetime)):
            return val
        try:
            return datetime.datetime.strptime(str(val), "%Y-%m-%d").date() if val else None
        except (ValueError, TypeError):
            return None

    moa_date = st.date_input(
        "MoA Date * (if signed)",
        value=parse_date(project_data["moa_date"]),
        disabled=moa_signed == "No"
    ) if moa_signed == "Yes" else None
    if moa_signed == "Yes" and not moa_date:
        st.warning("MoA Date is mandatory when MoA is signed.")

    # MoA Validity
    try:
        moa_validity = int(project_data["moa_validity"] or 0)
    except (ValueError, TypeError):
        moa_validity = 0
    moa_validity = st.number_input(
        "MoA Validity (Months)",
        min_value=0,
        value=moa_validity,
        step=1
    )

    # Execution Validity
    try:
        execution_validity = int(project_data["execution_validity"] or 0)
    except (ValueError, TypeError):
        execution_validity = 0
    execution_validity = st.number_input(
        "Execution Validity (Months)",
        min_value=0,
        value=execution_validity,
        step=1
    )

    # DISHA Files
    disha_file_1 = st.text_input(
        "DISHA File 1 *",
        value=project_data["disha_file_1"],
        max_chars=250
    )
    if not disha_file_1.strip():
        st.warning("DISHA File 1 is mandatory.")
    disha_file_2 = st.text_input(
        "DISHA File 2",
        value=project_data["disha_file_2"],
        max_chars=250
    )
    disha_file_3 = st.text_input(
        "DISHA File 3",
        value=project_data["disha_file_3"],
        max_chars=250
    )

    # Screening Committee
    screening_committee = st.selectbox(
        "Screening Committee",
        ["Yes", "No"],
        index=["Yes", "No"].index(project_data["screening_committee"])
    )

    # Schedule 7
    schedule_7_options = ["I0001", "I0002"]
    schedule_7 = st.selectbox(
        "Schedule 7 / Internal Order No.",
        schedule_7_options,
        index=schedule_7_options.index(project_data["schedule_7"]) if project_data["schedule_7"] in schedule_7_options else 0
    )

    # Dates
    commencement_date = st.date_input(
        "Commencement Date",
        value=parse_date(project_data["commencement_date"])
    )
    end_date = st.date_input(
        "End Date",
        value=parse_date(project_data["end_date"])
    )
    execution_end_date = st.date_input(
        "Execution End Date",
        value=parse_date(project_data["execution_end_date"])
    )

    # Duration
    try:
        duration = str(int(project_data["duration"] or 0))
    except (ValueError, TypeError):
        duration = "0"
    duration_value = int(duration) if duration.isdigit() else 0
    duration = str(st.number_input(
        "Duration (Months)",
        min_value=0,
        value=duration_value,
        step=1
    ))

    # Mode of Implementation
    mode_implementation = st.selectbox(
        "Mode of Implementation",
        ["Own", "Agency"],
        index=["Own", "Agency"].index(project_data["mode_implementation"])
    )

    # Milestones
    try:
        milestones = int(project_data["milestones"] or 0)
    except (ValueError, TypeError):
        milestones = 0
    milestones = st.number_input(
        "Milestones",
        min_value=0,
        value=milestones,
        step=1
    )

    # Focused Category
    focused_category_options = ["Category A", "Category B"]
    focused_category = st.selectbox(
        "Focused Category",
        focused_category_options,
        index=focused_category_options.index(project_data["focused_category"])
    )

    return {
        "project_name": project_name,
        "disha_file_1": disha_file_1,
        "disha_file_2": disha_file_2,
        "disha_file_3": disha_file_3,
        "moa_signed": moa_signed,
        "moa_date": moa_date,
        "moa_validity": moa_validity,
        "execution_validity": execution_validity,
        "screening_committee": screening_committee,
        "schedule_7": schedule_7,
        "commencement_date": commencement_date,
        "end_date": end_date,
        "duration": duration,
        "mode_implementation": mode_implementation,
        "execution_end_date": execution_end_date,
        "milestones": milestones,
        "focused_category": focused_category
    }