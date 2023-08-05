#### !!!!!!!!!! Use "help(Epsexec)" This will show you the available methods. (This usage form will contain it, but it is yet to be completed.) !!!!!!!!!!

### About
epsexec (Enhanced psexec) uses [Microsoft's Sysinternals PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) utility that uses SMB to execute programs on remote systems.
PsExec is a light-weight telnet replacement.    
If you find any bugs, PLEASE report to ***`EpsexecNoReply@gmail.com`***   

### Installation
Run the following to install:   
```
pip install Enhanced-PsExec
```

### Requirements
**Attacker Machine:**
1) You MUST have a 64-bit version of python.   
2) You MUST have [psexec install](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)ed and in your system32 folder.   
   *The `psPc` class has a static method `download_psexec` that can automate the process for you.*   
   *Run: `psPc.download_psexec()`*    
3) You MUST run python as administrator (Ctrl+Esc, type "python", Ctrl+Shift+Enter,Alt-Y).

**The Remote PC:**   
The remote pc (The pc that you are attacking) have very few requirements;
1) SMBv2 needs to be up and running on the Windows port. Run this CMD script on the remote computer:
`powershell.exe Set-SmbServerConfiguration -EnableSMB2Protocol $true`
2) The ADMIN$ share to be enabled with read/write access of the user configured.   
   Unless the machine already has an administrator user with password, I recommend making Another user that is administrator.   
   CMD:   
`net user /add usernameToHack passToBeUsed`   
To enable administrator:   
`net localgroup administrators usernameToHack /add`    

3) You'll need to add A registry key.   
This is because UAC is set up to deny connections like this, so you will get an `ACCESS_IS_DENIED` error when attempting to connect.   
Fix: run CMD as administrator and run:   
`reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f`   

4) RECOMMENDED: Disable firewall on the remote machine.   
This will allow for a faster experience while connecting.   
There is also A method to do this, so you dont need to go to the remote PC NOW.   
you can do it remotely using: `pc.firewallChange(state="rule")`   
Or, run on this on the remote machine in administrator CMD:   
`netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in new enable=Yes`   
Or, you can just disable the firewall entirely administrator CMD:   
`netsh advfirewall set allprofiles state off`

5) Restart the system.   

## Import
To import the package, use `from epsexec import psPc`.   

# Usage
1) Create a psPc class instance.   
```python
pc1 = psPc("IPv4","username","password")   
```
General settings:   

**`delay_before`** --- This pauses the operation {delay_before} millisecond before starting the operation.  (Default 100)   
**`runAsAdmin`**  --- If true, it will run the operation in administrative privileges. (default True)   

## firewallChange
This is probably the most important method. why?   
Well, because firewall makes the psexec process extremely slow (It takes about 12 seconds instead of 1).   
So, it becomes very frustrating.   
Modes:
1. "on" to enable firewall on the remote machine.
2. "off" to disable firewall on the remote machine.
3. "smb" to add a SMB-only rule. This will allow connections from port 445 (smb)
4. "rdp" to add a remote desktop rule to make connections from remote desktop easier.  

