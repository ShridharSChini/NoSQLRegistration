import streamlit as st
import pandas as pd
from pathlib import Path

def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            st.session_state['user'] = st.session_state["username"]
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        # st.write(st.secrets["passwords"])
        return True

def app():
    try:
        if check_password():
            user = st.session_state["user"]
            dept = user[-3:].upper()

            csv_path = Path(__file__).parent.parent / "students.csv"
            result = pd.read_csv(csv_path)

            csv_file = open(csv_path,"rb")
            st.download_button(label= "Download All Registerd Student of Your Dept.",data=csv_file,file_name="students" + ".csv",mime="text/csv")
            
            no_of_students = 0
            fees_pending = 0
            fees_paid = 0
            header = False
            for j in range(0,len(list(result['branch']))):
                usn,Name,fee_pending,fee_paid,Ph_number,admission_quota,btn = st.columns([1.5,2,2,2,2,1,2],gap="small")
                
                if header == False:
                    header = True
                    with usn:
                        st.markdown("**:red[USN]**")
                        st.write(" ")
                    with Name:
                        st.markdown("**:red[Name]**")
                        st.write(" ")
                    # with branch:
                    #     st.markdown("**:red[Branch]**")
                    #     st.write(" ")

                    with fee_pending:
                        st.markdown("**:red[Fee Pending]**")
                        st.write(" ")
                    with fee_paid:
                        st.markdown("**:red[Fee Paid]**")
                        st.write(" ")
                    # with fee_paid_date:
                    #     st.markdown("**:red[Date]**")
                    #     st.write(" ")
                    with Ph_number:
                        st.markdown("**:red[Ph. No.]**")
                        st.write(" ")
                    # with admission_year:
                    #     st.markdown("**:red[Year]**")
                        st.write(" ")
                    with admission_quota:
                        st.markdown("**:red[Quota]**")
                        st.write(" ")
                    with btn:
                        st.markdown("**:red[Receipt]**")
                        st.write(" ")

                if list(result["branch"])[j] == dept or user == "admin":
                    
                    no_of_students = no_of_students+1

                    with usn:   
                        st.write(str(list(result["usn"])[j]).upper())
                    with Name:
                            st.write((list(result["Name"])[j]).capitalize())
                    # with branch:
                    #         st.write(list(result["branch"])[j])
                    with fee_pending:
                            st.write(str(list(result["fee_pending"])[j]))
                    with fee_paid:
                            st.write(str(list(result["fee_paid"])[j]))
                    # with fee_paid_date:
                    #         st.write(list(result["fee_paid_date"])[j])
                    with Ph_number:
                            st.write(str(list(result["Ph_number"])[j]))
                    # with admission_year:
                    #         st.write(list(result["admission_year"])[j])
                    with admission_quota:
                            st.write(list(result["admission_quota"])[j])
                    with btn:
                        img = open(result["html1"][j],"rb")
                        (st.download_button(label= str(list(result["usn"])[j]).upper(),data=img,file_name=str(list(result["usn"])[j]).upper() + ".png"))
                    
            st.write("Total No. of students : ",len(list(result['fee_pending'])))
            st.write("Fees Pending : ",sum(list(result['fee_pending'])))
            st.write("Fees Pending : ",sum(list(result['fee_paid'])))
    except FileNotFoundError as e:
         st.write("No student has registerd yet",e)