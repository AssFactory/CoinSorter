from machine import Pin
import config
import utime

class CoinSensor:
    def __init__(self, pin_number, trigger=Pin.IRQ_FALLING):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.last_time = utime.ticks_ms()
        self._count = 0  # <--- Die Zählvariable
        
        self.pin.irq(trigger=trigger, handler=self._irq_handler)

    def _irq_handler(self, pin):
        current_time = utime.ticks_ms()
        
        # Führe Entprell-Prüfung durch
        if utime.ticks_diff(current_time, self.last_time) > config.SENSOR_DEBOUNCE:            
                    # Nur bei einem gültigen Ereignis:
            self.last_time = current_time
            self._count += 1  # <--- Nur interne Aktion: Zähler erhöhen
            print(f"DEBUG: Sensor an Pin Zähler auf {self._count} erhöht.")

    # Property-Methode, um den Zählerwert sicher abzufragen
    @property
    def count(self):
        return self._count
    
    def reset_count(self):
        """Setzt den Zähler zurück."""
        self._count = 0