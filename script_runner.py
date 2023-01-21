import subprocess
import sys
import os

AIO_PIKA_PACKAGE = "aio_pika"
AMQP_API_CLIENT_PACKAGE = "amqp_api_client_py"
COOPLAN_INTEGRATION_TEST_BOILERPLATE_PACKAGE = "cooplan_integration_test_boilerplate"
GIT_PACKAGE = "GitPython"
MONGODB_PACKAGE = "pymongo[srv]"


def main():
    if len(sys.argv) != 3:
        print('usage script_runner.py: <integration tests path> <api token>')
        exit(1)

    install_dependencies()
    if not run_all_test_scripts(sys.argv[1], sys.argv[2]):
        exit(1)


def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           AIO_PIKA_PACKAGE,
                           AMQP_API_CLIENT_PACKAGE,
                           COOPLAN_INTEGRATION_TEST_BOILERPLATE_PACKAGE,
                           GIT_PACKAGE,
                           MONGODB_PACKAGE])


def run_all_test_scripts(directory, api_token) -> bool:
    test_processes = {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(root, filename)
            test_processes[filepath] = subprocess.Popen(["python3", filepath, api_token],
                                                        stdout=sys.stdout,
                                                        stderr=sys.stderr)

    is_all_ok = True
    for filepath in test_processes:
        process = test_processes[filepath]

        result_code = 0
        if process.poll() is None:
            result_code = process.wait()
        else:
            result_code = process.returncode

        if result_code == 0:
            print(f"[OK] {filepath}")
        else:
            is_all_ok = False
            print(f"[FAIL] {filepath}")

    return is_all_ok


if __name__ == "__main__":
    main()
