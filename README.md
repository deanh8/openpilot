![](https://user-images.githubusercontent.com/37757984/127420744-89ca219c-8f8e-46d3-bccf-c1cb53b81bb1.png)

### Appreciate my work? 
------

**[Buy me a beer/coffee](https://www.patreon.com/twilsonco)***

# Fork description
------

This fork exists to improve OP performance and convenience for GM cars, specifically the Chevy Volt, because the kegman fork wouldn't run on Comma Three.
The basic plan is to import all the features Volt OP users (on Discord) desire.

Running on move-fast fork of openpilot, which adds:

* Vision and/or map-based slowing down for curves
* Map-based automatic changing of speed limit (with optional offset)
* Hands on wheel monitoring
* Disable disengage when gas pressed

#### Current fork features [✅ = optional via toggle]:
-----

- [x] [Chevy Volt] Sigmoidal steering response (thanks Qadmus)
- [x] [GM] [✅] AutoHold (autohold brakes when stopped; ported from kegman)
- [x] [GM] Adjustable follow "mode" using ACC distance button (ported from kegman, but smoother follow profiles)
- [x] [GM] Toggle steering with LKAS button (wheel color changes to indicate disengagement)
- [x] [GM] One-pedal driving: using regen (volt) and/or light/moderate/heavy braking, control OP all the way to a stop, without a lead, and without disengaging, with just the gas pedal (see below)
- [x] [✅] [Dynamic Lane Profile](https://github.com/sunnyhaibin/openpilot#new-dynamic-lane-profile-dlp) (DLP); *tap button while driving to switch between auto/laneless/lane-only. must enable "Disable use of lanelines" for button to appear* (ported from sunnyhaibin)
- [x] [✅] Normal/sport acceleration modes with improved acceleration/braking profiles (ported from kegman)
- [x] [✅] 1/5 mph changes for tap/hold of the inc/dec buttons (ported from Spector56)
- [x] [✅] 3mph cruise speed offset: speed will be 23/28/33/38/etc.
- [x] [✅] Alternate sound effect set
- [x] [✅] Mute engage and disengage sounds
- [x] [✅] Downhill (max-regen) coasting: OP will still brake behind a lead car and to slow down for curves, but friction brakes won't be used in order to keep the set speed (by user or map speed limit)
- [x] [✅] Brake when 10mph+ over set speed when downhill coasting enabled
- [x] [✅] Nudgeless lane change: OP will start lane change automatically in direction of blinker after blinker on for 3s
- [x] [✅] Friction braking indicator
- [x] **Customizable, dynamic vehicle/device metrics**
    * To use:
        * Tap the current speed on the openpilot display to cycle the number of metrics
        * Tap any metric to cycle its content (sorry for all the god-forsaken tapping, a better metric display with vehicle, following, position, and device widgets is a WIP)
    * Metrics (24 to choose from):
        * Device info: CPU temperature, CPU percent, CPU temp + percent, memory temperature, memory used, free storage, ambient temperature, fanspeed (as percent of max), GPS accuracy (and number of satelites), altitude
        * Vehicle info: Engine RPM, steering torque, steering angle, desired steering angle, vehicle acceleration, vehicle jerk, percent grade of current road
        * Lead-following info: lead distance [length], desired lead distance [length], lead distance [time], desired lead distance [time], follow distance cost [in units of the stock OP distance cost; i.e. 2.5 meand 2.5× the stock OP value], relative lead velocity, absolute lead velocity
- [x] [GM] **"Auto-on steering lite"**: You control accel/decel with gas pedal in "L-mode" and OP keeps steering (down to 7mph)
    * To use:
    1. Enable the following toggles: Disable disengage on gas, Downhill coasting
    2. Put your volt in "L-mode"
    3. Engage OP and set the cruise speed to 1 (with or without gas pedal pressed)
    4. Now drive around; OP will steer while you control accel/decel with the gas pedal with the Volt's regen in "L-mode"
    * OP will pause steering if <30mph and blinker is on while in this mode
        * won't pause steering for low speed blinker if a) both toggles in (1) are disabled, or b) cruise set speed >10mph and the gas pedal isn't pressed (i.e. under normal OP control)
- [x] [GM] [✅] **One-pedal driving**: When in "auto-on steering lite" mode (i.e. with cruise speed set to 1), OP will apply light to heavy braking when you let completely off the gas, allowing you to come to a full stop and resume without OP disengaging
    * When in one-pedal mode, the max speed indicator in openpilot will be replaced with a one-pedal mode indicator. Tap the one-pedal icon (or use follow distance button, see below) to toggle coasting/braking
    * Vehicle follow distance indicator and pedal icon color indicate the one-pedal braking profile in use; 1/2/3 = 🟢/🟠/🔴 = light/moderate/heavy braking
    * Follow distance button:
      * Press: cycle between persistent light or moderate braking
      * Hold: apply temporary hard braking (indicated by follow level 3 on vehicle cluster and red one-pedal icon) (Chevy's the ones that decided a brake paddle on the steering wheel was a good idea; not me)
      * Press when coasting: activating braking
      * Double-press when gas is press and braking is active: deactivate braking (you'll get used to it...)
- [x] [GM] [✅] One-pedal pro braking: Completely disable cruise/speed limit/curve/follow braking when in one-pedal mode. You are soley responsible for slowing the car using the adjustable one-pedal braking (by pressing/holding the follow distance button) or with the physical brakes/regen paddle
- [x] [GM] [✅] One-pedal/always-on-steering engage on gas: When cruising at speed and the driver presses the gas (i.e. not when resuming from a stop), engage one-pedal/always-on-steering mode
    * Increase or reset speed to return to normal cruise.
- [x] [GM] JShuler panda-based GM steering fault fix
- [x] Remember last follow mode

#### Planned fork features (in no particular order):
-----

- [ ] Stop-and-go for 2018 Volt
- [ ] Grey panda support
- [ ] Chevy Bolt support
- [ ] Record screen button
- [ ] Redo UI metrics as themed "widgets" instead that can be activated independently and stack against the right (and left if necessary) side of the screen
  * Follow widget: a colored vertical bar indicating follow distance with lines indicating the actual and desired (length/time) follow distances. Tap to include more info items like current distance cost
  * Openpilot widget: a similar vertical bar (or maybe something like a circular progress bar or a speedometer--looking thing) showing the gas/braking being requested by OP. Also include Driver monitoring info.
  * Car widget: Acceleration/jerk, tire pressures, low voltage battery info, ...
  * Geo widget: GPS signal/coords/#satellites, altitude, percent grade of current road, ...
  * Device widget: CPU/memory/temps/fans/...
  * EV widget: high voltage battery info similar to that shown in the LeafSpyPro app
- [ ] [✅] [Modified assistive driving system](https://github.com/sunnyhaibin/openpilot#new-modified-assistive-driving-safety-mads) (MADS)
- [ ] [✅] 0.5 second delay before activating newly selected follow mode so user can switch around without OP slightly jerking in response
- [ ] [✅] Auto screen brightness (or at least a way to dim a bit at night)
- [ ] [✅] Lane Speed alerts ([sshane](https://github.com/sshane/openpilot#lane-speed-alerts))
- [ ] [✅] Dynamic camera offset (based on oncoming traffic) ([sshane)](https://github.com/sshane/openpilot#dynamic-camera-offset-based-on-oncoming-traffic)
- [ ] [Chevy Volt] Steering control below 7mph using parking commands
- [ ] [Chevy Volt] [✅] Road trip mode: automatically put car into Mountain Mode if sustained speed 55mph+
- [ ] [GM] Use physical drive mode button to switch between normal/sport acceleration profiles
- [ ] [GM] [✅] Dynamic follow mode: point-based
    * Follow distance "earns points" the longer you're behind the same lead car, moving from close to medium after about 5 minutes 
    * When on highway, continue to increase from medium to far follow distance after about 20 minutes behind the same car
    * If someone cuts in, the follow distance "takes a penalty" down to a closer follow distance proportional to the distance and relative speed of the car that cut in
    * The penalties can "go negative", that is, repeated cut-ins can result in close follow being use for longer than normal
* Metrics to add:
    - [ ] number of interventions/cut-ins during drive session
    - [ ] time since last intervention/cut-in
    - [ ] apply gas/apply brake

### Supported Hardware
------

This fork is developed and used on a Comma Three in a 2018 Chevy Volt, and is also *known* to work on Comma Two and Comma Zero, and in 2017 Volt and 2018 Acadia.

### Installation Instructions
------

#### Easy: using sshane's [openpilot-installer-generator](https://github.com/sshane/openpilot-installer-generator)

Use [these instructions](https://github.com/sshane/openpilot-installer-generator#usage) and the following url:
`https://smiskol.com/fork/twilsonco`

#### Less easy

With a stock installation of OpenPilot confirmed working, SSH into device and run the following:

`cd /data;mv openpilot openpilot_stock;git clone --recurse-submodules https://github.com/twilsonco/openpilot;sudo reboot`

### Automatic Updates
------

This fork will auto-update while your device has internet access, and changes are automatically applied the next time the device restarts.
If you're device stays connected to your car all the time, you'll be presented with a message to update when your car is off.

---

# What is openpilot?
------

[openpilot](http://github.com/commaai/openpilot) is an open source driver assistance system. Currently, openpilot performs the functions of Adaptive Cruise Control (ACC), Automated Lane Centering (ALC), Forward Collision Warning (FCW) and Lane Departure Warning (LDW) for a growing variety of supported [car makes, models and model years](#supported-cars). In addition, while openpilot is engaged, a camera based Driver Monitoring (DM) feature alerts distracted and asleep drivers.

<table>
  <tr>
    <td><a href="https://www.youtube.com/watch?v=mgAbfr42oI8" title="YouTube" rel="noopener"><img src="https://i.imgur.com/kAtT6Ei.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=394rJKeh76k" title="YouTube" rel="noopener"><img src="https://i.imgur.com/lTt8cS2.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=1iNOc3cq8cs" title="YouTube" rel="noopener"><img src="https://i.imgur.com/ANnuSpe.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=Vr6NgrB-zHw" title="YouTube" rel="noopener"><img src="https://i.imgur.com/Qypanuq.png"></a></td>
  </tr>
  <tr>
    <td><a href="https://www.youtube.com/watch?v=Ug41KIKF0oo" title="YouTube" rel="noopener"><img src="https://i.imgur.com/3caZ7xM.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=NVR_CdG1FRg" title="YouTube" rel="noopener"><img src="https://i.imgur.com/bAZOwql.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=tkEvIdzdfUE" title="YouTube" rel="noopener"><img src="https://i.imgur.com/EFINEzG.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=_P-N1ewNne4" title="YouTube" rel="noopener"><img src="https://i.imgur.com/gAyAq22.png"></a></td>
  </tr>
</table>



Limitations of openpilot ALC and LDW
------

openpilot ALC and openpilot LDW do not automatically drive the vehicle or reduce the amount of attention that must be paid to operate your vehicle. The driver must always keep control of the steering wheel and be ready to correct the openpilot ALC action at all times.

While changing lanes, openpilot is not capable of looking next to you or checking your blind spot. Only nudge the wheel to initiate a lane change after you have confirmed it's safe to do so.

Many factors can impact the performance of openpilot ALC and openpilot LDW, causing them to be unable to function as intended. These include, but are not limited to:

* Poor visibility (heavy rain, snow, fog, etc.) or weather conditions that may interfere with sensor operation.
* The road facing camera is obstructed, covered or damaged by mud, ice, snow, etc.
* Obstruction caused by applying excessive paint or adhesive products (such as wraps, stickers, rubber coating, etc.) onto the vehicle.
* The device is mounted incorrectly.
* When in sharp curves, like on-off ramps, intersections etc...; openpilot is designed to be limited in the amount of steering torque it can produce.
* In the presence of restricted lanes or construction zones.
* When driving on highly banked roads or in presence of strong cross-wind.
* Extremely hot or cold temperatures.
* Bright light (due to oncoming headlights, direct sunlight, etc.).
* Driving on hills, narrow, or winding roads.

The list above does not represent an exhaustive list of situations that may interfere with proper operation of openpilot components. It is the driver's responsibility to be in control of the vehicle at all times.

Limitations of openpilot ACC and FCW
------

openpilot ACC and openpilot FCW are not systems that allow careless or inattentive driving. It is still necessary for the driver to pay close attention to the vehicle’s surroundings and to be ready to re-take control of the gas and the brake at all times.

Many factors can impact the performance of openpilot ACC and openpilot FCW, causing them to be unable to function as intended. These include, but are not limited to:

* Poor visibility (heavy rain, snow, fog, etc.) or weather conditions that may interfere with sensor operation.
* The road facing camera or radar are obstructed, covered, or damaged by mud, ice, snow, etc.
* Obstruction caused by applying excessive paint or adhesive products (such as wraps, stickers, rubber coating, etc.) onto the vehicle.
* The device is mounted incorrectly.
* Approaching a toll booth, a bridge or a large metal plate.
* When driving on roads with pedestrians, cyclists, etc...
* In presence of traffic signs or stop lights, which are not detected by openpilot at this time.
* When the posted speed limit is below the user selected set speed. openpilot does not detect speed limits at this time.
* In presence of vehicles in the same lane that are not moving.
* When abrupt braking maneuvers are required. openpilot is designed to be limited in the amount of deceleration and acceleration that it can produce.
* When surrounding vehicles perform close cut-ins from neighbor lanes.
* Driving on hills, narrow, or winding roads.
* Extremely hot or cold temperatures.
* Bright light (due to oncoming headlights, direct sunlight, etc.).
* Interference from other equipment that generates radar waves.

The list above does not represent an exhaustive list of situations that may interfere with proper operation of openpilot components. It is the driver's responsibility to be in control of the vehicle at all times.

Limitations of openpilot DM
------

openpilot DM should not be considered an exact measurement of the alertness of the driver.

Many factors can impact the performance of openpilot DM, causing it to be unable to function as intended. These include, but are not limited to:

* Low light conditions, such as driving at night or in dark tunnels.
* Bright light (due to oncoming headlights, direct sunlight, etc.).
* The driver's face is partially or completely outside field of view of the driver facing camera.
* The driver facing camera is obstructed, covered, or damaged.

The list above does not represent an exhaustive list of situations that may interfere with proper operation of openpilot components. A driver should not rely on openpilot DM to assess their level of attention.


Licensing
------

openpilot and this fork are released under the MIT license. Some parts of the software are released under other licenses as specified.

Any user of this software shall indemnify and hold harmless comma.ai, Inc. and its directors, officers, employees, agents, stockholders, affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without limitation attorneys’ fees and costs) which arise out of, relate to or result from any use of this software by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT.
YOU ARE RESPONSIBLE FOR COMPLYING WITH LOCAL LAWS AND REGULATIONS.
NO WARRANTY EXPRESSED OR IMPLIED.**

---