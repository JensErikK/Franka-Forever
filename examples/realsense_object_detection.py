# Load the Tensorflow model into memory.
import tensorflow as tf
import pyrealsense2 as rs
import numpy as np
import cv2

Path_to_cpth = "faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb" 

Path_to_pptxt = "faster_rcnn_inception_v2_coco_2018_01_28/mscoco_label_map.pbtxt"


def load_label_map(label_map_path):
    label_map = {}
    with open(label_map_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 5):  # Process each item block
            id_line = lines[i+2].strip()  # Get the line with the id
            display_name_line = lines[i+3].strip()  # Get the line with the display_name

            # Extract the id number
            id_ = int(id_line.split(': ')[1])
            # Extract the display name
            display_name = display_name_line.split(': ')[1].replace('"', '')

            label_map[id_] = display_name
    return label_map

if __name__ == '__main__':

    #Label map for Id
    label_map = load_label_map(Path_to_pptxt)

    print(label_map)

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
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    #Starting camera
    pipeline.start(config)

    # Get the intrinsics of the color stream
    profile = pipeline.get_active_profile()
    color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
    intrinsics = color_profile.get_intrinsics()

    #Getting a frame for depth
    align_to = rs.stream.color
    align = rs.align(align_to)

    #Get data
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)

    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    if not aligned_depth_frame or not color_frame:
        print("Didnt get frame")
    
    depth_image = np.asanyarray(aligned_depth_frame.get_data())

    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    expanded_image = color_image[np.newaxis, ...]

    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                         feed_dict={image_tensor: expanded_image})

    colors_hash = dict()
    W = 1280
    H = 720

    for idx in range(int(num)):
        class_id = int(classes[0, idx])
        class_ = classes[0,idx]
        score = scores[0,idx]
        box = boxes[0,idx]

        if class_ not in colors_hash:
            colors_hash[class_id] = tuple(np.random.choice(range(256), size=3))
        if score > 0.8:
            class_name = label_map.get(class_id, 'N/A')
            left = box[1] * W
            top = box[0] * H
            right = box[3] * W
            bottom = box[2] * H

            #finding center of object
            center_x = int((left + right) // 2)
            center_y = int((top + bottom) // 2)
            pixel = [center_x, center_y]
            print(pixel) 
            depth = depth_image[center_y, center_x]
            print(depth)

            point = rs.rs2_deproject_pixel_to_point(intrinsics, pixel, depth)

            print(point)

            width = right - left
            height = bottom - top
            bbox = (int(left), int(top), int(width), int(height))
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # draw box
            r, g, b = colors_hash[class_id]
            cv2.rectangle(color_image, p1, p2, (int(r), int(g), int(b)), 2)

            label = f'{class_name}: {score:.2f}'
            cv2.putText(color_image, label, (p1[0], p1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(r), int(g), int(b)), 2)

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Display the image
    cv2.imshow('Detected Objects', color_image)

    cv2.imshow('RealSense Depth Image', depth_colormap)

    # Wait for a key press and then close all open windows
    cv2.waitKey(0)
    pipeline.stop()
    cv2.destroyAllWindows()





