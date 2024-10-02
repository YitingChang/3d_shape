import os
import numpy as np
from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights

def resnet50_vh(img):

    # Step 1: Initialize model with the best available weights
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()

    # Step 2: Initialize the inference transforms
    preprocess = weights.transforms()

    # Step 3: Apply inference preprocessing transforms
    batch = preprocess(img).unsqueeze(0)

    # Step 4: Use the model and print the predicted category
    prediction = model(batch).squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    score = prediction[class_id].item()
    category_name = weights.meta["categories"][class_id]

    return class_id, score

if __name__ == "__main__":
    ## Setting 
    # Get the 2D image (png) folder
    main_dir = r'/home/yiting/Documents/Data/Shapes/png_no_base'
    # Save dir
    save_dir = r'/home/yiting/Documents/Shape_analysis/resnet50_vh'
    # Get the category folders
    category_folders = os.listdir(main_dir)

    for cat in category_folders:
        # Get input file
        png_category_path = os.path.join(main_dir,cat)
        png_files = os.listdir(png_category_path)

        # Get Resnet50 classification outputs
        class_outputs = []
        score_outputs = []

        for png_file in png_files:
            img = read_image(os.path.join(png_category_path, png_file))
            class_id, score = resnet50_vh(img)
            class_outputs.append(class_id)
            score_outputs.append(score)
        
        # Save the classification and score outputs as .npy file
        data = {'class_id' : np.array(class_outputs), 'score': np.array(score_outputs)}
        save_file = os.path.join(save_dir, f"resnet50_{cat}.npy")
        np.save(save_file, data)
    
        print(f"Processed {cat} objects.")
        print(f"Saved Resnet50 classification and score outputs to {save_file}.")