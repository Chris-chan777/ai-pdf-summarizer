"""Windows development launcher for AI PDF Summarizer."""

import csv
import io
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 5000


def listener_pids():
    result = subprocess.run(
        ["netstat", "-ano", "-p", "tcp"],
        capture_output=True,
        text=True,
        check=True,
    )
    pids = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5:
            local_port = parts[1].rsplit(":", 1)[-1]
            if parts[3].upper() == "LISTENING" and local_port == str(PORT):
                if parts[4].isdigit():
                    pids.add(int(parts[4]))
    return pids


def process_name(pid):
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=True,
    )
    rows = list(csv.reader(io.StringIO(result.stdout.strip())))
    return rows[0][0].lower() if rows and rows[0] else ""


def stop_old_server():
    pids = listener_pids()
    if not pids:
        print("[1/3] 已关闭旧进程：未发现占用 5000 端口的服务。")
        return

    for pid in sorted(pids):
        name = process_name(pid)
        if not name.startswith(("python", "pythonw", "flask")):
            raise RuntimeError(
                f"端口 {PORT} 被非 Python 进程占用："
                f"{name or '未知进程'} (PID {pid})。"
            )
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"[1/3] 已关闭旧进程：{name} (PID {pid})。")

    deadline = time.time() + 5
    while listener_pids() and time.time() < deadline:
        time.sleep(0.2)
    if listener_pids():
        raise RuntimeError(f"端口 {PORT} 未能及时释放。")


def install_dependencies():
    print("[2/3] 正在安装依赖……")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=ROOT,
        check=True,
    )
    print("[2/3] 已安装依赖。")


def start_flask():
    environment = os.environ.copy()
    environment.setdefault("FLASK_DEBUG", "true")
    print("[3/3] 服务启动地址 http://127.0.0.1:5000")
    subprocess.run(
        [sys.executable, "run.py"],
        cwd=ROOT,
        env=environment,
        check=True,
    )


def main():
    if platform.system() != "Windows":
        raise RuntimeError("run_dev.py 仅支持 Windows。")
    try:
        stop_old_server()
        install_dependencies()
        start_flask()
    except KeyboardInterrupt:
        print("\n开发服务器已停止。")
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        print(f"启动失败：{error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
