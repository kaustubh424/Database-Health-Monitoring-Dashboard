import streamlit as st
import time
import random

# Try importing MySQL connector safely
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

st.set_page_config(page_title="DB Health Monitor", layout="centered")

st.title("📊 Database Health Monitoring Dashboard")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.radio("Select Mode", ["Demo Mode", "Real Database Mode"])

if mode == "Real Database Mode":
    if not MYSQL_AVAILABLE:
        st.error("❌ mysql-connector-python not installed. Add it in requirements.txt")
    else:
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

                # Show metrics
                st.subheader("📈 Database Metrics (Real Mode)")
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

else:
    # Demo Mode (Random data)
    uptime = random.randint(1000, 50000)
    connections = random.randint(1, 100)
    query_time = round(random.uniform(0.1, 2.0), 3)
    failed_conn = random.randint(0, 10)

    st.subheader("📈 Database Metrics (Demo Mode)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏱️ Uptime (sec)", uptime)
        st.metric("⚡ Query Time (s)", query_time)
    with col2:
        st.metric("👥 Active Connections", connections)
        st.metric("❌ Failed Connections", failed_conn)

    # Alerts
    if connections > 50:
        st.error("⚠️ Too many active connections!")
    if query_time > 1:
        st.warning("⏳ Query running slow!")
