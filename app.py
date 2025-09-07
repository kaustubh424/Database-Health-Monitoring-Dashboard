import streamlit as st
import mysql.connector
import time

st.set_page_config(page_title="DB Health Monitor", layout="centered")

st.title("📊 Database Health Monitoring Dashboard")

# Sidebar for DB Config
st.sidebar.header("🔑 Database Configuration")
db_host = st.sidebar.text_input("Host", "localhost")
db_user = st.sidebar.text_input("User", "root")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database", "testdb")

if st.sidebar.button("Connect to Database"):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()

        # Uptime
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Uptime';")
        uptime = cursor.fetchone()[1]

        # Active Connections
        cursor.execute("SHOW STATUS LIKE 'Threads_connected';")
        connections = cursor.fetchone()[1]

        # Query Time
        start = time.time()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables;")
        cursor.fetchall()
        query_time = round(time.time() - start, 3)

        # Failed Connections
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Aborted_connects';")
        failed_conn = cursor.fetchone()[1]

        # Display metrics
        st.subheader("📈 Database Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⏱️ Uptime (sec)", uptime)
            st.metric("⚡ Query Time (s)", query_time)
        with col2:
            st.metric("👥 Active Connections", connections)
            st.metric("❌ Failed Connections", failed_conn)

        # Alerts
        if int(connections) > 50:
            st.error("⚠️ Too many active connections!")
        if query_time > 1:
            st.warning("⏳ Query running slow!")

    except Exception as e:
        st.error(f"Database Connection Error: {e}")
