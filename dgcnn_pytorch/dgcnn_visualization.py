import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D  


def plot_class_hist(data, dataset_name, vh_category_name, main_dir):
    # data: ModelNet40 class prediction

    # Plotting the histogram
    plt.figure(figsize=(8, 6))  
    bins = np.arange(0, 40, 1) # ModelNet 40 categories
    plt.hist(data, bins=bins, color='blue', edgecolor='black', alpha=0.7) 

    # Customizing the plot
    plt.title('Histogram of prediction (' + dataset_name + ', ' + vh_category_name + ')')  
    plt.xlabel('ModelNet40 class')  
    plt.ylabel('Number of objects')  
    plt.xlim(0,40)

    # Save the plot as an image (optional)
    plt.savefig(os.path.join(main_dir, dataset_name, vh_category_name,'histogram_prediction.png'), dpi=300, bbox_inches='tight')

    # # Show the plot
    # plt.show()

def plot_2d_tsne(data, dataset_name, vh_category_name, main_dir):
    # data: latent features extracted from a layer of DGCNN

    # Perform t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    features_tsne = tsne.fit_transform(data)

    # Create a scatter plot with labels for coloring
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=features_tsne[:, 0], y=features_tsne[:, 1], hue=vh_label, palette='viridis', s=30, legend='full')

    # Customize plot
    plt.title('The second-to-last layer outputs of DGCNN\n(cls_1024, ' + dataset_name + ', ' + 
            vh_category_name + ', ' + str(features.shape[0]) + ' samples, ' + str(features.shape[1]) + ' features)')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.legend(fontsize = 10,title='Labels', bbox_to_anchor=(1.02, 1), loc='upper left')  # Optional legend positioning
    plt.tight_layout()  # Adjust layout to make room for legend

    # Save the figure
    plt.savefig(os.path.join(main_dir, dataset_name, vh_category_name, 'tsne_dgcnn_cls_1024_second-to-last.png'), bbox_inches='tight')

if __name__ == "__main__":
    ## Setting 
    main_dir = r'/home/yiting/Documents/GitHub/dgcnn.pytorch/layer_outputs'
    dataset_name = 'vhObject'
    vh_cat_names = ["axial_component", "torso", "sheet"]

    for vh_cat in vh_cat_names:
        modelnet_pred =  np.load(os.path.join(main_dir, dataset_name, vh_cat, 'modelnet_pred.npy')) # ModelNet 40 categories
        vh_label = np.load(os.path.join(main_dir, dataset_name, vh_cat, 'vhObject_label.npy')) # axial = 1, torso = 2, sheet = 3
        features = np.load(os.path.join(main_dir, dataset_name, vh_cat, 'second-to-last_layer_outputs.npy'))
        plot_class_hist(modelnet_pred, dataset_name, vh_cat, main_dir)
        plot_2d_tsne(features, dataset_name, vh_cat, main_dir)



        

