from PIL import Image
import os

def crop_image(input_file, output_file):

    # Load an image
    image = Image.open(input_file)

    # Define the cropping box (left, upper, right, lower), original image size: 1920x1080
    crop_box = (0, 0, 1920, 615)

    # Crop the image using the box
    cropped_image = image.crop(crop_box)

    # # Show the cropped image (optional)
    # cropped_image.show()

    # Save the cropped image
    cropped_image.save(output_file)


if __name__ == "__main__":

    ### Setting ###
    main_dir = r'/home/yiting/Documents/Data/Shapes'
    # Get the input folder path
    input_folder_dir = os.path.join(main_dir, 'png')
    # Get the category folders
    category_folders = os.listdir(input_folder_dir)
    # Get the output (png) folder path
    output_folder_dir = os.path.join(main_dir, 'png_no_base')

    for cat in category_folders:
        # input path
        input_category_path = os.path.join(input_folder_dir, cat)
        input_files = os.listdir(input_category_path)
        # output path
        output_category_path = os.path.join(output_folder_dir, cat)
        os.makedirs(output_category_path, exist_ok = True)

        for input in input_files:
            input_file_path = os.path.join(input_category_path, input)
            # Get file name
            root, ext = os.path.splitext(input)
            output_file_path = os.path.join(output_category_path, f"{root}.png")
            crop_image(input_file_path, output_file_path)



