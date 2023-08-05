import os
import sys
import time
import subprocess


class psPc:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.adminSetting = "-s"
        self.dontWaitForTerminate = "-d"
        self.interactive = "-i"
        self.accept_eula = "-accepteula"

    def openURL(self, url="*://*/*", fromFile="fileName.txt", tabs=1, new_window=False, delayBeforeOpening=100,
                delayBetweenTabs=100, incognito=False, invisible=False):
        def get_installation_folder():
            p = subprocess.Popen(
                f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.accept_eula} {self.adminSetting} cmd.exe /c cd "c:\\Program Files (x86)\\Google\\Chrome\\Application" & where chrome.exe',
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            p.communicate(b"input data that is passed to subprocess' stdin")
            returncode = p.returncode
            if returncode == 0:
                # Its in program files x86

                installation_location = 'c:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

            else:
                p = subprocess.Popen(
                    f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.accept_eula} {self.adminSetting} cmd.exe /c cd "%userprofile%\\AppData\\Local\\Google\\Chrome\\Application" & where chrome.exe',
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate(b"input data that is passed to subprocess' stdin")
                returncode = p.returncode
                if returncode == 0:
                    user_profile = "C:\\users\\{0}".format(self.username)
                    installation_location = user_profile + '\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'

                else:
                    # Its in program files x64
                    installation_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            return installation_location



        # set minimum requirements for delay before opening and delay between tab
        delayBeforeOpening = 1 if delayBeforeOpening < 1 else delayBeforeOpening
        delayBeforeOpening /= 1000
        delayBetweenTabs = 100 if delayBetweenTabs < 100 else delayBetweenTabs
        delayBetweenTabs /= 1000

        # get incognito value
        if incognito:
            incognito = " -incognito"
        else:
            incognito = ""

        # --new-window to get new tab
        if new_window:
            new_window = "--new-window"
        else:
            new_window = ""

        # IMPORT FROM FILE ################################3
        if fromFile != "fileName.txt" or url == "*://*/*":
            # get user text file name (fromFile)
            # save into list using a pre-made config structure
            # output to the user the things
            # get user's choice

            file = open(fromFile, 'r', encoding="UTF-8-sig")
            urls = {}
            for line in file.readlines():
                if "urls:" in line:
                    continue
                if "endurl" in line:
                    break
                # get name and URL to assign to the dictionary. split them by space and get only the string itself
                # without special characters like \n or \t
                name = line.split(' ')[0][1:]
                url = line.split(' ')[1][:-1]
                urls[name] = url
            # ended getting values from file
            file.close()

            ##########################################
            # what does the USER want?
            user_index = 1
            for shortName, url in urls.items():
                msg = f"{shortName}"
                msg += ' ' + '.' * (35 - len(shortName)) + ' ' + url
                print(f"      {user_index}. " + f"{msg}")
                user_index += 1
            user_index = input("\n    Choice: ")

            # if the user picked the name not bye index number but from shortcut name then yes
            if user_index in urls.keys():
                url = urls[user_index]
            else:
                # get the list of the urls and get the user's index minus 1 cuz it starts at 0.
                url = list(urls.values())[int(user_index) - 1]

        # sleep before opening tabs
        time.sleep(delayBeforeOpening)

        if invisible:
            # if user wants invisible to be True:
            if delayBetweenTabs == 500 and new_window != "--new-window":
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} cmd /c start " + f" {url} "*tabs + f" {new_window} {incognito} ")
            for tab in range(1, tabs + 1):
                # make invisible somehow...
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.accept_eula} cmd.exe /c start chrome {url} {new_window} {incognito}")
                time.sleep(delayBetweenTabs)
        else:
            # get chrome installation location

            # check for the location
            try:
                installation_location = globals()['installation_location']
            except KeyError:
                globals()['installation_location'] = get_installation_folder()

            installation_location = globals()['installation_location']
            # if user DOES NOT WANT invisible:
            # if we can do it in one line, do it
            if delayBetweenTabs == 100 and new_window != "--new-window":
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.dontWaitForTerminate} {self.accept_eula} \"{installation_location}\"" + f" {url} " * tabs + f" {new_window} {incognito} {self.accept_eula}")
            # else:
            for tab in range(1, tabs + 1):
                # make start visible
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.dontWaitForTerminate} {self.accept_eula} \"{installation_location}\" {url} {new_window} {incognito}")
                time.sleep(delayBetweenTabs)

    def getShell(self, shell="cmd.exe", isAdmin=True):
        if not isAdmin:
            self.adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} {self.accept_eula} {shell}")
        self.adminSetting = '-s'

    def closeProcess(self, procNameOrID, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.accept_eula} cmd.exe /c taskkill /F /IM {procNameOrID} /T ")

    def firewallChange(self, state="off", delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        if state == "rule":
            subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} cmd.exe /c netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in new enable=Yes')
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} cmd.exe /c netsh advfirewall set allprofiles state {state}")

    def startRemoteDesktop(self):
        subprocess.call(f"mstsc /v {self.ip}")

    def download_nir(self):
        powershell_command = 'wget """http://www.nirsoft.net/utils/nircmd-x64.zip""" -OutFile C:\\windows\\system32\\nircmd.zip; '
        powershell_command += 'Expand-Archive -Force C:\\windows\\system32\\nircmd.zip -DestinationPath C:\\windows\\system32; '
        powershell_command += 'del C:\\windows\\system32\\nircmd.zip'

        subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} powershell /c {powershell_command}')

    def setVolume(self, precent, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        # max = 65535
        num_from_prec = 655 * precent

        if precent == 0 or precent.lower() == "mute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 1")
        elif precent == 101 or precent.lower() == "unmute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 0")
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} setsysvolume {num_from_prec}")

    def textToSpeech(self, text, maleVoice=True, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        # self.adminsetting for male
        if not maleVoice:
            self.adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.interactive} {self.accept_eula} nircmd.exe speak text \"{text}\"")
        self.adminSetting = "-s"

    def beep(self, frequency, duration_ms, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        # self.interactive (-i) is a MUST
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.interactive} {self.accept_eula} nircmd.exe beep {frequency} {duration_ms}")

    def send_screenshot(self, emailRecipientAddr, delay_before=100):
        delay_before /= 1000

        body = "<center>"
        body += "<p dir=\"\"ltr\"\" center=\"\"true\"\">"
        body += "<b><font size=4>"
        body += "Computer Information:"
        body += "</font><br >"
        body += "<font size=3>"
        body += "User:"
        body += "</font>"
        body += " $($i.CsUsername)<br>"

        body += "<font size=3>"
        body += "IP: "
        body += "</font>"
        body += "$($ip[0].IPAddressToString)"
        body += "<br>"
        body += "<font size=3>"
        body += "CPU: "
        body += "</font>"
        body += "$($i.CsProcessors.Name)"
        body += "</b>"
        body += "</p>"
        body += "</center>"
        # m = message
        # c = SMTPClient
        # i = Get-ComputerInfo
        powershellCommand = "$ip=$([System.Net.Dns]::GetHostAddresses($hostname)); "
        powershellCommand += "$i = Get-ComputerInfo; "
        powershellCommand += "$m=New-Object System.Net.Mail.MailMessage; "
        powershellCommand += f'$m.subject="""ScreenShot Captured from {self.ip}"""; '
        powershellCommand += "$m.IsBodyHtml=$true; "
        powershellCommand += f'$m.body = """{body}"""; '
        powershellCommand += f'$m.to.add("""{emailRecipientAddr}"""); '
        powershellCommand += '$m.from="""Epsexec@NoReply <EpsexecNoReply@gmail.com>"""; '
        powershellCommand += '$m.attachments.add("""C:\\EpsexecScreenshot.png"""); '
        powershellCommand += '$c=New-Object Net.Mail.SmtpClient("""smtp.gmail.com""", 587); '
        powershellCommand += "$c.EnableSsl=$true; "
        powershellCommand += '$c.Credentials=New-Object System.Net.NetworkCredential("""EpsexecNoReply@gmail.com""", """qncoqhtnqasyqgmg"""); '
        powershellCommand += "$c.Send($m)"
        # sleeeep
        time.sleep(delay_before)
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.adminSetting} {self.accept_eula} nircmd savescreenshot C:\\EpsexecScreenshot.png")

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.accept_eula} powershell.exe {powershellCommand}")

    def closeChrome(self, delay_before=100, runAsAdmin=True):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        if not runAsAdmin:
            self.adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} {self.accept_eula} cmd.exe /c taskkill /F /IM chrome.exe /t")
        self.adminSetting = '-s'

#   def addurltoFile(self,fileNames,urls):
#       fileNames = list(fileNames.split(','))
#       urls = list(urlS.split(','))

    @staticmethod
    def download_psexec():
        # Check if python is ran as administrator
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        except PermissionError:
            print("**********WARNING: this may not work, because you did not run python as administrator.**********")
            time.sleep(1)

        ps_command =  'wget "https://download.sysinternals.com/files/PSTools.zip" -OutFile C:\\windows\\system32\\PsExec.zip; '
        ps_command += 'Expand-Archive -Force C:\\windows\\system32\\PsExec.zip -DestinationPath C:\\windows\\system32; '
        ps_command += 'del C:\\windows\\system32\\PsExec.zip'
        os.system(f'powershell {ps_command}')


# Enhanced PsExec uses 64-bit python. check for it
if not sys.maxsize > 2 ** 32:
    print("\n\n\n\n                    You must have a 64-bit installation of python or Epsexec will not work.")