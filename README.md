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
        - Fresh Air Intake with damper: <- indoor air
        - Reactivation air outlet: -> outdoor air
    - Chamber HVAC: 
        - HVACTemplate:Zone:PTAC
        - gc temperature sp
        - Outdoor Air Method - DetailedSpecification - dsoa
        - Heating Coil Type - Electric - 2 kW
        - lights: 1.07E+01 W/m2
        - Living Wall
            - PM method
            - DaylightControl1-1 ✅
            - Total leaf area (m2): 20 ✅
            - LED nominal intensity (umol/m2/s): 32.5 ✅
            - LED nominal power (W): 640 ✅
            - Outputs:Evaporatranspiration rate (kg/s) ✅
    - Chamber Outside boundary condition: Adiabatic (No heat transfer, but store heat in the thermal mass)
    - Room HVAC: None

2. Debugging
    - outdoor air might be in fact indoor air within SI building，which means DesignSpecification:OutdoorAir should be removed.
    - SI building growth chamber access
    - lights: LED from spec to E+
    - Change HVAC from PTAC to FanCoil (electricity power etc.)
        - CX9041-WATER COOLED DX CONDENSING UNIT WITH HOT GAS SYSTEM FOR CONTINUOUS COMPRESSOR OPERATION AND TIGHT TEMPERATURE CONTROL
            - ElectricCentrifugalChiller
            - ❓NominalCOP (W/W): 3.2
        - ❓CX9041-ASSY-AIR HANDLER UNIT, MT, DX COILS, 2X1000W HEATERS, 60HZ
    - No Differences:
        - Dehumidifier:Desiccant:NoFans
        - Humidifier:Steam:Electric


3. copy and paste

Lights,
    led lights,              !- Name
    Thermal Zone 1,          !- Zone or ZoneList or Space or SpaceList Name
    Always On Continuous,    !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    10.6562713125426,        !- Watts per Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    ,                        !- Return Air Fraction
    ,                        !- Fraction Radiant
    ,                        !- Fraction Visible
    ;                        !- Fraction Replaceable

IndoorLivingWall,
    gc living wall,          !- Name
    Floor,                   !- Surface Name
    Always On Discrete,      !- Schedule Name
    Penman-Monteith,         !- Evapotranspiration Calculation Method
    LED,                     !- Lighting Method
    Always On Continuous,    !- LED Intensity Schedule Name
    DaylightControl1-1,      !- Daylighting Control Name
    ,                        !- LED-Daylight Targeted Lighting Intensity Schedule Name
    200,                     !- Total Leaf Area {m2}
    65,                      !- LED Nominal Intensity {umol/m2-s}
    1280,                    !- LED Nominal Power {W}
    0.6;                     !- Radiant Fraction of LED Lights



HVACTemplate:Zone:PTAC,
    Thermal Zone 1,          !- Zone Name
    gc temperature sp,       !- Template Thermostat Name
    autosize,                !- Cooling Supply Air Flow Rate {m3/s}
    autosize,                !- Heating Supply Air Flow Rate {m3/s}
    ,                        !- No Load Supply Air Flow Rate {m3/s}
    ,                        !- Zone Heating Sizing Factor
    ,                        !- Zone Cooling Sizing Factor
    DetailedSpecification,   !- Outdoor Air Method
    ,                        !- Outdoor Air Flow Rate per Person {m3/s}
    ,                        !- Outdoor Air Flow Rate per Zone Floor Area {m3/s-m2}
    0,                       !- Outdoor Air Flow Rate per Zone {m3/s}
    ,                        !- System Availability Schedule Name
    ,                        !- Supply Fan Operating Mode Schedule Name
    DrawThrough,             !- Supply Fan Placement
    0.7,                     !- Supply Fan Total Efficiency
    75,                      !- Supply Fan Delta Pressure {Pa}
    0.9,                     !- Supply Fan Motor Efficiency
    SingleSpeedDX,           !- Cooling Coil Type
    ,                        !- Cooling Coil Availability Schedule Name
    autosize,                !- Cooling Coil Gross Rated Total Capacity {W}
    autosize,                !- Cooling Coil Gross Rated Sensible Heat Ratio
    3,                       !- Cooling Coil Gross Rated Cooling COP {W/W}
    Electric,                !- Heating Coil Type
    ,                        !- Heating Coil Availability Schedule Name
    2000,                    !- Heating Coil Capacity {W}
    0.8,                     !- Gas Heating Coil Efficiency
    ,                        !- Gas Heating Coil Parasitic Electric Load {W}
    ,                        !- Dedicated Outdoor Air System Name
    SupplyAirTemperature,    !- Zone Cooling Design Supply Air Temperature Input Method
    14,                      !- Zone Cooling Design Supply Air Temperature {C}
    11.11,                   !- Zone Cooling Design Supply Air Temperature Difference {deltaC}
    SupplyAirTemperature,    !- Zone Heating Design Supply Air Temperature Input Method
    50,                      !- Zone Heating Design Supply Air Temperature {C}
    30,                      !- Zone Heating Design Supply Air Temperature Difference {deltaC}
    dsoa,                    !- Design Specification Outdoor Air Object Name
    ,                        !- Design Specification Zone Air Distribution Object Name
    None,                    !- Baseboard Heating Type
    ,                        !- Baseboard Heating Availability Schedule Name
    autosize,                !- Baseboard Heating Capacity {W}
    None;                    !- Capacity Control Method


