#!/usr/bin/python3

# This script automate the MikroTik routers/APs' configurations
# Script by Arash // arash66@gmail.com

# Requirements:
# Run this script with Administrator privilege.
# Port 8729 for site in new portal and 8728 for sites with insuecure connection must be open on the gateways
# Files must be in the same location of the script file

import routeros_api
import os   


#################### API function #####################
def Core(filepath, ssl):

    # First open a file and read each line
    # The format of the file: (name ip user pass)   
    String = []        
    with open(filepath) as lines: 
        next(lines)
        for line in lines:
            for word in line.split():
                String.append(word)
            
            # If one of user / pass / IP / name is missing, show an error and the line!
            length = len(String)
            if length < 4: 
                print("=====================================================================================")
                print("\n> Data in this line is incomplete: {}> File name: {}\n".format(line, filepath))
                print("=====================================================================================\n\n")
                break 

            else:   
                name = String[0]
                server = String[1]
                user = String[2]
                passw = String[3]
                
                print("\n=====================================================================================")
                print("\n        > Test the connectivity of", server ," for: ", name , "<")
                print("         ..........................................................\n")
                    
                # Ping the given IP using os.system library
                # Sending 2 echo requests // Remove NUM if you need the Ping result on the screen
                SRV_UP = True if os.system("ping -n 2 " + server + "> NUL") == 0 else False
                
                # First condition triggered if a router is reachable and based on SSL
                if SRV_UP == True and ssl == True:
                    print("\n> Connecting to the router...\n")
                    
                    try:
                        # Estblish a connection to each router but it is based digital certificate installed on each router!       
                        connection = routeros_api.RouterOsApiPool(server, user, passw, plaintext_login=True, use_ssl=True, ssl_verify_hostname=False, ssl_verify=True, port=8729)
                        api = connection.get_api()
                        print(">> Connection has been established\n")
                        try:
                            # Run a MikroTik command
                            list_hotspot = api.get_resource('/ip/hotspot')
                            
                            # Get data from a command based on the ID
                            output = list_hotspot.get(id='*1') [0]["id"] # To see all the parametrs of /ip/hotspot, remove everything in () and the following
                            print(">>> Hotspot ID: ", output) 
                            
                            # Set new data to router(s) using the parameter of "disbaled"
                            # true: hotsput disable // false: enable hotspot
                            # Must uncomment your line
							
							#list_hotspot.set(id=output,addresses_per_mac='2') 
                            #list_hotspot.set(id=output,disabled='false')
                            print("\n>>>> Hotspot has been disabled\n")
                            
                            # Close the connection and clear the array of string
                            connection.disconnect()
                            String.clear()         
                            print("=====================================================================================\n\n")                    
                        
                        # An exception that logs and prints when an error happned in try section
                        except Exception as Argument:
                            print(">>> The given argument is wrong or doesn't exist in your MikroTik: {} | {} \n".format(name, server))              
                            # Print inside error.txt file if any errors for invalid credentials 
                            f = open("logs.txt", "a")
                            f.write("\nThe given argument is wrong or doesn't exist in your MikroTik: {} | {} \n".format(name, server))
                            f.close()
                            String.clear() 
                            print("=====================================================================================\n\n") 
                        
                    # An exception that logs and prints when an error happned in try section
                    except Exception as Argument:
                        print(">> Invalid User/Password or port (8729) isn't open: {} | {} \n".format(name, server))
                        
                        # Print inside error.txt file if any errors for invalid credentials 
                        f = open("logs.txt", "a")
                        f.write("\nInvalid User/Password or port (8729) isn't open: {} | {} \n".format(name, server))
                        f.close()
                        String.clear() 
                        print("=====================================================================================\n\n")		

                # Second condition triggered if a router is reachable but not based on SSL
                if SRV_UP == True and ssl == False:
                    print("\n> Connecting to the router...\n")
                    
                    try:
                        # Estblish a connection to each router from "SERVERS" but based on plaintext!       
                        connection = routeros_api.RouterOsApiPool(server, user, passw, plaintext_login=True, port=8728)
                        api = connection.get_api()
                        print("> Connection has been established")
                        try:
                            # Run a MikroTik command
                            list_hotspot = api.get_resource('/ip/hotspot')
                            # Get data from a command based on the ID
                            output = list_hotspot.get(id='*1') [0]["id"] # To see all the parametrs of /ip/hotspot, remove everything in () and the following
                            print(">>> Hotspot ID: ", output)                                     

							# Set new data to router(s) using the parameter of "disbaled"
                            # true: hotsput disable // false: enable hotspot
                            # Must uncomment your line
							
							#list_hotspot.set(id=output,addresses_per_mac='2') 
                            #list_hotspot.set(id=output,disabled='false')
                            print("\n>>>> Hotspot has been disabled\n")
							
                            connection.disconnect()
                            String.clear()         
                            print("=====================================================================================\n\n")                    
                        
                        # An exception that logs and prints when an error happned in try section
                        except Exception as Argument:
                            print(">>> The given argument is wrong or doesn't exist in your MikroTik: {} | {} \n".format(name, server))              
                            # Print inside error.txt file if any errors for invalid credentials 
                            f = open("logs.txt", "a")
                            f.write("\nThe given argument is wrong or doesn't exist in your MikroTik: {} | {} \n".format(name, server))
                            f.close()
                            String.clear() 
                            print("=====================================================================================\n\n")                         
                        
                    # An exception that logs and prints when an error happned in try section
                    except Exception as Argument:
                        print(">> Invalid User/Password or port (8728) isn't open: {} | {} \n".format(name, server))
                        
                        # Print inside error.txt file if any errors for invalid credentials 
                        f = open("logs.txt", "a")
                        f.write("\nInvalid User/Password or port (8728) isn't open: {} | {} \n".format(name, server))
                        f.close()
                        String.clear() 
                        print("=====================================================================================\n\n")                        
						        
                # If there is no connectin to a gateway, print time out
                if SRV_UP == False: 
                    print("                            -------------------")
                    print("                           |   >> TIME OUT <<  |")
                    print("                            -------------------")
                    print("\n=====================================================================================\n\n")
                    # Print the unreachable cases into a file 
                    f = open("logs.txt", "a")
                    f.write("\nThis site/IP is unreachable: {} | {} \n".format(name, server))
                    f.close()
                    String.clear()  
                    

