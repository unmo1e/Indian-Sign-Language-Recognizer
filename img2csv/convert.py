import os
import subprocess

characters = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

for c in characters:
    current_character = c
    output_string = ""
    for root, dirs, files in os.walk("input\\" + current_character):
        for f in files:
            f_path = os.path.join(root, f)
            opt = subprocess.check_output("powershell -command ./main.exe " + f_path + " " + "output.csv")
            output_string += opt.decode('utf-8') + f_path[6] + "\n"
            
    with open("output" + current_character + ".csv", "w") as f:
        f.write(output_string)

    print("Done output for " + current_character)
