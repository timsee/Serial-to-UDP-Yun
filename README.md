
# Serial-To-UDP-Yun

A simple arduino Yun project that creates a two way communication stream between a device connected to the Yun over UDP and a device connected over serial. Example uses for this project includes making arduino sensor readings accessible over wifi and converting arduino projects into wireless projects quickly by adding in a Yun. 

## <a name="toc"></a>Table of Contents

* [Installation](#installation)
* [Limitations and Potential Changes](#limitations)
* [Version Notes](#changelog)
* [Contributing](#contributing)
* [License](#license)

## <a name="installation"></a>Installation

To get this project running, you'll need to add a python script to the arduino Yun that runs at bootup.

* The first step is the same as any other arduino proejct: upload the [Serial-to-UDP-Yun](Serial-to-UDP-Yun/Serial-to-UDP-Yun.ino) sketch to the arduino yun. 

Now let's get the python script onto the yun's linux microprocessor. To do so, you'll need to get the the IP address of your arduino and the password to ssh into it. For this sample, we will be using the IP address of `192.168.0.102` but this will likely be different in your environment. 

* ssh into your arduino yun. To do so, enter your terminal and run this command:

```
ssh root@192.168.0.102
```
* It will ask you if you are sure you trust your host (choose yes) and then it will ask for the password that you entered during the initial setup of the arduino yun. 

* Now that you're in the arduino's terminal, type this command to make a directory for your sample code:

```
mkdir scripts
```
* Now that we have a place to put the script, we're going to modify the arduino yun's bootup script so that it runs the server automatically. The arduino yun has a very basic version of linux installed, which leads to limited options for text editors. I recommend using vi, which may require you to look up keybindings if you are not familiar. Load `/etc/rc.local` into the text editor, and add this line above the `exit 0` line:

```
python /root/scripts/yun-udp-server.py
```
* Great, now everything that required ssh should be all set up. The next step is to open a new terminal
and navigate to the `/server` directory in this git repo. Then, secure copy the server's python script to the arduino yun. To do so, run this line: 

```
scp yun-udp-server.py root@192.168.0.102:/root/scripts

```

* Restart your arduino yun. If everything is set up correctly, the server should start up at boot and after 30-60 seconds, you'll be able to control the arduino over UDP.

## <a name="limitations"></a>Limitations and Potential Changes

* UDP in this project is faster than the BridgeClient's HTTP but it is still not incredibly fast. Assume you'll only get a few updates per second from this stream.
* UDP is not reliable and serial packets can be dropped or garbled. Because of this, this is not a reliable data stream. 
* No buffer system is implemented anywhere. New packets overwrite old packets even when the old packets haven't been read. 
* Receiving buffer between the Yun and Arduino is 50 characters large. Adjust as needed. 
* Semicolons are used as the delimiter on the arduino side instead of newlines. Adjust as needed.
* UDP code in the python script uses the port 10008. Adjust as needed. 
* The delay between arduino sketch loops that is most effective will vary from application to application. The bridge library benefits from a bit of a delay so it is not recommended to remove it all together. Adjust as needed. 
* If you only want the data stream to go one way (either sending or receiving) you can get a significant speed increase by removing the other direction both from the python script and the arudino sketch.

## <a name="changelog"></a>Version Notes

### **v1.0** 
#### January 22, 2017
* Initial version


## <a name="contributing"></a>Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.


## <a name="license"></a>License

MIT License, provided [here](LICENSE).

