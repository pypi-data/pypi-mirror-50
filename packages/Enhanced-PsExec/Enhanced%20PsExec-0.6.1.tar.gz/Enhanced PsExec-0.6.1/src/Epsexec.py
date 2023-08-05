import os
import sys
import time
import subprocess
import csv

class psPc:

    def __init__(self, **kwargs):
        self.adminSetting = "-s"
        self.dontWaitForTerminate = "-d"
        self.interactive = "-i"
        self.accept_eula = "-accepteula"
        if len(kwargs.keys()) < 3:
            if 'delimiter' in kwargs.keys():
                self.ip, self.username, self.password = self.set_by_config_file(kwargs[list(kwargs.keys())[0]],
                                                                                delimiter=kwargs['delimiter'])
            else:
                self.ip, self.username, self.password = self.set_by_config_file(kwargs[list(kwargs.keys())[0]])
        else:
            self.ip = kwargs[list(kwargs.keys())[0]]
            self.username = kwargs[list(kwargs.keys())[1]]
            self.password = kwargs[list(kwargs.keys())[2]]

    def set_by_config_file(self, file_name, delimiter=' ', extern=False):
        ip = ''
        username = ''
        password = ''
        ips = []
        usernames = []
        passwords = []
        startAble = False
        with open(file_name, 'r', encoding="UTF-8-sig") as file:
            lines = file.readlines()

            for line in lines:
                # print(line)
                if 'config:' in line:
                    startAble = True
                    continue
                if 'endconfig' in line:
                    startAble = False
                    break
                if startAble:
                    # if '\t' in line:
                    line = line.split(delimiter)
                    if '' in line:
                        for i in range(line.count('')):
                            line.remove('')

                    ip, username, password = line
                    # clean everything
                    ip = ip.replace('\t', '')
                    ip = ip.replace(' ', '')

                    password = password.replace('\n', '')


                    ips.append(ip)
                    usernames.append(username)
                    passwords.append(password)
        # end of file read

        index = 1
        # this works because MATH!
        # import math
        print('  ID  |        IP        |       Username      |'+' '*(int((max(list(map(len, passwords))) +2)/2)) + 'Password')
        print('------|------------------|---------------------|'+'-'*(max(list(map(len, passwords)))+9))
        for ip, username, password in zip(ips, usernames, passwords):
            print('  '+str(index), end='')
            print(' '*(4-len(str(index))), end='')

            print('|', ip, end='')
            print(' '*(17-len(ip)), end='')

            print('|', username,end='')
            print(' '*(19-len(username)), '|', end='')

            print(' '+password)
            # os.system("pause")
            index += 1
        index = int(input("\n    Choice: "))
        ip, username, password = ips[index-1], usernames[index-1], passwords[index-1]
        if not extern:
            return ip, username, password
        else:
            self.ip, self.username, self.password = ip, username, password

    def openURL(self, url="*://*/*", fromFile="fileName.txt", delimiter=' ', tabs=1, new_window=False, delayBeforeOpening=100,
                delayBetweenTabs=100, incognito=False, invisible=False):
        def get_installation_folder():
            p = subprocess.Popen(
                f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.accept_eula} {self.adminSetting} cmd.exe /c cd "c:\\Program Files (x86)\\Google\\Chrome\\Application" & where chrome.exe',
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            p.communicate(b"input data that is passed to subprocess' stdin")
            return_code = p.returncode
            if return_code == 0:
                # Its in program files x86

                Installation_location = 'c:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

            else:
                p = subprocess.Popen(
                    f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.accept_eula} {self.adminSetting} cmd.exe /c cd "%userprofile%\\AppData\\Local\\Google\\Chrome\\Application" & where chrome.exe',
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate(b"input data that is passed to subprocess' stdin")
                return_code = p.returncode
                if return_code == 0:
                    user_profile = "C:\\users\\{0}".format(self.username)
                    Installation_location = user_profile + '\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'

                else:
                    # Its in program files x64
                    Installation_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            return Installation_location

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
            startAble = False
            for line in file.readlines():
                if "urls:" in line or "url:" in line:
                    startAble = True
                    continue
                if "endurl" in line:
                    startAble = False
                    break
                if startAble:
                    # get name and URL to assign to the dictionary. split them by space and get only the string itself
                    # without special characters like \n or \t
                    line = line.split(delimiter)
                    if '' in line:
                        for i in range(line.count('')):
                            line.remove('')

                    name, url = line
                    # url = line.split(' ')[1][:-1]
                    name = name.replace(' ', '')
                    name = name.replace('\t', '')
                    url = url.replace(' ', '')
                    url = url.replace('\n', '')

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

    def getShell(self, shell="cmd.exe", run_as_admin=True):
        if not run_as_admin:
            self.adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} {self.accept_eula} {shell}")
        self.adminSetting = '-s'

    def close_process(self, procNameOrID, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.accept_eula} cmd.exe /c taskkill /F /IM {procNameOrID} /T ")

    def firewallChange(self, state="off", delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        if state.lower() == "smb":
            subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} cmd.exe /c netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in new enable=Yes')
        elif state.lower() == "rdp":
            subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} cmd.exe /c netsh advfirewall firewall set rule group="remote desktop" new enable=Yes')
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} cmd.exe /c netsh advfirewall set allprofiles state {state}")

    def startRemoteDesktop(self):
        subprocess.call(f"mstsc /v {self.ip}")

    def enable_remote_desktop(self):
        subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} cmd /c reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f')

    def download_nir(self):

        powershell_command = 'wget """http://www.nirsoft.net/utils/nircmd-x64.zip""" -OutFile C:\\windows\\system32\\nircmd.zip; '
        powershell_command += 'Expand-Archive -Force C:\\windows\\system32\\nircmd.zip -DestinationPath C:\\windows\\system32; '
        powershell_command += 'del C:\\windows\\system32\\nircmd.zip'

        subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} powershell /c {powershell_command}')

    def setVolume(self, percent, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        # max = 65535
        num_from_perc = 655 * percent

        if percent == 0 or percent.lower() == "mute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 1")
        elif percent == 101 or percent.lower() == "unmute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 0")
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.accept_eula} nircmd.exe cmdwait {delay_before} setsysvolume {num_from_perc}")

    def textToSpeech(self, text, male_voice=True, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        # self.adminsetting for male
        if not male_voice:
            self.adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.interactive} {self.accept_eula} nircmd.exe speak text \"{text}\"")
        self.adminSetting = "-s"

    def beep(self, frequency, duration_ms, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)

        # self.interactive (-i) is a MUST
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.interactive} {self.accept_eula} nircmd.exe beep {frequency} {duration_ms}")

    def send_screenshot(self, email_recipient_addr, delay_before=100):
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
        powershell_command = "$ip=$([System.Net.Dns]::GetHostAddresses($hostname)); "
        powershell_command += "$i = Get-ComputerInfo; "
        powershell_command += "$m=New-Object System.Net.Mail.MailMessage; "
        powershell_command += f'$m.subject="""ScreenShot Captured from {self.ip}"""; '
        powershell_command += "$m.IsBodyHtml=$true; "
        powershell_command += f'$m.body = """{body}"""; '
        powershell_command += f'$m.to.add("""{email_recipient_addr}"""); '
        powershell_command += '$m.from="""Epsexec@NoReply <EpsexecNoReply@gmail.com>"""; '
        powershell_command += '$m.attachments.add("""C:\\epsexecScreenshot.png"""); '
        powershell_command += '$c=New-Object Net.Mail.SmtpClient("""smtp.gmail.com""", 587); '
        powershell_command += "$c.EnableSsl=$true; "
        powershell_command += '$c.Credentials=New-Object System.Net.NetworkCredential("""EpsexecNoReply@gmail.com""", """qncoqhtnqasyqgmg"""); '
        powershell_command += "$c.Send($m); "
        powershell_command += "del C:\\epsexecScreenshot.png"
        # sleeeep
        time.sleep(delay_before)
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.adminSetting} {self.accept_eula} nircmd savescreenshot C:\\epsexecScreenshot.png")

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.accept_eula} powershell.exe {powershell_command}")

    def closeChrome(self, delay_before=100):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} {self.accept_eula} cmd.exe /c taskkill /F /IM chrome.exe /t")


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

        install_to = 'C:\\windows\\system32'
        # Enhanced PsExec uses 64-bit python. check for it
        if not sys.maxsize > 2 ** 32:
            install_to = 'C:\\windows\\sysWOW64'

        ps_command = f'wget "https://download.sysinternals.com/files/PSTools.zip" -OutFile {install_to}\\PsExec.zip; '
        ps_command += f'Expand-Archive -Force C:\\windows\\system32\\PsExec.zip -DestinationPath {install_to}; '
        ps_command += f'del {install_to}\\PsExec.zip'
        os.system(f'powershell {ps_command}')
