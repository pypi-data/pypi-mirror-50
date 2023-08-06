from __future__ import print_function
from CherwellAPI import CherwellClient
import pickle

#########################################################################################
# This example demonstrates how the CherwellAPI Connection object can be used to
# create a new business object
###########################################################################################

#############################################
# Change the following to suit your instance
#############################################

base_uri = "http://<Your Cherwell Host here>"
username = "<Your UserName Here>"
password = "<Your Password here>"
api_key = "<Your Cherwell REST API Client Key here>"

# Create a new CherwellClient connection
cherwell_client = CherwellClient.Connection(base_uri, api_key, username, password)

# Get a new business object
ci_computer = cherwell_client.get_new_business_object("ConfigNetworkDevice")

# Set some attributes
ci_computer.FriendlyName = "DavidsTestComputer"

# Save the new CI
ci_computer.Save()




