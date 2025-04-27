import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from db_helper import DatabaseHelper
import json
import os
from datetime import datetime

# Initialize database
db = DatabaseHelper()

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
template_categories = ["Announcement", "Achievement", "Story", "Question", "Tip"]

# Initialize session state
if 'current_post' not in st.session_state:
    st.session_state.current_post = None
if 'editing_post' not in st.session_state:
    st.session_state.editing_post = None
if 'editing_template' not in st.session_state:
    st.session_state.editing_template = None

# Load user preferences
def load_user_preferences():
    preferences = db.get_user_preferences()
    if preferences:
        return {
            'use_emojis': bool(preferences[1]),
            'show_hashtags': bool(preferences[2]),
            'default_length': preferences[3],
            'default_language': preferences[4]
        }
    return {
        'use_emojis': True,
        'show_hashtags': True,
        'default_length': 'Medium',
        'default_language': 'English'
    }

# Main app layout
def main():
    st.title("LinkedIn Post Generator")
    
    # Load user preferences
    user_prefs = load_user_preferences()
    
    # Sidebar for settings and history
    with st.sidebar:
        st.header("Settings")
        use_emojis = st.checkbox("Add Emojis", value=user_prefs['use_emojis'])
        show_hashtags = st.checkbox("Show Hashtag Suggestions", value=user_prefs['show_hashtags'])
        
        # Save preferences when changed
        if (use_emojis != user_prefs['use_emojis'] or 
            show_hashtags != user_prefs['show_hashtags']):
            db.save_user_preferences(use_emojis, show_hashtags, 
                                   user_prefs['default_length'], 
                                   user_prefs['default_language'])
        
        # Templates section
        st.header("Templates")
        template_category = st.selectbox("Template Category", options=template_categories)
        templates = db.get_templates()
        if templates:
            for template in templates:
                if template[3] == template_category:  # Check category
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"Use: {template[1]}", key=f"template_{template[0]}"):
                            st.session_state.current_post = template[2]
                    with col2:
                        if st.button("✏️", key=f"edit_template_{template[0]}"):
                            st.session_state.editing_template = template
                            st.rerun()
        
        # Post History
        st.header("Post History")
        posts = db.get_all_posts()
        for post in posts:
            with st.expander(f"Post {post[0]}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"Topic: {post[2]}")
                    st.write(f"Length: {post[3]}")
                    st.write(f"Language: {post[4]}")
                    st.write(f"Time: {post[5]}")
                with col2:
                    if st.button("✏️", key=f"edit_{post[0]}"):
                        st.session_state.editing_post = post
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"delete_{post[0]}"):
                        db.delete_post(post[0])
                        st.rerun()
                st.write("---")
                st.write(post[1])

    # Main content area
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    # Template creation/editing
    with st.expander("Create/Edit Template"):
        if st.session_state.editing_template:
            template_name = st.text_input("Template Name", value=st.session_state.editing_template[1])
            template_content = st.text_area("Template Content", value=st.session_state.editing_template[2])
            template_category = st.selectbox("Category", options=template_categories, index=template_categories.index(st.session_state.editing_template[3]))
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes"):
                    # Update template in database
                    st.success("Template updated!")
                    st.session_state.editing_template = None
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.editing_template = None
                    st.rerun()
        else:
            template_name = st.text_input("Template Name")
            template_content = st.text_area("Template Content")
            template_category = st.selectbox("Category", options=template_categories)
            if st.button("Save Template"):
                db.save_template(template_name, template_content, template_category)
                st.success("Template saved!")

    # Generate and Regenerate buttons
    col1, col2 = st.columns(2)
    with col1:
        generate_clicked = st.button("Generate Post")
    with col2:
        regenerate_clicked = st.button("Regenerate")

    # Generate or regenerate post
    if generate_clicked or (regenerate_clicked and st.session_state.current_post):
        with st.spinner('Generating your post...'):
            post = generate_post(selected_length, selected_language, selected_tag, use_emojis=use_emojis)
            st.session_state.current_post = post
            # Save to database
            db.save_post(post, selected_tag, selected_length, selected_language)

    # Display the generated post
    if st.session_state.current_post:
        st.subheader("Generated Post")
        
        # Edit post section
        if st.session_state.editing_post:
            edited_post = st.text_area("Edit Post", value=st.session_state.editing_post[1], height=200)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes"):
                    # Update post in database
                    st.success("Post updated!")
                    st.session_state.current_post = edited_post
                    st.session_state.editing_post = None
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.editing_post = None
                    st.rerun()
        else:
            st.write(st.session_state.current_post)
            
            # Character count
            char_count = len(st.session_state.current_post)
            st.caption(f"Character count: {char_count}/3000 (LinkedIn limit)")
            
            # Copy to clipboard button
            if st.button("Copy to Clipboard"):
                st.code(st.session_state.current_post)
                st.success("Post copied to clipboard!")
            
            # Save as template
            if st.button("Save as Template"):
                template_name = f"Template_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                db.save_template(template_name, st.session_state.current_post, "Custom")
                st.success("Saved as template!")
            
            # Hashtag suggestions
            if show_hashtags:
                st.subheader("Suggested Hashtags")
                suggested_hashtags = [
                    f"#{selected_tag.replace(' ', '')}",
                    "#LinkedIn",
                    "#ProfessionalGrowth",
                    "#CareerDevelopment"
                ]
                st.write(" ".join(suggested_hashtags))

if __name__ == "__main__":
    main()