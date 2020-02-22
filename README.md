# securityCamera
# https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/

# use the faces in /dataset
python extract_embeddings.py --dataset dataset \
	--embeddings output/embeddings.pickle \
	--detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7

# train the model to recognize the faces
python train_model.py --embeddings output/embeddings.pickle \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle

# try to recognize faces in a still image
python recognize.py --detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle \
	--image images/YOUR_PHOTO.jpg

# try to recognize faces in live video stream
python recognize_video.py --detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle

# Dependencies
pip install --upgrade imutils
pip install opencv-contrib-python
pip install scikit-learn
