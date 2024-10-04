import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D  

def load_ModelNet_cat_name(file_path):
    # Open the text file and read lines into a list
    with open(file_path, "r") as file:
        data_list = file.readlines()

    # Strip newlines and whitespace from each line
    ModelNet_categories = [line.strip() for line in data_list]

    return ModelNet_categories

def plot_class_hist(data, dataset_name, vh_cat_name, main_dir):
    # Get ModelNet40 class prediction ans score
    class_id_all = data['class_id']
    score_all = data['score']*100

    # Setting 
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    plt.tight_layout(pad=3.0)
    bins_class = np.arange(0, 40, 1) # ModelNet 40 categories
    bins_score = np.arange(0, 105, 5) # 0-100 score

    # First subplot: histogram of class prediction 
    axs[0].hist(class_id_all, bins=bins_class, color='blue', edgecolor='black', alpha=0.7)  
    axs[0].set_title(f"Histogram of prediction: {dataset_name}, {vh_cat_name}")
    axs[0].set_xlabel('ModelNet40 class')
    axs[0].set_ylabel('Number of objects')

    # Second subplot: histogram of score
    axs[1].hist(score_all, bins=bins_score, color='blue', edgecolor='black', alpha=0.7)  
    axs[1].set_title(f"Histogram of score: {dataset_name}, {vh_cat_name}")
    axs[1].set_xlabel('Score')
    axs[1].set_ylabel('Number of objects')

    # Save the plot as an image
    plt.savefig(os.path.join(main_dir, "results", f"histogram_prediction_{vh_cat_name}.png"), dpi=300, bbox_inches='tight')

    print(f"Plots have been saved to 'histogram_prediction_{vh_cat_name}.png'.")

def get_ModelNet_cat_name_hist(data, vh_cat_name, main_dir):

    # Get class_id
    class_id_all = data['class_id']
    # Get histogram results: counts and bin edges
    bins = np.arange(0, 40, 1) # 40 classes from ModelNet
    counts, _ = np.histogram(class_id_all, bins=bins)

    # Get ModelNet category names
    file_path = os.path.join(main_dir, 'modelnet40_shape_names.txt')
    ModelNet_categories = load_ModelNet_cat_name(file_path)

    # Get the indices of non-zero values
    non_zero_cat_indices = np.nonzero(counts)[0]

    # Open a .txt file to save the results
    txt_file = os.path.join(main_dir, "results", f"histogram_prediction_{vh_cat_name}.txt")
    with open(txt_file, "w") as file:
        for class_id in non_zero_cat_indices:
            class_name = ModelNet_categories[class_id] # ModelNet class name
            class_count = counts[class_id]
            # Write to the file
            file.write(f"{class_name}: {class_count}\n")

    print(f"Results have been saved to 'histogram_prediction_{vh_cat_name}.txt'.")

def get_ModelNet_cat_name(data, vh_cat_name, main_dir):

    # Get object name, class_id ans score of a object
    class_id_all = data['class_id']
    score_all = data['score']*100
    object_name_all = data['object_name']

    # Get the indices of the sorted order based on object names
    sorted_indices = sorted(range(len(object_name_all)), key=lambda x: object_name_all[x])
    class_id_all = class_id_all[sorted_indices]
    score_all = score_all[sorted_indices]
    object_name_all = object_name_all[sorted_indices]

    # Get ModelNet category names
    file_path = os.path.join(main_dir, 'modelnet40_shape_names.txt')
    ModelNet_categories = load_ModelNet_cat_name(file_path)

    # Open a .txt file to save the results
    txt_file = os.path.join(main_dir, "results", f"class_prediction_{vh_cat_name}.txt")
    with open(txt_file, "w") as file:
        for idx, (name, class_id, score) in enumerate(zip(object_name_all, class_id_all, score_all)):
            class_name = ModelNet_categories[class_id] # ModelNet40 class name
            rounded_score = round(float(score), 1)
            # Write to the file
            file.write(f"{name}:{class_name}({rounded_score})\n")           

    print(f"Results have been saved to 'class_prediction_{vh_cat_name}.txt'.")

def plot_2d_tsne(data, dataset_name, vh_cat_name, main_dir):
    # Get class id and latent features extracted from a layer of DGCNN
    class_id_all = data['class_id']
    features = data['second-to-last_layer_outputs']
    
    # Perform t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    features_tsne = tsne.fit_transform(features)

    # Create a scatter plot with labels for coloring
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=features_tsne[:, 0], y=features_tsne[:, 1], hue=class_id_all, palette='viridis', s=30, legend='full')

    # Customize plot
    plt.title('The second-to-last layer outputs of DGCNN\n(cls_1024, ' + dataset_name + ', ' + 
            vh_cat_name + ', ' + str(features.shape[0]) + ' samples, ' + str(features.shape[1]) + ' features)')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.tight_layout()  # Adjust layout to make room for legend

    # Save the figure
    plt.savefig(os.path.join(main_dir, "results", f"tsne_dgcnn_cls_1024_second-to-last_{vh_cat_name}_modelnet40.png"), bbox_inches='tight')

if __name__ == "__main__":
    ## Setting 
    main_dir = r'/home/yiting/Documents/Shape_analysis/dgcnn_vh'
    dataset_name = 'vhObject'
    vh_cat_names = ["axial_component", "torso", "sheet", "all"]

    for vh_cat in vh_cat_names:
        data = np.load(os.path.join(main_dir, f"dgcnn_cls_{vh_cat}.npy"), allow_pickle=True).item()
        plot_class_hist(data, dataset_name, vh_cat, main_dir)
        plot_2d_tsne(data, dataset_name, vh_cat, main_dir)
        get_ModelNet_cat_name_hist(data, vh_cat, main_dir)
        get_ModelNet_cat_name(data, vh_cat, main_dir)




        

