import os
import gradio as gr
import pandas as pd

# Function to count frames in a folder
def count_frames_in_folder(folder_path):
    # Count number of images in the folder
    return len([f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))])

# Function to check the status of each pass
def check_pass_status(root_folder, project_name, ep_name, shot_name, passes):
    # Original path
    original_path = os.path.join(root_folder, project_name, ep_name, shot_name, 'original')
    
    # Count frames in original
    original_frames = count_frames_in_folder(original_path)
    
    # List to hold the data for each pass
    pass_data = []
    
    # Check status for each pass
    for pass_name in passes:
        pass_path = os.path.join(root_folder, project_name, ep_name, shot_name, pass_name)
        
        # Check if pass folder exists
        if not os.path.exists(pass_path):
            status = 'To do'
            frames = 0
        else:
            frames = count_frames_in_folder(pass_path)
            if frames < original_frames:
                status = 'Missing frames'
            elif frames == original_frames:
                status = 'Done'
            else:
                status = 'Extra frames'
        
        # Append data
        pass_data.append([pass_name, frames, status])
    
    # Return as DataFrame
    return pd.DataFrame(pass_data, columns=['Pass Name', 'Frames', 'Status'])

# Gradio Interface function
def check_project_status(root_folder, project_name, ep_name, shot_name):
    passes = ['depth', 'openpose', 'animelineart', 'firstpass', 'animatediff', 'comp']
    
    # Check status
    df = check_pass_status(root_folder, project_name, ep_name, shot_name, passes)
    
    return df

# Gradio interface
interface = gr.Interface(
    fn=check_project_status,
    inputs=[
        gr.Textbox(label="Root Folder", placeholder="Path to root folder"),
        gr.Textbox(label="Project Name", placeholder="Project name"),
        gr.Textbox(label="Episode Name", placeholder="Episode name (e.g., V1)"),
        gr.Textbox(label="Shot Name", placeholder="Shot name (e.g., V1-001)")
    ],
    outputs=gr.DataFrame(),
    title="Shot Pass Status Checker",
    description="This app checks the status of shot passes and compares them to the original pass frame count."
)

# Launch the interface
interface.launch()
