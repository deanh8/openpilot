#!/usr/bin/env python3
import datetime
import os
import signal
import subprocess
import sys
import traceback

import cereal.messaging as messaging
import selfdrive.crash as crash
from common.basedir import BASEDIR
from common.params import Params, ParamKeyType
from common.text_window import TextWindow
from selfdrive.boardd.set_time import set_time
from selfdrive.hardware import HARDWARE, PC
from selfdrive.manager.helpers import unblock_stdout
from selfdrive.manager.process import ensure_running
from selfdrive.manager.process_config import managed_processes
from selfdrive.athena.registration import register, UNREGISTERED_DONGLE_ID
from selfdrive.swaglog import cloudlog, add_file_handler
from selfdrive.version import dirty, get_git_commit, version, origin, branch, commit, \
                              terms_version, training_version, comma_remote, \
                              get_git_branch, get_git_remote

sys.path.append(os.path.join(BASEDIR, "pyextra"))

def manager_init():

  # update system time from panda
  set_time(cloudlog)

  params = Params()
  params.clear_all(ParamKeyType.CLEAR_ON_MANAGER_START)

  default_params = [
    ("CompletedTrainingVersion", "0"),
    ("HasAcceptedTerms", "0"),
    ("HandsOnWheelMonitoring", "0"),
    ("OpenpilotEnabledToggle", "1"),
    ("ShowDebugUI", "1"),
    ("SpeedLimitControl", "1"),
    ("SpeedLimitPercOffset", "1"),
    ("TurnSpeedControl", "1"),
    ("TurnVisionControl", "1"),
    ("GMAutoHold", "1"),
    ("CruiseSpeedOffset", "1"),
    ("StockSpeedAdjust", "1"),
    ("CustomSounds", "0"),
    ("SilentEngageDisengage", "0"),
    ("ScreenDimMode", "2"),
    ("AccelModeButton", "0"),
    ("AccelMode", "0"),
    ("EndToEndToggle", "1"),
    ("LanelessMode", "2"),
    ("NudgelessLaneChange", "0"),
    ("Coasting", "0"),
    ("CoastingDL", "0"),
    ("RegenBraking", "0"),
    ("OnePedalMode", "0"),
    ("OnePedalModeSimple", "0"),
    ("OnePedalDLCoasting", "0"),
    ("OnePedalModeEngageOnGas", "0"),
    ("OnePedalDLEngageOnGas", "0"),
    ("OnePedalBrakeMode", "0"),
    ("OnePedalPauseBlinkerSteering", "1"),
    ("FollowLevel", "2"),
    ("DynamicFollow", "1"),
    ("DynamicFollowToggle", "0"),
    ("CoastingBrakeOverSpeed", "0"),
    ("FrictionBrakePercent", "0"),
    ("BrakeIndicator", "1"),
    ("DisableOnroadUploads", "0"),
    ("MeasureNumSlots", "0"),
    ("MeasureSlot00", "0"), # steering angle
    ("MeasureSlot01", "11"), # percent grade
    ("MeasureSlot02", "10"), # altitude
    ("MeasureSlot03", "5"), # engine rpm + coolant temp °F
    ("MeasureSlot04", "13"), # follow gap level
    ("MeasureSlot05", "16"), # lead dist [s]
    ("MeasureSlot06", "15"), # lead dist [m]
    ("MeasureSlot07", "20"), # lead rel spd [mph]
    ("MeasureSlot08", "21"),# lead spd [mph]
    ("MeasureSlot09", "23"),# device cpu percent and temp °F
  ]
  if not PC:
    default_params.append(("LastUpdateTime", datetime.datetime.utcnow().isoformat().encode('utf8')))

  if params.get_bool("RecordFrontLock"):
    params.put_bool("RecordFront", True)

  # set unset params
  for k, v in default_params:
    if params.get(k) is None:
      params.put(k, v)

  # parameters set by Enviroment Varables
  if os.getenv("HANDSMONITORING") is not None:
    params.put_bool("HandsOnWheelMonitoring", bool(int(os.getenv("HANDSMONITORING"))))

  # is this dashcam?
  if os.getenv("PASSIVE") is not None:
    params.put_bool("Passive", bool(int(os.getenv("PASSIVE"))))

  if params.get("Passive") is None:
    raise Exception("Passive must be set to continue")

  # Create folders needed for msgq
  try:
    os.mkdir("/dev/shm")
  except FileExistsError:
    pass
  except PermissionError:
    print("WARNING: failed to make /dev/shm")

  # set version params
  params.put("Version", version)
  params.put("TermsVersion", terms_version)
  params.put("TrainingVersion", training_version)
  params.put("GitCommit", get_git_commit(default=""))
  params.put("GitBranch", get_git_branch(default=""))
  params.put("GitRemote", get_git_remote(default=""))

  # set dongle id
  reg_res = register(show_spinner=True)
  if reg_res:
    dongle_id = reg_res
  else:
    serial = params.get("HardwareSerial")
    raise Exception(f"Registration failed for device {serial}")
  os.environ['DONGLE_ID'] = dongle_id  # Needed for swaglog

  if not dirty:
    os.environ['CLEAN'] = '1'

  cloudlog.bind_global(dongle_id=dongle_id, version=version, dirty=dirty,
                       device=HARDWARE.get_device_type())

  if comma_remote and not (os.getenv("NOLOG") or os.getenv("NOCRASH") or PC):
    crash.init()
  crash.bind_user(id=dongle_id)
  crash.bind_extra(dirty=dirty, origin=origin, branch=branch, commit=commit,
                   device=HARDWARE.get_device_type())


