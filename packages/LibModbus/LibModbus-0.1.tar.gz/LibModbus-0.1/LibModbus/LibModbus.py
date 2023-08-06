#!/usr/bin/env python3

import socket
import uuid
import paho.mqtt.client as mqtt
import asyncio
import json
import struct

client_id = str(uuid.uuid4())

mqtt_topic = " "
mqtt_publish_in = str(uuid.uuid4())

class AsyncioHelper:
    def __init__(self, loop, client):
        self.loop = loop
        self.client = client
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.on_socket_register_write = self.on_socket_register_write
        self.client.on_socket_unregister_write = self.on_socket_unregister_write

    def on_socket_open(self, client, userdata, sock):
        pass

        def cb():
            client.loop_read()

        self.loop.add_reader(sock, cb)
        self.misc = self.loop.create_task(self.misc_loop())

    def on_socket_close(self, client, userdata, sock):
        self.loop.remove_reader(sock)
        self.misc.cancel()

    def on_socket_register_write(self, client, userdata, sock):

        def cb():
            client.loop_write()

        self.loop.add_writer(sock, cb)

    def on_socket_unregister_write(self, client, userdata, sock):
        self.loop.remove_writer(sock)

    async def misc_loop(self):
        while self.client.loop_misc() == mqtt.MQTT_ERR_SUCCESS:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break

