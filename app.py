import streamlit as st
import json

def load_data():
    with open('risk-measures.json', 'r') as file:
        return json.load(file)

def display_item(item, item_type="source"):
    """Display individual risk/measure items"""
    if isinstance(item, dict):
        for key, value in item.items():
            if ("Risk source" in key and item_type == "source") or \
               ("Risk management measure" in key and item_type == "measure"):
                
                # Style based on type with smaller heading (h4)
                if item_type == "source":
                    st.markdown(f"#### ⚠️ {value['title']}")
                else:
                    st.markdown(f"#### 🛡️ {value['title']}")
                
                st.markdown(value['description'])
                st.markdown("")  # Add spacing

def collect_items(data, item_type="source"):
    """Recursively collect all items of specified type"""
    items = []
    if isinstance(data, list):
        for item in data:
            items.extend(collect_items(item, item_type))
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                items.extend(collect_items(value, item_type))
            elif isinstance(value, dict):
                if ("Risk source" in key and item_type == "source") or \
                   ("Risk management measure" in key and item_type == "measure"):
                    items.append({key: value})
    return items

def main():
    st.set_page_config(
        page_title="AI Risk Measures Explorer",
        page_icon="🤖",
        layout="wide"
    )

    st.title("AI Risk Sources & Measures")
    st.markdown("""
    Explore various AI risk sources and management strategies.
    """)

    data = load_data()

    # Move category selector to main content area
    selected_category = st.selectbox(
        "Select Category",
        list(data.keys())
    )

    # Search functionality
    search_term = st.text_input("🔍 Search for specific terms", "")

    # Main content area
    if search_term:
        st.subheader(f"Search Results for: '{search_term}'")
        category_data = data[selected_category]
        sources = [item for item in collect_items(category_data, "source") 
                  if search_term.lower() in str(item).lower()]
        measures = [item for item in collect_items(category_data, "measure")
                   if search_term.lower() in str(item).lower()]
    else:
        category_data = data[selected_category]
        sources = collect_items(category_data, "source")
        measures = collect_items(category_data, "measure")

    # Create two columns
    col1, col2 = st.columns(2)

    # Left column: Risk Sources
    with col1:
        with st.expander("⚠️ Risk Sources", expanded=True):
            if not sources:
                st.info("No risk sources found.")
            for item in sources:
                display_item(item, "source")

    # Right column: Risk Measures
    with col2:
        with st.expander("🛡️ Risk Management Measures", expanded=True):
            if not measures:
                st.info("No risk management measures found.")
            for item in measures:
                display_item(item, "measure")

if __name__ == "__main__":
    main()