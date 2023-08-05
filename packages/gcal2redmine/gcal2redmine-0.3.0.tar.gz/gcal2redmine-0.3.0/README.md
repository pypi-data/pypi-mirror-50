# GCal2Redmine

Track your time in Redmine from Google Calendar.

# Configuration

1. The first step is to turn on your Google Calendar API.
   * Use the following link to create or select a project from the google developer console and turn on the api: <https://console.developers.google.com/start/api?id=calendar>
   * Click continue and Go to credentials.
   * On the Add credentials to your project page, click the Cancel button.
   * At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
   * Select the Credentials tab, click the Create credentials button and select OAuth client ID.
   * Select the application type "Other", enter the desired name, and click the Create button.
   * Click OK to dismiss the resulting dialog.
   * Click the Download JSON button to the right of the client ID.
   * Move this file to your config directory (default: `~/.config/g2c/`) and rename it google.secret.json.
2. Redmine API

## TODO

- proper handling of time entry activity
