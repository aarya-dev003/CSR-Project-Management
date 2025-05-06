import streamlit as st
import pandas as pd
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
            created_on = "2025-03-28"
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
            created_on = "2025-03-28"
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
    elif st.session_state.current_page == "create":
        st.title("Create New Project")
        
        # Initialize save_project_clicked in session state
        if 'save_project_clicked' not in st.session_state:
            st.session_state.save_project_clicked = False

        # Tabs for Data Entry
        project_data, agency_data, financial_data, location_data, other_data = {}, {}, {}, {}, {}
        tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
        
        with tabs[0]:
            project_data = project_details_tab()
        with tabs[1]:
            agency_data = agency_details_tab()
        with tabs[2]:
            financial_data = financial_details_tab()
        with tabs[3]:
            location_data = location_beneficiary_tab()
        with tabs[4]:
            other_data = other_information_tab()

        # Handle Save Project button click (logic in main content area)
        if st.session_state.save_project_clicked:
            # Validate Mandatory Fields
            if not financial_data["company_code"]:
                st.error("Company Code in Financial Details is mandatory.")
            elif not project_data["project_name"] or not project_data["disha_file_1"] or (project_data["moa_signed"] == "Yes" and not project_data["moa_date"]):
                st.error("Please fill all mandatory fields in Project Details.")
            elif not agency_data["vendor_no"] or not agency_data["csr1_reg_no"] or not agency_data["agency_type"]:
                st.error("Please fill all mandatory fields in Agency Details.")
            elif not financial_data["amount_applied"] or not financial_data["amount_approved"] or not financial_data["total_cost"] or not financial_data["first_pay_date"]:
                st.error("Please fill all mandatory fields in Financial Details.")
            elif not location_data["plan_campaign"] or not location_data["activity"] or not location_data["districts_impacted"]:
                st.error("Please fill all mandatory fields in Location/Beneficiary.")
            elif not other_data["project_ref"] or not other_data["ref_name"] or not other_data["designation"] or not other_data["beneficiaries"]:
                st.error("Please fill all mandatory fields in Other Information.")
            else:
                try:
                    # Generate project_id
                    year = "2025"
                    project_id = generate_project_id(financial_data["company_code"], year)
                    # Change status to "Saved" before saving to the database
                    status = "Saved"
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
    elif st.session_state.current_page == "update":
        st.title(f"Update Project: {st.session_state.selected_project}")
        project_id = st.session_state.selected_project
        
        # Initialize update_project_clicked in session state
        if 'update_project_clicked' not in st.session_state:
            st.session_state.update_project_clicked = False

        # Load existing data
        header, project, agency, financial, location, other = get_project(project_id)
        
        # Check if the current user is the owner of the project
        project_owner = header[2]  # created_by from database
        current_user = st.session_state.username
        is_owner = project_owner == current_user

        if not is_owner:
            st.error("You are not authorized to update this project. Only the project owner can update it.")
        else:
            # Tabs for Data Entry
            project_data, agency_data, financial_data, location_data, other_data = {}, {}, {}, {}, {}
            tabs = st.tabs(["Project Details", "Agency Details", "Financial Details", "Location/Beneficiary", "Other Information"])
            
            with tabs[0]:
                project_data = project_details_tab(project_data=project)
            with tabs[1]:
                agency_data = agency_details_tab(agency_data=agency)
            with tabs[2]:
                financial_data = financial_details_tab(financial_data=financial)
            with tabs[3]:
                location_data = location_beneficiary_tab(location_data=location)
            with tabs[4]:
                other_data = other_information_tab(other_data=other)

            # Handle Update Project button click (logic in main content area)
            if st.session_state.update_project_clicked:
                if not financial_data["company_code"]:
                    st.error("Company Code in Financial Details is mandatory.")
                else:
                    try:
                        created_by = st.session_state.username
                        created_on = "2025-03-28"
                        status = header[4]
                        save_project(project_id, project_portal_id, created_by, created_on, status,
                                     project_data, agency_data, financial_data, location_data, other_data)
                        st.success("Project Updated Successfully!")
                        st.session_state.current_page = "dashboard"
                        st.session_state.selected_project = None
                        st.session_state.update_project_clicked = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating project: {e}")
                        st.session_state.update_project_clicked = False

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