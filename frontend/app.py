import streamlit as st
import requests

API_URL = "http://localhost:8000/data"

st.set_page_config(page_title="Cancer Genomics Research Tool", layout="centered")

st.title("Cancer Genomics Research Tool")
st.caption("Research Assistant Tool - Not for Clinical Use")
st.divider()

col1, col2 = st.columns(2)

with col1:
    cancer_type = st.selectbox("Cancer Type", ["Breast", "Lung"])

with col2:
    gene = st.text_input("Gene Symbol", value="TP53").strip().upper()

search = st.button("Search", type="primary")

if search and gene:
    with st.spinner("Getting the data from cBioPortal..."):
        try:
            response = requests.get(API_URL, params={"cancer_type": cancer_type, "gene": gene})
            data = response.json()
        except Exception as e:
            st.error(f"Could not reach the backend: {e}")
            st.stop()

    if "error" in data:
        st.error(data["error"])
        st.stop()

    st.subheader(f"{data['gene']} in {data['cancer_type']} Cancer")

    mf = data["mutation_frequency"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Mutated Samples", mf["mutated_samples"])
    col2.metric("Total Samples", mf["total_samples"])
    col3.metric("Mutation Rate", f"{mf['percentage']}%")

    st.divider()

    if data["common_mutations"]:
        st.subheader("Top Mutations")
        mutations = data["common_mutations"]
        labels = [m["amino_acid_change"] for m in mutations]
        counts = [m["count"] for m in mutations]

        chart_data = {"Mutation": labels, "Count": counts}
        st.bar_chart(chart_data, x="Mutation", y="Count")

        st.table(
            [
                {"Amino Acid Change": m["amino_acid_change"], "Type": m["type"], "Count": m["count"]}
                for m in mutations
            ]
        )

    st.divider()
    st.caption(data["disclaimer"])