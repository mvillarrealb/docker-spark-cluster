https://spark.apache.org/docs/latest/tuning.html

### empacotamento 

#### (OBSOLETO) empacotar as lib usadas do virtualenv com ven-pack
venv-pack -o pyspark_venv.tar.gz

#### empacotar com pex
- https://github.com/pex-tool/pex
- https://medium.com/criteo-engineering/packaging-code-with-pex-a-pyspark-example-9057f9f144f3

pex $(pip freeze) -o venv_app01.pex


### submeter para spark
 https://spark.apache.org/docs/latest/submitting-applications.html
#### execução como client remoto
spark-submit app01/main.py

#### execução no cluster 
spark-submit --master spark://192.168.2.5:7077 app01/main.py

## Provisioning 
https://medium.com/@swethamurali03/apache-spark-executors-cba87f3de78d#:~:text=Executors%20are%20responsible%20for%20actually,node%20can%20have%20multiple%20executors.
https://spoddutur.github.io/spark-notes/distribution_of_executors_cores_and_memory_for_spark_application.html#:~:text=Number%20of%20available%20executors%20%3D%20(total,node%20%3D%2030%2F10%20%3D%203

We want multi threading on each executor , at the same time throughput should also not get affected. It is observed, HDFS achieves full write throughput with ~5 tasks per executor, which means we can allot ~5 cores for each executor to get optimal performance .

Calculating total number of executors in the cluster
We have 10 Node cluster with, 16 CPU cores anf 64 GB RAM on each node .

1 core goes for background processes and 1GB RAM is given to OS. We have 15 code CPU and 64 GB RAM.

Doing a optimal cut, we can have 3 executors — 5 CORES and 21 GB RAM each.

Off-Heap Memory
This is memory outside the JVM heap space, used for off-heap storage (like caching), reducing GC overhead.

off heap memory = MAX(384 MB, 7% of executor memory)

In our case, 7% of executor memory ( 7 % of 21 GB = 1.5 GB) goes to off heap memory. 19 GB remaining to be allotted for executors.

Total Executors
Each executor has 5 cores and 19 GB RAM, with 3 executors per node, making it 30 executors across the cluster.
One goes for YARN application manager, resulting in 29 executors on the cluster.
How many tasks can run in parallel
Each executor can run 5 tasks in parallel ( 5 Cores each) and and with 3 executors in each node, 15 tasks can run in parallel on a node
Across the cluster, 150 tasks can run in parallel.