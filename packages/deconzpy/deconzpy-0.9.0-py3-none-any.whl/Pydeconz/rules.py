#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def lookupAddress(adr):
    # print(adr)
    adr = adr.split("/")
    del adr[0]
    ret = ""
    if adr[0] == "sensors":
        ret += "/s/"
        try:
            sensor = next(x for x in sensors if x.getId() == adr[1])
            ret += (
                sensor.getIcon() + "-" + sensor.getName() + "-" + sensor.getId() + "/"
            )  # + sensor.getManufactur() + "-" + sensor.getId() + "/"
            ret += "/".join(adr[2:])
        except StopIteration:
            ret += "invalid-" + adr[1]
        return ret
    elif adr[0] == "groups":
        ret += "/g/"
        try:
            group = next(x for x in groups if x.getId() == adr[1])
            ret += (
                group.getName() + "-" + group.getId() + "/"
            )  # + sensor.getManufactur() + "-" + sensor.getId() + "/"
            ret += "/".join(adr[2:])
        except StopIteration:
            ret += "invalid-" + adr[1]
        return ret
    else:
        return "/".join(adr)


from .Router import Router

router = Router()

# getAllRules()
sensors = router.getAllSensors()
for s in sensors:
    s.println()
    s.dump()

print("---")

groups = router.getAllGroups()
for g in groups:
    g.println()

print("---")

rules = router.getAllRules()
for r in rules:
    r.println()

for g in groups:
    if g.getName() == "Alle Lichter":
        g.actionOff()


print("== Start == ")
# startAndRunWsThread()

# start websocket
# router.startAndRunThread("192.168.1.196")

# saveConfigIfExists()

# try:
#    input("Press enter to continue")
# except SyntaxError:
#    pass


# write it back to the file
# with open('config.json', 'w') as f:
#    json.dump(config, f)

# [{"success":{"username":"5ED4C6BC6A"}}]