def manager_prepare():
  for p in managed_processes.values():
    p.prepare()


def manager_cleanup():
  for p in managed_processes.values():
    p.stop()

  cloudlog.info("everything is dead")


def manager_thread():
  cloudlog.info("manager start")
  cloudlog.info({"environ": os.environ})

  # save boot log
  subprocess.call("./bootlog", cwd=os.path.join(BASEDIR, "selfdrive/loggerd"))

  params = Params()

  ignore = []
  if params.get("DongleId", encoding='utf8') == UNREGISTERED_DONGLE_ID:
    ignore += ["manage_athenad", "uploader"]
  if os.getenv("NOBOARD") is not None:
    ignore.append("pandad")
  if os.getenv("BLOCK") is not None:
    ignore += os.getenv("BLOCK").split(",")

  ensure_running(managed_processes.values(), started=False, not_run=ignore)

  started_prev = False
  sm = messaging.SubMaster(['deviceState'])
  pm = messaging.PubMaster(['managerState'])

  while True:
    sm.update()
    not_run = ignore[:]

    if sm['deviceState'].freeSpacePercent < 5:
      not_run.append("loggerd")

    started = sm['deviceState'].started
    driverview = params.get_bool("IsDriverViewEnabled")
    ensure_running(managed_processes.values(), started, driverview, not_run)

    # trigger an update after going offroad
    if started_prev and not started and 'updated' in managed_processes:
      os.sync()
      managed_processes['updated'].signal(signal.SIGHUP)

    started_prev = started

    running_list = ["%s%s\u001b[0m" % ("\u001b[32m" if p.proc.is_alive() else "\u001b[31m", p.name)
                    for p in managed_processes.values() if p.proc]
    cloudlog.debug(' '.join(running_list))

    # send managerState
    msg = messaging.new_message('managerState')
    msg.managerState.processes = [p.get_process_state_msg() for p in managed_processes.values()]
    pm.send('managerState', msg)

    # TODO: let UI handle this
    # Exit main loop when uninstall is needed
    if params.get_bool("DoUninstall"):
      break


def main():
  prepare_only = os.getenv("PREPAREONLY") is not None

  manager_init()

  # Start UI early so prepare can happen in the background
  if not prepare_only:
    managed_processes['ui'].start()

  manager_prepare()

  if prepare_only:
    return

  # SystemExit on sigterm
  signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(1))

  try:
    manager_thread()
  except Exception:
    traceback.print_exc()
    crash.capture_exception()
  finally:
    manager_cleanup()

  if Params().get_bool("DoUninstall"):
    cloudlog.warning("uninstalling")
    HARDWARE.uninstall()


if __name__ == "__main__":
  unblock_stdout()

  try:
    main()
  except Exception:
    add_file_handler(cloudlog)
    cloudlog.exception("Manager failed to start")

    # Show last 3 lines of traceback
    error = traceback.format_exc(-3)
    error = "Manager failed to start\n\n" + error
    with TextWindow(error) as t:
      t.wait_for_exit()

    raise

  # manual exit because we are forked
  sys.exit(0)
