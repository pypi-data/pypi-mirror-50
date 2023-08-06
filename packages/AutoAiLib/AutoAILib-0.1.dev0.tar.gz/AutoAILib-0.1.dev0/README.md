# AutoAI
This repository is a compilation of scripts that I have created in my time working with machine learning. These scripts aim to automate the annoying and silly parts of ML, allowing you to focus on what is important.
<h2> AutoAi.manual_test(model, testing_dir, labels) </h2>
<h5> This function tests a model given labels and testing data. It then compiles the results in a CSV file, and groups the results by class, and by correct and incorrect.</h5>
<ul> 
  <li> Model - Path of model that you want to test or model object.</li>
  <li> Testing_dir - Path to the directory with your testing data.</li>
  <li> Labels - Dictionary of the classes, in form (index:class_name)</li>
  </ul>
<h2> AutoAi.compile_data(src, dest, num_imgs_per_class=0, train_ratio=.7, validation_ratio=.2, test_ratio=.1) </h2>
<h5 This function takes 2 required arguments, an original data source file, and a path to the desired data directory. Given just these two arguments, this function will create a new testing data folder at dest with training, validation, and testing folders, containing folders for each class. You can alter the ratio with the ratio arguments, as well as provide a number of img transforms to do if you are using images.</h5>
<ul>
  <li> Src - Path to a folder that contains a folder for each class and then data examples in those class folders. </li>
  <li> Dest - Path to a folder where you want the data to end up. </li>
  <li> Num_imgs_per_class - This number of images will be added to the original set for each class through transforms. The theoretical limit for this would be 3! * original images per class </li>
  </ul>
