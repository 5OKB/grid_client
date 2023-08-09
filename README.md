# GridAuthClient

```
logger = logging.getLogger()
```

```
keycloak_openid = KeycloakOpenID(server_url="https://login.gridgs.com", client_id="grid-api", realm_name="grid")
grid_auth_client = GridAuthClient(open_id_client=keycloak_openid, username="user@gridgs.com", password="userpass", company_id=1, logger=logger)
```

# GridApiClient

```
grid_api_client = GridApiClient(base_url="https://api.gridgs.com" auth_client=grid_auth_client, logger=logger)
```

### Get predicted sessions
```
sessions = grid_api_client.get_predicted_sessions() 
```

### Create a session

```
session = Session() # A session from get_predicted_sessions
session = grid_api_client.create_session(session)
```

# GridEventSubscriber

Receive statuses of sessions

```
grid_event_subscriber = GridEventSubscriber(host="api.gridgs.com", port=1883, auth_client=grid_auth_client, logger=logger)

grid_event_subscriber.on_event(on_event)
grid_event_subscriber.run()

def on_event(self, event: SessionEvent):
    session = event.session
```

# GridMQTTClient

```
grid_mqtt_client = GridMQTTClient(host="api.gridgs.com", port=1883, auth_client=grid_auth_client, logger=logger)

grid_mqtt_client.subscribe(session, on_downlink_frame)
grid_mqtt_client.connect()

def on_downlink_frame(frame: Frame):
```

### Sending a frame

```
grid_mqtt_client.send(session, b'Uplink frame data')
```