import streamlit as st
import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.app.config import settings
from backend.app.langgraph_agent import generate_minutes

# Page configuration
st.set_page_config(
    page_title="ClarifyMeet AI - Meeting Minutes Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6264A7 0%, #8B5CF6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #6264A7;
        margin: 1rem 0;
    }
    .action-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .decision-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
    }
    .risk-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .summary-point {
        background: #f5f5f5;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .speaker-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .priority-high {
        color: #d32f2f;
        font-weight: bold;
    }
    .priority-medium {
        color: #f57c00;
        font-weight: bold;
    }
    .priority-low {
        color: #388e3c;
        font-weight: bold;
    }
    .warning-badge {
        background: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

def display_header():
    """Display application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 ClarifyMeet AI</h1>
        <p style="font-size: 1.1rem; margin: 0;">Transform meeting conversations into actionable insights using AI</p>
    </div>
    """, unsafe_allow_html=True)

def display_features():
    """Display feature overview"""
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("📝 **Summary**")
    with col2:
        st.markdown("✅ **Action Items**")
    with col3:
        st.markdown("💡 **Decisions**")
    with col4:
        st.markdown("⚠️ **Risks**")
    with col5:
        st.markdown("👥 **Speakers**")

def display_executive_summary(summary_points):
    """Display executive summary section"""
    st.subheader("📋 Executive Summary")
    for idx, point in enumerate(summary_points, 1):
        st.markdown(f"""
        <div class="summary-point">
            <strong>{idx}.</strong> {point}
        </div>
        """, unsafe_allow_html=True)

