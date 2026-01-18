import pandas as pd
import streamlit as st
import pickle
from config import BASE_DIR
# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Recommendation of Properties",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
    /* ---------- FORCE DARK BACKGROUND ---------- */
    .stApp {
        background-color: #0e1117;
    }

    /* ---------- REMOVE STREAMLIT WHITE BLOCKS ---------- */
    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
    }

    /* ---------- PROPERTY CARD ---------- */
    .property-card {
        background: linear-gradient(135deg, #1f2937, #111827) !important;
        color: #f9fafb !important;
        border-radius: 18px;
        padding: 5px;
        margin-bottom: 14px;
        border: 1px solid #374151;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        user-select: none;
        cursor: default;
    }

    .property-card h4 {
        margin: 0;
        color: #e5e7eb;
        font-size: 20px;
    }

    .property-card p {
        margin-top: 8px;
        color: #d1d5db;
        font-size: 15px;
    }

    .property-card:hover {
    transform: translateY(-2px);
    transition: 0.2s ease;
    box-shadow: 0 10px 22px rgba(0,0,0,0.12);
}


    /* ---------- REMOVE BLUE TEXT SELECTION ---------- */
    .property-card ::selection {
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏡 Property Recommendations")
st.markdown("---")

# ---------------- Load Data ----------------
location_df = pd.read_csv(BASE_DIR/"datasets"/"Location_data.csv")
location_df.set_index("PropertyName", inplace=True)

# ---------------- Inputs ----------------
area = st.selectbox("Select your Area", sorted(location_df.columns))
radius = st.number_input("Select Radius (in kms)", min_value=1, step=1)

# ---------------- Search Button ----------------
if st.button("Find Properties"):
    results_df = location_df[location_df[area] < radius * 1000]

    st.session_state["area"] = area
    st.session_state["radius"] = radius
    st.session_state["results_df"] = results_df
    st.session_state["search_results"] = results_df.index.to_list()
    st.session_state["selected_property"] = None

# ---------------- Display Results ----------------
if "results_df" in st.session_state:

    results_df = st.session_state["results_df"]

    st.success(
        f"Finding properties in {st.session_state['area']} "
        f"within {st.session_state['radius']} kms radius!"
    )

    st.write(f"### 🔍 Found {len(results_df)} properties")

    for prop in results_df.index:
        distance = results_df.loc[prop, st.session_state["area"]] / 1000

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(
    f"""
    <div class="property-card">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:22px;">🏢</span>
            <h4>{prop}</h4>
        </div>
        <p>📍 Distance: <b>{distance:.2f} km</b></p>
    </div>
    """,
    unsafe_allow_html=True
)



        with col2:
            if st.button("View", key=f"view_{prop}"):
                st.session_state["selected_property"] = prop
                st.rerun()
def show_property_basic_info(prop_name):
    if prop_name not in property_detail_df.index:
        st.warning("Property details not available.")
        return

    prop = property_detail_df.loc[prop_name]

    st.markdown("### 🏠 Property Overview")

    # -------- Two-column layout --------
    left_col, right_col = st.columns([2, 1])  # left wider than right

# ================= LEFT COLUMN =================
    with left_col:
    # ---- Property Name ----
     st.markdown(f"## {prop_name}")

    # ---- Sub Location ----
     st.markdown(f"📍 **Sub-Location:** {prop.get('PropertySubName', 'N/A')}")

    # ---- Property Link ----
     link = prop.get("Link", "")
     if pd.notna(link) and link != "":
        st.markdown(f"🔗 **More Details:** [Visit Property Page]({link})")

# ================= RIGHT COLUMN =================
    with right_col:
     facility = prop.get("TopFacilitiesStr", "")
     if pd.notna(facility) and facility != "":
        facility = facility.replace("[", "").replace("]", "")
        facilities_list = facility.split(", ")
        st.markdown("### 🛠️ Top Facilities")
        m=0
        for fac in facilities_list:
            m=m+1
            if m>5:
                break
            fac = fac.strip().strip("'").strip('"')
            st.markdown(
                f"""
                <span style="
                    background:#1f2937;
                    padding:6px 10px;
                    border-radius:10px;
                    display:inline-block;
                    margin:4px 0;
                    border:1px solid #374151;
                    color:#e5e7eb;
                    font-size:14px;
                ">
                {fac}
                </span>
                """,
                unsafe_allow_html=True
            )
# load cosine matrices
cosine_sim1 = pickle.load(open("streamlit\models\cosine_sim1.pkl",'rb'))
cosine_sim2 = pickle.load(open("streamlit\models\cosine_sim2.pkl",'rb'))
cosine_sim3 = pickle.load(open("streamlit\models\cosine_sim3.pkl",'rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.3*cosine_sim3 + 0.3*cosine_sim2 + 0.1*cosine_sim1

    idx = location_df.index.get_loc(property_name)

    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    top_scores = [i[1] for i in sim_scores[1:top_n+1]]

    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        "PropertyName": top_properties,
        "SimilarityScore": top_scores
    })
def show_recommendations(current_property):
    st.markdown("## 🔁 Recommended Properties")

    rec_df = recommend_properties_with_scores(current_property, top_n=5)

    for _, row in rec_df.iterrows():
        prop = row["PropertyName"]
        links = property_detail_df.loc[prop, "Link"]

        col1, col2 = st.columns([2, 1])

        with col1:
         st.markdown(
         f"""
         <div class="property-card">
            <h4>{prop}</h4>
            <p>For more details click below</p>
            <a href="{links}" target="_blank"
               style="
                   color:#60a5fa;
                   text-decoration:none;
                   font-weight:500;
               ">
               🔗 View Property Details
            </a>
        </div>
        """,
        unsafe_allow_html=True
         )

        with col2:
          if st.button("View", key=f"rec_view_{prop}"):
           st.session_state["selected_property"] = prop

           st.markdown(
            """
            <script>
            document.getElementById("property-details")
                    .scrollIntoView({behavior: "smooth"});
            </script>
            """,
            unsafe_allow_html=True
           )

           st.rerun()

    

    

 

# ---------------- Selected Property ----------------
if st.session_state.get("selected_property"):
    st.markdown("---")
    st.markdown('<div id="property-details"></div>', unsafe_allow_html=True)
    st.subheader("🏠 Selected Property")
    st.success(f"You selected: **{st.session_state['selected_property']}**")
    property_detail_df = pd.read_csv(BASE_DIR/"datasets"/"property_detail.csv")
    property_detail_df.set_index("PropertyName", inplace=True)
    show_property_basic_info(st.session_state["selected_property"])
    st.markdown("---")
    show_recommendations(st.session_state["selected_property"])


    