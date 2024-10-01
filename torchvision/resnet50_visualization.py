import numpy as np
import os
import matplotlib.pyplot as plt
from torchvision.models import resnet50, ResNet50_Weights

def plot_class_hist(data, vh_cat_name, main_dir):
    # Get class_id and score
    class_id_all = data['class_id']
    score_all = data['score']*100

    # Setting 
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    plt.tight_layout(pad=3.0)
    bins_class = np.arange(0, 1000, 1) # 1000 classes from ImageNet
    bins_score = np.arange(0, 105, 5) # 0-100 score
    

    # First subplot: histogram of class prediction 
      
    axs[0].hist(class_id_all, bins=bins_class, color='blue', edgecolor='black', alpha=0.7)  # 'bins' sets the number of bins
    axs[0].set_title(f"Histogram of prediction: {vh_cat_name}")
    axs[0].set_xlabel('ImageNet class')
    axs[0].set_ylabel('Number of objects')

    # Second subplot: histogram of score
    axs[1].hist(score_all, bins=bins_score, color='blue', edgecolor='black', alpha=0.7)  # 'bins' sets the number of bins
    axs[1].set_title(f"Histogram of score: {vh_cat_name}")
    axs[1].set_xlabel('Score')
    axs[1].set_ylabel('Number of objects')

    # Save the plot as an image (optional)
    fig.savefig(os.path.join(main_dir, "results", f"histogram_prediction_{vh_cat_name}.png"), dpi=300, bbox_inches='tight')

    print(f"Plots have been saved to 'histogram_prediction_{vh_cat_name}.png'.")

def get_ImageNet_cat_name(data, vh_cat_name, main_dir):

    # Get class_id
    class_id_all = data['class_id']
    # Get histogram results: counts and bin edges
    bins_class = np.arange(0, 1000, 1) # 1000 classes from ImageNet
    counts, _ = np.histogram(class_id_all, bins=bins_class)

    # Get category names
    weights = ResNet50_Weights.DEFAULT
    ImageNet_categories = weights.meta["categories"]

    # Get the indices of non-zero values
    non_zero_cat_indices = np.nonzero(counts)[0]

    # Open a .txt file to save the results
    txt_file = os.path.join(main_dir, "results", f"histogram_prediction_{vh_cat_name}.txt")
    with open(txt_file, "w") as file:
        for class_id in non_zero_cat_indices:
            class_name = ImageNet_categories[class_id] # ImageNet class name
            class_count = counts[class_id]
            # Write to the file
            file.write(f"{class_name}: {class_count}\n")

    print(f"Results have been saved to 'histogram_prediction_{vh_cat_name}.txt'.")

if __name__ == "__main__":
    ## Setting 
    main_dir = r'/home/yiting/Documents/Shape_analysis/resnet50_vh'
    vh_cat_names = ["axial_component", "torso", "sheet"]

    for vh_cat in vh_cat_names:
        data = np.load(os.path.join(main_dir, f"resnet50_{vh_cat}.npy"), allow_pickle=True).item()
        plot_class_hist(data, vh_cat, main_dir)
        get_ImageNet_cat_name(data, vh_cat, main_dir)