from dotenv import load_dotenv
import openai
import os
from PIL import Image
import pytesseract
import sys
from gtts import gTTS

if __name__ == '__main__':
    '''
    Usage: ./prescription.py <prescription_image>

    This program uses OCR to read the text on a prescription label.
    Afterwards, it uses ChatGPT to extract the medication name, dosage, and form,
    and states what the medication is commonly used for and its effects.
    '''
    load_dotenv()
    openai.api_key = os.getenv('APIKEY')

    # Capture an image from the RTSP stream and save it to the 'images' folder
    os.system('ffmpeg -i rtsp://192.168.42.1:8554/stream0 -vframes 1 images/captured_image.jpg')

    # Path to the captured image
    captured_image_path = 'images/captured_image.jpg'

    # ./prescription <img file>
    if (len(sys.argv) != 2):
        exit(1)

    content = '''
            Please extract ONLY the medication name, dosage, form, and instructions from the following text.
            Your response should consist ONLY of the extracted medication name, dosage, and form, and nothing else.
            If there is no medication name present, please state 'NO MEDICATION DETECTED':


            '''
    
    content += pytesseract.image_to_string(Image.open(sys.argv[1]))

    
    messages = [ {"role": "system", "content": content} ]

    chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
            ) 
    
    medication_name = chat.choices[0].message.content
    print(f'ChatGPT: {medication_name}')

    content = f'''
            Please describe the following medication:
            {medication_name}

            Please be short and concise with your explanation.
            Please describe common uses and side effects of the medication as well.
            Also, DO NOT, under any circumstance, restate the medication name, dosage, or form.
            '''
    
    messages.append({"role": "system", "content": content})
    chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
            ) 
    medication_info = chat.choices[0].message.content
    print(f'ChatGPT: {medication_info}')
    
    outfile = open('./prescription_info.txt', 'w')
    outfile.write(f'{medication_name}\n\n{medication_info}')
    outfile.close()

    tts = gTTS(text = f'{medication_name}\n\n{medication_info}', lang = 'en', slow = False)
    tts_path = f'./prescription_info.mp3'
    tts.save(tts_path)