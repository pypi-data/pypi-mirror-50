#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import base64
import tensorflow as tf

base64.b64decode()

os.system("kinit -kt ./dragonfly.lu.keytab dragonfly.lu@HCC.COM")
#os.environ["SPARK_HOME"] = "/opt/cloudera/parcels/SPARK2/lib/spark2"
os.environ["PYSPARK_PYTHON"] = "/bin/python"
#os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/bin/python2"
#os.environ["PYLIB"] = "/opt/cloudera/parcels/SPARK2/lib/spark2/python/lib/"


img_path = "hdfs://nameservice1/OWNER_USER/dragonfly.lu/dt_img_python2info/part_t0".encode("")
# IMAGE_DIR = '/home/dragonfly/data/part_t0'  # Path to folders of labeled images. HDFS path
OUTPUT_GRAPH = '/home/dragonfly/output_graph.pb'  # Where to save the trained graph. HDFS path
FINAL_TENSOR_NAME = 'result'  # The name of the output classification layer in the retrained graph.
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'


conf = SparkConf().setAppName("mydemo").setMaster("local[3]")
sc = SparkContext.getOrCreate(conf)
# spark = SparkSession.builder.enableHiveSupport().getOrCreate()
#
# spark.read.text()



with tf.gfile.FastGFile(OUTPUT_GRAPH, 'rb') as f:
    model_data = f.read()
    model_data_bc = sc.broadcast(model_data)
img_rdd = sc.textFile(img_path)

# parts = img_rdd.getNumPartitions()
# print("\n", img_rdd.first())


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


# 参数传入二进制数组
def apply_batch(image_url):
    with tf.Graph().as_default() as g:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(model_data_bc.value)
        #  _ =               name = ''
        _ = tf.import_graph_def(graph_def, name='')
        # image's binary array 需要的就是二进制数组
        image_data = image_url
        # image_data = urllib.request.urlopen(image_url, timeout=1.0).read()

    with tf.Session() as sess:
        # FINAL_TENSOR_NAME result
        softmax_tensor = sess.graph.get_tensor_by_name(FINAL_TENSOR_NAME + ":0")
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
            print(type(each))
            list_score.append(each)
        return "\t".join(list_score)




if __name__ == '__main__':
    i_rdd = img_rdd\
        .map(lambda line: splitData(line))\
        .filter(lambda x_y: None != x_y[0])\
        .filter(lambda x_y: ".jpg" in x_y[0])\
        .map(lambda x_y:  (x_y[0], apply_batch(x_y[1]))).map(
        lambda  x_y:  x_y[0] + ',' + x_y[1])

    i_rdd.saveAsTextFile("hdfs://nameservice1/OWNER_USER/dragonfly.lu/result")


