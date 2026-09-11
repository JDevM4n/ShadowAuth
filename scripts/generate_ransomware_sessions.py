import getpass
import time
import paramiko


HOST = "192.168.2.27"
PORT = 2222
USER = "shadowauthlab"
COUNT = 12


SCENARIOS = [
    [
        "echo SHADOWAUTH_CONTROLLED_RANSOMWARE_V1",
        "whoami",
        "pwd",
        "uname -a",
        "ls -la /opt/banco-andino",
        "wget http://192.168.2.27:8080/ransomware-sim.sh -O /tmp/ransomware-sim.sh",
        "chmod +x /tmp/ransomware-sim.sh",
        "touch /tmp/clientes.csv",
        "touch /tmp/pagos.sql",
        "cp /tmp/clientes.csv /tmp/clientes.csv.locked",
        "cp /tmp/pagos.sql /tmp/pagos.sql.locked",
        "echo SIMULATED_RANSOM_NOTE",
        "touch /tmp/README_RESTORE_FILES.txt",
        "ls -la /tmp",
    ],
    [
        "echo SHADOWAUTH_CONTROLLED_RANSOMWARE_V1",
        "whoami",
        "pwd",
        "ls /opt/banco-andino",
        "curl http://192.168.2.27:8080/ransomware-sim.sh -o /tmp/ransomware-sim.sh",
        "chmod +x /tmp/ransomware-sim.sh",
        "touch /tmp/accounts.csv",
        "touch /tmp/transactions.sql",
        "cp /tmp/accounts.csv /tmp/accounts.csv.encrypted",
        "cp /tmp/transactions.sql /tmp/transactions.sql.encrypted",
        "echo RECOVER_FILES_SIMULATION",
        "touch /tmp/RECOVER_FILES.txt",
        "ls -la /tmp",
    ],
]


def run_session(password, commands):

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )

    client.connect(
        hostname=HOST,
        port=PORT,
        username=USER,
        password=password,
        allow_agent=False,
        look_for_keys=False,
        timeout=10,
    )

    channel = client.invoke_shell()

    time.sleep(0.8)

    for command in commands:

        if channel.closed:
            raise RuntimeError(
                f"Channel closed before: {command}"
            )

        print("     >", command)

        channel.send(command + "\n")

        time.sleep(0.5)

        if channel.recv_ready():
            channel.recv(16384)

    if not channel.closed:
        channel.send("exit\n")
        time.sleep(0.3)

    client.close()


def main():

    password = getpass.getpass(
        "Cowrie password: "
    )

    print("=" * 70)
    print("CONTROLLED RANSOMWARE")
    print("=" * 70)

    successful = 0
    failed = 0

    for i in range(COUNT):

        print(
            f"\n[{i + 1}/{COUNT}] "
            "CONTROLLED RANSOMWARE"
        )

        scenario = SCENARIOS[
            i % len(SCENARIOS)
        ]

        try:

            run_session(
                password,
                scenario,
            )

            successful += 1
            print("  ✅ OK")

        except Exception as exc:

            failed += 1
            print(
                "  ❌ ERROR:",
                exc,
            )

        time.sleep(0.7)

    print()
    print("=" * 70)
    print("FINISHED")
    print("=" * 70)
    print("Successful:", successful)
    print("Failed    :", failed)


if __name__ == "__main__":
    main()
