# created the vector encodings for the faces you want to accept from the /dataset folder
python3 encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# run this pointing it at the image that you would like to detect a face on
python3 pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle  --image dataset/chris/YOUR_IMAGE.jpg