Dehumidifier:Desiccant:NoFans,
    drier,                   !- Name
    ,                        !- Availability Schedule Name
    Model Outdoor Air Node,  !- Process Air Inlet Node Name
    humidifier outlet,       !- Process Air Outlet Node Name
    Regen Coil Out Node,     !- Regeneration Air Inlet Node Name
    Model Outdoor Air Node,  !- Regeneration Fan Inlet Node Name
    LeavingMaximumHumidityRatioSetpoint,  !- Control Type
    0.007,                   !- Leaving Maximum Humidity Ratio Setpoint {kgWater/kgDryAir}
    1,                       !- Nominal Process Air Flow Rate {m3/s}
    2.5,                     !- Nominal Process Air Velocity {m/s}
    10,                      !- Rotor Power {W}
    Coil:Heating:Electric,   !- Regeneration Coil Object Type
    drier regen coil,        !- Regeneration Coil Name
    Fan:VariableVolume,      !- Regeneration Fan Object Type
    drier regen fan,         !- Regeneration Fan Name
    DEFAULT;                 !- Performance Model Type

Humidifier:Steam:Electric,
    humidifier,              !- Name
    ,                        !- Availability Schedule Name
    0.00000222,              !- Rated Capacity {m3/s}
    autosize,                !- Rated Power {W}
    ,                        !- Rated Fan Power {W}
    ,                        !- Standby Power {W}
    humidifier air inlet,    !- Air Inlet Node Name
    humidifier outlet;       !- Air Outlet Node Name

DesignSpecification:OutdoorAir,
    dsoa,                    !- Name
    Flow/Zone,               !- Outdoor Air Method
    ,                        !- Outdoor Air Flow per Person {m3/s-person}
    ,                        !- Outdoor Air Flow per Zone Floor Area {m3/s-m2}
    0.047;                   !- Outdoor Air Flow per Zone {m3/s}

ZoneControl:Humidistat,
    humidity sp,             !- Name
    Thermal Zone 1,          !- Zone Name
    humidifying Relative Humidity Sch,  !- Humidifying Relative Humidity Setpoint Schedule Name
    dehumidifying Relative Humidity Sch;  !- Dehumidifying Relative Humidity Setpoint Schedule Name

!-   ===========  ALL OBJECTS IN CLASS: FAN:VARIABLEVOLUME ===========

Fan:VariableVolume,
    drier regen fan,         !- Name
    ,                        !- Availability Schedule Name
    0.7,                     !- Fan Total Efficiency
    600.0,                   !- Pressure Rise {Pa}
    1.3,                     !- Maximum Flow Rate {m3/s}
    FixedFlowRate,           !- Fan Power Minimum Flow Rate Input Method
    ,                        !- Fan Power Minimum Flow Fraction
    0.0,                     !- Fan Power Minimum Air Flow Rate {m3/s}
    0.9,                     !- Motor Efficiency
    1.0,                     !- Motor In Airstream Fraction
    0,                       !- Fan Power Coefficient 1
    1,                       !- Fan Power Coefficient 2
    0,                       !- Fan Power Coefficient 3
    0,                       !- Fan Power Coefficient 4
    0,                       !- Fan Power Coefficient 5
    Model Outdoor Air Node,  !- Air Inlet Node Name
    Regen Coil Inlet Node;   !- Air Outlet Node Name


!-   ===========  ALL OBJECTS IN CLASS: COIL:HEATING:ELECTRIC ===========

Coil:Heating:Electric,
    drier regen coil,        !- Name
    ,                        !- Availability Schedule Name
    1,                       !- Efficiency
    1200.0,                  !- Nominal Capacity {W}
    Regen Coil Inlet Node,   !- Air Inlet Node Name
    Regen Coil Out Node;     !- Air Outlet Node Name


4. Upgraded model (chamber within a room):
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