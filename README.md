# BoardDoc Policy Downloader
Designed to gather all the policy pages and attachments for a board doc site.  It downloads all of 
the text for a policy and saves it as a file in the current directory with the title of the page as
the file name.  The attachments associated with a policy are downloaded and saved as whatever the
name the attachment was given on the BoardDocs site itself.

Currently the code is directed at the Kent School District BoardDocs site, but can be changed to fit other BoardDoc sites by editing the url line:

```url = 'http://www.boarddocs.com/wa/ksdwa/Board.nsf/Public'```

To have the url for the BoardDoc site you wish to download from.

This script is for educational purposes only.  Any usage outside of educational is at your own risk.

## Script Requirements
This script uses
- Selenium
- PathValidate
- UrlLib

All of which can be installed from the command line with 

`` pip install selenium``
