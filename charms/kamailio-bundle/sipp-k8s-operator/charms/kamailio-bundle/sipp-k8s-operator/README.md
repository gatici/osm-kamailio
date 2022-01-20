# sipp-k8s

## Description

Basic charm operator for SIPP.

## Usage

```shell
juju add-model test-kamailio
charmcraft pack
juju deploy ./sipp-k8s_ubuntu-20.04-amd64.charm --resource sipp-image=grigiu/sipp:latest
```

Deploy kamailio:

```shell
git clone https://github.com/davigar15/charm-kamailio
cd charm-kamailio/
charmcraft pack
juju deploy ./kamailio_ubuntu-20.04-amd64.charm  --resource kamailio-image=kamailio/kamailio:5.3.3-stretch
watch -c juju status --color
```

Test:

```shell
$ juju run-action sipp-k8s/0 options ip=10.1.245.121 port=5060 --wait
unit-sipp-k8s-0:
  UnitId: sipp-k8s/0
  id: "8"
  results:
    Stderr: "Resolving remote host '10.1.245.121'... Done.\n2022-01-20\t17:42:45.972900\t1642700565.972900:
      Dead call 5-22@10.1.245.107 (successful), received 'SIP/2.0 404 Not Found\nVia:
      SIP/2.0/UDP 10.1.245.107:5060;branch=z9hG4bK-22-5-0\nTo: <sip:30@10.1.245.121>;tag=a6a1c5f60faecf035a1ae5b6e96e979a-69bbef29\nFrom:
      sipp <sip:sipp@10.1.245.107:5060>;tag=5\nCall-ID: 5-22@10.1.245.107\nCSeq: 1
      OPTIONS\nServer: kamailio (5.3.3 (x86_64/linux))\nContent-Length: 0\n\n'.\nsipp:
      There were more errors, enable -trace_err to log them.\n"
    Stdout: "------------------------------ Scenario Screen -------- [1-9]: Change
      Screen --\n  Call-rate(length)   Port   Total-time  Total-calls  Remote-host\n
      \ 10.0(0 ms)/1.000s   5060       0.00 s            0  10.1.245.121:5060(UDP)\n\n
      \ 0 new calls during 0.000 s period      0 ms scheduler resolution\n  0 calls
      (limit 30)                     Peak was 0 calls, after 0 s\n  0 Running, 0 Paused,
      0 Woken up\n  0 dead call msg (discarded)            0 out-of-call msg (discarded)
      \       \n  3 open sockets                        \n\n                                 Messages
      \ Retrans   Timeout   Unexpected-Msg\n     OPTIONS ---------->         0         0
      \                           \n------ [+|-|*|/]: Adjust rate ---- [q]: Soft exit
      ---- [p]: Pause traffic -----\n\n------------------------------ Scenario Screen
      -------- [1-9]: Change Screen --\n  Call-rate(length)   Port   Total-time  Total-calls
      \ Remote-host\n  10.0(0 ms)/1.000s   5060       0.50 s            5  10.1.245.121:5060(UDP)\n\n
      \ Call limit reached (-m 5), 0.504 s period  1 ms scheduler resolution\n  0
      calls (limit 30)                     Peak was 1 calls, after 0 s\n  0 Running,
      6 Paused, 6 Woken up\n  5 dead call msg (discarded)            0 out-of-call
      msg (discarded)        \n  1 open sockets                        \n\n                                 Messages
      \ Retrans   Timeout   Unexpected-Msg\n     OPTIONS ---------->         5         0
      \                           \n------------------------------ Test Terminated
      --------------------------------\n\n\n------------------------------ Scenario
      Screen -------- [1-9]: Change Screen --\n  Call-rate(length)   Port   Total-time
      \ Total-calls  Remote-host\n  10.0(0 ms)/1.000s   5060       0.50 s            5
      \ 10.1.245.121:5060(UDP)\n\n  Call limit reached (-m 5), 0.000 s period  0 ms
      scheduler resolution\n  0 calls (limit 30)                     Peak was 1 calls,
      after 0 s\n  0 Running, 6 Paused, 0 Woken up\n  5 dead call msg (discarded)
      \           0 out-of-call msg (discarded)        \n  1 open sockets                        \n\n
      \                                Messages  Retrans   Timeout   Unexpected-Msg\n
      \    OPTIONS ---------->         5         0                            \n------------------------------
      Test Terminated --------------------------------\n\n\n-----------------------------
      Statistics Screen ------- [1-9]: Change Screen --\n  Start Time             |
      2022-01-20\t17:42:45.468682\t1642700565.468682         \n  Last Reset Time        |
      2022-01-20\t17:42:45.972974\t1642700565.972974         \n  Current Time           |
      2022-01-20\t17:42:45.972986\t1642700565.972986         \n-------------------------+---------------------------+--------------------------\n
      \ Counter Name           | Periodic value            | Cumulative value\n-------------------------+---------------------------+--------------------------\n
      \ Elapsed Time           | 00:00:00:000000           | 00:00:00:504000          \n
      \ Call Rate              |    0.000 cps              |    9.921 cps             \n-------------------------+---------------------------+--------------------------\n
      \ Incoming call created  |        0                  |        0                 \n
      \ OutGoing call created  |        0                  |        5                 \n
      \ Total Call created     |                           |        5                 \n
      \ Current Call           |        0                  |                          \n-------------------------+---------------------------+--------------------------\n
      \ Successful call        |        0                  |        5                 \n
      \ Failed call            |        0                  |        0                 \n-------------------------+---------------------------+--------------------------\n
      \ Call Length            | 00:00:00:000000           | 00:00:00:000000          \n------------------------------
      Test Terminated --------------------------------\n\n\n"
    output: Options action executed successfully
  status: completed
  timing:
    completed: 2022-01-20 17:42:46 +0000 UTC
    enqueued: 2022-01-20 17:42:45 +0000 UTC
    started: 2022-01-20 17:42:45 +0000 UTC```

## OCI Images

- sipp-image: grigiu/sipp:latest

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines 
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.
