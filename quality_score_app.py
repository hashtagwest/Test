import streamlit as st
import pandas as pd
import io

def calculate_quality_scores(input_data):
    """Calculates quality scores based on user input."""
    scores = {}
    for platform, data in input_data.items():
        score = (data['metric1'] * 0.4) + (data['metric2'] * 0.6)  # Example calculation
        scores[platform] = score
    return scores

def save_results_excel(results):
    """Saves results to an Excel (.xlsx) file."""
    df = pd.DataFrame(list(results.items()), columns=['Platform', 'Quality Score'])
    st.dataframe(df)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Quality Scores')
    buffer.seek(0)

    st.download_button(
        label="Download Results as Excel (.xlsx)",
        data=buffer,
        file_name="quality_scores.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

def main():
    st.title("Platform Quality Score Calculator")

    # Initialize session state variables if they don't exist
    if 'input_data' not in st.session_state:
        st.session_state.input_data = {}
    if 'results' not in st.session_state:
        st.session_state.results = None

    platform_names = ["Platform A", "Platform B", "Platform C"]  # Add your platform names

    # User Input
    for platform in platform_names:
        st.subheader(f"Enter data for {platform}")
        metric1 = st.number_input(f"{platform} Metric 1", value=st.session_state.input_data.get(platform, {}).get('metric1', 0.0), key=f"metric1_{platform}")
        metric2 = st.number_input(f"{platform} Metric 2", value=st.session_state.input_data.get(platform, {}).get('metric2', 0.0), key=f"metric2_{platform}")
        st.session_state.input_data[platform] = {"metric1": metric1, "metric2": metric2}

    if st.button("Calculate Scores"):
        st.session_state.results = calculate_quality_scores(st.session_state.input_data)
        st.subheader("Quality Scores:")
        for platform, score in st.session_state.results.items():
            st.write(f"{platform}: {score}")

    if st.session_state.results: # only shows the save button if there are results.
        if st.button("Save Results"):
            save_results_excel(st.session_state.results)

if __name__ == "__main__":
    main()