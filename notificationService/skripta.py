#!/usr/bin/env python
# -*- coding utf-8 -*-

import time
from os import environ as env
import novaclient.client
from credentials import get_nova_creds
import os
import smtplib
import random
from clockwork import clockwork
from validate_email import validate_email

os.system('cls' if os.name == 'nt' else 'clear')

print "Wellcome to instace creator wizard, would you like to proceed (Y/N)?"
proceed = raw_input()
if proceed !="Y" and proceed != "y":
        exit()
nova = novaclient.client.Client("2", **get_nova_creds())

images = nova.images.list()
flavors = nova.flavors.list()
keys = nova.keypairs.list()
networks = nova.networks.list()

print "Please enter your instace name:"
name = raw_input()

noError = True
while (noError):
    print "Please enter your instance flavor, valid falvors are:"
    for each in flavors:
        print (each.name+","),
    print
    flavor = raw_input()
    for each in flavors:
        if flavor == each.name:
            noError = False
    if noError == True:
        print "ERROR, INVALID FLAVOR!!!"

noError = True
while (noError):
    print "Please enter your instance image, valid images are:"
    for each in images:
        print (each.name+","),
    print    
    image = raw_input()
    for each in images:
        if image == each.name:
            noError = False
    if noError == True:
        print "ERROR, INVALID IMAGE!!!"

noError = True
while (noError):
    print "Please enter your instance key, valid keys are:"
    for each in keys:
        print (each.name+","),
    print    
    key = raw_input()
    for each in keys:
        if key == each.name:
            noError = False
    if noError == True:
        print "ERROR, INVALID KEY!!!"

noError = True
while (noError):
    print "Please enter your instance network, valid networks are:"
    for each in networks:
        print (each.label+","),
    print
    network = raw_input()
    for each in networks:
        if network == each.label:
            noError = False
    if noError == True:
        print "ERROR, INVALID NETWORK!!!"
#Email
flag = 0
while (flag==0):
    print "Enter e-mail address for verification"
    email = raw_input()
    ispravan= validate_email(email)
    if (ispravan):
        flag=1
    else:
        print "Invalid e-mail form"

sender = 'riteh.openstack@gmail.com'
receivers = []

receivers.append(email)

a = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
length = 8
code = ""

for i in range(length):
    next_index = random.randrange(len(a))
    code = code + a[next_index]


message =("From: RiTeh SEIP lab <riteh.openstack@gmail.com>\n"
        "To: <" + email+">\n"
	"Subject: Activation mail\n\n"
	
	"You have requested instance creation, instance that will be created have next attributes:\n\n"
	"--------------------------------------------------------------------------------------------\n"
	"Instance name: " + name +"\n"
	"Instance image: " + image + "\n"
	"Instance key: "  + key + "\n"
	"Instace network: " + network + "\n"
	"--------------------------------------------------------------------------------------------\n\n"
        "Activation code: "+code+"\n"
)



try:
   smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587) 
   smtpObj.ehlo()
   smtpObj.starttls()
   smtpObj.login("riteh.openstack@gmail.com", "domagojfranko")
   smtpObj.sendmail(sender, receivers, message) 
        
   print "E-mail is successfully send!"
   
except smtplib.SMTPException,error:
   print "Error while sending e-mail"
   print str(error)
    
flag=0

while(flag<3):
    print "Enter activation key"
    mail_code=raw_input()
    if (mail_code==code):
        flag=4
    else:
        print "Wrong activation key"
        if (flag==2):
            print "You have entered wrong key three times, exiting!!!"
            exit()
        else:
            flag=flag+1
        
print "PLEASE WAIT, YOUR INSTANCE IS BEEING CREATED!"

try:
    image = nova.images.find(name=image)
    flavor = nova.flavors.find(name=flavor)
    net = nova.networks.find(label=network)
    nics = [{'net-id': net.id}]
    
     # stvaranje instance
    instance = nova.servers.create(name=name, image=image,
                                   flavor=flavor, key_name=key,
                                   nics=nics)

    # cekanje 5 sec. prije ispisa
    
    print("Sleeping for 5s after create command")
    time.sleep(5)

    
finally:
    print("Execution Completed")
    print "Instance created"

"""api = clockwork.API('ee6b0cdc140d5a9c1aef2e46c498e265ffaaa5be')


message = clockwork.SMS(
    to = '385989699158',
    message = 'SEIP LAB INFO: NEW INSTACE HAS BEEN CREATED FROM EMAIL: '+email+' INSTANCE NAME: '+name )

response = api.send(message)

if response.success:
    print ("SMS SEND SUCCESSFULLYY!!!")
else:
    print ("SMS SEND FAILURE!!!")"""


