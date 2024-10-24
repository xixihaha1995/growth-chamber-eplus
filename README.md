### To delete

1. People
2. Electric Equipment

### To modify

1. Outside boundary condition
    - Outdoors -> Adiabatic

### To upgrade

1. Current Model (simple isolated chamber):
    - Geometry: Chamber
    - Material: None or default
    - Chamber HVAC: 
        - Ideal Loads Air System (thermostat name, Humidistat)
        - only internal heat gain
        - air intake is room air or outdoor air
        - lights: 1.07E+01 W/m2
        - Living Wall
            - PM method
            - Total leaf area (m2): 30
            - LED nominal intensity (umol/m2/s): 32.5
            - LED nominal power (W): 640
    - Chamber Outside boundary condition: Adiabatic (No heat transfer, but store heat in the thermal mass)
    - Room HVAC: None

2. Upgraded model (chamber within a room):
    - Geometry: Chamber, Room
    - Material: for chamber and room
    - Chamber HVAC: 
        - real package unit
        - internal and external heat gain between chamber and room
        - air intake is room air or outdoor air
    - Chamber outside boundary condition: Surface
    - Room HVAC:
        - real rooftop unit
        - air exchange, waste heat from chamber

3. Calibration
    - Chamber inside and outside temperatures
    - Energy consumption (electricity)




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