import os
from PIL import Image, ImageSequence

def combine_gifs(gif1_path, gif2_path, gif3_path, orientation):
    # Open the GIFs
    gif1 = Image.open(gif1_path)
    gif2 = Image.open(gif2_path)
    gif3 = Image.open(gif3_path)

    # Get the size of the first GIF (assuming both are the same size)
    width, height = gif1.size

    # Create a list to store combined frames
    frames = []

    # Loop over frames in both GIFs and combine them
    for frame1, frame2, frame3 in zip(ImageSequence.Iterator(gif1), ImageSequence.Iterator(gif2), ImageSequence.Iterator(gif3)):
    
        if orientation == "horizontal":
            # Create a new image for each frame with width = width of GIFs combined
            combined_frame = Image.new("RGBA", (width * 3, height))
            # Paste the frames side by side 
            combined_frame.paste(frame1, (0, 0))
            combined_frame.paste(frame2, (width, 0))
            combined_frame.paste(frame3, (width*2, 0))  

        elif  orientation == "vertical":
            # Create a new image for each frame with height = height of GIFs combined
            combined_frame = Image.new("RGBA", (width, height * 3))
            # Paste the frames side by side 
            combined_frame.paste(frame1, (0, 0))
            combined_frame.paste(frame2, (0, height))
            combined_frame.paste(frame3, (0, height*2))  

        # Append combined frame to frames list
        frames.append(combined_frame)

    return frames
    
if __name__ == "__main__":

    # Setting
    main_dir = r'/home/yiting/Documents/Data/Shapes/gif'
    save_dir = r'/home/yiting/Documents/Data/Shapes/example_gif'
    vh_cat_names = ["axial_component", "torso", "sheet"]
    example_gifs = {
        "axial_component": ["025", "034", "057"],
        "torso": ["010", "018", "096"],
        "sheet": ["018", "024", "040"]
                    }

    for vh_cat in vh_cat_names:
        data_dir = os.path.join(main_dir, vh_cat)
        gif1_path = os.path.join(data_dir, f"{vh_cat}_{example_gifs[vh_cat][0]}.gif")
        gif2_path = os.path.join(data_dir, f"{vh_cat}_{example_gifs[vh_cat][1]}.gif")
        gif3_path = os.path.join(data_dir, f"{vh_cat}_{example_gifs[vh_cat][2]}.gif")
        gif1 = Image.open(gif1_path)
        frames = combine_gifs(gif1_path, gif2_path, gif3_path, "horizontal")

        # Save the combined frames as a new GIF
        save_file_path = os.path.join(save_dir, f'{vh_cat}_combined.gif')
        frames[0].save(save_file_path, save_all=True, append_images=frames[1:], loop=0, duration=gif1.info['duration'])

    # Combine gif for each vhObject category vertically
    gif1_path = os.path.join(save_dir, f"axial_component_combined.gif")
    gif2_path = os.path.join(save_dir, f"torso_combined.gif")
    gif3_path = os.path.join(save_dir, f"sheet_combined.gif")

    frames_all = combine_gifs(gif1_path, gif2_path, gif3_path, "vertical")
    # Save the combined frames as a new GIF
    save_file_path = os.path.join(save_dir, f'example_combined.gif')
    frames_all[0].save(save_file_path, save_all=True, append_images=frames_all[1:], loop=0, duration=gif1.info['duration'])


