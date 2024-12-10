### To upgrade

1. Current Model (simple isolated chamber):
    - Chamber Outside boundary condition: Adiabatic, NoSun, NoWind (No heat transfer, but store heat in the thermal mass)
    - no people, no electric equipment
    - gc temperature sp: 20 °C， -+ 0.5 °C
    - Humidistat: 72% to 78% RH
    - dsoa: Flow/Zone, 100 CFM -> 0.047 m3/s, -> 0 m3/s
    - Geometry: Chamber
    - Material: 
        - https://www.betterhomesbc.ca/products/what-is-r-or-rsi-value/
        - Material:NoMass (R24 ft2*h*F/Btu - RSI 4.2 m2*K/W)
    - Spray nozzle (❌): 
        - Humidifier:Steam:Electric
        - 8.1 liters/hour -> 0.00000222 m3/s
    - Chemical drier unit (❌):
        - Regeneration Coil:Heating:Electric, 1200 W
        - Regeneration Fan:VariableVolume, 600 Pressure Rise, 1.3 Maximum Flow Rat, 0,7 Fan Total Efficiency
        - Fresh Air Intake with damper: <- indoor air
        - Reactivation air outlet: -> outdoor air
    - Chamber HVAC: 
        - HVACTemplate:Zone:PTAC
        - gc temperature sp
        - Outdoor Air Method - zero
        - Heating Coil Type - Electric - 2 kW
        - lights: 
            - living wall lights (second tier)
            - normal lights (third and top tiers)
        - Living Wall
            - PM method
            - DaylightControl1-1 ✅
            - Outputs:Evaporatranspiration rate (kg/s) ✅
    - Room HVAC: None

2. 11/12/2024 Upgraded
    - outdoor air might be in fact indoor air within SI building，which means DesignSpecification:OutdoorAir should be zero.
    - Areas:
        - Building area: 11.43 m2
        - **Experimental area**: 1.5 m2
        - Leaf area: 0.158 m2 per stem * 72 stems = 11.376 m2 @ 300 PPFD, 0.256 m2 per stem * 72 stems = 18.432 m2 @ 600 PPFD
    - lights: 
        - LED Specs
            - https://fluence-led.com/products/ray-series/, Photon Flux (360-780 nm), Fluence Ray44 LED, Pfr (Pfr stands for a far red absorbing form, https://fluence-led.com/science-articles/guide-to-photo-morphogenesis/). Others: 84 W for one bar electricial specifications from https://fluence-led.com/wp-content/uploads/2019/11/70334C-RAY-Series-User-Manual-1812-1.pdf.
            - 162 umol/s, 65 W (277 V AC power), 2.49 umol/J
        - LivingWall-Lights (one module, in total 4 modules):
            - Second Tier, 4 Fluence LED Modules, each module is: 
            - Total leaf area: 0.158 m2 per stem * 72 stems = 11.376 m2 @ 300 PPFD, 11.376 m2  * 4 modules = 45.504 m2
            - PPFD: 4 bars * 162 umol/s / 1.5 m2 = 432 umol/m2/s (PPFD)
            - LED Nominal Power: 4 bars * 65 W/bar = 260 W, 260 W * 4 modules = 1040 W
        - Normal Lights without living walls:
            - Top tier: 2080 W
            - Third tier: 1040 W
        - LivingWall: LED = 0, PPFD works well the LED intensity schedule (ET process)
        - Normal lights = 780 W (with on12off12)
3. debugging
    - Questions:
    - Humidity control debugging:
        - Dehumidifier:Desiccant:NoFans
        - Humidifier:Steam:Electric
    - Convert PPFD to LED interior lighting power consumption.


3. copy and paste

Lights,
    led lights,              !- Name
    Thermal Zone 1,          !- Zone or ZoneList or Space or SpaceList Name
    Always On Continuous,    !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    224,        !- Watts per Floor Area {W/m2}
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


  SetpointManager:SingleZone:Humidity:Maximum,
    dehumidifying manager,  !- Name
    Mixed Air Node,          !- Setpoint Node or NodeList Name
    Zone 2 Node;             !- Control Zone Air Node Name

  SetpointManager:SingleZone:Humidity:Minimum,
    humidifying manager,  !- Name
    Air Loop Outlet Node,    !- Setpoint Node or NodeList Name
    Zone 2 Node;             !- Control Zone Air Node Name

  ZoneHVAC:EquipmentConnections,
    EAST ZONE,               !- Zone Name
    Zone2Equipment,          !- Zone Conditioning Equipment List Name
    Zone2Inlets,             !- Zone Air Inlet Node or NodeList Name
    ,                        !- Zone Air Exhaust Node or NodeList Name
    Zone 2 Node,             !- Zone Air Node Name
    Zone 2 Outlet Node;      !- Zone Return Air Node or NodeList Name


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

HVACTemplate:Zone:IdealLoadsAirSystem,
    Thermal Zone 1,          !- Zone Name
    gc temperature sp,       !- Template Thermostat Name
    ,                        !- System Availability Schedule Name
    50,                      !- Maximum Heating Supply Air Temperature {C}
    13,                      !- Minimum Cooling Supply Air Temperature {C}
    0.0156,                  !- Maximum Heating Supply Air Humidity Ratio {kgWater/kgDryAir}
    0.0077,                  !- Minimum Cooling Supply Air Humidity Ratio {kgWater/kgDryAir}
    NoLimit,                 !- Heating Limit
    ,                        !- Maximum Heating Air Flow Rate {m3/s}
    ,                        !- Maximum Sensible Heating Capacity {W}
    NoLimit,                 !- Cooling Limit
    ,                        !- Maximum Cooling Air Flow Rate {m3/s}
    ,                        !- Maximum Total Cooling Capacity {W}
    ,                        !- Heating Availability Schedule Name
    ,                        !- Cooling Availability Schedule Name
    Humidistat,              !- Dehumidification Control Type
    0.7,                     !- Cooling Sensible Heat Ratio {dimensionless}
    78,                      !- Dehumidification Setpoint {percent}
    Humidistat,              !- Humidification Control Type
    72,                      !- Humidification Setpoint {percent}
    None,                    !- Outdoor Air Method
    ,                 !- Outdoor Air Flow Rate per Person {m3/s}
    ,                        !- Outdoor Air Flow Rate per Zone Floor Area {m3/s-m2}
    ,                        !- Outdoor Air Flow Rate per Zone {m3/s}
    ,                        !- Design Specification Outdoor Air Object Name
    None,                    !- Demand Controlled Ventilation Type
    NoEconomizer,            !- Outdoor Air Economizer Type
    None,                    !- Heat Recovery Type
    0.7,                     !- Sensible Heat Recovery Effectiveness {dimensionless}
    0.65;                    !- Latent Heat Recovery Effectiveness {dimensionless}


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