#################### File-check function #####################
def filechk(filepath, ssl):
    # 1st check whether the file exists or not       
    if os.path.isfile(filepath): 
        # 2nd check whether the file is empty or not
        if os.stat(filepath).st_size == 0:
            print("\n> No data is in: ", filepath)
        else:
            Core(filepath, ssl) # Call main/API function
    else:  
        print("\n> No file with this name!", filepath)
        
        
######################## Main Menu #############################

# This loop read data from keyboard
while True:

    print("\n###################           MikroTik API remote controller        #####################")
    print("###################                                                 #####################")
    print("                   |                  Site lists                    |")
    print("                   |             1) Sites in Melbourne              |")
    print("                   |             2) Sites in Sydney                 |")
    print("                   |             3) Sites in Brisbane               |")
    print("                   |             4) Sites in Adelaide               |")
    print("                   |             5) Exit                            |")
    print("                    ------------------------------------------------")
    
    value = input("\n> Enter a number to apply change for .... :  ")
	
######################## Inputs #############################	
    
    if value == '1':
        filepath = '.\ip-list.txt'
        ssl = True # If connection is based on SSL use port 8729
        filechk(filepath, ssl) # Call File-check function
            
    elif value == '2':
        #filepath = '.\ip-list2.txt'
        ssl = False # If connection is not based SSL use port 8728 
        filechk(filepath, ssl)  

    elif value == '3':
        #filepath = '.\ip-list3.txt'
        ssl = True
        filechk(filepath, ssl)   
         
    elif value == '4':
        #filepath = '.\ip-list4.txt'
        ssl = False
        filechk(filepath, ssl)          
            
    elif value == '6':
        break    

input('\n> Press Enter to exit: ')
