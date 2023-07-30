# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from PIL import Image
from sign_in import sign_in_page
from st_aggrid import AgGrid, ColumnsAutoSizeMode
import pandas as pd
from st_aggrid import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def run_custom_code():

    st.markdown("""
    <style id="customstyle">
    .stApp{    
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-image: url("flex_bg.png"); 
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                }
            </style>
            """, unsafe_allow_html=True)
    components.html("""

    
    """,
        height=0,
        width=0,
    )
    
    return 1


st.session_state["selected"] = ""
def streamlit_menu():
    st.session_state["selected"] = option_menu(
        menu_title=None,
        options=["Refresh", "Sign out"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "45px", "background-color": "transparent"},
            "icon": {"color": "#990033", "font-size": "16px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "right",
                "margin": "0px",
                "font-weight": "100",
                "background-color": "transparent"
            },
            "nav-link-selected": { "color":"#990033", "font-weight": "100", "background-color": "transparent"},
        },
    )
    return st.session_state["selected"]

def get_home_content():
    
    #top navigation
    with st.container():
        logo, empty1, empty2, menu = st.columns([4, 1, 1, 2], gap="large")

        with logo:
            ''
            logoimage = Image.open(r'flex.png')
            st.image(logoimage)
        
        with menu:
            st.session_state["selected"] = streamlit_menu()
            if st.session_state["selected"] == 'Sign out':
                st.session_state['sign_out_state'] = True
                st.session_state['active_session'].close()
                st.session_state = {}
                st.experimental_rerun()
                

    # h2 = st.markdown('''
        
    #     <h1 style="font-size: 30px; margin-top: 20px; padding: 5px 5px 0 5px;text-align: center;color:#990033">List Of Tables</h1>   
    #     ''', unsafe_allow_html=True)
    
    l,m,r = st.columns(3)

    with m:
        st.header('List Of Tables')
        

    # rows = run_query(''' select TABLE_CATALOG as DB, TABLE_SCHEMA,TABLE_NAME from "DEV_DWH_RAW"."INFORMATION_SCHEMA"."TABLES" where TABLE_SCHEMA='NETSUITE';''')
    
    if "active_session" in st.session_state:
       
        data_df = run_query('''SELECT * FROM DATA_DICT.PUBLIC.TABLE_METADATA ;''')
        df = pd.DataFrame(data_df, columns = ['DATABASE_NAME', 'TABLE_SCHEMA', 'TABLE_NAME', 'DESCRIPTION']) 

        with r:
            search_option = ['All']
            search_option.extend(df['TABLE_NAME'])
            search_term = st.selectbox("Search:", search_option)
            if search_term != 'All':
                df = df[df["TABLE_NAME"] == search_term]

        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(10)
        gd.configure_selection(selection_mode='single')

        gd.configure_default_column(editable=True,groupable=True,wrapText=True, autoHeight=True)
        gridoptions = gd.build()

        # gridoptions = {'defaultColDef': 
        # {'minWidth': 5, 'editable': True, 'filter': True, 'resizable': True, 'sortable': True, 'enableRowGroup': True},
        #  'columnDefs': [
        #     {'headerName': 'DATABASE_NAME', 'field': 'DATABASE_NAME', 'type': [], 'editable':False},
        #      {'headerName': 'TABLE_SCHEMA', 'field': 'TABLE_SCHEMA', 'type': [],'editable':False},
        #       {'headerName': 'TABLE_NAME', 'field': 'TABLE_NAME', 'type': [],'editable':False},
        #        {'headerName': 'Help', 'field': 'Help', 'type': [],'editable':True}],
        #         'pagination': True, 'paginationAutoPageSize': True, 'rowSelection': 'single', 'rowMultiSelectWithClick': False, 'suppressRowDeselection': False, 'suppressRowClickSelection': False, 'groupSelectsChildren': False, 'groupSelectsFiltered': True}
        
        grid_tb = AgGrid(df,gridOptions=gridoptions,height = 520,width=150,wrapText=True, autoHeight=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,reload_data = True,theme='alpine')

        if grid_tb["selected_rows"]:
            sel_row = grid_tb["selected_rows"][0]
            table = sel_row['TABLE_NAME']
            help_data = sel_row['DESCRIPTION']
            if sel_row:
                help_df = pd.DataFrame({"Table Name": [table],
                                        "DESCRIPTION": [help_data]})
                st.session_state['help_df'] = help_df

            else:
                help_df = st.session_state['help_df']

            st.subheader('Description')
            help_response = AgGrid(help_df, editable=True,height = 100, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW, wrapText=True, autoHeight=True)
            updated_help = help_response['data']['DESCRIPTION'].iloc[0]

            # st.write(updated_help)
            if sel_row and (updated_help != help_data):
                st.write("Query call for updating table to :",updated_help,": from :",help_data)
                
                # st.write(f'''UPDATE FIVETRAN_DATABASE.PUBLIC.TABLE_METADATA SET DESCRIPTION='{updated_help}' WHERE TABLE_NAME='{table}';''')
                run_query(f'''UPDATE DATA_DICT.PUBLIC.TABLE_METADATA SET DESCRIPTION='{updated_help}' WHERE TABLE_NAME='{table}';''')
                st.experimental_rerun()
            if sel_row:    
                col_list = run_query(f"SELECT COLUMN_NAME,DATA_TYPE,DESCRIPTION FROM DATA_DICT.PUBLIC.COLUMN_METADATA WHERE TABLE_NAME='{table}';")
                st.subheader(f"Columns in table: {table}")
                col_df =  pd.DataFrame(col_list, columns = ['COLUMN NAME', 'DATA TYPE', 'DESCRIPTION']) 
                grid_options = {
                    "columnDefs": [
                        {
                            "headerName": "COLUMN NAME",
                            "field": "COLUMN NAME",
                            "editable": False,
                        },
                        {
                            "headerName": "DATA TYPE",
                            "field": "DATA TYPE",
                            "editable": False,
                        },
                        {
                            "headerName": "DESCRIPTION",
                            "field": "DESCRIPTION",
                            "editable": True,
                            "wrapText": True, 
                            "autoHeight":True
                        },
                    ],
                }
                st.session_state['col_response'] = AgGrid(col_df, grid_options, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW, reload_data = True)['data']

                if 'col_response' in st.session_state:
                    comparison_df = pd.concat([st.session_state['col_response'], col_df])
                    # comparison_df[comparison_df[]]
                    comparison_df = comparison_df.mask(comparison_df.eq('None')).dropna().drop_duplicates(keep=False).reset_index(drop=True)
                    # st.dataframe(comparison_df)
                    # st.dataframe(st.session_state['col_response'])
                    # st.dataframe(col_df)
                    # st.write(comparison_df.empty, len(comparison_df['DESCRIPTION']))
                    if not comparison_df.empty and (len(comparison_df['DESCRIPTION']) >=1):
                        if len(comparison_df['DESCRIPTION'] == 2) and ((len(comparison_df['DESCRIPTION'] == 1)) or (comparison_df['DESCRIPTION'].iloc[0] != comparison_df['DESCRIPTION'].iloc[1])):
                            updated_desc = comparison_df['DESCRIPTION'].iloc[0]
                            selected_col_name = comparison_df['COLUMN NAME'].iloc[0]
                            # st.write("Query call for updating table to :",updated_desc)            
                            st.write(f'''UPDATE DATA_DICT.PUBLIC.COLUMN_METADATA SET DESCRIPTION='{updated_desc}' WHERE COLUMN_NAME='{selected_col_name}' AND TABLE_NAME='{table}';''')
                            run_query(f'''UPDATE DATA_DICT.PUBLIC.COLUMN_METADATA SET DESCRIPTION='{updated_desc}' WHERE COLUMN_NAME='{selected_col_name}' AND TABLE_NAME='{table}';''')
                            st.experimental_rerun()

                        # elif len(comparison_df['DESCRIPTION'] == 1):
                        #     st.write("Query call for updating table to :",updated_desc)            
                        #     st.write(f'''UPDATE FIVETRAN_DATABASE.PUBLIC.COLUMN_METADATA SET DESCRIPTION='{updated_desc}' WHERE COLUMN_NAME='{selected_col_name}' AND TABLE_NAME='{table}';''')
                            # run_query(f'''UPDATE FIVETRAN_DATABASE.PUBLIC.COLUMN_METADATA SET DESCRIPTION='{updated_desc}' WHERE COLUMN_NAME='{selected_col_name}' AND TABLE_NAME='{table}';''')
                            # st.experimental_rerun()

                st.subheader(f"Joins in table: {table}")
                joins = run_query(f"SELECT F.FKCOLUMN_NAME AS FKEY_COLUMN_NAME,F.PKTABLE_NAME AS REFERENCE_TABLE, F.PKCOLUMN_NAME AS REFERENCE_COLUMN, T.SCHEMA_NAME AS REFERENCE_TABLE_SCHEMA FROM DATA_DICT.PUBLIC.FKEYS F JOIN DATA_DICT.PUBLIC.TABLE_METADATA T ON T.TABLE_NAME=F.PKTABLE_NAME WHERE F.FKTABLE_NAME='{table}';")
                join_df = pd.DataFrame(joins, columns = ['FKEY_COLUMN_NAME', 'REFERENCE_TABLE', 'REFERENCE_COLUMN', 'REFERENCE_TABLE_SCHEMA']) 
                AgGrid(join_df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)
    return 

# Initialize connection.
# Uses st.experimental_singleton to only run once.
#st.session_state['active_session']

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
def run_query(query):
    with st.session_state['active_session'].cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def data_display():

    with st.container():
        get_home_content()
        run_custom_code()
        # if st.session_state["selected"] == "Sign out":
        #     st.session_state['active_session'].close()
        #     sign_in_page()
        # Note: Don't remove the run custom code call---------------------------------------------------------   
        
