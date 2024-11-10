import wmi

def monitor_usb_printer():
    # Set up the WMI interface
    wmi_obj = wmi.WMI()
    watcher = wmi_obj.Win32_USBControllerDevice.watch_for("creation")  # Listen for USB device addition

    print("Monitoring for USB printer connection...")

    while True:
        # Wait for a new USB device to be plugged in
        device = watcher()
        
        # Get device information
        usb_device = device.Dependent
        device_name = usb_device.Name
        
        # Check if it matches the printer name or part of it
        if "Brother DCP-T310" in device_name:
            print(f"Printer '{device_name}' connected!")
            break  # Optionally exit loop if you only want to detect once

# Start monitoring
monitor_usb_printer()
