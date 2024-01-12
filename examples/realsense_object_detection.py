# Load the Tensorflow model into memory.
import tensorflow as tf
import pyrealsense2 as rs
import numpy as np
import cv2



Path_to_cpth = "faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb" 

if __name__ == '__main__':

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v1.gfile.GFile(Path_to_cpth, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.compat.v1.import_graph_def(od_graph_def, name='')
        sess = tf.compat.v1.Session(graph=detection_graph)

    
    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    #Starting camear capturing
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    #Starting camera
    pipeline.start(config)

    #Get data
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    expanded_image = color_image[np.newaxis, ...]

    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                         feed_dict={image_tensor: expanded_image})

    colors_hash = dict()
    W = 1280
    H = 720

    for idx in range(int(num)):
        class_ = classes[0,idx]
        score = scores[0,idx]
        box = boxes[0,idx]

        if class_ not in colors_hash:
            colors_hash[class_] = tuple(np.random.choice(range(256), size=3))
        if score > 0.8:
            left = box[1] * W
            top = box[0] * H
            right = box[3] * W
            bottom = box[2] * H

            width = right - left
            height = bottom - top
            bbox = (int(left), int(top), int(width), int(height))
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # draw box
            r, g, b = colors_hash[class_]
            cv2.rectangle(color_image, p1, p2, (int(r), int(g), int(b)), 2, 1)

    # Display the image
    cv2.imshow('Detected Objects', color_image)

    # Wait for a key press and then close all open windows
    cv2.waitKey(0)
    pipeline.stop()
    cv2.destroyAllWindows()





