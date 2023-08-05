# PanaceaMobile "API" client Python implementation

For now this implementation is limited to `send_message` action.

It's designed to work with HomeAssistant.

## Usage

```
from PanaceaMobile import PanaceaMobile

pm = PanaceaMobile(panacea_login='<your_username>', panacea_password='<your_password_or_api_key>')

pm.send(recipient='+31612345678', message='Testing')
``` 