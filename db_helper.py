import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Get database connection details from environment variables
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn
    except Exception as e:
        raise Exception(f"Error connecting to database: {e}")

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Create Users Table (with approver status)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(50),
                is_approver BOOLEAN DEFAULT FALSE
            );
        """)
        # Insert default users (admin is an approver, user1 is not)
        cursor.execute("""
            INSERT INTO users (username, password, is_approver)
            VALUES ('admin', 'admin123', TRUE),
                   ('user1', 'user123', FALSE)
            ON CONFLICT (username) DO NOTHING;
        """)

        # Create Project Counter Table for Incremental project_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_counter (
                year VARCHAR(4) PRIMARY KEY,
                counter INTEGER DEFAULT 1
            );
        """)
        cursor.execute("""
            INSERT INTO project_counter (year, counter)
            VALUES ('2025', 1)
            ON CONFLICT (year) DO NOTHING;
        """)

        # Create Header Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS csr_project_header (
                project_id VARCHAR(15) PRIMARY KEY,
                project_portal_id VARCHAR(15),
                created_by VARCHAR(50),
                created_on DATE,
                status VARCHAR(20)
            );
        """)

        # Create Project Details Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_details (
                project_id VARCHAR(15) PRIMARY KEY,
                project_name VARCHAR(100),
                disha_file_1 VARCHAR(250),
                disha_file_2 VARCHAR(250),
                disha_file_3 VARCHAR(250),
                moa_signed VARCHAR(3),
                moa_date DATE,
                moa_validity INTEGER,
                execution_validity INTEGER,
                screening_committee VARCHAR(3),
                schedule_7 VARCHAR(50),
                commencement_date DATE,
                end_date DATE,
                duration VARCHAR(10),
                mode_implementation VARCHAR(10),
                execution_end_date DATE,
                milestones INTEGER,
                focused_category VARCHAR(50)
            );
        """)

        # Create Agency Details Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agency_details (
                project_id VARCHAR(15) PRIMARY KEY,
                vendor_no VARCHAR(10),
                csr1_reg_no VARCHAR(25),
                agency_type VARCHAR(50),
                pan_no VARCHAR(10),
                gstn_no VARCHAR(18),
                reg_active VARCHAR(3),
                accounts_audited VARCHAR(3),
                bye_laws VARCHAR(3),
                admin_cost DECIMAL,
                gst_amount DECIMAL,
                total_cost DECIMAL
            );
        """)

        # Create Financial Details Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_details (
                project_id VARCHAR(15) PRIMARY KEY,
                bdp_name VARCHAR(14),
                company_code VARCHAR(4),
                amount_applied DECIMAL,
                amount_approved DECIMAL,
                total_cost DECIMAL,
                first_pay_date DATE
            );
        """)

        # Create Location/Beneficiary Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS location_beneficiary (
                project_id VARCHAR(15) PRIMARY KEY,
                operational_area VARCHAR(3),
                plan_campaign VARCHAR(50),
                plan_campaign_other TEXT,
                activity TEXT,
                all_india VARCHAR(3),
                districts_impacted INTEGER,
                pin_codes JSONB
            );
        """)

        # Create Other Information Table (project_id as primary key)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS other_information (
                project_id VARCHAR(15) PRIMARY KEY,
                fpr_cpf VARCHAR(12),
                project_ref VARCHAR(50),
                ref_name VARCHAR(50),
                designation VARCHAR(50),
                beneficiaries DECIMAL,
                direct_beneficiaries DECIMAL,
                indirect_beneficiaries DECIMAL,
                obc_percent INTEGER,
                scst_percent INTEGER,
                divyang_percent INTEGER,
                women_percent INTEGER,
                ews_percent INTEGER
            );
        """)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT is_approver FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        return user if user else None
    except Exception as e:
        raise Exception(f"Error authenticating user: {e}")
    finally:
        cursor.close()
        conn.close()

def generate_project_id(company_code, year):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT counter FROM project_counter WHERE year = %s FOR UPDATE", (year,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO project_counter (year, counter) VALUES (%s, 1)", (year,))
            counter = 1
        else:
            counter = result[0]
        
        cursor.execute("UPDATE project_counter SET counter = counter + 1 WHERE year = %s", (year,))
        project_id = f"{company_code[:3]}{year}{str(counter).zfill(5)}"
        
        conn.commit()
        return project_id
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error generating project_id: {e}")
    finally:
        cursor.close()
        conn.close()

