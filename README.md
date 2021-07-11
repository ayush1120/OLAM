# OLAM
OLAM: A Devanagari OCR employing Neural Networks

![sdsad](https://github.com/ayush1120/OLAM/blob/master/olam.jpeg?raw=true)

Download Data from [link to data](https://drive.google.com/drive/folders/1CCaW7ko7GzwvQ-a_5yqv8DUlieQjUizm?usp=sharing), and put it in datagen folder.

Code Links:

- [Object Detection Co-Lab - Models Based on Config](https://colab.research.google.com/drive/1ZrBp7oJbDJUqXAIJJsXWJcCZ2AjI2Cfk?usp=sharing)
- [CRNN Training Notebook Co-lab](https://colab.research.google.com/drive/1F6KzFQLgAZ80bfrtBRnDfh2R_bX6w07B?usp=sharing)
- [Data Generation Code &amp; Analysis - GitHub](https://github.com/ayush1120/OLAM/tree/master)

Data Links:

- [Text &amp; Line Segmentation Model Data](https://drive.google.com/file/d/1-1BewHFMQ-54YDUKRAk6Xc-dSLvGjAsX/view)
- [Line to Word Segmentation Data](https://drive.google.com/file/d/1M9xwqh1PyRbxvjyYVu7ISQmboDDK0Q0p/view)
- [Word Sequence Detection Data](https://drive.google.com/file/d/17km6sW3Zn4HoDjiD2exxIvE1Ox61rJA8/view?usp=sharing)

Model Links:

- [Object Segmentation Models](https://drive.google.com/drive/folders/1IYyx6wyjqPVCQ-fG9BIZ8s-vHvyGjxbF?usp=sharing)
- [Word Sequence Detection Model](https://drive.google.com/file/d/1yQ5F35i_quQeIk3PYk7zYcyGfc1SnOig/view?usp=sharing)

**Objective and Potential Applications:**

Olam is a Neural Network based OCR for languages in the Devanagari Script family currently supporting Hindi. The proposed model can be optimized and implemented to tackle challenges across several Human-to-Machine as well as Machine-to-Machine interaction domains. Consumer Businesses can use this to adaptively widen their reach and expand their market to remote areas by understanding data in Hindi (Devanagari script better). Recruiters and Consultants can use this to provide solutions to clients beyond their current operational languages and hire regional talent surmounting the Language barrier. Academicians can extract and decipher long texts and Primary Sources in Hindi/Hindustani, a language that finds prevalence in quite a few Administrative records across regions and eras. Beyond that, Devanagari has been of critical aid in deciphering numerous historical edicts and texts of rich Cultural Heritage. An OCR equipped with and optimized for predicting phrases in columns can be of great use in decoding them. Today, Devnagri enjoys a massive usage by more than 608 million people across 120 different languages, from Hindi and Sanskrit to Nepali and Marathi, thus a project on this can positively impact many lives on a huge proportion across regions and cultures. Socially, much Legal information/documentation and Medical prescriptions as standard follow English or Hindi as their media for exchange which may not be very accessible to local populations in many regions of India. A Hindi based OCR can act as a bridge to streamline the translation of vital information into native languages/scripts quickly. Which can be a great social equalizer to the regional populace in terms of access to mainstream information and vital prescriptions. Consumer tools built around this can highly aid migrants and travelers traveling in Hindi speaking areas, helping them in capturing and translating signboards/Direction/Station Boards. This can also be of great value to translators or people looking to pick up the language who encounter it in Non-Digital form, say while reading a Newspaper. Such Handy tools can also bring cultures closer through streamlining everyday interactions like reading a Food Menu or the Local journal in different tongues, highly adding to the first-hand experience of traveling.

**Approach:**

**Nature of Dataset:** The dataset for the model will be a huge collection of images with labeled bounding boxes around text, lines, words, and characters. We are going to create our dataset using the following approach:

We make a Python program to write text in Hindi on an image using libraries like Pillow and Opencv. Doing so we can easily compare the two successive images as we have White (later on introducing different sorts of backgrounds to make the model even robust) background and textual content is written in Black to find the pixel of the most recent word/ character. Once we have the pixel values of the new region we can pad the extremes of this region to form bounding boxes around the word. We can augment the data by changing the background color, using different text sizes. Further adding random noise or blurriness to the images can also be considered as an expansion of the dataset. Addition of this noise makes the generated images closer to photos of documents in grayscale.

**Dataset**

Hindi Text data is taken from Hindi data from [HC corpora: Collection of corpora for various language](https://web.archive.org/web/20161021044006/http://corpora.heliohost.org/)

**Code For Data Preparation:**
[https://github.com/ayush1120/OLAM/tree/master](https://github.com/ayush1120/OLAM/tree/master)

**Inference**

Due to a lack of Hindi grammatical rules, the function detected some words which were incorrect upon character segmentation. Thus analyzing such words helped us preprocess the data used to generate the Image Data set for training the model.

1. There were around 800 words that start with a dependent vowel.
  1. &#39;ॅषिकेश, &#39;ूबाजार, &#39;ंिचंताजनक, &#39;ेलेकिन, &#39;ँँँँँअविनाश
2. There were some words with half vowels which
  1. &#39;जकिउ्द्दीन&#39;, &#39;कोइ्रü&#39;, &#39;गइ्र&#39;, &#39;कोइ्र्र&#39;, &#39;हुइ्र्र&#39;, &#39;जाए्गा।&#39;, &#39;हुइ्र्र&#39;, &#39;सुरमइ्रर्&#39;, &#39;जुलार्इ्र&#39;, &#39;कोइ्र&#39;, &#39;उ्देश्य&#39;, &#39;राष्अ्रपति&#39;, &#39;आइ्र&#39;, &#39;स्काउ्ट्स&#39;, &#39;चढार्इ्&#39;, &#39;&#39;&#39;देखो-श्-अ्!&#39;&#39;&#39;, &#39;कोई्र&#39;, &#39;हेडलाइ्ट्स&#39;
3. There were some words that have half consonants followed by a dependent vowel.
  1. जलर्ापूत्ति, वष्ाीüय, विशेष्ा, घोष्ाणा, चट््टानें&#39;

**Challenges and Redirections:**

- The Segmentation Model Architecture will have to be reiterated time and again for obtaining a more accurate model.

- Pillow currently doesn&#39;t have sufficient support for prominent Devnagari fonts and thus we had to make do with the not so popular alternative fonts that it does.
 (Ref: [https://github.com/python-pillow/Pillow/issues/3191](https://github.com/python-pillow/Pillow/issues/3191)**)**

- Different fonts have varying rules for merging advanced (half) consonants. Hence for character segmentation, there can emerge an ambiguity in how we choose the correct bounding box.

- It was a bit challenging to coordinate tasks and timings being away from campus.

**Modeling:**

Currently, our model pipeline consists of 3 different learnable models that work together to attempt to reach our final goal of detecting the written letters from an optical image. We choose YOLO as a base model for object detection because the YOLO model is fast enough to be used in a scenario requiring real-time speeds in processing the image keeping the same accuracy as previous state-of-the-art models. Along with this, YOLO also learns a more general representation of the underlying structure The three models have their details as described below:

**Text/Line detection model:**

This is the first model in our pipeline which takes as input a full image with words written in Hindi and detects the lines or the text boxes based on which type of data the model is trained for. We use the current model for directly detecting the lines as that was the best we could do given the constraints.

This is an object detection model which is based on the YOLO architecture. To be more precise, we use the YOLO-SPP model for detecting the lines in the image.

SPP stands for Spatial Pyramid Pooling which is used to increase the mAP(mean Average Precision) of the model which is used to detect the lines. The YOLO-SPP model takes the best features in the max-pooling layers along with the downsampling from the convolutional layers which is what a traditional full-size YOLO model does.

We have trained the YOLO-SPP model to around 3.0 average IOU values as provided by the darknet implementation of YOLO.

![](RackMultipart20210711-4-1hwhj4j_html_e606877ef3e19e8.png)

**Word Detection Model:**

The next model in our pipeline is again an Object detection model based on YOLO which takes the input of the lines we have segmented from the previous model. This model is not based on the full-sized YOLO but the smaller Tiny-YOLO architecture. This design decision was based on the fact that any image may contain a multitude of lines which will again run through the word detection model each time. Thus to make sure that the complete pipeline is not slowed down due to running on each image separately. The Tiny-YOLO model is a good fit for our needs and also provides good enough accuracy.

We have again trained the Tiny-YOLOmodel to around 3.0 average IOU values as provided by the darknet implementation of YOLO, similar to the YOLO-SPP model. There is room for improvement but the time constraints were severe and we were unable to train the model further.

**CRNN word to sequence model:**

The final model in our pipeline is a CRNN model written in Keras and TensorFlow which uses bi-directional LSTMs built on top of a conventional convolutional network to identify the correct sequence of characters in the given words which have been identified by the previous models. The model we have constructed is based on the research paper [**An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition**](https://arxiv.org/pdf/1507.05717.pdf).

This model has been trained using the connectionist Temporal Classification(CTC) loss function. The model was trained for 10 epochs but reached a point of diminishing returns sooner than expected and the validation loss started increasing at the 8th epoch. We still continued training and the validation loss did not decrease giving us the impression that the model was being overfitted at that point. We have chosen the model with the lowest validation loss as the best model for our final pipeline.

All three models described above can be found in the [drive](https://drive.google.com/drive/folders/1eVi9cPwUxkURQUeeQXnvc2HkvmHXGlLS?usp=sharing) folder. The object detection models contain their respective special builds of darknet along with all the extra needed files to mitigate any problems which may arise due to minor changes in the code. The code is also compiled to be run on the CPU instead of GPU as most &quot;consumer&quot; GPUs would not be able to handle the model size of YOLO-SPP and would return a &quot;CUDA: Out of memory&quot; error, and it would also render the compiled binary being unusable on machines without NVIDIA GPUs supporting CUDA. Nevertheless, the complete training was carried out on GPUs provided by collab and the model was saved.

Although the accuracy achieved so far illustrates considerable progress from where we were a few weeks back, there is still room for improvement. We have been tackling constraints in terms of computing resources available on Google Colab as well as Time on our hands given it&#39;s currently a hectic phase for our batch. Nevertheless, we as a group are continuously working on optimizing OLAM parallel to all other undertakings and expect to achieve considerably improved accuracy through more rigorous training of the model as well as improving the architecture of our models.