## download_nir
[NirCMD](https://www.nirsoft.net/utils/nircmd.html) is A windows command-line utility that allows you to do useful tasks without displaying any user interface.   
Unfortunately, NirCMD is NOT installed by default on windows systems.   
Thats why this method exists. all this method do, is download NirCMD on the remote PC using powershell.   
Nircmd is required for the following methods:   
1. beep   
2. sendScreenshot   
3. setVolume   
4. textToSpeech   

## beep
**Requires Nircmd**   
The beep method takes frequency(hz) and duration(millisecond) parameters.   
Then it plays A sound at the given frequency and duration.   

## getShell
The getShell method is the most basic method.   
It takes A shell to open as and administration privileges. (default "cmd.exe",True)   
This is your everyday remote shell on another PC.   
You can also choose powershell instead of cmd   


## closeProcess
The closeProcess method takes A process name or processID, and delay_before to wait before the program closes the process.   
Then it uses taskkill (CMD command) to close it.   


## closeChrome
This method closes every chrome tab on the remote machine.   
It takes 2 parameters: runAsAdmin, and delay_before. (Default True)       


## textToSpeech
**Requires Nircmd**   
The textToSpeech method takes A string to speak, and MaleVoice as a boolean. (default True)   
Then it uses NirCMD to speak the text on the remote PC.   

## setVolume
**Requires Nircmd**   
The setVolume method takes a number from 0 to 100 as the percentage And delay_before.   
Then it opens NirCMD in the remote pc and uses "setsysvolume" to set the computer's volume.   
If the volume is set to zero, it will mute the remote pc.
If the volume is set to 101, it will un-mute the remote pc (A pc can be muted, but the volume is high.)


## send_screenshot
**Requires Nircmd**   
The sendScreenshot takes email address and delay_before.    
It uses NirCMD to take A screenshot, save it to C:\epsexecScreenshot.png   
Then, it uses powershell SMTPClient.send() to send an email to the given Email Address   

# openURL 
This method is the most complicated method.   
It can potentially take multiple parameters.   
RECOMMENDED: Go to `chrome://extensions` on the remote machine. then go to your AdBlocker's settings.   
Click **"Allow in incognito"**. This will allow your AdBlocker on incognito.   
So YouTube songs will not load ads, making for better experience.   
   
I will now explain every parameter:   
**`URL`** --- This is the URL to be opened in the remote machine. If `fromFile` parameter is used, it must be: `'*://*/*'`, its default   

**`fromFile`** --- This parameter is used to take A text file and get every URL and its shotcut name.   
**[See more](https://github.com/orishamir/Epsexec/blob/master/fromFile.md)**

**`tabs`** --- This parameter is responsible for the amount of tabs to open on the remote machine. (Default=1)   

**`delayBeforeOpening`** --- This parameter decides how much time in millisecond the program should pause before starting the operation. (Default=100)   

**`delayBetweenTabs`** --- This parameter decides how much time in millisecond the program should pause BETWEEN every time it opens A new tab.

**`new_window`** --- This parameter decides whether or not to open the tab(s) in new window each time. (Default=False)    

**`incognito`** --- This parameter decides if the tab(s) would be opened in Incognito mode. (Default=False)   

**`invisible`** --- This parameter decides if the tab(s) would be opened invisibly, and not interactive, so the user would not notice its opened, unless the window plays sound (Default=False).    


Available class methods:   
```python
Help on class psPc in module epsexec:

class psPc(builtins.object)
 |  psPc(ip, username, password)
 |
 |  Methods defined here:
 |
 |  __init__(self, ip, username, password)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  beep(self, frequency, duration_ms, delay_before=100)
 |
 |  closeChrome(self, delay_before=100, runAsAdmin=True)
 |
 |  closeProcess(self, procNameOrID, delay_before=100)
 |
 |  download_nir(self)
 |
 |  enable_remote_desktop(self)
 |
 |  firewallChange(self, state='off', delay_before=100)
 |
 |  getShell(self, shell='cmd.exe', isAdmin=True)
 |
 |  openURL(self, url='*://*/*', fromFile='fileName.txt', tabs=1, new_window=False, delayBeforeOpening=100, delayBetweenTabs=100, incognito=False, invisible=False)
 |
 |  send_screenshot(self, emailRecipientAddr, delay_before=100)
 |
 |  setVolume(self, percent, delay_before=100)
 |
 |  startRemoteDesktop(self)
 |
 |  textToSpeech(self, text, male_voice=True, delay_before=100)
 |
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |
 |  download_psexec()
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
```

### Credits
Epsexec was created by Ori Shamir.   
If you find any bugs, PLEASE report to ***`EpsexecNoReply@gmail.com`***


### Changelog:
**0.4.9** - Fixed openURL delayBetweenTabs not working properly.   

**0.5.1:**   
* Added this changelog.   
* Added static method `download_psexec`. This is to download PsExec on your machine.
* openURL method now automatically gets the installation folder of google chrome.      
* PEP 8:
    * Changed `downloadNirCMD` method name to `download_nir`.   
    * Changed `sleepBefore` parameter name to `delay_before`.   
    * Changed `durationMs` parameter name to `duration_ms` in `beep` method.      


**0.5.3:**   
* Now, openURL saves the installation folder to `globals` dictionary, so you wont do the search process twice.   

**0.5.5:**
* `get_installation_folder` is A nested function inside `openURL`.   
 It gets called if `globals()` dictionary does NOT contain Chrome installation location.    

**0.5.6:**   
* PEP 8:
    * Changed `sendScreenshot` method name to `send_screenshot`.   
    * Changed `newWindow` parameter name to `new_window`.

**0.5.7:**   
* Added `enable_remote_desktop` method.
* Added value `"rdp"` to the `firewallChange` method to allow rdp connections.    
* Change value `"rule"` to `"smb"` in the `firewallChange` method to allow smb connections.   
* PEP 8:
    * When importing, use `from` **`e`**`psexec import psPc`   
    instead of   
    `from Epsexec import psPc`.    
    * Changed `maleVoice` parameter name to `male_voice` in the method `textToSpeech`.
    * Changed `URL` parameter name to `url` in the method `openURL`.
    
