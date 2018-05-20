# Variability

Variability: An ncurses-based frontend for Volatility.

<a href="http://www.desperadosecurity.com/images/variability/ScreenShot1.png"><img src="http://www.desperadosecurity.com/images/variability/ScreenShot1.png" width="75%"></a>

### Prerequisites
* Volatility
* A full memory dump compatible with Volatility

## Getting a memory dump: 
### From a VirtualBox VM
* If you are running a malware sample in VirtualBox, you can dump memory from within Variability:
* Edit config.ini VMNAME field to match the name of your target VM.
* Press 'd' and wait for the dump to complete (it will be created at the path specified in config.ini).
* Alternately, you can manually run:
```VBoxManage debugvm <uuid|vmname> dumpvmcore```

### Other methods 
* Use a popular memory dumping tool such as [DumpIt](https://blog.comae.io/your-favorite-memory-toolkit-is-back-f97072d33d5c)
* Specify this dumpfile from the command line.

To run with an existing memory dump:
```
python run.py /path/to/dump.bin
```
