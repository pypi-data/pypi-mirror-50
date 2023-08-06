from pyspark.context import SparkContext
from pyspark.conf import SparkConf
# from tensorflowonspark import TFCluster,TFNode
from pyspark.sql import SparkSession
from day01 import tensor_test

def showResout(x):
    print(x)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rdma", help="use rdma connection", default=False)
    args = parser.parse_args()
    spark = SparkSession.builder \
              .getOrCreate()
    #conf = SparkConf().setAppName("ceshi")
    #sc = SparkContext(conf=conf)
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    import numpy as np
    x_data = np.linspace(-1,1,300)[:,np.newaxis]
    noise = np.random.normal(0,0.05,x_data.shape)
    y_data = np.square(x_data) + noise
    x_data_rdd = sc.parallelize(x_data)
    y_data_rdd = sc.parallelize(y_data)
    in_rdd = x_data_rdd.zip(y_data_rdd)

    # in_rdd.foreach(lambda ax: showResout(ax))


    num_executors = 4
    # num_executors = int(sc._conf.get("spark.executor.instances"))
    # num_executors = int(executors) if executors is not None else 1
    tensorboard = False
    num_ps = 1
    cluster = TFCluster.run(sc, tensor_test.main_func, args,
                            num_executors,
                            num_ps,
                            tensorboard,
                            TFCluster.InputMode.SPARK)
    cluster.train(in_rdd, 1)  # 1 代表epochs
    print("Done===")
    cluster.shutdown()
    
    





