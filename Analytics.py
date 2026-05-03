"""
Analytics Application with Streamlit
======================================

Professional data analytics dashboard using Streamlit with dark mode theme.
Provides data loading, statistical analysis, and interactive visualizations.

Author: Analytics Team
Version: 3.0.0
"""

import logging
import os
from pathlib import Path
from typing import Optional
import io

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode CSS with enhanced styling
st.markdown("""
    <style>
    :root {
        --primary-color: #1f77b4;
        --background-color: #0e1117;
        --secondary-bg: #161b22;
        --text-color: #e6edf3;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        color: #e6edf3;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0d1117;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1f77b4;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# Configuration Constants
# ============================================================================

DEFAULT_CSV_DELIMITER = ';'
DEFAULT_HISTOGRAM_BINS = 30
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# ============================================================================
# Logging Configuration
# ============================================================================

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('analytics.log')
        ]
    )


# ============================================================================
# Data Loading Functions
# ============================================================================

@st.cache_data
def load_data(file_path: str, delimiter: str = DEFAULT_CSV_DELIMITER) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file with error handling and validation.

    Parameters
    ----------
    file_path : str
        Path to the CSV file to load.
    delimiter : str, optional
        CSV delimiter character (default: ';').

    Returns
    -------
    Optional[pd.DataFrame]
        Loaded DataFrame or None if loading fails.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        data = pd.read_csv(file_path, delimiter=delimiter)

        if data.empty:
            raise ValueError("The CSV file is empty.")

        logger.info(
            f"Data loaded successfully from '{file_path}'. "
            f"Shape: {data.shape[0]} rows × {data.shape[1]} columns"
        )
        return data

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


@st.cache_data
def load_data_from_bytes(file_bytes: bytes, delimiter: str = DEFAULT_CSV_DELIMITER) -> Optional[pd.DataFrame]:
    """Load data from uploaded file bytes."""
    try:
        data = pd.read_csv(io.BytesIO(file_bytes), delimiter=delimiter)
        
        if data.empty:
            raise ValueError("The CSV file is empty.")
        
        logger.info(f"Data loaded from uploaded file. Shape: {data.shape[0]} rows × {data.shape[1]} columns")
        return data
    
    except Exception as e:
        logger.error(f"Error loading data from bytes: {e}")
        raise


# ============================================================================
# Analysis Functions
# ============================================================================

def get_data_summary(data: pd.DataFrame) -> str:
    """Generate data summary statistics."""
    return data.describe().to_string()


def get_missing_values(data: pd.DataFrame) -> str:
    """Generate missing values report."""
    missing = data.isnull().sum()
    
    if missing.sum() == 0:
        return "✓ No missing values detected!"
    
    report = missing[missing > 0].to_string()
    report += f"\n\nMissing Value Percentage:\n"
    for col in missing[missing > 0].index:
        percentage = (missing[col] / len(data)) * 100
        report += f"{col}: {percentage:.2f}%\n"
    
    return report


def get_data_types(data: pd.DataFrame) -> str:
    """Generate data types report."""
    types_info = data.dtypes.to_string()
    type_counts = data.dtypes.value_counts()
    
    report = f"{types_info}\n\n{'='*45}\nTYPE SUMMARY\n{'='*45}\n{type_counts.to_string()}"
    return report


# ============================================================================
# Visualization Functions
# ============================================================================

def create_histograms(data: pd.DataFrame) -> Optional[Figure]:
    """Create histogram visualizations for numerical columns."""
    numerical_data = data.select_dtypes(include=['number'])
    
    if numerical_data.empty:
        return None
    
    n_cols = min(3, len(numerical_data.columns))
    n_rows = (len(numerical_data.columns) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4*n_rows))
    fig.patch.set_facecolor('#0e1117')
    
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, col in enumerate(numerical_data.columns):
        ax = axes[idx]
        
        data_col = numerical_data[col].dropna()
        
        ax.hist(data_col, bins=DEFAULT_HISTOGRAM_BINS, color='#1f77b4', alpha=0.7, edgecolor='#ffffff')
        ax.set_title(f"{col}", fontweight='bold', color='#e6edf3', fontsize=11)
        ax.set_xlabel("Value", color='#e6edf3')
        ax.set_ylabel("Frequency", color='#e6edf3')
        ax.grid(axis='y', alpha=0.2, color='#30363d')
        ax.set_facecolor('#161b22')
        ax.tick_params(colors='#e6edf3')
        
        # Add mean and median lines
        mean_val = data_col.mean()
        median_val = data_col.median()
        ax.axvline(mean_val, color='#f85149', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='#3fb950', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        ax.legend(fontsize=8, facecolor='#161b22', edgecolor='#30363d')
    
    # Hide extra subplots
    for idx in range(len(numerical_data.columns), len(axes)):
        axes[idx].set_visible(False)
    
    fig.suptitle("Data Distribution Analysis", fontsize=14, fontweight='bold', color='#e6edf3')
    fig.tight_layout()
    
    return fig


def create_correlation_heatmap(data: pd.DataFrame) -> Optional[Figure]:
    """Create correlation heatmap for numerical columns."""
    numerical_data = data.select_dtypes(include=['number'])
    
    if numerical_data.shape[1] < 2:
        return None
    
    correlation_matrix = numerical_data.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#0e1117')
    
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        ax=ax,
        cbar_kws={'label': 'Correlation'},
        linewidths=0.5,
        linecolor='#30363d'
    )
    
    ax.set_facecolor('#161b22')
    ax.set_title("Correlation Matrix", fontweight='bold', color='#e6edf3', fontsize=12)
    ax.tick_params(colors='#e6edf3')
    
    fig.tight_layout()
    return fig


def create_boxplots(data: pd.DataFrame) -> Optional[Figure]:
    """Create boxplot visualizations for numerical columns."""
    numerical_data = data.select_dtypes(include=['number'])
    
    if numerical_data.empty:
        return None
    
    fig, axes = plt.subplots(1, len(numerical_data.columns), figsize=(4*len(numerical_data.columns), 5))
    fig.patch.set_facecolor('#0e1117')
    
    if len(numerical_data.columns) == 1:
        axes = [axes]
    
    for idx, col in enumerate(numerical_data.columns):
        ax = axes[idx]
        
        data_col = numerical_data[col].dropna()
        bp = ax.boxplot([data_col], labels=[col], patch_artist=True)
        
        # Customize boxplot colors
        for patch in bp['boxes']:
            patch.set_facecolor('#1f77b4')
            patch.set_alpha(0.7)
        
        for whisker in bp['whiskers']:
            whisker.set_color('#e6edf3')
        
        for median in bp['medians']:
            median.set_color('#f85149')
            median.set_linewidth(2)
        
        ax.set_facecolor('#161b22')
        ax.set_title(f"{col}", fontweight='bold', color='#e6edf3')
        ax.tick_params(colors='#e6edf3')
        ax.grid(axis='y', alpha=0.2, color='#30363d')
    
    fig.suptitle("Data Distribution (Boxplots)", fontsize=14, fontweight='bold', color='#e6edf3')
    fig.tight_layout()
    
    return fig


# ============================================================================
# Streamlit UI
# ============================================================================

def main():
    """Main Streamlit application."""
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'file_info' not in st.session_state:
        st.session_state.file_info = None
    
    # Header
    st.markdown("# 📊 Analytics Dashboard")
    st.markdown("*Data Analysis with Streamlit*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        
        upload_option = st.radio(
            "Choose data source:",
            ["Upload File", "Use Default File"]
        )
        
        data = None
        file_info = None
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload CSV file",
                type=['csv'],
                help="Upload a CSV file with any delimiter"
            )
            
            if uploaded_file:
                try:
                    delimiter = st.selectbox(
                        "CSV Delimiter",
                        [';', ',', '\t', '|'],
                        help="Select the delimiter used in your CSV file"
                    )
                    
                    file_bytes = uploaded_file.getvalue()
                    data = load_data_from_bytes(file_bytes, delimiter=delimiter)
                    file_info = f"📄 {uploaded_file.name}"
                    
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
        
        else:  # Use Default File
            default_file = "osb_tnatalidad.csv"
            if os.path.exists(default_file):
                try:
                    data = load_data(default_file)
                    file_info = f"📄 {default_file}"
                except Exception as e:
                    st.error(f"❌ Error loading default file: {str(e)}")
            else:
                st.warning(f"⚠️ Default file '{default_file}' not found")
        
        # Analysis options
        if data is not None:
            st.divider()
            st.subheader("📈 Visualization Options")
            
            show_histogram = st.checkbox("Show Histograms", value=True)
            show_correlation = st.checkbox("Show Correlation Matrix", value=True)
            show_boxplot = st.checkbox("Show Boxplots", value=True)
            
            st.divider()
            
            # Export options
            st.subheader("💾 Export")
            
            if st.button("📥 Export Report (PNG)", use_container_width=True):
                try:
                    # Create comprehensive figure
                    fig = create_histograms(data)
                    if fig:
                        png_buffer = io.BytesIO()
                        fig.savefig(png_buffer, format='png', dpi=300, bbox_inches='tight')
                        png_buffer.seek(0)
                        
                        st.download_button(
                            label="⬇️ Download Report",
                            data=png_buffer,
                            file_name="analytics_report.png",
                            mime="image/png",
                            use_container_width=True
                        )
                        logger.info("Report exported successfully")
                        st.success("✓ Report generated!")
                except Exception as e:
                    st.error(f"Error exporting report: {str(e)}")
    
    # Main content
    if data is not None:
        # Display file information
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Rows", f"{data.shape[0]:,}")
        with col2:
            st.metric("🔢 Columns", data.shape[1])
        with col3:
            missing = data.isnull().sum().sum()
            st.metric("❓ Missing Values", missing)
        with col4:
            numerical = len(data.select_dtypes(include=['number']).columns)
            st.metric("📈 Numerical Cols", numerical)
        
        st.divider()
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📉 Visualizations", "📋 Data Explorer", "🔍 Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Summary Statistics")
                with st.container(border=True):
                    st.code(get_data_summary(data), language="text")
            
            with col2:
                st.subheader("Data Types")
                with st.container(border=True):
                    st.code(get_data_types(data), language="text")
        
        with tab2:
            if show_histogram:
                st.subheader("📊 Distribution Histograms")
                fig = create_histograms(data)
                if fig:
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns to visualize")
            
            if show_correlation:
                st.subheader("🔗 Correlation Heatmap")
                fig = create_correlation_heatmap(data)
                if fig:
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.info("Need at least 2 numerical columns for correlation analysis")
            
            if show_boxplot:
                st.subheader("📦 Boxplots")
                fig = create_boxplots(data)
                if fig:
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns for boxplots")
        
        with tab3:
            st.subheader("📋 Data Preview")
            
            col1, col2 = st.columns(2)
            with col1:
                rows = st.slider("Rows to display:", 1, min(100, len(data)), 10)
            with col2:
                search_col = st.selectbox("Search in column:", ["All"] + list(data.columns))
            
            if search_col == "All":
                st.dataframe(data.head(rows), use_container_width=True)
            else:
                search_term = st.text_input(f"Search in {search_col}:")
                if search_term:
                    filtered = data[data[search_col].astype(str).str.contains(search_term, case=False)]
                    st.dataframe(filtered.head(rows), use_container_width=True)
                else:
                    st.dataframe(data.head(rows), use_container_width=True)
        
        with tab4:
            st.subheader("📊 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Missing Values Report")
                with st.container(border=True):
                    st.code(get_missing_values(data), language="text")
            
            with col2:
                st.subheader("Column Information")
                info_df = pd.DataFrame({
                    'Column': data.columns,
                    'Type': data.dtypes.values,
                    'Non-Null': data.count().values,
                    'Unique': [data[col].nunique() for col in data.columns]
                })
                st.dataframe(info_df, use_container_width=True)
        
        logger.info("Dashboard rendered successfully")
    
    else:
        st.info("👈 Upload a CSV file or select the default option to get started!")
        
        # Display sample structure
        st.subheader("📝 Expected CSV Format")
        st.markdown("""
        Your CSV file should have:
        - **Headers** in the first row
        - **Supported delimiters**: `;` `,` `\\t` `|`
        - **Data types**: Numerical and text columns
        
        Example:
        ```
        Column1;Column2;Column3
        Value1;123;456
        Value2;789;012
        ```
        """)


if __name__ == "__main__":
    main()
