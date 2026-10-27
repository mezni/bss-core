---
document_id: RB-BB-001
title: Broadband No Connectivity
document_type: troubleshooting_runbook
domain: broadband_troubleshooting
version: "1.0"
status: active
access_level: internal
source_type: synthetic
---

# Broadband No Connectivity

## Symptoms

The customer cannot access the internet through the
residential or business gateway.

## Diagnostic procedure

1. Confirm whether the issue affects one device or all devices.
2. Verify that the gateway has power.
3. Check the gateway WAN status.
4. Verify the ONT status when fiber access is used.
5. Check for an active service outage using an authorized
   operational system.
6. Record diagnostic results before escalation.

## Decision guidance

- If one device is affected, investigate that device and
  its local network connection.
- If all devices are affected, continue with gateway and
  access-network diagnostics.
- If optical loss is reported, follow RB-OPT-001.
- If a confirmed network outage exists, follow the
  applicable outage-handling procedure.

## Escalation

Escalate unresolved issues through the approved support
process. Do not claim that service has been restored
without verification.
