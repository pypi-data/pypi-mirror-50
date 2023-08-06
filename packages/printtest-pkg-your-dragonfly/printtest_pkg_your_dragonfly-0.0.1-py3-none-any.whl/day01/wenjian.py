
# from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

import tensorflow as tf
import base64


IMAGE_DIR = '/home/dragonfly/data/part_t0'  # Path to folders of labeled images. HDFS path
OUTPUT_GRAPH = './output_graph.pb'  # Where to save the trained graph. HDFS path
FINAL_TENSOR_NAME = 'softmax'  # The name of the output classification layer in the retrained graph.
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'

# spark = SparkSession.builder.appName("myapp_test").getOrCreate()

conf = SparkConf().setAppName("myTestDemo").setMaster("local[2]")
sc = SparkContext.getOrCreate(conf)


# img_rdd = spark.read.text(IMAGE_DIR).rdd
img_rdd = sc.textFile(IMAGE_DIR)


# 读取模型分发给各个节点 ， 以后可以作成 hdfs目录，每次关联目录就行，

with tf.gfile.FastGFile(OUTPUT_GRAPH, 'rb') as f:
    model_data = f.read()
    model_data_bc = sc.broadcast(model_data)


score_rdd = img_rdd.map(lambda x: {x[0],
                       apply_batch(base64.b64decode(x[1]))
                       })

# tt.show();
# tt.write.mode(SaveMode.Overwrite).saveAsTable("test05")

# score_rdd.write.mode(SaveMode.Overwrite).saveAsTable("reslout")






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
        softmax_tensor = sess.graph.get_tensor_by_name("softmax:0")
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


















# Base64 String  转化成 二进制数组


print(type(rawData))
rawData.collect()
sc.stop()


