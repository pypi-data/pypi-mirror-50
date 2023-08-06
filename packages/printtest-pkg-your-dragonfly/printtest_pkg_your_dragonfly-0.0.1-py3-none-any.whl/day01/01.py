#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import base64


os.system("kinit -kt /home/dragonfly/dragonfly.lu.keytab dragonfly.lu@HCC.COM")
# os.environ["SPARK_HOME"] = "/opt/cloudera/parcels/SPARK2/lib/spark2"
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python"
# os.environ["PYSPARK_PYTHON"] = "/bin/python3"
# os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/bin/python3"


img_path = "hdfs://nameservice1/OWNER_USER/dragonfly.lu/test"
OUTPUT_GRAPH = '/home/dragonfly/output_graph.pb'  # Where to save the trained graph. HDFS path
FINAL_TENSOR_NAME = 'result'  # The name of the output classification layer in the retrained graph.
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'


conf = SparkConf().setAppName("mydemo").setMaster("local[3]")
sc = SparkContext.getOrCreate(conf)
spark = SparkSession.builder.enableHiveSupport().getOrCreate()
sql = "select * from dragonfly_lu.test"
row = spark.sql(sql).rdd

img_rdd = row.map(lambda row: row[0]).map(lambda x : str(x).split("\t"))



# img_rdd = sc.textFile(img_path)

def splitData(x):
    y = x.split("\t")
    if 2 == len(y) and ".jpg" in y[0]:
        return (y[0], y[1])
    else:
        return (None, None)

def tensorFlowDeal(img_info):

    img_data = base64.b64decode(img_info)
    img_real = []
    for i in range(10):
        img_real.append(str(img_data[i]))
    return ",".join(img_real)
'''
# 参数传入二进制数组
def apply_batch(image_url):

    graph_1 = tf.GraphDef()
    graph_1.ParseFromString(model_data_bc.value)
    _ = tf.import_graph_def(graph_1, name='')
        # image's binary array 需要的就是二进制数组
    image_data = image_url
        # image_data = urllib.request.urlopen(image_url, timeout=1.0).read()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('result:0')

        predictions = sess.run(softmax_tensor, {JPEG_DATA_TENSOR_NAME: image_data})
        # print(predictions)

        # f.write('%s' % image)
        # for score in predictions[0]:
        #     f.write(',{:.6f}'.format(score))
        # f.write('\n')
        #
        # _progress(index, len(image_list))
        # 对应每张图的 所有特征 类型 list
        list_score = list()
        for score in predictions[0]:
            each = '{:.6f}'.format(score)
            #print(type(each))
            list_score.append(each)
        return ",".join(list_score)
'''
#if __name__ == '__main__':
i_rdd = img_rdd\
        .filter(lambda x_y: None != x_y[0])\
        .filter(lambda x_y: ".jpg" in x_y[0])\
        .map(lambda x_y:  (x_y[0], x_y[1])).map(
        lambda  x_y:  x_y[0] + ',' + x_y[1])

        # .map(lambda line: splitData(line))\
i_rdd.saveAsTextFile("hdfs://nameservice1/OWNER_USER/dragonfly.lu/tensor_demo")
# i_rdd.saveAsTextFile("file:\\\\\\" + "/home/dragonfly/data/reslout")
