from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Click Event Count") \
    .getOrCreate()

# Read the CSV file from HDFS
df = spark.read.csv(
    "hdfs://hadoop-namenode:9000/input/events.csv",
    header=True,
    inferSchema=True
)

# Filter for 'click' events
clicks = df.filter(df["event_type"] == "click")

# Group by user_id and count the number of click events
click_counts = clicks.groupBy("user_id").count()

# Show the results in the console
click_counts.show()

# Write the results to HDFS
click_counts.write.csv(
    "hdfs://hadoop-namenode:9000/output/click_counts",
    mode="overwrite",
    header=True
)

# Stop the SparkSession
spark.stop()
