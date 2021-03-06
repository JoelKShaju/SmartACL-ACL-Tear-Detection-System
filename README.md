# ACL-Tear-Detection
Detect Anterior Cruciate Ligament (ACL) tear by analyzing MRI scans.

* This project aims to detect and expedite the complete process of Detecting an ACL by analyzing MRI scans. Deep Learning was used to classify an MRI scan to ACL tear or Normal or any other Abnormality. 
* The components involved in the entire system is a database to store data that will be received from the users, a backend model to classify the MRI scan and a frontend web application that serves as the User Interface of the system. 
* For the backend there are four models in total. Three CNNs and a Softmax Regression. Since there are three different planes in each MRI Scan, three different CNN Models for each plane is built. 
* The input is given to the system by the user through the web interface. The input consists of images from three different planes, i.e., Coronal, Sagittal and Axial planes. These separate images are fed to the CNN model where the probability of the three classes (Normal, Abnormal, ACL) is predicted
by a Softmax Layer. 
* Each image of a plane has different number of slices therefore, each CNN model is iterated according to the number of slices. The probabilities from each iteration is then aggregated. The aggregated probability from each CNN Model acts as an input to the Softmax Regression Model. 
* The output of the Softmax Regression Model will be either an ACL Tear or Normal or any other Abnormality. Finally, this model is integrated with a web application so that users can upload their scans and get the results. Flowchart of the backend model is as shown below.

![alt text](https://github.com/JoelKShaju/ACL-Tear-Detection/blob/main/images/system_architecture.png)

## Deep Learning Models Architecture and Description:
* CNN models for Axial, Coronal and Sagittal Plane: A typical MRI for a patient consists of three scans, for the three planes. These three MRI scans act as input represented on three different anatomical planes: Coronal, Sagittal and Axial in the structure. The function of these CNN models is to find the probability of the three classes (Normal, Abnormal, ACL) and forward the output to the Softmax Regression model.

* Softmax Regression model: Softmax regression is a generalization of logistic regression where multiple classes are handled to normalize an input value into a vector of values that follows a probability distribution whose total sums up to 1. The output values are between the range [0,1] in order to avoid binary classification and accommodate as many classes or dimensions in a neural network model. Here, we use this model as a final step towards our prediction. This model takes input, which is the output of the three CNN models and finds the probability of the three classes by taking into account all the three planes.

### Architecture:

![alt text](https://github.com/JoelKShaju/ACL-Tear-Detection/blob/main/images/final_architecture.png)

## Results:

![alt text](https://github.com/JoelKShaju/ACL-Tear-Detection/blob/main/images/confusion_matrix.jpg)

* A confusion matrix was used to check the accuracy of the final Softmax model. It was generated by testing the model with data other than the training data. The dataset consisted of 377 cases; 124 ACL cases, 188 Abnormal cases and 65 Normal Cases. The accuracy obtained according to the confusion matrix is 90.8%. The results of the Softmax model as seen in the confusion matrix are as follows:
1. 65 cases out of 65 cases of the Normal class. 100% were detected properly.
2. 162 cases out of 188 cases of the Abnormal class. 86.20% were detected 
properly.
3. 111 cases out of 124 cases of the ACL class. 89.50% were detected properly.

# Training the models:
* The CNN models were trained in kaggle. The file is available [here](https://github.com/JoelKShaju/ACL-Tear-Detection/blob/main/training/CNN_Training.ipynb).
* The softmax model was trained locally. The file is available [here](https://github.com/JoelKShaju/ACL-Tear-Detection/blob/main/training/softmax_reg.ipynb).
