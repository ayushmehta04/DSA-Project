import streamlit as st

# ----- Initialize Queues -----
if 'normal_queue' not in st.session_state:
    st.session_state.normal_queue = []
if 'emergency_queue' not in st.session_state:
    st.session_state.emergency_queue = []

def create_patient(pid, name, age, disease, priority):
    return {
        'id': int(pid),
        'name': name,
        'age': int(age),
        'disease': disease,
        'priority': int(priority)
    }

def enqueue(patient):
    """Add patient to the correct queue based on priority."""
    if 0 <= patient['priority'] <= 3:
        st.session_state.normal_queue.append(patient)
    else:
        # Insert in emergency queue based on priority (descending order)
        queue = st.session_state.emergency_queue
        inserted = False
        for i, p in enumerate(queue):
            if patient['priority'] > p['priority']:
                queue.insert(i, patient)
                inserted = True
                break
        if not inserted:
            queue.append(patient)

def treat_next():
    """Treat (remove) the next patient from queues."""
    if st.session_state.emergency_queue:
        patient = st.session_state.emergency_queue.pop(0)
        st.info(f"Treated Emergency Patient: {patient['name']} (ID: {patient['id']})")
    elif st.session_state.normal_queue:
        patient = st.session_state.normal_queue.pop(0)
        st.info(f"Treated Normal Patient: {patient['name']} (ID: {patient['id']})")
    else:
        st.error("No patients in queue!")

def dequeue(pid):
    """Remove a patient by ID from either queue."""
    pid = int(pid)
    norm = st.session_state.normal_queue
    emer = st.session_state.emergency_queue
    # Try to remove from normal
    for i, patient in enumerate(norm):
        if patient['id'] == pid:
            norm.pop(i)
            st.success(f"Removed (dequeued) Normal Patient with ID {pid}")
            return
    # Try to remove from emergency
    for i, patient in enumerate(emer):
        if patient['id'] == pid:
            emer.pop(i)
            st.success(f"Removed (dequeued) Emergency Patient with ID {pid}")
            return
    st.warning("Patient ID not found in any queue.")

def search_patient(search_type, search_value):
    """Search for a patient by ID or Name."""
    all_patients = st.session_state.emergency_queue + st.session_state.normal_queue
    found = None
    if search_type == "ID":
        try:
            sid = int(search_value)
        except:
            st.error("Enter a valid ID (number).")
            return
        found = next((p for p in all_patients if p['id'] == sid), None)
    else:
        found = next((p for p in all_patients if p['name'].strip().lower() == search_value.strip().lower()), None)
    if found:
        st.success("✅ Patient Found")
        st.write({
            "ID": found['id'],
            "Name": found['name'],
            "Age": found['age'],
            "Disease": found['disease'],
            "Priority": found['priority'],
            "Type": "Normal" if 0 <= found['priority'] <= 3 else "Emergency"
        })
    else:
        st.error("❌ Patient not found!")

st.title("🏥 Hospital Patient Queue Management (Easy Version)")

# ---- Layout Left: Add, Search, Treat, Dequeue ----
col1, col2 = st.columns(2)
with col1:
    st.header("➕ Add Patient")
    with st.form("add_form"):
        pid = st.number_input("Patient ID", min_value=0, step=1, key="id")
        name = st.text_input("Name", key="name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age")
        disease = st.text_input("Disease", key="disease")
        priority = st.selectbox(
            "Priority (0-3 → Normal, 4-10 → Emergency)", list(range(0, 11)), key="priority"
        )
        add_btn = st.form_submit_button("Add Patient")
        if add_btn:
            patient = create_patient(pid, name, age, disease, priority)
            enqueue(patient)
            st.success("Patient added!")

    st.divider()
    st.header("🔍 Search / Treat / Dequeue")
    with st.form("action_form"):
        search_type = st.selectbox("Search By", ["ID", "Name"], key="stype")
        search_value = st.text_input("Enter ID or Name", key="svalue")
        search_btn = st.form_submit_button("Search Patient")
        treat_btn = st.form_submit_button("Treat Next Patient")
        dequeue_btn = st.form_submit_button("Dequeue by ID")
        if search_btn:
            if not search_value.strip():
                st.warning("Please enter a search value!")
            else:
                search_patient(search_type, search_value)
        if treat_btn:
            treat_next()
        if dequeue_btn:
            if not search_value.strip():
                st.warning("Enter ID to dequeue.")
            else:
                dequeue(search_value)

# ---- Layout Right: Display Queues ----
with col2:
    st.header("🚨 Emergency Queue (Priority 4-10)")
    if not st.session_state.emergency_queue:
        st.info("No emergency patients.")
    else:
        for p in st.session_state.emergency_queue:
            st.write(
                f"**{p['name']}** | ID: {p['id']} | Age: {p['age']} | Disease: {p['disease']} | "
                f"Priority: {p['priority']}"
            )

    st.header("📋 Normal Queue (Priority 0-3)")
    if not st.session_state.normal_queue:
        st.info("No normal patients.")
    else:
        for p in st.session_state.normal_queue:
            st.write(
                f"**{p['name']}** | ID: {p['id']} | Age: {p['age']} | Disease: {p['disease']} | "
                f"Priority: {p['priority']}"
            )