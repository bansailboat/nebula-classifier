# Nebulae Classification Using Transfer Learning

This tool was created to assist in the task of nebulae classification using the deep learning library TensorFlow coupled with a powerful image classification technique known as transfer learning.

## Setup and Installation

Begin by cloning the directory to the desired directory on your local machine and moving into it:
```bash
git clone https://github.com/bansailboat/nebula-classifier
cd nebula-classifier
```

It would be best to create a new environment to run the code. With conda, you can run:
```bash
conda create --name <env> --file requirements.txt
```
...passing in the desired name of the conda environment in place of `<env>`.

Then activate this environment using:
```bash
conda activate <env>
```
...passing in the name you designated for the new environment in place of `<env>`.

## Usage

This tool spins up a small web server using [Flask](http://flask.pocoo.org/) so that you don't have to operate from within the command line.

Run the following commands from the root of the project directory to get started in `localhost`:
```bash
export FLASK_APP=nebula_classifier
export FLASK_ENV=production
flask run
```

Navigate to the correct `localhost` port by simply right-clicking the output from the `flask run` command.

From within the web page, you can upload a nebula image and hit submit. Inference will then be run as the trained model attempts to classify the image. Usually in a second or so, the results will be outputted back to the page with confidence estimates.

## More Details, Please

At a high level, nebulae can classified among 6 major categories:
- Dark: So dense that it blocks emitted light from objects behind it
- Emission/H II regions: Emit spectral line radiation from excited/ionized gas
- Reflection: Reflect large amounts of light from nearby stars
- Planetary: Glowing shell of ionized gas ejected from red giant stars late in their lives
- Protoplanetary: The phase right before planetary
- Supernova remnant: Resulting structure of the explosion of a star during a supernova

This tool has been trained on hundreds of images for 2/6 of the categories, dark and emission nebulae.

### Compiling a list of nebulae

I began by researching the distinctions between the 6 different classifications, and then compiled a large list of actual nebulae that fell into each category. When compiling the nebulae, I made sure to include most alternative names/designations as well; for example, [NGC 2359](https://en.wikipedia.org/wiki/NGC_2359) is called NGC 2359 but it's also colloquially known among the astro community as Thor's Helmet. As a result, when I was collecting names, it looked a little like this:

```python
emission = ["Barnard's Loop", "NGC 7635", "California Nebula", ("Sh2-155", "Sharpless 155", "S155", "Cave Nebula"), ... ]
```
...where strings within this list were nebulae that typically only had that one designation but tuples were all designations.

### Image collection

This was by far the most time consuming part of this project. For each nebula in my compiled list, I would manually search for them on Google Images and then used a plugin called [Fatkun Batch Download Image](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf) to batch download hundreds of images at a time, making sure to exclude those that contained watermarks or other undesirable signal.

### Transfer learning

I wanted to use transfer learning because I knew I wouldn't be able to collect tens of thousands of images in the timeframe I was operating within. I used [this resource](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/?utm_campaign=chrome_series_machinelearning_063016&utm_source=gdev&utm_medium=yt-desc#0) to learn all about it and how powerful it is.

## Extending upon the model and/or retraining it

If you want to add more functionality by either adding other images or by retraining the model with more particular hyperparameters, here's how you can do that.

From the root of the project directory, run:

```bash
IMAGE_SIZE=224
ARCHITECTURE="mobilenet_1.0_${IMAGE_SIZE}"
```

The MobileNet we're using is configurable in 2 ways: input image resolution and the relative size of the model as a fraction of the largest MobileNet. The input image resolution options are 128, 160,192, or 224px. My model uses 224px because although this may take more time, it results in better accuracy. As for architecture, the options are 1.0, 0.75, 0.50, or 0.25. My model uses 1.0.

After this, we'll run:

```bash
python -m scripts.retrain \
  --bottleneck_dir=tf_files/bottlenecks \
  --how_many_training_steps=4000 \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" \
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=tf_files/nebula_photos
```

Next to the `--how_many_training_steps` flag, feel free to enter a number different from 4000.

The `retrained_graph.pb` file will now be updated such that when you re-run the flask web page and upload a new image, the new model will be the one being used.

## Contributing

Pull requests are (very) welcome, whether it be updating incorrect information about the nebula classification itself or the code. I'm just a passionate beginner interested in getting more involved in the field of astrophotography and imaging and would very much appreciate any and all expert feedback! :)

## License
[MIT](https://choosealicense.com/licenses/mit/)