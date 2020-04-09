from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry

ENDPOINT = "https://northcentralus.api.cognitive.microsoft.com"

# Replace with a valid key
training_key = "f9ca6ce9001f4fefa70aa71e2e74dc24"
prediction_key = "f9ca6ce9001f4fefa70aa71e2e74dc24"
prediction_resource_id = "/subscriptions/f74b3d72-3d7d-4953-b16a-0e4b045e66a7/resourceGroups/SdmAssignment5/providers/Microsoft.CognitiveServices/accounts/SdmAssignment5"

publish_iteration_name = "Iteration 1"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Create a new project
print ("Creating project...")
project = trainer.create_project("covid-19 image classifier")

# Make three tags in the new project
covid_19_image = trainer.create_tag(project.id, "covid -19 image")
illustrative_covid_19_image = trainer.create_tag(project.id, "illustrative covid-19 image")
info_graphic_covid_19_image = trainer.create_tag(project.id, "info graphic covid-19 image")


#Upload and tag images

base_image_url = "C:/Users/lokes/OneDrive/Documents/Classes/2nd sem/Social Data Mining/Assignment5"

print("Adding images...")

image_list = []

for image_num in range(1, 8):
    file_name = "{}.jpg".format(image_num)
    with open(base_image_url + "/covid-19 image/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[covid_19_image.id]))
        
for image_num in range(1, 8):
    file_name = "{}.jpg".format(image_num)
    with open(base_image_url + "/illustrative/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[illustrative_covid_19_image.id]))
        
for image_num in range(1, 9):
    file_name = "{}.jpg".format(image_num)
    with open(base_image_url + "/InfoGraphic/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[info_graphic_covid_19_image.id]))

        

upload_result = trainer.create_images_from_files(project.id, images=image_list)
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)
    
    
# Train the classifier and publish    
    
import time

print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")


# Get and use the published iteration on the prediction endpoint


from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Now there is a trained endpoint that can be used to make a prediction
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

with open(base_image_url + "/InfoGraphic/" + file_name, "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))