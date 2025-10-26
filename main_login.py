import sqlite3
import bcrypt
import streamlit as st
def algo_add():
    with st.expander("Add_data"):
        placeholder = st.empty()
        with placeholder.form("Algo_data_entry"):
            st.markdown("#### Enter your credentials")
            username = st.text_input("username")
            password = st.text_input("Password", type="password")
            n_algo = st.text_input("Nifty_algo")
            b_algo = st.text_input("Banknifty_algo")
            f_algo = st.text_input("Finifty_algo")
            stk1_algo = st.text_input("Stock1_algo")
            stk2_algo = st.text_input("Stock2_algo")
            stk3_algo = st.text_input("Stock3_algo")
            stk4_algo = st.text_input("Stock4_algo")
            submit = st.form_submit_button("registration")
            if submit == True:
                st.success("Registration successful!")
                st.info(f"Username: {username}")
                create_database()
                create_data(username, password,n_algo,b_algo,f_algo,stk1_algo,stk2_algo,stk3_algo,stk4_algo)
def algo_del():
    with st.expander("Delete_data"):
        placeholder = st.empty()
        with placeholder.form("Algo_data_entry"):
            username = st.text_input("username")
            submit = st.form_submit_button("registration")
            if submit == True:
                st.success("data deleted")
                st.info(f"Username: {username}")
                delete_main_1(username)
# Function to hash and salt a password
def create_database():
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    c.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='main_1'
    """)
    if not c.fetchone():
        c.execute('''CREATE TABLE IF NOT EXISTS main_1
                     (username TEXT, password TEXT, nf TEXT, bn TEXT, fn TEXT,stk1 TEXT, stk2 TEXT, stk3 TEXT,stk4 TEXT)''')
        conn.commit()
    conn.close()


def add_main_1(username, password, nf, bn, fn, stk1, stk2, stk3, stk4):
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    c.execute("INSERT INTO main_1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (username, password, nf, bn, fn, stk1, stk2, stk3, stk4))
    conn.commit()
    conn.close()


def delete_main_1(username):
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    c.execute("DELETE FROM main_1 WHERE username=?", (username,))
    conn.commit()
    conn.close()


# def update_main_1(username, password, nf, bn, fn, stk1, stk2, stk3, stk4,nfint):
#     conn = sqlite3.connect('main_1.db')
#     c = conn.cursor()
#     c.execute('''UPDATE main_1 SET password = password,nf=nf,bn=bn,fn=fn,stk1=stk1,stk2=stk2,stk3=stk3,stk4=stk4,nfint=nfint WHERE username="gvparmar"''')
#     c.execute('''SELECT * from main_1''')
#     conn.commit()
#     conn.close()


def update_main_1(username, password, nf, bn, fn, stk1, stk2, stk3, stk4):
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    # Use placeholders in the UPDATE statement
    c.execute('''
        UPDATE main_1
        SET nf=?, bn=?, fn=?, stk1=?, stk2=?, stk3=?, stk4=? WHERE username=? and password=?
    ''', (username,password, nf, bn, fn, stk1, stk2, stk3, stk4))

    c.execute('SELECT * FROM main_1')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def view_main_1():
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM main_1")
    main_1 = c.fetchall()
    conn.close()
    return main_1


def search_main_1(username):
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM main_1 WHERE username=?", (username,))
    main_1 = c.fetchall()
    conn.close()
    return main_1


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def get_hashed_password(username):
    conn = sqlite3.connect('main_1.db')
    c = conn.cursor()

    # Execute a SELECT query to retrieve the hashed password
    c.execute("SELECT password FROM main_1 WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    # Return the hashed password if the user is found, otherwise return None
    return result[0] if result else None


# Function to verify a password against a hashed and salted version
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


# connected to main----------------------------------
def create_data(u_name, pw, nf, bn, fn, stk1, stk2, stk3, stk4):
    username = u_name
    password = pw
    hashed_password = hash_password(password)
    add_main_1(username, hashed_password, nf, bn, fn, stk1, stk2, stk3, stk4)
    return username, hashed_password, nf, bn, fn, stk1, stk2, stk3, stk4


def varify_data(username, password):
    hashed_password = get_hashed_password(username)
    print(hashed_password)
    user_input_password = password
    if verify_password(user_input_password, hashed_password):
        res = "Password is correct!"
    else:
        res = "Password is incorrect!"
    return res


def update_data(username, password, nf, bn, fn, stk1, stk2, stk3, stk4):
    # data = search_main_1(username)
    # hashed_password = get_hashed_password(username)
    # if verify_password(password, hashed_password):
    update_main_1(username,password, nf, bn, fn, stk1, stk2, stk3, stk4)

#create_database()
#delete_main_1('gvparmar')
# # add_main_1('gvparmar','gvp@123','Y','Y','Y','N','N','N','N')
# tb=search_main_1("gvparmar")
# print(tb)
