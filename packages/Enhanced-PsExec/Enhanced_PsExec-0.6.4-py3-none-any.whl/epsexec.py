import os
import sys
import time
import subprocess


class pspc:

    def __init__(self, **kwargs):
        self._adminSetting = "-s"
        self._dontWaitForTerminate = "-d"
        self._interactive = "-i"
        self._accept_eula = "-accepteula"
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

    def __getitem__(self, item):
        if item == 0 or item == 'ip':
            return self.ip
        elif item == 1 or item == 'username':
            return self.username
        elif item == 2 or item == 'password' or item == 'pass':
            return self.password
        else:
            raise IndexError("Index does not exist. (index 0-2)")

    def __setitem__(self, key, value):
        if key == 0 or key == 'ip':
            self.ip = value
        elif key == 1 or key == 'username':
            self.username = value
        elif key == 2 or key == 'password' or key == 'pass':
            self.password = value
        else:
            raise IndexError("Index does not exist. (index 0-2)")

    def __repr__(self):
        return "<Enhanced-PsExec: [{0}, {1}, {2}]>".format(self.ip, self.username, self.password)

    def set_by_config_file(self, file_name, delimiter=' ', extern=False):

        ips = []
        usernames = []
        passwords = []

        startAble = False
        with open(file_name, 'r', encoding="UTF-8-sig") as file:
            lines = file.readlines()

            for line in lines:
                if 'config:' in line:
                    startAble = True
                    continue
                if 'endconfig' in line:
                    startAble = False
                    break
                if startAble:
                    # if '\t' in line:
                    line = line.split(delimiter)
                    line = list(filter(lambda x: x != '', line))

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
        # import MATH
        max_ips = max(list(map(len, ips)))+8
        max_usernames = max(list(map(len, usernames)))
        max_passwords = max(list(map(len, passwords)))
        max_index = len(ips)

        print(f'{"ID":^{max_index+6}s}|{"IP":^{max_ips}s}|{"Username":^{max_usernames+13}s}|{"Password":^{max_passwords+12}s}|')
        print(f'---{"":-^{max_index}s}---|{"":-^{max_ips}s}|{"":-^{max_usernames+13}}|{"":-^{max_passwords+12}}|')
        for ip, username, password in zip(ips, usernames, passwords):
            index_len = len(str(index))
            ip_len = len(ip)
            # print ID
            print(f'   {index:^{index_len+1}d}   |', end='')

            # print IP
            print(f'    {ip:^{max_ips-8}s}    |', end='')

            # print Username
            print(f'    {username:^{max_usernames+5}s}    |', end='')

            # print Password
            print(f'    {password:^{max_passwords+4}s}    |')
            index += 1
        index = int(input("\n    Choice: "))
        ip, username, password = ips[index-1], usernames[index-1], passwords[index-1]

        if not extern:
            return ip, username, password
        else:
            self.ip, self.username, self.password = ip, username, password

    def openURL(self, url="*://*/*", fromFile="fileName.txt", delimiter=' ', tabs=1, new_window=False, delay_before=0,
                delay_between=10, incognito=False, invisible=False):
        """

        URL --- This is the URL to be opened in the remote machine. If `fromFile` parameter is used, it must be: `'*://*/*'`, its default

        fromFile --- This parameter is used to take A text file and get every URL and its shotcut name.
        See more: https://github.com/orishamir/Epsexec/blob/master/fromFile.md

        delimiter --- This is only if you also specified `fromFile` - How to seperate each name,url

        tabs --- This parameter is responsible for the amount of tabs to open on the remote machine. (Default=1)

        delayBeforeOpening --- This parameter decides how much time in millisecond the program should pause before starting the operation. (Default=100)

        delayBetweenTabs --- This parameter decides how much time in millisecond the program should pause BETWEEN every time it opens A new tab.

        new_window --- This parameter decides whether or not to open the tab(s) in new window each time. (Default=False)

        incognito --- This parameter decides if the tab(s) would be opened in Incognito mode. (Default=False)

        invisible --- This parameter decides if the tab(s) would be opened invisibly, and not interactive, so the user would not notice its opened, unless the window plays sound (Default=False).
        """

        # set minimum requirements for delay before opening and delay between tab
        delay_before = 0 if delay_before < 0 else delay_before
        delay_between = 10 if delay_between < 10 else delay_between

        delay_before /= 1000
        delay_between /= 1000

        def get_installation_folder():
            p = subprocess.Popen(
                f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._accept_eula} {self._adminSetting} cmd.exe /c cd "c:\\Program Files (x86)\\Google\\Chrome\\Application" & where chrome.exe',
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            p.communicate(b"input data that is passed to subprocess' stdin")
            return_code = p.returncode
            if return_code == 0:
                # Its in program files x86

                Installation_location = 'c:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

            else:
                p = subprocess.Popen(
                    f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._accept_eula} {self._adminSetting} cmd.exe /c cd "%userprofile%\\AppData\\Local\\Google\\Chrome\\Application" & where chrome.exe',
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

            with open(fromFile, 'r', encoding="UTF-8-sig") as file:
                urls = {}
                can_start = False
                for line in file.readlines():
                    if "urls:" in line or "url:" in line:
                        can_start = True
                        continue
                    if "endurl" in line or line == 'config:':
                        can_start = False
                        break
                    if can_start:
                        # get name and URL to assign to the dictionary. split them by space and get only the string itself
                        # without special characters like \n or \t
                        line = line.split(delimiter)
                        line = filter(lambda x: x != '', line)

                        name, url = line
                        name = name.replace(' ', '')
                        name = name.replace('\t', '')
                        url = url.replace(' ', '')
                        url = url.replace('\n', '')

                        urls[name] = url
            # ended getting values from file

            ##########################################
            # what does the USER want?
            user_index = 1

            for shortName, url in urls.items():
                print(f'      {user_index}. {shortName} {"":.^{40 - len(shortName)}} {url}')
                user_index += 1

            # In python  3.8 - change this to: while (user_index := input("Choice: ") (not in urls.keys() and type(
            # user_index) != int) or (type(user_index) == int and user_index > len(urls.keys())):

            user_index = input("\n    Choice: ")

            # if the user picked the name not by index number but from shortcut name then yes
            if user_index in urls.keys():
                url = urls[user_index]
            else:
                if user_index.isalpha():
                    raise ValueError("URL Shortcut does not exist.")
                # get the list of the urls and get the user's index minus 1 cuz it starts at 0.
                elif int(user_index) > len(urls.keys()):
                    raise IndexError("URL index does not exist.")
                url = list(urls.values())[int(user_index) - 1]

        # sleep before opening tabs
        time.sleep(delay_before)

        if invisible:
            # if user wants invisible to be True:
            if delay_between == 500 and new_window != "--new-window":
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} cmd /c start " + f" {url} "*tabs + f" {new_window} {incognito} ")
            for tab in range(1, tabs + 1):
                # make invisible somehow...
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._accept_eula} cmd.exe /c start chrome {url} {new_window} {incognito}")
                time.sleep(delay_between)
        else:
            # get chrome installation location
            try:
                installation_location = globals()['installation_location']
            except KeyError:
                globals()['installation_location'] = get_installation_folder()

            installation_location = globals()['installation_location']
            # if user DOES NOT WANT invisible:
            # if we can do it in one line, do it
            if delay_between == 10 and new_window != "--new-window":
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._interactive} {self._dontWaitForTerminate} {self._accept_eula} \"{installation_location}\"" + f" {url} " * tabs + f" {new_window} {incognito} {self._accept_eula}")
            # else:
            for tab in range(1, tabs + 1):
                # make start visible
                subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._interactive} {self._dontWaitForTerminate} {self._accept_eula} \"{installation_location}\" {url} {new_window} {incognito}")
                time.sleep(delay_between)

    def getShell(self, shell="cmd.exe", run_as_admin=True):
        """

        shell --- program to open (default "cmd.exe")
        run_as_admin --- Should the shell be ran with administrative privileges (default True)

        """
        if not run_as_admin:
            self._adminSetting = ''
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._adminSetting} {self._accept_eula} {shell}")
        self._adminSetting = '-s'

    def close_process(self, proc_name, delay_before=0):
        """
        proc_name --- The process to close (could be either a name, or an ID).
        delay_before --- The amount (in milliseconds) to pause before closing the process.
        """
        # if sleep before less than 1, NO.
        delay_before = 0 if delay_before < 0 else delay_before
        delay_before /= 1000
        time.sleep(delay_before)

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._accept_eula} cmd.exe /c taskkill /F /IM {proc_name} /T ")

    def firewallChange(self, state="smb", delay_before=0):
        """
        
        state --- Controls the operation to perform.
            off/on - Turn off/on the firewall.
            smb - Add a rule to allow smb connections (recommended).
            rdp - Add a rule to allow remote desktop connections.

        delay_before --- The amount (in milliseconds) to pause before performing the operation.
        """
        # if sleep before less than 1, NO.
        delay_before = 0 if delay_before < 0 else delay_before
        delay_before /= 1000
        time.sleep(delay_before)
        if state.lower() == "smb":
            subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} cmd.exe /c netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in new enable=Yes')
        elif state.lower() == "rdp":
            subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} cmd.exe /c netsh advfirewall firewall set rule group="remote desktop" new enable=Yes')
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} cmd.exe /c netsh advfirewall set allprofiles state {state}")

    def startRemoteDesktop(self):
        subprocess.call(f"mstsc /v {self.ip}")

    def enable_remote_desktop(self):
        subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} cmd /c reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f')

    def download_nir(self):

        powershell_command = 'wget """http://www.nirsoft.net/utils/nircmd-x64.zip""" -OutFile C:\\windows\\system32\\nircmd.zip; '
        powershell_command += 'Expand-Archive -Force C:\\windows\\system32\\nircmd.zip -DestinationPath C:\\windows\\system32; '
        powershell_command += 'del C:\\windows\\system32\\nircmd.zip'

        subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} powershell /c {powershell_command}')

    def set_volume(self, percent, delay_before=0):
        # if sleep before less than 1, NO.
        delay_before = 0 if delay_before < 0 else delay_before
        delay_before /= 1000
        # max = 65535
        num_from_perc = 655 * percent
        time.sleep(delay_before)
        if percent == 0 or percent.lower() == "mute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 1")
        elif percent == 101 or percent.lower() == "unmute":
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} nircmd.exe cmdwait {delay_before} nircmd mutesysvolume 0")
        else:
            subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._accept_eula} nircmd.exe cmdwait {delay_before} setsysvolume {num_from_perc}")

    def textToSpeech(self, text, male_voice=True, delay_before=0):
        # if sleep before less than 1, NO.
        delay_before = 0 if delay_before < 0 else delay_before
        delay_before /= 1000
        # self.adminsetting for male
        if not male_voice:
            self._adminSetting = ''
        time.sleep(delay_before)
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._adminSetting} {self._interactive} {self._accept_eula} nircmd.exe speak text \"{text}\"")
        self._adminSetting = '-s'

    def beep(self, frequency, duration_ms, delay_before=0):
        # if sleep before less than 1, NO.
        delay_before = 0 if delay_before < 0 else delay_before
        delay_before /= 1000
        time.sleep(delay_before)
        # self._interactive (-i) is a MUST
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._interactive} {self._accept_eula} nircmd.exe beep {frequency} {duration_ms}")

    def send_screenshot(self, email_recipient_addr, delay_before=0):
        delay_before = 0 if delay_before < 0 else delay_before
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
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._interactive} {self._adminSetting} {self._accept_eula} nircmd savescreenshot C:\\epsexecScreenshot.png")

        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._dontWaitForTerminate} {self._accept_eula} powershell.exe {powershell_command}")

    def close_chrome(self, delay_before=0):
        # if sleep before less than 1, NO.
        delay_before /= 1000
        time.sleep(delay_before)
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._adminSetting} {self._accept_eula} cmd.exe /c taskkill /F /IM chrome.exe /t")

    def run_command(self, program, arguments, delay_before=0, run_as_admin=True, invisible=False):
        delay_before /= 1000
        time.sleep(delay_before)
        if not run_as_admin:
            self._adminSetting = ''
        if invisible:
            invisible = ''
        else:
            invisible = '-i'
        subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self._accept_eula} {self._dontWaitForTerminate} {self._adminSetting} {invisible} {program} /c {arguments}")
        self._adminSetting = '-s'
        self._interactive = '-i'

