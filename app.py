import streamlit as st
import pandas as pd
from datetime import date
from project_details import project_details_tab
from agency_details import agency_details_tab
from financial_details import financial_details_tab
from location_beneficiary import location_beneficiary_tab
from other_information import other_information_tab
from db_helper import create_tables, authenticate_user, generate_project_id, save_project, get_all_projects, get_project, update_status, delete_project

# Initialize Database Tables
create_tables()

# Session State for Login and Navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_approver' not in st.session_state:
    st.session_state.is_approver = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'project_portal_id' not in st.session_state:
    st.session_state.project_portal_id = ""


# Define keys corresponding to each tuple if you're getting raw DB tuples
PROJECT_KEYS = ["name", "description", "created_by", "start_date", "end_date"]
AGENCY_KEYS = ["agency_name", "contact_person", "contact_number"]
FINANCIAL_KEYS = ["budget", "approved", "company_code"]
LOCATION_KEYS = ["district", "block", "village"]
OTHER_KEYS = ["remarks", "status"]

# Login Screen
if not st.session_state.logged_in:
    st.title("Login to CSR Project Management System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_approver = user[0]  # is_approver from database
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    # Sidebar for all post-login screens
    with st.sidebar:
        # Display username at the top of the sidebar
        st.write(f"Logged in as: {st.session_state.username}")

        # Sidebar content specific to each page
        if st.session_state.current_page == "create":
            st.header("Project Header")
            project_portal_id = st.text_input("Project Portal ID", value=st.session_state.project_portal_id, max_chars=15)
            st.session_state.project_portal_id = project_portal_id
            created_by = st.session_state.username
            created_on = date.today()
            # Set initial status to "New" when the page is first loaded
            status = "New"
            st.text_input("Created By", value=created_by, disabled=True)
            st.text_input("Created On", value=created_on, disabled=True)
            st.selectbox("Status", [status], disabled=True)

            # Save Project button
            if st.button("Save Project"):
                st.session_state.save_project_clicked = True

            # Add Back to Dashboard button
            st.markdown("---")
            if st.button("Back to Dashboard"):
                st.session_state.current_page = "dashboard"
                st.session_state.save_project_clicked = False
                st.rerun()

        elif st.session_state.current_page == "update":
            st.header("Project Header")
            project_id = st.session_state.selected_project
            project_portal_id = st.text_input("Project Portal ID", value=st.session_state.project_portal_id, max_chars=15)
            st.session_state.project_portal_id = project_portal_id
            st.text_input("Project ID", value=project_id, disabled=True)
            created_by = st.session_state.username
            created_on = date.today()
            header, *_ = get_project(project_id)
            status = header[4]  # Use the existing status from the database
            st.text_input("Created By", value=header[2], disabled=True)  # Show actual creator
            st.text_input("Created On", value=created_on, disabled=True)
            st.selectbox("Status", [status], disabled=True)

            # Update Project button (action handled in main content)
            if st.button("Update Project"):
                st.session_state.update_project_clicked = True

            # Add Back to Dashboard button
            st.markdown("---")
            if st.button("Back to Dashboard"):
                st.session_state.current_page = "dashboard"
                st.session_state.update_project_clicked = False
                st.rerun()

        # Add Logout button at the bottom of the sidebar for all pages
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_approver = False
            st.session_state.current_page = "dashboard"
            st.session_state.selected_project = None
            st.session_state.project_portal_id = ""
            st.rerun()

    # Main Content Area
    # Dashboard Screen (Post-Login)
    if st.session_state.current_page == "dashboard":
        st.title("CSR Project Management Dashboard")
        st.write(f"Welcome, {st.session_state.username}!")

        # CRUD Operations
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            if st.button("Create New Project"):
                st.session_state.current_page = "create"
                st.session_state.selected_project = None
                st.session_state.project_portal_id = ""
                st.rerun()
        with col2:
            if st.button("View Projects"):
                st.session_state.current_page = "view"
                st.rerun()
        with col3:
            if st.button("Update Project"):
                st.session_state.current_page = "update_select"
                st.rerun()
        with col4:
            if st.button("Delete Project"):
                st.session_state.current_page = "delete_select"
                st.rerun()
        with col5:
            if st.session_state.is_approver and st.button("Approve Project"):
                st.session_state.current_page = "approve_select"
                st.rerun()
        with col6:
            if st.button("View Report"):
                st.session_state.current_page = "report"
                st.rerun()

    # Create Project Screen
    # elif st.session_state.current_page == "create":
    #     st.title("Create New Project")
        
    #     # Initialize save_project_clicked in session state
    #     if 'save_project_clicked' not in st.session_state:
    #         st.session_state.save_project_clicked = False

    #     # Tabs for Data Entry
    #     project_data, agency_data, financial_data, location_data, other_data = {}, {}, {}, {}, {}
    #     tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
        
    #     with tabs[0]:
    #         project_data = project_details_tab()
    #     with tabs[1]:
    #         agency_data = agency_details_tab()
    #     with tabs[2]:
    #         financial_data = financial_details_tab()
    #     with tabs[3]:
    #         location_data = location_beneficiary_tab()
    #     with tabs[4]:
    #         other_data = other_information_tab()

    #     # Handle Save Project button click (logic in main content area)
    #     if st.session_state.save_project_clicked:
    #         # Validate Mandatory Fields
    #         if not financial_data["company_code"]:
    #             st.error("Company Code in Financial Details is mandatory.")
    #         elif not project_data["project_name"] or not project_data["disha_file_1"] or (project_data["moa_signed"] == "Yes" and not project_data["moa_date"]):
    #             st.error("Please fill all mandatory fields in Project Details.")
    #         elif not agency_data["vendor_no"] or not agency_data["csr1_reg_no"] or not agency_data["agency_type"]:
    #             st.error("Please fill all mandatory fields in Agency Details.")
    #         elif not financial_data["amount_applied"] or not financial_data["amount_approved"] or not financial_data["total_cost"] or not financial_data["first_pay_date"]:
    #             st.error("Please fill all mandatory fields in Financial Details.")
    #         elif not location_data["plan_campaign"] or not location_data["activity"] or not location_data["districts_impacted"]:
    #             st.error("Please fill all mandatory fields in Location/Beneficiary.")
    #         elif not other_data["project_ref"] or not other_data["ref_name"] or not other_data["designation"] or not other_data["beneficiaries"]:
    #             st.error("Please fill all mandatory fields in Other Information.")
    #         else:
    #             try:
    #                 # Generate project_id
    #                 year = "2025"
    #                 project_id = generate_project_id(financial_data["company_code"], year)
    #                 # Change status to "Saved" before saving to the database
    #                 status = "Saved"
    #                 save_project(project_id, project_portal_id, created_by, created_on, status,
    #                              project_data, agency_data, financial_data, location_data, other_data)
                    
    #                 st.success(f"Project Saved Successfully! Project ID: {project_id}")
    #                 st.session_state.current_page = "dashboard"
    #                 st.session_state.save_project_clicked = False
    #                 st.rerun()
    #             except Exception as e:
    #                 st.error(f"Error saving project: {e}")
    #                 st.session_state.save_project_clicked = False

    elif st.session_state.current_page == "create":
        st.title("Create New Project")
        
        if 'save_project_clicked' not in st.session_state:
            st.session_state.save_project_clicked = False

        # Initialize default dictionaries
        project_data = {
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
        agency_data = {
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
        financial_data = {
            "bdp_name": "",
            "company_code": "",
            "amount_applied": 0.0,
            "amount_approved": 0.0,
            "total_cost": 0.0,
            "first_pay_date": None
        }
        location_data = {
            "operational_area": "Yes",
            "plan_campaign": "SWACHHTA ACTION PLAN",
            "plan_campaign_other": "",
            "activity": "",
            "all_india": "Yes",
            "districts_impacted": 1,
            "pin_codes": []
        }
        other_data = {
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

        with st.form("create_project_form"):
            tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
            
            with tabs[0]:
                project_data = project_details_tab(project_data)
            with tabs[1]:
                agency_data = agency_details_tab(agency_data)
            with tabs[2]:
                financial_data = financial_details_tab(financial_data, gst_amount=agency_data["gst_amount"])
            with tabs[3]:
                location_data = location_beneficiary_tab(location_data)
            with tabs[4]:
                other_data = other_information_tab(other_data)

            confirm_create = st.checkbox("Confirm create")
            submitted = st.form_submit_button("Save Project")

            if submitted:
                if not confirm_create:
                    st.error("Please confirm the creation by checking the box.")
                elif not financial_data["company_code"]:
                    st.error("Company Code in Financial Details is mandatory.")
                elif not project_data["project_name"] or not project_data["disha_file_1"] or (project_data["moa_signed"] == "Yes" and not project_data["moa_date"]):
                    st.error("Please fill all mandatory fields in Project Details.")
                elif not agency_data["vendor_no"] or not agency_data["csr1_reg_no"] or not agency_data["agency_type"]:
                    st.error("Please fill all mandatory fields in Agency Details.")
                elif not financial_data["amount_applied"] or not financial_data["amount_approved"] or not financial_data["total_cost"] or not financial_data["first_pay_date"]:
                    st.error("Please fill all mandatory fields in Financial Details.")
                elif financial_data["amount_applied"] <= financial_data["amount_approved"] and (financial_data["amount_applied"] != 0.0 or financial_data["amount_approved"] != 0.0):
                    st.error("Amount Applied must be greater than Amount Approved.")
                elif not location_data["plan_campaign"] or not location_data["activity"] or not location_data["districts_impacted"]:
                    st.error("Please fill all mandatory fields in Location/Beneficiary.")
                elif not other_data["project_ref"] or not other_data["ref_name"] or not other_data["designation"] or not other_data["beneficiaries"]:
                    st.error("Please fill all mandatory fields in Other Information.")
                else:
                    try:
                        year = "2025"
                        project_id = generate_project_id(financial_data["company_code"], year)
                        status = "Saved"
                        project_portal_id = st.session_state.project_portal_id
                        created_by = st.session_state.username
                        created_on = date.today()
                        save_project(project_id, project_portal_id, created_by, created_on, status,
                                    project_data, agency_data, financial_data, location_data, other_data)
                        
                        st.success(f"Project Saved Successfully! Project ID: {project_id}")
                        st.session_state.current_page = "dashboard"
                        st.session_state.save_project_clicked = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving project: {e}")
                        st.session_state.save_project_clicked = False

    # View Projects Screen
    elif st.session_state.current_page == "view":
        st.title("View Projects")
        projects = get_all_projects()
        if projects:
            st.table({
                "Project ID": [p[0] for p in projects],
                "Portal ID": [p[1] for p in projects],
                "Created By": [p[2] for p in projects],
                "Created On": [p[3] for p in projects],
                "Status": [p[4] for p in projects],
                "Project Name": [p[5] for p in projects],
                "Company Code": [p[20] for p in projects],
                "Beneficiaries": [p[35] for p in projects]
            })
        else:
            st.write("No projects found.")
        if st.button("Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # Update Project Screen (Select Project)
    elif st.session_state.current_page == "update_select":
        st.title("Select Project to Update")
        projects = get_all_projects()
        project_ids = [p[0] for p in projects]
        selected_project = st.selectbox("Select Project", project_ids)
        if st.button("Edit"):
            st.session_state.selected_project = selected_project
            st.session_state.current_page = "update"
            header, *_ = get_project(selected_project)
            st.session_state.project_portal_id = header[1]
            st.rerun()
        if st.button("Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # Update Project Screen
    # elif st.session_state.current_page == "update":
    #     st.title(f"Update Project: {st.session_state.selected_project}")
    #     project_id = st.session_state.selected_project
        
    #     # Initialize update_project_clicked in session state
    #     if 'update_project_clicked' not in st.session_state:
    #         st.session_state.update_project_clicked = False

    #     # Load existing data
    #     header, project, agency, financial, location, other = get_project(project_id)
        
    #     # Check if the current user is the owner of the project
    #     project_owner = header[2]  # created_by from database
    #     current_user = st.session_state.username
    #     is_owner = project_owner == current_user

    #     if not is_owner:
    #         st.error("You are not authorized to update this project. Only the project owner can update it.")
    #     else:
    #         # Tabs for Data Entry
    #         project_data, agency_data, financial_data, location_data, other_data = {}, {}, {}, {}, {}
    #         tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
            
    #         with tabs[0]:
    #             project_data = project_details_tab(project_data=project)
    #         with tabs[1]:
    #             agency_data = agency_details_tab(agency_data=agency)
    #         with tabs[2]:
    #             financial_data = financial_details_tab(financial_data=financial)
    #         with tabs[3]:
    #             location_data = location_beneficiary_tab(location_data=location)
    #         with tabs[4]:
    #             other_data = other_information_tab(other_data=other)

    #         # Handle Update Project button click (logic in main content area)
    #         if st.session_state.update_project_clicked:
    #             if not financial_data["company_code"]:
    #                 st.error("Company Code in Financial Details is mandatory.")
    #             else:
    #                 try:
    #                     created_by = st.session_state.username
    #                     created_on = "2025-03-28"
    #                     status = header[4]
    #                     save_project(project_id, project_portal_id, created_by, created_on, status,
    #                                  project_data, agency_data, financial_data, location_data, other_data)
    #                     st.success("Project Updated Successfully!")
    #                     st.session_state.current_page = "dashboard"
    #                     st.session_state.selected_project = None
    #                     st.session_state.update_project_clicked = False
    #                     st.rerun()
    #                 except Exception as e:
    #                     st.error(f"Error updating project: {e}")
    #                     st.session_state.update_project_clicked = False


    # # elif st.session_state.current_page == "update":
    #     st.title(f"Update Project: {st.session_state.selected_project}")
    #     project_id = st.session_state.selected_project

    #     # Initialize update_project_clicked in session state
    #     if 'update_project_clicked' not in st.session_state:
    #         st.session_state.update_project_clicked = False

    #     # Load existing data
    #     header, project, agency, financial, location, other = get_project(project_id)

    #     # Convert raw tuples to dicts if needed
    #     def to_dict(keys, data):
    #         return dict(zip(keys, data)) if isinstance(data, tuple) else data

    #     project = to_dict(PROJECT_KEYS, project)
    #     agency = to_dict(AGENCY_KEYS, agency)
    #     financial = to_dict(FINANCIAL_KEYS, financial)
    #     location = to_dict(LOCATION_KEYS, location)
    #     other = to_dict(OTHER_KEYS, other)

    #     # Check if the current user is the owner of the project
    #     project_owner = header[2]  # created_by from database
    #     current_user = st.session_state.username
    #     is_owner = project_owner == current_user

    #     if not is_owner:
    #         st.error("You are not authorized to update this project. Only the project owner can update it.")
    #     else:
    #         # Tabs for Data Entry
    #         project_data, agency_data, financial_data, location_data, other_data = {}, {}, {}, {}, {}
    #         tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])

    #         with tabs[0]:
    #             from datetime import datetime

    #             def parse_date(val):
    #                 try:
    #                     return datetime.strptime(val, "%Y-%m-%d").date() if isinstance(val, str) else val
    #                 except Exception:
    #                     return datetime.today().date()

    #             project["start_date"] = parse_date(project.get("start_date"))
    #             project["end_date"] = parse_date(project.get("end_date"))

                
    #             project_data = project_details_tab(project_data=project)
    #         with tabs[1]:
    #             agency_data = agency_details_tab(agency_data=agency)
    #         with tabs[2]:
    #             financial_data = financial_details_tab(financial_data=financial)
    #         with tabs[3]:
    #             location_data = location_beneficiary_tab(location_data=location)
    #         with tabs[4]:
    #             other_data = other_information_tab(other_data=other)

    #         # Handle Update Project button click (logic in main content area)
    #         if st.session_state.update_project_clicked:
    #             if not financial_data.get("company_code"):
    #                 st.error("Company Code in Financial Details is mandatory.")
    #             else:
    #                 try:
    #                     created_by = st.session_state.username
    #                     created_on = date.today()
    #                     status = header[4]  # Assuming this is the current status
    #                     save_project(project_id, project_portal_id, created_by, created_on, status,
    #                                 project_data, agency_data, financial_data, location_data, other_data)
    #                     st.success("Project Updated Successfully!")
    #                     st.session_state.current_page = "dashboard"
    #                     st.session_state.selected_project = None
    #                     st.session_state.update_project_clicked = False
    #                     st.rerun()
    #                 except Exception as e:
    #                     st.error(f"Error updating project: {e}")
    #                     st.session_state.update_project_clicked = False

    #     # elif st.session_state.current_page == "update":
    #         st.title(f"Update Project: {st.session_state.selected_project}")
    #         project_id = st.session_state.selected_project

    #         # Load existing data
    #         header, project, agency, financial, location, other = get_project(project_id)
            
    #         # Check authorization
    #         project_owner = header[2] if header[2] else "Unknown"
    #         current_user = st.session_state.username
    #         is_owner = project_owner == current_user
    #         is_approver = st.session_state.is_approver
            
    #         if not (is_owner or is_approver):
    #             st.error("You are not authorized to update this project. Only the project owner or an approver can update it.")
    #         elif header[4] == "Approved" and not is_approver:
    #             st.error("Approved projects can only be updated by approvers.")
    #         else:
    #             # Convert tuples to dictionaries
    #             project_dict = {
    #                 "project_name": project[1] or "",
    #                 "disha_file_1": project[2] or "",
    #                 "disha_file_2": project[3] or "",
    #                 "disha_file_3": project[4] or "",
    #                 "moa_signed": project[5] or "Yes",
    #                 "moa_date": project[6],
    #                 "moa_validity": project[7] or 0,
    #                 "execution_validity": project[8] or 0,
    #                 "screening_committee": project[9] or "No",
    #                 "schedule_7": project[10] or "I0001",
    #                 "commencement_date": project[11],
    #                 "end_date": project[12],
    #                 "duration": project[13] or "0",
    #                 "mode_implementation": project[14] or "Own",
    #                 "execution_end_date": project[15],
    #                 "milestones": project[16] or 0,
    #                 "focused_category": project[17] or "Category A"
    #             }
    #             agency_dict = {
    #                 "vendor_no": agency[1] or "",
    #                 "csr1_reg_no": agency[2] or "",
    #                 "agency_type": agency[3] or "Registered Society",
    #                 "pan_no": agency[4] or "",
    #                 "gstn_no": agency[5] or "",
    #                 "reg_active": agency[6] or "Yes",
    #                 "accounts_audited": agency[7] or "Yes",
    #                 "bye_laws": agency[8] or "Yes",
    #                 "admin_cost": agency[9] or 0.0,
    #                 "gst_amount": agency[10] or 0.0,
    #                 "total_cost": agency[11] or 0.0
    #             }
    #             financial_dict = {
    #                 "bdp_name": financial[1] or "",
    #                 "company_code": financial[2] or "",
    #                 "amount_applied": financial[3] or 0.0,
    #                 "amount_approved": financial[4] or 0.0,
    #                 "total_cost": financial[5] or 0.0,
    #                 "first_pay_date": financial[6]
    #             }
    #             location_dict = {
    #                 "operational_area": location[1] or "Yes",
    #                 "plan_campaign": location[2] or "SWACHHTA ACTION PLAN",
    #                 "plan_campaign_other": location[3] or "",
    #                 "activity": location[4] or "",
    #                 "all_india": location[5] or "Yes",
    #                 "districts_impacted": location[6] or 1,
    #                 "pin_codes": location[7] or []
    #             }
    #             other_dict = {
    #                 "fpr_cpf": other[1] or "",
    #                 "project_ref": other[2] or "None",
    #                 "ref_name": other[3] or "",
    #                 "designation": other[4] or "",
    #                 "beneficiaries": other[5] or 1,
    #                 "direct_beneficiaries": other[6] or 0,
    #                 "indirect_beneficiaries": other[7] or 0,
    #                 "obc_percent": other[8] or 0,
    #                 "scst_percent": other[9] or 0,
    #                 "divyang_percent": other[10] or 0,
    #                 "women_percent": other[11] or 0,
    #                 "ews_percent": other[12] or 0
    #             }

    #             with st.form("update_project_form"):
    #                 tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
                    
    #                 with tabs[0]:
    #                     from datetime import datetime

    #                     def parse_date(val):
    #                         if val and isinstance(val, (datetime.date, datetime.datetime)):
    #                             return val
    #                         try:
    #                             return datetime.strptime(str(val), "%Y-%m-%d").date() if val else None
    #                         except (ValueError, TypeError):
    #                             return None

    #                     project_dict["moa_date"] = parse_date(project_dict["moa_date"])
    #                     project_dict["commencement_date"] = parse_date(project_dict["commencement_date"])
    #                     project_dict["end_date"] = parse_date(project_dict["end_date"])
    #                     project_dict["execution_end_date"] = parse_date(project_dict["execution_end_date"])
                        
    #                     project_data = project_details_tab(project_dict)
    #                 with tabs[1]:
    #                     agency_data = agency_details_tab(agency_dict)
    #                 with tabs[2]:
    #                     financial_dict["first_pay_date"] = parse_date(financial_dict["first_pay_date"])
    #                     financial_data = financial_details_tab(financial_dict, gst_amount=agency_dict["gst_amount"])
    #                 with tabs[3]:
    #                     location_data = location_beneficiary_tab(location_dict)
    #                 with tabs[4]:
    #                     other_data = other_information_tab(other_dict)
                    
    #                 confirm_update = st.checkbox("Confirm update")
    #                 submitted = st.form_submit_button("Update Project")
                    
    #                 if submitted:
    #                     if not confirm_update:
    #                         st.error("Please confirm the update by checking the box.")
    #                     elif not financial_data.get("company_code"):
    #                         st.error("Company Code in Financial Details is mandatory.")
    #                     elif not project_data.get("project_name") or not project_data.get("disha_file_1") or (project_data.get("moa_signed") == "Yes" and not project_data.get("moa_date")):
    #                         st.error("Please fill all mandatory fields in Project Details.")
    #                     elif not agency_data.get("vendor_no") or not agency_data.get("csr1_reg_no") or not agency_data.get("agency_type"):
    #                         st.error("Please fill all mandatory fields in Agency Details.")
    #                     elif not financial_data.get("amount_applied") or not financial_data.get("amount_approved") or not financial_data.get("total_cost") or not financial_data.get("first_pay_date"):
    #                         st.error("Please fill all mandatory fields in Financial Details.")
    #                     elif financial_data.get("amount_applied") <= financial_data.get("amount_approved") and (financial_data.get("amount_applied") != 0.0 or financial_data.get("amount_approved") != 0.0):
    #                         st.error("Amount Applied must be greater than Amount Approved.")
    #                     elif not location_data.get("plan_campaign") or not location_data.get("activity") or not location_data.get("districts_impacted"):
    #                         st.error("Please fill all mandatory fields in Location/Beneficiary.")
    #                     elif not other_data.get("project_ref") or not other_data.get("ref_name") or not other_data.get("designation") or not other_data.get("beneficiaries"):
    #                         st.error("Please fill all mandatory fields in Other Information.")
    #                     else:
    #                         try:
    #                             created_by = header[2]  # Preserve original created_by
    #                             created_on = header[3]  # Preserve original created_on
    #                             status = header[4]
    #                             project_portal_id = st.session_state.project_portal_id
    #                             save_project(project_id, project_portal_id, created_by, created_on, status,
    #                                         project_data, agency_data, financial_data, location_data, other_data)
    #                             st.success("Project Updated Successfully!")
    #                             st.session_state.current_page = "dashboard"
    #                             st.session_state.selected_project = None
    #                             st.session_state.project_portal_id = ""
    #                             st.rerun()
    #                         except ValueError as ve:
    #                             st.error(f"Validation error: {ve}")
    #                         except Exception as e:
    #                             st.error(f"An unexpected error occurred: {e}")

        # elif st.session_state.current_page == "update":
        #     st.title(f"Update Project: {st.session_state.selected_project}")
        #     project_id = st.session_state.selected_project

        #     # Import datetime at the start of the update section
        #     import datetime

        #     # Load existing data
        #     header, project, agency, financial, location, other = get_project(project_id)
            
        #     # Check authorization
        #     project_owner = header[2] if header[2] else "Unknown"
        #     current_user = st.session_state.username
        #     is_owner = project_owner == current_user
        #     is_approver = st.session_state.is_approver
            
        #     if not (is_owner or is_approver):
        #         st.error("You are not authorized to update this project. Only the project owner or an approver can update it.")
        #     elif header[4] == "Approved" and not is_approver:
        #         st.error("Approved projects can only be updated by approvers.")
        #     else:
        #         # Convert tuples to dictionaries
        #         project_dict = {
        #             "project_name": project[1] or "",
        #             "disha_file_1": project[2] or "",
        #             "disha_file_2": project[3] or "",
        #             "disha_file_3": project[4] or "",
        #             "moa_signed": project[5] or "Yes",
        #             "moa_date": project[6],
        #             "moa_validity": project[7] or 0,
        #             "execution_validity": project[8] or 0,
        #             "screening_committee": project[9] or "No",
        #             "schedule_7": project[10] or "I0001",
        #             "commencement_date": project[11],
        #             "end_date": project[12],
        #             "duration": project[13] or "0",
        #             "mode_implementation": project[14] or "Own",
        #             "execution_end_date": project[15],
        #             "milestones": project[16] or 0,
        #             "focused_category": project[17] or "Category A"
        #         }
        #         agency_dict = {
        #             "vendor_no": agency[1] or "",
        #             "csr1_reg_no": agency[2] or "",
        #             "agency_type": agency[3] or "Registered Society",
        #             "pan_no": agency[4] or "",
        #             "gstn_no": agency[5] or "",
        #             "reg_active": agency[6] or "Yes",
        #             "accounts_audited": agency[7] or "Yes",
        #             "bye_laws": agency[8] or "Yes",
        #             "admin_cost": agency[9] or 0.0,
        #             "gst_amount": agency[10] or 0.0,
        #             "total_cost": agency[11] or 0.0
        #         }
        #         financial_dict = {
        #             "bdp_name": financial[1] or "",
        #             "company_code": financial[2] or "",
        #             "amount_applied": financial[3] or 0.0,
        #             "amount_approved": financial[4] or 0.0,
        #             "total_cost": financial[5] or 0.0,
        #             "first_pay_date": financial[6]
        #         }
        #         location_dict = {
        #             "operational_area": location[1] or "Yes",
        #             "plan_campaign": location[2] or "SWACHHTA ACTION PLAN",
        #             "plan_campaign_other": location[3] or "",
        #             "activity": location[4] or "",
        #             "all_india": location[5] or "Yes",
        #             "districts_impacted": location[6] or 1,
        #             "pin_codes": location[7] or []
        #         }
        #         other_dict = {
        #             "fpr_cpf": other[1] or "",
        #             "project_ref": other[2] or "None",
        #             "ref_name": other[3] or "",
        #             "designation": other[4] or "",
        #             "beneficiaries": other[5] or 1,
        #             "direct_beneficiaries": other[6] or 0,
        #             "indirect_beneficiaries": other[7] or 0,
        #             "obc_percent": other[8] or 0,
        #             "scst_percent": other[9] or 0,
        #             "divyang_percent": other[10] or 0,
        #             "women_percent": other[11] or 0,
        #             "ews_percent": other[12] or 0
        #         }

        #         # Define parse_date function
        #         def parse_date(val):
        #             if val and isinstance(val, (datetime.date, datetime.datetime)):
        #                 return val
        #             try:
        #                 return datetime.datetime.strptime(str(val), "%Y-%m-%d").date() if val else None
        #             except (ValueError, TypeError):
        #                 return None

        #         # Parse all date fields before passing to tab functions
        #         project_dict["moa_date"] = parse_date(project_dict["moa_date"])
        #         project_dict["commencement_date"] = parse_date(project_dict["commencement_date"])
        #         project_dict["end_date"] = parse_date(project_dict["end_date"])
        #         project_dict["execution_end_date"] = parse_date(project_dict["execution_end_date"])
        #         financial_dict["first_pay_date"] = parse_date(financial_dict["first_pay_date"])

        #         with st.form("update_project_form"):
        #             st.sidebar.header("Project Header")
        #             project_portal_id = st.sidebar.text_input("Project Portal ID", value=st.session_state.project_portal_id, max_chars=15, key="update_project_portal_id")
        #             st.session_state.project_portal_id = project_portal_id
        #             # Add unique key for Project ID input
        #             st.sidebar.text_input("Project ID", value=project_id, disabled=True, key="update_project_id")
        #             # Add unique keys for other inputs to prevent future conflicts
        #             st.sidebar.text_input("Created By", value=header[2], disabled=True, key="update_created_by")
        #             st.sidebar.text_input("Created On", value=str(header[3]), disabled=True, key="update_created_on")
        #             st.sidebar.selectbox("Status", [header[4]], disabled=True, key="update_status")

        #             tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
                    
        #             with tabs[0]:
        #                 project_data = project_details_tab(project_dict)
        #             with tabs[1]:
        #                 agency_data = agency_details_tab(agency_dict)
        #             with tabs[2]:
        #                 financial_data = financial_details_tab(financial_dict, gst_amount=agency_dict["gst_amount"])
        #             with tabs[3]:
        #                 location_data = location_beneficiary_tab(location_dict)
        #             with tabs[4]:
        #                 other_data = other_information_tab(other_dict)
                    
        #             confirm_update = st.checkbox("Confirm update")
        #             submitted = st.form_submit_button("Update Project")
                    
        #             if submitted:
        #                 if not confirm_update:
        #                     st.error("Please confirm the update by checking the box.")
        #                 elif not financial_data.get("company_code"):
        #                     st.error("Company Code in Financial Details is mandatory.")
        #                 elif not project_data.get("project_name") or not project_data.get("disha_file_1") or (project_data.get("moa_signed") == "Yes" and not project_data.get("moa_date")):
        #                     st.error("Please fill all mandatory fields in Project Details.")
        #                 elif not agency_data.get("vendor_no") or not agency_data.get("csr1_reg_no") or not agency_data.get("agency_type"):
        #                     st.error("Please fill all mandatory fields in Agency Details.")
        #                 elif not financial_data.get("amount_applied") or not financial_data.get("amount_approved") or not financial_data.get("total_cost") or not financial_data.get("first_pay_date"):
        #                     st.error("Please fill all mandatory fields in Financial Details.")
        #                 elif financial_data.get("amount_applied") <= financial_data.get("amount_approved") and (financial_data.get("amount_applied") != 0.0 or financial_data.get("amount_approved") != 0.0):
        #                     st.error("Amount Applied must be greater than Amount Approved.")
        #                 elif not location_data.get("plan_campaign") or not location_data.get("activity") or not location_data.get("districts_impacted"):
        #                     st.error("Please fill all mandatory fields in Location/Beneficiary.")
        #                 elif not other_data.get("project_ref") or not other_data.get("ref_name") or not other_data.get("designation") or not other_data.get("beneficiaries"):
        #                     st.error("Please fill all mandatory fields in Other Information.")
        #                 else:
        #                     try:
        #                         created_by = header[2]  # Preserve original created_by
        #                         created_on = header[3]  # Preserve original created_on
        #                         status = header[4]
        #                         project_portal_id = st.session_state.project_portal_id
        #                         save_project(project_id, project_portal_id, created_by, created_on, status,
        #                                     project_data, agency_data, financial_data, location_data, other_data)
        #                         st.success("Project Updated Successfully!")
        #                         st.session_state.current_page = "dashboard"
        #                         st.session_state.selected_project = None
        #                         st.session_state.project_portal_id = ""
        #                         st.rerun()
        #                     except ValueError as ve:
        #                         st.error(f"Validation error: {ve}")
        #                     except Exception as e:
        #                         st.error(f"An unexpected error occurred: {e}")


    elif st.session_state.current_page == "update":
        st.title(f"Update Project: {st.session_state.selected_project}")
        project_id = st.session_state.selected_project

        # Import datetime at the start of the update section
        import datetime

        # Load existing data
        header, project, agency, financial, location, other = get_project(project_id)
        
        # Check authorization
        project_owner = header[2] if header[2] else "Unknown"
        current_user = st.session_state.username
        is_owner = project_owner == current_user
        is_approver = st.session_state.is_approver
        
        if not (is_owner or is_approver):
            st.error("You are not authorized to update this project. Only the project owner or an approver can update it.")
        elif header[4] == "Approved" and not is_approver:
            st.error("Approved projects can only be updated by approvers.")
        else:
            # Convert tuples to dictionaries
            project_dict = {
                "project_name": project[1] or "",
                "disha_file_1": project[2] or "",
                "disha_file_2": project[3] or "",
                "disha_file_3": project[4] or "",
                "moa_signed": project[5] or "Yes",
                "moa_date": project[6],
                "moa_validity": project[7] or 0,
                "execution_validity": project[8] or 0,
                "screening_committee": project[9] or "No",
                "schedule_7": project[10] or "I0001",
                "commencement_date": project[11],
                "end_date": project[12],
                "duration": project[13] or "0",
                "mode_implementation": project[14] or "Own",
                "execution_end_date": project[15],
                "milestones": project[16] or 0,
                "focused_category": project[17] or "Category A"
            }
            agency_dict = {
                "vendor_no": agency[1] or "",
                "csr1_reg_no": agency[2] or "",
                "agency_type": agency[3] or "Registered Society",
                "pan_no": agency[4] or "",
                "gstn_no": agency[5] or "",
                "reg_active": agency[6] or "Yes",
                "accounts_audited": agency[7] or "Yes",
                "bye_laws": agency[8] or "Yes",
                "admin_cost": agency[9] or 0.0,
                "gst_amount": agency[10] or 0.0,
                "total_cost": agency[11] or 0.0
            }
            financial_dict = {
                "bdp_name": financial[1] or "",
                "company_code": financial[2] or "",
                "amount_applied": financial[3] or 0.0,
                "amount_approved": financial[4] or 0.0,
                "total_cost": financial[5] or 0.0,
                "first_pay_date": financial[6]
            }
            location_dict = {
                "operational_area": location[1] or "Yes",
                "plan_campaign": location[2] or "SWACHHTA ACTION PLAN",
                "plan_campaign_other": location[3] or "",
                "activity": location[4] or "",
                "all_india": location[5] or "Yes",
                "districts_impacted": location[6] or 1,
                "pin_codes": location[7] or []
            }
            other_dict = {
                "fpr_cpf": other[1] or "",
                "project_ref": other[2] or "None",
                "ref_name": other[3] or "",
                "designation": other[4] or "",
                "beneficiaries": other[5] or 1,
                "direct_beneficiaries": other[6] or 0,
                "indirect_beneficiaries": other[7] or 0,
                "obc_percent": other[8] or 0,
                "scst_percent": other[9] or 0,
                "divyang_percent": other[10] or 0,
                "women_percent": other[11] or 0,
                "ews_percent": other[12] or 0
            }

            # Define parse_date function
            def parse_date(val):
                if val and isinstance(val, (datetime.date, datetime.datetime)):
                    return val
                try:
                    return datetime.datetime.strptime(str(val), "%Y-%m-%d").date() if val else None
                except (ValueError, TypeError):
                    return None

            # Parse all date fields before passing to tab functions
            project_dict["moa_date"] = parse_date(project_dict["moa_date"])
            project_dict["commencement_date"] = parse_date(project_dict["commencement_date"])
            project_dict["end_date"] = parse_date(project_dict["end_date"])
            project_dict["execution_end_date"] = parse_date(project_dict["execution_end_date"])
            financial_dict["first_pay_date"] = parse_date(financial_dict["first_pay_date"])

            # Move sidebar inputs outside the form to avoid form context issues
            st.sidebar.header("Project Header")
            project_portal_id = st.sidebar.text_input("Project Portal ID", value=st.session_state.project_portal_id, max_chars=15, key="update_project_portal_id")
            st.session_state.project_portal_id = project_portal_id
            st.sidebar.text_input("Project ID", value=project_id, disabled=True, key="update_project_id")
            st.sidebar.text_input("Created By", value=header[2], disabled=True, key="update_created_by")
            st.sidebar.text_input("Created On", value=str(header[3]), disabled=True, key="update_created_on")
            st.sidebar.selectbox("Status", [header[4]], disabled=True, key="update_status")

            with st.form("update_project_form"):
                tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
                
                with tabs[0]:
                    project_data = project_details_tab(project_dict)
                with tabs[1]:
                    agency_data = agency_details_tab(agency_dict)
                with tabs[2]:
                    financial_data = financial_details_tab(financial_dict, gst_amount=agency_dict["gst_amount"])
                with tabs[3]:
                    location_data = location_beneficiary_tab(location_dict)
                with tabs[4]:
                    other_data = other_information_tab(other_dict)
                
                confirm_update = st.checkbox("Confirm update")
                
                # Add submit button here
                submitted = st.form_submit_button("Update Project")
                
                if submitted:
                    if not confirm_update:
                        st.error("Please confirm the update by checking the box.")
                    elif not financial_data.get("company_code"):
                        st.error("Company Code in Financial Details is mandatory.")
                    elif not project_data.get("project_name") or not project_data.get("disha_file_1") or (project_data.get("moa_signed") == "Yes" and not project_data.get("moa_date")):
                        st.error("Please fill all mandatory fields in Project Details.")
                    elif not agency_data.get("vendor_no") or not agency_data.get("csr1_reg_no") or not agency_data.get("agency_type"):
                        st.error("Please fill all mandatory fields in Agency Details.")
                    elif not financial_data.get("amount_applied") or not financial_data.get("amount_approved") or not financial_data.get("total_cost") or not financial_data.get("first_pay_date"):
                        st.error("Please fill all mandatory fields in Financial Details.")
                    elif financial_data.get("amount_applied") <= financial_data.get("amount_approved") and (financial_data.get("amount_applied") != 0.0 or financial_data.get("amount_approved") != 0.0):
                        st.error("Amount Applied must be greater than Amount Approved.")
                    elif not location_data.get("plan_campaign") or not location_data.get("activity") or not location_data.get("districts_impacted"):
                        st.error("Please fill all mandatory fields in Location/Beneficiary.")
                    elif not other_data.get("project_ref") or not other_data.get("ref_name") or not other_data.get("designation") or not other_data.get("beneficiaries"):
                        st.error("Please fill all mandatory fields in Other Information.")
                    else:
                        try:
                            created_by = header[2]  # Preserve original created_by
                            created_on = header[3]  # Preserve original created_on
                            status = header[4]
                            project_portal_id = st.session_state.project_portal_id
                            save_project(project_id, project_portal_id, created_by, created_on, status,
                                        project_data, agency_data, financial_data, location_data, other_data)
                            st.success("Project Updated Successfully!")
                            st.session_state.current_page = "dashboard"
                            st.session_state.selected_project = None
                            st.session_state.project_portal_id = ""
                            st.rerun()
                        except ValueError as ve:
                            st.error(f"Validation error: {ve}")
                        except Exception as e:
                            st.error(f"An unexpected error occurred: {e}")

    
    # Delete Project Screen
    elif st.session_state.current_page == "delete_select":
        st.title("Select Project to Delete")
        projects = get_all_projects()
        if projects:
            # Display project details including the owner
            project_data = {
                "Project ID": [p[0] for p in projects],
                "Created By": [p[2] for p in projects],
                "Project Name": [p[5] for p in projects],
                "Status": [p[4] for p in projects]
            }
            st.table(project_data)

        project_ids = [p[0] for p in projects]
        selected_project = st.selectbox("Select Project", project_ids)
        
        if st.button("Delete"):
            # Fetch project details to check ownership
            header, *_ = get_project(selected_project)
            project_owner = header[2]  # created_by from database
            current_user = st.session_state.username
            is_owner = project_owner == current_user

            if not is_owner:
                st.error("You are not authorized to delete this project. Only the project owner can delete it.")
            else:
                delete_project(selected_project)
                st.success("Project Deleted Successfully!")
                st.session_state.current_page = "dashboard"
                st.rerun()
                
        if st.button("Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # Approve Project Screen
    elif st.session_state.current_page == "approve_select":
        st.title("Select Project to Approve")
        projects = get_all_projects()
        project_ids = [p[0] for p in projects if p[4] == "Saved"]
        selected_project = st.selectbox("Select Project", project_ids)
        if st.button("Approve"):
            update_status(selected_project, "Approved")
            st.success("Project Approved Successfully!")
            st.session_state.current_page = "dashboard"
            st.rerun()
        if st.button("Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # Enhanced ALV-Like Report Screen
    elif st.session_state.current_page == "report":
        st.title("Project Report (ALV-Like)")
        projects = get_all_projects()
        
        if projects:
            # Prepare data for DataFrame
            data = {
                "Project ID": [p[0] for p in projects],
                "Portal ID": [p[1] for p in projects],
                "Created By": [p[2] for p in projects],
                "Created On": [p[3] for p in projects],
                "Status": [p[4] for p in projects],
                "Project Name": [p[5] for p in projects],
                "MoA Signed": [p[6] for p in projects],
                "MoA Date": [p[7] for p in projects],
                "Execution Validity (Months)": [p[8] for p in projects],
                "Schedule 7": [p[9] for p in projects],
                "Commencement Date": [p[10] for p in projects],
                "End Date": [p[11] for p in projects],
                "Duration": [p[12] for p in projects],
                "Mode of Implementation": [p[13] for p in projects],
                "Milestones": [p[14] for p in projects],
                "Focused Category": [p[15] for p in projects],
                "Vendor No": [p[16] for p in projects],
                "CSR-1 Reg No": [p[17] for p in projects],
                "Agency Type": [p[18] for p in projects],
                "Total Cost (Agency)": [p[19] for p in projects],
                "Company Code": [p[20] for p in projects],
                "BDP Name": [p[21] for p in projects],
                "Amount Applied": [p[22] for p in projects],
                "Amount Approved": [p[23] for p in projects],
                "Total Cost (Financial)": [p[24] for p in projects],
                "First Payment Date": [p[25] for p in projects],
                "Operational Area": [p[26] for p in projects],
                "Plan/Campaign": [p[27] for p in projects],
                "Activity": [p[28] for p in projects],
                "All India": [p[29] for p in projects],
                "Districts Impacted": [p[30] for p in projects],
                "PIN Codes": [p[31] for p in projects],
                "FPR CPF": [p[32] for p in projects],
                "Project Reference": [p[33] for p in projects],
                "Reference Name": [p[34] for p in projects],
                "Beneficiaries": [p[35] for p in projects],
                "Direct Beneficiaries": [p[36] for p in projects],
                "Indirect Beneficiaries": [p[37] for p in projects],
                "OBC %": [p[38] for p in projects],
                "Women %": [p[39] for p in projects]
            }
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Add Filtering Options
            st.subheader("Filter Report")
            status_filter = st.multiselect("Filter by Status", options=df["Status"].unique(), default=df["Status"].unique())
            project_name_filter = st.text_input("Filter by Project Name (contains)")

            # Apply Filters
            filtered_df = df[df["Status"].isin(status_filter)]
            if project_name_filter:
                filtered_df = filtered_df[filtered_df["Project Name"].str.contains(project_name_filter, case=False, na=False)]

            # Display Interactive DataFrame
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("No projects found.")
        
        if st.button("Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()