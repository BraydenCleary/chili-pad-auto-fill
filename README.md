# Chili Pad Auto-Fill

Automatically refills your [Chili Sleep](https://chilisleep.com) device's water reservoir once a day using an ESP32, a peristaltic pump, and a water level sensor. Just plug it in each morning and it checks the level and tops up if needed — no more waking up to a dry pad.

---

## How It Works

On power-up the ESP32 checks the water level sensor. If the reservoir is low it runs the peristaltic pump until the sensor reads full (or hits the 30-second safety timeout). Then it sleeps for 24 hours and repeats. Plug it in whenever you want the daily check to happen.

---

## Parts List

| Part | Notes |
|---|---|
| ESP32 dev board (WROOM) | Any standard 38-pin ESP32 works |
| [Kamoer 12V peristaltic pump](https://www.kamoer.com) | KPP-DC-S108 or similar |
| CQRobot optical water level sensor | Has a 3V/5V selector switch — set to 3V |
| 1-channel relay module (high/low level trigger) | Songle SRD-05VDC or similar |
| 12V 2A DC wall adapter | Barrel connector, cut off and strip the wires |
| Silicone tubing | Match your pump's tube diameter |
| WAGO 222-412 lever connectors | For joining pump and adapter ground wires |
| Male-to-male jumper wires | For connecting pump terminals to relay |
| Female-to-male jumper wires | For connecting sensor and relay to ESP32 |

---

## Wiring

### Sensor → ESP32
| Sensor wire | ESP32 pin |
|---|---|
| Red (VCC) | 3V3 |
| Black (GND) | GND |
| Green (signal) | P23 |

⚠️ Make sure the selector switch on the sensor is set to **3V** or it won't respond.

### Relay control side → ESP32
| Relay terminal | ESP32 pin |
|---|---|
| DC+ | 5V (VIN) |
| DC- | GND |
| IN | P22 |

### Relay switch side → pump (12V circuit)
| From | To |
|---|---|
| 12V adapter `+` (red wire) | Relay `COM` |
| Relay `NO` | Pump terminal 1 (via jumper wire) |
| 12V adapter `−` (black wire) | Pump terminal 2 (via WAGO connector) |

⚠️ The 12V circuit is electrically isolated from the ESP32 — do not connect the 12V ground to the ESP32 ground.

---

## Setup

### 1. Install MicroPython on the ESP32

1. Download and install [Thonny IDE](https://thonny.org)
2. Plug in your ESP32 via USB
3. In Thonny: **Run → Configure interpreter → MicroPython (ESP32)**
4. Click **Install or update MicroPython**
5. Select variant: **Espressif ESP32 / WROOM**, version **1.28.0**
6. Hit **Install** and wait ~30 seconds
7. You should see `>>>` in the Thonny shell when done

### 2. Configure the script

Open `main.py` and adjust these settings at the top if needed:

```python
MAX_RUN_S = 30   # max pump runtime in seconds -- set to ~2x a normal fill time
SENSOR_WET = 1   # 1 = sensor reads high when wet (confirmed for CQRobot optical)
```

### 3. Flash to the ESP32

1. In Thonny: **File → Save as → MicroPython device**
2. Name it exactly `main.py`
3. Hit OK

The ESP32 will now run the script automatically every time it powers up — no laptop needed.

---

## Usage

1. Fill a water jug and run the pump's inlet tube into it
2. Run the outlet tube into the Chili device's fill port
3. Submerge the sensor probe in the Chili reservoir
4. Plug the ESP32 into any USB power source
5. Plug the 12V adapter into the wall

The system checks the level immediately on power-up, pumps if needed, then sleeps 24 hours. Plug it in each morning at the time you want the daily refill to happen.

---

## Troubleshooting

**Sensor always reads the same value**
- Check the 3V/5V selector switch on the sensor — it must match your power pin
- Make sure the signal wire is on P23, not the adjacent GND pin

**Relay doesn't click**
- Confirm DC+ is on the ESP32's 5V/VIN pin, not 3.3V — the relay coil needs 5V
- Check the high/low trigger jumper on the relay board

**Pump runs backwards**
- Swap the two pump terminal wires — peristaltic pumps are reversible

**Pump runs but no water moves**
- Make sure the inlet tube is submerged in the water source
- Check for kinks in the tubing

---

## 3D Printed Parts

The file `chilisleep_cap_v2.stl` is a replacement cap for the Chili Sleep reservoir fill port — useful if your original cap is lost or damaged. It's a 133.5 × 133.5mm footprint, 5mm tall. Print in PLA or PETG with standard settings.

---

## License

MIT — do whatever you want with it.