def display_action_items(action_items):
    """Display action items section"""
    st.subheader("✅ Action Items")
    
    if not action_items:
        st.info("No action items found in the transcript.")
        return
    
    for idx, action in enumerate(action_items, 1):
        priority = action.get('priority', 'Medium')
        priority_class = f"priority-{priority.lower()}"
        
        st.markdown(f"""
        <div class="action-item">
            <h4>Action #{idx}: {action.get('description', 'N/A')}</h4>
            <p><strong>Owner:</strong> {action.get('owner', 'Unassigned')}</p>
            <p><strong>Due Date:</strong> {action.get('due_date', 'Not specified')}</p>
            <p><strong>Priority:</strong> <span class="{priority_class}">{priority}</span></p>
            <p><strong>Status:</strong> {action.get('status', 'Pending')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_decisions(decisions):
    """Display decisions section"""
    st.subheader("💡 Decisions Made")
    
    if not decisions:
        st.info("No decisions found in the transcript.")
        return
    
    for idx, decision in enumerate(decisions, 1):
        st.markdown(f"""
        <div class="decision-box">
            <h4>Decision #{idx}</h4>
            <p><strong>What:</strong> {decision.get('decision', 'N/A')}</p>
            <p><strong>Rationale:</strong> {decision.get('rationale', 'Not provided')}</p>
            <p><strong>Owner:</strong> {decision.get('owner', 'Not assigned')}</p>
            <p><strong>Context:</strong> {decision.get('context', 'Not provided')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_risks(risks):
    """Display risks section"""
    st.subheader("⚠️ Risks & Concerns")
    
    if not risks:
        st.info("No risks identified in the transcript.")
        return
    
    for idx, risk in enumerate(risks, 1):
        impact = risk.get('impact', 'Medium')
        st.markdown(f"""
        <div class="risk-box">
            <h4>Risk #{idx}</h4>
            <p><strong>Risk:</strong> {risk.get('risk', 'N/A')}</p>
            <p><strong>Impact:</strong> <span class="priority-{impact.lower()}">{impact}</span></p>
            <p><strong>Mitigation:</strong> {risk.get('mitigation', 'Not provided')}</p>
            <p><strong>Owner:</strong> {risk.get('owner', 'Not assigned')}</p>
        </div>
        """, unsafe_allow_html=True)

def display_speaker_spotlight(speakers):
    """Display speaker spotlight section"""
    st.subheader("👥 Speaker Spotlight")
    
    if not speakers:
        st.info("No speaker information available.")
        return
    
    cols = st.columns(min(len(speakers), 3))
    for idx, speaker in enumerate(speakers):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="speaker-card">
                <h4>{speaker.get('speaker', 'Unknown')}</h4>
                <p><strong>Role:</strong> {speaker.get('role', 'Not specified')}</p>
                <p><strong>Contributions:</strong> {speaker.get('contribution_count', 0)}</p>
                <p><strong>Key Points:</strong></p>
                <ul>
                    {''.join(f'<li>{point}</li>' for point in speaker.get('key_points', []))}
                </ul>
            </div>
            """, unsafe_allow_html=True)

def display_metadata(metadata, warnings):
    """Display metadata and warnings"""
    st.subheader("📊 Analysis Metadata")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Transcript Length", f"{metadata.get('transcript_length_words', 0)} words")
    with col2:
        st.metric("Speakers", metadata.get('speaker_count', 0))
    with col3:
        st.metric("Processing Method", metadata.get('processing_method', 'N/A').upper())
    with col4:
        st.metric("Confidence", metadata.get('confidence_score', 'N/A'))
    
    if warnings:
        st.warning(f"⚠️ {len(warnings)} warnings detected")
        with st.expander("View Warnings"):
            for warning in warnings:
                st.markdown(f"""
                <div class="warning-badge">
                    {warning.get('type', 'unknown')}: {warning.get('message', 'N/A')}
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main application function"""
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        st.info(f"""
        **Model:** {settings.OLLAMA_MODEL}  
        **Ollama Host:** {settings.OLLAMA_HOST}  
        **Max File Size:** {settings.MAX_TRANSCRIPT_SIZE_MB} MB
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 📖 How to Use
        1. Upload a meeting transcript (.txt file)
        2. Click "Analyze Transcript"
        3. View the AI-generated meeting minutes
        4. Download results as JSON
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 📝 Transcript Format
        Use speaker-based format:
        ```
        John: Let's discuss the project.
        Sarah: I agree. We need to...
        ```
        """)
    
    # Main content
    display_features()
    st.markdown("---")
    
    # File upload section
    st.subheader("📤 Upload Meeting Transcript")
    uploaded_file = st.file_uploader(
        "Choose a transcript file (.txt)",
        type=['txt'],
        help="Upload your meeting transcript in .txt format"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)
        
        # Analyze button
        if st.button("🚀 Analyze Transcript", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your transcript... This may take a minute."):
                try:
                    # Read file content
                    transcript_text = uploaded_file.read().decode('utf-8')
                    
                    # Validate file size
                    if len(transcript_text) > settings.MAX_TRANSCRIPT_SIZE_MB * 1024 * 1024:
                        st.error(f"File too large. Maximum size is {settings.MAX_TRANSCRIPT_SIZE_MB} MB.")
                        return
                    
                    # Process transcript
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Step 1/3: Processing transcript...")
                    progress_bar.progress(33)
                    
                    # Run async function
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(generate_minutes(transcript_text))
                    loop.close()
                    
                    status_text.text("Step 2/3: Extracting insights...")
                    progress_bar.progress(66)
                    
                    status_text.text("Step 3/3: Finalizing results...")
                    progress_bar.progress(100)
                    
                    # Store results - extract minutes from result if it's wrapped
                    if isinstance(result, dict) and 'minutes' in result:
                        st.session_state.analysis_results = result['minutes']
                    else:
                        st.session_state.analysis_results = result
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing transcript: {str(e)}")
                    st.exception(e)
    
    # Display results if available
    if st.session_state.analysis_results:
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Add timestamp
        st.caption(f"Analyzed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Summary", "✅ Action Items", "💡 Decisions", 
            "⚠️ Risks", "👥 Speakers", "📊 Metadata"
        ])
        
        with tab1:
            display_executive_summary(results.get('executive_summary', []))
        
        with tab2:
            display_action_items(results.get('action_items', []))
        
        with tab3:
            display_decisions(results.get('decisions', []))
        
        with tab4:
            display_risks(results.get('risks', []))
        
        with tab5:
            display_speaker_spotlight(results.get('speaker_spotlight', []))
        
        with tab6:
            display_metadata(
                results.get('metadata', {}),
                results.get('warnings', [])
            )
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="📥 Download JSON Results",
                data=json_str,
                file_name=f"meeting_minutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
