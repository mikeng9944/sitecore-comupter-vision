import streamlit as st
import base64
import requests 
import json 

api_base = 'https://gpt-4-with-vision.openai.azure.com/'
deployment_name = 'gpt-4-with-vision'
API_KEY = '8394bf7dbbfb4619b30ff97f095a7486'

base_url = f"{api_base}openai/deployments/{deployment_name}" 
headers = {   
    "Content-Type": "application/json",   
    "api-key": API_KEY 
} 

def generate_vision_result(encoded_image):

    # Prepare endpoint, headers, and request body 
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview" 
    data = { 
        "messages": [ 
            { "role": "system", "content": "You are a helpful assistant." }, 
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture:" 
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": encoded_image
                    }
                }
            ] } 
        ], 
        "max_tokens": 2000 
    }   

    # Make the API call   
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))   

    return response

if __name__ == "__main__":

    st.title("Computer Vision")
    st.write("Provide an image for computer vision:")

    # Upload image
    image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    # Convert image to base64
    if image is not None:
        st.write("Analyzing image...")
        encoded_image = base64.b64encode(image.read()).decode('utf-8')
        result = generate_vision_result("data:image/png;base64," + encoded_image)
    
        if result:
            data = result.json()
            content_value = data['choices'][0]['message']['content']
            st.write(content_value)