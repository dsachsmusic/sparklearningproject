#pyspark.sql...
# - library for making sparksession ...we use it as the entry point...
# - ... for everything spark
# - ("sql" is a misnomer)...
#   - it doesn't just do structured data/doesn't just...
#     - sql queries 
#     - manipulate dataframes 
#     - ...(with pandas like syntax)
#   - it also does 
#     - RDD stuff (with sparksession)
#     - Hive stuff (old...Apache Hive databse...less used)
#       - SparkSession.builder.enableHiveSupport()
#     - streaming (microbatch, and continuous) stuff 
#        - SparkSession.builder.appName("StructuredStreaming")
# - it is also the library to do RDD with...
# ...sparksession and sparkcontext...there u)
# ...(not RDD ...we'd use RDD if 
# ...Java or Python objects...or some (other?) unstructured data/raw text, etc.)
# ...with RDD we'd use SparkContext (not spark session)
#...with SparkSession
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from datetime import datetime

# Initialize Spark
spark = SparkSession.builder \
    .appName("Log Parser RDD Job") \
    .getOrCreate()

sc = spark.sparkContext

# Load raw log lines (as RDD)
rdd = sc.textFile("hdfs://hadoop-namenode:9000/input/events.log")

# Parse log lines like: [2024-06-01 12:00:00] user_id=123 event=click
def parse_line(line):
    try:
        ts_part, rest = line.split("] ", 1)
        timestamp = ts_part.strip("[]")
        parts = rest.split()
        user_id = parts[0].split("=")[1]
        event_type = parts[1].split("=")[1]
        return (user_id, event_type, timestamp)
    except Exception as e:
        return None  # skip malformed lines

parsed_rdd = rdd.map(parse_line).filter(lambda row: row is not None)

# Filter for 'click' events
clicks = parsed_rdd.filter(lambda row: row[1] == "click")

# Convert to DataFrame
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("timestamp", StringType(), True),  # or use TimestampType with parsing
])
df = spark.createDataFrame(clicks, schema=schema)

# Group and count clicks per user
click_counts = df.groupBy("user_id").count()

# Output to HDFS
click_counts.write.csv(
    "hdfs://hadoop-namenode:9000/output/log_click_counts",
    mode="overwrite",
    header=True
)

spark.stop()

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
