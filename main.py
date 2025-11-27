import streamlit as st
import tempfile
import os
import functions

st.title("My Break and My Heal")
st.subheader("This is my file manager app.")
st.write("This app allows file sharing")

with st.expander("My Break"):
    with st.form("my_form"):
        uploaded_file = st.file_uploader(label="Enter file to break", key="file")
        st.text_input(label="Enter Prefix", key="prefix")
        st.text_input(label="Enter Chunk Size (in KB)", key="chunk_size")
        submitted = st.form_submit_button("Submit")

if submitted:
    # example
    # uploaded_file = UploadedFile(file_id='9df08f1a-a7e2-4111-8d0e-24fbd160eb15',
    #         name='me.jpg', type='image/jpeg', size=204150,
    #         _file_urls=file_id: "9df08f1a-a7e2-4111-8d0e-24fbd160eb15"
    # prefix = hassan
    # chunk_size = 20
    file_name = uploaded_file.name
    prefix = st.session_state["prefix"]
    chunk_size = int(st.session_state["chunk_size"])
    # make temp director
    temp_dir = tempfile.mkdtemp()
    # example temp_dir=C:\Users\dotma\AppData\Local\Temp\tmp6vton91d
    source = os.path.join(temp_dir, file_name)
    # example C:\Users\dotma\AppData\Local\Temp\tmp6vton91d\me.jpg
    with open(source, "wb") as f:
        f.write(uploaded_file.getvalue())
    print(f"Temporary new path {source}")
    destination = os.path.join(temp_dir, "chunks")
    os.makedirs(destination, exist_ok=True)
    run_break_it = functions.break_it(source, prefix, chunk_size, destination)
    if run_break_it:
        print(f"Breaking complete. Find your files at:")
        print(destination)

st.session_state