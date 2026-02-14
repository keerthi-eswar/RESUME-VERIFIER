"""
Streamlit Frontend for AI-Based Smart Resume Screening System
Provides user interface for uploading resumes and viewing ranked results
"""

import streamlit as st
import requests
import pandas as pd
from typing import List
import io

# Configure Streamlit page
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .rank-1 { background-color: #FFD700; }
    .rank-2 { background-color: #C0C0C0; }
    .rank-3 { background-color: #CD7F32; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("⚙️ Settings")
api_url = st.sidebar.text_input(
    "API Endpoint URL",
    value="http://localhost:8000",
    help="URL of the resume screening API"
)

st.sidebar.info("""
    ### How to use:
    1. Enter the job description
    2. Upload resume files (PDF/DOCX)
    3. Click "Screen Resumes" to analyze
    4. View ranked results
    """)


def main():
    """Main application logic"""

    # Header
    st.title("🤖 AI-Based Resume Screening System")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=200,
            placeholder="Paste the job description here...",
            label_visibility="collapsed"
        )

    with col2:
        st.header("📊 Analysis Stats")
        stats_placeholder = st.empty()

    st.markdown("---")

    # File upload section
    st.header("📤 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Select resume files (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload multiple resume files for screening"
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        screen_button = st.button(
            "🔍 Screen Resumes",
            use_container_width=True,
            type="primary"
        )

    st.markdown("---")

    # Process resumes when button is clicked
    if screen_button:
        if not job_description.strip():
            st.error("❌ Please enter a job description")
            return

        if not uploaded_files:
            st.error("❌ Please upload at least one resume")
            return

        with st.spinner("🔄 Analyzing resumes... This may take a moment"):
            try:
                # Prepare files for API
                files = []
                for uploaded_file in uploaded_files:
                    files.append(
                        ("resumes", (uploaded_file.name, uploaded_file.getbuffer(), uploaded_file.type))
                    )

                # Send request to API
                response = requests.post(
                    f"{api_url}/screen-resumes",
                    data={"job_description": job_description},
                    files=files,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display results
                    st.success("✅ Analysis completed successfully!")

                    # Update stats
                    with stats_placeholder.container():
                        st.metric("Total Resumes", result["total_resumes"])

                    # Display ranking table
                    st.header("🏆 Resume Rankings")

                    # Prepare data for table
                    table_data = []
                    for i, resume in enumerate(result["ranked_resumes"], 1):
                        table_data.append({
                            "Rank": f"#{resume['rank']}",
                            "Candidate Name": resume["candidate_name"],
                            "Similarity Score": f"{resume['similarity_score']:.4f}",
                            "Match %": f"{resume['similarity_score'] * 100:.2f}%",
                            "Relevance": get_relevance_label(resume["similarity_score"])
                        })

                    df = pd.DataFrame(table_data)

                    # Display table with styling
                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=400,
                        hide_index=True
                    )

                    # Download results as CSV
                    st.markdown("---")
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="resume_rankings.csv",
                        mime="text/csv"
                    )

                    # Display detailed metrics
                    st.header("📈 Detailed Analysis")

                    col1, col2, col3 = st.columns(3)

                    top_score = result["ranked_resumes"][0]["similarity_score"]
                    avg_score = sum(r["similarity_score"] for r in result["ranked_resumes"]) / len(
                        result["ranked_resumes"]
                    )
                    min_score = result["ranked_resumes"][-1]["similarity_score"]

                    with col1:
                        st.metric("Highest Match", f"{top_score:.4f}", "Top Candidate")

                    with col2:
                        st.metric("Average Match", f"{avg_score:.4f}", f"{avg_score * 100:.2f}%")

                    with col3:
                        st.metric("Lowest Match", f"{min_score:.4f}", "Bottom Candidate")

                    # Top candidate details
                    if result["ranked_resumes"]:
                        st.markdown("---")
                        st.header("🌟 Top Candidate")
                        top_candidate = result["ranked_resumes"][0]

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"**Name:** {top_candidate['candidate_name']}")
                        with col2:
                            st.success(f"**Score:** {top_candidate['similarity_score']:.4f}")
                        with col3:
                            st.success(f"**Match:** {top_candidate['similarity_score'] * 100:.2f}%")

                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.error(response.json().get("error", "Unknown error"))

            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to API at {api_url}")
                st.info("Make sure the backend API is running (python -m backend.main)")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def get_relevance_label(similarity_score: float) -> str:
    """
    Get relevance label based on similarity score

    Args:
        similarity_score: Score between 0 and 1

    Returns:
        Relevance label
    """
    if similarity_score >= 0.8:
        return "🟢 Highly Relevant"
    elif similarity_score >= 0.6:
        return "🟡 Relevant"
    elif similarity_score >= 0.4:
        return "🟠 Moderately Relevant"
    else:
        return "🔴 Low Relevance"


if __name__ == "__main__":
    main()
