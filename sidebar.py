import streamlit as st


def show(show_slider=False):
    st.markdown(
        """
    <style>
    section[data-testid="stSidebar"] {
        background-color: #2F4A6D;
        border-right: 1px solid #8B949E;
    }
    section[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"],
    nav[data-testid="stSidebarNav"],
    ul[data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavItems"],
    header[data-testid="stSidebarNavSeparator"] {
        display: none !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        try:
            st.image(str("./logo/logo.png"))
            st.markdown(
                "## <span style='font-size: 2.5rem; font-weight: 800;'>TARDIS</span>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.markdown(
                "## <span style='font-size: 2.5rem; font-weight: 800;'>TARDIS</span>",
                unsafe_allow_html=True,
            )
            st.error(f"Logo introuvable : {e}")

        st.divider()

        if st.button("Accueil", width="stretch"):
            st.switch_page("tardis_dashboard.py")
        if st.button("Analyse", width="stretch"):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("Prédictions des retards", width="stretch"):
            st.switch_page("pages/2_Delays_prediction.py")
        if st.button("Informations", width="stretch"):
            st.switch_page("pages/3_Info.py")

        st.divider()

        if show_slider:
            start_year, end_year = st.slider(
                "Années",
                min_value=2018,
                max_value=2025,
                value=(2018, 2025),
            )
            return start_year, end_year

    return None, None
