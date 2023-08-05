"""
NeurodataLab LLC 12.04.2019
Created by Andrey Belyaev
"""
import argparse
import json
import os
import os.path as osp
from time import sleep

import ndlapi.api.auth.Auth as Auth
from ndlapi.api.recognition.FaceDetection import FaceDetector
from ndlapi.api.recognition.EmotionRecognition import MultiFrameEmotionDetector, SingleFrameEmotionRecognition
from ndlapi.api.utils.image import Image
from ndlapi.api.utils.video import Video


# Parse command line arguments
def parse_args():
    # Parse arguments
    parser = argparse.ArgumentParser("python3 -m ndlapi")
    parser.add_argument('--cert-path', type=str, required=True, help='Path to folder with certificate files')
    parser.add_argument('--image-path', type=str, default=None, help='Path to image')
    parser.add_argument('--video-path', type=str, default=None, help='Path to video')
    parser.add_argument('-fd', action='store_true', default=False, help='Use FaceDetector (default=False)')
    parser.add_argument('-er-sf', '-er', action='store_true', default=False,
                        help='Use EmotionRecognition by SingleFrame network (default=False)')
    parser.add_argument('-er-mm', action='store_true', default=False,
                        help='Use EmotionRecognition by MultiModal network (default=False)')
    parser.add_argument('--out-path', type=str, default='result', help='Path to save result (default="result")')
    parser.add_argument('--api-url', type=str, default='emotionsdemo.com', help="API's url (default=emotionsdemo.com)")
    return parser.parse_args()


# Initialize secure connection
def initialize_connection(args):
    # Check arguments
    assert args.fd or args.er_sf or args.er_mm, \
        'Choose face detector (-fd) or emotion recognition (-er-[sf/mm]) to process'

    # Initialize paths
    cert_home = args.cert_path

    # Find certificate files
    cert_files = os.listdir(cert_home)
    client_crt_file, client_key_file, ca_crt_file, root_json_filepath = [''] * 4
    try:
        client_key_file = list(filter(lambda p: p.startswith('client') and p.endswith('.key'), cert_files))[0]
        client_crt_file = list(filter(lambda p: p.startswith('client') and p.endswith('.crt'), cert_files))[0]
        ca_crt_file = list(filter(lambda p: p.startswith('ca') and p.endswith('.crt'), cert_files))[0]
        root_json_filepath = list(filter(lambda p: p.startswith('root') and p.endswith('json'), cert_files))[0]
    except IndexError:
        print("You don't have all certificate's files. "
              "Please check for client_*.key, client_*.crt, ca_*.crt, root_*.json")
        exit(0)

    # Create common auth credentials
    ssl_auth_info = Auth.SslCredential(osp.join(cert_home, client_key_file),
                                  osp.join(cert_home, client_crt_file),
                                  osp.join(cert_home, ca_crt_file))

    auth = Auth.AuthCredential('%s:50051' % args.api_url, osp.join(cert_home, root_json_filepath), ssl_auth_info)

    # Create directory to store results
    if not osp.exists(args.out_path):
        os.mkdir(args.out_path)

    return auth


# Process image with face detector
def process_face_detector_image(fd, image_path, out_path):
    # Prepare image data from file
    image = Image.from_file(image_path)

    # Send image to server and get result
    # This is blocking operation
    image_result, status, error_msg = fd.on_image(image)

    # Print result or error
    if status == 2:
        print('Error when processing image:', error_msg)
    else:
        result = fd.postprocess_result(image_result)
        with open(osp.join(out_path, 'image_fd_result.json'), 'w') as f:
            json.dump(result, f, indent=2)


# Process video with face detector
def process_face_detector_video(fd, video_path, out_path):
    # Prepare video data
    video = Video.from_file(video_path)

    # Send video to server and get query object
    # This is non blocking operation
    query = fd.on_video(video)

    # Check query status
    while not query.finished():
        print('Query status:', query.status(),
              'Total progress:', query.total_progress(),
              'Workers progress:', query.worker_progress())
        sleep(0.5)

    # Catch query result
    video_result = query.result()

    # Check query errors
    if query.ok():
        result = face_detector.postprocess_result(video_result)
        with open(osp.join(out_path, 'fd_video_result.json'), 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print('Query error:', query.error())


# Process image with emotion recognition
def process_single_frame_emotion_recognition_image(er, image_path, out_path):
    # Prepare image data from file
    image = Image.from_file(image_path)

    # Send image to server and get result
    # This is blocking operation
    image_result, status, error_msg = er.on_image(image)

    # Print result or error
    if status == 2:
        print('Error when processing image:', error_msg)
    else:
        result = er.postprocess_result(image_result)
        with open(osp.join(out_path, 'image_er_result.json'), 'w') as f:
            json.dump(result, f, indent=2)


# Process image with emotion recognition
def process_single_frame_emotion_recognition_video(er, video_path, out_path):
    # Prepare video data
    video = Video.from_file(video_path)

    # Send video to server and get query object
    # This is non blocking operation
    query = er.on_video(video)

    # Check query status
    while not query.finished():
        print('Query status:', query.status(),
              'Total progress:', query.total_progress(),
              'Workers progress:', query.worker_progress())
        sleep(0.5)

    # Catch query result
    video_result = query.result()

    # Check query errors
    if query.ok():
        result = er.postprocess_result(video_result)
        with open(osp.join(out_path, 'er_sf_video_result.json'), 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print('Query error:', query.error())


# Process video with multi modal emotion recognition
def process_multi_modal_emotion_recognition_video(er, video_path, out_path):
    # Prepare video data
    video = Video.from_file(video_path)

    # Send video to server and get query object
    # This is non blocking operation
    query = er.on_video(video)

    # Check query status
    while not query.finished():
        print('Query status:', query.status(),
              'Total progress:', query.total_progress(),
              'Workers progress:', query.worker_progress())
        sleep(0.5)

    # Catch query result
    video_result = query.result()

    # Check query errors
    if query.ok():
        result = er.postprocess_result(video_result)
        with open(osp.join(out_path, 'er_mm_video_result.json'), 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print('Query error:', query.error())


if __name__ == '__main__':
    arguments = parse_args()
    ssl_auth = initialize_connection(arguments)

    if arguments.fd:
        face_detector = FaceDetector(ssl_auth)

        if arguments.image_path is not None:
            print("Start processing image with Face Detector " + arguments.image_path)
            process_face_detector_image(face_detector, arguments.image_path, arguments.out_path)
            print("Processing image done")

        if arguments.video_path is not None:
            print("Start processing video with Face Detector " + arguments.video_path)
            process_face_detector_video(face_detector, arguments.video_path, arguments.out_path)
            print("Processing video done")

    if arguments.er_sf:
        emotion_recognition = SingleFrameEmotionRecognition(ssl_auth)

        if arguments.image_path is not None:
            print("Start processing image with Emotion Recognition " + arguments.image_path)
            process_single_frame_emotion_recognition_image(emotion_recognition, arguments.image_path, arguments.out_path)
            print("Processing image done")

        if arguments.video_path is not None:
            print("Start processing video with Emotion Recognition " + arguments.video_path)
            process_single_frame_emotion_recognition_video(emotion_recognition, arguments.video_path, arguments.out_path)
            print("Processing video done")

    if arguments.er_mm:
        emotion_recognition = MultiFrameEmotionDetector(ssl_auth)

        if arguments.video_path is not None:
            print("Start processing video with Emotion Recognition " + arguments.video_path)
            process_multi_modal_emotion_recognition_video(emotion_recognition, arguments.video_path,
                                                          arguments.out_path)
            print("Processing video done")
