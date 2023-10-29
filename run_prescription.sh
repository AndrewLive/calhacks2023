#!/bin/bash

./capture_image.sh

latest_image=$(ls -t images/captured_image*.jpg | head -n 1)

output=$(./prescription.py "$latest_image")

cat <<EOF > prescription_output.html
<!DOCTYPE html>
<html>
<head>
    <title>Prescription Output</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        h1 {
            background-color: #007BFF;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <h1>Prescription Output</h1>
    <div class="container">
        <p>
            $output
        </p>

        <audio controls>
            <source src="prescription_info.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>

        <img src="$latest_image" alt="Prescription Image">
        
    </div>
</body>
</html>
EOF

# Open the generated HTML file in the default web browser on macOS
open prescription_output.html
