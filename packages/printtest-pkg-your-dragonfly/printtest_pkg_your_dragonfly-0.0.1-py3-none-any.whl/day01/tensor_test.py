def main_func(args, ctx):
    import numpy as np
    import tensorflow as tf
    import sys
    job_name = ctx.job_name
    task_index = ctx.task_index
    cluster, server = ctx.start_cluster_server(1, args.rdma)
    tf_feed = ctx.get_data_feed()

    def add_layer(inputs, insize, outsize, activation_func=None):
        Weights = tf.Variable(tf.random_normal([insize, outsize]))
        bias = tf.Variable(tf.zeros([1, outsize]) + 0.1)
        wx_plus_b = tf.matmul(inputs, Weights) + bias
        if activation_func:
            return activation_func(wx_plus_b)
        else:
            return wx_plus_b

    def rdd_generator():
        while not tf_feed.should_stop():
            batch = tf_feed.next_batch(1)
            if len(batch) == 0:
                return
            row = batch[0]
            x = np.array(row[0]).astype(np.float32)
            y = np.array(row[1]).astype(np.int64)
            yield (x, y)

    # x_data = np.linspace(-1,1,300)[:,np.newaxis]
    # noise = np.random.normal(0,0.05,x_data.shape)
    # y_data = np.square(x_data)  + noise
    if job_name == "ps":
        server.join()
    elif job_name == "worker":
        ds = tf.data.Dataset.from_generator(rdd_generator, (tf.float32, tf.float32)).batch(100)
        iterator = ds.make_one_shot_iterator()
        x, y_ = iterator.get_next()
        l1 = add_layer(x, 1, 10, activation_func=tf.nn.relu)
        preds = add_layer(l1, 10, 1, activation_func=None)

        global_step = tf.train.get_or_create_global_step()
        loss = tf.reduce_mean(tf.reduce_sum(tf.square(y_ - preds), reduction_indices=[1]))
        train = tf.train.GradientDescentOptimizer(0.05).minimize(loss, global_step=global_step)
        # Test trained labels
        saver = tf.train.Saver()
        init_op = tf.global_variables_initializer()
    logdir = ctx.absolute_path("my/log")
    # hooks = [tf.train.StopAtStepHook(last_step=2)]
    hooks = []
    with tf.train.MonitoredTrainingSession() as sess:
        sess.run(init_op)
        step = 0
        while not sess.should_stop() and not tf_feed.should_stop():
            _, preds_val, step = sess.run([train, preds, global_step])
            # if (step % 1 == 0) and (not sess.should_stop()):
    print("{} step of Values of predictions are:{}".format(step, preds_val))
    if step >= 10 or sess.should_stop():
        tf_feed.terminate()



