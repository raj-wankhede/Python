from ncclient import manager
import xml.dom.minidom as DOM
import xmltodict

router = {"host": "192.168.171.91", "port": "830",
         "username": "admin", "passwd": "admin"}

netconf_filter= """ 
<filter>
    <interfaces xmlns= "urn:ietf:params:xml:ns:yang:ietf-interfaces">
    </interfaces>
</filter>
"""
## Connect to device and run above XML filter - send rpc message to device
with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["passwd"], hostkey_verify=False) as mgr:
    
    int_netconf = mgr.get(netconf_filter)
    #xmlDom=DOM.parseString(str(int_netconf))
    #print(xmlDom.toprettyxml(indent=" "))
    #print('*' * 25 + 'Break' + '*' * 25 )

## important to mention .xml 
## Convert to dictionary and save it in variable
int_python = xmltodict.parse(int_netconf.xml) ["rpc-reply"] ["data"]
#print(int_python)
print('*' * 50 )

##print(len(int_python['interfaces']['interface']))

## Fetch specific attribute like name, description, IP address, vlans from the int_python created above:
for inter in range (0,len(int_python['interfaces']['interface'])):

    int_name = int_python['interfaces']['interface'][inter]['name']
    print(f"Interface name: {int_name}")
    #print('*' * 50 )

    try:
        int_descr= int_python ['interfaces']['interface'][inter]['description']
        print(f"Interface Description: {int_descr}")
    except:
        print(f"Interface Description: ")

    if 'lo' in int_name:
        try:
            int_ipadd = int_python['interfaces']['interface'][inter]['ipv4']['address']['ip']
            print(f"Interface IPv4 addr: {int_ipadd}")        
        except:
            print("Interface IPv4 addr: IP not assigned on loopback interface!")        

    elif '.' in int_name and 'lo' not in int_name:
        try:
            int_Vlan = int_python['interfaces']['interface'][inter]['pif-lif']['vlans']
            print(f"Interface VLAN: {int_Vlan}")
        except:
            print(f"Interface VLAN: No Vlan")

        try:
            int_ipadd = int_python['interfaces']['interface'][inter]['ipv4']['address']['ip']
            print(f"Interface IPv4 addr: {int_ipadd}")        
        except:
            print("Interface IPv4 addr: IP not assigned on LIF")       
    
    else:
        int_PortType = int_python['interfaces']['interface'][inter]['pif-interface']['pif-port-type']
        print(f"Interface Type: {int_PortType}")    
    
    print('*' * 50)


