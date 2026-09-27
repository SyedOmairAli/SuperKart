
import streamlit as st
import pandas as pd
import requests


# Page settings
st.set_page_config(
    page_title=
    "SuperKart Sales Forecasting",
    layout="centered"
)


st.title(
    "SuperKart Sales Forecasting"
)

st.write(
    """
    Enter product and store information
    below to predict expected sales.
    """
)


# Backend Flask service
BACKEND_URL = "http://backend:7860"


# ----------------------------------
# Product Details
# ----------------------------------

st.subheader(
    "Product Information"
)


Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)


Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)


Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027,
    format="%.3f"
)


Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)


Product_Id_char = st.selectbox(
    "Product ID Category",
    [
        "FD",
        "DR",
        "NC"
    ]
)


Product_Type_Category = st.selectbox(
    "Product Type Category",
    [
        "Perishables",
        "Non Perishables"
    ]
)


# ----------------------------------
# Store Details
# ----------------------------------

st.subheader(
    "Store Information"
)


Store_Size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)


Store_Location_City_Type = (
    st.selectbox(
        "Store Location City Type",
        [
            "Tier 1",
            "Tier 2",
            "Tier 3"
        ]
    )
)


Store_Type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)


Store_Age_Years = st.number_input(
    "Store Age in Years",
    min_value=0,
    value=16
)


# ----------------------------------
# Prediction
# ----------------------------------

if st.button(
    "Predict Sales"
):

    payload = {

        "Product_Weight":
            Product_Weight,

        "Product_Sugar_Content":
            Product_Sugar_Content,

        "Product_Allocated_Area":
            Product_Allocated_Area,

        "Product_MRP":
            Product_MRP,

        "Store_Size":
            Store_Size,

        "Store_Location_City_Type":
            Store_Location_City_Type,

        "Store_Type":
            Store_Type,

        "Product_Id_char":
            Product_Id_char,

        "Store_Age_Years":
            Store_Age_Years,

        "Product_Type_Category":
            Product_Type_Category
    }


    try:

        response = requests.post(
            BACKEND_URL
            + "/v1/predict",
            json=payload
        )


        result = response.json()


        if (
            response.status_code == 200
            and
            "predicted_sales"
            in result
        ):

            st.success(
                "Predicted Sales: "
                f"{result['predicted_sales']:.2f}"
            )

        else:

            st.error(result)


    except Exception as e:

        st.error(
            f"""
            Unable to connect to
            prediction API: {e}
            """
        )


# ----------------------------------
# Batch Prediction
# ----------------------------------

st.divider()

st.subheader(
    "Batch Sales Prediction"
)


uploaded_file = (
    st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )
)


if uploaded_file is not None:

    st.write(
        "Uploaded data:"
    )

    preview_df = pd.read_csv(
        uploaded_file
    )

    st.dataframe(
        preview_df.head()
    )


    # Reset the uploaded file pointer
    uploaded_file.seek(0)


    if st.button(
        "Generate Batch Predictions"
    ):

        try:

            files = {

                "file":
                    (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )

            }


            response = requests.post(

                BACKEND_URL
                + "/v1/predictbatch",

                files=files

            )


            if (
                response.status_code
                == 200
            ):

                predictions = (
                    response.json()
                )

                result_df = (
                    preview_df.copy()
                )

                result_df[
                    "Predicted_Sales"
                ] = list(
                    predictions.values()
                )


                st.success(
                    """
                    Batch prediction
                    completed successfully.
                    """
                )


                st.dataframe(
                    result_df
                )


            else:

                st.error(
                    response.json()
                )


        except Exception as e:

            st.error(
                f"""
                Batch prediction
                failed: {e}
                """
            )
