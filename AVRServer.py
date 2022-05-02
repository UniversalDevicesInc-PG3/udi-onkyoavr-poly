#!/usr/bin/env python3

"""
This is a Polglot NodeServer for a Onkyo/Pioneer AVR written by TangoWhiskey1
"""
import udi_interface
import sys
import time
import logging
import ipaddress
from typing import Any

from Node_Shared import *
from AVRNode import *
from WriteProfile import write_nls, write_editors

Custom = udi_interface.Custom

_MIN_IP_ADDR_LEN = 8
#
#
#  Controller Class
#
#
class AVRServer(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name):
        """
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.

         Class Variables:
        self.nodes: Dictionary of nodes. Includes the Controller node. Keys are the node addresses
        self.name: String name of the node
        self.address: String Address of Node, must be less than 14 characters (ISY limitation)
        self.polyConfig: Full JSON config dictionary received from Polyglot for the controller Node
        self.added: Boolean Confirmed added to ISY as primary node
        self.config: Dictionary, this node's Config
        """
        super(AVRServer, self).__init__(polyglot, primary, address, name)
        # ISY required
        self.name = 'AVRServer'
        self.hb = 0 #heartbeat
        self.poly = polyglot
        self.queryON = True

        LOGGER.debug('Entered init')

        # implementation specific
        self.device_nodes = dict()  #dictionary of ISY address to device Name and device IP address.
        self.configComplete = False

        self.Parameters = Custom(polyglot, 'customparams')

        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.CUSTOMPARAMS, self.parameterHandler)
        polyglot.subscribe(polyglot.DISCOVER, self.on_discover)

        polyglot.ready()
        polyglot.addNode(self, conn_status="ST")  #add this controller node first

    def start(self):
        """
        This  runs once the NodeServer connects to Polyglot and gets it's config.
        No need to Super this method, the parent version does nothing.
        """        
        LOGGER.info('AVR NodeServer: Started Onkyo/Pioneer AVR Polyglot Node Server')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()

        # Show values on startup if desired.
        LOGGER.debug('ST=%s',self.getDriver('ST'))
        self.heartbeat(0)
        
        #  Auto Find devices if nothing in config
        if len(self.Parameters) == 0:
            self.auto_find_devices()
        
        while not self.configComplete:
            self.poly.Notices['cfg'] = "Waiting for a valid configuration"
            LOGGER.info('Waiting for a valid user config')
            time.sleep(5)
            self.poly.Notices.delete('cfg')


    def auto_find_devices(self) -> bool:
        """
        Finds the AVRs on the network
        """
        self.poly.Notices['disc'] = "AVR discovery: Looking for devices on network, this will take few seconds"
        new_device_found = False

        LOGGER.debug( "Looking for Onkyo/Pioneer Devices")
        devices =  Receiver.discover(timeout=5)
        LOGGER.debug(  "Controller: Found " + str( len( devices) ) + " devices:" )
        for avr in devices:
            ipAddr =avr.host
            cleaned_dev_name = self.generate_name(avr.info['model_name'],avr.info['identifier'] )
            if( cleaned_dev_name == None):
                LOGGER.error('Controller: Unable to generate key name for: ' +  avr.info['model_name'] + ' ID ' + avr.info['identifier'] )
                continue

            # See if device exists in custom parameters, if not add it
            if cleaned_dev_name not in self.Parameters:
                LOGGER.info('Adding Discovered device to config: ' + cleaned_dev_name + ' ('+ ipAddr + ')')
                self.Parameters[cleaned_dev_name] = ipAddr
                new_device_found = True

        self.poly.Notices.delete('disc')
        return new_device_found

    def generate_name(self, model_name, identifier, )->str:
        """
        Create a name for the AVR if one is found
        """
        try:
            network_device_name = model_name
            network_device_name.replace(' ','_')
            network_device_name = network_device_name+'_'+identifier[-6:]
            return network_device_name
        except Exception as ex:
            return None


    def parseConfigIP(self, addressToParse: str):
        """Make sure IP format with port"""
        try:
            port_index = addressToParse.index(':')
            if port_index < _MIN_IP_ADDR_LEN:
                return None
            port = addressToParse[port_index+1 : ]
            if not port.isnumeric():
                return None
            ip = ipaddress.IPv4Address(addressToParse[0 :port_index])
        except ValueError:
            return None
        return {'ip' : str(ip), 'port' : port }


    def parameterHandler(self, params):
        """
        Set up the polyglot config
        """
        self.Parameters.load(params)
        self.poly.Notices.clear()
        LOGGER.debug('parameterHandler called')
        LOGGER.debug(params)
        try:
            if params == None:
                LOGGER.error('Controller: customParams not found in Config')
                return

            for devName in params:
                device_name = devName.strip()
                device_addr = params[devName].strip()
                isy_addr = 's'+device_addr.replace(".","")
                if( len(isy_addr) < _MIN_IP_ADDR_LEN ):
                    LOGGER.error('Controller: Custom Params device IP format incorrect. IP Address too short:' + isy_addr)
                    continue
                self.device_nodes[isy_addr] = [device_name, device_addr]
                LOGGER.debug('AVR NodeServer: Added device_node: ' + device_name + ' as isy address ' + isy_addr + ' (' + device_addr + ')')
            
            if len(self.device_nodes) == 0:
                LOGGER.error('AVR NodeServer: No devices found in config, nothing to do!')
                return

            self.configComplete = True
            self.add_devices()
        except Exception as ex:
            LOGGER.error('AVR NodeServer: Error parsing config in the Projector NodeServer: %s', str(ex))

    def add_devices(self):
        """
        Add any devices found
        """
        LOGGER.debug('AVR NodeServer: add_devices called')
        for isy_addr in self.device_nodes.keys():
            if not isy_addr in self.nodes:
                device_name = self.device_nodes[isy_addr][0]
                device_addr = self.device_nodes[isy_addr][1]
                try:                
                    avr = Receiver(device_addr)
                    nri = avr.nri # get NRI info
                    write_nls(LOGGER,avr)
                    write_editors(LOGGER,avr)
                    avr.disconnect()
                    if not self.poly.getNode(isy_addr):
                        self.poly.addNode( AVRNode(self.poly, self.address, isy_addr, device_addr, device_name) )
                except Exception as ex:
                    LOGGER.error('AVR NodeServer: Could not add device ' + device_name + ' at address ' + device_addr )
                    LOGGER.error('   +--- Could not get entries for profile.  Error: ' + str(ex))
           
    
    def poll(self, pollflag):
        if pollflag == 'longPoll':
            LOGGER.debug('AVR NodeServer: longPoll')
            self.heartbeat()
        
    def heartbeat(self,init=False):
        LOGGER.debug('AVR NodeServer: heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def delete(self):
        """
        This is sent by Polyglot upon deletion of the NodeServer. If the process is
        co-resident and controlled by Polyglot, it will be terminiated within 5 seconds
        of receiving this message.
        """
        LOGGER.info('AVR NodeServer: Deleting the Projector Nodeserver')

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    def on_discover(self):
        """
        UI call to look fo rnew devices
        """
        dev_found = self.auto_find_devices()

        #if dev_found == True:
        #    self.process_config(self.polyConfig)

    id = 'AVRServer'
    drivers = [{'driver': 'ST', 'value': 0, 'uom': ISY_UOM_25_INDEX},  # Status
    ]

if __name__ == "__main__":
    try:
        poly = udi_interface.Interface([])
        poly.start('1.0.0')
        AVRServer(poly, 'controller', 'controller', 'AVRServer')
        poly.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
