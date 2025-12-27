import streamlit as st
from streamlit_autorefresh import st_autorefresh
import home
def get_data():
    st_autorefresh(interval=60 * 1000, key="dataframerefresh")

    df1 = home.economics()
    hide_table_row_index = """
                                                                                                                                                                                  <style>
                                                                                                                                                                                  tbody th {display:none}
                                                                                                                                                                                  .blank {display:none}
                                                                                                                                                                                  </style>
                                                                                                                                                                                  """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    th_props = [
        ('font-size', '17px'),
        ('text-align', 'center'),
        # ('font-weight', 'bold'),
        ('color', '#FF7F50'),

    ]

    td_props = [
        ('font-size', '17px'),
        ('color', '#2E8B57'),
    ]

    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]

    df2 = df1.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df2)
    # with col2:
    #     df2 = home.cnbc()
    #     hide_table_row_index = """
    #                                                                                                                                                                                               <style>
    #                                                                                                                                                                                               tbody th {display:none}
    #                                                                                                                                                                                               .blank {display:none}
    #                                                                                                                                                                                               </style>
    #                                                                                                                                                                                    """
    #     st.markdown(hide_table_row_index, unsafe_allow_html=True)
    #
    #     th_props = [
    #         ('font-size', '17px'),
    #         ('text-align', 'center'),
    #         # ('font-weight', 'bold'),
    #         ('color', '#FF7F50'),
    #
    #     ]
    #
    #     td_props = [
    #         ('font-size', '17px'),
    #         ('color', '#2E8B57'),
    #     ]
    #
    #     styles = [
    #         dict(selector="th", props=th_props),
    #         dict(selector="td", props=td_props)
    #     ]
    #
    #     df2 = df2.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    #     st.table(df2)
    # with col3:
    #     df5 = home.bloomberg()
    #     hide_table_row_index = """
    #                                                                                                                                                                                               <style>
    #                                                                                                                                                                                               tbody th {display:none}
    #                                                                                                                                                                                               .blank {display:none}
    #                                                                                                                                                                                               </style>
    #                                                                                                                                                                                    """
    #     st.markdown(hide_table_row_index, unsafe_allow_html=True)
    #
    #     th_props = [
    #         ('font-size', '17px'),
    #         ('text-align', 'center'),
    #         # ('font-weight', 'bold'),
    #         ('color', '#FF7F50'),
    #
    #     ]
    #
    #     td_props = [
    #         ('font-size', '17px'),
    #         ('color', '#2E8B57'),
    #     ]
    #
    #     styles = [
    #         dict(selector="th", props=th_props),
    #         dict(selector="td", props=td_props)
    #     ]
    #
    #     df3 = df5.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    #     st.table(df3)
    # col1, col2 = st.columns(2)
    # with col1:
    #     df1 = home.earning()
    #     hide_table_row_index = """
    #                                                                                                                                                                                          <style>
    #                                                                                                                                                                                          tbody th {display:none}
    #                                                                                                                                                                                          .blank {display:none}
    #                                                                                                                                                                                          </style>
    #                                                                                                                                                                                          """
    #     st.markdown(hide_table_row_index, unsafe_allow_html=True)
    #
    #     th_props = [
    #         ('font-size', '17px'),
    #         ('text-align', 'center'),
    #         # ('font-weight', 'bold'),
    #         ('color', '#FF7F50'),
    #
    #     ]
    #
    #     td_props = [
    #         ('font-size', '17px'),
    #         ('color', '#2E8B57'),
    #     ]
    #
    #     styles = [
    #         dict(selector="th", props=th_props),
    #         dict(selector="td", props=td_props)
    #     ]
    #
    #     df2 = df1.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    #     st.table(df2)
    # with col2:
    #     df2 = home.bt()
    #     hide_table_row_index = """
    #                                                                                                                                                                                                      <style>
    #                                                                                                                                                                                                      tbody th {display:none}
    #                                                                                                                                                                                                      .blank {display:none}
    #                                                                                                                                                                                                      </style>
    #                                                                                                                                                                                           """
    #     st.markdown(hide_table_row_index, unsafe_allow_html=True)
    #
    #     th_props = [
    #         ('font-size', '17px'),
    #         ('text-align', 'center'),
    #         # ('font-weight', 'bold'),
    #         ('color', '#FF7F50'),
    #
    #     ]
    #
    #     td_props = [
    #         ('font-size', '17px'),
    #         ('color', '#2E8B57'),
    #     ]
    #
    #     styles = [
    #         dict(selector="th", props=th_props),
    #         dict(selector="td", props=td_props)
    #     ]
    #
    #     df2 = df2.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    #     st.table(df2)