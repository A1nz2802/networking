# CCNA 200-301 Official Cert Guide, Volume 1 - Chapter 6 Labs

Lab topics covering auth concepts.

- [Securing User Mode and Privileged Mode with Simple Passwords](#securing-user-mode-and-privileged-mode-with-simple-passwords)
- [Securing User Mode Access with Local Usernames and Passwords](#securing-user-mode-access-with-local-usernames-and-passwords)
- [Securing Remote Access with Secure Shell](#securing-remote-access-with-secure-shell)
- [Securing User Mode Access with External Authentication Servers](#securing-user-mode-access-with-external-authentication-servers)

## Securing User Mode and Privileged Mode with Simple Passwords

- **Step 1:** Configure the enable password with the enable secret password-value command.
    ```bash
    Switch> enable
    Switch# configure terminal
    Switch(config)# enable secret love
    ```

- **Step 2.** Configure the console password:
    - Use the line con 0 command to enter console configuration mode.
        ```bash
        Switch(config)# line console 0
        ```

    - Use the password password-value subcommand to set the value of the 
    console password.
        ```bash
        Switch(config-line)# password faith
        ```

    - Use the login subcommand to enable console password security using a 
    simple password.
        ```bash
        Switch(config-line)# login
        Switch(config-line)# exit
        ```

- **Step 3.** Configure the Telnet (vty) password:
    - Use the line vty 0 15 command to enter vty configuration mode for all 16 vty lines (numbered 0 through 15).
        ```bash
        Switch(config)# line vty 0 15
        ```

    - Use the password password-value subcommand to set the value of the console password.
        ```bash
        Switch(config-line)# password hope
        ```

    - Use the login subcommand to enable console password security using a simple password.
        ```bash
        Switch(config-line)# login
        Switch(config-line)# end
        ```

- **Step 4.** Check the current configuration:
    ```bash
    Switch# show running-config
    ```

## Securing User Mode Access with Local Usernames and Passwords

- **Step 1:** Use the username name secret password global configuration command to add one or more username/password pairs on the local switch.
    ```bash
    Switch# configure terminal
    Switch(config)# username a1nz secret rem3232 
    Switch(config)# username albedo secret ram1212 
    ```

- **Step 2.** Configure the console to use locally configured username/password pairs:
    - Use the line con 0 command to enter console configuration mode.
        ```bash
        Switch(config)# line console 0
        ```

    - Use the login local subcommand to enable the console to prompt for both username and password, checked versus the list of local usernames/pass-words.
        ```bash
        Switch(config-line)# login local
        ```

    - (Optional) Use the no password subcommand to remove any existing simple shared passwords, just for good housekeeping of the configuration file.
        ```bash
        Switch(config-line)# no password
        ```

- **Step 3.** Configure Telnet (vty) to use locally configured username/password pairs:
    - Use the line vty 0 15 command to enter vty configuration mode for all 16 vty lines (numbered 0 through 15).
        ```bash
        Switch(config)# line vty 0 15
        ```

    - Use the login local subcommand to enable the switch to prompt for both username and password for all inbound Telnet users, checked versus the list of local usernames/passwords.
        ```bash
        Switch(config-line)# login local
        ```

    - (Optional) Use the no password subcommand to remove any existing simple shared passwords, just for good housekeeping of the configuration file.
        ```bash
        Switch(config-line)# no password
        ```



## Securing Remote Access with Secure Shell

- **Step 1.** Configure the switch to generate a matched public and private key pair to use for encryption:
    - If not already configured, use the hostname name in global configuration mode to configure a hostname for this switch.
        ```bash
        Switch# configure terminal
        Switch(config)# hostname mysw1
        ```
    - If not already configured, use the ip domain-name name in global configuration mode to configure a domain name for the switch, completing the switch’s FQDN.
        ```bash
        mysw1(config)# ip domain-name a1nzdev.com
        ```
    - Use the crypto key generate rsa command in global configuration mode (or the crypto key generate rsa modulus modulus-value command to avoid being prompted for the key modulus) to generate the keys. (Use at least a 768-bit key to support SSH version 2.)
        ```bash
        mysw1(config)# crypto key generate rsa
        How many bits in the modulus [512]: 1024
        ```

- **Step 2.** (Optional) Use the ip ssh version 2 command in global configuration mode to override the default of supporting both versions 1 and 2, so that only SSHv2 connections are allowed:
    ```bash
    mysw1(config)# ip ssh version 2
    ```

- **Step 3.** (Optional) If not already configured with the setting you want, configure the vty lines to accept SSH and whether to also allow Telnet:
    ```bash
    mysw1(config)# line vty 0 15
    mysw1(config-line)# login local
    ```

    - Use the transport input ssh command in vty line configuration mode to allow SSH only.
        ```bash
        mysw1(config-line)# transport input ssh
        ```
    - Use the transport input all command (default) or transport input telnet ssh command in vty line configuration mode to allow both SSH and Telnet.
        ```bash
        mysw1(config-line)# transport input all
        ```

- **Step 4.** Use various commands in vty line configuration mode to configure local username login authentication as discussed earlier in this chapter.
    ```bash
    mysw1(config)# username a1nz secret rem3232
    mysw1(config)# username albedo secret ram1212
    ```

- **Step 5.** Display SSH status:
    ```bash
    mysw1# show ip ssh
    mysw1# show ssh
    ```
    
> [!NOTE]
> To control which protocols a switch supports on its vty lines, use the **transport input { all | none | telnet | ssh}** vty subcommand in vty mode.

## Securing User Mode Access with External Authentication Servers