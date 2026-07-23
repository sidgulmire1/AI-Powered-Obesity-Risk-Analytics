"""
ETL Module

Loads, inspects, cleans and saves the obesity dataset using PySpark.
"""

from spark.spark_session import get_spark_session
from pyspark.sql.functions import col, count, when, isnan
from pyspark.sql.types import (
    DoubleType,
    FloatType,
    IntegerType,
    LongType
)


class ETL:

    def __init__(self, file_path):

        self.spark = get_spark_session()
        self.file_path = file_path

        self.original_df = None
        self.cleaned_df = None

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    def load_data(self):

        self.original_df = (
            self.spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(self.file_path)
        )

        self.cleaned_df = self.original_df

        print("\nDataset Loaded Successfully.\n")

    # ==========================================================
    # DATASET INFORMATION
    # ==========================================================

    def dataset_info(self):

        print("=" * 70)
        print("RAW DATASET INFORMATION")
        print("=" * 70)

        print(f"Rows    : {self.original_df.count()}")
        print(f"Columns : {len(self.original_df.columns)}")

    # ==========================================================
    # SCHEMA
    # ==========================================================

    def show_schema(self):

        print("\nRaw Dataset Schema\n")

        self.original_df.printSchema()

    # ==========================================================
    # SAMPLE
    # ==========================================================

    def show_sample(self, rows=5):

        print("\nSample Records\n")

        self.original_df.show(rows, truncate=False)


    # ==========================================================
    # REMOVE DUPLICATES
    # ==========================================================

    def remove_duplicates(self):

        before = self.cleaned_df.count()

        self.cleaned_df = self.cleaned_df.dropDuplicates()

        after = self.cleaned_df.count()

        print(f"\nDuplicate Rows Removed : {before-after}")

    # ==========================================================
    # MISSING VALUE REPORT
    # ==========================================================

    def missing_value_report(self):

        print("\nMissing Value Report\n")

        expressions = []

        for field in self.cleaned_df.schema.fields:

            column = field.name
            datatype = field.dataType

            if isinstance(
                datatype,
                (DoubleType, FloatType, IntegerType, LongType)
            ):

                expressions.append(

                    count(

                        when(

                            col(column).isNull() |
                            isnan(col(column)),

                            column

                        )

                    ).alias(column)

                )

            else:

                expressions.append(

                    count(

                        when(

                            col(column).isNull(),

                            column

                        )

                    ).alias(column)

                )

        self.cleaned_df.select(expressions).show(
            vertical=True,
            truncate=False
        )

    # ==========================================================
    # CLEANED DATASET INFO
    # ==========================================================

    def cleaned_dataset_info(self):

        print("\n" + "=" * 70)
        print("CLEANED DATASET")
        print("=" * 70)

        print(f"Rows    : {self.cleaned_df.count()}")
        print(f"Columns : {len(self.cleaned_df.columns)}")

        self.cleaned_df.printSchema()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save_processed_data(self):

        output_path = "data/processed/clean_data.csv"
        print("\nColumns being saved:")
        print(self.cleaned_df.columns)
        print(f"Total columns: {len(self.cleaned_df.columns)}")

        self.cleaned_df.toPandas().to_csv(
            output_path,
            index=False
        )

        print("\nProcessed Dataset Saved Successfully")
        print(output_path)
        
        
        
        
        
    def remove_identifier_columns(self):

        columns_to_remove = [

            # IDs
            "ClassID",
            "TopicID",
            "QuestionID",
            "DataValueTypeID",
            "LocationID",
            "StratificationCategoryId1",
            "StratificationID1",

            # Metadata
            "Data_Value_Footnote",
            "Data_Value_Footnote_Symbol",
            
            "Data_Value_Alt",

    "Low_Confidence_Limit",

    "High_Confidence_Limit ",

    "Sample_Size"


        ]

        self.cleaned_df = self.cleaned_df.drop(*columns_to_remove)

        print("\nIdentifier and metadata columns removed.")

        print(f"Remaining Columns : {len(self.cleaned_df.columns)}")

    # ==========================================================
    # GET DATAFRAME
    # ==========================================================

    def get_dataframe(self):

        return self.cleaned_df
    
    
    # ==========================================================
# COLUMN PROFILE REPORT
# ==========================================================

    def column_profile(self):

        print("\n" + "=" * 90)
        print("COLUMN PROFILE REPORT")
        print("=" * 90)

        total_rows = self.cleaned_df.count()

        for column in self.cleaned_df.columns:

            print("\n" + "-" * 90)
            print(f"Column : {column}")

            dtype = dict(self.cleaned_df.dtypes)[column]
            print(f"Type   : {dtype}")

            missing = self.cleaned_df.filter(
                col(column).isNull()
            ).count()

            print(f"Missing Values : {missing}")

            unique = self.cleaned_df.select(column).distinct().count()

            print(f"Unique Values  : {unique}")

            print("Sample Values")

            self.cleaned_df.select(column).distinct().show(
                10,
                truncate=False
            )

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self):

        self.spark.stop()

        print("\nSpark Session Closed.\n")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    etl = ETL("data/raw/obesity.csv")

    etl.load_data()

    etl.dataset_info()

    etl.show_schema()

    etl.show_sample()

    etl.remove_duplicates()

    etl.missing_value_report()
    
    etl.remove_identifier_columns()

    etl.column_profile()

    etl.cleaned_dataset_info()

    etl.save_processed_data()

    print("\nETL Completed Successfully.\n")

    etl.stop()