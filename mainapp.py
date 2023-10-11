import pandas as pd
import numpy as np
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os
import pygwalker as pyg
import streamlit.components.v1 as components
from ydata_profiling import ProfileReport


st.set_page_config(
    page_title="StackAi"
)
ti=st.title("StackAi 🔰")
st.write('Developed By [Jagadeesha](https://www.linkedin.com/in/jagadeesha-gowda-6a30382b)')
page=st.selectbox("List of Services",("Select","AI Powered Chat GPT","EMI Calculator","Tax Calculator","Chart's Playground","Data Profiling"))


def main():
    def tax_cal():
        st.title("Tax Calculator 📝")
        income=st.text_input("**Total Income (Rs)**")
        ded_1=st.text_input("**Deduction under 80c**",0)
        ded_2=st.text_input("**Interest on Home Loan**",0)
        ded_3=st.text_input("**Any other exemptions and deduction**",0)
    
        if income == "":
            print ("You did not enter a number.")
        else:
            income = int(income)
    
        if ded_1 == "":
            print ("You did not enter a number.")
        else:
            ded_1 = int(ded_1)
    
        if ded_2 == "":
            print ("You did not enter a number.")
        else:
            ded_2 = int(ded_2)
    
        if ded_3 == "":
            print ("You did not enter a number.")
        else:
            ded_3=int(ded_3)
    
            
    
        def old_tax_cal(income_1):
            if income_1 <= 500000:
                return 0
            elif income_1 <=250000:
                tax=0
            elif income_1 <= 500000:
                tax=(income_1 -250000) * 0.05
            elif income_1 <=1000000:
                tax=12500 +(income_1 - 500000) * 0.2
            else:
                tax=112500 + (income_1 - 1000000)*0.3
            return tax

        def new_tax_cal(income):
            if income <700000:
                return 0
            elif income <=300000:
                tax= 0
            elif income <= 600000:
                tax=(income -300000) * 0.05
            elif income <= 900000:
                tax=15000 + (income -600000)* 0.1
            elif income <=1200000:
                tax=45000 + (income - 900000) * 0.15
            elif income <= 1500000:
                tax=90000 + (income - 1200000) * 0.2
            else:
                tax=150000 + (income - 1500000) * 0.3
            return tax        
        
        ok=st.button("**Calculate Tax**")
        if ok:    
            deduction=(ded_1+ded_2+ded_3)
            if deduction == "":
                print("enter")
            else:
                deduction=int(deduction)
            
            stan_dedcu=50000
            income_1=income - deduction - stan_dedcu
            income_2=income-stan_dedcu
    
            old_tax=old_tax_cal(income_1) 
            new_tax=new_tax_cal(income_2)

            if old_tax == "":
                print("enter")
            else:
                 old_tax=int(old_tax)
        
            if new_tax == "":
                print('enter')
            else:
                new_tax=int(new_tax)
            
            b_tax=income-stan_dedcu-deduction
            n_tax=income-stan_dedcu
            
            final_old_tax=(old_tax * 0.04) 
            final_new_tax=(new_tax * 0.04) 
        
            final_old_tax_1=final_old_tax + old_tax
            final_new_tax_1=final_new_tax + new_tax
        
            a=final_old_tax_1 - final_new_tax_1
            b=final_new_tax_1 - final_old_tax_1
        
            st.subheader("Your Tax Calculation Suammary")
        
            df=pd.DataFrame({"Particulars":['Total Income','Total Dedcutions','Standard Deduction','Final Taxable incme','Tax Amount before Cess','Cess (%)','Final Tax Amount'],
                         "New Tax Regim":[income,0,stan_dedcu,n_tax,new_tax,"4",final_new_tax_1],
                         "Old Tax Regim":[income,deduction,stan_dedcu,b_tax,old_tax,"4",final_old_tax_1]})
        
            df=df.set_index("Particulars")       
            st.table(df)
            if final_old_tax_1 > final_new_tax_1:
                st.write ("***Old Tax Regim having higher tax laiblity","," "if you opted for New Tax Regim you will save Rs.***",(f"{a}"),"/-")
            elif final_old_tax_1 == final_new_tax_1:
                st.write("***Old Tax Regim and New Tax Regim having same tax laiblity","," "You can opt for any regim depend on the Deduction***")
            else:
                st.write("***New Tax Regim having higher tax laiblity","," "if you opted for Old Tax Regim you will save Rs.***",(f"{b}"),"/-")
           
       
           
    def loan_repay():
    
        st.title("Loan EMI Calculator 🏦 ")
        Loan=st.text_input("**Loan Amount**")
        Interest=st.text_input("**Enter Rate of Interest (without %)**")
        Tenor=st.text_input("**Number of months**")
    
        if Loan == "":
            print("You did not enter a number.")
        else:
            Loan = int(Loan)
    
        if Interest == "":
            print("You did not enter a number.")
        else:
            Interest = float(Interest)
    
        if Tenor == "":
            print("You did not enter a number.")
        else:
            Tenor = int(Tenor)
    
    
        genrate=st.button("**Genrate Repayment Schedule**")
        if genrate:
            monthly_rate=(Interest/100)/12 
            monthly_payment=(monthly_rate*Loan)/(1-(1 + monthly_rate)**(-Tenor))
            repayment_schedule=[]
            balance=Loan
            for i in range(Tenor):
                interest=monthly_rate*balance
                principal_paid=monthly_payment - interest
                balance -= principal_paid
                repayment_schedule.append((i+1,monthly_payment,principal_paid,interest,balance))
            print("Payment\tBalance\tPrincipal\tInterest\tPayment")
            for i,(month,monthly_payment,principal_paid,interest,balance)in enumerate (repayment_schedule):
                print(f"{month}\t{monthly_payment:.2f}\t{principal_paid:.2f}\t{interest:.2f}\t{balance:.2f}")
           
            
            columns=['Month','Installment Amount','Principal Payment','Interest Payment','Principal Balance']
            df=pd.DataFrame(repayment_schedule,columns=columns)
            df=df.set_index('Month')
            df['Principal Balance'] = df['Principal Balance'].astype('int64')
            df['Principal Payment'] = df['Principal Payment'].astype('int64')
            df['Interest Payment'] = df['Interest Payment'].astype('int64')
            df['Installment Amount'] = df['Installment Amount'].astype('int64')

        
            st.subheader("Your Loan EMI Calculation Summary")
        
            st.write("***Your Loan Amount:***","Rs.",(f"{Loan}"),"/-")
            st.write("***Rate of Interest:***",(f"{Interest:.2f}"),"%")
            st.write("***Total Tenor :***",(f"{Tenor}"),"Months")
            st.write("***Total Interest Payable  :***","Rs.",(f"{df['Interest Payment'].sum()}"),"/-")
            st.write("***Monthly Installment :***","Rs.",(f"{round(monthly_payment)}"),"/-")
        
            st.subheader("Your Estimated Loan Repayment Schedule")
         
            st.dataframe(df)
        
    def chatbot():
        st.title("AI powered Chat GPT 💬")
        st.markdown('''
         - This may produce inacurate information about people, places, or facts
         - Limited knowledge of world and events after 2021
         
         
         💡 Note: No Sign-in or API key required!
         ''')
            
        EMAIL = "jaga.m.gowda@gmail.com"
        PASSWD = "Jagadeesha@9731"
        
        sign = Login(EMAIL,PASSWD)
        cookies = sign.login()
        
        # Save cookies to the local directory
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)

        
        try:
            sign = Login(EMAIL,PASSWD)
            cookies = sign.loadCookiesFromDir(cookie_path_dir)
        except Exception as e:
            st.error(f"An error occurred during login: {str(e)}")
            st.stop()
    
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Function to generate a response        
        def generate_response(dialogue_history):
                        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
                        response = chatbot.chat(dialogue_history, stream=True)
                        if isinstance(response, str):
                            return response
                        else:
                            return str(response)
        # Accept user input
        if prompt := st.chat_input("Send your query"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Append the dialogue history to the user's prompt
            dialogue_history = "\n".join([message["content"] for message in st.session_state.messages])
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Display assistant response in chat message container
            with st.spinner('Generating response....'):
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    try:
                        for response in generate_response(dialogue_history):
                            full_response += response
                            message_placeholder.markdown(full_response + "▌")
                            sleep(0.01)
                        message_placeholder.markdown(full_response)

                        # Check if there are follow-up questions
                        if "?" in prompt:
                        # Update the chat history with the assistant's response
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            # Clear the chat input box
                            st.session_state.prompt = ""
                            # Set the chat input box value to the assistant's response
                            st.chat_input("Follow-up question", value=full_response)

                        # Update the chat history
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    except Exception as e:
                        st.error(f"An error occurred during response generation: {str(e)}")
                        # Update the chat history with the error message
                        st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})                    
    def charting():
        st.title("Charting the Extraordinary 💹")
        data = st.file_uploader("Choose File only csv/excel")

        if data is not None:
            file_extension = data.name.split(".")[-1].lower()

            if file_extension == "csv":
                data1 = pd.read_csv(data)
            elif file_extension in ["xls","xlsx"]:
                data1 = pd.read_excel(data)
            else:
                st.write("Error:Unsupported file format")
                data1=None
        
            if data1 is not None and not data1.empty:
                ok = st.button("Generate playground")
        
                if ok:
                    profile = pyg.to_html(data1)
                    with st.spinner("Generating Report....\nplease wait...."):
                        st.write("## Report")
                        st.components.v1.html(profile, width=1000, height=1200, scrolling=True)    
    def data_profiling():
        st.title("Data Profiling 📊")
        data = st.file_uploader("Choose File only csv/excel")

        if data is not None:
            file_extension = data.name.split(".")[-1].lower()

            if file_extension == "csv":
                data1 = pd.read_csv(data)
            elif file_extension in ["xls","xlsx"]:
                data1 = pd.read_excel(data)
            else:
                st.write("Error:Unsupported file format")
                data1=None
        
            if data1 is not None and not data1.empty:
                ok = st.button("Generate Report")
        
                if ok:
                    profile = ProfileReport(data1, title="Pandas Profiling Report")
                    with st.spinner("Generating Report....\nplease wait...."):
                        st.write("## Report")
                        st.components.v1.html(profile.to_html(), width=1000, height=1200, scrolling=True)            
    
                          
    if page == "Select":
        st.write("Please select the services")
    elif page == "EMI Calculator":
        loan_repay()
    elif page == "Tax Calculator":
        tax_cal()
    elif page == "AI Powered Chat GPT":
        chatbot()   
    elif page == "Chart's Playground":
        charting()
    else:
        data_profiling()
        
if __name__=='__main__':
    main()