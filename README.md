# created the vector encodings for the faces you want to accept from the /dataset folder
python3 encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# run this pointing it at the image that you would like to detect a face on
python3 face_detection.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle  --image dataset/chris/YOUR_IMAGE.jpg


#systemd service
face_detection.service -> /etc/systemd/system/
sudo system chmod 644 /etc/systemd/system/face_detection
systemctl daemon-reload
systemctl start face_detection.service
systemctl enable face_detection.service