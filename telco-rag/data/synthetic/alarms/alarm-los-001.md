---
document_id: ALARM-LOS-001
title: Loss of Signal Alarm
document_type: network_alarm
domain: access_network
alarm_code: LOS
severity: major
version: "1.0"
status: active
access_level: internal
source_type: synthetic
---

# Loss of Signal (LOS)

## Description

The fictional LOS alarm indicates that the monitored
interface is not receiving the expected optical signal.

## Severity

Major. The affected service may be unavailable.

## Potential impact

- Customer broadband connectivity loss.
- Multiple affected services if the fault is shared.
- Service degradation or interruption.

## Recommended response

1. Confirm the alarm source and timestamp.
2. Identify the affected interface and associated services.
3. Check for correlated alarms and network outages.
4. Follow RB-OPT-001.
5. Escalate according to the applicable operational policy.

## Related documents

- RB-OPT-001: Optical Signal Loss Troubleshooting
- RB-BB-001: Broadband No Connectivity