def save_project(project_id, project_portal_id, created_by, created_on, status, project_data, agency_data, financial_data, location_data, other_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert into Header
        cursor.execute("""
            INSERT INTO csr_project_header (project_id, project_portal_id, created_by, created_on, status)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET project_portal_id = EXCLUDED.project_portal_id,
                created_by = EXCLUDED.created_by,
                created_on = EXCLUDED.created_on,
                status = EXCLUDED.status;
        """, (project_id, project_portal_id, created_by, created_on, status))

        # Insert into Project Details
        cursor.execute("""
            INSERT INTO project_details (
                project_id, project_name, disha_file_1, disha_file_2, disha_file_3,
                moa_signed, moa_date, moa_validity, execution_validity,
                screening_committee, schedule_7, commencement_date, end_date,
                duration, mode_implementation, execution_end_date, milestones,
                focused_category
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET project_name = EXCLUDED.project_name,
                disha_file_1 = EXCLUDED.disha_file_1,
                disha_file_2 = EXCLUDED.disha_file_2,
                disha_file_3 = EXCLUDED.disha_file_3,
                moa_signed = EXCLUDED.moa_signed,
                moa_date = EXCLUDED.moa_date,
                moa_validity = EXCLUDED.moa_validity,
                execution_validity = EXCLUDED.execution_validity,
                screening_committee = EXCLUDED.screening_committee,
                schedule_7 = EXCLUDED.schedule_7,
                commencement_date = EXCLUDED.commencement_date,
                end_date = EXCLUDED.end_date,
                duration = EXCLUDED.duration,
                mode_implementation = EXCLUDED.mode_implementation,
                execution_end_date = EXCLUDED.execution_end_date,
                milestones = EXCLUDED.milestones,
                focused_category = EXCLUDED.focused_category;
        """, (
            project_id, project_data["project_name"], project_data["disha_file_1"], project_data["disha_file_2"],
            project_data["disha_file_3"], project_data["moa_signed"], project_data["moa_date"],
            project_data["moa_validity"], project_data["execution_validity"], project_data["screening_committee"],
            project_data["schedule_7"], project_data["commencement_date"], project_data["end_date"],
            project_data["duration"], project_data["mode_implementation"], project_data["execution_end_date"],
            project_data["milestones"], project_data["focused_category"]
        ))

        # Insert into Agency Details
        cursor.execute("""
            INSERT INTO agency_details (
                project_id, vendor_no, csr1_reg_no, agency_type, pan_no, gstn_no,
                reg_active, accounts_audited, bye_laws, admin_cost, gst_amount, total_cost
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET vendor_no = EXCLUDED.vendor_no,
                csr1_reg_no = EXCLUDED.csr1_reg_no,
                agency_type = EXCLUDED.agency_type,
                pan_no = EXCLUDED.pan_no,
                gstn_no = EXCLUDED.gstn_no,
                reg_active = EXCLUDED.reg_active,
                accounts_audited = EXCLUDED.accounts_audited,
                bye_laws = EXCLUDED.bye_laws,
                admin_cost = EXCLUDED.admin_cost,
                gst_amount = EXCLUDED.gst_amount,
                total_cost = EXCLUDED.total_cost;
        """, (
            project_id, agency_data["vendor_no"], agency_data["csr1_reg_no"], agency_data["agency_type"],
            agency_data["pan_no"], agency_data["gstn_no"], agency_data["reg_active"],
            agency_data["accounts_audited"], agency_data["bye_laws"], agency_data["admin_cost"],
            agency_data["gst_amount"], agency_data["total_cost"]
        ))

        # Insert into Financial Details
        cursor.execute("""
            INSERT INTO financial_details (
                project_id, bdp_name, company_code, amount_applied, amount_approved,
                total_cost, first_pay_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET bdp_name = EXCLUDED.bdp_name,
                company_code = EXCLUDED.company_code,
                amount_applied = EXCLUDED.amount_applied,
                amount_approved = EXCLUDED.amount_approved,
                total_cost = EXCLUDED.total_cost,
                first_pay_date = EXCLUDED.first_pay_date;
        """, (
            project_id, financial_data["bdp_name"], financial_data["company_code"],
            financial_data["amount_applied"], financial_data["amount_approved"],
            financial_data["total_cost"], financial_data["first_pay_date"]
        ))

        # Insert into Location/Beneficiary
        cursor.execute("""
            INSERT INTO location_beneficiary (
                project_id, operational_area, plan_campaign, plan_campaign_other,
                activity, all_india, districts_impacted, pin_codes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET operational_area = EXCLUDED.operational_area,
                plan_campaign = EXCLUDED.plan_campaign,
                plan_campaign_other = EXCLUDED.plan_campaign_other,
                activity = EXCLUDED.activity,
                all_india = EXCLUDED.all_india,
                districts_impacted = EXCLUDED.districts_impacted,
                pin_codes = EXCLUDED.pin_codes;
        """, (
            project_id, location_data["operational_area"], location_data["plan_campaign"],
            location_data["plan_campaign_other"], location_data["activity"], location_data["all_india"],
            location_data["districts_impacted"], Json(location_data["pin_codes"])
        ))

        # Insert into Other Information
        cursor.execute("""
            INSERT INTO other_information (
                project_id, fpr_cpf, project_ref, ref_name, designation,
                beneficiaries, direct_beneficiaries, indirect_beneficiaries,
                obc_percent, scst_percent, divyang_percent, women_percent, ews_percent
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE
            SET fpr_cpf = EXCLUDED.fpr_cpf,
                project_ref = EXCLUDED.project_ref,
                ref_name = EXCLUDED.ref_name,
                designation = EXCLUDED.designation,
                beneficiaries = EXCLUDED.beneficiaries,
                direct_beneficiaries = EXCLUDED.direct_beneficiaries,
                indirect_beneficiaries = EXCLUDED.indirect_beneficiaries,
                obc_percent = EXCLUDED.obc_percent,
                scst_percent = EXCLUDED.scst_percent,
                divyang_percent = EXCLUDED.divyang_percent,
                women_percent = EXCLUDED.women_percent,
                ews_percent = EXCLUDED.ews_percent;
        """, (
            project_id, other_data["fpr_cpf"], other_data["project_ref"], other_data["ref_name"],
            other_data["designation"], other_data["beneficiaries"], other_data["direct_beneficiaries"],
            other_data["indirect_beneficiaries"], other_data["obc_percent"], other_data["scst_percent"],
            other_data["divyang_percent"], other_data["women_percent"], other_data["ews_percent"]
        ))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error saving project: {e}")
    finally:
        cursor.close()
        conn.close()

def get_all_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                h.project_id, h.project_portal_id, h.created_by, h.created_on, h.status,
                p.project_name, p.moa_signed, p.moa_date, p.execution_validity, p.schedule_7, p.commencement_date, p.end_date, p.duration, p.mode_implementation, p.milestones, p.focused_category,
                a.vendor_no, a.csr1_reg_no, a.agency_type, a.total_cost,
                f.company_code, f.bdp_name, f.amount_applied, f.amount_approved, f.total_cost AS financial_total_cost, f.first_pay_date,
                l.operational_area, l.plan_campaign, l.activity, l.all_india, l.districts_impacted, l.pin_codes,
                o.fpr_cpf, o.project_ref, o.ref_name, o.beneficiaries, o.direct_beneficiaries, o.indirect_beneficiaries, o.obc_percent, o.women_percent
            FROM csr_project_header h
            LEFT JOIN project_details p ON h.project_id = p.project_id
            LEFT JOIN agency_details a ON h.project_id = a.project_id
            LEFT JOIN financial_details f ON h.project_id = f.project_id
            LEFT JOIN location_beneficiary l ON h.project_id = l.project_id
            LEFT JOIN other_information o ON h.project_id = o.project_id
            ORDER BY h.created_on DESC;
        """)
        return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Error fetching projects: {e}")
    finally:
        cursor.close()
        conn.close()

def get_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM csr_project_header WHERE project_id = %s", (project_id,))
        header = cursor.fetchone()
        cursor.execute("SELECT * FROM project_details WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()
        cursor.execute("SELECT * FROM agency_details WHERE project_id = %s", (project_id,))
        agency = cursor.fetchone()
        cursor.execute("SELECT * FROM financial_details WHERE project_id = %s", (project_id,))
        financial = cursor.fetchone()
        cursor.execute("SELECT * FROM location_beneficiary WHERE project_id = %s", (project_id,))
        location = cursor.fetchone()
        cursor.execute("SELECT * FROM other_information WHERE project_id = %s", (project_id,))
        other = cursor.fetchone()
        return header, project, agency, financial, location, other
    except Exception as e:
        raise Exception(f"Error fetching project: {e}")
    finally:
        cursor.close()
        conn.close()

def update_status(project_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE csr_project_header SET status = %s WHERE project_id = %s", (status, project_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating status: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM project_details WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM agency_details WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM financial_details WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM location_beneficiary WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM other_information WHERE project_id = %s", (project_id,))
        cursor.execute("DELETE FROM csr_project_header WHERE project_id = %s", (project_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error deleting project: {e}")
    finally:
        cursor.close()
        conn.close()