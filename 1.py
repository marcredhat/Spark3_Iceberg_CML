#https://github.com/pdefusco/Spark3_Iceberg_CML

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder\
  .appName("1.1 - Ingest") \
  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", "us-east-2")\
  .config("spark.yarn.access.hadoopFileSystems", "s3a://demo-aws-go02")\
  .config("spark.jars","/home/cdsw/lib/iceberg-spark3-runtime-0.9.1.1.13.317211.0-9.jar") \
  .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
  .config("spark.sql.catalog.spark_catalog","org.apache.iceberg.spark.SparkSessionCatalog") \
  .config("spark.sql.catalog.local","org.apache.iceberg.spark.SparkCatalog") \
  .config("spark.sql.catalog.local.type","hadoop") \
  .config("spark.sql.catalog.spark_catalog.type","hive") \
  .getOrCreate()
spark.sql("CREATE DATABASE IF NOT EXISTS spark_catalog.testdb")
spark.sql("USE spark_catalog.testdb")
spark.sql("SHOW CURRENT NAMESPACE").show()
spark.sql("CREATE TABLE IF NOT EXISTS newtesttable (id bigint, data string) USING iceberg")
spark.sql("SELECT * FROM spark_catalog.testdb.newtesttable")
spark.read.format("iceberg").load("spark_catalog.testdb.newtesttable.history").show(20, False)
spark.sql("INSERT INTO spark_catalog.testdb.newtesttable VALUES (1, 'x'), (2, 'y'), (3, 'z')")
spark.sql("SELECT * FROM spark_catalog.testdb.newtesttable").show()
spark.read.format("iceberg").load("spark_catalog.testdb.newtesttable.history").show(10, False)
