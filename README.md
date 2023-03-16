# create-wpt-agent
A script to bulk deploy WPT Agents within Linode for use with a private WPT Server

You will need to obtain a Linode API Token to execute this script. https://cloud.linode.com/profile/tokens

Within linode_settings.txt be sure to fill in:

api_token: [Your Linode API token]
username: [The unsername for the sudo user to create on the agent. WPT will be installed under this user]
password: [The password for the sudo user]
root_pass: [The password for the root user]
wpt_server: [The name of your WPT Server. Note the agent will by default connect via HTTPS]

Within agent_list.txt use one line per agent to install. The format is linode_region,location_name,location_key

For example

us-central,Dallas,mysecretkey1
us-iad,Washington,mysecretkey2
us-east,Newark,mysecretkey3

Note the linode_region must be a valid location, the Location Name must have a corresponding entry on the WPT server locations.ini, and the Location Key must match the location listed in locations.ini. Default directory on the server is /var/www/webpagetest/www/settings/locations.ini

