Copy sample csv file to namenode and and use hdfs commands to add it to hdfs
- docker cp ./data/events.log hadoop-namenode:/tmp/events.log
- docker exec -it hadoop-namenode bash
- hdfs dfs -mkdir -p /input
- hdfs dfs -put /tmp/events.csv /input/
- hdfs dfs -ls /input
  - This one is optional, it checks that the file exists

Submit the spark job
- docker exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-apps/submit/job.py

Look 
- Spark Master UI: http://localhost:8080
- HDFS Namenode Web UI: http://localhost:9870

Read output from HDFS
- docker exec -it hadoop-namenode hdfs dfs -ls /output/click_counts