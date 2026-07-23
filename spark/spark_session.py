"""
spark_session.py
----------------
Creates and returns a SparkSession for the project.
"""

from pyspark.sql import SparkSession


def get_spark_session(app_name="AI Powered Obesity Risk Analytics"):
    """
    Creates and returns a Spark Session.

    Returns:
        SparkSession: Configured Spark session.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


if __name__ == "__main__":
    spark = get_spark_session()

    print("=" * 50)
    print("Spark Session Created Successfully")
    print(f"Spark Version : {spark.version}")
    print("=" * 50)

    spark.stop()