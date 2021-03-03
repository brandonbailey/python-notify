#!/usr/bin/env python3

# Filename: test.py

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio account
notify_key = os.environ['NOTIFY_KEY']
notify_secret = os.environ['NOTIFY_SECRET']
notify_service = os.environ['NOTIFY_SERVICE']
client = Client(notify_key, notify_secret)

def create_sms_binding(identity, address, *tags):
    """Creates an SMS binding with the given identity, address, and tags."""

    binding = client.notify.services(notify_service) \
                    .bindings.create(
                        identity=identity,
                        binding_type="sms",
                        address=address,
                        tag=tags
                    )
    return binding

def add_binding_tags(binding_sid, *tags):
    """Fetches a binding and recreates it with additional tags."""
    binding = client.notify.services(notify_service) \
                    .bindings(binding_sid).fetch()
    new_tags = [*binding.tags, *tags]
    new_binding = client.notify.services(notify_service) \
                    .bindings.create(
                        identity=binding.identity,
                        binding_type="sms",
                        address=binding.address,
                        tag=new_tags
                    )

def remove_binding_tags(binding_sid, *tags):
    """Fetches a binding and recreates it, removing tags."""
    binding = client.notify.services(notify_service) \
                    .bindings(binding_sid).fetch()
    # TODO: Remove tags from the list
    new_tags = new_tags
    new_binding = client.notify.services(notify_service) \
                    .bindings.create(
                        identity=binding.identity,
                        binding_type="sms",
                        address=binding.address,
                        tag=new_tags
                    )

def send_notification(tag, body):
    """Sends the provided notification body to all addresses with the provided tag."""
    
    notification = client.notify.services(notify_service) \
                         .notifications \
                         .create(tag=tag, body=body)
    return notification

if __name__ == '__main__':
    notification = send_notification('admin', 'This is a notification test')
    print(notification.sid)