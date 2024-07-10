import json
import os
import argparse
from PIL import Image, ImageDraw

# Function to convert a matrix to an image with a grid
def matrix_to_image(matrix, hex_colors, output_path, cell_size=20, border_color='#555555', border_width=1):
    height = len(matrix)
    width = len(matrix[0])
    
    # Calculate the size of the image
    img_width = width * (cell_size + border_width) + border_width + 1
    img_height = height * (cell_size + border_width) + border_width + 1
    
    # Create a new image with RGB mode and a white background
    image = Image.new('RGB', (img_width, img_height), color='#555555')
    draw = ImageDraw.Draw(image)
    
    # Draw the grid cells
    for y in range(height):
        for x in range(width):
            value = matrix[y][x]
            color = hex_colors.get(value, '#000000')  # Default to black if the color is not specified
            top_left_x = x * (cell_size + border_width) + border_width
            top_left_y = y * (cell_size + border_width) + border_width
            bottom_right_x = top_left_x + cell_size
            bottom_right_y = top_left_y + cell_size
            
            # Draw the cell
            draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], fill=color)
            
            # Draw the border
            draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], outline=border_color, width=border_width)
    
    # Save the image
    image.save(output_path)

# Main function to process JSON file and generate images
def json_to_images(json_file, output_dir, hex_colors):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each training example
    for i, example in enumerate(data.get('train', [])):
        input_matrix = example['input']
        output_matrix = example['output']
        
        input_image_path = os.path.join(output_dir, f'train_{i}_input.png')
        output_image_path = os.path.join(output_dir, f'train_{i}_output.png')
        
        matrix_to_image(input_matrix, hex_colors, input_image_path)
        matrix_to_image(output_matrix, hex_colors, output_image_path)
    
    # Process each test example
    for i, example in enumerate(data.get('test', [])):
        input_matrix = example['input']
        output_matrix = example['output']
        
        input_image_path = os.path.join(output_dir, f'test_{i}_input.png')
        output_image_path = os.path.join(output_dir, f'test_{i}_output.png')
        
        matrix_to_image(input_matrix, hex_colors, input_image_path)
        matrix_to_image(output_matrix, hex_colors, output_image_path)

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a JSON file to generate images.')
    parser.add_argument('json_file', help='The input JSON file')
    args = parser.parse_args()
    
    output_dir = os.path.splitext(os.path.basename(args.json_file))[0]
    hex_colors = {
        0: "#000000", # Black
        1: "#3172D2", # Blue  
        2: "#EB5242", # Red
        3: "#65C955", # Green
        4: "#F9DD4A", # Yellow
        5: "#AAAAAA", # Gray
        6: "#DC34B9", # Purple
        7: "#EF8B3B", # Orange
        8: "#95D9FB", # Light Blue
        9: "#7C1C28", # Dark Red
    }
    
    json_to_images(args.json_file, output_dir, hex_colors)