#   def addurltoFile(self,fileNames,urls):
#       fileNames = list(fileNames.split(','))
#       urls = list(urlS.split(','))

    # def run_exe(self):

    @staticmethod
    def download_psexec():
        # Check if python is ran as administrator
        try:
            # only windows users with admin privileges can read C:\windows\temp
            os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        except PermissionError:
            print("\n**********WARNING: this may not work, because you did not run python as administrator.**********")
            time.sleep(1)

        install_to = 'C:\\windows\\system32'
        # check for it
        if not sys.maxsize > 2 ** 32:
            install_to = 'C:\\windows\\sysWOW64'

        ps_command = f'wget "https://download.sysinternals.com/files/PSTools.zip" -OutFile {install_to}\\PsExec.zip; '
        ps_command += f'Expand-Archive -Force C:\\windows\\system32\\PsExec.zip -DestinationPath {install_to}; '
        ps_command += f'del {install_to}\\PsExec.zip'
        os.system(f'powershell {ps_command}')


        print(r' _______   ________   ___  ___  ________  ________   ________  _______   ________ ')
        print(r'|\  ___ \ |\   ___  \|\  \|\  \|\   __  \|\   ___  \|\   ____\|\  ___ \ |\   ___ \ ')
        print(r'\ \   __/|\ \  \\ \  \ \  \\\  \ \  \|\  \ \  \\ \  \ \  \___|\ \   __/|\ \  \_|\ \ ')
        print(r' \ \  \_|/_\ \  \\ \  \ \   __  \ \   __  \ \  \\ \  \ \  \    \ \  \_|/_\ \  \ \\ \ ')
        print(r'  \ \  \_|\ \ \  \\ \  \ \  \ \  \ \  \ \  \ \  \\ \  \ \  \____\ \  \_|\ \ \  \_\\ \ ')
        print(r'   \ \_______\ \__\\ \__\ \__\ \__\ \__\ \__\ \__\\ \__\ \_______\ \_______\ \_______\ ')
        print(r'    \|_______|\|__| \|__|\|__|\|__|\|__|\|__|\|__| \|__|\|_______|\|_______|\|_______| ')
        print(r' ')
        print(r' ')
        print(r' ')
        print(r'                    ________  ________  _______      ___    ___ _______   ________ ')
        print(r'                   |\   __  \|\   ____\|\  ___ \    |\  \  /  /|\  ___ \ |\   ____\ ')
        print(r'                   \ \  \|\  \ \  \___|\ \   __/|   \ \  \/  / | \   __/|\ \  \___| ')
        print(r'                    \ \   ____\ \_____  \ \  \_|/__  \ \    / / \ \  \_|/_\ \  \ ')
        print(r'                     \ \  \___|\|____|\  \ \  \_|\ \  /     \/   \ \  \_|\ \ \  \____ ')
        print(r'                      \ \__\     ____\_\  \ \_______\/  /\   \    \ \_______\ \_______\ ')
        print(r'                       \|__|    |\_________\|_______/__/ /\ __\    \|_______|\|_______| ')
        print(r'                                \|_________|        |__|/ \|__| ')
        print(r' ')

        print('', end='\n\n\n')


