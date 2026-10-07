import streamlit as st
from db import notes_collection
# Page Configuration
st.set_page_config(
    page_title="AI Notes Manager",
    page_icon="📝",
    layout="wide"
)
# Check MongoDB
if notes_collection is None:
    st.error("❌ MongoDB is not connected!")
    st.info("Please start your local MongoDB server.")
    st.stop()
# Title
st.title("📝 AI Notes Manager")
st.write("MongoDB + Python + Streamlit")
# Sidebar

st.sidebar.header("📚 Note Manager")
menu = st.sidebar.radio(
    "Select Operation",
    [
        "Add Note",
        "View Notes",
        "Search Notes",
        "Update Note",
        "Delete Note"
    ]
)
# 1. ADD NOTES
if menu == "Add Note":
    st.header("➕ Add New Note")
    title = st.text_input("Note Title")
    category = st.selectbox(
        "Category",
        [
            "Python",
            "AI",
            "Machine Learning",
            "MongoDB",
            "Streamlit",
            "Other"
        ]
    )
    content = st.text_area(
        "Note Content",
        height=250
    )
    if st.button("💾 Save Note"):
        if title.strip() == "":
            st.warning("Please enter a note title.")
        elif content.strip() == "":
            st.warning("Please enter note content.")
        else:
            note = {
                "title": title,
                "category": category,
                "content": content
            }
            notes_collection.insert_one(note)
            st.success("✅ Note saved successfully!")
# 2. VIEW NOTES

elif menu == "View Notes":
    st.header("📋 All Notes")
    notes = list(
        notes_collection.find().sort("_id", -1)
    )
    if len(notes) == 0:
        st.info("No notes found.")
    else:
        for note in notes:
            with st.expander(
                f"📌 {note['title']} — {note['category']}"
            ):
                st.write(note["content"])
                st.caption(
                    f"MongoDB ID: {note['_id']}"
                )
# 3. SEARCH NOTES
elif menu == "Search Notes":
    st.header("🔍 Search Notes")
    search_text = st.text_input(
        "Enter title or category"
    )
    if search_text:
        results = list(
            notes_collection.find(
                {
                    "$or": [
                        {
                            "title": {
                                "$regex": search_text,
                                "$options": "i"
                            }
                        },
                        {
                            "category": {
                                "$regex": search_text,
                                "$options": "i"
                            }
                        }
                    ]
                }
            )
        )
        if len(results) == 0:
            st.warning("No matching notes found.")
        else:
            st.success(
                f"{len(results)} note(s) found."
            )
            for note in results:
                st.subheader(note["title"])
                st.write(
                    f"**Category:** {note['category']}"
                )
                st.write(note["content"])
                st.divider()
# 4. UPDATE NOTES
elif menu == "Update Note":
    st.header("✏️ Update Note")
    notes = list(
        notes_collection.find().sort("_id", -1)
    )
    if len(notes) == 0:
        st.info("No notes available.")
    else:
        note_options = {
            f"{note['title']} ({note['_id']})": note
            for note in notes
        }
        selected = st.selectbox(
            "Select Note",
            list(note_options.keys())
        )
        note = note_options[selected]
        new_title = st.text_input(
            "Title",
            value=note["title"]
        )
        new_category = st.text_input(
            "Category",
            value=note["category"]
        )
        new_content = st.text_area(
            "Content",
            value=note["content"],
            height=250
        )
        if st.button("🔄 Update Note"):
            notes_collection.update_one(
                {"_id": note["_id"]},
                {
                    "$set": {
                        "title": new_title,
                        "category": new_category,
                        "content": new_content
                    }
                }
            )
            st.success("✅ Note updated successfully!")
            st.rerun()
# 5. DELETE NOTES
elif menu == "Delete Note":
    st.header("🗑️ Delete Note")
    notes = list(
        notes_collection.find().sort("_id", -1)
    )
    if len(notes) == 0:
        st.info("No notes available.")
    else:
        note_options = {
            f"{note['title']} ({note['_id']})": note["_id"]
            for note in notes
        }
        selected = st.selectbox(
            "Select Note to Delete",
            list(note_options.keys())
        )
        if st.button("🗑️ Delete Note"):
            note_id = note_options[selected]
            notes_collection.delete_one(
                {"_id": note_id}
            )
            st.success("✅ Note deleted successfully!")
            st.rerun()