class AsyncMqtt:
  
    def __init__(self, loop):
        self.loop = loop
        
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(mqtt_publish_in,0)

    def on_message(self, client, userdata, msg):
        if not self.got_message:
            pass
        else:
            self.got_message.set_result(msg.payload)

    def on_disconnect(self, client, userdata, rc):
        self.disconnected.set_result(rc)

    def config(self, server_url, server_port, username, password, tls=None):
        self.server_url = server_url
        self.server_port = server_port
        self.username = username
        self.password = password
        self.tls = tls

    async def _device_reset(self, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_reset":1}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _device_baudrate(self, baudrate, timeout=10):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.baudrate =  baudrate
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in +'","mb_baudrate":' + str(self.baudrate) +'}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)
            
    async def _write_registers(self, mb_address, address_offset, values, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.values = values
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_write":{"f16":[{"address":' + str(self.address_offset) + ',"value":'+str(self.values)+ '}]}}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
           
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _write_single_register(self, mb_address, address_offset, values, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.values = values
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)
        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_write":{"f06":[{"address":' + str(self.address_offset) + ',"value":'+str(self.values)+ '}]}}'

        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)    

    async def _write_coils(self, mb_address, address_offset, quantity_coil, values, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.values = values
        self.quantity_coil = quantity_coil
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_write":{"f15":[{"address":' + str(self.address_offset) + ',"quantity":'+str(self.quantity_coil)+',"value":'+str(self.values)+ '}]}}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)   

    async def _write_single_coil(self, mb_address, address_offset, values, quantity_coil=1, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.values = values
        self.quantity_coil = quantity_coil
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);        
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_write":{"f05":[{"address":' + str(self.address_offset) + ',"quantity":'+str(self.quantity_coil)+',"value":'+str(self.values)+ '}]}}'

        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
        self.got_message = None
        self.client.disconnect()
        return str(msg)   

    async def _read_input_registers(self, mb_address, address_offset, quantity, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.quantity = quantity
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f04":[{"address":' + str(self.address_offset)+',"quantity":'+str(self.quantity)+ '}]}}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _read_multi_input_registers(self, mb_address, t_address_value, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()

        y = json.dumps(t_address_value)
        if len(json.loads(y)) == 0:
            msg = "error"
            return str(msg)
            
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f04":['
        for x in range(0, len(json.loads(y))):
            request_msg = request_msg + str(json.loads(y)[x])
            if x+1 < len(json.loads(y)):
                request_msg = request_msg + ','
        request_msg = request_msg + ']}}'
        request_msg = request_msg.replace(" ", "")
        request_msg = request_msg.replace("'", "\"")
       
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _read_holding_registers(self, mb_address, address_offset, quantity, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.quantity = quantity
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f03":[{"address":' + str(self.address_offset)+',"quantity":'+str(self.quantity)+ '}]}}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _read_multi_holding_registers(self, mb_address, t_address_value, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()

        y = json.dumps(t_address_value)
        if len(json.loads(y)) == 0:
            msg = "error"
            return str(msg)
            
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f03":['
        for x in range(0, len(json.loads(y))):
            request_msg = request_msg + str(json.loads(y)[x])
            if x+1 < len(json.loads(y)):
                request_msg = request_msg + ','
        request_msg = request_msg + ']}}'
        request_msg = request_msg.replace(" ", "")
        request_msg = request_msg.replace("'", "\"")

        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)
    async def _read_discrete_inputs(self, mb_address, address_offset, quantity, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.quantity = quantity
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f02":[{"address":' + str(self.address_offset)+',"quantity":'+str(self.quantity)+ '}]}}'
        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _read_multi_discrete_inputs(self, mb_address, t_address_value, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()

        y = json.dumps(t_address_value)
        if len(json.loads(y)) == 0:
            msg = "error"
            return str(msg)
            
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f02":['
        for x in range(0, len(json.loads(y))):
            request_msg = request_msg + str(json.loads(y)[x])
            if x+1 < len(json.loads(y)):
                request_msg = request_msg + ','
        request_msg = request_msg + ']}}'
        request_msg = request_msg.replace(" ", "")
        request_msg = request_msg.replace("'", "\"")

        self.client.publish(mqtt_topic, request_msg , qos=0)
        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

    async def _read_coils(self, mb_address, address_offset, quantity, timeout=5):
        self.disconnected = self.loop.create_future()
        self.got_message = None
        self.timeout = timeout
        self.mb_address = mb_address
        self.address_offset = address_offset
        self.quantity = quantity
        
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AsyncioHelper(self.loop, self.client)
        self.client.username_pw_set(self.username, self.password)
        if self.tls != None:
            self.tls_set(self.tls);
        self.client.connect(self.server_url, self.server_port)

        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4048)

        self.got_message = self.loop.create_future()
        request_msg = '{"mqtt_publish_in":"' + mqtt_publish_in + '","mb_address":' + str(self.mb_address) +',"mb_read":{"f01":[{"address":' + str(self.address_offset)+',"quantity":'+str(self.quantity)+ '}]}}'

        self.client.publish(mqtt_topic, request_msg , qos=0)

        try:
            msg = await asyncio.wait_for(self.got_message, timeout=self.timeout)
        except asyncio.TimeoutError:
            msg = "error"
            
        self.got_message = None
        self.client.disconnect()
        return str(msg)

   

class Modbus(AsyncMqtt):

    def __init__(self,server_url,server_port,username,password, tls=None):
        self.loop = asyncio.get_event_loop()
        self.config(server_url,server_port,username,password, tls)
        super().__init__(self.loop)

    def mqtt_topic(self, mqtttopic):
        global mqtt_topic
        mqtt_topic = mqtttopic

    def mqtt_publish_in(self, mqttpublish_in):
        global mqtt_publish_in
        mqtt_publish_in = mqttpublish_in

    def check(self, result, mb_fc):
        if result != "error":
            try:
                result = result[2:]
                result = result[:-1]
                js =  json.loads(result)
                result = js['mb_read'][mb_fc][0]['value']
                return result
            except:
                return "error"
        return result        

    def multi_check(self, result, mb_fc):
        if result != "error":
            try:
                result = result[2:]
                result = result[:-1]
                js =  json.loads(result)
                mylist = []
                for x in range(0, len(js['mb_read'][mb_fc])):
                    for y in range(0, (len(js['mb_read'][mb_fc][x]['value']))):
                        mylist.append(js['mb_read'][mb_fc][x]['value'][y])
                return tuple(mylist)
            except:
                return "error"
        return result 

    def device_reset(self, timeout=5 ):
        result = self.loop.run_until_complete(self._device_reset(timeout))
        return result
    def device_baudrate(self, baudrate, timeout=5 ):
        result = self.loop.run_until_complete(self._device_baudrate(baudrate, timeout))
        return result
    def write_registers(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._write_registers(mb_address, address, value, timeout))
        return self.check(result, "f03")
    def write_coils(self, mb_address, address, quantity, value, timeout=5 ):
        result = self.loop.run_until_complete(self._write_coils(mb_address, address, quantity, value, timeout))
        return self.check(result, "f01")
    def write_single_register(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._write_single_register(mb_address, address, value, timeout))
        return self.check(result, "f03")
    def write_single_coil(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._write_single_coil(mb_address, address, value, timeout))
        return self.check(result, "f01")

    """
    Input Registers
    """  
    def read_input_registers(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._read_input_registers(mb_address, address, value, timeout))
        return self.check(result, "f04")

    def read_multi_input_registers(self, mb_address, t_address_value, timeout=20 ):
        result = self.loop.run_until_complete(self._read_multi_input_registers(mb_address, t_address_value, timeout))
        return self.multi_check(result, "f04")
    """
    Holding registers
    """
    def read_holding_registers(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._read_holding_registers(mb_address, address, value, timeout))
        return self.check(result, "f03")
    
    def read_multi_holding_registers(self, mb_address, t_address_value, timeout=10 ):
        result = self.loop.run_until_complete(self._read_multi_holding_registers(mb_address, t_address_value, timeout))
        return self.multi_check(result, "f03")

    """
    Discrete inputs
    """    
    def read_discrete_inputs(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._read_discrete_inputs(mb_address, address, value, timeout))
        return self.check(result, "f02")

    def read_multi_discrete_inputs(self, mb_address, t_address_value, timeout=10 ):
        result = self.loop.run_until_complete(self._read_multi_discrete_inputs(mb_address, t_address_value, timeout))
        return self.multi_check(result, "f02")

    """
    Read Coils
    """
    def read_coils(self, mb_address, address, value, timeout=5 ):
        result = self.loop.run_until_complete(self._read_coils(mb_address, address, value, timeout))
        return self.check(result, "f01")
    
    def float(self, result, byte_order = '>f'):
        if result != "error" and len(result) == 2:
            try:
                high = "%0.2X" % int(list(result)[0], 16)
                low = "%0.2X" % int(list(result)[1], 16)
                tup = bytearray.fromhex(high)
                tup= tup + bytearray.fromhex(low)
                voltage = struct.unpack(byte_order, tup)
                return "%0.2f" % voltage
            except:
                return "error"
        return result
    def __del__(self):
        self.loop.close()
                                     