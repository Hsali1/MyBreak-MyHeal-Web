import streamlit as st
import tempfile
import os
import functions

st.title("My Break and My Heal")
st.subheader("This is my file manager app.")
st.write("This app allows file sharing")

with st.expander("My Break"):
    with st.form("break_form", clear_on_submit=True):
        file_to_break = st.file_uploader(label="Enter file to break", key="file")
        st.text_input(label="Enter Prefix", key="break_prefix")
        st.text_input(label="Enter Chunk Size (in KB)", key="break_chunk_size")
        submitted_break = st.form_submit_button("Submit")
    if submitted_break:
        # example
        # uploaded_file = UploadedFile(file_id='9df08f1a-a7e2-4111-8d0e-24fbd160eb15',
        #         name='me.jpg', type='image/jpeg', size=204150,
        #         _file_urls=file_id: "9df08f1a-a7e2-4111-8d0e-24fbd160eb15"
        # prefix = hassan
        # chunk_size = 20
        file_name = file_to_break.name
        prefix = st.session_state["break_prefix"]
        chunk_size = int(st.session_state["break_chunk_size"])
        # make temp directory
        temp_dir = tempfile.mkdtemp()
        # example temp_dir=C:\Users\dotma\AppData\Local\Temp\tmp6vton91d
        source = os.path.join(temp_dir, file_name)
        # example C:\Users\dotma\AppData\Local\Temp\tmp6vton91d\me.jpg
        with open(source, "wb") as f:
            f.write(file_to_break.getvalue())
        print(f"Temporary new path {source}")
        destination = os.path.join(temp_dir, "chunks")
        os.makedirs(destination, exist_ok=True)
        run_break_it = functions.break_it(source, prefix, chunk_size, destination)
        if run_break_it:
            st.write(f"Breaking file {file_name} complete. Find file at:")
            st.code(destination, language="python")
with st.expander("My Heal"):
    with st.form("heal_form", clear_on_submit=True):
        st.text_input(label="Enter chunk file path", key="chunk_path",
                      placeholder="example: C:\\Users\\my_name\\OneDrive\\Desktop\\chunkFolder")
        st.text_input(label="Enter File you want to create", key="heal_name",
                      placeholder="example: coffee.png")
        st.text_input(label="Enter Prefix", key="heal_prefix")
        st.text_input(label="Enter Chunk Size (in KB)", key="heal_chunk_size")
        st.text_input(label="Enter number of chunks", key="heal_num_chunks")
        submitted_heal = st.form_submit_button("Submit")

    if submitted_heal:
        file_name = st.session_state["heal_name"]
        chunk_path = st.session_state["chunk_path"]
        prefix = st.session_state["heal_prefix"]
        chunk_size = int(st.session_state["heal_chunk_size"])
        number_of_chunks = int(st.session_state["heal_num_chunks"])
        print(f"file_name = {file_name}")
        print(f"chunk_path = {chunk_path}")
        print(f"prefix = {prefix}")
        print(f"chunk_size = {chunk_size}")
        print(f"number_of_chunks = {number_of_chunks}")
        # make temp directory
        temp_dir = tempfile.mkdtemp()
        run_heal_it = functions.heal_it(file_name,
                                        prefix,
                                        chunk_size,
                                        number_of_chunks,
                                        chunk_path,
                                        temp_dir)
        if run_heal_it:
            st.write(f"Healing file {file_name} complete. Find file at:")
            st.code(temp_dir, language="python")
