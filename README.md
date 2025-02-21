For windows machines only
Use python 3.13.2 64-bit for windows
pip install openAI 

What it does currently:
Will automatically detect logs that are considered "slow" from MySQL server, and output the query that caused this to basic chatGPT wrapper in index.html

Set Up
- Download MySQL Server Workbench (Install SQL Server aswell)
- Once Workbench is open, create a new connection, and once created start the server from the workbench
- Once running, use the database-test-schema.txt file to copy and paste the SQL query to create the database.









- Once extracted, navigate to 'C:\ProgramData\MySQL\MySQL Server 8.0\Data\DESKTOP-BDLUB0E-slow.txt (values might slightly change), right click on it
  Open the Properties dialog:
  Right-click the file (mysql.slow_log.csv) and choose “Properties,” then go to the “Security” tab.

  Edit Permissions:
  Click the “Edit…” button to change permissions. If you’re not already listed, you’ll need to add your user account.

  Add Your User Account (if needed):
  • Click “Add…” and then type your username (or click “Advanced…” and then “Find Now” to select your account).
  • Click “OK” to add the account.

  Grant Read Permissions:
  Once your account is listed, select it and then check the “Read” box under “Allow.”
  If you want to allow more (such as List Folder Contents), adjust accordingly.

  Apply the Changes:
  Click “Apply” and “OK” to save the changes.
  You might need to confirm a User Account Control (UAC) prompt if you’re not running as an administrator.

- 
