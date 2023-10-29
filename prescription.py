from dotenv import load_dotenv
import openai
import os
from PIL import Image
import pytesseract
import sys

if __name__ == '__main__':
    '''
    Usage: ./prescription.py <prescription_image>

    This program uses OCR to read the text on a prescription label.
    Afterwards, it uses ChatGPT to extract the medication name, dosage, and form,
    and states what the medication is commonly used for and its effects.
    '''
    load_dotenv()
    openai.api_key = os.getenv('APIKEY')

    # ./prescription <img file>
    if (len(sys.argv) != 2):
        exit(1)

    content = '''
            Please extract ONLY the medication name, dosage, and form from the following text.
            Your response should consist ONLY of the extracted medication name, dosage, and form, and nothing else.
            If there is no medicatin name present, please state 'NO MEDICATION DETECTED':


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

            Please be concise, but descriptive with your explanation.
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