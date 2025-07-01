Run a command, inside a specific container, from Docker...
- docker exec [options] <container_name> <command>
- docker exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-apps/submit/job.py
  - container_name = spark-master, command is spark-submit