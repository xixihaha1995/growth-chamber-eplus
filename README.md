### To delete

1. People
2. Electric Equipment

### To modify

1. Outside boundary condition
    - Outdoors -> Adiabatic

### To upgrade

1. Current Model (simple isolated chamber):
    - gc temperature sp: 15 to 35 °C
    - Humidistat: 67% to 73% RH
    - dsoa: Flow/Zone, 100 CFM -> 0.047 m3/s
    - Geometry: Chamber
    - Material: 
        - https://www.betterhomesbc.ca/products/what-is-r-or-rsi-value/
        - Material:NoMass (R24 ft2*h*F/Btu - RSI 4.2 m2*K/W)
    - Spray nozzle: 
        - Humidifier:Steam:Electric
        - 8.1 liters/hour -> 0.00000222 m3/s
    - Chemical drier unit:
        - Regeneration Coil:Heating:Electric, 1200 W
        - Regeneration Fan:VariableVolume, 600 Pressure Rise, 1.3 Maximum Flow Rat, 0,7 Fan Total Efficiency
    - Chamber HVAC: 
        - HVACTemplate:Zone:PTAC
        - gc temperature sp
        - Outdoor Air Method - DetailedSpecification - dsoa
        - Heating Coil Type - Electric - 2 kW
        - lights: 1.07E+01 W/m2
        - Living Wall
            - PM method
            - Total leaf area (m2): 20
            - LED nominal intensity (umol/m2/s): 32.5
            - LED nominal power (W): 640
    - Chamber Outside boundary condition: Adiabatic (No heat transfer, but store heat in the thermal mass)
    - Room HVAC: None

2. Upgraded model (chamber within a room):
    - Geometry: Chamber, Room
    - Material: for chamber and room
    - Chamber HVAC: 
        - internal and external heat gain between chamber and room
        - air intake is room air or outdoor air
    - Chamber outside boundary condition: Surface
    - Room HVAC:
        - real rooftop unit
        - air exchange, waste heat from chamber
    - Calibration
        - Chamber inside and outside temperatures (HOBO sensors, secondly/minutely data, 1 week)
        - Energy consumption (electricity measured by meters, secondly/minutely data, 1 week)
            - three-phase meter: https://a.co/d/8dgtneY
            - single-phase meter: https://www.ebay.com/itm/176450277332?mkcid=16&mkevt=1&mkrid=711-127632-2357-0&ssspo=mq44qhk8r1q&sssrc=2047675&ssuid=&var=476016459298&widget_ver=artemis&media=COPY

### visualization-eplusr

```R
#View IDF 
setwd("C:\\Users\\wulic\\Documents\\GitHub\\growth-chamber-eplus")
getwd()
install.packages("eplusr") #No, or Yes
library("eplusr")
avail_eplus()
#[1] ‘9.2.0’  ‘9.6.0’  ‘22.1.0’
use_eplus("C:/EnergyPlusV24-1-0")
path_idf <- file.path("growthChamber.idf")
idf <- read_idf(path_idf)
geom <- idf$geometry()
viewer <- geom$view()
viewer$background("grey50")
viewer$render_by("zone")
viewer$show(zone = "Thermal Zone: Compartment 3 Thermal Zone")
```