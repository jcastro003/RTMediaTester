from flask import Flask, escape, request, render_template
import socket
import fcntl
import struct
import os
import commands

#Sets the app as a Flask App
app = Flask(__name__)

#Initial Page that uses the wificonnect.html template
@app.route('/')
def my_form():
    return render_template('wificonnect.html')

#Creates the form to register a new network
@app.route('/', methods=['POST'])
def my_form_post():
    #Gets the network ssid
    ssid = request.form['ssid']
    #Gets the network password
    password = request.form['password']
    #Created to save the new file lines
    newFile = []

    #Opens the wifi configurator file to read
    os.system("sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf")
    file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")

    #Reads all lines from this file
    for line in file:
        #Search for the first configuration line and copy this to new file
        if line.find("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev") != -1:
            newFile.append(line)

        #Search for the secomnd configuration line and copy this to new file with the new network data
        elif line.find("update_config=1") != -1:
            #Second configuration line
            newFile.append(line)
            #New network data
            newFile.append("network={\n")
            newFile.append('\tssid="'+ssid+'"\n')
            newFile.append('\tpsk="'+password+'"\n')
            newFile.append("}\n")
        #Just copies others lines to new file
        else:
            newFile.append(line)
    #Closes the file
    file.close()

    #Opens the wifi configurator file to write
    file = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
    #Replaces all lines
    file.writelines(newFile)
    #Closes the file
    file.close()

    #Reboots the system
    os.system("sudo reboot")
    return "Network added! BikeSensor is rebooting..."

#Gets the raspberrypi IP on the network. Not local
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#Runs the server
if __name__ == '__main__':
        app.run(debug=True, host=get_ip_address('wlan0'), port=8080)
