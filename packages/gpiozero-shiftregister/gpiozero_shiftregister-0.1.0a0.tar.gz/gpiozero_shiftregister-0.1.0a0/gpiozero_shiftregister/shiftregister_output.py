from gpiozero import CompositeOutputDevice, DigitalOutputDevice, GPIOPinMissing


class ShiftRegisterOutputDevice(CompositeOutputDevice):
    """Extends :class:`gpizero.CompositeOutputDevice` and represents a
    shift register such as SNx4HC595.

    Attach the SER, SERCLK, and RCLK to your Pi. connect OE to
    ground and SRCLR to high.

    TODO: Allow controlling of the SRCLR and OE pins

    """
    def __init__(self, serial=None, shift_clock=None, register_clock=None,
                 enable=None, clear=None, bits=8):
        if serial is None or shift_clock is None or register_clock is None:
            raise GPIOPinMissing(
                'serial, shift_clock pin must be provided'
            )

        self.bits = bits
        self.pulse_length = 700E-9  # 700 nano sec should be more than enough

        super(ShiftRegisterOutputDevice, self).__init__(
            serial_device=DigitalOutputDevice(serial, initial_value=False),
            shift_clock_device=DigitalOutputDevice(shift_clock,
                                                   initial_value=False),
            register_clock_device=DigitalOutputDevice(register_clock,
                                                      initial_value=False)
        )

    """
    Internal value of shift register
    """
    _value = 0

    @property
    def value(self):
        """
        Represents the current value of all the bits in the register.
        """
        return self._value

    @value.setter
    def value(self, value):
        if(not isinstance(value, int) or value < 0):
            raise TypeError("Value must be positive integer")

        print(self.bits)
        for bit_position in range(self.bits):
            self.serial_device.value = bool(value & 2**bit_position)
            self.shift_clock_device.blink(
                self.pulse_length,
                self.pulse_length,
                1,
                background=False)
        self.register_clock_device.blink(
            self.pulse_length,
            self.pulse_length,
            1,
            background=False
        )
        self._value = value

    def set_pin(self, pin, value):
        """
        Sets the value of a specific, pin/bit of the serial register.

        :type pin: int
        :param pin: The pin to set on the shift register

        :param bool value: The state to set the specified pin.
        """
        if value:
            return self.pin_on(pin)
        return self.pin_off(pin)

    def pin_on(self, pin):
        """
        Turns on a pin

        :param int pin: the pin to turn on
        """
        self.value |= (1 << pin)
        return self.value

    def pin_off(self, pin):
        """
        Turn off a pin
        :param int pin: the pin number to turn off

        """
        self.value &= ~(1 << pin)
        return self.value
